# app/stream_simulator.py
import random
import json
import time
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler # type: ignore
from datetime import datetime
from .db import SessionLocal, RawData, encrypt_bytes, UserHistory
from typing import Callable

scheduler = AsyncIOScheduler()

def generate_sample_payload():
    return {
        "heart_rate": round(random.normalvariate(72, 8), 1),
        "sleep_hours": round(random.normalvariate(7, 1.2), 1),
        "workload_score": round(random.uniform(0, 10), 1),
        "timestamp": datetime.utcnow().isoformat()
    }

def save_payload(payload: dict):
    db = SessionLocal()
    try:
        raw = json.dumps(payload).encode()
        enc = encrypt_bytes(raw)
        r = RawData(encrypted_payload=enc.decode())
        db.add(r)
        db.commit()
    finally:
        db.close()

# schedule job; callback is function(payload) used to notify live clients
def start_streaming(callback=None, interval_seconds=5):
    def job():
        payload = generate_sample_payload()
        save_payload(payload)
        if callback:
            # If callback is async or sync, call accordingly
            try:
                if asyncio.iscoroutinefunction(callback):
                    asyncio.create_task(callback(payload))
                else:
                    callback(payload)
            except Exception:
                pass
    scheduler.add_job(job, "interval", seconds=interval_seconds, id="stream_job")
    scheduler.start()
