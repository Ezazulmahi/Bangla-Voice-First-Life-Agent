"use client";

import { useEffect, useRef } from "react";

import { getToken, listReminders } from "@/lib/api";

const POLL_MS = 60_000;
const DUE_WINDOW_MS = 5 * 60_000; // nudge once a reminder is within 5 minutes of due (or overdue)

/**
 * Best-effort in-app reminder nudges via the browser Notification API,
 * polled while the app tab is open. This is NOT a real push-notification
 * system — it can't wake a closed tab or notify offline, and would need a
 * service worker + VAPID push (or an SMS gateway) for that. Flagged as a
 * product decision in the QA report; this covers the "app open" case for
 * real, which is a genuine capability, not a stub.
 */
export default function ReminderNudger() {
  const notifiedIds = useRef<Set<number>>(new Set());

  useEffect(() => {
    if (typeof window === "undefined" || !("Notification" in window)) return;
    if (Notification.permission === "default") {
      Notification.requestPermission().catch(() => {});
    }
  }, []);

  useEffect(() => {
    if (typeof window === "undefined" || !("Notification" in window)) return;

    async function checkDue() {
      if (!getToken() || Notification.permission !== "granted") return;
      try {
        const reminders = await listReminders();
        const now = Date.now();
        for (const r of reminders) {
          if (!r.enabled) continue;
          if (notifiedIds.current.has(r.id)) continue;
          const dueMs = new Date(r.due_at).getTime();
          if (dueMs - now <= DUE_WINDOW_MS) {
            notifiedIds.current.add(r.id);
            new Notification(r.title, { body: r.message || "Sohai reminder · সোহাই রিমাইন্ডার" });
          }
        }
      } catch {
        // silent — this is a best-effort nudge, not a critical path
      }
    }

    checkDue();
    const interval = setInterval(checkDue, POLL_MS);
    return () => clearInterval(interval);
  }, []);

  return null;
}
