const API_BASE = "http://localhost:8000";

export async function predictStress({ sleep_hours, hydration, mood }) {
  const res = await fetch(`${API_BASE}/predict_stress`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ sleep_hours, hydration, mood }),
  });
  return await res.json();
}

export async function analyzeJournal({ entry }) {
  const res = await fetch(`${API_BASE}/analyze_journal`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ entry }),
  });
  return await res.json();
}
