import { useEffect, useState } from "react";
import { createLead, deleteLead, getHealth, getStats, listLeads, updateLead } from "../services/api";

export default function Dashboard() {
  const [health, setHealth] = useState<any>(null);
  const [leads, setLeads] = useState<any[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [q, setQ] = useState("");
  const [statusFilter, setStatusFilter] = useState("");
  const [error, setError] = useState<string | null>(null);

  async function refresh() {
    try {
      const [h, s, l] = await Promise.all([getHealth(), getStats(), listLeads({ q, status: statusFilter })]);
      setHealth(h); setStats(s); setLeads(l.items);
      setError(null);
    } catch (e: any) {
      setError(e.message);
    }
  }

  useEffect(() => { refresh(); }, [q, statusFilter]);

  async function handleDelete(id: number) {
    if (!confirm("Delete this lead?")) return;
    await deleteLead(id);
    refresh();
  }

  async function handleStatus(id: number, status: string) {
    await updateLead(id, { status });
    refresh();
  }

  return (
    <main className="shell">
      <header className="topbar">
        <a className="brand" href="/">EnvyLead</a>
        <span className="phase">Voice lead desk</span>
      </header>

      <section className="hero">
        <p className="eyebrow">Multilingual voice intelligence for real estate</p>
        <h1>Every call becomes a lead you can verify.</h1>
        <p className="lede">
          Record an enquiry, transcribe it with Gnani Prisma, review the structured details,
          and save only what a human approves.
        </p>
      </section>

      <section className="stat-grid">
        <div className="stat-card"><span className="stat-label">Total leads</span><span className="stat-value">{stats?.total ?? "—"}</span></div>
        <div className="stat-card"><span className="stat-label">New</span><span className="stat-value">{stats?.by_status?.new ?? 0}</span></div>
        <div className="stat-card"><span className="stat-label">Qualified</span><span className="stat-value">{stats?.by_status?.qualified ?? 0}</span></div>
        <div className="stat-card stat-card--accent"><span className="stat-label">High priority</span><span className="stat-value">{stats?.high_priority ?? 0}</span></div>
      </section>

      <section className="voice-lab">
        <div className="section-head">
          <p className="eyebrow">Voice AI</p>
          <h2>Transcribe an enquiry</h2>
          <p className="section-copy">Upload an audio file. Prisma transcribes it; fields are extracted for review.</p>
        </div>
        <div className="voice-grid">
          <div className="voice-card">
            <h3>Prisma transcription</h3>
            <form className="voice-form" onSubmit={async (e) => {
              e.preventDefault();
              const f = (e.currentTarget.elements.namedItem("audio") as HTMLInputElement)?.files?.[0];
              if (!f) return;
              const lang = (e.currentTarget.elements.namedItem("lang") as HTMLSelectElement).value;
              try {
                const r = await (await fetch("/api/stt/transcribe", { method: "POST", body: (() => { const fd = new FormData(); fd.append("file", f); fd.append("language", lang); return fd; })() })).json();
                alert("Transcript: " + (r.transcript || ""));
                if (r.extracted?.name) {
                  await createLead({ name: r.extracted.name || "Unknown", phone: r.extracted.phone, budget: r.extracted.budget, location: r.extracted.location, property_type: r.extracted.property_type, bhk: r.extracted.bhk, intent: r.extracted.intent, notes: r.extracted.notes, transcript: r.transcript, language: lang, source: "voice", status: "new", priority: "medium" });
                  refresh();
                }
              } catch (err: any) { alert(err.message); }
            }}>
              <input name="audio" type="file" accept="audio/*" />
              <select name="lang" defaultValue="indic-auto">
                <option value="indic-auto">Indic auto</option>
                <option value="en-IN">English (India)</option>
                <option value="te-IN">Telugu</option>
              </select>
              <button className="button" type="submit">Transcribe &amp; save lead</button>
            </form>
          </div>
          <div className="voice-card">
            <h3>Timbre synthesis</h3>
            <form className="voice-form" onSubmit={async (e) => {
              e.preventDefault();
              const text = (e.currentTarget.elements.namedItem("ttext") as HTMLTextAreaElement).value;
              try {
                const fd = new FormData(); fd.append("text", text); fd.append("language", "en-IN");
                const r = await fetch("/api/tts/synthesize", { method: "POST", body: fd });
                const blob = await r.blob();
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a"); a.href = url; a.download = "envylead-tts.wav"; a.click();
              } catch (err: any) { alert(err.message); }
            }}>
              <textarea name="ttext" placeholder="Type text to speak..." />
              <button className="button" type="submit">Generate speech</button>
            </form>
          </div>
        </div>
      </section>

      <section className="lead-section">
        <div className="section-head section-head--wide">
          <div>
            <h2>Lead desk</h2>
            <p className="section-copy">Search, filter, edit and manage approved leads.</p>
          </div>
          <div className="table-toolbar">
            <div className="toolbar-search">
              <input placeholder="Search name, phone, location..." value={q} onChange={e => setQ(e.target.value)} />
            </div>
            <div className="toolbar-field">
              <span>Status</span>
              <select value={statusFilter} onChange={e => setStatusFilter(e.target.value)}>
                <option value="">All</option>
                <option value="new">New</option>
                <option value="contacted">Contacted</option>
                <option value="qualified">Qualified</option>
                <option value="closed">Closed</option>
              </select>
            </div>
            <button className="button button--small" onClick={refresh}>Refresh</button>
          </div>
        </div>

        <div className="lead-table-card">
          <div className="table-wrap">
            <table className="lead-table">
              <thead>
                <tr>
                  <th>Lead</th><th>Requirement</th><th>Budget</th><th>Location</th><th>Status</th><th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {leads.length === 0 && (
                  <tr><td colSpan={6}><div className="empty-state"><h4>No leads yet</h4><p>Leads you approve will appear here.</p></div></td></tr>
                )}
                {leads.map(l => (
                  <tr key={l.id}>
                    <td>
                      <button className="lead-link">{l.name}</button>
                      <span className="lead-sub">{l.phone || "—"}</span>
                    </td>
                    <td>{l.bhk || "—"} · {l.property_type || "—"} · {l.intent || "—"}</td>
                    <td>{l.budget || "—"}</td>
                    <td>{l.location || "—"}</td>
                    <td>
                      <select value={l.status} onChange={e => handleStatus(l.id, e.target.value)}>
                        <option value="new">New</option>
                        <option value="contacted">Contacted</option>
                        <option value="qualified">Qualified</option>
                        <option value="closed">Closed</option>
                      </select>
                    </td>
                    <td>
                      <button className="button button--small button--danger" onClick={() => handleDelete(l.id)}>Delete</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
          <p className="table-foot">Showing {leads.length} of {stats?.total ?? leads.length} leads · newest first</p>
        </div>
      </section>

      <section className="panel">
        <div className="panel-head">
          <div>
            <p className="eyebrow">Backend connection</p>
            <h2>Service status</h2>
          </div>
          {health && <span className={`status status--${health.status === "ok" ? "online" : "offline"}`}>{health.status === "ok" ? "Online" : "Offline"}</span>}
        </div>
        {health && (
          <dl className="facts">
            <div><dt>Service</dt><dd>{health.service}</dd></div>
            <div><dt>Version</dt><dd>{health.version}</dd></div>
            <div><dt>Environment</dt><dd>{health.environment}</dd></div>
            <div><dt>Gnani key</dt><dd>{health.gnani_configured ? "Configured" : "Not set"}</dd></div>
            <div><dt>STT</dt><dd>{health.stt_model}</dd></div>
            <div><dt>TTS</dt><dd>{health.tts_model}</dd></div>
          </dl>
        )}
        {error && <div className="error-box"><p>{error}</p></div>}
      </section>

      <footer className="footer">
        <span>EnvyLead</span>
        <span>Leads are stored in a local SQLite database on the backend.</span>
      </footer>
    </main>
  );
}