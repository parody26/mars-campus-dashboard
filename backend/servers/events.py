from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/events/upcoming")
def get_events():
    return {
        "source": "events",
        "data": [
            {"name": "Tech Fest 2026", "date": "June 20, 2026", "venue": "Main Auditorium", "time": "10:00 AM"},
            {"name": "AI Workshop", "date": "June 22, 2026", "venue": "Lab Block 3", "time": "2:00 PM"},
            {"name": "Cultural Night", "date": "June 25, 2026", "venue": "Open Air Theatre", "time": "6:00 PM"}
        ]
    }

@app.get("/events/clubs")
def get_clubs():
    return {
        "source": "events",
        "data": [
            {"club": "MARS Robotics", "meeting": "Every Saturday, 4 PM"},
            {"club": "Coding Club", "meeting": "Every Wednesday, 5 PM"},
            {"club": "Photography Club", "meeting": "Every Sunday, 3 PM"}
        ]
    }