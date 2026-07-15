const CACHE = 'zmax-comfyui-v1';
const URLS = [
  '/comfyui.html',
  '/manifest.json',
  '/pwa/icon-192.png',
  '/pwa/icon-512.png'
];

self.addEventListener('install', e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(URLS)));
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(caches.keys().then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))));
  self.clients.claim();
});

self.addEventListener('fetch', e => {
  e.respondWith(
    caches.match(e.request).then(r => r || fetch(e.request).then(res => {
      if(res.ok){const clone=res.clone();caches.open(CACHE).then(c=>c.put(e.request,clone))}
      return res;
    }))
  );
});
