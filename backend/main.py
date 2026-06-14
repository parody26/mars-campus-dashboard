from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from ai_router import answer_question

app = FastAPI()

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

# ---- Library routes ----
@app.get("/library/hours")
def get_hours():
    return {"source": "library", "data": {"monday_to_friday": "8:00 AM - 10:00 PM", "saturday": "9:00 AM - 6:00 PM", "sunday": "Closed"}}

@app.get("/library/books")
def get_books():
    return {"source": "library", "data": [
        {"title": "Introduction to Algorithms", "available": True},
        {"title": "Clean Code", "available": False},
        {"title": "The Pragmatic Programmer", "available": True}
    ]}

# ---- Mess routes ----
@app.get("/cafeteria/menu")
def get_menu():
    return {"source": "cafeteria", "data": {
        "monday": ["Pasta", "Salad", "Juice"],
        "tuesday": ["Rice & Dal", "Roti", "Lassi"],
        "wednesday": ["Burger", "Fries", "Cold Drink"],
        "thursday": ["Paneer Curry", "Naan", "Buttermilk"],
        "friday": ["Pizza", "Garlic Bread", "Lemonade"]
    }}

@app.get("/cafeteria/timings")
def get_timings():
    return {"source": "cafeteria", "data": {"breakfast": "7:30 AM - 9:30 AM", "lunch": "12:00 PM - 2:30 PM", "dinner": "7:00 PM - 9:30 PM"}}

# ---- Events routes ----
@app.get("/events/upcoming")
def get_events():
    return {"source": "events", "data": [
        {"name": "Tech Fest 2026", "date": "June 20, 2026", "venue": "Main Auditorium", "time": "10:00 AM"},
        {"name": "AI Workshop", "date": "June 22, 2026", "venue": "Lab Block 3", "time": "2:00 PM"},
        {"name": "Cultural Night", "date": "June 25, 2026", "venue": "Open Air Theatre", "time": "6:00 PM"}
    ]}

@app.get("/events/clubs")
def get_clubs():
    return {"source": "events", "data": [
        {"club": "MARS Robotics", "meeting": "Every Saturday, 4 PM"},
        {"club": "Coding Club", "meeting": "Every Wednesday, 5 PM"},
        {"club": "Photography Club", "meeting": "Every Sunday, 3 PM"}
    ]}

# ---- Academics routes ----
@app.get("/academics/exams")
def get_exams():
    return {"source": "academics", "data": [
        {"subject": "Mathematics", "date": "July 1, 2026", "time": "9:00 AM"},
        {"subject": "Physics", "date": "July 3, 2026", "time": "9:00 AM"},
        {"subject": "Computer Science", "date": "July 5, 2026", "time": "2:00 PM"}
    ]}

@app.get("/academics/holidays")
def get_holidays():
    return {"source": "academics", "data": [
        {"holiday": "Independence Day", "date": "August 15, 2026"},
        {"holiday": "Diwali Break", "date": "October 20-24, 2026"},
        {"holiday": "Winter Break", "date": "December 25 - January 1"}
    ]}

# ---- AI route ----
@app.post("/ask")
def ask(q: Question):
    result = answer_question(q.question)
    return result