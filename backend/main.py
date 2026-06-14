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
    return {"source": "library", "data": {
        "name": "James Thomason Library (JTL), IIT Roorkee",
        "monday_to_friday": "8:00 AM - 12:00 AM (Midnight)",
        "saturday": "9:00 AM - 10:00 PM",
        "sunday": "10:00 AM - 6:00 PM",
        "note": "Reading Room open 24x7 during exam season"
    }}

@app.get("/library/books")
def get_books():
    return {"source": "library", "data": [
        {"title": "Engineering Mathematics by B.S. Grewal", "available": True},
        {"title": "Signals and Systems by Oppenheim", "available": False},
        {"title": "Data Structures by Cormen (CLRS)", "available": True},
        {"title": "Fluid Mechanics by Frank White", "available": True},
        {"title": "Computer Networks by Tanenbaum", "available": False}
    ]}

# ---- Mess routes ----
@app.get("/cafeteria/menu")
def get_menu():
    return {"source": "cafeteria", "data": {
        "sunday": {
            "breakfast": ["Poha", "Jalebi", "Chai", "Milk"],
            "lunch": ["Dal Makhani", "Paneer Butter Masala", "Rice", "Roti", "Raita", "Salad"],
            "dinner": ["Shahi Paneer", "Naan", "Rice", "Dal Tadka", "Gulab Jamun"]
        },
        "monday": {
            "breakfast": ["Idli", "Sambar", "Coconut Chutney", "Chai", "Milk"],
            "lunch": ["Rajma", "Rice", "Mix Veg", "Roti", "Curd", "Salad"],
            "dinner": ["Kadai Paneer", "Dal Fry", "Rice", "Roti", "Kheer"]
        },
        "tuesday": {
            "breakfast": ["Aloo Paratha", "Curd", "Pickle", "Chai", "Milk"],
            "lunch": ["Chole", "Bhature", "Rice", "Salad", "Lassi"],
            "dinner": ["Matar Paneer", "Dal Tadka", "Rice", "Roti", "Ice Cream"]
        },
        "wednesday": {
            "breakfast": ["Upma", "Coconut Chutney", "Boiled Eggs", "Chai", "Milk"],
            "lunch": ["Dal Makhani", "Aloo Gobi", "Rice", "Roti", "Raita"],
            "dinner": ["Paneer Tikka Masala", "Dal", "Rice", "Naan", "Halwa"]
        },
        "thursday": {
            "breakfast": ["Puri", "Aloo Sabzi", "Chai", "Milk"],
            "lunch": ["Sambar Rice", "Rasam", "Papad", "Curd", "Salad"],
            "dinner": ["Palak Paneer", "Dal Fry", "Rice", "Roti", "Rasgulla"]
        },
        "friday": {
            "breakfast": ["Bread Omelette", "Cornflakes", "Milk", "Juice"],
            "lunch": ["Biryani", "Raita", "Salan", "Salad", "Cold Drink"],
            "dinner": ["Paneer Butter Masala", "Dal", "Rice", "Naan", "Fruit Custard"]
        },
        "saturday": {
            "breakfast": ["Chole Bhature", "Chai", "Milk"],
            "lunch": ["Kadhi Chawal", "Mix Veg", "Roti", "Papad", "Pickle"],
            "dinner": ["Special Thali — Dal, Sabzi, Rice, Roti, Sweet, Papad, Pickle"]
        }
    }}

@app.get("/cafeteria/timings")
def get_timings():
    return {"source": "cafeteria", "data": {
        "breakfast": "7:30 AM - 9:30 AM",
        "lunch": "12:00 PM - 2:30 PM",
        "evening_snacks": "4:30 PM - 6:00 PM",
        "dinner": "7:30 PM - 9:30 PM",
        "note": "Timings for all hostels at IIT Roorkee"
    }}

# ---- Events routes ----
@app.get("/events/upcoming")
def get_events():
    return {"source": "events", "data": [
        {
            "name": "Cognizance 2026 — Annual Tech Fest",
            "date": "June 20, 2026",
            "venue": "IIT Roorkee Campus",
            "time": "9:00 AM",
            "description": "Asia's largest student-run technical festival"
        },
        {
            "name": "AI & ML Workshop by IITR ACM",
            "date": "June 22, 2026",
            "venue": "CSE Department, Lab 3",
            "time": "2:00 PM",
            "description": "Hands-on workshop on deep learning and LLMs"
        },
        {
            "name": "Thomso 2026 — Cultural Fest",
            "date": "June 25, 2026",
            "venue": "Convocation Hall & Open Air Theatre",
            "time": "5:00 PM",
            "description": "IIT Roorkee's annual cultural extravaganza"
        },
        {
            "name": "Inter-IIT Sports Meet Trials",
            "date": "June 28, 2026",
            "venue": "Sports Complex, IITR",
            "time": "6:00 AM",
            "description": "Selection trials for Inter-IIT Sports Meet 2026"
        },
        {
            "name": "Entrepreneurship Summit by E-Cell IITR",
            "date": "July 2, 2026",
            "venue": "Lecture Hall Complex",
            "time": "10:00 AM",
            "description": "Startup pitches, investor talks, and networking"
        }
    ]}

@app.get("/events/clubs")
def get_clubs():
    return {"source": "events", "data": [
        {"club": "IITR ACM Student Chapter", "meeting": "Every Saturday, 4 PM, CSE Dept"},
        {"club": "Robotics Club (RoboIITR)", "meeting": "Every Wednesday, 5 PM, Hobbies Club"},
        {"club": "Photography Club (Aperture)", "meeting": "Every Sunday, 3 PM, SAC Building"},
        {"club": "Coding Club (IITR)", "meeting": "Every Tuesday, 6 PM, CC Lab"},
        {"club": "Music Club (Swaranjali)", "meeting": "Every Friday, 5 PM, Cultural Hall"},
        {"club": "NSS IIT Roorkee", "meeting": "Every Sunday, 9 AM, Civil Dept"}
    ]}

# ---- Academics routes ----
@app.get("/academics/exams")
def get_exams():
    return {"source": "academics", "data": [
        {"subject": "Engineering Mathematics - II", "date": "July 1, 2026", "time": "9:00 AM", "venue": "Examination Hall 1"},
        {"subject": "Data Structures & Algorithms", "date": "July 3, 2026", "time": "9:00 AM", "venue": "CSE Block"},
        {"subject": "Thermodynamics", "date": "July 5, 2026", "time": "2:00 PM", "venue": "ME Department"},
        {"subject": "Signals & Systems", "date": "July 7, 2026", "time": "9:00 AM", "venue": "ECE Block"},
        {"subject": "Engineering Drawing", "date": "July 9, 2026", "time": "2:00 PM", "venue": "Drawing Hall"}
    ]}

@app.get("/academics/holidays")
def get_holidays():
    return {"source": "academics", "data": [
        {"holiday": "Independence Day", "date": "August 15, 2026"},
        {"holiday": "Mid Semester Break", "date": "September 20-27, 2026"},
        {"holiday": "Diwali Vacation", "date": "October 18-24, 2026"},
        {"holiday": "End Semester Break", "date": "November 25 - December 5, 2026"},
        {"holiday": "Winter Vacation", "date": "December 25, 2026 - January 3, 2027"}
    ]}

@app.get("/academics/departments")
def get_departments():
    return {"source": "academics", "data": [
        {"dept": "Computer Science & Engineering", "hod": "Prof. R.C. Joshi", "location": "CSE Block"},
        {"dept": "Electrical Engineering", "hod": "Prof. S.K. Singh", "location": "EE Block"},
        {"dept": "Mechanical Engineering", "hod": "Prof. A.K. Sharma", "location": "ME Block"},
        {"dept": "Civil Engineering", "hod": "Prof. M.L. Sharma", "location": "Civil Block"},
        {"dept": "Electronics & Communication", "hod": "Prof. D.K. Upadhyay", "location": "ECE Block"}
    ]}

# ---- AI route ----
@app.post("/ask")
def ask(q: Question):
    result = answer_question(q.question)
    return result