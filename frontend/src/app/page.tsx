"use client";

import { FormEvent, useState } from "react";
import { investigate, type Evidence, type InvestigationResult } from "../services/api";

const quickIds = ["ANOM-001", "ANOM-002", "ANOM-003"];

function evidenceTitle(evidence: Evidence) {
  return String(evidence.title ?? evidence.type ?? "Evidence").replaceAll("_", " ");
}

function EvidenceCard({ evidence, index }: { evidence: Evidence; index: number }) {
  const steps = Array.isArray(evidence.steps) ? evidence.steps : [];
  return <article className="evidence-card">
    <span className="item-number">{String(index + 1).padStart(2, "0")}</span>
    <div><p className="card-type">{String(evidence.type ?? "Mission data").replaceAll("_", " ")}</p><h3>{evidenceTitle(evidence)}</h3>
      {typeof evidence.description === "string" && <p>{evidence.description}</p>}
      {typeof evidence.resolution === "string" && <p><strong>Resolution:</strong> {evidence.resolution}</p>}
      {steps.length > 0 && <ul>{steps.map((step) => <li key={String(step)}>{String(step)}</li>)}</ul>}
      {evidence.data !== undefined && evidence.data !== null && <pre>{JSON.stringify(evidence.data, null, 2)}</pre>}
    </div>
  </article>;
}

function SignalChart() {
  return <div className="chart" aria-label="Illustrative telemetry chart"><svg viewBox="0 0 300 80" role="img"><path className="chart-grid" d="M0 20H300M0 40H300M0 60H300" /><path className="chart-line" d="M0 61 L18 57 L35 58 L51 48 L69 51 L88 44 L104 46 L123 35 L140 21 L157 13 L176 20 L195 40 L214 45 L235 36 L252 39 L267 52 L285 57 L300 55" /></svg></div>;
}

export default function Home() {
  const [query, setQuery] = useState("ANOM-001");
  const [result, setResult] = useState<InvestigationResult | null>(null);
  const [error, setError] = useState("");
  const [isLoading, setIsLoading] = useState(false);

  async function onSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const anomalyId = query.trim();
    if (!anomalyId) return;
    setIsLoading(true); setError("");
    try { setResult(await investigate(anomalyId)); }
    catch (caught) { setResult(null); setError(caught instanceof Error ? caught.message : "Unable to run investigation."); }
    finally { setIsLoading(false); }
  }

  const confidenceValue = result ? Math.round(Math.max(0, Math.min(1, result.confidence)) * 100) : 0;
  const confidence = result ? `${confidenceValue}%` : "--";
  const signals = result?.anomalies.length ?? 0;
  const severity = signals > 0 ? "HIGH" : "CLEAR";

  return <main className="app-shell">
    <header className="topbar">
      <a className="brand" href="#workspace"><span className="brand-symbol">✦</span><span><strong>NEXUS</strong><small>MISSION INTELLIGENCE</small></span></a>
      <nav aria-label="Main navigation"><a className="active" href="#workspace">Dashboard</a><a href="#mission">Missions</a><a href="#workspace">Investigations</a><a href="#telemetry">Telemetry</a><a href="#evidence">Knowledge</a></nav>
      <div className="header-status"><span><i />SYSTEM STATUS<b>OPERATIONAL</b></span><time>14:32:08 <small>UTC</small></time><button className="avatar" type="button" aria-label="User profile">N</button></div>
    </header>

    <div className="dashboard">
      <aside className="mission-rail" id="mission">
        <p className="rail-title">MISSION CONSOLE</p>
        <form onSubmit={onSubmit} className="investigate-form"><label htmlFor="query">ANOMALY ID</label><div className="query-input"><input id="query" value={query} onChange={(event) => setQuery(event.target.value)} required /><span>×</span></div><button className="investigate-button" disabled={isLoading}>{isLoading ? <><i className="spinner" />ANALYZING</> : <>INVESTIGATE <b>&rarr;</b></>}</button></form>
        <div className="quick-access"><p>QUICK ACCESS</p>{quickIds.map((id) => <button key={id} type="button" onClick={() => setQuery(id)} className={query === id ? "selected" : ""}>{id}</button>)}</div>
        <section className="mission-card"><div className="card-row"><b>MISSION STATUS</b><span>All systems nominal <i /></span></div><div className="spacecraft">⟨<span>═══</span>◈<span>═══</span>⟩</div><div className="system-bars"><p>POWER <b>87.4%</b><i><em style={{ width: "87%" }} /></i></p><p>THERMAL <b>STABLE</b><i><em style={{ width: "91%" }} /></i></p><p>COMM LINK <b>NOMINAL</b><i><em style={{ width: "80%" }} /></i></p></div></section>
        <section className="events"><p>24H EVENTS</p><span className="warning">⚠ ANOM-001</span><span>✓ EVT-204</span><span>✓ EVT-203</span></section>
        <div className="rail-footer"><b>✦ NEXUS AI CORE</b><span>v1.0.0</span><span>© 2026 Nexus Space Systems</span></div>
      </aside>

      <section className="workspace" id="workspace">
        <div className="active-hero"><div><p className="live-label"><i />LIVE INVESTIGATION</p><h1>{query || "ANOM-001"}</h1><h2>Autonomous anomaly analysis</h2><p>Mission context, telemetry correlation, and operational guidance in one focused view.</p><div className="hero-actions"><button type="button">◉ WATCH LIVE</button><button type="button" aria-label="Bookmark investigation">♡</button></div></div><div className="orbital-graphic"><div className="orbit" /><span>✦</span><small>MISSION<br />ORBITAL NODE</small></div></div>
        {error && <div className="error-panel" role="alert"><b>!</b><span><strong>INVESTIGATION UNAVAILABLE</strong>{error}</span></div>}
        {isLoading && <div className="loading-panel"><i className="spinner" /> Correlating mission telemetry and historical evidence...</div>}
        <section className="investigation-results" aria-live="polite"><div className="section-top"><p>INVESTIGATION RESULT <i /> {result ? "COMPLETED" : "STANDING BY"}</p><span>{result ? `ID: ${result.investigation_id.slice(0, 8).toUpperCase()}` : "READY FOR INPUT"}</span></div>
          <div className="metric-grid"><article className={signals > 0 ? "severity high" : "severity"}><p>SEVERITY</p><strong>{result ? severity : "--"}</strong><small>{result ? (signals > 0 ? "Immediate attention" : "No active signals") : "Awaiting investigation"}</small></article><article><p>CONFIDENCE</p><strong className="cyan-text">{confidence}</strong><SignalChart /></article><article><p>SIGNALS DETECTED</p><strong className="cyan-text">{result ? String(signals).padStart(2, "0") : "--"}</strong><small>{result ? "Related telemetry signals" : "No data available"}</small></article></div>
          <div className="report-grid"><article className="assessment"><p>AI ASSESSMENT</p>{result?.summary.length ? <div className="summary-copy">{result.summary.map((item, index) => <p key={`${item}-${index}`}><b>{String(index + 1).padStart(2, "0")}</b>{item}</p>)}</div> : <p className="empty-copy">Run an investigation to receive a contextual AI assessment.</p>}<h3>KEY INSIGHT</h3><p className="empty-copy">{result ? `Assessment confidence is ${confidence} based on currently available mission data.` : "Signal analysis will appear here."}</p></article>
            <article id="evidence"><div className="report-card-title"><p>EVIDENCE</p><span>{result?.evidence.length ?? 0} ITEMS</span></div>{result?.evidence.length ? <div className="evidence-list">{result.evidence.map((item, index) => <EvidenceCard key={`${evidenceTitle(item)}-${index}`} evidence={item} index={index} />)}</div> : <p className="empty-copy">No evidence loaded. Investigation evidence will be organized here.</p>}</article>
            <article><p>RECOMMENDED NEXT STEPS</p>{result?.next_steps.length ? <ol className="next-steps">{result.next_steps.map((step, index) => <li key={`${step}-${index}`}><b>{String(index + 1).padStart(2, "0")}</b><span>{step}</span></li>)}</ol> : <p className="empty-copy">Recommended procedures will appear after analysis.</p>}<button type="button" className="download-button">DOWNLOAD REPORT ↓</button></article></div>
        </section>
      </section>

      <aside className="telemetry-rail" id="telemetry"><section><p className="rail-title">SYSTEM STATUS</p><div className="nominal"><i /> NOMINAL</div></section><section className="telemetry-summary"><p className="rail-title">TELEMETRY</p><b>92% <span>Signal</span></b><span>28.4°C</span><span>3.2 A</span><span>28.1 V</span></section><section className="telemetry-card"><div className="card-row"><b>LIVE TELEMETRY</b><span>View all</span></div><div className="telemetry-numbers"><span>SIGNAL STRENGTH<b>92%</b></span><span>DATA RATE<b>2.48 Mbps</b></span></div><SignalChart /><small>00:00　　　　　00:30　　　　　01:00</small></section><section className="analysis-feed"><p>AI ANALYSIS FEED</p><span><i />14:31:59 <small>Anomaly correlation complete</small></span><span><i />14:31:42 <small>Telemetry patterns matched</small></span><span><i />14:31:21 <small>Historical data retrieved</small></span></section></aside>
    </div>
    <footer><b>SYSTEM LOG</b><span>12:41:02</span><span>{result ? "Investigation completed successfully" : "Investigation console ready"}</span></footer>
  </main>;
}
