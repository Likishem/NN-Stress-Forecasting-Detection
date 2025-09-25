from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI(title="Basic Chat API")

class ChatMessage(BaseModel):
    user: str
    message: str

def simple_bot_reply(msg: str) -> str:
    """
    Very basic logic. Replace this with an LLM call (e.g., OpenAI) later.
    """
    text = msg.lower()
    if "hello" in text or "hi" in text:
        return "Hello! how can i help you today?"
    elif "" in text:
        return ""
    elif "" in text:
        return ""
    else:
        return f"You said: {msg}"

@app.post("/chat")
async def chat(message: ChatMessage):
    reply = simple_bot_reply(message.message)
    return {
        "user": message.user,
        "bot_reply": reply
    }
