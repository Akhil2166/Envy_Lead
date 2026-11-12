export const BASE = (import.meta.env.VITE_API_BASE_URL as string | undefined) || "/api";

async function req(path: string, init?: RequestInit) {
  const r = await fetch(BASE + path, init);
  if (!r.ok) throw new Error(await r.text());
  if (r.status === 204) return null;
  return r.json();
}

export async function getHealth(): Promise<any> {
  return req("/health");
}

export async function listLeads(params: Record<string, string> = {}): Promise<any> {
  const q = new URLSearchParams(params).toString();
  return req("/leads" + (q ? "?" + q : ""));
}

export async function getStats(): Promise<any> {
  return req("/leads/stats");
}

export async function createLead(lead: any): Promise<any> {
  return req("/leads", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(lead) });
}

export async function updateLead(id: number, patch: any): Promise<any> {
  return req(`/leads/${id}`, { method: "PATCH", headers: { "Content-Type": "application/json" }, body: JSON.stringify(patch) });
}

export async function deleteLead(id: number): Promise<any> {
  return req(`/leads/${id}`, { method: "DELETE" });
}

export async function transcribeAudio(file: File, language: string): Promise<any> {
  const fd = new FormData();
  fd.append("file", file);
  fd.append("language", language);
  const r = await fetch(BASE + "/stt/transcribe", { method: "POST", body: fd });
  if (!r.ok) throw new Error(await r.text());
  return r.json();
}

export async function synthesizeSpeech(text: string, voice?: string, language?: string): Promise<Blob> {
  const fd = new FormData();
  fd.append("text", text);
  if (voice) fd.append("voice", voice);
  if (language) fd.append("language", language);
  const r = await fetch(BASE + "/tts/synthesize", { method: "POST", body: fd });
  if (!r.ok) throw new Error(await r.text());
  return r.blob();
}

export async function extractLead(transcript: string): Promise<any> {
  return req("/leads/extract", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ transcript }) });
}