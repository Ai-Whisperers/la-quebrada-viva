# MCP socket status — diagnostic + retire decision (CC-TOOL.1)

> **TL;DR:** the BlenderMCP socket on `localhost:9876` is intentionally **retired for the escritura phase** (through 2026-06-27 + immediate aftermath). The sub-render-first workflow does not depend on it. Revival recipe is in §3 — only execute if the work actually needs it.

Date of decision: 2026-06-26 (T-1).
Owner: AI (Nyx).
Related: `docs/MASTER_TODO.md` CC-TOOL.1, `docs/AUTONOMOUS_PLAN.md:28`, `docs/master_plan.md:45`, `docs/external_assets.md:7`, `docs/asset_plan.md:203`.

---

## 1 — Symptom

- `127.0.0.1:9876` → `Connection refused`.
- `lsof -i :9876` → empty.
- `ss -tlnp | grep 9876` → empty.
- The `uvx blender-mcp` processes that show up in `ps -ef | grep mcp` are the **stdio bridge** on the Claude Code side. They do not bind the port — they marshal stdio ↔ socket once the Blender-side server is up.
- `~/.config/blender/4.2/scripts/addons/blender_mcp.py` is present (ahujasid v1.2). The addon code is fine; nothing is binding it.

## 2 — Why it is dead

There is no long-running Blender instance with the BlenderMCP addon enabled. The sub-render workflow used by this project launches Blender per render (`/home/ai-whisperers/.local/bin/blender --background --python build_scene.py`) and exits — that lifecycle never registers a persistent socket.

`scripts/mcp_daemon.py` exists to run Blender headless with the addon enabled and block forever, which is the canonical revival path. It is **gitignored** (`.gitignore:45`) per the standing operational rule "never stage `scripts/mcp_daemon.py`".

## 3 — Revival recipe (only if needed)

If a future task genuinely needs `mcp__blender__*` tools (Sketchfab import, Hyper3D/Hunyuan3D generation, Poly Haven in-process download, live viewport screenshot):

```bash
# Terminal 1 — start the Blender-side server (blocks)
/home/ai-whisperers/.local/bin/blender --background --python scripts/mcp_daemon.py

# Terminal 2 — verify
timeout 2 bash -c '</dev/tcp/127.0.0.1/9876' && echo OK || echo DEAD
```

The Claude Code stdio bridge (`uvx blender-mcp`) is already running per the user's MCP config, so once the Blender server binds, the tools come back to life.

**Resource cost:** ~4.0–4.5 GB RSS for the daemon Blender + addon, on a 14 GB host that already serializes one sub-render at a time (~4.3 GB peak per render). Keeping the daemon up while rendering pushes the host close to OOM; see [[feedback_render_parallelism]] memory. So: bring it up only when interactive work is queued, tear it down before the next render batch.

## 4 — Why retire for escritura phase

1. **The deliverables do not need it.** All 18/18 final renders + the print pack at `dist/print_pack_2026-06-27/` were produced through the CLI sub-render path. The HDRI swap (P1.A.5, commit `5958124`) used `scripts/download_polyhaven_assets.py` (HTTPS, no MCP). The flora/material/sub-render pipeline does not touch MCP either.
2. **Resource budget says no.** 14 GB host + ~4.3 GB render peak + ~4 GB daemon = no headroom for the next render batch if anyone is debugging.
3. **Risk:** a stale daemon that ate memory mid-render is a credible OOM trigger on T-1 / T-0 / T+1 days. Cleaner to keep it down.
4. **The standing exclude rule already handles it.** `scripts/mcp_daemon.py` is gitignored and stays that way. No commit hygiene cost.

## 5 — Conditions to revive

Revive if and only if a planned task explicitly needs one of:

- `mcp__blender__search_polyhaven_assets` / `mcp__blender__download_polyhaven_asset` (and the HTTPS download script is insufficient).
- `mcp__blender__search_sketchfab_models` / Sketchfab import for furniture or model asset.
- `mcp__blender__generate_hyper3d_model_via_text` / Hunyuan3D text→mesh.
- `mcp__blender__get_viewport_screenshot` for an interactive debug session.

Otherwise: leave dead. T1.6 (per-variant lighting differentiation), T2.6 (terrain DEM wiring), T2.1 (stub population) all live within the CLI sub-render path.

## 6 — Followups (post-escritura, not blocking)

- Once T2.x tasks resume, re-evaluate whether the daemon is worth keeping resident for a long workday vs. on-demand-only.
- If kept resident, add a SIGTERM-on-OOM watchdog in `scripts/mcp_daemon.py` so the addon Blender dies gracefully before stealing memory from a render. Optional, low priority.
- Memory note: keep [[feedback_render_parallelism]] cross-referenced from this doc — that constraint is the actual reason for the retire.

---

**Decision:** retire for now, revival recipe documented above, `scripts/mcp_daemon.py` stays gitignored, no code edits needed. Task CC-TOOL.1 closes as **resolved-by-retire** rather than resolved-by-fix.
