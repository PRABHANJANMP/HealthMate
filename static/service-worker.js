/**
 * HealthMate AI - Service Worker
 * Version: healthmate-v2
 * Provides complete offline capabilities for the Bilingual First-Aid Guide,
 * local styles, scripts, and offline fallback.
 */

const CACHE_NAME = 'healthmate-v2';
const ESSENTIAL_ASSETS = [
    '/',
    '/?tab=wounds',
    '/static/css/style.css',
    '/static/js/app.js',
    '/static/manifest.json',
    '/static/offline.html',
    '/static/images/icon-192.png',
    '/static/images/icon-512.png'
];

const OPTIONAL_ASSETS = [
    'https://cdn.jsdelivr.net/npm/chart.js',
    'https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Tamil:wght@400;500;600;700&display=swap'
];

self.addEventListener('install', (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(async (cache) => {
            console.log('[Service Worker] Pre-caching core offline assets...');
            await cache.addAll(ESSENTIAL_ASSETS);
            for (const url of OPTIONAL_ASSETS) {
                try {
                    const response = await fetch(url, { mode: 'cors' });
                    if (response && response.ok) {
                        await cache.put(url, response);
                    }
                } catch (err) {}
            }
        }).then(() => self.skipWaiting())
    );
});

self.addEventListener('activate', (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((name) => {
                    if (name !== CACHE_NAME) {
                        return caches.delete(name);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

self.addEventListener('fetch', (event) => {
    const url = new URL(event.request.url);

    // Skip POST / non-GET requests
    if (event.request.method !== 'GET') {
        return;
    }

    // HTML Navigation requests
    if (event.request.mode === 'navigate') {
        event.respondWith(
            fetch(event.request)
                .then((networkResponse) => {
                    if (networkResponse && networkResponse.ok) {
                        const clone = networkResponse.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
                    }
                    return networkResponse;
                })
                .catch(async () => {
                    const cachedApp = await caches.match(event.request);
                    if (cachedApp) return cachedApp;
                    const cachedWounds = await caches.match('/?tab=wounds');
                    if (cachedWounds) return cachedWounds;
                    const cachedFallback = await caches.match('/static/offline.html');
                    if (cachedFallback) return cachedFallback;
                    return new Response('Offline: Please reconnect to internet.', {
                        headers: { 'Content-Type': 'text/plain; charset=utf-8' }
                    });
                })
        );
        return;
    }

    // Static Assets - Stale-While-Revalidate
    event.respondWith(
        caches.match(event.request).then((cachedResponse) => {
            const fetchPromise = fetch(event.request)
                .then((networkResponse) => {
                    if (networkResponse && networkResponse.status === 200) {
                        const clone = networkResponse.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
                    }
                    return networkResponse;
                })
                .catch(() => {});
            return cachedResponse || fetchPromise;
        })
    );
});
