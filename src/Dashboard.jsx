import React, { useState } from "react";
import { predictStress, analyzeJournal } from "./api";

export default function Dashboard() {
  const [sleep, setSleep] = useState(7);
  const [hydration, setHydration] = useState(4);
  const [mood, setMood] = useState("okay");
  const [prediction, setPrediction] = useState(null);

  const [entry, setEntry] = useState("");
  const [analysis, setAnalysis] = useState(null);

  async function handlePredict() {
    const res = await predictStress({ sleep_hours: sleep, hydration, mood });
    setPrediction(res);
  }

  async function handleAnalyze() {
    const res = await analyzeJournal({ entry });
    setAnalysis(res);
  }

  return (
    <div>
      <h2>Stress Forecast</h2>
      <input type="number" value={sleep} onChange={(e) => setSleep(e.target.value)} />
      <input type="number" value={hydration} onChange={(e) => setHydration(e.target.value)} />
      <select value={mood} onChange={(e) => setMood(e.target.value)}>
        <option value="great">Great</option>
        <option value="okay">Okay</option>
        <option value="stressed">Stressed</option>
        <option value="tired">Tired</option>
        <option value="anxious">Anxious</option>
      </select>
      <button onClick={handlePredict}>Predict Stress</button>
      {prediction && <p>Forecast: {prediction.forecast} (Prob: {prediction.high_stress_prob})</p>}

      <h2>Journal Analysis</h2>
      <textarea value={entry} onChange={(e) => setEntry(e.target.value)} />
      <button onClick={handleAnalyze}>Analyze</button>
      {analysis && <p>Sentiment: {analysis.sentiment} (Conf: {analysis.confidence})</p>}
    </div>
  );
}
