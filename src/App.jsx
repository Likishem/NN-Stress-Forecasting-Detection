import React from "react";
import Dashboard from "./Dashboard";
import Chatbot from "./Chatbot";

export default function App() {
  return (
    <main>
      <h1>MindCast</h1>
      <Dashboard />
      <Chatbot />   {/* 👈 This makes the chatbot show up */}
    </main>
  );
}

<div className="chatbot-container">
  <Chatbot />
</div>
