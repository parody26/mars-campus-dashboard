from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/cafeteria/menu")
def get_menu():
    return {
        "source": "cafeteria",
        "data": {
            "monday": ["Pasta", "Salad", "Juice"],
            "tuesday": ["Rice & Dal", "Roti", "Lassi"],
            "wednesday": ["Burger", "Fries", "Cold Drink"],
            "thursday": ["Paneer Curry", "Naan", "Buttermilk"],
            "friday": ["Pizza", "Garlic Bread", "Lemonade"]
        }
    }

@app.get("/cafeteria/timings")
def get_timings():
    return {
        "source": "cafeteria",
        "data": {
            "breakfast": "7:30 AM - 9:30 AM",
            "lunch": "12:00 PM - 2:30 PM",
            "dinner": "7:00 PM - 9:30 PM"
        }
    }