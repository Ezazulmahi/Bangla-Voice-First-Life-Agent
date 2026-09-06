export const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

const TOKEN_KEY = "sohai_token";
const PHONE_KEY = "sohai_phone";
const CONVERSATION_KEY = "sohai_conversation_id";

export function getToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(PHONE_KEY);
  localStorage.removeItem(CONVERSATION_KEY);
}

export function getStoredPhone(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem(PHONE_KEY);
}

export function setStoredPhone(phone: string) {
  localStorage.setItem(PHONE_KEY, phone);
}

export function getStoredConversationId(): number | null {
  if (typeof window === "undefined") return null;
  const raw = localStorage.getItem(CONVERSATION_KEY);
  return raw ? Number(raw) : null;
}

export function setStoredConversationId(id: number) {
  localStorage.setItem(CONVERSATION_KEY, String(id));
}

export function mediaUrl(path: string | null | undefined): string | null {
  if (!path) return null;
  return path.startsWith("http") ? path : `${API_BASE}${path}`;
}

export class ApiError extends Error {
  status: number;
  constructor(status: number, message: string) {
    super(message);
    this.status = status;
  }
}

async function apiFetch<T>(path: string, options: RequestInit = {}): Promise<T> {
  const token = getToken();
  const headers = new Headers(options.headers);
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (options.body && !(options.body instanceof FormData) && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  if (res.status === 401) {
    clearToken();
    if (typeof window !== "undefined") window.location.href = "/";
    throw new ApiError(401, "Session expired");
  }

  if (!res.ok) {
    const body = await res.json().catch(() => ({ detail: res.statusText }));
    throw new ApiError(res.status, body.detail || "Request failed");
  }

  if (res.status === 204) return undefined as T;
  return res.json();
}

// ---- auth ----

export function requestOtp(phoneNumber: string) {
  return apiFetch<{ message: string; debug_code: string | null }>("/auth/request-otp", {
    method: "POST",
    body: JSON.stringify({ phone_number: phoneNumber }),
  });
}

export function verifyOtp(phoneNumber: string, code: string) {
  return apiFetch<{ access_token: string; token_type: string }>("/auth/verify-otp", {
    method: "POST",
    body: JSON.stringify({ phone_number: phoneNumber, code }),
  });
}

export function getMe() {
  return apiFetch<{ id: number; phone_number: string; audio_retention_opt_in: boolean }>("/auth/me");
}

// ---- conversations ----

export interface ConversationSummary {
  id: number;
  created_at: string;
  last_transcript: string | null;
  last_tool_used: string | null;
}

export function createConversation() {
  return apiFetch<ConversationSummary>("/conversations", { method: "POST" });
}

export function listConversations() {
  return apiFetch<ConversationSummary[]>("/conversations");
}

export interface AudioTurnResult {
  transcript: string;
  reply_text: string;
  reply_audio_url: string | null;
  tool_used: string | null;
  data: Record<string, unknown> | null;
}

function extensionForMimeType(mimeType: string): string {
  if (mimeType.includes("webm")) return "webm";
  if (mimeType.includes("mp4")) return "m4a";
  if (mimeType.includes("ogg")) return "ogg";
  if (mimeType.includes("wav")) return "wav";
  return "webm";
}

export function submitAudio(conversationId: number, audioBlob: Blob) {
  const form = new FormData();
  form.append("audio", audioBlob, `recording.${extensionForMimeType(audioBlob.type)}`);
  return apiFetch<AudioTurnResult>(`/conversations/${conversationId}/audio`, {
    method: "POST",
    body: form,
  });
}

// ---- tools ----

export interface MobilePackage {
  id: number;
  operator: string;
  name: string;
  data_gb: number;
  validity_days: number;
  price_bdt: number;
}

export function listMobilePackages() {
  return apiFetch<MobilePackage[]>("/tools/mobile-packages");
}

export interface ComplaintDraft {
  id: number;
  company_name: string;
  issue_description: string;
  generated_text: string;
  created_at: string;
}

export function createComplaintDraft(companyName: string, issueDescription: string) {
  return apiFetch<ComplaintDraft>("/tools/complaint-draft", {
    method: "POST",
    body: JSON.stringify({ company_name: companyName, issue_description: issueDescription }),
  });
}

// ---- reminders ----

export interface Reminder {
  id: number;
  title: string;
  message: string | null;
  due_at: string;
  enabled: boolean;
  notify_channel: string;
  created_at: string;
}

export function listReminders() {
  return apiFetch<Reminder[]>("/reminders");
}

export function updateReminder(id: number, patch: Partial<Pick<Reminder, "enabled" | "title" | "due_at">>) {
  return apiFetch<Reminder>(`/reminders/${id}`, {
    method: "PATCH",
    body: JSON.stringify(patch),
  });
}
