// LQV 10 km viewer — service worker.
// Strategy:
//   - cache-first for rasters (hillshade, color-relief, NDVI backdrop, HAND)
//   - stale-while-revalidate for GeoJSONs
//   - cache-first for shell HTML/JS/CSS
//   - cache OSM/Esri tiles with LRU eviction (max 1500 tiles)

const VERSION = 'v22';
const RASTER_CACHE = `lqv-rasters-${VERSION}`;
const GEOJSON_CACHE = `lqv-geojson-${VERSION}`;
const SHELL_CACHE   = `lqv-shell-${VERSION}`;
const TILE_CACHE    = `lqv-tiles-${VERSION}`;
const TILE_MAX = 1500;

const RASTER_PATHS = [
  '/data/hillshade_10km.jpg',
  '/data/dem_color_relief_10km.jpg',
  '/data/ndvi_canopy_10km.png',
  '/data/hand_10km.png',
];

const GEOJSON_PATHS = [
  '/data/client_gps/client_gps_polygon.geojson',
  '/data/client_gps/client_gps_corners.geojson',
  '/data/client_gps/client_gps_features.geojson',
  '/data/local_quebradas_10km.geojson',
  '/data/ndvi_canopy_10km.geojson',
  '/data/dem_streams_10km.geojson',
  '/data/dem_streams_arrows_10km.geojson',
  '/data/dem_contours_10km.geojson',
  '/data/water_combined_10km.geojson',
  '/data/surface_water_10km.geojson',
  '/data/hand_10km.geojson',
  '/data/hand_10km.png',
  '/data/local_quebradas_10km.geojson',
  '/data/ndvi_canopy_10km.png',
  '/data/mapbiomas_2023_10km.geojson',
  '/data/hansen_loss_10km.geojson',
  '/data/hansen_gain_10km.geojson',
  '/data/woodland_merged_10km.geojson',
  '/data/lqv_jrc_waterbodies_10km.geojson',
  '/data/osm_10km/roads.geojson',
  '/data/osm_10km/water.geojson',
  '/data/osm_10km/waterways.geojson',
  '/data/osm_10km/trees.geojson',
  '/data/osm_10km/buildings.geojson',
  '/data/osm_10km/places.geojson',
  '/data/osm_10km/pois.geojson',
  '/data/osm_10km/landuse.geojson',
  '/data/hillshade_bounds.json',
  '/data/dem_color_relief_bounds.json',
  '/data/ndvi_canopy_bounds.json',
];

const SHELL_PATHS = [
  '/mapa-10km.html',
  '/js/lqv-inline.js',
  '/404.html',
];

const TILE_HOSTS = [
  'tile.openstreetmap.org',
  'server.arcgisonline.com',
  'services.arcgisonline.com',
];

self.addEventListener('install', event => {
  event.waitUntil((async () => {
    const shell = await caches.open(SHELL_CACHE);
    await shell.addAll(SHELL_PATHS);
    const rast = await caches.open(RASTER_CACHE);
    await rast.addAll(RASTER_PATHS);
    self.skipWaiting();
  })());
});

self.addEventListener('activate', event => {
  event.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => !k.endsWith(VERSION))
                          .map(k => caches.delete(k)));
    self.clients.claim();
  })());
});

self.addEventListener('fetch', event => {
  const req = event.request;
  if (req.method !== 'GET') return;
  const url = new URL(req.url);

  // Tiles from map providers
  if (TILE_HOSTS.includes(url.hostname)) {
    event.respondWith(cacheFirst(TILE_CACHE, req, TILE_MAX));
    return;
  }

  if (url.origin !== self.location.origin) return;  // skip other external

  // Raster (JPG/PNG): cache-first
  if (RASTER_EXTENSIONS.some(ext => url.pathname.endsWith(ext))) {
    event.respondWith(cacheFirst(RASTER_CACHE, req));
    return;
  }
  // GeoJSON: stale-while-revalidate
  if (url.pathname.endsWith('.geojson') || GEOJSON_PATHS.includes(url.pathname)) {
    event.respondWith(staleWhileRevalidate(GEOJSON_CACHE, req));
    return;
  }
  // Shell: cache-first
  if (url.pathname.endsWith('.html') || url.pathname.endsWith('.js')
      || url.pathname.endsWith('.css')) {
    event.respondWith(cacheFirst(SHELL_CACHE, req));
    return;
  }
  // Other: network only
});

async function cacheFirst(cacheName, req, maxEntries) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(req);
  if (cached) return cached;
  try {
    const resp = await fetch(req);
    if (resp.ok) {
      cache.put(req, resp.clone());
      if (maxEntries) await trimCache(cache, maxEntries);
    }
    return resp;
  } catch (e) {
    return new Response('Offline', { status: 503 });
  }
}

async function staleWhileRevalidate(cacheName, req) {
  const cache = await caches.open(cacheName);
  const cached = await cache.match(req);
  const fetchPromise = fetch(req).then(resp => {
    if (resp.ok) cache.put(req, resp.clone());
    return resp;
  }).catch(() => cached);
  return cached || fetchPromise;
}

// LRU eviction for tile cache (keep last maxEntries).
async function trimCache(cache, maxEntries) {
  const keys = await cache.keys();
  if (keys.length <= maxEntries) return;
  const toDelete = keys.length - maxEntries;
  for (let i = 0; i < toDelete; i++) {
    await cache.delete(keys[i]);
  }
}