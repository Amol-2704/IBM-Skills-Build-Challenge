export type Evidence = Record<string, unknown>;

export interface InvestigationResult {
  investigation_id: string;
  query: string;
  summary: string[];
  anomalies: unknown[];
  evidence: Evidence[];
  confidence: number;
  next_steps: string[];
}

const apiBaseUrl = process.env.NEXT_PUBLIC_API_URL ?? "http://127.0.0.1:8000";

export async function investigate(query: string): Promise<InvestigationResult> {
  const response = await fetch(`${apiBaseUrl}/investigate`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query, time_range: "24h" }),
  });

  if (!response.ok) {
    const detail = await response.text();
    throw new Error(detail || `Investigation failed (${response.status}).`);
  }

  return response.json() as Promise<InvestigationResult>;
}
