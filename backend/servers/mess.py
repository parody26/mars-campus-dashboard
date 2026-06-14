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
    return {"source": "cafeteria", "data": {
        "sunday": {
            "breakfast": ["Poha", "Jalebi", "Chai", "Milk"],
            "lunch": ["Dal Makhani", "Paneer Butter Masala", "Rice", "Roti", "Raita"],
            "dinner": ["Shahi Paneer", "Naan", "Rice", "Gulab Jamun"]
        },
        "monday": {
            "breakfast": ["Idli", "Sambar", "Coconut Chutney", "Chai"],
            "lunch": ["Rajma", "Rice", "Mix Veg", "Roti", "Curd"],
            "dinner": ["Kadai Paneer", "Dal Fry", "Rice", "Roti", "Kheer"]
        },
        "tuesday": {
            "breakfast": ["Aloo Paratha", "Curd", "Pickle", "Chai"],
            "lunch": ["Chole", "Bhature", "Rice", "Salad", "Lassi"],
            "dinner": ["Matar Paneer", "Dal Tadka", "Rice", "Roti"]
        },
        "wednesday": {
            "breakfast": ["Upma", "Coconut Chutney", "Boiled Eggs", "Chai"],
            "lunch": ["Dal Makhani", "Aloo Gobi", "Rice", "Roti", "Raita"],
            "dinner": ["Paneer Tikka Masala", "Dal", "Rice", "Naan"]
        },
        "thursday": {
            "breakfast": ["Puri", "Aloo Sabzi", "Chai"],
            "lunch": ["Sambar Rice", "Rasam", "Papad", "Curd"],
            "dinner": ["Palak Paneer", "Dal Fry", "Rice", "Roti"]
        },
        "friday": {
            "breakfast": ["Bread Omelette", "Cornflakes", "Milk", "Juice"],
            "lunch": ["Biryani", "Raita", "Salan", "Salad"],
            "dinner": ["Paneer Butter Masala", "Dal", "Rice", "Naan"]
        },
        "saturday": {
            "breakfast": ["Aloo Paratha", "Curd", "Chai"],
            "lunch": ["Kadhi Chawal", "Mix Veg", "Roti", "Papad"],
            "dinner": ["Special Thali", "Dal", "Sabzi", "Rice", "Roti", "Sweet"]
        }
    }}

@app.get("/cafeteria/timings")
def get_timings():
    return {"source": "cafeteria", "data": {
        "breakfast": "7:30 AM - 9:30 AM",
        "lunch": "12:00 PM - 2:30 PM",
        "evening_snacks": "4:30 PM - 6:00 PM",
        "dinner": "7:30 PM - 9:30 PM"
    }}