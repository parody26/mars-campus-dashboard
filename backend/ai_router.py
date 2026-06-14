import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENROUTER_API_KEY"),
    base_url="https://openrouter.ai/api/v1"
)

MODEL = "poolside/laguna-m.1:free"
SERVERS = {
    "library": {"port": 8001, "endpoints": ["/library/hours", "/library/books"], "description": "library hours, book availability"},
    "mess": {"port": 8002, "endpoints": ["/cafeteria/menu", "/cafeteria/timings"], "description": "mess menu, cafeteria food, meal timings"},
    "events": {"port": 8003, "endpoints": ["/events/upcoming", "/events/clubs"], "description": "college events, workshops, clubs, fests"},
    "academics": {"port": 8004, "endpoints": ["/academics/exams", "/academics/holidays"], "description": "exam schedule, holidays, academic calendar"}
}

def decide_server(question: str):
    prompt = f"""You are a campus assistant router. Based on the student's question, decide which server and endpoint to call.

Available servers:
- library: {SERVERS['library']['description']}, endpoints: {SERVERS['library']['endpoints']}
- mess: {SERVERS['mess']['description']}, endpoints: {SERVERS['mess']['endpoints']}
- events: {SERVERS['events']['description']}, endpoints: {SERVERS['events']['endpoints']}
- academics: {SERVERS['academics']['description']}, endpoints: {SERVERS['academics']['endpoints']}

Student question: "{question}"

Reply with ONLY this format, nothing else: SERVER_NAME|/endpoint/path
Example: library|/library/hours"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=300
    )
    
    if not response.choices or response.choices[0].message.content is None:
        return "library|/library/hours"
    
    return response.choices[0].message.content.strip()

def fetch_data(server_name: str, endpoint: str):
    # On hosted environment, call our own main server endpoints
    base_url = os.getenv("BASE_URL", "http://localhost:8000")
    url = f"{base_url}{endpoint}"
    try:
        response = requests.get(url, timeout=10)
        return response.json()
    except Exception as e:
        return {"error": f"Could not fetch data: {str(e)}"}

def generate_answer(question: str, data: dict, server_name: str):
    from datetime import datetime
    today = datetime.now().strftime("%A, %B %d, %Y")
    
    prompt = f"""You are a campus assistant. Today is {today}.
Question: "{question}"
Data: {data}
Answer in 2-3 sentences. Be specific. If asked about "this week" or "today", only mention relevant items based on today's date."""

    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=500
        )
        if response.choices and response.choices[0].message.content:
            return response.choices[0].message.content.strip()
    except:
        pass

    # Fallback
    if server_name == "library":
        d = data.get("data", {})
        if isinstance(d, dict):
            hours = ", ".join([f"{k.replace('_',' ')}: {v}" for k,v in d.items()])
            return f"The library is open: {hours}."
    elif server_name == "mess":
        d = data.get("data", {})
        today_name = datetime.now().strftime("%A").lower()
        if today_name in d:
            menu = d[today_name]
            return f"Today's mess menu: {menu}"
        return "Mess menu retrieved successfully."
    elif server_name == "events":
        d = data.get("data", [])
        if isinstance(d, list) and len(d) > 0:
            names = ", ".join([e.get("name","") for e in d[:3]])
            return f"Upcoming events: {names}."
    elif server_name == "academics":
        d = data.get("data", [])
        if isinstance(d, list) and len(d) > 0:
            exams = ", ".join([f"{e.get('subject','')} on {e.get('date','')}" for e in d])
            return f"Upcoming exams: {exams}."
    return "I found the information! Check the dashboard cards for details."
def answer_question(question: str):
    routing = decide_server(question)
    try:
        server_name, endpoint = routing.split("|")
        server_name = server_name.strip()
        endpoint = endpoint.strip()
    except:
        return {"answer": "Sorry, I couldn't understand which campus service to check.", "server_used": "none", "endpoint_used": "none"}
    
    data = fetch_data(server_name, endpoint)
    answer = generate_answer(question, data, server_name)
    return {"answer": answer, "server_used": server_name, "endpoint_used": endpoint, "raw_data": data}