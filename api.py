from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from rag import ask

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_methods=["*"], allow_headers=["*"])

class Question(BaseModel):
    question: str

import os
from helpdesk_vuln import ask_vuln

BOT_MODE = os.getenv("BOT_MODE", "vuln")

@app.post("/chat")
def chat(body: Question):
    if BOT_MODE == "vuln":
        return {"answer": ask_vuln(body.question)}
    return {"answer": ask(body.question)}

@app.post("/chat")
def chat(body: Question):
    return {"answer": ask(body.question)}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/")
def home():
    return FileResponse("widget.html")

