export type ModuleKey = "live" | "timeline" | "geospatial";

export interface ModuleState {
  key: ModuleKey;
  name: string;
  script: string;
  description: string;
  status: "running" | "stopped";
  pid: number | null;
}

const API_BASE = (import.meta.env.VITE_CPS_API_URL as string | undefined) ?? "http://127.0.0.1:5001";

async function parseResponse<T>(response: Response): Promise<T> {
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    const message = (data as { error?: string }).error ?? `Request failed with status ${response.status}`;
    throw new Error(message);
  }
  return data as T;
}

export async function listModuleStates(): Promise<ModuleState[]> {
  const response = await fetch(`${API_BASE}/api/modules`);
  const data = await parseResponse<{ modules: ModuleState[] }>(response);
  return data.modules;
}

export async function startModule(key: ModuleKey): Promise<ModuleState> {
  const response = await fetch(`${API_BASE}/api/modules/${key}/start`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  return parseResponse<ModuleState>(response);
}

export async function stopModule(key: ModuleKey): Promise<ModuleState> {
  const response = await fetch(`${API_BASE}/api/modules/${key}/stop`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
  });
  return parseResponse<ModuleState>(response);
}
