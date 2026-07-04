// ==============================================
// LQV MapLibre Viewer + Cesium 3D — with WebGL fallback
// ==============================================
// For the main buyer walkthrough page.
// 2D: MapLibre (with WebGL). If no WebGL → Leaflet fallback.
// 3D: Cesium (requires WebGL). If no WebGL → static hero image.
// ==============================================

(function () {
  'use strict';

  // ---- WebGL preflight ----
  // Cesium needs full WebGL2 OR WebGL with depth+stencil. Just probing basic
  // WebGL isn't enough — we need to test the full context attributes Cesium uses.
  function detectWebGL() {
    try {
      // Test 1: basic WebGL context
      const probe = document.createElement('canvas');
      let gl = probe.getContext('webgl2')
            || probe.getContext('webgl')
            || probe.getContext('experimental-webgl');
      if (!gl) return false;
      // Test 2: can we get depth + stencil buffers (Cesium needs these)
      const attrs = gl.getContextAttributes();
      if (attrs && attrs.depth === false) return false;
      // Test 3: try to allocate a small render buffer
      const rb = gl.createRenderbuffer();
      if (!rb) return false;
      gl.bindRenderbuffer(gl.RENDERBUFFER, rb);
      try {
        gl.renderbufferStorage(gl.RENDERBUFFER, gl.DEPTH_STENCIL, 1, 1);
      } catch (e) {
        return false;
      }
      gl.deleteRenderbuffer(rb);
      // Test 4: try to compile a simple shader (Cesium uses shaders a lot)
      const vs = gl.createShader(gl.VERTEX_SHADER);
      gl.shaderSource(vs, 'attribute vec2 p;void main(){gl_Position=vec4(p,0,1);}');
      gl.compileShader(vs);
      const compiled = gl.getShaderParameter(vs, gl.COMPILE_STATUS);
      gl.deleteShader(vs);
      if (!compiled) return false;
      return true;
    } catch (e) {
      return false;
    }
  }

  const HAS_WEBGL = detectWebGL();
  const F = (p) => fetch('./data/' + p).then((r) => (r.ok ? r.json() : null)).catch(() => null);

  // ---- 1. MapLibre loader ----
  function loadMapLibre() {
    if (!HAS_WEBGL) return Promise.reject(new Error('WebGL not supported'));
    if (window.maplibregl) return Promise.resolve(window.maplibregl);
    // Load CSS first
    if (!document.getElementById('maplibre-css')) {
      const link = document.createElement('link');
      link.id = 'maplibre-css';
      link.rel = 'stylesheet';
      link.href = 'https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.css';
      document.head.appendChild(link);
    }
    return loadScript('https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js', { checkGlobal: 'maplibregl' });
  }

  // ---- 2. Leaflet fallback (CSS-based, no WebGL) ----
  function buildLeafletFallback() {
    if (document.getElementById('leaflet-css') === null) {
      const link = document.createElement('link');
      link.id = 'leaflet-css';
      link.rel = 'stylesheet';
      link.href = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.css';
      link.crossOrigin = '';
      document.head.appendChild(link);
    }
    const s = document.createElement('script');
    s.src = 'https://unpkg.com/leaflet@1.9.4/dist/leaflet.js';
    s.crossOrigin = '';
    s.onload = function () {
      const L = window.L;
      if (!L) return;
      const map = L.map('maplibre-mount', {
        center: [-25.6073, -57.0355],
        zoom: 15,
        zoomControl: true,
      });
      // Default: Esri satellite
      L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
        maxZoom: 19, attribution: 'Esri World Imagery (CC-BY)'
      }).addTo(map);

      // Boundary
      F('rv_boundary.geojson').then((b) => {
        if (b) L.geoJSON(b, { style: { color: '#d4a154', weight: 2.5, fillOpacity: 0 }}).addTo(map);
      });

      // Load all data
      const layers = {
        canopy:    { src: 'canopy_classes.geojson',        color: '#4ade80', fillOpacity: 0.5 },
        streams:   { src: 'hydrography_dem_v2.geojson',     color: '#60a5fa', fillOpacity: 0.85 },
        osm_water: { src: 'osm_water_v2.geojson',           color: '#3b82f6' },
        osm_roads: { src: 'osm_roads_v2.geojson',           color: '#fbbf24', lineWidth: 2 },
        buildings: { src: 'osm_buildings_near.geojson',     color: '#a3a3a3', fillOpacity: 0.5 },
        landcover: { src: 'osm_landcover_zones_v2.geojson', color: '#065f46', fillOpacity: 0.3 },
      };
      Object.entries(layers).forEach(([name, cfg]) => {
        F(cfg.src).then((data) => {
          if (!data || !data.features || !data.features.length) return;
          const t = data.features[0].geometry.type;
          const style = {};
          if (t === 'Polygon' || t === 'MultiPolygon') {
            style.color = cfg.color; style.fillColor = cfg.color; style.fillOpacity = cfg.fillOpacity || 0.4; style.weight = 1;
          } else if (t === 'LineString' || t === 'MultiLineString') {
            style.color = cfg.color; style.weight = cfg.lineWidth || 1.5; style.opacity = 0.85;
          }
          const layer = L.geoJSON(data, { style });
          // Don't add by default for noisy ones
          // Actually for buyer walkthrough, add all by default
          layer.addTo(map);
        });
      });

      // Wire basemap toggles
      const baseMaps = {
        hybrid: L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { maxZoom: 19 }),
        aerial: L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { maxZoom: 19 }),
        topo: L.tileLayer('https://a.tile.opentopomap.org/{z}/{x}/{y}.png', { maxZoom: 17 }),
      };
      // For now just use Esri for everything (since hybrid/aerial are the same here)
      document.querySelectorAll('[data-basemap]').forEach((btn) => {
        btn.addEventListener('click', () => {
          document.querySelectorAll('[data-basemap]').forEach((b) => b.classList.remove('active'));
          btn.classList.add('active');
          const which = btn.dataset.basemap;
          if (which === 'topo') {
            Object.values(baseMaps).forEach((layer) => { if (map.hasLayer(layer)) map.removeLayer(layer); });
            baseMaps.topo.addTo(map);
          } else {
            Object.values(baseMaps).forEach((layer) => { if (map.hasLayer(layer)) map.removeLayer(layer); });
            baseMaps.hybrid.addTo(map);
          }
        });
      });
    };
    s.onerror = function () {
      const el = document.getElementById('maplibre-mount');
      if (el) el.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#aaa;padding:2rem;text-align:center;font-family:sans-serif">Interactive map unavailable. All data is downloadable.</div>';
    };
    document.head.appendChild(s);
  }

  // ---- 3. MapLibre 2D map ----
  async function buildMap() {
    let maplibregl;
    try {
      maplibregl = await loadMapLibre();
    } catch (e) {
      console.warn('[LQV] MapLibre unavailable — falling back to Leaflet:', e.message);
      buildLeafletFallback();
      return;
    }

    let map;
    try {
      map = new maplibregl.Map({
        container: 'maplibre-mount',
        style: {
          version: 8,
          sources: {
            'esri-hybrid': {
              type: 'raster',
              tiles: ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'],
              tileSize: 256, attribution: 'Esri Hybrid'
            },
            'esri-aerial': {
              type: 'raster',
              tiles: ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'],
              tileSize: 256, attribution: 'Esri Aerial'
            },
            'opentopomap': {
              type: 'raster',
              tiles: ['https://a.tile.opentopomap.org/{z}/{x}/{y}.png'],
              tileSize: 256, attribution: 'OpenTopoMap (CC-BY-SA)'
            },
          },
          layers: [{ id: 'base', type: 'raster', source: 'esri-hybrid' }],
        },
        center: [-57.0355, -25.6073],
        zoom: 15,
        maxZoom: 19,
      });
    } catch (e) {
      console.warn('[LQV] MapLibre constructor failed — falling back to Leaflet:', e.message);
      buildLeafletFallback();
      return;
    }

    map.on('error', (e) => console.warn('[LQV] MapLibre error:', e && e.error));

    map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), 'bottom-right');
    map.addControl(new maplibregl.ScaleControl({ unit: 'metric' }), 'bottom-right');

    const COLORS = {
      canopy1: '#4ade80', stream: '#60a5fa', osm_water: '#3b82f6',
      road_primary: '#fbbf24', building: '#a3a3a3',
      landuse_forest: '#065f46', camera: '#fbbf24',
    };

    const layers = {
      canopy:    { src: 'canopy_classes.geojson',        color: COLORS.canopy1, fillOpacity: 0.5 },
      streams:   { src: 'hydrography_dem_v2.geojson',     color: COLORS.stream,  fillOpacity: 0.85 },
      osm_water: { src: 'osm_water_v2.geojson',           color: COLORS.osm_water },
      osm_roads: { src: 'osm_roads_v2.geojson',           color: COLORS.road_primary, lineWidth: 2 },
      buildings: { src: 'osm_buildings_near.geojson',     color: COLORS.building, fillOpacity: 0.5 },
      landcover: { src: 'osm_landcover_zones_v2.geojson', color: COLORS.landuse_forest, fillOpacity: 0.3 },
      trees_estimated: { src: 'trees_estimated.geojson', color: '#86efac' },
    };

    map.on('load', async () => {
      // Centroid marker
      map.addSource('centroid', {
        type: 'geojson',
        data: { type: 'Feature', geometry: { type: 'Point', coordinates: [-57.0355, -25.6073] }, properties: {} }
      });
      map.addLayer({ id: 'centroid-dot', type: 'circle', source: 'centroid',
        paint: { 'circle-radius': 9, 'circle-color': COLORS.camera, 'circle-stroke-color': '#000', 'circle-stroke-width': 2 }
      });

      // Boundary
      try {
        const boundary = await F('rv_boundary.geojson');
        if (boundary) {
          map.addSource('parcel', { type: 'geojson', data: boundary });
          map.addLayer({ id: 'parcel-line', type: 'line', source: 'parcel',
            paint: { 'line-color': COLORS.camera, 'line-width': 2.5, 'line-opacity': 0.9 }
          });
        }
      } catch (e) {}

      // GPS waterfall
      map.addSource('gps-waterfall', {
        type: 'geojson',
        data: { type: 'Feature', geometry: { type: 'Point', coordinates: [-57.0264, -25.6074] },
                properties: { name: 'GPS Waterfall', altitude: 274 } }
      });
      map.addLayer({ id: 'gps-waterfall-dot', type: 'circle', source: 'gps-waterfall',
        paint: { 'circle-radius': 10, 'circle-color': '#ef4444', 'circle-stroke-color': '#fff', 'circle-stroke-width': 2.5 }
      });

      // Load layers
      for (const [name, cfg] of Object.entries(layers)) {
        try {
          const data = await F(cfg.src);
          if (!data || !data.features || !data.features.length) continue;
          map.addSource(name, { type: 'geojson', data });
          const t = data.features[0].geometry.type;
          if (t === 'Polygon' || t === 'MultiPolygon') {
            map.addLayer({ id: name, type: 'fill', source: name,
              paint: { 'fill-color': cfg.color, 'fill-opacity': cfg.fillOpacity || 0.4 }
            });
          } else if (t === 'LineString' || t === 'MultiLineString') {
            map.addLayer({ id: name, type: 'line', source: name,
              paint: { 'line-color': cfg.color, 'line-width': cfg.lineWidth || 1.5, 'line-opacity': 0.85 }
            });
          } else if (t === 'Point') {
            map.addLayer({ id: name, type: 'circle', source: name,
              paint: { 'circle-radius': 4, 'circle-color': cfg.color, 'circle-opacity': 0.8 }
            });
          }
          if (name === 'trees_estimated' || name === 'gbif') {
            map.setLayoutProperty(name, 'visibility', 'none');
          }
        } catch (e) {}
      }
    });

    // Basemap toggles
    document.querySelectorAll('[data-basemap]').forEach((btn) => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('[data-basemap]').forEach((b) => b.classList.remove('active'));
        btn.classList.add('active');
        const layer = btn.dataset.basemap;
        const sourceMap = { hybrid: 'esri-hybrid', aerial: 'esri-aerial', topo: 'opentopomap' };
        const newSrc = sourceMap[layer];
        if (newSrc && map.getLayer('base')) {
          map.setLayoutProperty('base', 'visibility', 'none');
          if (!map.getLayer(layer)) {
            map.addLayer({ id: layer, type: 'raster', source: newSrc });
          } else {
            map.setLayoutProperty(layer, 'visibility', 'visible');
          }
        }
      });
    });
  }

  // ---- Script loaders (Cesium + MapLibre) ----
  function loadScript(src, attrs = {}) {
    return new Promise((resolve, reject) => {
      // Already loaded?
      if (attrs.checkGlobal && window[attrs.checkGlobal]) return resolve(window[attrs.checkGlobal]);
      const s = document.createElement('script');
      s.src = src;
      if (attrs.integrity) { s.integrity = attrs.integrity; s.crossOrigin = ''; }
      s.onload = () => resolve(attrs.checkGlobal ? window[attrs.checkGlobal] : true);
      s.onerror = () => reject(new Error('Failed to load ' + src));
      document.head.appendChild(s);
    });
  }

  // ---- Cesium 3D viewer ----
  async function buildCesium() {
    // Re-check WebGL fresh (the cached HAS_WEBGL might be stale)
    if (!detectWebGL()) {
      const mount = document.getElementById('cesium-mount');
      if (mount) {
        mount.innerHTML = '<div style="position:relative;width:100%;height:100%;background:linear-gradient(135deg,#1a2a1a 0%,#0a1a2a 100%);display:flex;align-items:center;justify-content:center"><div style="text-align:center;padding:2rem"><h3 style="color:#d4a154;margin-bottom:1rem;font-family:Cormorant Garamond,serif;font-size:1.8rem">3D viewer needs WebGL</h3><p style="color:#aaa;max-width:400px;margin:0 auto">Your browser has WebGL disabled or in a sandboxed environment. All data is downloadable below.</p></div></div>';
      }
      return;
    }
    const token = window.LQV_CESIUM_ION_TOKEN;
    if (!token) return;

    // Load Cesium + widgets CSS on demand
    let Cesium;
    try {
      if (!document.getElementById('cesium-css')) {
        const link = document.createElement('link');
        link.id = 'cesium-css';
        link.rel = 'stylesheet';
        link.href = 'https://cdn.jsdelivr.net/npm/cesium@1.121/Build/Cesium/Widgets/widgets.css';
        document.head.appendChild(link);
      }
      Cesium = await loadScript('https://cdn.jsdelivr.net/npm/cesium@1.121/Build/Cesium/Cesium.js', { checkGlobal: 'Cesium' });
      if (!Cesium || !Cesium.Viewer) throw new Error('Cesium did not initialize');
    } catch (e) {
      console.warn('[LQV] Cesium failed to load:', e.message);
      const mount = document.getElementById('cesium-mount');
      if (mount) {
        mount.innerHTML = '<div style="position:relative;width:100%;height:100%;background:linear-gradient(135deg,#1a2a1a 0%,#0a1a2a 100%);display:flex;align-items:center;justify-content:center"><div style="text-align:center;padding:2rem"><h3 style="color:#d4a154;margin-bottom:1rem;font-family:Cormorant Garamond,serif;font-size:1.8rem">3D viewer unavailable</h3><p style="color:#aaa;max-width:400px;margin:0 auto">Could not load Cesium in this environment. The 2D map below shows the same data.</p></div></div>';
      }
      return;
    }

    let viewer;
    try {
      Cesium.Ion.defaultAccessToken = token;
      const LON = -57.0355, LAT = -25.6073, ALT = 166;
      viewer = new Cesium.Viewer('cesium-mount', {
        timeline: false, animation: false, baseLayerPicker: false, geocoder: false,
        homeButton: false, sceneModePicker: false, navigationHelpButton: false,
        fullscreenButton: false, infoBox: false, selectionIndicator: false, shadows: false,
        terrainProvider: new Cesium.EllipsoidTerrainProvider(),
      });
    } catch (e) {
      console.warn('[LQV] Cesium construction failed:', e.message);
      const mount = document.getElementById('cesium-mount');
      if (mount) {
        mount.innerHTML = '<div style="position:relative;width:100%;height:100%;background:linear-gradient(135deg,#1a2a1a 0%,#0a1a2a 100%);display:flex;align-items:center;justify-content:center"><div style="text-align:center;padding:2rem"><h3 style="color:#d4a154;margin-bottom:1rem;font-family:Cormorant Garamond,serif;font-size:1.8rem">3D viewer unavailable</h3><p style="color:#aaa;max-width:400px;margin:0 auto">Your browser is in a sandboxed environment. The 2D map and the static renders below show the same data.</p></div></div>';
      }
      return;
    }
    // If construction succeeded, set up the viewer
    try {
      viewer.imageryLayers.removeAll();
      viewer.imageryLayers.addImageryProvider(new Cesium.UrlTemplateImageryProvider({
        url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
        maximumLevel: 18,
      }));
      const LON = -57.0355, LAT = -25.6073, ALT = 166;
      viewer.camera.setView({
        destination: Cesium.Cartesian3.fromDegrees(LON, LAT, ALT + 800),
        orientation: { heading: 0, pitch: -Cesium.Math.toRadians(60), roll: 0 }
      });
      Cesium.createWorldTerrainAsync({}).then((t) => { viewer.terrainProvider = t; });
    } catch (e) {
      console.warn('[LQV] Cesium setup partial:', e.message);
    }

    let flyAround = null;
    document.querySelectorAll('[data-cesium-action]').forEach((btn) => {
      btn.addEventListener('click', () => {
        const a = btn.dataset.cesiumAction;
        if (a === 'fly-lqv') {
          if (flyAround) { viewer.clock.onTick.removeEventListener(flyAround); flyAround = null; }
          viewer.camera.flyTo({
            destination: Cesium.Cartesian3.fromDegrees(LON, LAT, ALT + 400),
            orientation: { heading: 0, pitch: -Cesium.Math.toRadians(35), roll: 0 },
            duration: 1.8,
          });
          btn.parentElement.querySelectorAll('.map-btn').forEach(b => b.classList.remove('active'));
          btn.classList.add('active');
        } else if (a === 'fly-around') {
          if (flyAround) return;
          const t0 = Date.now();
          flyAround = () => {
            const s = (Date.now() - t0) / 1000;
            const a = s * 0.04;
            viewer.camera.setView({
              destination: Cesium.Cartesian3.fromDegrees(LON + Math.cos(a) * 0.006, LAT + Math.sin(a) * 0.006, ALT + 350),
              orientation: { heading: a + Math.PI, pitch: -Cesium.Math.toRadians(30), roll: 0 }
            });
            if (s > 240) { viewer.clock.onTick.removeEventListener(flyAround); flyAround = null; }
          };
          viewer.clock.onTick.addEventListener(flyAround);
        } else if (a === 'toggle-imagery') {
          const layers = viewer.imageryLayers;
          const cur = layers.get(0);
          const isEsri = cur && cur.imageryProvider && cur.imageryProvider.url && cur.imageryProvider.url.includes('arcgisonline');
          layers.removeAll();
          if (isEsri) {
            layers.addImageryProvider(new Cesium.UrlTemplateImageryProvider({ url: 'https://tile.openstreetmap.org/{z}/{x}/{y}.png', maximumLevel: 18 }));
          } else {
            layers.addImageryProvider(new Cesium.UrlTemplateImageryProvider({ url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', maximumLevel: 18 }));
          }
        } else if (a === 'toggle-terrain') {
          const isFlat = viewer.terrainProvider instanceof Cesium.EllipsoidTerrainProvider;
          viewer.terrainProvider = isFlat ? Cesium.createWorldTerrain() : new Cesium.EllipsoidTerrainProvider();
        } else if (a === 'fullscreen') {
          const c = document.getElementById('cesium-mount');
          if (!document.fullscreenElement) c.requestFullscreen(); else document.exitFullscreen();
        }
      });
    });
  }

  // ---- Boot ----
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => { buildMap(); buildCesium(); });
  } else {
    buildMap();
    buildCesium();
  }
})();
