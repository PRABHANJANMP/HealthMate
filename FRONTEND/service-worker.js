/**
 * HealthMate AI - Service Worker
 * Version: healthmate-v1
 * Provides complete offline capabilities for the Bilingual First-Aid Guide,
 * local styles, scripts, and offline fallback.
 */

const CACHE_NAME = "healthmate-v1";
const ESSENTIAL_ASSETS = [
    "./",
    "./index.html",
    "./style.css",
    "./script.js",
    "./manifest.json",
    "./offline.html",
    "./icons/icon-192.png",
    "./icons/icon-512.png"
];

// External assets to attempt caching (gracefully skip if offline during install)
const OPTIONAL_ASSETS = [
    "https://cdn.jsdelivr.net/npm/chart.js",
    "https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=Noto+Sans+Tamil:wght@400;500;600;700&display=swap"
];

// Install Event: Pre-cache essential frontend assets
self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then(async (cache) => {
            console.log("[Service Worker] Pre-caching core offline assets...");
            // Cache essential local assets strictly
            await cache.addAll(ESSENTIAL_ASSETS);
            
            // Attempt caching external optional assets
            for (const url of OPTIONAL_ASSETS) {
                try {
                    const response = await fetch(url, { mode: "cors" });
                    if (response && response.ok) {
                        await cache.put(url, response);
                    }
                } catch (err) {
                    console.log("[Service Worker] Non-critical asset cache skipped:", url);
                }
            }
        }).then(() => self.skipWaiting())
    );
});

// Activate Event: Clean up old caches
self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((name) => {
                    if (name !== CACHE_NAME) {
                        console.log("[Service Worker] Deleting obsolete cache:", name);
                        return caches.delete(name);
                    }
                })
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch Event: Network & Cache Strategy
self.addEventListener("fetch", (event) => {
    const url = new URL(event.request.url);

    // 1. Skip non-GET requests and API calls (API requests are handled in script.js)
    if (event.request.method !== "GET" || url.pathname.startsWith("/api/") || url.pathname.startsWith("/chat") || url.pathname === "/health") {
        return;
    }

    // 2. Navigation Requests (HTML pages)
    if (event.request.mode === "navigate") {
        event.respondWith(
            fetch(event.request)
                .then((networkResponse) => {
                    // Update cache with fresh version
                    if (networkResponse && networkResponse.ok) {
                        const clone = networkResponse.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(event.request, clone));
                    }
                    return networkResponse;
                })
                .catch(async () => {
                    // Offline fallback: serve cached index.html first, else offline.html
                    const cachedApp = await caches.match("./index.html");
                    if (cachedApp) return cachedApp;
                    const cachedFallback = await caches.match("./offline.html");
                    if (cachedFallback) return cachedFallback;
                    return new Response("Offline: Please reconnect to internet.", {
                        headers: { "Content-Type": "text/plain; charset=utf-8" }
                    });
                })
        );
        return;
    }

    // 3. Static Assets (CSS, JS, Fonts, Icons) - Stale-While-Revalidate
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
                .catch(() => {
                    // Silently fail fetch if offline, cached response will serve
                });

            // Return cached response immediately if present, otherwise wait for network
            return cachedResponse || fetchPromise;
        })
    );
});

// Listen for messages from client (e.g. check cache status)
self.addEventListener("message", (event) => {
    if (event.data && event.data.type === "CHECK_CACHE") {
        caches.open(CACHE_NAME).then(async (cache) => {
            const keys = await cache.keys();
            const hasIndex = keys.some(k => k.url.includes("index.html") || k.url.endsWith("/"));
            const hasGuide = keys.some(k => k.url.includes("script.js"));
            event.ports[0].postMessage({
                status: "ready",
                cachedCount: keys.length,
                isReady: hasIndex && hasGuide
            });
        });
    }
});
