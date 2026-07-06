// lqv-map.js — Index page 3D-map init stub.
//
// HISTORY
//   2026-06-30: original MapLibre GL JS viewer (12 layers, 3 basemaps).
//   2026-07-05: the index page stopped embedding the 2D viewer — the gold
//               "Open the full interactive map" CTA card points buyers at
//               the unified Leaflet-based /mapa viewer instead.
//   2026-07-06: the old MapLibre code was dead and the `import maplibregl`
//               statement at the top crashed the whole script (classic
//               scripts can't have `import`). Replaced with this init stub.
//
// INTENDED MOUNT
//   The index.html has an empty <div id="cesium-mount"> at line 494. If
//   the LQV_CESIUM_TOKEN env var is set at deploy time, data/DEPLOY.md
//   describes the recipe for generating ./lqv-secrets/cesium-token.js and
//   adding the Cesium CDN script. In that future state this stub would
//   grow to a proper Cesium init function.
//
// CURRENT BEHAVIOUR
//   WebGL probe + graceful no-op. If WebGL is unavailable (sandbox,
//   headless, very old browser), we set a clear status in the #cesium-mount
//   div so the user understands why the area is empty rather than thinking
//   the page is broken. If WebGL is available but there's no cesium-token
//   (the current state on Cloudflare Pages), we also show a clean status
//   pointing the user at /mapa.
//
// This file is intentionally tiny (< 1 KB) and dependency-free so a deploy
// can never break on a missing CDN or a CSP block.

(function () {
  'use strict';

  function probeWebGL() {
    try {
      const c = document.createElement('canvas');
      return !!(c.getContext('webgl2') || c.getContext('webgl'));
    } catch (_) {
      return false;
    }
  }

  function status(msg, kind) {
    const el = document.getElementById('cesium-mount');
    if (!el) return;
    const fg = kind === 'warn' ? '#d4a154' : '#7a766c';
    el.innerHTML = '' +
      '<div style="position:absolute;inset:0;display:flex;flex-direction:column;' +
      'align-items:center;justify-content:center;gap:0.6rem;padding:2rem;text-align:center;' +
      'background:#0a0e0f;color:' + fg + ';">' +
      '<div style="font-size:0.95rem;font-family:Inter,system-ui,sans-serif;">' +
        msg +
      '</div>' +
      '<a href="./mapa" style="color:#d4a154;text-decoration:none;border:1px solid #d4a154;' +
      'padding:0.5rem 1.2rem;border-radius:4px;font-size:0.85rem;">' +
        'Open the full interactive map →' +
      '</a>' +
      '</div>';
    el.style.position = 'relative';
  }

  if (!probeWebGL()) {
    status('3D map disabled — WebGL is not available in this browser.', 'warn');
    return;
  }

  // If LQV_CESIUM_TOKEN is ever added at deploy time, the cesium-token.js
  // script tag will be re-inserted and we'll have access to Cesium. Until
  // then, we show a clean status pointing the user at /mapa.
  if (typeof window.Cesium === 'undefined') {
    status('3D terrain viewer is offline — use the interactive map below for the same data with toggleable layers.', '');
    return;
  }
})();
