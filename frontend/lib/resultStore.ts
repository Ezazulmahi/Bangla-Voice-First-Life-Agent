"use client";

// Hands tool result data from the listening screen to the detail screen it
// routes to (packages/statement/complaint) across a real navigation, since
// they're separate routes. sessionStorage keeps it tab-local and out of the
// URL.

const KEYS = {
  mobile_compare: "sohai_result_packages",
  statement_explain: "sohai_result_statement",
  complaint_draft: "sohai_result_complaint",
} as const;

export type StorableTool = keyof typeof KEYS;

export function storeToolResult(tool: StorableTool, data: unknown) {
  sessionStorage.setItem(KEYS[tool], JSON.stringify(data));
}

export function readToolResult<T>(tool: StorableTool): T | null {
  if (typeof window === "undefined") return null;
  const raw = sessionStorage.getItem(KEYS[tool]);
  if (!raw) return null;
  try {
    return JSON.parse(raw) as T;
  } catch {
    return null;
  }
}

export function routeForTool(tool: string | null): string | null {
  switch (tool) {
    case "mobile_compare":
      return "/packages";
    case "statement_explain":
      return "/statement";
    case "complaint_draft":
      return "/complaint";
    default:
      return null;
  }
}
