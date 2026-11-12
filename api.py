from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from rag import ask

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

class Message(BaseModel):
    message: str

import os
from helpdesk_vuln import ask_vuln

BOT_MODE = os.getenv("BOT_MODE", "vuln")

@app.post("/chat")
def chat(body: Message):
    if BOT_MODE == "vuln":
        return {"reply": ask_vuln(body.message)}
    return {"reply": ask(body.message)}

@app.post("/chat")
def chat(body: Message):
    return {"reply": ask(body.message)}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def home():
    return FileResponse("widget.html")

