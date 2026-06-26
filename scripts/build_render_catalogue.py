#!/usr/bin/env python3
"""
Walk the renders/ tree + Monday deliverables, group every PNG by asset, sort
chronologically, and emit a markdown catalogue at docs/render_catalogue/.

No file copies. The catalogue links to existing paths (disk is 91% full).

Coverage:
    renders/*.png                                 (18 canonical escritura finals + previews)
    renders/sub/*.png                             (~100 flat "latest" sub-renders)
    renders/sub/runs/<run_id>_<asset>[_tag]/*.png (~302 versioned run folders)
    renders/sub/latest/*.png                      (mirrored latest variants)
    docs/site_data_2026-06-13_snapshot/renders_monday/*.png    (5 Monday-deliverable renders)

Output:
    docs/render_catalogue/INDEX.md                (top-level)
    docs/render_catalogue/by_asset/<asset>.md     (per-asset chronological page)
    docs/render_catalogue/catalogue.json          (machine-readable sidecar)

Asset canonicalization: a run folder named `20260612_phase2a_bamboo_river_house_dusk`
canonicalizes to asset `bamboo_river_house` and variant tag `dusk`. Date tokens are
extracted (YYYYMMDD), otherwise the leading non-asset token is treated as the run_tag.
"""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass, asdict
from datetime import datetime, timezone, UTC
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
RENDERS = REPO / "renders"
SUB = RENDERS / "sub"
SUB_RUNS = SUB / "runs"
SUB_LATEST = SUB / "latest"
MONDAY = REPO / "docs" / "site_data_2026-06-13_snapshot" / "renders_monday"
OUT = REPO / "docs" / "render_catalogue"

# Canonical asset names (from lqv/typologies + lqv/amenities + sub-render drivers).
# Order matters: longer names must come before shorter prefixes so the matcher
# doesn't bind "bamboo_beton_28" to the "bamboo_beton" stem.
CANONICAL_ASSETS = [
    # houses (15 typologies)
    "bamboo_beton_family_rectangular",
    "bamboo_beton_family_curved",
    "bamboo_beton_28",
    "bamboo_beton_30",
    "bamboo_boomhut_treehouse",
    "bamboo_curved_roof_villa",
    "bamboo_container_4pax",
    "bamboo_wigwam_lodge",
    "bamboo_river_house",
    "container_river_house",
    "italian_river_house_4pax",
    "italian_stone_small_v1",
    "italian_stone_small_v2",
    "clay_terracotta_estate",
    "hobbit_house",
    # typology-amenities (3) + amenities (4)
    "bamboo_outdoor_shower",
    "bamboo_portal",
    "candle_path",
    "eco_retreat_modern_oasis",
    "labrisa_lounge",
    "floating_dining",
    "eco_pool",
    # site-scale
    "terrain_62ha_photoreal",
    "terrain_62ha",
    "terrain_house_scale",
    "mushroom_cob_house_aerial",
    "mushroom_cob_house_elev",
    "mushroom_cob_house_hero",
    "mushroom_cob_house",
    # flora / scatter / misc
    "bamboo_clump",
    "boulder_cluster",
    "flora_anthurium",
    "flora_jacaranda",
    "flora_pachira",
    "anthurium",
    "agave",
    "bottle_wall",
    "lapacho_petals",
    "hdri_dusk_compare",
    "material_wall_compare",
    # photoreal / gallery feature sub-renders (one bucket per feature; views A/B/C
    # = front/side/top become variants within the page)
    "lapacho_tree",
    "tree_fern",
    "pindo_palm",
    "mango",
    "canopy_volume",
    "cob_walls",
    "escarpment",
    "fireflies",
    "services",
    "stream",
    "tatakua",
    "terraces",
    "valley_mist",
    "window_emission",
]

# View / time / camera suffixes that should be treated as sub-variants, not part
# of the asset name.
VIEW_SUFFIXES: set[str] = {
    "front", "side", "top", "iso", "aerial", "hero", "elev",
    "dusk", "day", "noon", "night", "golden",
    "oblique", "oblique_alos", "oblique_cop30",
}

# Protocol-v2 view axis (RENDER_VIEW) — see docs/RESULTS_GUIDE.md §5.
# Untagged renders default to `hero3q` per the back-compat invariant
# (`renders/sub/<asset>_<variant>.png` flat path == hero3q).
PROTOCOL_V2_VIEWS: tuple[str, ...] = (
    "hero3q", "elevation", "plan", "section", "interior", "xray",
)
DEFAULT_VIEW = "hero3q"

# Prefixes to strip before canonical match (longest first).
STRIP_PREFIXES: tuple[str, ...] = (
    "gallery_flora_photoreal_v2_",
    "gallery_flora_photoreal_",
    "gallery_real_",
    "p0_rerender_",
)

VARIANT_RE = re.compile(r"^(A|B|C)\.png$")
VARIANT_VIEW_RE = re.compile(
    r"^(A|B|C)_(" + "|".join(PROTOCOL_V2_VIEWS) + r")\.png$"
)
DATE_RE = re.compile(r"^(20\d{6})$")
PREVIEW_RE = re.compile(r"^_preview_([ABC])_([a-z_]+)\.png$")
CANONICAL_FINAL_RE = re.compile(r"^([ABC])_([a-z_]+)\.png$")
# `<asset_stem>_<A|B|C>_<view>` — protocol-v2 flat / latest-mirror grammar.
STEM_V2_RE = re.compile(
    r"^(.+?)_(A|B|C)_(" + "|".join(PROTOCOL_V2_VIEWS) + r")$"
)


@dataclass
class Render:
    path: str                 # repo-relative
    asset: str                # canonical asset
    variant: str              # A / B / C / preview / other
    view: str                 # protocol-v2 view (hero3q | elevation | plan | section | interior | xray)
    date: str                 # YYYY-MM-DD (or "" if unknown)
    run_tag: str              # short identifier from run folder name
    sub_variant: str          # extra suffix after asset (dusk, oblique_alos, etc.)
    size_bytes: int
    mtime: str                # ISO date
    source: str               # "canonical_final" | "preview" | "monday" | "sub_flat" | "sub_run" | "sub_latest"


def _peel_view_suffix(s: str) -> tuple[str, str]:
    """If `s` ends in a known view suffix (e.g. `_front`, `_oblique_alos`),
    return (base, view). Otherwise (s, '').
    """
    # try longer suffixes first
    for view in sorted(VIEW_SUFFIXES, key=len, reverse=True):
        if s == view:
            return "", view
        if s.endswith("_" + view):
            return s[: -len(view) - 1], view
    return s, ""


def canonicalize_asset(stem: str) -> tuple[str, str]:
    """Return (canonical_asset, sub_variant_suffix) for a name.

    Strategy:
      1. Strip leading `p0_rerender_` / gallery prefixes.
      2. Strip a leading `YYYYMMDD_` date token (and surrounding underscores).
      3. Match against CANONICAL_ASSETS (longest-first via list order):
         exact, then `<name>_<suffix>`, then `<prefix>_<name>` (anchored).
      4. Fallback: peel a trailing view suffix (front/side/top/dusk/...) so
         e.g. `phase2a_bamboo_river_house_dusk` → (`bamboo_river_house`, `dusk`).
    """
    s = stem
    # 1. strip known prefixes (longest first via STRIP_PREFIXES order)
    changed = True
    while changed:
        changed = False
        for pfx in STRIP_PREFIXES:
            if s.startswith(pfx):
                s = s[len(pfx):]
                changed = True
                break
    # 2. strip leading date
    m = re.match(r"^(20\d{6})_(.+)$", s)
    if m:
        s = m.group(2)
    # 3. canonical match
    for name in CANONICAL_ASSETS:
        if s == name:
            return name, ""
        if s.startswith(name + "_"):
            return name, s[len(name) + 1:]
        if s.endswith("_" + name):
            return name, s[: -len(name) - 1]
        # also handle name embedded with a run-tag prefix: `<head>_<name>_<tail>`
        token = "_" + name + "_"
        if token in s:
            idx = s.index(token)
            tail = s[idx + len(token):]
            return name, tail
    # 4. peel trailing view suffix as a fallback bucket name
    base, view = _peel_view_suffix(s)
    if base and view:
        return base, view
    return s, ""


def parse_run_folder(folder: str) -> tuple[str, str, str, str]:
    """Parse a run-folder name into (date, run_tag, asset, sub_variant).

    Examples:
        20260612_phase2a_bamboo_river_house_dusk
            → ("2026-06-12", "phase2a", "bamboo_river_house", "dusk")
        p0_rerender_20260612_agave_front
            → ("2026-06-12", "p0_rerender", "agave", "front")
        bamboo_rebuild_v1_bamboo_clump
            → ("", "bamboo_rebuild_v1", "bamboo_clump", "")
        dem_ab_20260618_terrain_62ha_photoreal_oblique_alos
            → ("2026-06-18", "dem_ab", "terrain_62ha_photoreal", "oblique_alos")
    """
    tokens = folder.split("_")
    date = ""
    date_idx = -1
    for i, t in enumerate(tokens):
        m = DATE_RE.match(t)
        if m:
            y = m.group(1)
            date = f"{y[0:4]}-{y[4:6]}-{y[6:8]}"
            date_idx = i
            break
    asset, sub = canonicalize_asset(folder)
    if date_idx >= 0:
        # everything before date = run_tag prefix; everything between date+1 and asset = also run_tag
        before = "_".join(tokens[:date_idx])
        # strip the asset+suffix off the back
        run_tag = before if before else "_".join(tokens[date_idx + 1:date_idx + 2])
    else:
        # No date — use leading tokens until asset starts as the run_tag
        if asset != folder:
            idx = folder.index(asset)
            head = folder[:idx].rstrip("_")
            run_tag = head or "(no-tag)"
        else:
            run_tag = "(no-tag)"
    return date, run_tag, asset, sub


def fmt_size(n: int) -> str:
    v: float = float(n)
    for unit in ("B", "KB", "MB", "GB"):
        if v < 1024:
            return f"{int(v)}{unit}" if unit == "B" else f"{v:.1f}{unit}"
        v /= 1024
    return f"{v:.1f}TB"


def iso_mtime(p: Path) -> str:
    return datetime.fromtimestamp(p.stat().st_mtime).strftime("%Y-%m-%d")


def repo_rel(p: Path) -> str:
    return str(p.relative_to(REPO))


def collect_canonical_finals() -> list[Render]:
    out: list[Render] = []
    for p in sorted(RENDERS.glob("*.png")):
        name = p.name
        m = CANONICAL_FINAL_RE.match(name)
        if m:
            variant, cam = m.groups()
            out.append(Render(
                path=repo_rel(p),
                asset="ESCRITURA_FINALS",
                variant=variant,
                view=DEFAULT_VIEW,
                date="2026-06-10",
                run_tag="canonical_85e86aa",
                sub_variant=cam,
                size_bytes=p.stat().st_size,
                mtime=iso_mtime(p),
                source="canonical_final",
            ))
            continue
        m = PREVIEW_RE.match(name)
        if m:
            variant, cam = m.groups()
            out.append(Render(
                path=repo_rel(p),
                asset="ESCRITURA_FINALS",
                variant=f"{variant}_preview",
                view=DEFAULT_VIEW,
                date="",
                run_tag="preview",
                sub_variant=cam,
                size_bytes=p.stat().st_size,
                mtime=iso_mtime(p),
                source="preview",
            ))
    return out


def collect_sub_flat() -> list[Render]:
    out: list[Render] = []
    if not SUB.exists():
        return out
    for p in sorted(SUB.glob("*.png")):
        stem = p.stem
        # Protocol v2 flat grammar: `<asset_stem>_<A|B|C>_<view>`.
        # Legacy back-compat: `<asset_stem>_<A|B|C>` → view = hero3q.
        variant = ""
        view = DEFAULT_VIEW
        asset_stem = stem
        m = STEM_V2_RE.match(stem)
        if m:
            asset_stem, variant, view = m.group(1), m.group(2), m.group(3)
        elif stem.endswith(("_A", "_B", "_C")):
            variant = stem[-1]
            asset_stem = stem[:-2]
        asset, sub = canonicalize_asset(asset_stem)
        out.append(Render(
            path=repo_rel(p),
            asset=asset,
            variant=variant or "(none)",
            view=view,
            date="",
            run_tag="flat_latest",
            sub_variant=sub,
            size_bytes=p.stat().st_size,
            mtime=iso_mtime(p),
            source="sub_flat",
        ))
    return out


def collect_sub_runs() -> list[Render]:
    out: list[Render] = []
    if not SUB_RUNS.exists():
        return out
    for d in sorted(SUB_RUNS.iterdir()):
        if not d.is_dir() or d.name.startswith("_"):
            continue
        date, run_tag, asset, sub = parse_run_folder(d.name)
        for p in sorted(d.glob("*.png")):
            # Protocol v2: `<A|B|C>_<view>.png` — fall back to legacy `<A|B|C>.png`.
            view = DEFAULT_VIEW
            mv = VARIANT_VIEW_RE.match(p.name)
            if mv:
                variant, view = mv.group(1), mv.group(2)
            else:
                m = VARIANT_RE.match(p.name)
                variant = m.group(1) if m else p.stem
            out.append(Render(
                path=repo_rel(p),
                asset=asset,
                variant=variant,
                view=view,
                date=date,
                run_tag=run_tag,
                sub_variant=sub,
                size_bytes=p.stat().st_size,
                mtime=iso_mtime(p),
                source="sub_run",
            ))
    return out


def collect_sub_latest() -> list[Render]:
    out: list[Render] = []
    if not SUB_LATEST.exists():
        return out
    for p in sorted(SUB_LATEST.rglob("*.png")):
        rel = p.relative_to(SUB_LATEST)
        view = DEFAULT_VIEW
        # latest/<asset>/<variant>.png OR latest/<asset>_<variant>[_<view>].png
        parts = rel.parts
        if len(parts) == 2:
            asset_stem, fname = parts
            file_stem = Path(fname).stem
            # nested: try `<A|B|C>_<view>` then bare `<variant>`.
            mv = VARIANT_VIEW_RE.match(fname)
            if mv:
                variant, view = mv.group(1), mv.group(2)
            else:
                variant = file_stem
            asset, sub = canonicalize_asset(asset_stem)
        else:
            stem = p.stem
            m = STEM_V2_RE.match(stem)
            if m:
                asset_stem, variant, view = m.group(1), m.group(2), m.group(3)
            elif stem.endswith(("_A", "_B", "_C")):
                variant, asset_stem = stem[-1], stem[:-2]
            else:
                variant, asset_stem = "(none)", stem
            asset, sub = canonicalize_asset(asset_stem)
        out.append(Render(
            path=repo_rel(p),
            asset=asset,
            variant=variant,
            view=view,
            date="",
            run_tag="sub_latest_mirror",
            sub_variant=sub,
            size_bytes=p.stat().st_size,
            mtime=iso_mtime(p),
            source="sub_latest",
        ))
    return out


def collect_monday() -> list[Render]:
    out: list[Render] = []
    if not MONDAY.exists():
        return out
    for p in sorted(MONDAY.glob("*.png")):
        stem = p.stem  # monday_cam_a_italian etc.
        out.append(Render(
            path=repo_rel(p),
            asset="MONDAY_DELIVERABLE",
            variant=stem,
            view=DEFAULT_VIEW,
            date="",
            run_tag="monday_pack",
            sub_variant="",
            size_bytes=p.stat().st_size,
            mtime=iso_mtime(p),
            source="monday",
        ))
    return out


def write_asset_page(asset: str, records: list[Render], out_dir: Path) -> Path:
    # sort: date asc (blanks last), then run_tag, view, sub_variant, variant
    def key(r: Render):
        d = r.date or "9999-99-99"
        return (d, r.run_tag, r.view, r.sub_variant, r.variant)

    records = sorted(records, key=key)
    page = out_dir / f"{asset}.md"
    sheet = out_dir.parent / "contact_sheets" / f"{asset}.jpg"
    lines = [
        f"# {asset}",
        "",
        f"Total renders: **{len(records)}**.",
        "",
    ]
    # per-view coverage block — protocol v2 axis at a glance
    by_view: dict[str, int] = defaultdict(int)
    for r in records:
        by_view[r.view] += 1
    if by_view:
        lines += [
            "## Coverage by view",
            "",
            "| View | Renders |",
            "|---|---:|",
        ]
        for view in PROTOCOL_V2_VIEWS:
            lines.append(f"| `{view}` | {by_view.get(view, 0)} |")
        other = sorted(v for v in by_view if v not in PROTOCOL_V2_VIEWS)
        for view in other:
            lines.append(f"| `{view}` | {by_view[view]} |")
        lines.append("")
    if sheet.exists():
        lines += [
            f"![{asset} contact sheet](../contact_sheets/{asset}.jpg)",
            "",
            "_Contact sheet above shows up to 9 latest renders, deduped by variant._",
            "",
        ]
    lines += [
        "Grouped by run (date + tag), then view, then variant.",
        "",
    ]
    # group by (date, run_tag, view, sub_variant)
    groups: dict[tuple[str, str, str, str], list[Render]] = defaultdict(list)
    for r in records:
        groups[(r.date, r.run_tag, r.view, r.sub_variant)].append(r)

    for (date, run_tag, view, sub), recs in sorted(groups.items()):
        header_bits = [date or "(undated)"]
        if run_tag:
            header_bits.append(run_tag)
        header_bits.append(f"view={view}")
        if sub:
            header_bits.append(sub)
        lines.append(f"## {' · '.join(header_bits)}")
        lines.append("")
        lines.append("| Variant | Path | Size | mtime | Source |")
        lines.append("|---|---|---:|---|---|")
        for r in recs:
            lines.append(
                f"| `{r.variant}` | [`{r.path}`](../../../{r.path}) "
                f"| {fmt_size(r.size_bytes)} | {r.mtime} | {r.source} |"
            )
        lines.append("")
    page.write_text("\n".join(lines))
    return page


def write_index(by_asset: dict[str, list[Render]], all_records: list[Render], out_dir: Path) -> Path:
    page = out_dir / "INDEX.md"
    by_source = defaultdict(int)
    by_date = defaultdict(int)
    by_view = defaultdict(int)
    for r in all_records:
        by_source[r.source] += 1
        by_date[r.date or "(undated)"] += 1
        by_view[r.view] += 1

    lines = [
        "# Render catalogue — La Quebrada Viva",
        "",
        f"_Generated by `scripts/build_render_catalogue.py`. PNG count: **{len(all_records)}**._",
        "",
        "Index of every render artefact in the repo, organised by",
        "`(asset, view, variant)`. Per-asset pages chronologically by run-date,",
        "then by view (protocol-v2 axis), then variant (lighting A/B/C). No",
        "physical file copies (catalogue links to existing paths under `renders/`).",
        "",
        "## Summary",
        "",
        "| Source | Count |",
        "|---|---:|",
    ]
    for src in sorted(by_source):
        lines.append(f"| `{src}` | {by_source[src]} |")
    lines.append("")

    lines += [
        "## View distribution (protocol-v2 axis)",
        "",
        "Renders predating `RENDER_VIEW` default to `hero3q` per the back-compat",
        "invariant. See `docs/RESULTS_GUIDE.md` §5 for the multi-view shotlist.",
        "",
        "| View | Renders |",
        "|---|---:|",
    ]
    for view in PROTOCOL_V2_VIEWS:
        lines.append(f"| `{view}` | {by_view.get(view, 0)} |")
    extra_views = sorted(v for v in by_view if v not in PROTOCOL_V2_VIEWS)
    for view in extra_views:
        lines.append(f"| `{view}` | {by_view[view]} |")
    lines.append("")

    lines += [
        "## Date distribution",
        "",
        "| Date | Renders |",
        "|---|---:|",
    ]
    for d in sorted(by_date):
        lines.append(f"| {d} | {by_date[d]} |")
    lines.append("")

    # canonical finals + Monday: pull these up
    lines += [
        "## Canonical escritura finals (18, frozen at `85e86aa`, dated 2026-06-10)",
        "",
        "All six cameras × variants A/B/C, used in the escritura deck (`02_deck`)",
        "and Wesley bundle (`03_renders`). Source commit `85e86aa` is the renderer",
        "byte-freeze parent of the print pack.",
        "",
    ]
    finals = by_asset.get("ESCRITURA_FINALS", [])
    finals_sorted = sorted(finals, key=lambda r: (r.variant, r.sub_variant))
    lines.append("| Variant | Camera | Path | Size |")
    lines.append("|---|---|---|---:|")
    for r in finals_sorted:
        lines.append(f"| `{r.variant}` | {r.sub_variant} | [`{r.path}`](../../{r.path}) | {fmt_size(r.size_bytes)} |")
    lines.append("")

    monday = by_asset.get("MONDAY_DELIVERABLE", [])
    if monday:
        lines += [
            "## Monday deliverable pack (5 renders)",
            "",
            "| Variant | Path | Size |",
            "|---|---|---:|",
        ]
        for r in sorted(monday, key=lambda r: r.variant):
            lines.append(f"| `{r.variant}` | [`{r.path}`](../../{r.path}) | {fmt_size(r.size_bytes)} |")
        lines.append("")

    # per-asset roster (sub-renders only)
    lines += [
        "## Per-asset roster",
        "",
        "Each link points to the asset's chronological page. Sub-renders only —",
        "canonical finals and the Monday pack appear above. `Views covered`",
        "lists protocol-v2 views present (legacy renders count as `hero3q`).",
        "",
        "| Asset | Renders | Latest date | Views covered |",
        "|---|---:|---|---|",
    ]
    sub_assets: list[str] = []
    view_counts_per_asset: dict[str, dict[str, int]] = {}
    for asset in sorted(by_asset):
        if asset in ("ESCRITURA_FINALS", "MONDAY_DELIVERABLE"):
            continue
        recs = by_asset[asset]
        latest_dates = [r.date for r in recs if r.date]
        latest = max(latest_dates) if latest_dates else "(undated)"
        view_counts: dict[str, int] = defaultdict(int)
        for r in recs:
            view_counts[r.view] += 1
        view_counts_per_asset[asset] = dict(view_counts)
        covered = [v for v in PROTOCOL_V2_VIEWS if view_counts.get(v, 0) > 0]
        covered += sorted(v for v in view_counts if v not in PROTOCOL_V2_VIEWS)
        covered_str = ", ".join(f"`{v}`" for v in covered) or "—"
        lines.append(
            f"| [{asset}](by_asset/{asset}.md) | {len(recs)} | {latest} | {covered_str} |"
        )
        sub_assets.append(asset)
    lines.append("")

    # per-asset × view matrix (protocol-v2 axis)
    lines += [
        "## Per-asset × view matrix",
        "",
        "Counts per protocol-v2 view per asset. Empty cells = no renders for that",
        "view yet; gaps here are the shotlist backlog. Legacy renders without an",
        "explicit `_<view>` suffix are bucketed into `hero3q`.",
        "",
        "| Asset | " + " | ".join(f"`{v}`" for v in PROTOCOL_V2_VIEWS) + " |",
        "|---|" + "|".join(["---:"] * len(PROTOCOL_V2_VIEWS)) + "|",
    ]
    for asset in sub_assets:
        counts = view_counts_per_asset.get(asset, {})
        cells = [str(counts.get(v, 0)) if counts.get(v, 0) else "—" for v in PROTOCOL_V2_VIEWS]
        lines.append(f"| [{asset}](by_asset/{asset}.md) | " + " | ".join(cells) + " |")
    lines.append("")

    # contact-sheet gallery: per-asset thumbnail JPGs built by build_contact_sheets.py
    sheets_dir = out_dir / "contact_sheets"
    sheets = [a for a in sub_assets if (sheets_dir / f"{a}.jpg").exists()]
    if sheets:
        lines += [
            "## Contact sheets",
            "",
            f"Per-asset thumbnail grids (≤9 latest renders each), built by",
            f"`scripts/build_contact_sheets.py`. {len(sheets)} sheets total.",
            "",
            "| Asset | Sheet |",
            "|---|---|",
        ]
        for a in sheets:
            lines.append(f"| [{a}](by_asset/{a}.md) | [![{a}](contact_sheets/{a}.jpg)](contact_sheets/{a}.jpg) |")
        lines.append("")
    lines += [
        "## Notes",
        "",
        "- Run-folder convention: `<YYYYMMDD>_<run_tag>_<asset>[_<sub_variant>]/{A,B,C}.png`.",
        "- Sub-render workflow per `feedback_sub_render_first` memory: every asset",
        "  gets a `lqv/subscene/<asset>.py` driver and lands under",
        "  `renders/sub/runs/<RENDER_RUN_ID>_<asset>[_<tag>]/<variant>.png`.",
        "- Latest-mirror copies live under `renders/sub/latest/` and the flat",
        "  `renders/sub/*.png`. These are the active references; older runs in",
        "  `renders/sub/runs/` are the version-history.",
        "- The escritura print pack at `dist/print_pack_2026-06-27/03_renders/`",
        "  ships the 18 canonical finals only; everything else here is provenance.",
        "",
    ]
    page.write_text("\n".join(lines))
    return page


def main() -> int:
    if not RENDERS.exists():
        print(f"ERROR: {RENDERS} missing", file=sys.stderr)
        return 1
    OUT.mkdir(parents=True, exist_ok=True)
    asset_dir = OUT / "by_asset"
    asset_dir.mkdir(exist_ok=True)

    all_records: list[Render] = []
    all_records += collect_canonical_finals()
    all_records += collect_sub_flat()
    all_records += collect_sub_runs()
    all_records += collect_sub_latest()
    all_records += collect_monday()

    by_asset: dict[str, list[Render]] = defaultdict(list)
    for r in all_records:
        by_asset[r.asset].append(r)

    # per-asset pages (skip the two special buckets — they live in INDEX.md)
    for asset, recs in by_asset.items():
        if asset in ("ESCRITURA_FINALS", "MONDAY_DELIVERABLE"):
            continue
        write_asset_page(asset, recs, asset_dir)

    index = write_index(by_asset, all_records, OUT)

    # JSON sidecar — keep `generated_at` stable if content is unchanged so
    # `make catalogue` is idempotent and re-runs don't churn git history.
    json_path = OUT / "catalogue.json"
    payload = {
        "total_renders": len(all_records),
        "by_source": {src: sum(1 for r in all_records if r.source == src)
                      for src in sorted({r.source for r in all_records})},
        "assets": {a: [asdict(r) for r in recs] for a, recs in sorted(by_asset.items())},
    }
    prev_ts = None
    prev_payload = None
    if json_path.exists():
        try:
            prev = json.loads(json_path.read_text())
            prev_ts = prev.get("generated_at")
            prev_payload = {k: v for k, v in prev.items() if k != "generated_at"}
        except json.JSONDecodeError:
            pass
    ts = prev_ts if prev_payload == payload and prev_ts else \
        datetime.now(UTC).isoformat().replace("+00:00", "Z")
    json_path.write_text(json.dumps({"generated_at": ts, **payload}, indent=2))

    print(f"Wrote {index}")
    print(f"Wrote {json_path}")
    print(f"Wrote {len(by_asset) - 2} per-asset pages under {asset_dir}/")
    print(f"Total renders catalogued: {len(all_records)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
