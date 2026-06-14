from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_router import answer_question

app = FastAPI()

# This allows your React frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class Question(BaseModel):
    question: str

@app.get("/")
def root():
    return {"status": "Campus AI Assistant is running"}

@app.post("/ask")
def ask(q: Question):
    result = answer_question(q.question)
    return result