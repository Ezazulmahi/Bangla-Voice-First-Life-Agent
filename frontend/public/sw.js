// Minimal service worker: shows a notification for each push event, and
// focuses (or opens) the app when the user taps it. Registered from
// components/PushRegistration.tsx.

self.addEventListener("push", (event) => {
  let payload = { title: "Sohai", body: "আপনার একটি রিমাইন্ডার আছে।" };
  if (event.data) {
    try {
      payload = event.data.json();
    } catch {
      payload.body = event.data.text();
    }
  }
  event.waitUntil(
    self.registration.showNotification(payload.title, {
      body: payload.body,
    })
  );
});

self.addEventListener("notificationclick", (event) => {
  event.notification.close();
  event.waitUntil(
    self.clients.matchAll({ type: "window", includeUncontrolled: true }).then((clients) => {
      for (const client of clients) {
        if ("focus" in client) return client.focus();
      }
      if (self.clients.openWindow) return self.clients.openWindow("/home");
    })
  );
});
