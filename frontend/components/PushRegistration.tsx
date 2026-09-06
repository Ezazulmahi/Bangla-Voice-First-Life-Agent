"use client";

import { useEffect } from "react";

import { getToken } from "@/lib/api";
import { ensurePushSubscription } from "@/lib/push";

/**
 * Mounted once in the root layout. Registers the service worker and a Web
 * Push subscription so reminders can notify even when the app tab is
 * closed — real push (via the backend's APScheduler job + VAPID), not a
 * client-side poll. No-ops silently if there's no session yet, or if the
 * browser/user doesn't support or grant notifications.
 */
export default function PushRegistration() {
  useEffect(() => {
    if (!getToken()) return;
    ensurePushSubscription().catch(() => {});
  }, []);

  return null;
}
