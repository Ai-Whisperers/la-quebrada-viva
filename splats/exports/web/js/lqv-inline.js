/* eslint-disable */
// ==============================================
// LQV 10km context map — extracted from mapa-10km.html
// Loaded as a regular <script> before the inline boot script.
// All symbols attached to window.LQV.
// ==============================================
(function () {
'use strict';
// ==============================================
// LQV 10km context map — uses CLIENT-PROVIDED GPS
// perimeter (Guru Maps walk 2026-06-22 + 2026-06-28)
// ==============================================

const F = (p) => fetch(p).then(r => r.ok ? r.json() : null).catch(e => { console.warn('fetch failed', p, e); return null; });

// Centroid of the CLIENT-PROVIDED GPS polygon (17 pts walked on-site)
// supersedes the older 8-vertex KML polygon — see README in client_gps/
// Computed from docs/site_data/property_gps_walk_2026-06-28/guru_maps_geojson.json
//   vertices = 17   area = 71.37 ha   perimeter = 4.26 km
//   bbox = lon -57.036..-57.026,  lat -25.616..-25.603
//   centroid = -57.030381, -25.608231
const LON = -57.030381;
const LAT = -25.608231;
const CENTER = [LAT, LON];

// 10km radius bbox around the GPS centroid (-57.030, -25.608).
// 10 km at lat=-25.6 is 0.0898° lat × 0.0996° lon.
const BBOX_10KM = [
  [LAT - 0.0898, LON - 0.0996],
  [LAT + 0.0898, LON + 0.0996],
];

// ---- Map init ----
const map = L.map('map', {
  center: CENTER,
  zoom: 13,
  zoomControl: true,
  preferCanvas: true,
  worldCopyJump: false,
  // Auto-declutter overlapping labels at low zooms
  // (Leaflet 1.9 only declutters canvas renderers — that's OK, we use canvas)
});

// Fix default Leaflet icon path (broken with bundlers / CDN)
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  iconUrl:       'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  shadowUrl:     'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
});

// Basemaps
const baseEsri = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', { maxZoom: 19, attribution: 'Esri World Imagery' });
const baseTopo = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}', { maxZoom: 19, attribution: 'Esri Topographic' });
const baseOSM  = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19, attribution: '© OpenStreetMap' });

let currentBase = baseEsri.addTo(map);

function switchBase(layer, btnId) {
  map.removeLayer(currentBase);
  currentBase = layer.addTo(map);
  ['basemap-esri','basemap-topo','basemap-osm'].forEach(id => {
    document.getElementById(id).classList.toggle('active', id === btnId);
  });
}
document.getElementById('basemap-esri').onclick = () => switchBase(baseEsri, 'basemap-esri');
document.getElementById('basemap-topo').onclick = () => switchBase(baseTopo, 'basemap-topo');
document.getElementById('basemap-osm').onclick  = () => switchBase(baseOSM,  'basemap-osm');

map.fitBounds(BBOX_10KM, { padding: [20, 20] });
L.control.scale({ imperial: false, position: 'bottomright' }).addTo(map);

// ---- Layers ----
const layers = {};   // name → Leaflet layer (or cluster group)
const data   = {};   // name → GeoJSON FeatureCollection
const labels = {};   // name → array of { lyr, opts } for permanent tooltips

let totalFeatures = 0;

// ---- Styles ----
function roadStyle(feature) {
  const h = feature.properties.highway || '';
  const map_ = {
    trunk:        { color: '#dc2626', weight: 4,   opacity: 0.95, dashArray: null },
    primary:      { color: '#ea580c', weight: 3.5, opacity: 0.95, dashArray: null },
    secondary:    { color: '#f59e0b', weight: 3,   opacity: 0.95, dashArray: null },
    tertiary:     { color: '#facc15', weight: 2.5, opacity: 0.95, dashArray: null },
    residential:  { color: '#fef3c7', weight: 1.6, opacity: 0.9,  dashArray: null },
    unclassified: { color: '#d6d3d1', weight: 1.4, opacity: 0.85, dashArray: null },
    service:      { color: '#e7e5e4', weight: 1,   opacity: 0.75, dashArray: null },
    track:        { color: '#a8a29e', weight: 1.2, opacity: 0.7,  dashArray: '5 3' },
    path:         { color: '#a8a29e', weight: 0.8, opacity: 0.55, dashArray: '2 3' },
    footway:      { color: '#a8a29e', weight: 0.6, opacity: 0.4,  dashArray: '1 3' },
    raceway:      { color: '#7e22ce', weight: 2,   opacity: 0.85, dashArray: null },
    living_street:{ color: '#e7e5e4', weight: 1.2, opacity: 0.7,  dashArray: null },
  };
  return map_[h] || { color: '#fbbf24', weight: 1.2, opacity: 0.7 };
}

function landuseStyle(feature) {
  const lu = feature.properties.landuse || feature.properties.landcover || '';
  const m = {
    forest:        { color: '#15803d', fillColor: '#15803d', fillOpacity: 0.22 },
    residential:   { color: '#d97706', fillColor: '#fde68a', fillOpacity: 0.35 },
    commercial:    { color: '#7c3aed', fillColor: '#ddd6fe', fillOpacity: 0.4 },
    industrial:    { color: '#4b5563', fillColor: '#d1d5db', fillOpacity: 0.4 },
    farmland:      { color: '#854d0e', fillColor: '#fef3c7', fillOpacity: 0.25 },
    farmyard:      { color: '#854d0e', fillColor: '#fcd34d', fillOpacity: 0.3 },
    orchard:       { color: '#65a30d', fillColor: '#bef264', fillOpacity: 0.3 },
    meadow:        { color: '#65a30d', fillColor: '#d9f99d', fillOpacity: 0.3 },
    grass:         { color: '#65a30d', fillColor: '#d9f99d', fillOpacity: 0.25 },
    vineyard:      { color: '#7e22ce', fillColor: '#e9d5ff', fillOpacity: 0.3 },
    plant_nursery: { color: '#16a34a', fillColor: '#86efac', fillOpacity: 0.3 },
    cemetery:      { color: '#404040', fillColor: '#a3a3a3', fillOpacity: 0.4 },
    quarry:        { color: '#52525b', fillColor: '#a1a1aa', fillOpacity: 0.4 },
    railway:       { color: '#1f2937', fillColor: '#6b7280', fillOpacity: 0.3 },
    reservoir:     { color: '#1d4ed8', fillColor: '#3b82f6', fillOpacity: 0.3 },
  };
  return m[lu] || { color: '#fcd34d', fillColor: '#fef3c7', fillOpacity: 0.18, weight: 1 };
}

function treesStyle(feature) {
  const t = feature.properties.natural || feature.properties.landuse || feature.properties.landcover || '';
  const m = {
    wood:     { color: '#14532d', fillColor: '#15803d', fillOpacity: 0.35, weight: 0.5 },
    forest:   { color: '#14532d', fillColor: '#16a34a', fillOpacity: 0.45, weight: 0.5 },
    tree_row: { color: '#16a34a', weight: 2, opacity: 0.7, dashArray: '4 2' },
    trees:    { color: '#166534', fillColor: '#22c55e', fillOpacity: 0.4, weight: 0.5 },
    orchard:  { color: '#65a30d', fillColor: '#bef264', fillOpacity: 0.3, weight: 0.5 },
    farmland: { color: '#854d0e', fillColor: '#fef3c7', fillOpacity: 0.2, weight: 0.5 },
    meadow:   { color: '#65a30d', fillColor: '#d9f99d', fillOpacity: 0.25, weight: 0.5 },
  };
  if (feature.geometry.type === 'Point') {
    return { color: '#16a34a', radius: 2.5, fillColor: '#16a34a', fillOpacity: 0.8, weight: 0 };
  }
  return m[t] || { color: '#16a34a', fillColor: '#22c55e', fillOpacity: 0.3, weight: 0.5 };
}

function placeStyle(feature) {
  const p = feature.properties.place || '';
  const m = {
    city:      { radius: 14, color: '#9d174d', fillColor: '#f9a8d4', weight: 2.5, fillOpacity: 0.9 },
    town:      { radius: 11, color: '#9d174d', fillColor: '#fbcfe8', weight: 2,   fillOpacity: 0.9 },
    village:   { radius: 8,  color: '#be185d', fillColor: '#fce7f3', weight: 1.5, fillOpacity: 0.85 },
    hamlet:    { radius: 6,  color: '#9d174d', fillColor: '#fce7f3', weight: 1,   fillOpacity: 0.7 },
    suburb:    { radius: 7,  color: '#a21caf', fillColor: '#f5d0fe', weight: 1.5, fillOpacity: 0.85 },
    neighbourhood: { radius: 7, color: '#a21caf', fillColor: '#f5d0fe', weight: 1.5, fillOpacity: 0.85 },
    locality:  { radius: 5,  color: '#9d174d', fillColor: '#fbcfe8', weight: 1,   fillOpacity: 0.6 },
    isolated_dwelling: { radius: 4, color: '#9d174d', fillColor: '#fce7f3', weight: 1, fillOpacity: 0.6 },
    farm:      { radius: 5,  color: '#9d174d', fillColor: '#fce7f3', weight: 1,   fillOpacity: 0.7 },
  };
  return m[p] || { radius: 5, color: '#9d174d', fillColor: '#fbcfe8', weight: 1, fillOpacity: 0.7 };
}

function buildingStyle(feature) {
  const b = feature.properties.building || '';
  const m = {
    commercial: { color: '#6d28d9', fillColor: '#c4b5fd', fillOpacity: 0.6 },
    industrial: { color: '#1f2937', fillColor: '#9ca3af', fillOpacity: 0.6 },
    school:     { color: '#1d4ed8', fillColor: '#93c5fd', fillOpacity: 0.65 },
    university: { color: '#1e40af', fillColor: '#bfdbfe', fillOpacity: 0.65 },
    barn:       { color: '#854d0e', fillColor: '#fcd34d', fillOpacity: 0.55 },
    cowshed:    { color: '#854d0e', fillColor: '#fcd34d', fillOpacity: 0.55 },
    sty:        { color: '#854d0e', fillColor: '#fcd34d', fillOpacity: 0.55 },
    residential:{ color: '#78716c', fillColor: '#e7e5e4', fillOpacity: 0.55 },
    house:      { color: '#78716c', fillColor: '#e7e5e4', fillOpacity: 0.55 },
  };
  return m[b] || { color: '#78716c', fillColor: '#d6d3d1', fillOpacity: 0.5, weight: 0.5 };
}

function waterStyle()      { return { color: '#1d4ed8', fillColor: '#3b82f6', fillOpacity: 0.55, weight: 1 }; }
function waterwaysStyle(feature) {
  const w = feature.properties.waterway || '';
  const m = {
    river: { color: '#1e3a8a', weight: 4,   opacity: 0.95 },
    stream: { color: '#3b82f6', weight: 2.5, opacity: 0.85 },
    ditch: { color: '#60a5fa', weight: 1.4, opacity: 0.7, dashArray: '3 2' },
    drain: { color: '#60a5fa', weight: 1.4, opacity: 0.7, dashArray: '3 2' },
    tidal_channel: { color: '#1e40af', weight: 2, opacity: 0.85 },
    dam:   { color: '#1e3a8a', weight: 3, opacity: 0.9 },
  };
  return m[w] || { color: '#3b82f6', weight: 1.5, opacity: 0.8 };
}

function poisStyle(feature) {
  const a = feature.properties.amenity;
  const t = feature.properties.tourism;
  const s = feature.properties.shop;
  const l = feature.properties.leisure;
  const c = a || t || s || l || '';
  const type = c.split('_')[0];
  // Distinct symbol per category — using SVG divIcons with emoji
  const sym = {
    hospital:           { icon: '🏥', color: '#dc2626' },
    police:             { icon: '🚓', color: '#1e40af' },
    school:             { icon: '🎓', color: '#1d4ed8' },
    university:         { icon: '🎓', color: '#1e40af' },
    fuel:               { icon: '⛽', color: '#f59e0b' },
    restaurant:         { icon: '🍴', color: '#dc2626' },
    cafe:               { icon: '☕', color: '#92400e' },
    pharmacy:           { icon: '💊', color: '#16a34a' },
    bank:               { icon: '🏦', color: '#0891b2' },
    place_of_worship:   { icon: '⛪', color: '#7c3aed' },
    hotel:              { icon: '🏨', color: '#db2777' },
    guest_house:        { icon: '🏨', color: '#db2777' },
    camp_site:          { icon: '⛺', color: '#15803d' },
    viewpoint:          { icon: '🌄', color: '#0d9488' },
    attraction:         { icon: '⭐', color: '#ca8a04' },
    parking:            { icon: '🅿️', color: '#64748b' },
    pitch:              { icon: '⚽', color: '#16a34a' },
    park:               { icon: '🌳', color: '#16a34a' },
    shop:               { icon: '🛒', color: '#7c3aed' },
    default:            { icon: '•',   color: '#a855f7' },
  }[type] || { icon: '•', color: '#a855f7' };
  return sym;
}

// ---- Layer loaders ----
async function loadLQVLayer(name, src, styleFn, options = {}) {
  const fc = await F(src);
  if (!fc || !fc.features) return 0;
  data[name] = fc;
  totalFeatures += fc.features.length;
  setLayerCount(name, fc.features.length);
  // P0-3: parcel coverage (skip the parcel itself)
  if (name !== 'parcel') computeParcelCoverage(name, fc);
  const layerOpts = {
    style: styleFn,
    pointToLayer: (feature, latlng) => L.circleMarker(latlng, styleFn(feature)),
    onEachFeature: (feature, lyr) => bindInfoPopup(feature, lyr),
  };
  const layer = L.geoJSON(fc, layerOpts);
  layers[name] = layer;
  return fc.features.length;
}

async function loadLQVPolygons(name, src) {
  const fc = await F(src);
  if (!fc || !fc.features) return 0;
  data[name] = fc;
  setLayerCount(name, fc.features.length);
  // P0-3: stash the parcel feature for coverage computation
  if (name === 'parcel' && fc.features[0]) {
    parcelFeature = fc.features[0];
    // P0-3 fix: retroactively compute coverage for already-loaded layers.
    // Without this, layers that loaded before the parcel polygon (which
    // happens because parcel loads first but the OSM cluster Promise.allSettled
    // resolves layers while parcel is mid-fetch) end up with 0 inside counts.
    setTimeout(() => {
      for (const [layerName, layerData] of Object.entries(data)) {
        if (layerName === 'parcel' || parcelInsideCounts[layerName] !== undefined) continue;
        computeParcelCoverage(layerName, layerData);
      }
      updateCoverageMatrix();
    }, 100);
  }
  const layer = L.geoJSON(fc, {
    style: (f) => parcelStyle(f, name),
    onEachFeature: (feature, lyr) => bindInfoPopup(feature, lyr),
  });
  layers[name] = layer;
  return fc.features.length;
}

function parcelStyle(f, name) {
  if (name === 'parcel')
    return { color: '#c89b3c', weight: 4, fillColor: '#fcd34d', fillOpacity: 0.18, dashArray: '8 4' };
  if (name === 'aoi62-legacy')
    return { color: '#a8a29e', weight: 1, fillColor: 'transparent', fillOpacity: 0, dashArray: '3 4', opacity: 0.5 };
  if (name === 'escobar-legacy')
    return { color: '#94a3b8', weight: 1.5, fillColor: '#94a3b8', fillOpacity: 0.05, dashArray: '2 3', opacity: 0.6 };
  return { color: '#999', weight: 1 };
}

function bindInfoPopup(feature, lyr) {
  const p = feature.properties || {};
  const label = p.name || p.highway || p.waterway || p.place || p.amenity || p.natural || p.landuse || p.building || 'feature';
  if (label && label !== 'feature') lyr.bindTooltip(label, { sticky: true, direction: 'top', className: 'lqv-tooltip' });
  if (Object.keys(p).length) {
    lyr.bindPopup(`<strong>${escape(label)}</strong><br><pre style="margin:6px 0;font-size:11px;max-height:200px;overflow:auto;">${escape(JSON.stringify(p, null, 0).slice(0, 600))}</pre>`);
  }
}

function setLayerCount(name, n) {
  const el = document.querySelector(`[data-count="${name}"]`);
  if (el) el.textContent = n.toLocaleString();
}

// P0-3: Coverage indicator — count features inside the LQV parcel and
// append "· X inside" to the layer name. Computed once on boot,
// refreshed when the parcel polygon is loaded.
const parcelInsideCounts = {};

// Cheap bbox of GeoJSON geometry: returns [minLon, minLat, maxLon, maxLat]
function bbox_of_geom(g) {
  let minLon = Infinity, minLat = Infinity, maxLon = -Infinity, maxLat = -Infinity;
  function walk(coords) {
    if (typeof coords[0] === 'number') {
      const [lon, lat] = coords;
      if (lon < minLon) minLon = lon;
      if (lat < minLat) minLat = lat;
      if (lon > maxLon) maxLon = lon;
      if (lat > maxLat) maxLat = lat;
    } else {
      for (const c of coords) walk(c);
    }
  }
  walk(g.coordinates);
  return [minLon, minLat, maxLon, maxLat];
}
function bboxes_overlap(a, b) {
  // bboxes: [minLon, minLat, maxLon, maxLat]
  return !(b[2] < a[0] || b[0] > a[2] || b[3] < a[1] || b[1] > a[3]);
}
// Point-in-polygon ray-casting for the parcel polygon (single ring or
// multi-polygon). For the parcel-check we use bbox then precise test.
function pip(lon, lat, polygon) {
  // Ray casting: for each edge of the polygon, check if it crosses
  // the horizontal line at lat to the right of the point.
  let inside = false;
  const ring = polygon.type === 'Polygon' ? polygon.coordinates[0]
             : polygon.type === 'MultiPolygon' ? null // fallback
             : null;
  if (!ring) return null; // tell caller to fall back to bbox-only
  for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
    const xi = ring[i][0], yi = ring[i][1];
    const xj = ring[j][0], yj = ring[j][1];
    const intersect = ((yi > lat) !== (yj > lat))
      && (lon < (xj - xi) * (lat - yi) / (yj - yi) + xi);
    if (intersect) inside = !inside;
  }
  return inside;
}
function point_in_parcel(lon, lat) {
  // Use the dominant polygon (first ring) of the parcel Feature
  if (!parcelFeature || !parcelFeature.geometry) return null;
  const g = parcelFeature.geometry;
  if (g.type === 'Polygon') return pip(lon, lat, g);
  if (g.type === 'MultiPolygon') {
    for (const poly of g.coordinates) {
      const r = pip(lon, lat, { type: 'Polygon', coordinates: poly });
      if (r) return true;
    }
    return false;
  }
  return null;
}

function computeParcelCoverage(layerName, fc) {
  if (!fc || !fc.features || !parcelFeature) return 0;
  const parcelBbox = bbox_of_geom(parcelFeature.geometry);
  let inside = 0;
  for (const f of fc.features) {
    if (!f.geometry) continue;
    const g = f.geometry;
    let counted = false;
    try {
      const gt = g.type;
      if (gt === 'Point') {
        const [lon, lat] = g.coordinates;
        const r = point_in_parcel(lon, lat);
        if (r === true) counted = true;
        else if (r === null) {
          // MultiPolygon parcel: fall back to bbox envelope (false positives OK)
          const pb = [lon - 1e-4, lat - 1e-4, lon + 1e-4, lat + 1e-4];
          if (bboxes_overlap(parcelBbox, pb)) counted = true;
        }
      } else if (gt === 'Polygon' || gt === 'MultiPolygon' ||
                 gt === 'LineString' || gt === 'MultiLineString') {
        const bbox = bbox_of_geom(g);
        if (bboxes_overlap(parcelBbox, bbox)) counted = true;
      }
    } catch (e) {}
    if (counted) inside += 1;
  }
  parcelInsideCounts[layerName] = inside;
  const el = document.querySelector(`[data-count="${layerName}"]`);
  if (el && el.parentElement && el.parentElement.tagName === 'SPAN') {
    let badge = el.parentElement.querySelector('.coverage-badge');
    if (!badge) {
      badge = document.createElement('span');
      badge.className = 'coverage-badge';
      el.parentElement.appendChild(badge);
    }
    if (inside > 0) {
      badge.textContent = ` · ${inside.toLocaleString()} inside parcel`;
      badge.classList.add('coverage-on');
    } else {
      badge.textContent = ` · 0 inside parcel`;
      badge.classList.remove('coverage-on');
    }
  }
  return inside;
}

// ---- Permanent label rendering ----
// Use Leaflet permanent tooltips so cities, towns and labeled features are
// always readable. Hide below a zoom threshold to avoid clutter at country-level.
function addPermanentLabels(name, fc, predicate, opts = {}) {
  const minZoom = opts.minZoom ?? 10;
  const maxLabels = opts.maxLabels ?? 200;
  let n = 0;
  const stops = [];
  for (const f of fc.features) {
    if (n >= maxLabels) break;
    if (!predicate(f)) continue;
    const pt = centroid(f);
    if (!pt) continue;
    const label = (f.properties?.name || '').trim();
    if (!label) continue;
    const tooltip = L.tooltip({
      permanent: true,
      direction: opts.direction || 'right',
      className: 'permanent',
      offset: opts.offset || [8, 0],
    })
      .setLatLng(pt)
      .setContent(label);
    stops.push({ tooltip, minZoom });
    n++;
  }
  if (stops.length) {
    labels[name] = (labels[name] || []).concat(stops);
    // Add to map and toggle by zoom
    const update = () => {
      const z = map.getZoom();
      stops.forEach(({ tooltip }) => {
        const visible = z >= minZoom && (layers[name] && map.hasLayer(layers[name]));
        const onMap  = map.hasLayer(tooltip);
        if (visible && !onMap) tooltip.addTo(map);
        else if (!visible && onMap) map.removeLayer(tooltip);
      });
    };
    map.on('zoomend', update);
    map.on('layeradd layerremove', update);
    update();
  }
}

function centroid(f) {
  const g = f.geometry;
  if (!g) return null;
  if (g.type === 'Point') return [g.coordinates[1], g.coordinates[0]];
  // For polygons/lines use a simple bbox-centroid (good enough at country scale)
  let sx=0, sy=0, n=0;
  const push = (c) => { if (Array.isArray(c[0])) c.forEach(push); else { sx+=c[0]; sy+=c[1]; n++; } };
  if (g.type === 'Polygon')  g.coordinates.forEach(push);
  else if (g.type === 'MultiPolygon') g.coordinates.forEach(p => p.forEach(push));
  else if (g.type === 'LineString')  push(g.coordinates);
  else if (g.type === 'MultiLineString') g.coordinates.forEach(push);
  if (n === 0) return null;
  return [sy/n, sx/n];
}

function escape(s) {
  return String(s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
}

// ---- Custom POI div icons ----
function poiDivIcon(feature, latlng) {
  const sym = poisStyle(feature);
  const html = `<div style="
      width:22px;height:22px;border-radius:50%;
      background:${sym.color};border:2px solid white;
      box-shadow:0 1px 3px rgba(0,0,0,0.4);
      display:flex;align-items:center;justify-content:center;
      font-size:11px;color:white;line-height:1;
    ">${sym.icon}</div>`;
  return L.marker(latlng, { icon: L.divIcon({ html, className: '', iconSize: [22,22], iconAnchor: [11,11] }) });
}

// ---- Property parcel pulse (Leaflet-based, zoom-aware size) ----
const parcelPulse = L.circleMarker(CENTER, {
  radius: 18,
  color: '#c89b3c',
  fillColor: '#fcd34d',
  fillOpacity: 0.3,
  weight: 3,
  opacity: 0.95,
});
// Outer expanding ring (renders as a separate pulse animation)
const parcelRing = L.circleMarker(CENTER, {
  radius: 24,
  color: '#c89b3c',
  fillColor: '#c89b3c',
  fillOpacity: 0,
  weight: 2,
  opacity: 0.7,
});
let parcelPulseAnim = 0;
function pulseAnim() {
  parcelPulseAnim += 1;
  const t = (parcelPulseAnim % 80) / 80;
  const sinT = Math.sin(t * Math.PI * 2);
  // Inner pulse (subtle)
  parcelPulse.setStyle({ radius: 16 + sinT * 4, fillOpacity: 0.35 + sinT * 0.15 });
  // Outer ring (1-cycle expansion + fade)
  const ringT = (parcelPulseAnim % 100) / 100;
  parcelRing.setStyle({ radius: 20 + ringT * 60, opacity: (1 - ringT) * 0.55, weight: 2 + ringT });
  requestAnimationFrame(pulseAnim);
}
pulseAnim();

parcelPulse.bindTooltip(`<strong>La Quebrada Viva</strong><br>71.4 ha · GPS walked 2026-06-28 · click to zoom`, {
  permanent: false, direction: 'top', offset: [0, -10], className: 'lqv-tooltip',
});
parcelPulse.on('click', () => map.flyTo(CENTER, 16, { duration: 1.2 }));
parcelPulse.addTo(map);
parcelRing.addTo(map);

// P0-3: parcelFeature for coverage computation — set after parcel loads
let parcelFeature = null;

// Inner solid core dot
const parcelCore = L.circleMarker(CENTER, {
  radius: 7,
  color: 'white',
  fillColor: '#c89b3c',
  fillOpacity: 1,
  weight: 2,
});
parcelCore.addTo(map);

// "Your property" callout label (permanent, only visible at z ≥ 10)
const parcelLabel = L.tooltip({
  permanent: true, direction: 'right', offset: [26, 0], className: 'parcel permanent',
}).setLatLng(CENTER).setContent('★ La Quebrada Viva');
function updateParcelLabel() {
  const z = map.getZoom();
  if (z >= 10 && !map.hasLayer(parcelLabel)) parcelLabel.addTo(map);
  else if (z < 10 && map.hasLayer(parcelLabel)) map.removeLayer(parcelLabel);
}
map.on('zoomend', updateParcelLabel);
updateParcelLabel();

// P0-5: at z>=14 (parcel-zoom), dim coarse regional layers to 30% opacity
// so the parcel-scale detail (quebrada, GPS path, contour, NDVI) reads clearly.
// At z<=13, restore full opacity.
const REGIONAL_LAYERS = ['mapbiomas', 'hansen-loss', 'hansen-gain',
                          'woodland-merged', 'osm-buildings', 'osm-landuse',
                          'places', 'pois'];
const REGIONAL_OPACITY = { default: 1.0, dimmed: 0.3 };

// P-topology: high-resolution parcel-scale hillshade (5m) for z>=15
// Loaded lazily on first zoom-in. Provides terrain detail that the
// 30m main hillshade loses at parcel zoom.
let _parcelHillshade = null;
function getParcelHillshade() {
  if (_parcelHillshade !== null) return _parcelHillshade;
  try {
    // Inline fetch via sync XMLHttpRequest (avoid async in zoom callback).
    // Actually we'll use a cached promise instead.
  } catch (e) {}
  return null;
}
async function loadParcelHillshade() {
  if (_parcelHillshade) return _parcelHillshade;
  try {
    const r = await fetch('./data/hillshade_parcel_bounds.json');
    const bounds = await r.json();
    _parcelHillshade = L.imageOverlay(
      './data/hillshade_parcel.jpg',
      [[bounds.min_lat, bounds.min_lon], [bounds.max_lat, bounds.max_lon]],
      { opacity: 0.65, interactive: false, className: 'parcel-hillshade' },
    );
  } catch (e) {
    console.warn('parcel hillshade load failed:', e);
    _parcelHillshade = false;
  }
  return _parcelHillshade;
}
function applyParcelZoomRule() {
  const z = map.getZoom();
  const dim = z >= 14;
  REGIONAL_LAYERS.forEach(name => {
    const lyr = layers[name];
    if (!lyr) return;
    // Don't change visibility — just opacity. Users can still see the data.
    lyr.setStyle({ opacity: dim ? 0.4 : 1.0, fillOpacity: dim ? 0.18 : lyr.options.fillOpacity || 0.55 });
  });
  // P-topology: show high-resolution 5m hillshade only at z>=15
  if (z >= 15) {
    if (_parcelHillshade === null || _parcelHillshade === false) {
      loadParcelHillshade().then(overlay => {
        if (overlay && !map.hasLayer(overlay)) overlay.addTo(map);
      });
    } else if (_parcelHillshade && !map.hasLayer(_parcelHillshade)) {
      _parcelHillshade.addTo(map);
    }
  } else {
    if (_parcelHillshade && map.hasLayer(_parcelHillshade)) map.removeLayer(_parcelHillshade);
  }
}
map.on('zoomend', applyParcelZoomRule);

// P1-6: cursor elevation/slope/aspect HUD. Loads elevation_grid.json (270 KB).
let elevGrid = null;
(async function loadElevGrid() {
  try {
    const r = await fetch('./data/elevation_grid.json');
    const j = await r.json();
    // Convert to typed arrays for fast sampling
    j.dem = new Uint16Array(j.dem);
    j.slope = new Uint16Array(j.slope);
    j.aspect = new Uint16Array(j.aspect);
    elevGrid = j;
    document.getElementById('elev-hud').style.display = 'block';
    console.log(`elev grid loaded: ${j.width}x${j.height} = ${j.dem.length} pixels`);
  } catch (e) {
    console.warn('elev grid load failed:', e);
  }
})();
const ASPECT_DIRS = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW'];
function aspectName(a) {
  return ASPECT_DIRS[Math.floor((a + 22.5) / 45) % 8];
}
function sampleElevGrid(lon, lat) {
  if (!elevGrid) return null;
  const [minLon, minLat, maxLon, maxLat] = elevGrid.bounds;
  if (lon < minLon || lon > maxLon || lat < minLat || lat > maxLat) return null;
  const W = elevGrid.width;
  const H = elevGrid.height;
  const col = Math.floor((lon - minLon) / (maxLon - minLon) * W);
  const row = Math.floor((maxLat - lat) / (maxLat - minLat) * H);
  const idx = row * W + col;
  return {
    elev: elevGrid.dem[idx],
    slope: elevGrid.slope[idx] / 10,   // decoded: 1 decimal precision
    aspect: elevGrid.aspect[idx],
  };
}
map.on('mousemove', (e) => {
  const { lat, lng } = e.latlng;
  document.getElementById('hud-lon').textContent = lng.toFixed(5);
  document.getElementById('hud-lat').textContent = lat.toFixed(5);
  const s = sampleElevGrid(lng, lat);
  if (s) {
    document.getElementById('hud-elev').textContent = `${s.elev.toFixed(0)} m`;
    document.getElementById('hud-slope').textContent = `${s.slope.toFixed(1)}%`;
    document.getElementById('hud-aspect').textContent = `${s.aspect.toFixed(0)}° ${aspectName(s.aspect)}`;
  } else {
    document.getElementById('hud-elev').textContent = '—';
    document.getElementById('hud-slope').textContent = '—';
    document.getElementById('hud-aspect').textContent = '—';
  }
});

// ---- Boot ----
(async function boot() {
  // 1. CLIENT-PROVIDED GPS perimeter polygon (71.37 ha, 17 corners walked 2026-06-22+28)
  await loadLQVPolygons('parcel', './data/client_gps/client_gps_polygon.geojson');

  // 2. The 17 individual corner points + 3 named features
  // Uses the official Guru Maps bookmark icons (orange border pins) so
  // the GPS-walked corners visually match the Guru Maps share exactly.
  const GURU_ICONS = {
    '118': './data/icons/gurumaps/BookmarkStyle_118.png',  // border — orange
    '26':  './data/icons/gurumaps/BookmarkStyle_26.png',   // waterfall — red
    '28':  './data/icons/gurumaps/BookmarkStyle_28.png',   // gate — blue
    '72':  './data/icons/gurumaps/BookmarkStyle_72.png',   // high point — green
  };
  const corners = await F('./data/client_gps/client_gps_corners.geojson');
  if (corners && corners.features) {
    data['gps-corners'] = corners;
    setLayerCount('gps-corners', corners.features.length);
    totalFeatures += corners.features.length;
    const cornerIcon = L.icon({
      iconUrl:    GURU_ICONS['118'],
      iconSize:   [37, 37],     // matches Guru Maps rendering exactly
      iconAnchor: [18, 37],     // bottom-center tip of the pin
      popupAnchor: [0, -37],
      className: 'guru-pin',
    });
    layers['gps-corners'] = L.geoJSON(corners, {
      pointToLayer: (feature, latlng) => {
        const m = L.marker(latlng, { icon: cornerIcon, zIndexOffset: 200 });
        m.on('click', () => map.flyTo(latlng, 17, { duration: 0.6 }));
        return m;
      },
      onEachFeature: (feature, lyr) => {
        const p = feature.properties || {};
        const ts = p.captured_at ? p.captured_at.replace('T', ' ').replace(/\.\d+Z$/, ' UTC') : '?';
        const label = `${p.name || 'Corner'} · ${p.walk_session || '?'}<br>${ts}`;
        lyr.bindTooltip(label, { sticky: true, direction: 'top', className: 'lqv-tooltip' });
      },
    });
  }
  const featuresGps = await F('./data/client_gps/client_gps_features.geojson');
  if (featuresGps && featuresGps.features) {
    data['gps-features'] = featuresGps;
    setLayerCount('gps-features', featuresGps.features.length);
    totalFeatures += featuresGps.features.length;
    layers['gps-features'] = L.geoJSON(featuresGps, {
      pointToLayer: (feature, latlng) => {
        const cat = String(feature.properties.icon_cat || feature.properties.symbol || 118);
        const url = GURU_ICONS[cat] || GURU_ICONS['118'];
        const icon = L.icon({
          iconUrl: url,
          iconSize: [44, 44],
          iconAnchor: [22, 44],
          popupAnchor: [0, -44],
          className: 'guru-pin-feature',
        });
        return L.marker(latlng, { icon, zIndexOffset: 600 });
      },
      onEachFeature: (feature, lyr) => {
        const p = feature.properties || {};
        const elev = p.altitude_m ? ` · ${p.altitude_m} m elevation` : '';
        const ts = p.captured_at ? p.captured_at.replace('T', ' ').replace(/\.\d+Z$/, ' UTC') : '?';
        const inside = p.inside_polygon === false ? 'outside polygon' : 'inside polygon';
        lyr.bindTooltip(
          `<strong>${p.name || 'Feature'}</strong>${elev}<br>` +
          `${p.feature_kind || '?'} · ${inside}<br>${ts}`,
          { sticky: true, direction: 'top', className: 'lqv-tooltip' }
        );
      },
    });
  }

  // 3. LEGACY polygons — off by default (KML subset + AOI buffer)
  await loadLQVPolygons('escobar-legacy', './data/client_gps/escobar_polygon_legacy.geojson');
  await loadLQVPolygons('aoi62-legacy',  './data/client_gps/aoi_62_extended_legacy.geojson');

  // 4. NDVI canopy loading now lives in section 7 below (canopy-10km +
  //    canopy-legacy) — they're styled inline with the full 10km dataset.

  // 5. WALKING PATH — Wes's actual trail captured via Guru Maps, two sessions
  const wpath = await F('./data/client_gps/client_gps_walking_path.geojson');
  if (wpath && wpath.features && wpath.features.length) {
    data['gps-walking-path'] = wpath;
    setLayerCount('gps-walking-path', wpath.features[0].geometry.coordinates.length);
    layers['gps-walking-path'] = L.geoJSON(wpath, {
      style: {
        color: '#f59e0b', weight: 3, opacity: 0.9, dashArray: '8 5',
        lineCap: 'round', lineJoin: 'round',
      },
      onEachFeature: (feature, lyr) => {
        const ts = (feature.properties?.timestamps || []);
        lyr.bindTooltip(
          `Wesley's walking path · ${ts.length} waypoints<br>` +
          `${ts[0] || '?'} → ${ts[ts.length-1] || '?'}`,
          { sticky: true, direction: 'top', className: 'lqv-tooltip' },
        );
      },
    });
  }

  // 6. PER-SESSION walking paths (two distinct colored polylines)
  const wsess = await F('./data/client_gps/client_gps_walking_sessions.geojson');
  if (wsess && wsess.features && wsess.features.length) {
    data['gps-sessions'] = wsess;
    layers['gps-sessions'] = L.geoJSON(wsess, {
      style: (feature) => ({
        color: feature.properties.color || '#a855f7',
        weight: feature.properties.stroke_width || 3,
        opacity: 0.9,
        dashArray: feature.properties.dashArray || null,
        lineCap: 'round',
      }),
      onEachFeature: (feature, lyr) => {
        lyr.bindTooltip(
          `${feature.properties.name}<br>${feature.properties.point_count} GPS points · ${feature.properties.session_date}`,
          { sticky: true, direction: 'top', className: 'lqv-tooltip' },
        );
      },
    });
  }

  // 7. Canopy (4-class NDVI polygons — one style for each, fills only)
  //    Two versions: 20 km (full Escobar) and legacy property-only.
  const canopyStyle = (feature) => {
    const p = feature.properties || {};
    const cls = (p.class ?? p.ndvi_class ?? 0);
    const color = p.color || p.fill_color || ['#a16207','#84cc16','#22c55e','#14532d'][Math.min(3, cls)];
    const fillOpacity = (() => {
      const c = Number(cls);
      return [0.35, 0.4, 0.45, 0.55][Math.min(3, c)] || 0.4;
    })();
    return { color, fillColor: color, fillOpacity, weight: 0.5 };
  };
  const canopy20 = await F('./data/ndvi_canopy_10km.geojson');
  if (canopy20 && canopy20.features && canopy20.features.length) {
    data['canopy-10km'] = canopy20;
    setLayerCount('canopy-10km', canopy20.features.length);
    layers['canopy-10km'] = L.geoJSON(canopy20, {
      style: canopyStyle,
      onEachFeature: (feature, lyr) => bindInfoPopup(feature, lyr),
    });
  }
  const canopyLegacy = await F('./data/canopy_classes.geojson');
  if (canopyLegacy && canopyLegacy.features && canopyLegacy.features.length) {
    data['canopy-legacy'] = canopyLegacy;
    setLayerCount('canopy-legacy', canopyLegacy.features.length);
    layers['canopy-legacy'] = L.geoJSON(canopyLegacy, {
      style: canopyStyle,
      onEachFeature: (feature, lyr) => bindInfoPopup(feature, lyr),
    });
  }
  // Legacy `canopy` key: point `data.canopy` at the legacy layer for any
  // code path that still references it (e.g. layer-count fallback).
  data.canopy = canopyLegacy || canopy20;

  // 9. COMBINED water (4 sources merged with shared taxonomy in
  //    family_taxonomy, ready for both lines + polygons).
  const combinedWater = await F('./data/water_combined_10km.geojson');
  if (combinedWater && combinedWater.features && combinedWater.features.length) {
    const taxonomy = (combinedWater.metadata && combinedWater.metadata.family_taxonomy) || {};
    data['combined-water'] = combinedWater;
    setLayerCount('combined-water', combinedWater.features.length);
    layers['combined-water'] = L.geoJSON(combinedWater, {
      style: (feature) => {
        const p = feature.properties || {};
        const gtype = feature.geometry.type;
        if (gtype === 'LineString' || gtype === 'MultiLineString') {
          // Pump up the widths on the combined layer so the named rivers
          // and OSM-mapped drainage linework read crisply at the 20 km zoom.
          const cls = p.category || '';
          const extraWidth = {
            main_river: 4.5, river: 3.5, tributary: 2.5,
            creek: 2, stream: 2, rill: 1.4,
            tidal_channel: 1.5, canal: 1.4, ditch: 1, dam: 1,
          }[cls] ?? 1.5;
          return {
            color: p.color || '#0c4a6e',
            weight: extraWidth,
            opacity: 0.95,
            lineCap: 'round',
          };
        }
        return {
          color: p.color || '#0ea5e9',
          weight: 1,
          fillColor: p.color || '#0ea5e9',
          fillOpacity: p.fill_opacity ?? 0.45,
        };
      },
      onEachFeature: (feature, lyr) => {
        const p = feature.properties || {};
        const fam = (p.audit_class_label || p.class_label || p.category || '').replace(/_/g, ' ');
        lyr.bindTooltip(
          `<strong>${fam}</strong><br>` +
          `Source: ${p.source || '?'}<br>` +
          (p.feature_id ? `id: ${p.feature_id}<br>` : '') +
          (p.catchment_km2 ? `catchment: ${p.catchment_km2} km²<br>` : '') +
          (p.audit_jrc_occurrence_mean !== undefined && p.audit_jrc_occurrence_mean !== null
              && !isNaN(parseFloat(p.audit_jrc_occurrence_mean))
              ? `JRC occurrence: ${p.audit_jrc_occurrence_mean}%<br>` : '') +
          (p.audit_dem_elev_min_m !== undefined && p.audit_dem_elev_min_m !== null
              && !isNaN(parseFloat(p.audit_dem_elev_min_m))
              ? `DEM elev: ${p.audit_dem_elev_min_m}–${p.audit_dem_elev_max_m} m<br>` : '') +
          (p.audit_centroid_near_waterway ? 'within 200 m of a waterway<br>' : ''),
          { sticky: true, direction: 'top', className: 'lqv-tooltip' }
        );
      },
    });
  }

  // 8. Streams (full 20 km DEM quebrada network + legacy property-scale)
  const streamStyle = (feature) => {
    const cls = feature.properties.class || '';
    if (cls === 'main')         return { color: '#1d4ed8', weight: 3,   opacity: 0.95 };
    if (cls === 'tributary')    return { color: '#3b82f6', weight: 2,   opacity: 0.85 };
    if (cls === 'headwater')    return { color: '#93c5fd', weight: 1.4, opacity: 0.75 };
    return { color: '#3b82f6', weight: 2, opacity: 0.85 };
  };
  // P1-2: Local Quebrada polyline (ground-truth, GPS-derived)
  const localQ = await F('./data/local_quebradas_10km.geojson');
  if (localQ && localQ.features) {
    data['local-quebrada'] = localQ;
    setLayerCount('local-quebrada', localQ.features.length);
    layers['local-quebrada'] = L.geoJSON(localQ, {
      style: (feature) => ({
        color: feature.properties.color || '#1d4ed8',
        weight: feature.properties.stroke_width || 4,
        opacity: 0.9,
        dashArray: '6,4',
      }),
      onEachFeature: (feature, lyr) => {
        const p = feature.properties || {};
        lyr.bindTooltip(
          `<strong>${p.name || 'LQV quebrada'}</strong><br>` +
          `${(p.length_m || 0).toFixed(0)} m long<br>` +
          `elev ${p.elev_min_m || '?'}-${p.elev_max_m || '?'} m<br>` +
          `<small>${p.description || ''}</small><br>` +
          `<small style="color:#9ca3af">captured ${p.captured_dates || ''} by ${p.captured_by || ''}</small>`,
          { sticky: true, direction: 'top', className: 'lqv-tooltip' }
        );
      },
    });
  }

  const streams20 = await F('./data/dem_streams_10km.geojson');
  if (streams20 && streams20.features && streams20.features.length) {
    data['streams-10km'] = streams20;
    setLayerCount('streams-10km', streams20.features.length);
    layers['streams-10km'] = L.geoJSON(streams20, {
      style: streamStyle,
      onEachFeature: (feature, lyr) => {
        const p = feature.properties || {};
        lyr.bindTooltip(
          `<strong>${p.class}</strong> quebrada stream<br>` +
          `catchment ${p.catchment_km2} km² (${p.accumulation_cells} cells @ 180 m)<br>` +
          `${p.vertex_count} vertices<br>` +
          `${p.source || ''}`,
          { sticky: true, direction: 'top', className: 'lqv-tooltip' }
        );
      },
    });
  }

  // 9b. Flow direction arrows: Point features every ~50 vertices along
  // main_rivers and tributaries. We use canvas via a custom renderer
  // (L.canvas()) so 1500 markers render fast. Each marker is a triangle
  // rendered with rotation based on flow direction.
  const flowArrows = await F('./data/dem_streams_arrows_10km.geojson');
  if (flowArrows && flowArrows.features && flowArrows.features.length) {
    data['flow-arrows'] = flowArrows;
    setLayerCount('flow-arrows', flowArrows.features.length);
    // Pre-compute every arrow's pixel location & rotation once, then
    // paint onto the map's overlay pane at draw time.
    const arrows = flowArrows.features.map((f) => {
      const p = f.properties || {};
      const [lon, lat] = f.geometry.coordinates;
      const [lon1, lat1] = p.from || [lon, lat];
      const [lon2, lat2] = p.to   || [lon, lat];
      const angle = (Math.atan2(lat2 - lat1, lon2 - lon1) * 180 / Math.PI);
      const cls = p.class || 'tributary';
      return { lat, lon, angle, cls };
    });
    const arrowRenderer = L.canvas({ padding: 0.5 });
    layers['flow-arrows'] = L.layerGroup();
    arrows.forEach(a => {
      const isMain = a.cls === 'main';
      const color = isMain ? '#0c4a6e' : '#1d4ed8';
      const size = isMain ? 28 : 22;
      const m = L.marker([a.lat, a.lon], {
        icon: L.divIcon({
          html: `<svg width="${size}" height="${size}" viewBox="-50 -50 100 100" style="transform: rotate(${a.angle.toFixed(1)}deg); filter: drop-shadow(0 0 2px rgba(255,255,255,0.9));">
            <polygon points="-32,-14 32,0 -32,14 -22,0" fill="${color}" stroke="white" stroke-width="6" stroke-linejoin="round"/>
          </svg>`,
          className: 'flow-arrow-icon',
          iconSize: [size, size],
          iconAnchor: [size / 2, size / 2],
        }),
        renderer: arrowRenderer,
        keyboard: false,
      });
      m.bindTooltip('↓ flow direction', { sticky: true, direction: 'top', className: 'lqv-tooltip' });
      m.addTo(layers['flow-arrows']);
    });
  }

  // 9c. Hillshade backdrop: JPEG image overlay derived from the DEM.
  // Stored as a JPEG (1.94 MB) under 25 MB cap. Bounds fetched from
  // 9d-bis. NDVI backdrop (continuous NDVI raster from MapBiomas-derived polygons).
  try {
    const r = await fetch('./data/ndvi_canopy_bounds.json');
    if (!r.ok) throw new Error(`ndvi bounds HTTP ${r.status}`);
    const ndviBounds = await r.json();
    layers['ndvi-backdrop'] = L.imageOverlay(
      './data/ndvi_canopy_10km.png',
      ndviBounds,
      { opacity: 0.55, interactive: false, className: 'ndvi-backdrop' },
    );
    data['ndvi-backdrop'] = { bounds: ndviBounds };
    setLayerCount('ndvi-backdrop', 1);
  } catch (err) {
    console.warn('NDVI backdrop load failed:', err);
  }

  // hillshade_bounds.json (1-pixel offset from BBOX corners).
  try {
    const r = await fetch('./data/hillshade_bounds.json');
    if (!r.ok) throw new Error(`bounds HTTP ${r.status}`);
    const hsBounds = await r.json();
    layers['hillshade'] = L.imageOverlay(
      './data/hillshade_10km.jpg',
      [
        [hsBounds.min_lat, hsBounds.min_lon],
        [hsBounds.max_lat, hsBounds.max_lon],
      ],
      { opacity: 0.5, interactive: false, className: 'hillshade' },
    );
    data['hillshade'] = { bounds: hsBounds };
  } catch (err) {
    console.warn('hillshade load failed:', err);
  }

  // 9d. Elevation colour-relief (green lowland → brown upland).
  try {
    const r = await fetch('./data/dem_color_relief_bounds.json');
    if (!r.ok) throw new Error(`relief bounds HTTP ${r.status}`);
    const reliefBounds = await r.json();
    layers['color-relief'] = L.imageOverlay(
      './data/dem_color_relief_10km.jpg',
      [
        [reliefBounds.min_lat, reliefBounds.min_lon],
        [reliefBounds.max_lat, reliefBounds.max_lon],
      ],
      { opacity: 0.5, interactive: false, className: 'relief' },
    );
    data['color-relief'] = { bounds: reliefBounds };
  } catch (err) {
    console.warn('color-relief load failed:', err);
  }

  // 9e. Elevation contours (LineString, 50 m steps).
  const contoursFc = await F('./data/dem_contours_10km.geojson');
  if (contoursFc && contoursFc.features && contoursFc.features.length) {
    data['contours'] = contoursFc;
    setLayerCount('contours', contoursFc.features.length);
    layers['contours'] = L.geoJSON(contoursFc, {
      style: (feature) => {
        const elev = feature.properties.elev_m;
        const color = feature.properties.color || '#0c4a6e';
        const weight = (elev % 100) === 0 ? 1.6 : 0.8;   // every 100 m thicker
        return { color, weight, opacity: 0.85 };
      },
      onEachFeature: (feature, lyr) => {
        lyr.bindTooltip(`${feature.properties.elev_label} contour`, {
          sticky: true, direction: 'top', className: 'lqv-tooltip'
        });
      },
    });
  }

  // 9e-bis. Parcel-scale 5m contours (P-topology) — denser contours at
  // parcel zoom, derived from the fused 5m tier-1 topology DEM.
  const parcelContoursFc = await F('./data/dem_contours_parcel_5m.geojson');
  if (parcelContoursFc && parcelContoursFc.features) {
    data['contours-parcel'] = parcelContoursFc;
    setLayerCount('contours-parcel', parcelContoursFc.features.length);
    layers['contours-parcel'] = L.geoJSON(parcelContoursFc, {
      style: (feature) => ({
        color: feature.properties.color || '#0284c7',
        weight: feature.properties.weight || 0.8,
        opacity: 0.85,
      }),
      onEachFeature: (feature, lyr) => {
        lyr.bindTooltip(`${feature.properties.elev_label} (5 m parcel topo)`, {
          sticky: true, direction: 'top', className: 'lqv-tooltip'
        });
      },
    });
  }

  // 9f. MapBiomas Paraguay 2023 land-cover (7-class polygons covering
  // the 20 km box at 30 m resolution).
  const mapbiomasFc = await F('./data/mapbiomas_2023_10km.geojson');
  if (mapbiomasFc && mapbiomasFc.features && mapbiomasFc.features.length) {
    data['mapbiomas'] = mapbiomasFc;
    setLayerCount('mapbiomas', mapbiomasFc.features.length);
    layers['mapbiomas'] = L.geoJSON(mapbiomasFc, {
      style: (feature) => {
        const p = feature.properties || {};
        return {
          color: p.color || '#16a34a',
          fillColor: p.color || '#16a34a',
          fillOpacity: 0.45,
          weight: 0.4,
        };
      },
      onEachFeature: (feature, lyr) => {
        const p = feature.properties || {};
        lyr.bindTooltip(
          `<strong>${p.name || 'land cover'}</strong><br>` +
          `MapBiomas class ${p.class_code}<br>` +
          `${(Math.round((p.area_ha || 0) * 100) / 100).toLocaleString()} ha (${(p.pixel_count || 0).toLocaleString()} px)<br>` +
          `<small>${p.description || ''}</small><br>` +
          `<small>${p.source || ''}</small>`,
          { sticky: true, direction: 'top', className: 'lqv-tooltip' }
        );
      },
    });
  }

  // 9g. Hansen forest loss (red patches 2001-2024).
  const lossFc = await F('./data/hansen_loss_10km.geojson');
  if (lossFc && lossFc.features && lossFc.features.length) {
    data['hansen-loss'] = lossFc;
    setLayerCount('hansen-loss', lossFc.features.length);
    layers['hansen-loss'] = L.geoJSON(lossFc, {
      style: {
        color: '#dc2626', weight: 0.8, fillColor: '#dc2626',
        fillOpacity: 0.55,
      },
      onEachFeature: (feature, lyr) => {
        try {
          // P0-4: use pre-computed area_ha (proper WGS84 geodesic) instead
          // of runtime shoelace approximation. pyproj.Geod used at build time.
          const areaHa = feature.properties.area_ha || 0;
          lyr.bindTooltip(
            `<strong>Forest loss (deforestation)</strong><br>` +
            `~${areaHa.toFixed(1)} ha clearcut<br>` +
            `Hansen v1.12 2001-2024`,
            { sticky: true, direction: 'top', className: 'lqv-tooltip' }
          );
        } catch (e) {
          lyr.bindTooltip(`Forest loss (Hansen GFC v1.12)`, { sticky: true });
        }
      },
    });
  }

  // 9h. Hansen forest gain (green patches 2000-2012).
  const gainFc = await F('./data/hansen_gain_10km.geojson');
  if (gainFc && gainFc.features && gainFc.features.length) {
    data['hansen-gain'] = gainFc;
    setLayerCount('hansen-gain', gainFc.features.length);
    layers['hansen-gain'] = L.geoJSON(gainFc, {
      style: {
        color: '#22c55e', weight: 0.8, fillColor: '#22c55e',
        fillOpacity: 0.55,
      },
      onEachFeature: (feature, lyr) => {
        try {
          // P0-4: use pre-computed area_ha (proper WGS84 geodesic).
          const areaHa = feature.properties.area_ha || 0;
          lyr.bindTooltip(
            `<strong>Forest gain (regrowth)</strong><br>` +
            `~${areaHa.toFixed(1)} ha<br>` +
            `Hansen v1.12 gain band 2000-2012`,
            { sticky: true, direction: 'top', className: 'lqv-tooltip' }
          );
        } catch (e) {
          lyr.bindTooltip(`Forest gain (Hansen GFC v1.12)`, { sticky: true });
        }
      },
    });
  }

  // 9i. Woodland & forest merged: 18,714 polygons from 4 sources
  // (MapBiomas classes 3+6, Hansen ≥30% and ≥75%, OSM wood filtered).
  // Colour by source for transparency.
  const woodlandFc = await F('./data/woodland_merged_10km.geojson');
  if (woodlandFc && woodlandFc.features && woodlandFc.features.length) {
    data['woodland-merged'] = woodlandFc;
    setLayerCount('woodland-merged', woodlandFc.features.length);
    layers['woodland-merged'] = L.geoJSON(woodlandFc, {
      style: (feature) => {
        const p = feature.properties || {};
        return {
          color: p.color || '#15803d',
          fillColor: p.color || '#15803d',
          fillOpacity: 0.45,
          weight: 0.4,
          opacity: 0.8,
        };
      },
      onEachFeature: (feature, lyr) => {
        const p = feature.properties || {};
        const descr = p.description || p.woodland_kind || 'woodland';
        lyr.bindTooltip(
          `<strong>${p.woodland_kind || 'woodland'}</strong><br>` +
          `${p.area_ha ? (Math.round(p.area_ha * 100) / 100).toLocaleString() + ' ha<br>' : ''}` +
          `<small>${descr}</small><br>` +
          `<small style="color:#9ca3af">${p.forest_source || ''}</small>`,
          { sticky: true, direction: 'top', className: 'lqv-tooltip' }
        );
      },
    });
  }

  // 2. OSM 10km layers
  // The OSM pulls cover thousands of features each; wrap in try/catch
  // so a single fetch failure doesn't stop the rest of the boot.
  // We use Promise.allSettled so we get the count of every layer that
  // loaded, even if some failed.
  let counts = [0, 0, 0, 0, 0, 0];
  try {
    const settled = await Promise.allSettled([
      loadLQVLayer('roads',      './data/osm_10km/roads.geojson',      roadStyle),
      loadLQVLayer('water',      './data/osm_10km/water.geojson',      waterStyle),
      loadLQVLayer('waterways',  './data/osm_10km/waterways.geojson',  waterwaysStyle),
      loadLQVLayer('trees',      './data/osm_10km/trees.geojson',      treesStyle),
      loadLQVLayer('buildings',  './data/osm_10km/buildings.geojson',  buildingStyle),
      loadLQVLayer('landuse',    './data/osm_10km/landuse.geojson',    landuseStyle),
    ]);
    counts = settled.map(s => s.status === 'fulfilled' ? s.value : 0);
    const failed = settled.filter(s => s.status === 'rejected');
    failed.forEach((f, i) => console.warn(
      `OSM 20 km load ${i} failed:`, f.reason
    ));
    console.log(`OSM 20 km loaded: roads=${counts[0]}  water=${counts[1]}  `
       + `waterways=${counts[2]}  trees=${counts[3]}  `
       + `buildings=${counts[4]}  landuse=${counts[5]}`);
  } catch (err) {
    console.warn('OSM 20 km block failed:', err);
  }
  // Belt and suspenders: re-emit the count for every layer that
  // did manage to load. Some style callbacks may throw during the
  // .addTo() phase and silently drop the layer; this ensures the
  // sidebar count is visible regardless.
  for (const k of ['roads','water','waterways','trees','buildings','landuse']) {
    if (data[k] && data[k].features) {
      setLayerCount(k, data[k].features.length);
    }
  }

  // 2b. Surface water 20 km (audited OSM polygons + waterways)
  // Each polygon has an audit_class set by scripts/audit_wetlands_10km.py:
  //   verified_lake, verified_wetland, seasonal_wetland, in_stream_pool,
  //   river_polygon, ambiguous, likely_mis-tagged, river, stream_water, ditch, canal
  const auditedWaterStyle = (feature) => {
    const cls = feature.properties?.audit_class || 'ambiguous';
    const color = feature.properties?.audit_color || '#3b82f6';
    return {
      color: color,
      weight: 2,
      opacity: 0.95,
      fillOpacity: cls === 'likely_mis-tagged' ? 0.25 :
                  cls === 'ambiguous' ? 0.3 :
                  cls.startsWith('verified') ? 0.7 :
                  cls === 'seasonal_wetland' ? 0.6 :
                  cls === 'in_stream_pool' ? 0.65 : 0.45,
      fillColor: color,
      dashArray: cls === 'likely_mis-tagged' ? '2 4' :
                 cls === 'ambiguous' ? '3 3' : null,
    };
  };
  const auditedWater = await F('./data/surface_water_10km.geojson');
  if (auditedWater && auditedWater.features) {
    data['surface-water'] = auditedWater;
    setLayerCount('surface-water', auditedWater.features.length);
    totalFeatures += auditedWater.features.length;
    layers['surface-water'] = L.geoJSON(auditedWater, {
      style: auditedWaterStyle,
      onEachFeature: (feature, lyr) => {
        const p = feature.properties || {};
        const cls = p.audit_class || '?';
        const jrc = p.audit_jrc_occurrence_mean;
        const cls_emoji = {
          'verified_lake':     '✓',
          'verified_wetland':  '✓',
          'seasonal_wetland':  '~',
          'in_stream_pool':    '≈',
          'river_polygon':     'R',
          'river':             'R',
          'stream_water':      'r',
          'ambiguous':         '?',
          'likely_mis-tagged': '✗',
        }[cls] || '·';
        const jrcText = (jrc != null && !Number.isNaN(jrc))
            ? `${jrc.toFixed(0)}% JRC occurrence` : 'no JRC sample';
        const html = `<strong>${cls_emoji} ${cls.replace(/_/g,' ')}</strong><br>` +
                     `${p.audit_class || ''}<br>` +
                     `OSM tags: natural=${p.natural || '—'}, water=${p.water || '—'}, wetland=${p.wetland || '—'}<br>` +
                     `${jrcText} · area ≈ ${((p.audit_area_m2 || 0)/10000).toFixed(2)} ha<br>` +
                     `Slope ≈ ${p.audit_dem_slope_proxy_deg ?? '?'}° · ` +
                     `DEM ${p.audit_dem_elev_min_m ?? '?'}-${p.audit_dem_elev_max_m ?? '?'} m<br>` +
                     (p.audit_centroid_near_waterway ? 'Within 200 m of an OSM waterway ✓' : '');
        lyr.bindTooltip(html, { sticky: true, direction: 'top', className: 'lqv-tooltip' });
      },
    });
  }

  // 2c-bis. HAND floodplain layer (P1-1) — DEM-derived wetland mapper.
  const handFc = await F('./data/hand_10km.geojson');
  if (handFc && handFc.features) {
    data['hand'] = handFc;
    setLayerCount('hand', handFc.features.length);
    totalFeatures += handFc.features.length;
    layers['hand'] = L.geoJSON(handFc, {
      style: (feature) => ({
        color: feature.properties.color || '#67e8f9',
        fillColor: feature.properties.color || '#67e8f9',
        fillOpacity: 0.45,
        weight: 0.4,
      }),
      onEachFeature: (feature, lyr) => {
        const p = feature.properties || {};
        lyr.bindTooltip(
          `<strong>HAND ${p.hand_low_m}-${p.hand_high_m} m</strong><br>` +
          `${p.name || ''}<br>` +
          `${(p.area_ha || 0).toFixed(2)} ha<br>` +
          `<small>${p.description || ''}</small>`,
          { sticky: true, direction: 'top', className: 'lqv-tooltip' }
        );
      },
    });
  }

  // 2c. JRC verified water bodies (only what satellite actually sees)
  const jrcWater = await F('./data/lqv_jrc_waterbodies_10km.geojson');
  if (jrcWater && jrcWater.features && jrcWater.features.length) {
    data['jrc-water'] = jrcWater;
    setLayerCount('jrc-water', jrcWater.features.length);
    totalFeatures += jrcWater.features.length;
    layers['jrc-water'] = L.geoJSON(jrcWater, {
      style: (feature) => ({
        color: feature.properties.audit_color || '#0ea5e9',
        weight: 1,
        fillColor: feature.properties.audit_color || '#0ea5e9',
        fillOpacity: 0.7,
        opacity: 0.95,
      }),
      onEachFeature: (feature, lyr) => {
        const p = feature.properties || {};
        lyr.bindTooltip(
          `<strong>${p.audit_class} waterbody</strong><br>` +
          `${p.audit_jrc_occurrence_mean}% JRC occurrence (1984-2024)<br>` +
          `Area: ${p.audit_area_ha} ha<br>` +
          `${p.name || ''}`,
          { sticky: true, direction: 'top', className: 'lqv-tooltip' }
        );
      },
    });
  }

  // 3. Places (with permanent labels)
  const places = await F('./data/osm_10km/places.geojson');
  if (places && places.features) {
    data.places = places;
    setLayerCount('places', places.features.length);
    totalFeatures += places.features.length;
    layers.places = L.geoJSON(places, {
      pointToLayer: (feature, latlng) => L.circleMarker(latlng, placeStyle(feature)),
      onEachFeature: (feature, lyr) => bindInfoPopup(feature, lyr),
    });
    // Permanent labels for city + town + suburb at z >= 11; villages at z >= 13
    const all = places.features.filter(f => (f.properties.name || '').trim() && f.properties.place !== 'city_block');
    const seen = new Set();
    const uniq = [];
    for (const f of all) {
      const n = f.properties.name.trim();
      if (!seen.has(n)) { seen.add(n); uniq.push(f); }
    }
    // rank by importance: city > town > suburb > village > neighbourhood > hamlet
    const rank = { city: 0, town: 1, suburb: 2, neighbourhood: 3, village: 4, hamlet: 5, locality: 6, isolated_dwelling: 7, farm: 8 };
    uniq.sort((a, b) => (rank[a.properties.place] ?? 9) - (rank[b.properties.place] ?? 9));
    const big   = uniq.filter(f => ['city','town','suburb','neighbourhood'].includes(f.properties.place));
    const small = uniq.filter(f => !['city','town','suburb','neighbourhood'].includes(f.properties.place));
    addPermanentLabels('places', { features: big },   () => true, { minZoom: 11, maxLabels: 50, direction: 'right', offset: [10, 0] });
    addPermanentLabels('places', { features: small }, () => true, { minZoom: 14, maxLabels: 50, direction: 'right', offset: [10, 0] });
  }

  // 4. POIs as cluster group (avoids 18,252 individual point icons)
  const pois = await F('./data/osm_10km/pois.geojson');
  if (pois && pois.features) {
    data.pois = pois;
    setLayerCount('pois', pois.features.length);
    totalFeatures += pois.features.length;
    const cluster = L.markerClusterGroup({
      maxClusterRadius: 50,
      showCoverageOnHover: false,
      spiderfyOnMaxZoom: true,
      disableClusteringAtZoom: 16,
    });
    pois.features.forEach(f => {
      const g = f.geometry;
      if (!g || g.type !== 'Point') return;
      const m = poiDivIcon(f, [g.coordinates[1], g.coordinates[0]]);
      bindInfoPopup(f, m);
      cluster.addLayer(m);
    });
    layers.pois = cluster;
  }

  // 5. Add permanent labels for major rivers / roads visible at z >= 13
  if (data.waterways) {
    const rivers = data.waterways.features
      .filter(f => (f.properties.waterway === 'river' || f.properties.waterway === 'stream') && (f.properties.name || '').trim());
    if (rivers.length) {
      const stops = [];
      rivers.forEach(f => {
        // label at the line's mid-point
        const g = f.geometry;
        let coords;
        if (g.type === 'LineString') coords = g.coordinates;
        else if (g.type === 'MultiLineString') coords = g.coordinates.flat();
        if (!coords || !coords.length) return;
        const mid = coords[Math.floor(coords.length/2)];
        const label = f.properties.name.trim();
        const t = L.tooltip({ permanent: true, direction: 'top', className: 'permanent', offset: [0, -4] })
          .setLatLng([mid[1], mid[0]]).setContent(label);
        stops.push({ tooltip: t, minZoom: 13 });
      });
      labels.waterways = stops;
      const update = () => {
        const z = map.getZoom();
        const visible = z >= 13 && map.hasLayer(layers.waterways);
        stops.forEach(({ tooltip }) => {
          const onMap = map.hasLayer(tooltip);
          if (visible && !onMap) tooltip.addTo(map);
          else if (!visible && onMap) map.removeLayer(tooltip);
        });
      };
      map.on('zoomend', update);
      map.on('layeradd layerremove', update);
      update();
    }
  }
  if (data.roads) {
    // Show road refs/names at z>=12 (already a pretty close-in zoom)
    const major = data.roads.features
      .filter(f => ['trunk','primary','secondary'].includes(f.properties.highway) && (f.properties.name || f.properties.ref))
      .slice(0, 80);
    if (major.length) {
      const stops = [];
      major.forEach(f => {
        const g = f.geometry;
        let coords;
        if (g.type === 'LineString') coords = g.coordinates;
        else if (g.type === 'MultiLineString') coords = g.coordinates.flat();
        if (!coords || !coords.length) return;
        const mid = coords[Math.floor(coords.length/2)];
        const label = f.properties.ref || f.properties.name;
        const t = L.tooltip({ permanent: true, direction: 'top', className: 'permanent', offset: [0, -6], opacity: 0.9 })
          .setLatLng([mid[1], mid[0]]).setContent(label);
        stops.push({ tooltip: t, minZoom: 12 });
      });
      labels.roads = stops;
      const update = () => {
        const z = map.getZoom();
        const visible = z >= 12 && map.hasLayer(layers.roads);
        stops.forEach(({ tooltip }) => {
          const onMap = map.hasLayer(tooltip);
          if (visible && !onMap) tooltip.addTo(map);
          else if (!visible && onMap) map.removeLayer(tooltip);
        });
      };
      map.on('zoomend', update);
      map.on('layeradd layerremove', update);
      update();
    }
  }

  // 7. Default-on layers — the GPS polygon + corners + features are now ON by default
  ['parcel','gps-corners','gps-features','roads','water','waterways','places'].forEach(n => {
    if (layers[n] && !map.hasLayer(layers[n])) {
      layers[n].addTo(map);
    }
  });

  // 7. Bring parcel layer to front (pulse + core added above)
  if (layers.parcel) {
    layers.parcel.bringToFront();
  }
  // Re-order: pulse below core but above parcel
  parcelPulse.bringToFront();
  parcelCore.bringToFront();

  // 7b. Hillshade sits below everything (over satellite tiles but under
  // all vector overlays).
  if (layers.hillshade && map.hasLayer(layers.hillshade)) {
    layers.hillshade.bringToBack();
  }
  if (layers['ndvi-backdrop'] && map.hasLayer(layers['ndvi-backdrop'])) {
    layers['ndvi-backdrop'].bringToBack();
  }

  // 8. Re-fit to 10km bbox
  map.fitBounds(BBOX_10KM, { padding: [30, 30] });

  // 9. Hide the loading banner once all data is rendered
  const lb = document.getElementById('loading');
  if (lb) lb.classList.add('hidden');

  // 9. Apply initial opacities from sliders (the init loop already wired inputs)
  document.querySelectorAll('[data-opacity]').forEach(slider => {
    applyOpacity(slider.dataset.opacity, parseFloat(slider.value));
  });

  // 10. Loading banner off + total stat
  setTimeout(() => document.getElementById('loading').classList.add('hidden'), 400);
  const stat = document.getElementById('total-stat');
  if (stat) stat.textContent = totalFeatures.toLocaleString() + ' features';

  // 11. Distance from parcel to nearest town + road on label level
  const d = (a, b) => Math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2);
  function km(a, b) {
    const R = 6371;
    const p1 = a[0]*Math.PI/180, p2 = b[0]*Math.PI/180;
    const dp = (b[0]-a[0])*Math.PI/180, dl = (b[1]-a[1])*Math.PI/180;
    const x = Math.sin(dp/2)**2 + Math.cos(p1)*Math.cos(p2)*Math.sin(dl/2)**2;
    return 2*R*Math.asin(Math.sqrt(x));
  }
  let nearestT = null, nearestT_km = Infinity;
  if (data.places) {
    for (const f of data.places.features) {
      const p = f.properties.place;
      if (!['city','town','village'].includes(p)) continue;
      const g = f.geometry;
      if (g.type !== 'Point') continue;
      const dist = km(CENTER, [g.coordinates[1], g.coordinates[0]]);
      if (dist < nearestT_km) { nearestT_km = dist; nearestT = f.properties.name; }
    }
  }
  let nearestR = null, nearestR_km = Infinity;
  if (data.roads) {
    for (const f of data.roads.features) {
      const h = f.properties.highway;
      if (!['trunk','primary','secondary','tertiary'].includes(h)) continue;
      const g = f.geometry;
      let coords = g.type === 'LineString' ? g.coordinates : g.coordinates.flat();
      // sample mid-point to avoid full polyline
      const mid = coords[Math.floor(coords.length/2)];
      const dist = km(CENTER, [mid[1], mid[0]]);
      if (dist < nearestR_km) { nearestR_km = dist; nearestR = f.properties.ref || f.properties.name || f.properties.highway; }
    }
  }
  const dEl = document.getElementById('distance-stat');
  if (dEl && (nearestT || nearestR)) {
    dEl.innerHTML = ` · ${nearestT ? `<b>${nearestT}</b> ${nearestT_km.toFixed(1)} km` : ''}${nearestR ? ` · paved road ${nearestR_km.toFixed(1)} km` : ''}`;
  }
})();

// ---- Opacity applier ----
function applyOpacity(name, opacity) {
  const lyr = layers[name];
  if (!lyr) return;
  try {
    if (lyr.setStyle) lyr.setStyle(f => ({ ...roadStyle(f), opacity: (roadStyle(f).opacity ?? 0.9) * opacity }));
    else if (lyr.setOpacity) lyr.setOpacity(opacity);
  } catch (e) {
    // Layer doesn't take a fill-opacity (e.g. layer groups / clusters); set on each child
    lyr.eachLayer(sub => {
      if (sub.setOpacity) sub.setOpacity(opacity);
    });
  }
  // P2-6: persist opacity to localStorage
  try {
    const k = 'lqv-opacity-' + name;
    localStorage.setItem(k, String(opacity));
  } catch (e) {}
}

// Slider click should not toggle parent checkbox — the <label> nesting
// would otherwise toggle the row's checkbox when the user grabs the slider.
document.querySelectorAll('[data-opacity]').forEach(slider => {
  slider.addEventListener('mousedown', e => e.stopPropagation());
  slider.addEventListener('click',     e => e.stopPropagation());
  slider.addEventListener('input',     e => {
    e.stopPropagation();
    applyOpacity(slider.dataset.opacity, parseFloat(slider.value));
  });
});

// P2-6: restore opacities from localStorage on boot
function restoreOpacities() {
  document.querySelectorAll('[data-opacity]').forEach(slider => {
    try {
      const v = localStorage.getItem('lqv-opacity-' + slider.dataset.opacity);
      if (v !== null && Number.isFinite(parseFloat(v))) {
        slider.value = v;
        applyOpacity(slider.dataset.opacity, parseFloat(v));
      }
    } catch (e) {}
  });
}
setTimeout(restoreOpacities, 2000);

// ---- Sidebar search filter ----
document.getElementById('layer-search').addEventListener('input', e => {
  const q = e.target.value.trim().toLowerCase();
  const rows = document.querySelectorAll('.sidebar-section');
  let matchCount = 0;
  rows.forEach(sec => {
    if (!sec.querySelector('.layer-row')) return;  // skip sections without rows (Basemap, Actions, About)
    let visible = 0;
    sec.querySelectorAll('.layer-row').forEach(row => {
      const text = (row.textContent || '').toLowerCase();
      const dataLayer = row.querySelector('[data-layer]')?.dataset?.layer || '';
      const haystack = text + ' ' + dataLayer;
      const match = q === '' || haystack.includes(q);
      row.classList.toggle('hidden', !match);
      if (match) visible += 1;
    });
    sec.classList.toggle('empty-section', visible === 0);
    matchCount += visible;
  });
  const countEl = document.getElementById('search-count');
  if (q === '') countEl.textContent = '';
  else countEl.textContent = matchCount + ' layer' + (matchCount === 1 ? '' : 's') + ' match';
});

// ---- In-map legend ----
const LEGEND_DATA = {
  'parcel': { swatch: 'var(--gold)', name: 'GPS perimeter', kind: 'line' },
  'gps-corners': { swatch: '#fef3c7;border:1.5px solid var(--gold)', name: 'GPS corners', kind: 'point' },
  'gps-features': { swatch: '#1d4ed8', name: 'Named features', kind: 'point' },
  'hillshade': { swatch: 'linear-gradient(45deg,#444 25%,#aaa 25% 50%,#444 50% 75%,#aaa 75%)', name: 'Hillshade backdrop', kind: 'raster' },
  'hillshade-parcel': { swatch: 'linear-gradient(135deg,#3a3a3a,#888 60%,#3a3a3a)', name: 'Hillshade (parcel-scale, 5m topology)', kind: 'raster' },
  'ndvi-backdrop': { swatch: 'linear-gradient(to right,#a16207 25%,#84cc16 25% 50%,#22c55e 50% 75%,#14532d 75%)', name: 'NDVI continuous backdrop', kind: 'raster' },
  'color-relief': { swatch: 'linear-gradient(to right,#94c864 0%,#c2c068 50%,#914530 100%)', name: 'Elevation colour-relief', kind: 'raster' },
  'contours': { swatch: 'linear-gradient(to right,#f0f9ff 11%,#38bdf8 33%,#0284c7 55%,#0c4a6e 100%)', name: 'Elevation contours (50 m)', kind: 'line' },
  'contours-parcel': { swatch: 'linear-gradient(to right,#7dd3fc 25%,#0284c7 50%,#0c4a6e 100%)', name: 'Parcel contours (5 m topo)', kind: 'line' },
  'local-quebrada': { swatch: '#1d4ed8', name: 'LQV quebrada (ground-truth)', kind: 'line' },
  'streams-10km': { swatch: 'linear-gradient(to right,#0c4a6e 0 35%,#3b82f6 35% 60%,#93c5fd 60% 100%)', name: 'DEM quebrada streams', kind: 'line' },
  'flow-arrows': { swatch: '#1d4ed8', name: 'Flow direction arrows', kind: 'point' },
  'waterways': { swatch: '#60a5fa', name: 'OSM streams & rivers', kind: 'line' },
  'water': { swatch: '#2563eb', name: 'OSM water polygons', kind: 'polygon' },
  'surface-water': { swatch: '#0ea5e9', name: 'Audited wetlands', kind: 'polygon' },
  'hand': {
    swatch: 'gradient', kind: 'polygon',
    sections: [
      { title: 'HAND floodplain (DEM-derived)', rows: [
        { swatch: '#0ea5e9', name: '0–1 m floodplain' },
        { swatch: '#22d3ee', name: '1–5 m riparian wetland' },
        { swatch: '#67e8f9', name: '5–15 m hillslope wetland' },
        { swatch: '#e2e8f0', name: '>15 m upland' },
      ]}
    ]
  },
  'jrc-water': { swatch: '#0369a1;border:1px dashed white', name: 'JRC waterbodies', kind: 'polygon' },
  'combined-water': { swatch: 'linear-gradient(to right,#0c4a6e 0 30%,#0ea5e9 30% 50%,#a78bfa 50% 70%,#f87171 70% 100%)', name: 'Combined water (4 sources)', kind: 'mixed' },
  'canopy-10km': {
    swatch: 'gradient', kind: 'polygon',
    sections: [
      { title: 'Sentinel-2 NDVI (4 classes)', rows: [
        { swatch: '#a16207', name: '< 0.25 bare / grass' },
        { swatch: '#84cc16', name: '0.25–0.45 sparse woody' },
        { swatch: '#22c55e', name: '0.45–0.60 open forest' },
        { swatch: '#14532d', name: '> 0.60 dense forest' },
      ]}
    ]
  },
  'mapbiomas': {
    swatch: 'gradient', kind: 'polygon',
    sections: [
      { title: 'MapBiomas 2023 (10 classes)', rows: [
        { swatch: '#15803d', name: '3 · Forest Formation' },
        { swatch: '#0d9488', name: '6 · Flooded Forest' },
        { swatch: '#a16207', name: '9 · Forest Plantation' },
        { swatch: '#06b6d4', name: '11 · Wetland' },
        { swatch: '#bef264', name: '12 · Grassland' },
        { swatch: '#fbbf24', name: '15 · Pasture' },
        { swatch: '#ea580c', name: '18 · Agriculture' },
        { swatch: '#94a3b8', name: '22 · Non-vegetated' },
        { swatch: '#0284c7', name: '26 · Water' },
      ]}
    ]
  },
  'hansen-loss': { swatch: '#dc2626', name: 'Hansen forest loss (2001–2024)', kind: 'polygon' },
  'hansen-gain': { swatch: '#22c55e', name: 'Hansen forest gain (2000–2012)', kind: 'polygon' },
  'woodland-merged': {
    swatch: 'gradient', kind: 'polygon',
    sections: [
      { title: 'Woodland merged (4 sources)', rows: [
        { swatch: '#15803d', name: 'MapBiomas Forest Formation' },
        { swatch: '#0d9488', name: 'MapBiomas Flooded Forest' },
        { swatch: '#365314', name: 'Hansen ≥75% canopy' },
        { swatch: '#166534', name: 'Hansen ≥30% canopy' },
        { swatch: '#22c55e', name: 'OSM natural=wood' },
      ]}
    ]
  },
  'trees': { swatch: '#15803d', name: 'OSM tags (mixed)', kind: 'polygon' },
  'roads': { swatch: 'var(--gold)', name: 'OSM roads & tracks', kind: 'line' },
  'places': { swatch: '#be185d', name: 'OSM towns & villages', kind: 'point' },
  'pois': { swatch: '#a855f7', name: 'OSM POIs', kind: 'point' },
  'landuse': { swatch: '#fcd34d', name: 'OSM land use polygons', kind: 'polygon' },
  'buildings': { swatch: '#a3a3a3', name: 'OSM buildings', kind: 'polygon' },
  'gps-walking-path': { swatch: 'transparent;border:2px solid #f59e0b', name: 'Walking track', kind: 'line' },
  'gps-sessions': { swatch: 'linear-gradient(to right,#a855f7 50%,#f59e0b 50%)', name: 'Walking sessions', kind: 'line' },
  'escobar-legacy': { swatch: 'transparent;border:1.5px dashed #94a3b8', name: '30.9 ha KML (legacy)', kind: 'polygon' },
  'aoi62-legacy': { swatch: 'transparent;border:1.5px dashed #a8a29e', name: '62 ha AOI (legacy)', kind: 'polygon' },
};
function updateMapLegend() {
  const body = document.getElementById('map-legend-body');
  if (!body) return;
  const active = [...document.querySelectorAll('[data-layer]:checked')]
    .map(cb => cb.dataset.layer)
    .filter(n => LEGEND_DATA[n] && n !== 'parcel' && n !== 'gps-corners' && n !== 'gps-features');
  if (active.length === 0) {
    body.innerHTML = '<div class="map-legend-empty">No data layers active.</div>';
    return;
  }
  let html = '';
  active.forEach(name => {
    const entry = LEGEND_DATA[name];
    if (entry.sections) {
      html += `<div class="map-legend-section">`;
      entry.sections.forEach(sec => {
        html += `<div class="map-legend-section-title">${sec.title}</div>`;
        sec.rows.forEach(r => {
          html += `<div class="map-legend-row"><span class="map-legend-swatch" style="background:${r.swatch}"></span><span class="map-legend-text">${r.name}</span></div>`;
        });
      });
      html += `</div>`;
    } else {
      const countEl = document.querySelector(`[data-count="${name}"]`);
      const count = countEl ? countEl.textContent : '';
      html += `<div class="map-legend-row"><span class="map-legend-swatch" style="background:${entry.swatch}"></span><span class="map-legend-text">${entry.name}</span>${count && count !== '—' ? `<span class="map-legend-count">${count}</span>` : ''}</div>`;
    }
  });
  body.innerHTML = html;
}

// ---- Toggle handlers ----
document.querySelectorAll('[data-layer]').forEach(cb => {
  cb.addEventListener('change', e => {
    const name = cb.dataset.layer;
    const lyr  = layers[name];
    if (!lyr) return;
    if (cb.checked) {
      lyr.addTo(map);
      if (name === 'parcel') lyr.bringToFront();
    } else {
      map.removeLayer(lyr);
    }
    // Also cancel checkbox toggle if event came from slider click
    if (e && e.target?.type === 'range') {
      e.preventDefault();
    }
    updateURLHash();
    updateMapLegend();
  });
});

// Initial legend render after boot
window.addEventListener('load', () => setTimeout(() => {
  updateMapLegend();
  // P2-5: set print date in topbar
  const tb = document.querySelector('header.topbar');
  if (tb) tb.dataset.printDate = new Date().toISOString().slice(0, 10);
}, 1500));
setInterval(updateMapLegend, 5000);  // refresh counts as data loads

// P2-1: Property coverage matrix in About section
function updateCoverageMatrix() {
  const tbody = document.getElementById('coverage-matrix-body');
  if (!tbody) return;
  const rows = [];
  Object.keys(parcelInsideCounts).forEach(name => {
    const fc = data[name];
    if (!fc) return;
    const total = (fc.features || []).length;
    const inside = parcelInsideCounts[name] || 0;
    rows.push({ name, total, inside });
  });
  rows.sort((a, b) => b.inside - a.inside);
  if (rows.length === 0) {
    tbody.innerHTML = '<tr><td colspan="3" style="color: var(--muted); font-style: italic;">No layers loaded yet.</td></tr>';
    return;
  }
  let html = '';
  rows.forEach(r => {
    const cls = r.inside > 0 ? 'has-coverage' : '';
    html += `<tr class="${cls}"><td>${r.name}</td><td>${r.total.toLocaleString()}</td><td>${r.inside.toLocaleString()}</td></tr>`;
  });
  tbody.innerHTML = html;
}
setTimeout(updateCoverageMatrix, 4000);
setInterval(updateCoverageMatrix, 8000);

// P2-7: Forest-change timeline chart (MapBiomas 1985 → 2023)
(async function renderForestTimeline() {
  try {
    const r = await fetch('./data/mapbiomas_forest_timeline.json');
    const tl = await r.json();
    const chart = document.getElementById('forest-timeline-chart');
    const text = document.getElementById('forest-timeline-text');
    if (!chart || !text || !tl.years) return;
    const W = chart.clientWidth || 280;
    const H = 88;
    const PAD = 20;
    const years = tl.years;
    const xs = years.map((_, i) => PAD + (W - 2*PAD) * i / (years.length - 1));
    const maxArea = Math.max(...tl.forest_area_ha);
    const minArea = Math.min(...tl.forest_area_ha);
    const ys = tl.forest_area_ha.map(v => H - PAD - (H - 2*PAD) * (v - minArea) / (maxArea - minArea || 1));
    const path = xs.map((x, i) => `${i===0?'M':'L'}${x},${ys[i]}`).join(' ');
    const area = `${path} L${xs[xs.length-1]},${H-PAD} L${xs[0]},${H-PAD} Z`;
    let svg = `<svg viewBox="0 0 ${W} ${H}" xmlns="http://www.w3.org/2000/svg">`;
    svg += `<path d="${area}" fill="rgba(21,128,61,0.18)" />`;
    svg += `<path d="${path}" stroke="#15803d" stroke-width="2" fill="none" />`;
    xs.forEach((x, i) => {
      svg += `<circle cx="${x}" cy="${ys[i]}" r="2.5" fill="#15803d" />`;
      svg += `<text x="${x}" y="${H-4}" font-size="8" text-anchor="middle" fill="#666">${years[i]}</text>`;
    });
    // Y-axis labels
    svg += `<text x="${W-2}" y="10" font-size="8" text-anchor="end" fill="#666">${(maxArea/1000).toFixed(1)}k ha</text>`;
    svg += `<text x="${W-2}" y="${H-PAD}" font-size="8" text-anchor="end" fill="#666">${(minArea/1000).toFixed(1)}k ha</text>`;
    svg += `</svg>`;
    chart.innerHTML = svg;
    text.innerHTML = `Forest area ${tl.forest_area_ha[0].toLocaleString()} → ${tl.forest_area_ha[tl.forest_area_ha.length-1].toLocaleString()} ha (${tl.change_pct >= 0 ? '+' : ''}${tl.change_pct}%) · parcel stable at ~${tl.parcel_inside_ha[0].toFixed(0)} ha`;
  } catch (e) {
    console.warn('forest timeline load failed:', e);
  }
})();

// ---- Measure tool (simple polyline ruler) ----
let measureMode = false;
let measurePoints = [];
let measureLine = null;
let measureMarkers = [];
function clearMeasure() {
  if (measureLine) { map.removeLayer(measureLine); measureLine = null; }
  measureMarkers.forEach(m => map.removeLayer(m));
  measureMarkers = [];
}
document.getElementById('measure-btn').onclick = () => {
  measureMode = !measureMode;
  document.getElementById('measure-btn').style.background = measureMode ? 'var(--gold)' : '';
  document.getElementById('measure-btn').style.color      = measureMode ? 'white' : '';
  if (!measureMode) clearMeasure();
  measurePoints = [];
};
map.on('click', e => {
  if (!measureMode) return;
  measurePoints.push(e.latlng);
  const mk = L.circleMarker(e.latlng, { radius: 4, color: '#c89b3c', fillColor: '#c89b3c', fillOpacity: 1 }).addTo(map);
  measureMarkers.push(mk);
  if (measurePoints.length >= 2) {
    if (measureLine) map.removeLayer(measureLine);
    const fmt = (m) => m < 1000 ? `${m.toFixed(0)} m` : `${(m/1000).toFixed(2)} km`;
    measureLine = L.polyline(measurePoints, { color: '#c89b3c', weight: 3, dashArray: '6 4' }).addTo(map);
    let total = 0;
    for (let i = 1; i < measurePoints.length; i++) total += measurePoints[i-1].distanceTo(measurePoints[i]);
    measureLine.bindTooltip(`Total: ${fmt(total)}`, { sticky: true, direction: 'center', className: 'lqv-tooltip' });
  }
});

// ---- Keyboard shortcuts ----
window.addEventListener('keydown', e => {
  if (e.key === 'm' || e.key === 'M') document.getElementById('measure-btn').click();
  if (e.key === '[' && document.getElementById('sidebar-collapse')) document.getElementById('sidebar-collapse').click();
  // number keys 1-6 = presets
  if (e.key === '1') applyPreset('all');
  if (e.key === '2') applyPreset('none');
  if (e.key === '3') applyPreset('property');
  if (e.key === '4') applyPreset('water');
  if (e.key === '5') applyPreset('forest');
  if (e.key === '6') applyPreset('terrain');
});

// ---- Mobile drawer ----
function toggleDrawer(open) {
  const sb = document.getElementById('sidebar');
  const bd = document.getElementById('drawer-backdrop');
  if (open === undefined) {
    open = !sb.classList.contains('open');
  }
  sb.classList.toggle('open', open);
  if (bd) bd.classList.toggle('visible', open);
}
document.getElementById('drawer-toggle').onclick = () => toggleDrawer();
const _backdrop = document.getElementById('drawer-backdrop');
if (_backdrop) _backdrop.onclick = () => toggleDrawer(false);

// ---- WALKING-PATH REPLAY (time scrubber) ----
// Build a virtual "playhead" dot that travels along Wes's path so you can
// see the perimeter being captured in time order. Uses the
// client_gps_walking_path GeoJSON (timestamps ISO8601).
let replayMarker = null;
let replayLine = null;
let replayPlaying = false;
let replayT = 0;
let replayReq = null;

function rebuildReplay() {
  if (replayMarker) { map.removeLayer(replayMarker); replayMarker = null; }
  if (replayLine)  { map.removeLayer(replayLine);  replayLine  = null; }
  const fc = data['gps-walking-path'];
  if (!fc || !fc.features.length) return;
  const feature = fc.features[0];
  const coords = feature.geometry.coordinates;
  const timestamps = feature.properties.timestamps || [];
  replayLine = L.polyline(coords.map(c => [c[1], c[0]]), {
    color: '#c89b3c', weight: 2.5, opacity: 0.6, dashArray: '4 4',
  }).addTo(map);
  replayMarker = L.circleMarker(coords[0].slice().reverse(), {
    radius: 8, color: '#c89b3c', fillColor: '#fef3c7', weight: 2.5, fillOpacity: 1,
  }).addTo(map).bindTooltip('Walk start', { permanent: false, direction: 'top', className: 'lqv-tooltip' });
}

function updateReplay(t) {
  const fc = data['gps-walking-path'];
  if (!fc || !replayMarker) return;
  const coords = fc.features[0].geometry.coordinates;
  const timestamps = fc.features[0].properties.timestamps || [];
  if (!coords.length) return;
  const n = Math.max(1, coords.length - 1);
  const idx = Math.min(Math.floor((t / 100) * n), coords.length - 1);
  const [lon, lat] = coords[idx];
  replayMarker.setLatLng([lat, lon]);
  // Truncate the polyline to the current point
  if (replayLine) {
    const upTo = coords.slice(0, idx + 1).map(c => [c[1], c[0]]);
    replayLine.setLatLngs(upTo);
  }
  const lbl = timestamps[idx] ? new Date(timestamps[idx]).toUTCString().slice(0, 22) : '';
  if (replayMarker.getTooltip()) replayMarker.getTooltip().setContent(`#${idx+1}/${coords.length} · ${lbl}`);
  // Highlight the corner if it coincides with a GPS corner feature
  const status = document.getElementById('replay-status');
  if (status) status.textContent = lbl ? `#${idx+1}/${coords.length} · ${lbl}` : `#${idx+1}/${coords.length}`;
}

document.getElementById('replay-btn').onclick = () => {
  const fc = data['gps-walking-path'];
  if (!fc) { alert('Walking path not loaded yet — wait a moment and try again.'); return; }
  if (!replayMarker) rebuildReplay();
  replayPlaying = !replayPlaying;
  const btn = document.getElementById('replay-btn');
  const durMs = getReplayRealDurationMs();
  const durMin = Math.round(durMs / 60000);
  btn.textContent = replayPlaying ? '⏸ Pause' : `▶ Replay walk (~${durMin} min)`;
  btn.style.background = replayPlaying ? 'var(--gold)' : '';
  if (replayPlaying) replayStep();
};

function replayStep() {
  if (!replayPlaying) return;
  replayT = Math.min(100, replayT + 0.6);
  document.getElementById('replay-time').value = replayT;
  updateReplay(replayT);
  if (replayT >= 100) {
    replayPlaying = false;
    document.getElementById('replay-btn').textContent = '▶ Replay walk';
    document.getElementById('replay-btn').style.background = '';
    return;
  }
  replayReq = requestAnimationFrame(replayStep);
}

// P2-3: replay duration estimate based on real timestamps.
// We compute the wall-clock duration of Wes's actual walk and use
// it to pace the playback (1 second of replay = ~N seconds of wall time).
function getReplayRealDurationMs() {
  const fc = data['gps-walking-path'];
  if (!fc || !fc.features[0]) return 60000;
  const ts = fc.features[0].properties.timestamps || [];
  if (ts.length < 2) return 60000;
  try {
    const a = new Date(ts[0]).getTime();
    const b = new Date(ts[ts.length-1]).getTime();
    return Math.max(5000, b - a);
  } catch (e) { return 60000; }
}

document.getElementById('replay-time').addEventListener('input', e => {
  replayT = parseFloat(e.target.value);
  if (replayMarker) updateReplay(replayT);
});

// ---- Action buttons ----
document.getElementById('zoom-fit').onclick = () => map.fitBounds(BBOX_10KM, { padding: [20, 20] });
document.getElementById('zoom-parcel').onclick = () => {
  if (data.parcel) map.fitBounds(layers.parcel.getBounds(), { padding: [60, 60], maxZoom: 16 });
};

// ════════════════════════════════════════════════════════════════
// PRESET BAR — turn on a coordinated set of layers in one click
// ════════════════════════════════════════════════════════════════
//
// "all" = every layer on; "none" = everything off; "property/water/forest/
// terrain/context" = only layers whose data-preset-group includes that token.
//
// Why: with 30+ layers the user wanted "one select-all button + easy presets"
// so they can swap context in one click (e.g. "I want to see the water story").
//
// Active preset gets the .active highlight on its button so the user knows
// what's on. The "all" / "none" buttons are intentionally separate from
// the contextual presets so a user can pick a meaningful subset without
// having to wade through the full list.
const PRESET_GROUPS = {
  all:      null, // special-cased below
  none:     [],   // special-cased below
  property: ['property'],
  water:    ['water'],
  forest:   ['forest'],
  terrain:  ['terrain'],
  context:  ['context'],
};

// Layers that are part of "context" but should stay ON when "context" preset
// is selected (these give the map its bones — basemap context, parcel outline).
const PROPERTY_KEEP_ON = new Set(['parcel']);

// Layers that are "housekeeping" and should NEVER be turned off by the
// "none" preset (the parcel is the center of the map; without it the
// viewer becomes meaningless).
function applyPreset(name) {
  const cbAll = Array.from(document.querySelectorAll('input[type=checkbox][data-layer]'));
  // Compute target state per layer
  let toCheck, toUncheck;
  if (name === 'all') {
    toCheck = cbAll.map(cb => cb);
    toUncheck = [];
  } else if (name === 'none') {
    toCheck = [];
    toUncheck = cbAll.filter(cb => !PROPERTY_KEEP_ON.has(cb.dataset.layer));
  } else {
    const groups = PRESET_GROUPS[name] || [];
    toCheck = cbAll.filter(cb => {
      const g = (cb.closest('.layer-row')?.dataset.presetGroup || '').split(',');
      return g.some(x => groups.includes(x));
    });
    toUncheck = cbAll.filter(cb => {
      if (PROPERTY_KEEP_ON.has(cb.dataset.layer)) return false;
      const g = (cb.closest('.layer-row')?.dataset.presetGroup || '').split(',');
      return !g.some(x => groups.includes(x));
    });
  }
  // Apply
  toCheck.forEach(cb => { if (!cb.checked) { cb.checked = true; cb.dispatchEvent(new Event('change')); } });
  toUncheck.forEach(cb => { if (cb.checked) { cb.checked = false; cb.dispatchEvent(new Event('change')); } });
  // Update button highlight
  document.querySelectorAll('.preset-btn[data-preset]').forEach(b => {
    b.classList.toggle('active', b.dataset.preset === name);
  });
}
document.querySelectorAll('.preset-btn[data-preset]').forEach(btn => {
  btn.onclick = () => applyPreset(btn.dataset.preset);
});
// Default highlight = "Property" (what loads by default has parcel on).
applyPreset('property');

// ════════════════════════════════════════════════════════════════
// SIDEBAR COLLAPSE — desktop rail mode (saves 296 px for the map)
// ════════════════════════════════════════════════════════════════
const _sb = document.getElementById('sidebar');
const _layout = document.querySelector('.layout');
const _collapseBtn = document.getElementById('sidebar-collapse');
function setSidebarCollapsed(collapsed) {
  _sb.classList.toggle('collapsed', collapsed);
  if (_layout) _layout.style.gridTemplateColumns = collapsed ? '44px 1fr' : '';
  if (_collapseBtn) _collapseBtn.textContent = collapsed ? '›' : '‹';
  if (_collapseBtn) _collapseBtn.title = collapsed ? 'Expand sidebar' : 'Collapse sidebar';
  try { localStorage.setItem('lqv-sidebar-collapsed', collapsed ? '1' : '0'); } catch (e) {}
  // Invalidate Leaflet size so tiles re-flow into the new map width
  setTimeout(() => map.invalidateSize(), 240);
}
if (_collapseBtn) _collapseBtn.onclick = () => setSidebarCollapsed(!_sb.classList.contains('collapsed'));
// Restore collapsed state
try {
  if (localStorage.getItem('lqv-sidebar-collapsed') === '1') setSidebarCollapsed(true);
} catch (e) {}

// Keyboard shortcut: `[` toggles collapse, `F` toggles fullscreen.
// Escape exits fullscreen automatically (browser native).
window.addEventListener('keydown', (e) => {
  // Don't trigger when user is typing in an input/textarea
  const tag = (e.target.tagName || '').toLowerCase();
  if (tag === 'input' || tag === 'textarea' || e.target.isContentEditable) return;
  if (e.key === '[') {
    e.preventDefault();
    setSidebarCollapsed(!_sb.classList.contains('collapsed'));
  } else if (e.key === 'f' || e.key === 'F') {
    e.preventDefault();
    toggleFullscreen();
  }
});

// ════════════════════════════════════════════════════════════════
// FULLSCREEN MODE — fills the viewport with just the map.
// Uses the Fullscreen API when available, falls back to a CSS class
// overlay if the user denies or the API is missing.
// ════════════════════════════════════════════════════════════════
function enterFullscreen() {
  const el = document.documentElement;
  const go = (enabled) => {
    document.body.classList.toggle('fullscreen-mode', enabled);
    const btn = document.getElementById('fullscreen-btn');
    if (btn) {
      btn.textContent = enabled ? '⛶ Exit fullscreen' : '⛶ Fullscreen';
      btn.title = enabled ? 'Exit fullscreen (Esc or F)'
                          : 'Fullscreen (F)';
    }
    if (enabled) {
      // Floating hint
      const hint = document.createElement('div');
      hint.className = 'fs-hint';
      hint.textContent = 'Press F or Esc to exit fullscreen';
      document.body.appendChild(hint);
      setTimeout(() => hint.remove(), 2600);
    }
    // Leaflet needs to recompute container size
    setTimeout(() => { try { map.invalidateSize(); } catch (e) {} }, 200);
  };
  if (document.fullscreenEnabled && el.requestFullscreen) {
    el.requestFullscreen().then(() => go(true)).catch(() => {
      // User denied or browser blocked — fall back to CSS overlay
      go(true);
    });
  } else {
    go(true);
  }
}

function exitFullscreen() {
  const go = () => {
    document.body.classList.remove('fullscreen-mode');
    const btn = document.getElementById('fullscreen-btn');
    if (btn) {
      btn.textContent = '⛶ Fullscreen';
      btn.title = 'Fullscreen (F)';
    }
    setTimeout(() => { try { map.invalidateSize(); } catch (e) {} }, 200);
  };
  if (document.fullscreenElement && document.exitFullscreen) {
    document.exitFullscreen().then(go).catch(go);
  } else {
    go();
  }
}

function toggleFullscreen() {
  const isFs = document.body.classList.contains('fullscreen-mode')
               || document.fullscreenElement;
  if (isFs) exitFullscreen();
  else enterFullscreen();
}

// React to native fullscreen change (F11, Esc, browser controls)
document.addEventListener('fullscreenchange', () => {
  if (!document.fullscreenElement) {
    document.body.classList.remove('fullscreen-mode');
    const btn = document.getElementById('fullscreen-btn');
    if (btn) { btn.textContent = '⛶ Fullscreen'; btn.title = 'Fullscreen (F)'; }
    setTimeout(() => { try { map.invalidateSize(); } catch (e) {} }, 200);
  } else {
    document.body.classList.add('fullscreen-mode');
    setTimeout(() => { try { map.invalidateSize(); } catch (e) {} }, 200);
  }
});

// Wire up the button
const _fsBtn = document.getElementById('fullscreen-btn');
if (_fsBtn) _fsBtn.onclick = toggleFullscreen;

// P2-4: Share view button — copy current URL with state hash to clipboard.
document.getElementById('share-view').onclick = async () => {
  try {
    updateURLHash();
    const url = window.location.href;
    await navigator.clipboard.writeText(url);
    const btn = document.getElementById('share-view');
    const orig = btn.textContent;
    btn.textContent = '✓ Copied!';
    btn.style.background = 'var(--gold)';
    setTimeout(() => { btn.textContent = orig; btn.style.background = ''; }, 1500);
  } catch (e) {
    prompt('Copy this URL:', window.location.href);
  }
};

// P2-8: Annotations layer — user-drawn notes persisted to localStorage.
const ANNOT_KEY = 'lqv-annotations';
function loadAnnotations() {
  try { return JSON.parse(localStorage.getItem(ANNOT_KEY) || '[]'); } catch { return []; }
}
function saveAnnotations(arr) {
  try { localStorage.setItem(ANNOT_KEY, JSON.stringify(arr)); } catch {}
}
const annotLayer = L.layerGroup();
let annotMode = false;
function renderAnnotations() {
  annotLayer.clearLayers();
  const arr = loadAnnotations();
  arr.forEach((a, i) => {
    const m = L.marker([a.lat, a.lon], {
      icon: L.divIcon({
        className: 'annot-pin',
        html: `<div style="background:#fcd34d;border:2px solid #92400e;border-radius:50%;width:24px;height:24px;display:flex;align-items:center;justify-content:center;font-size:14px;color:#451a03;box-shadow:0 2px 4px rgba(0,0,0,0.3);">${i+1}</div>`,
        iconSize: [24, 24],
        iconAnchor: [12, 12],
      }),
    }).addTo(annotLayer);
    if (a.note) m.bindTooltip(`#${i+1} · ${a.note}`, { sticky: true });
    m.on('contextmenu', () => {
      if (confirm(`Delete annotation #${i+1} "${a.note}"?`)) {
        const all = loadAnnotations().filter((_, j) => j !== i);
        saveAnnotations(all);
        renderAnnotations();
      }
    });
  });
}
document.getElementById('annotate-btn').onclick = () => {
  annotMode = !annotMode;
  const btn = document.getElementById('annotate-btn');
  const hint = document.getElementById('annotate-hint');
  btn.style.background = annotMode ? 'var(--gold)' : '';
  btn.style.color = annotMode ? 'white' : '';
  hint.style.display = annotMode ? 'block' : 'none';
  if (annotMode && !map.hasLayer(annotLayer)) annotLayer.addTo(map);
  if (!annotMode && map.hasLayer(annotLayer)) map.removeLayer(annotLayer);
};
map.on('click', (e) => {
  if (!annotMode) return;
  const note = prompt('Note for this annotation (or leave empty):', '');
  if (note === null) return; // cancelled
  const arr = loadAnnotations();
  arr.push({
    lat: e.latlng.lat,
    lon: e.latlng.lng,
    note: note || '(no note)',
    created_at: new Date().toISOString(),
  });
  saveAnnotations(arr);
  renderAnnotations();
  if (!map.hasLayer(annotLayer)) annotLayer.addTo(map);
});

// ---- Shareable URL state (#z=12&l=roads,water,places) ----
function updateURLHash() {
  const z = map.getZoom();
  const c = map.getCenter();
  const on = [];
  document.querySelectorAll('[data-layer]:checked').forEach(cb => on.push(cb.dataset.layer));
  const hash = `#z=${z}&lat=${c.lat.toFixed(4)}&lon=${c.lng.toFixed(4)}&l=${on.join(',')}`;
  history.replaceState(null, '', hash);
}
map.on('moveend zoomend', updateURLHash);
const initialHash = window.location.hash.slice(1);
if (initialHash) {
  const params = new URLSearchParams(initialHash);
  const z = parseFloat(params.get('z') || '11');
  const lat = parseFloat(params.get('lat') || LAT);
  const lon = parseFloat(params.get('lon') || LON);
  if (z && Number.isFinite(z)) map.setView([lat, lon], z);
  if (params.get('l')) {
    // Defer layer toggles until boot() finishes — at script-load time
    // `layers[name]` doesn't exist yet, so handlers silently no-op.
    const wantedList = params.get('l').split(',');
    (function applyWhenReady() {
      // We need both the boot() promise (if it exists) and the layer
      // registry. The simplest signal: poll until all data layers exist.
      const desired = new Set(wantedList);
      let tries = 0;
      const tryApply = () => {
        tries += 1;
        let allReady = true;
        desired.forEach(name => {
          if (!layers[name]) allReady = false;
        });
        if (allReady || tries > 80) {           // 80 * 100 ms = 8 s cap
          desired.forEach(name => {
            const cb = document.querySelector(`[data-layer="${name}"]`);
            if (cb && cb.checked) {
              if (layers[name] && !map.hasLayer(layers[name])) {
                layers[name].addTo(map);
              }
            } else if (cb) {
              cb.checked = true;
              if (layers[name] && !map.hasLayer(layers[name])) {
                layers[name].addTo(map);
              }
            }
          });
          return;
        }
        setTimeout(tryApply, 100);
      };
      tryApply();
    })();
  }
}

})();
