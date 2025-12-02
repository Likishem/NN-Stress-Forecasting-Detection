// frontend/src/Chatbot.jsx
import React, { useState } from "react";

export default function Chatbot() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  async function sendMessage() {
    const res = await fetch("http://localhost:8000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input }),
    });
    const data = await res.json();
    setMessages([...messages, { role: "user", text: input }, { role: "bot", text: data.reply }]);
    setInput("");
  }

  return (
    <div style={{ border: "1px solid #ddd", padding: 16, borderRadius: 8 }}>
      <h2>MindCast Chatbot</h2>
      <div style={{ maxHeight: 300, overflowY: "auto", marginBottom: 12 }}>
        {messages.map((m, i) => (
          <div key={i} style={{ textAlign: m.role === "user" ? "right" : "left" }}>
            <span style={{ background: m.role === "user" ? "#cce5ff" : "#e2e2e2", padding: 8, borderRadius: 6 }}>
              {m.text}
            </span>
          </div>
        ))}
      </div>
      <input value={input} onChange={(e) => setInput(e.target.value)} placeholder="Type a message..." />
      <button onClick={sendMessage}>Send</button>
    </div>
  );
}
