from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/library/hours")
def get_hours():
    return {
        "source": "library",
        "data": {
            "monday_to_friday": "8:00 AM - 10:00 PM",
            "saturday": "9:00 AM - 6:00 PM",
            "sunday": "Closed"
        }
    }

@app.get("/library/books")
def search_books():
    return {
        "source": "library",
        "data": [
            {"title": "Introduction to Algorithms", "available": True},
            {"title": "Clean Code", "available": False},
            {"title": "The Pragmatic Programmer", "available": True}
        ]
    }