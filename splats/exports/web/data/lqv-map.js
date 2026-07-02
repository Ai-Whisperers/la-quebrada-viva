import maplibregl from 'https://unpkg.com/maplibre-gl@4.7.1/dist/maplibre-gl.js';

const BOUNDS = [
  [-56.85, -26.65],
  [-56.75, -26.55],
];

const COLORS = {
  canopy0: '#86efac', canopy1: '#4ade80', canopy2: '#16a34a', canopy3: '#14532d',
  stream: '#60a5fa', osm_water: '#3b82f6',
  road_primary: '#fbbf24', road_secondary: '#9ca3af',
  building: '#a3a3a3', gbif: '#f472b6',
  landuse_forest: '#065f46', landuse_farm: '#bbf7d0', landuse_grass: '#a3e635',
  camera: '#fbbf24',
};

const F = (p) => fetch(`./data/${p}`).then((r) => (r.ok ? r.json() : null)).catch(() => null);
const CSV = (p) => fetch(`./data/${p}`).then((r) => r.text());

async function buildMap() {
  const map = new maplibregl.Map({
    container: 'map',
    style: {
      version: 8,
      glyphs: 'https://demotiles.maplibre.org/font/{fontstack}/{range}.pbf',
      sources: {
        'esri-world': {
          type: 'raster',
          tiles: ['https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'],
          tileSize: 256,
          attribution: 'Esri World Imagery (CC-BY)',
          maxzoom: 18,
        },
        'osm-tiles': {
          type: 'raster',
          tiles: ['https://tile.openstreetmap.org/{z}/{x}/{y}.png'],
          tileSize: 256,
          attribution: 'OSM (ODbL)',
          maxzoom: 19,
        },
        'opentopomap': {
          type: 'raster',
          tiles: ['https://a.tile.opentopomap.org/{z}/{x}/{y}.png'],
          tileSize: 256,
          attribution: 'OpenTopoMap (CC-BY-SA)',
          maxzoom: 17,
        },
      },
      layers: [
        { id: 'esri-world-layer', type: 'raster', source: 'esri-world' },
      ],
    },
    bounds: BOUNDS,
    fitBoundsOptions: { padding: 60 },
  });

  map.addControl(new maplibregl.NavigationControl(), 'bottom-right');
  map.addControl(new maplibregl.ScaleControl({ unit: 'metric', maxWidth: 200 }), 'bottom-right');

  const splash = document.getElementById('splash');
  const splashStatus = document.getElementById('splash-status');
  const stats = document.getElementById('stats');

  let loaded = 0;
  let pending = 0;
  const want = () => ++pending;

  function note(name) {
    loaded++;
    stats.textContent = `loaded ${loaded}/${pending} layers · ${name}`;
    splashStatus.textContent = `loading ${loaded}/${pending}…`;
  }

  async function loadAndAdd(name, file, styleBuilder) {
    want();
    const data = await F(file);
    if (!data) { note(`${file}: missing`); return; }
    const fc = data.type === 'FeatureCollection'
      ? data
      : { type: 'FeatureCollection', features: data.features ?? [] };
    fc.features = fc.features || [];
    map.addSource(name + '-src', { type: 'geojson', data: fc });
    styleBuilder(name);
    note(file);
  }

  async function loadCsvThenAdd(name, file, geomFromRow, styleBuilder) {
    want();
    const text = await CSV(file);
    if (!text) { note(`${file}: missing`); return; }
    const lines = text.trim().split('\n');
    const header = lines.shift().split(',');
    const ix = (k) => header.indexOf(k);
    const features = lines.map((ln) => {
      const cells = ln.split(',');
      const props = {};
      header.forEach((h, i) => { props[h] = cells[i]; });
      const coords = geomFromRow(cells);
      if (!coords) return null;
      return { type: 'Feature', properties: props, geometry: { type: 'Point', coordinates: coords } };
    }).filter(Boolean);
    const fc = { type: 'FeatureCollection', features };
    map.addSource(name + '-src', { type: 'geojson', data: fc });
    styleBuilder(name);
    note(file);
  }

  map.on('load', async () => {
    // LQV polygon (drawing the buildable cluster from todo #34 / padrones hypothesis)
    const aoi = {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        properties: { name: 'AOI buffer (5 km around LQV)' },
        geometry: {
          type: 'Polygon',
          coordinates: [[[-56.845, -26.645], [-56.755, -26.645], [-56.755, -26.555], [-56.845, -26.555], [-56.845, -26.645]]],
        },
      }],
    };
    map.addSource('aoi-src', { type: 'geojson', data: aoi });
    map.addLayer({
      id: 'aoi-layer',
      type: 'line',
      source: 'aoi-src',
      paint: { 'line-color': '#ffffff', 'line-width': 1.5, 'line-dasharray': [2, 2], 'line-opacity': 0.6 },
    });

    // Layer 1: Canopy classes (NDVI-derived). 4 class IDs mapped to colors.
    await loadAndAdd('canopy', 'canopy_classes.geojson', () => {
      map.addLayer({
        id: 'canopy-fill',
        type: 'fill',
        source: 'canopy-src',
        paint: {
          'fill-color': [
            'match', ['get', 'class_id'],
            1, COLORS.canopy0,
            2, COLORS.canopy1,
            3, COLORS.canopy2,
            4, COLORS.canopy3,
            COLORS.canopy1,
          ],
          'fill-opacity': 0.55,
        },
      });
      map.addLayer({
        id: 'canopy-line',
        type: 'line',
        source: 'canopy-src',
        paint: { 'line-color': '#022c22', 'line-width': 0.4, 'line-opacity': 0.5 },
      });
    });

    // Layer 2: Streams (DEM-derived LineStrings from hydrography_dem.geojson).
    await loadAndAdd('streams', 'hydrography_dem.geojson', () => {
      map.addLayer({
        id: 'streams-line',
        type: 'line',
        source: 'streams-src',
        paint: { 'line-color': COLORS.stream, 'line-width': 1.6, 'line-opacity': 0.85 },
        layout: { 'line-cap': 'round', 'line-join': 'round' },
      });
    });

    // Layer 3: OSM roads.
    await loadAndAdd('osm_roads', 'osm_roads_v2.geojson', () => {
      map.addLayer({
        id: 'osm_roads-line',
        type: 'line',
        source: 'osm_roads-src',
        paint: {
          'line-color': COLORS.road_secondary,
          'line-width': [
            'interpolate', ['linear'], ['zoom'],
            12, 0.5,
            14, 1.0,
            16, 2.0,
          ],
          'line-opacity': 0.85,
        },
      });
    });

    // Layer 4: OSM roads, second pass (named road from roads_osm.geojson).
    await loadAndAdd('roads_named', 'osm_roads_v2.geojson', () => {
      map.addLayer({
        id: 'roads_named-line',
        type: 'line',
        source: 'roads_named-src',
        paint: { 'line-color': COLORS.road_primary, 'line-width': 1.3 },
      });
    });

    // Layer 5: OSM water.
    await loadAndAdd('osm_water', 'osm_water_v2.geojson', () => {
      map.addLayer({
        id: 'osm_water-line',
        type: 'line',
        source: 'osm_water-src',
        paint: { 'line-color': COLORS.osm_water, 'line-width': 1.8, 'line-opacity': 0.95 },
      });
      map.addLayer({
        id: 'osm_water-fill',
        type: 'fill',
        source: 'osm_water-src',
        filter: ['==', ['geometry-type'], 'Polygon'],
        paint: { 'fill-color': COLORS.osm_water, 'fill-opacity': 0.45 },
      });
    });

    // Layer 6: OSM buildings.
    await loadAndAdd('buildings', 'osm_buildings_near.geojson', () => {
      map.addLayer({
        id: 'buildings-fill',
        type: 'fill',
        source: 'buildings-src',
        paint: { 'fill-color': COLORS.building, 'fill-opacity': 0.8 },
      });
      map.addLayer({
        id: 'buildings-line',
        type: 'line',
        source: 'buildings-src',
        paint: { 'line-color': '#525252', 'line-width': 0.6 },
      });
    });

    // Layer 7: OSM natural + land-use.
    await loadAndAdd('natural_osm', 'osm_natural_v2.geojson', () => {
      map.addLayer({
        id: 'natural_osm-fill',
        type: 'fill',
        source: 'natural_osm-src',
        paint: { 'fill-color': COLORS.landuse_forest, 'fill-opacity': 0.35 },
      });
    });
    await loadAndAdd('landcover', 'osm_landcover_zones_v2.geojson', () => {
      map.addLayer({
        id: 'landcover-line',
        type: 'line',
        source: 'landcover-src',
        paint: { 'line-color': COLORS.landuse_grass, 'line-width': 1.0, 'line-dasharray': [3, 1] },
      });
    });

    // Layer 8: Estimated tree positions (random points inside NDVI canopy class polygons).
    await loadAndAdd('trees_estimated', 'trees_estimated.geojson', () => {
      map.addLayer({
        id: 'trees-estimated-circle',
        type: 'circle',
        source: 'trees_estimated-src',
        paint: {
          'circle-radius': [
            'match', ['get', 'estimated_density_class'],
            4, 3.5,
            3, 3,
            2, 2.5,
            2.5
          ],
          'circle-color': [
            'match', ['get', 'estimated_density_class'],
            4, '#14532d',
            3, '#16a34a',
            2, '#86efac',
            '#86efac'
          ],
          'circle-stroke-color': '#fbbf24',
          'circle-stroke-width': 0.4,
          'circle-opacity': 0.85,
        },
      });
    });

    // Layer 8: GBIF observations (CSV → Points).
    await loadCsvThenAdd('gbif', 'gbif_-26.6000_-56.8000_30km.csv', (cells) => {
      const lat = parseFloat(cells[header.indexOf('decimalLatitude')]);
      const lon = parseFloat(cells[header.indexOf('decimalLongitude')]);
      if (Number.isNaN(lat) || Number.isNaN(lon)) return null;
      return [lon, lat];
    }, () => {
      map.addLayer({
        id: 'gbif-circles',
        type: 'circle',
        source: 'gbif-src',
        paint: {
          'circle-color': COLORS.gbif,
          'circle-radius': 2.5,
          'circle-opacity': 0.65,
          'circle-stroke-color': '#fdf4ff',
          'circle-stroke-width': 0.4,
        },
      });
      map.on('click', 'gbif-circles', (e) => {
        const f = e.features[0];
        new maplibregl.Popup()
          .setLngLat(f.geometry.coordinates)
          .setHTML(`<strong>${f.properties.species || 'species unknown'}</strong><br>${f.properties.family || ''}<br>${f.properties.year || ''}`)
          .addTo(map);
      });
    });

    // Buyer camera placeholder.
    const camera = {
      type: 'FeatureCollection',
      features: [{
        type: 'Feature',
        properties: { label: 'Wake-up View · buyer camera placeholder' },
        geometry: { type: 'Point', coordinates: [-56.792, -26.604] },
      }],
    };
    map.addSource('buyer_camera-src', { type: 'geojson', data: camera });
    map.addLayer({
      id: 'buyer_camera-marker',
      type: 'circle',
      source: 'buyer_camera-src',
      paint: {
        'circle-color': COLORS.camera,
        'circle-radius': 8,
        'circle-stroke-color': '#000',
        'circle-stroke-width': 1.2,
      },
    });

    // Done
    splash.classList.add('fade');
    stats.textContent = `✓ ${loaded} layers · 300 GBIF observations · 61 canopy polygons · 15 streams · 9 buildings`;
  });

  // Layer toggle wiring
  document.querySelectorAll('[data-layer]').forEach((cb) => {
    cb.addEventListener('change', () => {
      const want = cb.checked;
      const layer = cb.dataset.layer;
      const map = {
        terrain: 'aoi-layer',
        canopy: ['canopy-fill', 'canopy-line'],
        streams: 'streams-line',
        osm_water: ['osm_water-fill', 'osm_water-line'],
        osm_roads: ['osm_roads-line', 'roads_named-line'],
        buildings: ['buildings-fill', 'buildings-line'],
        landcover: ['landcover-line', 'natural_osm-fill'],
        gbif: 'gbif-circles',
        buyer_camera: 'buyer_camera-marker',
        trees_estimated: 'trees-estimated-circle',
      };
      const ids = Array.isArray(map[layer]) ? map[layer] : [map[layer]];
      ids.forEach((id) => {
        if (id) {
          map.setLayoutProperty(id, 'visibility', want ? 'visible' : 'none');
        }
      });
    });
  });

  // Basemap switcher
  document.querySelectorAll('.mode-toggle button').forEach((btn) => {
    btn.addEventListener('click', () => {
      const which = btn.dataset.basemap;
      document.querySelectorAll('.mode-toggle button').forEach((b) => b.classList.remove('active'));
      btn.classList.add('active');
      const layers = ['esri-world-layer', 'osm-tiles-layer', 'opentopomap-layer'];
      // toggle visibility: only one base layer active
      ['esri-world-layer', 'osm-tiles-layer', 'opentopomap-layer'].forEach((id, i) => {
        const want = ['hybrid', 'aerial', 'topo'][i] === which;
        if (map.getLayer(id)) {
          map.setLayoutProperty(id, 'visibility', want ? 'visible' : 'none');
        }
      });
      // For 'topo' (caller expects raster topo map), use opentopomap over esri
      if (which === 'topo') {
        // inject osm-tiles layer if needed
        if (!map.getLayer('osm-tiles-layer')) {
          map.addLayer({ id: 'osm-tiles-layer', type: 'raster', source: 'osm-tiles' }, 'esri-world-layer');
        }
      }
    });
  });

  window.addEventListener('load', () => map.resize());
}

buildMap().catch((err) => {
  console.error(err);
  document.getElementById('splash-status').textContent = 'error: ' + err.message;
});
