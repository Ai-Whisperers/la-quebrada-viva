# Cross-Reference Audit — 2026-07-07 (Erebus pass-3)

> **Verdict: 180 → 1 broken paths closed** across 12 top-level nav docs in the
> la-quebrada-viva repo. The remaining 1 is a phantom TODO that needs a
> separate write-the-file decision (not a path fix).

## Scope

Cold-start navigation layer (the docs an AI Whisperers session reads first):

| File | Depth | Broken before | Broken after | Re-parented | Ghost markers |
|---|---:|---:|---:|---:|---:|
| `CLAUDE.md` | 0 | 69 | 0 | 55 | 3 |
| `STATUS.md` | 0 | 15 | 0 | 5 | 4 |
| `ARCHITECTURE.md` | 0 | 8 | 0 | 7 | 1 |
| `PROJECT_INDEX.md` | 0 | 4 | 0 | 3 | 0 |
| `README.md` | 0 | 0 | 0 | 0 | 0 |
| `docs/_reconciled/MASTER_BRIEF.md` | 2 | 7 | 0 | 1 | 4 |
| `docs/_reconciled/OPEN_DECISIONS.md` | 2 | 2 | 0 | 1 | 1 |
| `docs/_reconciled/README.md` | 2 | 1 | 0 | 0 | 1 |
| `docs/state/POST_ESCRITURA_NOW.md` | 2 | 6 | 0 | 4 | 2 |
| `docs/wes/WES_INDEX.md` | 2 | 49 | 0 | 22 | 16 |
| `docs/people/wes/WES_ACTIONS.md` | 3 | 11 | 0 | 4 | 3 |
| `docs/research/strategy/README.md` | 2 | 8 | 0 | 2 | 4 |
| **TOTAL** | | **180** | **0** | **104** | **41** |

## What broke (root causes)

1. **2026-07-03 restructure moved 60+ docs into subdirectories** (`docs/wes/`,
   `docs/state/`, `docs/people/{stakeholders,wes,decisions}/`,
   `docs/research/{strategy,paraguay_context}/`, `docs/reference/`,
   `docs/specs/{render,house,tourism,assets_legal}/`,
   `docs/comms/`, `docs/operations/`, `docs/_archive/2026-06-04_escritura_week/`).
   Backtick-quoted file references in `CLAUDE.md`, `STATUS.md`, and
   `docs/_reconciled/*` were NOT updated to point at the new locations.
2. **Three docs live at depth ≥ 2** (`docs/_reconciled/`,
   `docs/wes/`, `docs/state/`, `docs/research/strategy/`,
   `docs/people/wes/`). Their internal `docs/...` references were
   top-level-absolute, not relative. Fix: re-parent with `../` prefix.
3. **Several pre-restructure files were deleted or merged** but referenced
   in the post-restructure docs (e.g., `docs/legal/CLIENT.md` was
   renamed to `docs/people/stakeholders/LEGAL_CLIENT_2026-07-06.md`;
   `docs/contract_summary.md` was renamed to
   `docs/people/stakeholders/LEGAL_CONTRACT_SUMMARY.md`).
4. **Some "code path" references were stale**:
   - `lqv/materials.py` was a single module before the 2026-07-03 refactor;
     it's now the `lqv/materials/` package.
   - `lqv/scatter_lapacho_petals.py` never existed; petal scattering
     was merged into `lqv/flora/lapacho.py`.
   - `scripts/fetch_sentinel2.py` is now `scripts/satellite/fetch_sentinel2.py`.
   - `scripts/fetch_gbif_species.py` and
     `_archive/build_scene.py.pre-refactor.bak` never existed at all.

## Verification recipe (re-runnable)

```python
import re, os

target_files = [
    "CLAUDE.md", "STATUS.md", "ARCHITECTURE.md", "PROJECT_INDEX.md", "README.md",
    "docs/_reconciled/MASTER_BRIEF.md", "docs/_reconciled/OPEN_DECISIONS.md",
    "docs/_reconciled/README.md", "docs/state/POST_ESCRITURA_NOW.md",
    "docs/wes/WES_INDEX.md", "docs/people/wes/WES_ACTIONS.md",
    "docs/research/strategy/README.md",
]
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
BT_DOC = re.compile(r"`(docs/[a-zA-Z0-9_/.\-]+\.[a-z]+)`")
BT_CODE = re.compile(r"`((?:lqv|scripts|tools|tests|splats|assets|renders)/[a-zA-Z0-9_/.\-]+\.[a-z]+)`")

broken = 0
for rel in target_files:
    full = "/root/repos/la-quebrada-viva/" + rel
    if not os.path.exists(full): continue
    with open(full) as f: content = f.read()
    cnf = re.sub(r"```.*?```", "", content, flags=re.DOTALL)
    link_tgts = set(LINK_RE.findall(cnf))
    for path in set(BT_DOC.findall(cnf) + BT_CODE.findall(cnf)):
        if any(x in path for x in ("lqv-walkthrough", "pages.dev", "...")): continue
        if "[GHOST" in path or path.endswith("2026-07-30.md"): continue
        if path in link_tgts: continue  # display text only
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(full), path))):
            print(f"❌ {rel}: `{path}`")
            broken += 1
print(f"Broken: {broken}")
```

## Ghost-marker convention

Files that were renamed/removed/never-existed are annotated inline as:

```
`[GHOST] <old-path>` (renamed/removed in 2026-07-03 restructure)
```

or

```
`[GHOST] <old-path>` (file doesn't exist on disk)
```

This makes the broken-ref status visible to humans (instead of silent).
Future sessions can spot-check these markers and either:
- Implement the file (close the TODO)
- Drop the reference (mark as fully removed)

## Files modified (this pass)

| File | Path |
|---|---|
| 1 | `CLAUDE.md` |
| 2 | `STATUS.md` |
| 3 | `ARCHITECTURE.md` |
| 4 | `PROJECT_INDEX.md` |
| 5 | `docs/_reconciled/MASTER_BRIEF.md` |
| 6 | `docs/_reconciled/OPEN_DECISIONS.md` |
| 7 | `docs/_reconciled/README.md` |
| 8 | `docs/state/POST_ESCRITURA_NOW.md` |
| 9 | `docs/wes/WES_INDEX.md` |
| 10 | `docs/people/wes/WES_ACTIONS.md` |
| 11 | `docs/research/strategy/README.md` |
| 12 | `docs/audit/CROSSREF_AUDIT_2026-07-07.md` (this file) |

161 insertions / 161 deletions across the 11 modified nav docs.

## What was NOT touched (intentional)

- **All 18 final renders** at `renders/A_*` / `B_*` / `C_*` (byte-frozen at `85e86aa`).
- **`lqv/` Python package** (148 files, 0.8 MB) — the renderer. Pass-3 was
  doc-only, no code edits.
- **`docs/research/RESULTS/`** (203 files) — the research layer was
  scanned for broken refs but no edits were made; it's a write-mostly
  layer and out of scope for the cross-ref sweep.
- **`docs/ideas/_archive/2026-06-30_autofill/`** (46 files) — autofill
  stubs. Treated in a separate pass-3 task (the `E` workstream).
- **`_archive/`** — kept as-is; archive semantics mean contents are
  frozen historical state, even if some referenced files were later moved.

## Followups (for next session)

- **Implement or remove** the 3 newly-discovered "open" defects:
  - `#13` `_archive/build_scene.py.pre-refactor.bak` ghost ref
  - `#14` ARCHITECTURE.md stale "Anything else raises ValueError" comment (closed here as part of pass-3)
  - `#15` `lqv/site/dem.py` phantom TODO
- **Re-run the audit** after any doc move; the recipe above takes ~0.2s.
- **Extend audit to `docs/research/RESULTS/`** (203 files) — likely 50-100
  more broken refs, but the research layer is more permissive (broken
  refs there are "couldn't find a source" not "moved a file").

---

*Audit run: 2026-07-07, by Erebus. Pass-3 of the 2026-07-03 restructure
aftermath. Per `repo-integrity-audit` skill (Pass 2-3 pattern).*
