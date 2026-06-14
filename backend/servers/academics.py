from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/academics/exams")
def get_exams():
    return {
        "source": "academics",
        "data": [
            {"subject": "Mathematics", "date": "July 1, 2026", "time": "9:00 AM"},
            {"subject": "Physics", "date": "July 3, 2026", "time": "9:00 AM"},
            {"subject": "Computer Science", "date": "July 5, 2026", "time": "2:00 PM"}
        ]
    }

@app.get("/academics/holidays")
def get_holidays():
    return {
        "source": "academics",
        "data": [
            {"holiday": "Independence Day", "date": "August 15, 2026"},
            {"holiday": "Diwali Break", "date": "October 20-24, 2026"},
            {"holiday": "Winter Break", "date": "December 25 - January 1"}
        ]
    }