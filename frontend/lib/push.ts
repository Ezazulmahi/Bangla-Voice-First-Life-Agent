"use client";

import { getVapidPublicKey, subscribePush } from "./api";

function urlBase64ToUint8Array(base64Url: string): Uint8Array {
  const padding = "=".repeat((4 - (base64Url.length % 4)) % 4);
  const base64 = (base64Url + padding).replace(/-/g, "+").replace(/_/g, "/");
  const raw = atob(base64);
  return Uint8Array.from([...raw].map((c) => c.charCodeAt(0)));
}

export function pushSupported(): boolean {
  return (
    typeof window !== "undefined" &&
    "serviceWorker" in navigator &&
    "PushManager" in window &&
    "Notification" in window
  );
}

/** Registers the service worker, requests notification permission, subscribes
 * to push, and registers the subscription with the backend. Safe to call
 * repeatedly (e.g. on every app load) — browsers return the existing
 * subscription if one is already active. Silently no-ops on unsupported
 * browsers or if permission is denied, rather than surfacing an error —
 * reminders still work via in-app viewing either way. */
export async function ensurePushSubscription(): Promise<void> {
  if (!pushSupported()) return;

  const permission =
    Notification.permission === "default" ? await Notification.requestPermission() : Notification.permission;
  if (permission !== "granted") return;

  const registration = await navigator.serviceWorker.register("/sw.js");
  await navigator.serviceWorker.ready;

  let subscription = await registration.pushManager.getSubscription();
  if (!subscription) {
    const { public_key } = await getVapidPublicKey();
    if (!public_key) return; // backend has no VAPID keys configured
    subscription = await registration.pushManager.subscribe({
      userVisibleOnly: true,
      applicationServerKey: urlBase64ToUint8Array(public_key),
    });
  }

  await subscribePush(subscription.toJSON()).catch(() => {});
}
