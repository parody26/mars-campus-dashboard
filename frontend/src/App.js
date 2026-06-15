import { useState, useEffect } from "react";
import axios from "axios";
import "./App.css";

const API = "https://mars-campus-backend.onrender.com";function App() {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [dashboardData, setDashboardData] = useState({});
  const [activeCard, setActiveCard] = useState(null);
  const [typed, setTyped] = useState("");
  const [backendLoading, setBackendLoading] = useState(true);

  const heroText = "Your Campus, Unified.";

  const [typingDone, setTypingDone] = useState(false);

  useEffect(() => {
    let i = 0;
    const interval = setInterval(() => {
      setTyped(heroText.slice(0, i));
      i++;
      if (i > heroText.length) {
        clearInterval(interval);
        setTypingDone(true);
      }
    }, 60);
    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
  setBackendLoading(true);
  try {
    const [library, mess, events, academics] = await Promise.all([
      axios.get(`${API}/library/hours`),
      axios.get(`${API}/cafeteria/menu`),
      axios.get(`${API}/events/upcoming`),
      axios.get(`${API}/academics/exams`),
    ]);
    setDashboardData({
      library: library.data.data,
      mess: mess.data.data,
      events: events.data.data,
      academics: academics.data.data,
    });
  } catch (err) {
    console.error("Dashboard fetch error:", err);
  }
  setBackendLoading(false);
};

  const askQuestion = async () => {
    if (!question.trim()) return;
    const userMsg = { role: "user", text: question };
    setMessages((prev) => [...prev, userMsg]);
    setQuestion("");
    setLoading(true);
    try {
      const res = await axios.post(`${API}/ask`, { question });
      const botMsg = {
        role: "bot",
        text: res.data.answer,
        server: res.data.server_used,
      };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "bot", text: "Sorry, something went wrong. Please try again." },
      ]);
    }
    setLoading(false);
  };

  const handleKey = (e) => {
    if (e.key === "Enter") askQuestion();
  };

  const quickQuestions = [
    "What time does library close?",
    "What's for lunch today?",
    "Any events this week?",
    "When is the CS exam?",
  ];
  if (backendLoading) {
    return (
      <div className="app">
        <div className="blob blob1" />
        <div className="blob blob2" />
        <div className="blob blob3" />
        <div className="loading-screen">
          <div className="spinner" />
          <p className="loading-msg">Connecting to campus servers...</p>
          <p className="loading-sub">This may take up to 50 seconds on first load</p>
        </div>
      </div>
    );
  }

  
  return (
    <div className="app">
      {/* Animated background blobs */}
      <div className="blob blob1" />
      <div className="blob blob2" />
      <div className="blob blob3" />

      <header className="header">
        <div className="header-badge">🚀 MARS — Models & Robotics Section</div>
        <h1 className="hero-title">
          {typed}
          {!typingDone && <span className="cursor">|</span>}
        </h1>
        <p className="hero-sub">
          Ask anything. Get instant answers from live campus systems.
        </p>
        <div className="server-status">
          {["Library", "Mess", "Events", "Academics", "AI"].map((s) => (
            <span key={s} className="status-pill">
              <span className="pulse-dot" />
              {s}
            </span>
          ))}
        </div>
      </header>

      <div className="main">
        {/* Dashboard Cards */}
        <div className="dashboard">
          {[
            {
              key: "library",
              icon: "📚",
              title: "Library Hours",
              color: "blue",
              content: dashboardData.library
                ? Object.entries(dashboardData.library).map(([day, time]) => (
                    <div key={day} className="card-row">
                      <span className="day">{day.replace(/_/g, " ")}</span>
                      <span className="time">{time}</span>
                    </div>
                  ))
                : <div className="skeleton-loader"><div className="skel"/><div className="skel"/><div className="skel"/></div>,
            },
            {
              key: "mess",
              icon: "🍽️",
              title: "Mess Menu — Today",
              color: "green",
              content: dashboardData.mess ? (() => {
                const days = ["sunday","monday","tuesday","wednesday","thursday","friday","saturday"];
                const today = days[new Date().getDay()];
                const todayMenu = dashboardData.mess[today];
                return todayMenu ? (
                  Object.entries(todayMenu).map(([meal, items]) => (
                    <div key={meal} className="card-row">
                      <span className="day">{meal}</span>
                      <span className="time">{Array.isArray(items) ? items.join(", ") : items}</span>
                    </div>
                  ))
                ) : <p className="loading-text">No menu available</p>;
              })()
              : <div className="skeleton-loader"><div className="skel"/><div className="skel"/><div className="skel"/></div>,
            },
            {
              key: "events",
              icon: "📅",
              title: "Upcoming Events",
              color: "purple",
              content: dashboardData.events
                ? dashboardData.events.slice(0, 3).map((e, i) => (
                    <div key={i} className="card-row">
                      <span className="day">{e.name}</span>
                      <span className="time">{e.date}</span>
                    </div>
                  ))
                : <div className="skeleton-loader"><div className="skel"/><div className="skel"/><div className="skel"/></div>,
            },
            {
              key: "academics",
              icon: "📝",
              title: "Exam Schedule",
              color: "orange",
              content: dashboardData.academics
                ? dashboardData.academics.map((ex, i) => (
                    <div key={i} className="card-row">
                      <span className="day">{ex.subject}</span>
                      <span className="time">{ex.date}</span>
                    </div>
                  ))
                : <div className="skeleton-loader"><div className="skel"/><div className="skel"/><div className="skel"/></div>,
            },
          ].map((card) => (
            <div
              key={card.key}
              className={`card card-${card.color} ${activeCard === card.key ? "card-active" : ""}`}
              onMouseEnter={() => setActiveCard(card.key)}
              onMouseLeave={() => setActiveCard(null)}
            >
              <div className="card-header">
                <span className="card-icon">{card.icon}</span>
                <h2>{card.title}</h2>
                <div className={`card-glow glow-${card.color}`} />
              </div>
              <div className="card-content">{card.content}</div>
            </div>
          ))}
        </div>

        {/* AI Chat */}
        <div className="chat-section">
          <div className="chat-header">
            <div className="ai-avatar">🤖</div>
            <div>
              <h2>AI Campus Assistant</h2>
              <span className="ai-status">● Online — powered by live MCP servers</span>
            </div>
          </div>

          {/* Quick questions */}
          <div className="quick-questions">
            {quickQuestions.map((q, i) => (
              <button
                key={i}
                className="quick-btn"
                onClick={() => { setQuestion(q); }}
              >
                {q}
              </button>
            ))}
          </div>

          <div className="chat-box">
            {messages.length === 0 && (
              <div className="empty-chat">
                <div className="empty-icon">💬</div>
                <p>Ask me anything about your campus!</p>
              </div>
            )}
            {messages.map((msg, i) => (
              <div key={i} className={`message ${msg.role}`}>
                {msg.role === "bot" && <span className="bot-avatar">🤖</span>}
                <div className="bubble-wrap">
                  <span className="bubble">{msg.text}</span>
                  {msg.server && (
                    <span className="meta">⚡ via {msg.server} server</span>
                  )}
                </div>
                {msg.role === "user" && <span className="user-avatar">👤</span>}
              </div>
            ))}
            {loading && (
              <div className="message bot">
                <span className="bot-avatar">🤖</span>
                <div className="bubble-wrap">
                  <span className="bubble typing-bubble">
                    <span className="dot" /><span className="dot" /><span className="dot" />
                  </span>
                </div>
              </div>
            )}
          </div>

          <div className="input-row">
            <input
              type="text"
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyDown={handleKey}
              placeholder="Ask about library, mess, events, exams..."
            />
            <button onClick={askQuestion} disabled={loading} className="send-btn">
              {loading ? "⏳" : "➤"}
            </button>
          </div>
        </div>
      </div>

      <footer className="footer">
        Built for MARS Open Projects 2026 · Unified Campus Intelligence Dashboard
      </footer>
    </div>
  );
}

export default App;