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
        max_tokens=20
    )
    
    if not response.choices or response.choices[0].message.content is None:
        return "library|/library/hours"
    
    return response.choices[0].message.content.strip()

def fetch_data(server_name: str, endpoint: str):
    port = SERVERS[server_name]["port"]
    url = f"http://localhost:{port}{endpoint}"
    try:
        response = requests.get(url, timeout=5)
        return response.json()
    except Exception as e:
        return {"error": f"Could not reach {server_name} server: {str(e)}"}

def generate_answer(question: str, data: dict):
    prompt = f"""You are a helpful campus assistant. A student asked: "{question}"
Here is the data: {data}
Give a friendly answer in 2-3 sentences based only on this data."""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    
    if not response.choices or response.choices[0].message.content is None:
        return "I found the information but couldn't generate a response. Please try again."
    
    return response.choices[0].message.content.strip()

def answer_question(question: str):
    routing = decide_server(question)
    try:
        server_name, endpoint = routing.split("|")
        server_name = server_name.strip()
        endpoint = endpoint.strip()
    except:
        return {"answer": "Sorry, I couldn't understand which campus service to check.", "server_used": "none", "endpoint_used": "none"}
    data = fetch_data(server_name, endpoint)
    answer = generate_answer(question, data)
    return {"answer": answer, "server_used": server_name, "endpoint_used": endpoint, "raw_data": data}

