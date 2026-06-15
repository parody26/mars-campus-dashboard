# 🎓 MARS Campus Intelligence Dashboard

A Unified Campus Intelligence Dashboard with an AI Assistant built for MARS Open Projects 2026.
## 📸 Demo
Live Demo: [https://your-vercel-url.vercel.app](https://mars-campus-dashboard-junv.vercel.app/)
## 💻 Backend
Backend: https://mars-campus-backend.onrender.com

## 🚀 Features
- 4 independent MCP servers for different campus data sources
- AI Assistant that routes natural language queries to the correct server in real-time
- Live dashboard showing Library Hours, Mess Menu, Events, and Exam Schedule
- No single database — data is fetched live from each MCP server

## 🛠️ Tech Stack
- **Frontend:** React.js
- **Backend:** Python FastAPI
- **AI:** OpenRouter API
- **MCP Servers:** 4 independent FastAPI servers

## 📡 MCP Servers
| Server | Port | Data |
|--------|------|------|
| Library | 8001 | Hours, Books |
| Mess | 8002 | Menu, Timings |
| Events | 8003 | Events, Clubs |
| Academics | 8004 | Exams, Holidays |

## ⚙️ Setup Instructions

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Start all servers:
```bash
uvicorn servers.library:app --reload --port 8001
uvicorn servers.mess:app --reload --port 8002
uvicorn servers.events:app --reload --port 8003
uvicorn servers.academics:app --reload --port 8004
uvicorn main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm start
```

### Environment Variables
Create `backend/.env`:
OPENROUTER_API_KEY=your_key_here
