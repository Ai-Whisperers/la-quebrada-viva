// LQV viewer bundle (auto-extracted from escobar3d.html)
// Do not edit — edits go in escobar3d.html or this file directly


// === WebGL detection ===
function hasWebGL() {
  try {
    const c = document.createElement('canvas');
    return !!(window.WebGLRenderingContext && (c.getContext('webgl') || c.getContext('experimental-webgl')));
  } catch (e) { return false; }
}
if (!hasWebGL()) {
  document.body.innerHTML = '<div class="no-webgl"><div><h1>La Quebrada Viva — 3D Map</h1><p>This browser does not support WebGL.<br><br>The 3D terrain viewer needs WebGL to render. Try a desktop browser with WebGL enabled (Chrome, Firefox, Edge, Safari 15+).<br><br>Asset pipeline verified — see <a href="https://github.com/Ai-Whisperers/la-quebrada-viva/tree/master/docs/game_assets" style="color:#c2a878">the repo</a>.</p></div></div>';
  throw new Error('No WebGL');
}

Cesium.Ion.defaultAccessToken = '';

// === LOD configuration ===
// 5-tier LOD: each level's imagery and resolution tuned to camera height
// (not distance to centroid — see lodFromHeight).
const LODS = [
  {
    // LOD3: at-surface. Heightmap is LOD0 (1.5m/pix). Imagery is the
    // new Esri z18 (0.6 m/pixel) PLUS a dense 500x hillshade overlay with
    // contour lines baked in — this is what makes the relief visible
    // when the camera is right next to the terrain.
    id: 3, name: 'Surface',
    desc: '0.5 m / pixel · 1.4 km × 1.4 km · 500× hillshade + contours',
    heightmapUrl: './game_assets_lite/assets/heightmaps/lod0_terrain.png',
    heightmapBounds: [-57.037494, -25.636757, -57.022506, -25.623243],
    heightmapSize: [1024, 1024], heightmapRange: [124.9, 182.3],
    imageryUrl: './game_assets_lite/assets/textures/lqv_esri_z18_lod3.png',
    imageryBounds: [-57.035522, -25.635336, -57.023163, -25.624192],
    imagerySize: [2304, 2304],
    hillshadeUrl: './game_assets_lite/assets/heightmaps/lqv_hillshade_dense.png',
    hillshadeBounds: [-57.035828, -25.635000, -57.024172, -25.625000],
    exaggeration: 320, viewRadius: 280, maxCameraAlt: 350,
  },
  {
    id: 0, name: 'Parcel',
    desc: '1.5 m / pixel · 1.5 km × 1.5 km',
    heightmapUrl: './game_assets_lite/assets/heightmaps/lod0_terrain.png',
    heightmapBounds: [-57.037494, -25.636757, -57.022506, -25.623243],
    heightmapSize: [1024, 1024], heightmapRange: [124.9, 182.3],
    imageryUrl: './game_assets_lite/assets/textures/lqv_esri_z17_2km.png',
    imageryBounds: [-57.041, -25.642, -57.019, -25.618],
    imagerySize: [1792, 1792],
    exaggeration: 160, viewRadius: 1500, maxCameraAlt: 1500,
  },
  {
    id: 1, name: 'Escobar',
    desc: '15 m / pixel · 7.7 km × 7.7 km',
    heightmapUrl: './game_assets_lite/assets/heightmaps/lod1_terrain.png',
    heightmapBounds: [-57.068470, -25.664685, -56.991530, -25.595315],
    heightmapSize: [512, 512], heightmapRange: [100.9, 436.3],
    imageryUrl: './game_assets_lite/assets/textures/lods/lod1_imagery.jpg',
    imageryBounds: [-57.0685, -25.6647, -56.9915, -25.5953],
    imagerySize: [1024, 1024],
    exaggeration: 30, viewRadius: 5000, maxCameraAlt: 6000,
  },
  {
    id: 2, name: 'Regional',
    desc: '60 m / pixel · 23 km × 23 km',
    heightmapUrl: './game_assets_lite/assets/heightmaps/lod2_terrain.png',
    heightmapBounds: [-57.144910, -25.733604, -56.915090, -25.526396],
    heightmapSize: [384, 384], heightmapRange: [88.0, 492.4],
    imageryUrl: './game_assets_lite/assets/textures/lods/lod2_imagery.jpg',
    imageryBounds: [-57.1449, -25.7336, -56.9151, -25.5263],
    imagerySize: [512, 512],
    exaggeration: 10, viewRadius: 30000, maxCameraAlt: 30000,
  },
];

// === Camera presets ===
const PRESETS = {
  'parcel-oblique':  { lon: -57.026, lat: -25.622, alt: 350,  heading: -25, pitch: -22 },
  'parcel-top':      { lon: -57.030, lat: -25.625, alt: 1200, heading: 0,   pitch: -89 },
  'south-cliff':     { lon: -57.040, lat: -25.640, alt: 600,  heading: 30,  pitch: -18 },
  'quebrada':        { lon: -57.027, lat: -25.625, alt: 200,  heading: 90,  pitch: -8 },
  'waterfall':       { lon: -57.020, lat: -25.625, alt: 800,  heading: -110, pitch: -25 },
  'regional':        { lon: -57.080, lat: -25.685, alt: 8000, heading: 30,  pitch: -45 },
};

// === Cesium viewer ===
const viewer = new Cesium.Viewer('cesiumContainer', {
  baseLayerPicker: false,
  geocoder: false,
  homeButton: false,
  sceneModePicker: true,
  navigationHelpButton: false,
  animation: false,
  timeline: false,
  fullscreenButton: true,
  infoBox: false,
  selectionIndicator: false,
  terrainProvider: new Cesium.EllipsoidTerrainProvider(),
});
viewer.scene.skyAtmosphere.show = true;
viewer.scene.globe.enableLighting = false;
viewer.scene.globe.depthTestAgainstTerrain = true;
viewer.scene.fog.enabled = false;
viewer._cesiumWidget._creditContainer.style.display = 'none';

// === Enable unlimited zoom/drag/tilt/look via ScreenSpaceCameraController ===
// Cesium's default ScreenSpaceCameraController already supports all these,
// but we want to make sure minimumZoomDistance and maximumZoomDistance
// don't restrict the user when they zoom in close.
const cam_ctrl = viewer.scene.screenSpaceCameraController;
cam_ctrl.minimumZoomDistance = 10;     // 10m minimum — user can put face in the dirt
cam_ctrl.maximumZoomDistance = 80000;  // 80km — orbital altitudes
cam_ctrl.enableRotate = true;
cam_ctrl.enableTranslate = true;
cam_ctrl.enableZoom = true;
cam_ctrl.enableTilt = true;
cam_ctrl.enableLook = true;
// Disable "collisions" so the camera passes through the terrain instead
// of getting stuck on a hilltop when going below 30m
viewer.scene.screenSpaceCameraController.enableCollisionDetection = false;
viewer.scene.screenSpaceCameraController.inertiaSpin = 0.92;
viewer.scene.screenSpaceCameraController.inertiaTranslate = 0.92;
viewer.scene.screenSpaceCameraController.inertiaZoom = 0.92;

// === LOD state ===
let activeLodId = -1;
let activeLayers = {};
const lodNameEl = document.getElementById('lodName');
const lodMetaEl = document.getElementById('lodMeta');
const lodCameraEl = document.getElementById('lodCamera');

function showLoading(show) {
  document.getElementById('loading').classList.toggle('show', show);
}

// === Pre-decode heightmap PNG → Float32Array (one per LOD) ===
// CustomHeightmapTerrainProvider needs raw elevation data via callback,
// not a URL. We decode the 16-bit grayscale PNG to a Float32Array once
// per LOD, then the callback samples from it.
const heightmapDataCache = {}; // lodId → Float32Array(w*h)

async function preloadHeightmap(lodId) {
  if (heightmapDataCache[lodId]) return heightmapDataCache[lodId];
  const lod = LODS[lodId];
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.crossOrigin = 'anonymous';
    img.onload = () => {
      const c = document.createElement('canvas');
      c.width = img.width; c.height = img.height;
      const ctx = c.getContext('2d');
      ctx.drawImage(img, 0, 0);
      const data = ctx.getImageData(0, 0, img.width, img.height).data;
      const elev = new Float32Array(img.width * img.height);
      const [emin, emax] = lod.heightmapRange;
      for (let i = 0; i < img.width * img.height; i++) {
        // Browser canvas decodes I;16 PNG → RGBA by dividing the uint16 by 256
        // and writing the same value to R, G, B (low byte lost). So:
        //   real_uint16 ≈ R * 256   (8-bit resolution, but still useful)
        const r1 = data[i * 4];
        elev[i] = emin + (r1 / 255) * (emax - emin);
      }
      heightmapDataCache[lodId] = {
        elev, width: img.width, height: img.height,
        bounds: lod.heightmapBounds,
        lod,
      };
      console.log(`[heightmap] decoded LOD${lodId} (${img.width}x${img.height})`);
      resolve(heightmapDataCache[lodId]);
    };
    img.onerror = e => reject(new Error(`Failed to load ${lod.heightmapUrl}: ${e}`));
    img.src = lod.heightmapUrl;
  });
}

function applyLod(lodId) {
  if (lodId === activeLodId) return;
  const lod = LODS[lodId];
  console.log(`[LOD] Switching to LOD${lod.id} (${lod.name})`);
  showLoading(true);

  // Use CustomHeightmapTerrainProvider (available in Cesium 1.122+).
  // Callback returns Float32Array(w*h) of elevation values for the tile (x, y, level).
  // We pre-decoded the full heightmap; callback samples from it.
  const provider = new Cesium.CustomHeightmapTerrainProvider({
    width: lod.heightmapSize[0],
    height: lod.heightmapSize[1],
    credit: new Cesium.Credit(`LQV heightmap LOD${lod.id} (ALOS + AWS terrain-rgb)`),
    tilingScheme: new Cesium.GeographicTilingScheme(),
    callback: (x, y, level) => {
      // For our 3 LODs, the entire AOI fits in a single tile at level 0.
      // Return the full heightmap; for higher levels we upsample via bilinear.
      const data = heightmapDataCache[lodId];
      if (!data) return new Float32Array(lod.heightmapSize[0] * lod.heightmapSize[1]);
      if (level === 0 && x === 0 && y === 0) {
        // Return raw data
        return data.elev;
      }
      // For higher detail levels, bilinear upsample
      const w = lod.heightmapSize[0], h = lod.heightmapSize[1];
      const scale = Math.pow(2, level);
      const out = new Float32Array(w * h);
      for (let py = 0; py < h; py++) {
        for (let px = 0; px < w; px++) {
          // Map output (px, py) → source via simple nearest-neighbor with scale
          const sx = Math.min(w - 1, Math.floor(px / scale));
          const sy = Math.min(h - 1, Math.floor(py / scale));
          out[py * w + px] = data.elev[sy * w + sx];
        }
      }
      return out;
    },
  });
  viewer.terrainProvider = provider;

  viewer.imageryLayers.removeAll();
  const imageryProvider = new Cesium.SingleTileImageryProvider({
    url: lod.imageryUrl,
    rectangle: Cesium.Rectangle.fromDegrees(...lod.imageryBounds),
    tileWidth: lod.imagerySize[0], tileHeight: lod.imagerySize[1],
    credit: new Cesium.Credit(`Esri World Imagery (z=${lod.id === 3 ? 18 : lod.id === 0 ? 17 : lod.id === 1 ? 15 : 11}) © Esri, Maxar, Earthstar Geographics`),
  });
  const baseLayer = viewer.imageryLayers.addImageryProvider(imageryProvider);

  // Auto-mount the dense hillshade overlay (only LOD3 has it).
  // This is what makes relief visible at close zoom — elevation
  // differences of 5m amplified 500x through multi-azimuth hillshade.
  if (lod.hillshadeUrl) {
    const hillshadeProvider = new Cesium.SingleTileImageryProvider({
      url: lod.hillshadeUrl,
      rectangle: Cesium.Rectangle.fromDegrees(...lod.hillshadeBounds),
      tileWidth: 2048, tileHeight: 2048,
      credit: new Cesium.Credit('LQV dense hillshade (ALOS v.exag 500× + 5m contours)'),
    });
    const hillshadeLayer = viewer.imageryLayers.addImageryProvider(hillshadeProvider);
    hillshadeLayer.alpha = 0.55;
  }

  viewer.scene.verticalExaggeration = lod.exaggeration;

  lodNameEl.textContent = `LOD ${lod.id} · ${lod.name}`;
  lodMetaEl.textContent = lod.desc;
  updateCameraReadout();

  activeLodId = lodId;
  updateOverlayVisibilityByLod();
  // Hide loading after tiles render
  setTimeout(() => showLoading(false), 800);
}

// Pre-load all 3 LOD heightmaps at startup (parallel)
async function preloadAllHeightmaps() {
  console.log('[heightmap] pre-loading all LODs in parallel...');
  await Promise.all([0, 1, 2].map(id => preloadHeightmap(id).catch(e => console.warn(`LOD${id} preload failed:`, e))));
  console.log('[heightmap] all LODs ready');
}

function updateCameraReadout() {
  const cam = viewer.camera.positionCartographic;
  const lon = Cesium.Math.toDegrees(cam.longitude).toFixed(4);
  const lat = Cesium.Math.toDegrees(cam.latitude).toFixed(4);
  const alt = cam.height.toFixed(0);
  lodCameraEl.textContent = `${lat}, ${lon} · ${alt}m`;
}

function cameraDistanceToCentroidM() {
  const cam = viewer.camera.positionCartographic;
  const centroid = Cesium.Cartographic.fromDegrees(-57.030, -25.630);
  const geodesic = new Cesium.EllipsoidGeodesic(cam, centroid);
  return geodesic.surfaceDistance;
}

// LOD selection by camera HEIGHT (not distance to centroid — that's the bug
// that caused the terrain to disappear when zooming in past the parcel).
//
//   camera height < 350m   → LOD3 Surface   (1.5m, 280m AOI, exaggeration 220)
//   350–1500m             → LOD0 Parcel    (1.5m, 1.5km AOI, exaggeration 130)
//   1500–6000m            → LOD1 Escobar   (15m, 7.7km AOI, exaggeration 30)
//   > 6000m               → LOD2 Regional  (60m, 23km AOI, exaggeration 10)
const LOD_BY_HEIGHT = [
  { maxHeight: 350,  lodId: 3 },
  { maxHeight: 1500, lodId: 0 },
  { maxHeight: 6000, lodId: 1 },
  { maxHeight: Infinity, lodId: 2 },
];
function lodFromHeight(heightM) {
  for (const tier of LOD_BY_HEIGHT) if (heightM < tier.maxHeight) return tier.lodId;
  return 2;
}

let lastLodUpdate = 0;
function updateLodIfNeeded() {
  const now = performance.now();
  if (now - lastLodUpdate < 250) return;
  lastLodUpdate = now;
  updateCameraReadout();
  const cam = viewer.camera.positionCartographic;
  const heightM = cam.height;
  const desired = lodFromHeight(heightM);
  if (desired !== activeLodId) applyLod(desired);

  // Also auto-scale exaggeration within a LOD tier as we get closer —
  // extreme close-up gets absurd vertical exaggeration for visible relief.
  if (activeLodId === 3) {
    // 220 at LOD3 max-camera alt (350m), ramps up to 380 at 80m, capped
    // at 450 at 30m surface altitude — makes relief obvious at any zoom
    const t = Math.max(0, Math.min(1, (heightM - 30) / 320));
    const targetExag = 450 - t * 230;  // 450 surface → 220 at LOD3 ceiling
    viewer.scene.verticalExaggeration = targetExag;
    // Hide LOD3 hillshade overlay if camera is far enough that user
    // is looking at the broader parcel (not at surface detail)
    if (heightM > 280) {
      // optional future: toggle hillshade layer
    }
  }
}

viewer.scene.postRender.addEventListener(updateLodIfNeeded);

// === Overlay management ===
function updateOverlayVisibilityByLod() {
  const showDetailed = (activeLodId === 0 || activeLodId === 1);
  const cb = name => document.querySelector(`[data-layer=${name}]`);
  if (activeLayers.roads) activeLayers.roads.show = showDetailed && cb('roads').checked;
  if (activeLayers.waterways) activeLayers.waterways.show = showDetailed && cb('waterways').checked;
  if (activeLayers.hillshade) activeLayers.hillshade.show = cb('hillshade').checked && activeLodId <= 1;
  if (activeLayers.contours) activeLayers.contours.show = cb('contours').checked && activeLodId === 0;
}

// === Topography overlays ===
async function loadOverlays() {
  const BASE = './game_assets_lite/assets/geodata';

  Cesium.GeoJsonDataSource.load(`${BASE}/lqv_property_polygon.geojson`, {
    stroke: Cesium.Color.fromCssColorString('#c2a878'),
    fill: Cesium.Color.fromCssColorString('#c2a878').withAlpha(0.4),
    strokeWidth: 3,
  }).then(ds => { viewer.dataSources.add(ds); activeLayers.parcel = ds; }).catch(e => console.warn('parcel:', e));

  Cesium.GeoJsonDataSource.load(`${BASE}/lqv_aoi_bbox.geojson`, {
    stroke: Cesium.Color.fromCssColorString('#7d6a4a'),
    fill: Cesium.Color.TRANSPARENT, strokeWidth: 1,
  }).then(ds => { viewer.dataSources.add(ds); activeLayers.aoi = ds; }).catch(e => console.warn('aoi:', e));

  Cesium.GeoJsonDataSource.load(`${BASE}/lqv_buildability_zones.geojson`, {
    stroke: Cesium.Color.fromCssColorString('#4a90e2'),
    fill: Cesium.Color.fromCssColorString('#4a90e2').withAlpha(0.35),
    strokeWidth: 1,
  }).then(ds => { viewer.dataSources.add(ds); activeLayers.buildability = ds; }).catch(e => console.warn('buildability:', e));

  Cesium.GeoJsonDataSource.load(`${BASE}/lqv_quebrada_polygon.geojson`, {
    stroke: Cesium.Color.fromCssColorString('#5fa8d3'),
    fill: Cesium.Color.fromCssColorString('#5fa8d3').withAlpha(0.55),
    strokeWidth: 1,
  }).then(ds => { viewer.dataSources.add(ds); activeLayers.quebrada = ds; }).catch(e => console.warn('quebrada:', e));

  Cesium.GeoJsonDataSource.load(`${BASE}/lqv_solar_pv_zones.geojson`, {
    stroke: Cesium.Color.fromCssColorString('#d4a52a'),
    fill: Cesium.Color.fromCssColorString('#d4a52a').withAlpha(0.45),
    strokeWidth: 1,
  }).then(ds => { viewer.dataSources.add(ds); activeLayers.solar = ds; }).catch(e => console.warn('solar:', e));

  fetch(`${BASE}/lqv_waterfall_candidates.geojson`).then(r => r.json()).then(gj => {
    gj.features.forEach((f, i) => {
      const [lon, lat] = f.geometry.coordinates;
      const drop = f.properties.drop_m || 0;
      viewer.entities.add({
        position: Cesium.Cartesian3.fromDegrees(lon, lat),
        point: { pixelSize: 12, color: Cesium.Color.fromCssColorString('#5fa8d3'), outlineColor: Cesium.Color.WHITE, outlineWidth: 2 },
        label: {
          text: `Waterfall ${i + 1} (${drop}m)`,
          font: '10px monospace', fillColor: Cesium.Color.WHITE,
          style: Cesium.LabelStyle.FILL_AND_OUTLINE,
          outlineColor: Cesium.Color.BLACK, outlineWidth: 2,
          pixelOffset: new Cesium.Cartesian2(0, -18),
          distanceDisplayCondition: new Cesium.DistanceDisplayCondition(0, 5000),
        }
      });
    });
  }).catch(e => console.warn('waterfall:', e));

  Cesium.GeoJsonDataSource.load(`${BASE}/lqv_osm_roads.geojson`, {
    stroke: Cesium.Color.fromCssColorString('#ffffff').withAlpha(0.7),
    fill: Cesium.Color.TRANSPARENT, strokeWidth: 1.5, clampToGround: true,
  }).then(ds => { viewer.dataSources.add(ds); activeLayers.roads = ds; ds.show = false; })
    .catch(e => console.warn('roads:', e));

  Cesium.GeoJsonDataSource.load(`${BASE}/lqv_osm_waterways.geojson`, {
    stroke: Cesium.Color.fromCssColorString('#3d7da3'),
    fill: Cesium.Color.fromCssColorString('#3d7da3').withAlpha(0.5),
    strokeWidth: 2,
  }).then(ds => { viewer.dataSources.add(ds); activeLayers.waterways = ds; ds.show = false; })
    .catch(e => console.warn('waterways:', e));

  // Compute hillshade from LOD0 heightmap (client-side)
  computeHillshade();
  // Compute contours from LOD0 heightmap (client-side)
  computeContours();
}

// === Hillshade overlay (computed client-side from LOD0 heightmap) ===
async function computeHillshade() {
  try {
    const url = LODS[0].heightmapUrl;
    const r = await fetch(url);
    const buf = await r.arrayBuffer();
    const blob = new Blob([buf]);
    const imgUrl = URL.createObjectURL(blob);
    const img = new Image();
    img.onload = () => {
      // Decode 16-bit grayscale PNG via canvas
      const c = document.createElement('canvas');
      c.width = img.width; c.height = img.height;
      const ctx = c.getContext('2d');
      ctx.drawImage(img, 0, 0);
      const data = ctx.getImageData(0, 0, img.width, img.height).data;
      const w = img.width, h = img.height;
      const elev = new Float32Array(w * h);
      for (let i = 0; i < w * h; i++) {
        // Browser canvas decodes I;16 → RGBA by /256, R=G=B=high byte
        const r1 = data[i * 4];
        elev[i] = r1 / 255;  // 0..1 normalised
      }
      // Normalise to metres
      const [emin, emax] = LODS[0].heightmapRange;
      const norm = emax - emin;
      for (let i = 0; i < elev.length; i++) {
        elev[i] = emin + elev[i] * norm;
      }
      // Compute hillshade: Horn's method, single sun azimuth 315° NW, alt 45°
      const sunAz = Math.PI * 5 / 4; // 315°
      const sunAlt = Math.PI / 4;    // 45°
      const dx = new Float32Array(w * h);
      const dy = new Float32Array(w * h);
      const pxRes = 1.5; // m/pixel for LOD0
      // Simple gradient: Sobel
      for (let y = 1; y < h - 1; y++) {
        for (let x = 1; x < w - 1; x++) {
          const i = y * w + x;
          const tl = elev[(y - 1) * w + (x - 1)];
          const t  = elev[(y - 1) * w + x];
          const tr = elev[(y - 1) * w + (x + 1)];
          const l  = elev[y * w + (x - 1)];
          const r  = elev[y * w + (x + 1)];
          const bl = elev[(y + 1) * w + (x - 1)];
          const b  = elev[(y + 1) * w + x];
          const br = elev[(y + 1) * w + (x + 1)];
          dx[i] = ((tr + 2 * r + br) - (tl + 2 * l + bl)) / (8 * pxRes);
          dy[i] = ((bl + 2 * b + br) - (tl + 2 * t + tr)) / (8 * pxRes);
        }
      }
      // Render hillshade as RGBA canvas
      const shade = new Float32Array(w * h);
      for (let i = 0; i < w * h; i++) {
        const slope = Math.atan(Math.sqrt(dx[i] * dx[i] + dy[i] * dy[i]));
        const aspect = Math.atan2(-dx[i], dy[i]);
        const hs = Math.cos(sunAlt) * Math.cos(slope) + Math.sin(sunAlt) * Math.sin(slope) * Math.cos(sunAz - aspect);
        shade[i] = Math.max(0, Math.min(1, hs));
      }
      // Write hillshade canvas
      const c2 = document.createElement('canvas');
      c2.width = w; c2.height = h;
      const ctx2 = c2.getContext('2d');
      const imgData = ctx2.createImageData(w, h);
      for (let i = 0; i < w * h; i++) {
        const v = Math.floor(shade[i] * 255);
        imgData.data[i * 4] = v;
        imgData.data[i * 4 + 1] = v;
        imgData.data[i * 4 + 2] = v;
        imgData.data[i * 4 + 3] = 200;
      }
      ctx2.putImageData(imgData, 0, 0);
      URL.revokeObjectURL(imgUrl);
      // Add as imagery layer
      const hillshadeUrl = c2.toDataURL('image/png');
      const provider = new Cesium.SingleTileImageryProvider({
        url: hillshadeUrl,
        rectangle: Cesium.Rectangle.fromDegrees(...LODS[0].heightmapBounds),
        tileWidth: w, tileHeight: h,
        credit: new Cesium.Credit('Hillshade (Horn 315° NW, 45° alt) computed client-side from LOD0 heightmap'),
      });
      const layer = viewer.imageryLayers.addImageryProvider(provider);
      layer.alpha = 0.5;
      layer.show = false;
      activeLayers.hillshade = layer;
      console.log(`[hillshade] computed ${w}x${h} client-side`);
    };
    img.src = imgUrl;
  } catch (e) {
    console.warn('hillshade failed:', e);
  }
}

// === Contour lines (10 m interval, only at LOD0) ===
async function computeContours() {
  try {
    const url = LODS[0].heightmapUrl;
    const r = await fetch(url);
    const buf = await r.arrayBuffer();
    const blob = new Blob([buf]);
    const imgUrl = URL.createObjectURL(blob);
    const img = new Image();
    img.onload = () => {
      const c = document.createElement('canvas');
      c.width = img.width; c.height = img.height;
      const ctx = c.getContext('2d');
      ctx.drawImage(img, 0, 0);
      const data = ctx.getImageData(0, 0, img.width, img.height).data;
      const w = img.width, h = img.height;
      const elev = new Float32Array(w * h);
      for (let i = 0; i < w * h; i++) {
        const r1 = data[i * 4];
        elev[i] = r1 / 255;  // 0..1
      }
      const [emin, emax] = LODS[0].heightmapRange;
      const norm = emax - emin;
      for (let i = 0; i < elev.length; i++) {
        elev[i] = emin + elev[i] * norm;
      }
      // Build a GeoJSON grid feature collection (turf will compute isolines)
      // Reduce resolution for turf performance (use 256x256)
      const step = Math.max(1, Math.floor(w / 256));
      const gw = Math.floor(w / step), gh = Math.floor(h / step);
      const [west, south, east, north] = LODS[0].heightmapBounds;
      const lonRes = (east - west) / (gw - 1);
      const latRes = (north - south) / (gh - 1);
      const points = [];
      for (let y = 0; y < gh; y++) {
        for (let x = 0; x < gw; x++) {
          const lon = west + x * lonRes;
          const lat = north - y * latRes;
          const e = elev[y * step * w + x * step];
          points.push(turf.point([lon, lat], { elev: e }));
        }
      }
      const fc = turf.featureCollection(points);
      const interval = 10; // metres
      const minElev = Math.floor(emin / interval) * interval;
      const maxElev = Math.ceil(emax / interval) * interval;
      const contours = [];
      for (let v = minElev; v <= maxElev; v += interval) {
        try {
          const isolines = turf.isolines(fc, v, { zProperty: 'elev', breaks: 1 });
          isolines.features.forEach(f => contours.push(f));
        } catch (e) {
          // skip if no isoline at this level
        }
      }
      // Render as entity polylines
      const contourCollection = {
        type: 'FeatureCollection',
        features: contours.map(f => ({
          type: 'Feature',
          properties: { elev: f.properties.elev || f.properties.value },
          geometry: f.geometry,
        })),
      };
      Cesium.GeoJsonDataSource.load(contourCollection, {
        stroke: Cesium.Color.fromCssColorString('#c2a878'),
        fill: Cesium.Color.TRANSPARENT,
        strokeWidth: 1,
        clampToGround: true,
      }).then(ds => {
        viewer.dataSources.add(ds);
        activeLayers.contours = ds;
        ds.show = false;
        console.log(`[contours] ${contours.length} isolines at ${interval}m interval`);
      });
    };
    img.src = imgUrl;
  } catch (e) {
    console.warn('contours failed:', e);
  }
}

// === Layer toggle UI ===
document.querySelectorAll('.lqv-layers input[type=checkbox]').forEach(input => {
  input.addEventListener('change', () => {
    const layerName = input.dataset.layer;
    const ds = activeLayers[layerName];
    if (!ds) return;
    if (layerName === 'hillshade' || layerName === 'contours') {
      ds.show = input.checked && activeLodId <= 1;
    } else if (layerName === 'roads' || layerName === 'waterways') {
      ds.show = input.checked && (activeLodId === 0 || activeLodId === 1);
    } else {
      ds.show = input.checked;
    }
  });
});

// === Section "all" toggles ===
document.querySelectorAll('.lqv-layers .section-toggle').forEach(btn => {
  btn.addEventListener('click', () => {
    const section = btn.dataset.section;
    const sectionMap = {
      property: ['parcel', 'aoi'],
      topo: ['buildability', 'quebrada', 'solar', 'hillshade', 'contours'],
      features: ['waterfall', 'roads', 'waterways'],
    };
    const items = sectionMap[section];
    const allOn = items.every(name => {
      const cb = document.querySelector(`[data-layer=${name}]`);
      return cb && cb.checked;
    });
    items.forEach(name => {
      const cb = document.querySelector(`[data-layer=${name}]`);
      if (cb) {
        cb.checked = !allOn;
        cb.dispatchEvent(new Event('change'));
      }
    });
  });
});

// === Camera presets ===
function flyToPreset(name) {
  const p = PRESETS[name];
  if (!p) return;
  document.querySelectorAll('.lqv-presets button').forEach(b => b.classList.remove('active'));
  const btn = document.querySelector(`[data-preset="${name}"]`);
  if (btn) btn.classList.add('active');
  viewer.camera.flyTo({
    destination: Cesium.Cartesian3.fromDegrees(p.lon, p.lat, p.alt),
    orientation: { heading: Cesium.Math.toRadians(p.heading), pitch: Cesium.Math.toRadians(p.pitch), roll: 0 },
    duration: 1.5,
  });
  // Update URL with the new camera
  setTimeout(updateUrlWithCamera, 1600);
}
document.querySelectorAll('.lqv-presets button').forEach(btn => {
  btn.addEventListener('click', () => flyToPreset(btn.dataset.preset));
});

// === Help modal ===
const helpModal = document.getElementById('helpModal');
document.getElementById('toolHelp').addEventListener('click', () => helpModal.classList.toggle('hidden'));
document.getElementById('modalClose').addEventListener('click', () => helpModal.classList.add('hidden'));
// Show on first visit
if (!localStorage.getItem('lqv-help-shown')) {
  helpModal.classList.remove('hidden');
  localStorage.setItem('lqv-help-shown', '1');
}
// ESC to close help + cancel ruler
window.addEventListener('keydown', e => {
  if (e.key === 'Escape') {
    helpModal.classList.add('hidden');
    if (rulerActive) deactivateRuler();
  }
  if (e.key === '?' || e.key === '/') {
    helpModal.classList.toggle('hidden');
  }
});

// === Ruler tool ===
let rulerActive = false;
let rulerPoints = [];
let rulerEntities = [];
const rulerBtn = document.getElementById('toolRuler');
const rulerReadout = document.getElementById('rulerReadout');

function activateRuler() {
  rulerActive = true;
  rulerBtn.classList.add('active');
  viewer.screenSpaceEventHandler.setInputAction(handleRulerClick, Cesium.ScreenSpaceEventType.LEFT_CLICK);
  viewer.canvas.style.cursor = 'crosshair';
  rulerReadout.textContent = 'Click on terrain — point 1 of 2';
  rulerReadout.classList.add('show');
}
function deactivateRuler() {
  rulerActive = false;
  rulerBtn.classList.remove('active');
  viewer.screenSpaceEventHandler.removeInputAction(Cesium.ScreenSpaceEventType.LEFT_CLICK);
  viewer.canvas.style.cursor = '';
  rulerReadout.classList.remove('show');
  rulerEntities.forEach(e => viewer.entities.remove(e));
  rulerEntities = [];
  rulerPoints = [];
}
rulerBtn.addEventListener('click', () => {
  if (rulerActive) deactivateRuler(); else activateRuler();
});
function handleRulerClick(click) {
  const carto = viewer.scene.pickPosition(click.position);
  if (!carto) {
    // Try globe.pick
    const ray = viewer.camera.getPickRay(click.position);
    if (!ray) return;
    const pos = viewer.scene.globe.pick(ray, viewer.scene);
    if (!pos) return;
    addRulerPoint(pos);
  } else {
    addRulerPoint(carto);
  }
}
function addRulerPoint(cartesian) {
  // Drop a marker
  const entity = viewer.entities.add({
    position: cartesian,
    point: { pixelSize: 10, color: Cesium.Color.fromCssColorString('#c2a878'), outlineColor: Cesium.Color.WHITE, outlineWidth: 2 },
  });
  rulerEntities.push(entity);
  rulerPoints.push(cartesian);

  if (rulerPoints.length === 1) {
    rulerReadout.textContent = `Point 1 set · click for point 2 · distance = —`;
  } else if (rulerPoints.length === 2) {
    // Compute geodesic distance (ground-following) and 3D line-of-sight
    const c1 = Cesium.Cartographic.fromCartesian(rulerPoints[0]);
    const c2 = Cesium.Cartographic.fromCartesian(rulerPoints[1]);
    const geodesic = new Cesium.EllipsoidGeodesic(c1, c2);
    const dist = geodesic.surfaceDistance;
    const bearing = Cesium.Math.toDegrees(geodesic.startHeading);
    // 3D straight-line distance (line-of-sight) — uses raw cartesian
    const los3d = Cesium.Cartesian3.distance(rulerPoints[0], rulerPoints[1]);
    // Elevation gain
    const elev1 = c1.height, elev2 = c2.height;
    const elevGain = elev2 - elev1;
    // Slope angle (rise/run): atan(dz/dist) in degrees
    const slopeDeg = los3d > 0 ? Math.atan2(Math.abs(elevGain), dist) * 180 / Math.PI : 0;
    // Slope percent: rise/run × 100
    const slopePct = dist > 0 ? Math.abs(elevGain) / dist * 100 : 0;
    // Up/down indicator
    const arrow = elevGain >= 0 ? '↑' : '↓';
    // Draw a line
    const lineEntity = viewer.entities.add({
      polyline: {
        positions: rulerPoints,
        width: 2,
        material: Cesium.Color.fromCssColorString('#c2a878'),
        clampToGround: true,
      },
    });
    rulerEntities.push(lineEntity);
    rulerReadout.innerHTML = `<b>${dist.toFixed(1)} m</b> ground · ` +
      `<b>${los3d.toFixed(1)} m</b> line-of-sight · ` +
      `${arrow} <b>${Math.abs(elevGain).toFixed(1)} m</b> elevation · ` +
      `<b>${slopeDeg.toFixed(1)}°</b> (${slopePct.toFixed(1)}% slope) · ` +
      `bearing ${bearing.toFixed(0)}° · ESC to clear`;
    setTimeout(() => { if (rulerActive) deactivateRuler(); }, 100);
  }
}

// === Share via URL ===
const shareBtn = document.getElementById('toolShare');
shareBtn.addEventListener('click', () => {
  updateUrlWithCamera();
  const url = window.location.href;
  navigator.clipboard?.writeText(url).then(() => {
    const old = shareBtn.textContent;
    shareBtn.textContent = '✓ Copied';
    setTimeout(() => shareBtn.textContent = old, 1500);
  });
});

function updateUrlWithCamera() {
  const cam = viewer.camera.positionCartographic;
  const heading = viewer.camera.heading;
  const pitch = viewer.camera.pitch;
  const params = new URLSearchParams();
  params.set('lon', Cesium.Math.toDegrees(cam.longitude).toFixed(6));
  params.set('lat', Cesium.Math.toDegrees(cam.latitude).toFixed(6));
  params.set('alt', cam.height.toFixed(0));
  params.set('h', Cesium.Math.toDegrees(heading).toFixed(1));
  params.set('p', Cesium.Math.toDegrees(pitch).toFixed(1));
  const url = `${window.location.pathname}?${params.toString()}${window.location.hash}`;
  history.replaceState(null, '', url);
}

function restoreCameraFromUrl() {
  const params = new URLSearchParams(window.location.search);
  const lon = parseFloat(params.get('lon'));
  const lat = parseFloat(params.get('lat'));
  const alt = parseFloat(params.get('alt'));
  const h = parseFloat(params.get('h'));
  const p = parseFloat(params.get('p'));
  if (!isNaN(lon) && !isNaN(lat) && !isNaN(alt)) {
    // Clamp altitude so the user never lands underground
    const safeAlt = clampAltitudeToTerrain(lon, lat, alt);
    setTimeout(() => {
      viewer.camera.flyTo({
        destination: Cesium.Cartesian3.fromDegrees(lon, lat, safeAlt),
        orientation: { heading: Cesium.Math.toRadians(isNaN(h) ? 0 : h), pitch: Cesium.Math.toRadians(isNaN(p) ? -30 : p), roll: 0 },
        duration: 0,
      });
    }, 200);
    return true;
  }
  return false;
}

// Clamp a requested altitude: camera ends up at least MIN_CAMERA_ALT_M above
// the local terrain (and at most MAX_CAMERA_ALT_M). UNLIMITED ZOOM IN —
// drag/trackpad/mousewheel will work natively through Cesium's default
// ScreenSpaceCameraController after we lower the minimum below 30m.
const MIN_CAMERA_ALT_M = 30;     // 30m above ground — close enough to see texture detail
const MAX_CAMERA_ALT_M = 50000;  // 50km — let user see the full Chaco
function clampAltitudeToTerrain(lon, lat, requestedAltM) {
  const clampedTop = Math.min(requestedAltM, MAX_CAMERA_ALT_M);
  const sample = sampleElevationFromCache(lon, lat);
  const groundAlt = sample != null ? sample : 150;
  // Allow infinite zoom: between 30m above ground and 5km above ground
  return Math.max(MIN_CAMERA_ALT_M + groundAlt, Math.min(clampedTop, groundAlt + 5000));
}

// Sample LOD3 (or fallback LOD0) heightmap cache for an elevation at lon/lat
const _eleCache = {};
function sampleElevationFromCache(lon, lat) {
  // Try LOD3 first (high-detail cache) — but for now use LOD0 since it's
  // the same heightmap. We can later split into a dedicated near-surface
  // heightmap when LiDAR is available.
  const cacheKey = `0_${lon.toFixed(5)}_${lat.toFixed(5)}`;
  if (_eleCache[cacheKey]) return _eleCache[cacheKey];
  const data = heightmapDataCache[0];
  if (!data) return null;
  const [w, s, e, n] = data.bounds;
  if (lon < w || lon > e || lat < s || lat > n) return null;
  const px = ((lon - w) / (e - w)) * (data.width - 1);
  const py = ((n - lat) / (n - s)) * (data.height - 1);
  const ix = Math.floor(px), iy = Math.floor(py);
  // Bilinear sample
  const fx = px - ix, fy = py - iy;
  const v00 = data.elev[iy * data.width + ix];
  const v10 = data.elev[iy * data.width + Math.min(ix+1, data.width-1)];
  const v01 = data.elev[Math.min(iy+1, data.height-1) * data.width + ix];
  const v11 = data.elev[Math.min(iy+1, data.height-1) * data.width + Math.min(ix+1, data.width-1)];
  const v = (v00*(1-fx) + v10*fx)*(1-fy) + (v01*(1-fx) + v11*fx)*fy;
  _eleCache[cacheKey] = v;
  return v;
}

// === Overlay toggles (contours, hillshade, waterfalls) ===
const overlayLayers = {
  contours: null,
  hillshade: null,
  waterfalls: null,
};

async function toggleContours(btn) {
  if (overlayLayers.contours) {
    viewer.scene.primitives.remove(overlayLayers.contours);
    overlayLayers.contours = null;
    btn.classList.remove('active');
    return;
  }
  btn.classList.add('active');
  showLoading(true);
  try {
    // 5m contours — generated by Cesium + the contour generation code.
    // We can use the same algorithm (turf isolines) but a precomputed
    // 1.6MB file exists in data/dem_contours_parcel_5m.geojson.
    const url = 'https://lqv-walkthrough.pages.dev/data/dem_contours_parcel_5m.geojson';
    const r = await fetch(url);
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const geo = await r.json();
    // Split into major (every 25m) and minor contours
    const minor = [], major = [];
    for (const f of geo.features || []) {
      const e = f.properties?.elevation ?? f.properties?.ELEV ?? 0;
      const interval = e % 25 < 1 ? 25 : 5;
      f.properties.kind = interval;
      if (interval === 25) major.push(f); else minor.push(f);
    }
    // Load minor first (lighter, more numerous)
    overlayLayers.contours = new Cesium.GeoJsonDataSource.load(
      { type: 'FeatureCollection', features: [...minor, ...major] },
      {
        stroke: Cesium.Color.fromCssColorString('#7d6a4a'),
        strokeWidth: 1,
        fill: Cesium.Color.TRANSPARENT,
        clampToGround: true,
      }
    );
    const ds = await overlayLayers.contours;
    viewer.dataSources.add(ds);

    // Now style major contours (every 25m) thicker + add ELEVATION LABELS.
    // For each major contour LineString, pick the midpoint and draw a
    // Cesium.Label showing the elevation in metres. Only label every
    // other major contour to reduce clutter (50m intervals of labels).
    const entities = ds.entities.values;
    let labelCounter = 0;
    for (const ent of entities) {
      const elev = ent.properties?.elevation?.getValue?.() ??
                   ent.properties?.ELEV?.getValue?.();
      if (elev == null) continue;
      const kind = ent.properties?.kind?.getValue?.();
      if (kind !== 25) continue;
      // Style: thicker, brighter
      if (ent.polyline) {
        ent.polyline.width = 2;
        ent.polyline.material = Cesium.Color.fromCssColorString('#c2a878');
      }
      // Place a label at the geometric center of the polyline positions
      const positions = ent.polyline?.positions?.getValue?.(ds._time);
      if (!positions || positions.length < 2) continue;
      const mid = positions[Math.floor(positions.length / 2)];
      if (!mid) continue;
      // Only every other major contour (50m label spacing)
      labelCounter++;
      if (labelCounter % 2 !== 0) continue;
      viewer.entities.add({
        position: mid,
        label: {
          text: `${elev.toFixed(0)} m`,
          font: '11px "Courier New", monospace',
          fillColor: Cesium.Color.fromCssColorString('#c2a878'),
          outlineColor: Cesium.Color.fromCssColorString('#0c0f0a'),
          outlineWidth: 3,
          style: Cesium.LabelStyle.FILL_AND_OUTLINE,
          verticalOrigin: Cesium.VerticalOrigin.CENTER,
          horizontalOrigin: Cesium.HorizontalOrigin.CENTER,
          heightReference: Cesium.HeightReference.NONE,
          pixelOffset: new Cesium.Cartesian2(0, -2),
          scale: 0.9,
          showBackground: false,
          disableDepthTestDistance: Number.POSITIVE_INFINITY, // always visible
        },
      });
    }
  } catch (e) {
    console.warn('Contours load failed:', e);
    btn.classList.remove('active');
  }
  showLoading(false);
}

async function toggleHillshade(btn) {
  if (overlayLayers.hillshade) {
    viewer.imageryLayers.remove(overlayLayers.hillshade, true);
    overlayLayers.hillshade = null;
    btn.classList.remove('active');
    return;
  }
  btn.classList.add('active');
  // Hillshade as a translucent overlay (alpha 0.4) over the active imagery.
  const provider = new Cesium.SingleTileImageryProvider({
    url: 'https://lqv-walkthrough.pages.dev/data/hillshade_parcel.jpg',
    rectangle: Cesium.Rectangle.fromDegrees(-57.041, -25.642, -57.019, -25.618),
    credit: 'LQV hillshade (ALOS-derived)',
  });
  overlayLayers.hillshade = viewer.imageryLayers.addImageryProvider(provider);
  overlayLayers.hillshade.alpha = 0.45;
}

async function toggleWaterfalls(btn) {
  if (overlayLayers.waterfalls) {
    viewer.entities.removeAll();
    overlayLayers.waterfalls = null;
    btn.classList.remove('active');
    return;
  }
  btn.classList.add('active');
  try {
    const r = await fetch('https://lqv-walkthrough.pages.dev/data/water_features_final.geojson');
    if (!r.ok) throw new Error(`HTTP ${r.status}`);
    const geo = await r.json();
    // Re-collect only waterfall candidates (not streams)
    const features = (geo.features || []).filter(f =>
      f.properties?.kind === 'waterfall' ||
      f.properties?.type === 'waterfall' ||
      /waterfall|cascada/i.test(JSON.stringify(f.properties || {}))
    );
    overlayLayers.waterfalls = viewer.dataSources.add(
      await Cesium.GeoJsonDataSource.load(
        { type: 'FeatureCollection', features },
        {
          stroke: Cesium.Color.AQUA,
          strokeWidth: 3,
          fill: Cesium.Color.fromCssColorString('rgba(0, 255, 255, 0.4)'),
          clampToGround: true,
        }
      )
    );
  } catch (e) {
    console.warn('Waterfalls load failed:', e);
    btn.classList.remove('active');
  }
}

document.getElementById('toolContours').addEventListener('click', e => toggleContours(e.currentTarget));
document.getElementById('toolHillshade').addEventListener('click', e => toggleHillshade(e.currentTarget));
document.getElementById('toolWaterfalls').addEventListener('click', e => toggleWaterfalls(e.currentTarget));

// === Altitude input — keyboard field that flies the camera there ===
const altInput = document.getElementById('altInput');
altInput.addEventListener('change', () => {
  const requested = parseFloat(altInput.value);
  if (!isFinite(requested)) return;
  const cam = viewer.camera.positionCartographic;
  const lon = Cesium.Math.toDegrees(cam.longitude);
  const lat = Cesium.Math.toDegrees(cam.latitude);
  const safeAlt = clampAltitudeToTerrain(lon, lat, requested);
  altInput.value = Math.round(safeAlt);
  viewer.camera.flyTo({
    destination: Cesium.Cartesian3.fromDegrees(lon, lat, safeAlt),
    orientation: {
      heading: viewer.camera.heading,
      pitch: viewer.camera.pitch,
      roll: 0,
    },
    duration: 1.2,
  });
});

// Keep altitude input in sync with camera position
viewer.scene.postRender.addEventListener(() => {
  const cam = viewer.camera.positionCartographic;
  if (cam && document.activeElement !== altInput) {
    const alt = Math.round(cam.height);
    if (altInput.value !== String(alt)) altInput.value = alt;
  }
});

// === Export PNG ===
const exportBtn = document.getElementById('toolExport');
exportBtn.addEventListener('click', () => {
  // Force render at higher resolution briefly
  showLoading(true);
  setTimeout(() => {
    const canvas = viewer.scene.canvas;
    canvas.toBlob(blob => {
      if (!blob) { showLoading(false); return; }
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      const stamp = new Date().toISOString().replace(/[:.]/g, '-').slice(0, 19);
      a.href = url;
      a.download = `lqv-3d-${stamp}.png`;
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
      URL.revokeObjectURL(url);
      showLoading(false);
    }, 'image/png');
  }, 200);
});

// === Initial camera ===
const restored = restoreCameraFromUrl();
if (!restored) {
  viewer.camera.flyTo({
    destination: Cesium.Cartesian3.fromDegrees(-57.026, -25.622, 350),
    orientation: { heading: Cesium.Math.toRadians(-25), pitch: Cesium.Math.toRadians(-22), roll: 0 },
    duration: 0,
  });
}

// === Kick off ===
// Pre-load all 3 heightmaps in parallel, then apply LOD0 and start overlays
preloadAllHeightmaps().then(() => {
  applyLod(0);
  loadOverlays();
});
// Apply LOD0 immediately so the flat ellipsoid + imagery render while heightmap loads
applyLod(0);

// Update URL every 5 seconds while user navigates
setInterval(updateUrlWithCamera, 5000);

console.log('[LQV] Viewer v2 ready. Drag to rotate. Press ? for help.');
