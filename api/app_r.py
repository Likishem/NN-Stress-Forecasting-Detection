# app/main.py
from fastapi import FastAPI
import os
import json
from typing import List
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import joblib
from .db import init_db, SessionLocal, encrypt_bytes, decrypt_bytes, RawData, UserHistory
from .recommender import recommend_for_user
from .stream_simulator import start_streaming, save_payload
from sqlalchemy.orm import Session
import asyncio

MODEL_PATH = os.environ.get("MODEL_PATH", "models/stress_model.joblib")
FERNET_KEY = os.environ.get("FERNET_KEY")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")  # optional webhook to call on warnings

app = FastAPI(title="Stress Forecasting & Recommender API")

# in-memory WebSocket manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.active_connections:
            self.active_connections.remove(ws)

    async def broadcast(self, message: dict):
        for conn in list(self.active_connections):
            try:
                await conn.send_json(message)
            except Exception:
                self.disconnect(conn)

manager = ConnectionManager()

# pydantic models
class PredictInput(BaseModel):
    heart_rate: float
    sleep_hours: float
    workload_score: float
    user_id: str = None

class EventInput(BaseModel):
    user_id: str
    event: dict

# init db and load model
@app.on_event("startup")
async def startup_event():
    init_db()
    global model
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
    else:
        model = None  # model can be trained later
    # start simulator with callback to websocket broadcast
    start_streaming(callback=notify_clients, interval_seconds=int(os.environ.get("STREAM_INTERVAL", 5)))

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def notify_clients(payload):
    # Basic rule: if heart_rate > 100 or workload > 9 → warning
    if payload.get("heart_rate", 0) > 100 or payload.get("workload_score", 0) >= 9.5:
        message = {"type": "warning", "payload": payload}
        # broadcast on websocket
        await manager.broadcast(message)
        # optional: call external webhook (async)
        if WEBHOOK_URL:
            import httpx
            try:
                await httpx.post(WEBHOOK_URL, json=message, timeout=5.0)
            except Exception:
                pass

@app.post("/predict")
async def predict(data: PredictInput, db: Session = Depends(get_db)):
    features = [[data.heart_rate, data.sleep_hours, data.workload_score]]
    if model is None:
        return JSONResponse({"error":"Model not available. Train or provide MODEL_PATH."}, status_code=503)
    pred = model.predict(features)[0]
    # persist raw input (encrypted)
    raw = {"features": features[0], "predicted": float(pred)}
    enc = encrypt_bytes(json.dumps(raw).encode())
    entry = RawData(encrypted_payload=enc.decode())
    db.add(entry)
    db.commit()
    return {"stress_score": float(pred)}

@app.post("/history")
def add_history(event: EventInput, db: Session = Depends(get_db)):
    enc = encrypt_bytes(json.dumps(event.event).encode())
    row = UserHistory(user_id=event.user_id, encrypted_event=enc.decode())
    db.add(row)
    db.commit()
    return {"status":"ok"}

@app.get("/history/{user_id}")
def get_history(user_id: str, db: Session = Depends(get_db)):
    rows = db.query(UserHistory).filter(UserHistory.user_id==user_id).all()
    out = []
    for r in rows:
        try:
            dec = decrypt_bytes(r.encrypted_event.encode())
            out.append(json.loads(dec.decode()))
        except Exception:
            continue
    return out

@app.get("/recommend/{user_id}")
def recommend(user_id: str, db: Session = Depends(get_db)):
    recs = recommend_for_user(db, user_id, top_n=5)
    return {"user_id": user_id, "recommendations": recs}

@app.websocket("/ws/notifications")
async def websocket_endpoint(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            msg = await ws.receive_text()
            # echo or accept commands
            await ws.send_text(f"Server received: {msg}")
    except WebSocketDisconnect:
        manager.disconnect(ws)

@app.post("/admin/save_payload")
def api_save_payload(payload: dict, db: Session = Depends(get_db)):
    # allow external ingestion
    enc = encrypt_bytes(json.dumps(payload).encode())
    row = RawData(encrypted_payload=enc.decode())
    db.add(row)
    db.commit()
    return {"saved": True}
