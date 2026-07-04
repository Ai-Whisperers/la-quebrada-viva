// ==============================================
// LQV MapLibre Viewer — clean, fast, well-typed
// ==============================================
// Loads: canopy, streams, OSM (water/roads/buildings/landuse), GBIF, soil
// Basemaps: Esri hybrid, Esri aerial, OpenTopoMap
// ==============================================

(function () {
  'use strict';

  // ---- 1. MapLibre loader (handles CDN + WebGL preflight) ----
  function loadMapLibre() {
    if (window.maplibregl) return Promise.resolve(window.maplibregl);
    return new Promise((resolve, reject) => {
      // Pre-flight WebGL — fail fast if not supported
      const probe = document.createElement('canvas');
      const gl = probe.getContext('webgl') || probe.getContext('experimental-webgl');
      if (!gl) return reject(new Error('WebGL not supported'));

      const s = document.createElement('script');
      s.src = 'https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js';
      s.onload = () => resolve(window.maplibregl);
      s.onerror = () => reject(new Error('Failed to load MapLibre'));
      document.head.appendChild(s);
    });
  }

  // ---- 2. Build the map ----
  async function buildMap() {
    let maplibregl;
    try {
      maplibregl = await loadMapLibre();
    } catch (e) {
      return showFallback('Map needs WebGL. Try a desktop browser.');
    }

    const map = new maplibregl.Map({
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

    map.addControl(new maplibregl.NavigationControl({ visualizePitch: true }), 'bottom-right');
    map.addControl(new maplibregl.ScaleControl({ unit: 'metric' }), 'bottom-right');

    // ---- 3. Load each data layer ----
    const F = (p) => fetch('./data/' + p).then((r) => (r.ok ? r.json() : null)).catch(() => null);
    const COLORS = {
      canopy0: '#86efac', canopy1: '#4ade80', canopy2: '#16a34a', canopy3: '#14532d',
      stream: '#60a5fa', osm_water: '#3b82f6',
      road_primary: '#fbbf24', road_secondary: '#9ca3af',
      building: '#a3a3a3', gbif: '#f472b6',
      landuse_forest: '#065f46', landuse_farm: '#bbf7d0', landuse_grass: '#a3e635',
      camera: '#fbbf24',
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
      // Add a default GPS marker for the centroid
      map.addSource('centroid', {
        type: 'geojson',
        data: { type: 'Feature', geometry: { type: 'Point', coordinates: [-57.0355, -25.6073] }, properties: {} }
      });
      map.addLayer({ id: 'centroid-dot', type: 'circle', source: 'centroid',
        paint: { 'circle-radius': 9, 'circle-color': COLORS.camera, 'circle-stroke-color': '#000', 'circle-stroke-width': 2 }
      });

      // Add the LQV polygon (drawn from the gps boundary we shipped)
      try {
        const boundary = await F('rv_boundary.geojson');
        if (boundary) {
          map.addSource('parcel', { type: 'geojson', data: boundary });
          map.addLayer({ id: 'parcel-line', type: 'line', source: 'parcel',
            paint: { 'line-color': COLORS.camera, 'line-width': 2.5, 'line-opacity': 0.9 }
          });
        }
      } catch (e) {}

      // Add the GPS-confirmed waterfall
      map.addSource('gps-waterfall', {
        type: 'geojson',
        data: { type: 'Feature', geometry: { type: 'Point', coordinates: [-57.0264, -25.6074] },
                properties: { name: 'GPS Waterfall', altitude: 274 } }
      });
      map.addLayer({ id: 'gps-waterfall-dot', type: 'circle', source: 'gps-waterfall',
        paint: { 'circle-radius': 10, 'circle-color': '#ef4444', 'circle-stroke-color': '#fff', 'circle-stroke-width': 2.5 }
      });

      // Load each layer
      for (const [name, cfg] of Object.entries(layers)) {
        try {
          const data = await F(cfg.src);
          if (!data || !data.features || !data.features.length) continue;
          map.addSource(name, { type: 'geojson', data });

          // Detect geometry type for styling
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
          // Toggle off by default for noisy layers
          if (name === 'trees_estimated' || name === 'gbif') {
            map.setLayoutProperty(name, 'visibility', 'none');
          }
        } catch (e) { /* skip silently */ }
      }
    });

    // ---- 4. Basemap toggles ----
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

  // ---- 5. Cesium 3D viewer (the strongest visual) ----
  function buildCesium() {
    const token = window.LQV_CESIUM_ION_TOKEN;
    if (!token) return; // skip silently if no token
    if (!window.Cesium) return;

    Cesium.Ion.defaultAccessToken = token;
    const LON = -57.0355, LAT = -25.6073, ALT = 166;
    const viewer = new Cesium.Viewer('cesium-mount', {
      timeline: false, animation: false, baseLayerPicker: false, geocoder: false,
      homeButton: false, sceneModePicker: false, navigationHelpButton: false,
      fullscreenButton: false, infoBox: false, selectionIndicator: false, shadows: false,
      terrainProvider: new Cesium.EllipsoidTerrainProvider(),
    });
    viewer.imageryLayers.removeAll();
    viewer.imageryLayers.addImageryProvider(new Cesium.UrlTemplateImageryProvider({
      url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      maximumLevel: 18,
    }));
    viewer.camera.setView({
      destination: Cesium.Cartesian3.fromDegrees(LON, LAT, ALT + 800),
      orientation: { heading: 0, pitch: -Cesium.Math.toRadians(60), roll: 0 }
    });
    Cesium.createWorldTerrainAsync({}).then((t) => { viewer.terrainProvider = t; });

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

  function showFallback(msg) {
    const el = document.getElementById('maplibre-mount');
    if (el) el.innerHTML = '<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#aaa;padding:2rem;text-align:center">' + msg + '</div>';
  }

  // ---- 6. Boot ----
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => { buildMap(); buildCesium(); });
  } else {
    buildMap();
    buildCesium();
  }
})();