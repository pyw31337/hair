// Upgrade path for visitors with a service worker registered by an older build.
// Deliberately no fetch handler: current pages always use the latest network assets.
self.addEventListener('install', () => self.skipWaiting());

self.addEventListener('activate', (event) => {
  event.waitUntil(self.clients.claim());
});
