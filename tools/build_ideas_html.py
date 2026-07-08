#!/usr/bin/env python3
"""Build /root/.hermes/lqv-splat/exports/web/ideas.html from
/root/la-quebrada-viva/docs/ideas/_meta/{INDEX,INSIGHTS,SUGGESTED}.md + per-category READMEs + per-idea files.

Output: single self-contained HTML page, dark themed, filterable by priority/status/category.
This is the canonical deploy artifact — landing page for the buyer's idea catalog.
"""
import re, os, html, json
from pathlib import Path

IDEAS_ROOT = Path("/root/la-quebrada-viva/docs/ideas")
OUT_PATH = Path("/root/.hermes/lqv-splat/exports/web/ideas.html")
CATEGORIES = [
    "vision", "buyer_experience", "amenities", "construction", "house_typologies",
    "operations", "finance_legal", "site_specifics", "marketing", "risk_mitigation",
]

CATEGORY_LABELS = {
    "vision": "Project Vision",
    "buyer_experience": "Buyer / Investor Experience",
    "amenities": "Site Amenities & Experiences",
    "construction": "Construction, Materials & Site Tech",
    "house_typologies": "House Typologies",
    "operations": "Operations, Team & Workflow",
    "finance_legal": "Finance, Legal & Insurance",
    "site_specifics": "Site-Specific Decisions",
    "marketing": "Marketing, Distribution & Sales",
    "risk_mitigation": "Risk Mitigation & Safety",
}

# ---------- 1. parse INDEX.md for structured table ----------
def parse_index():
    """Return list of dicts: {id, category, priority, status, owner, title}"""
    idx_md = (IDEAS_ROOT / "_meta" / "INDEX.md").read_text(encoding="utf-8")
    rows = []
    # Each row starts with || <id> | <priority> | <status> | ... |
    # Be permissive: any line that starts with "|| <letter+digit>" is a row.
    for line in idx_md.splitlines():
        m = re.match(r"\|\|\s*([a-z]\d{2}_[a-z_]+)\s*\|\s*(P\d)\s*\|\s*`?([\w_ ]+)`?\s*\|\s*([^|]+)\|\s*`?(✓ reviewed|○ auto-fill)`?", line)
        if m:
            rows.append({
                "id": m.group(1),
                "priority": m.group(2),
                "status": m.group(3).strip(),
                "owner": m.group(4).strip(),
                "quality": m.group(5).strip(),
                "title": m.group(1),  # we'll fill from per-file later
            })
    return rows

# ---------- 2. parse per-idea files for titles & priorities ----------
def parse_idea_files():
    """Read every per-idea .md file, extract: id (from filename), title (first H1), priority, status."""
    out = {}
    for cat in CATEGORIES:
        cat_dir = IDEAS_ROOT / cat
        if not cat_dir.exists():
            continue
        for f in sorted(cat_dir.glob("*.md")):
            if f.name.lower() == "readme.md":
                continue
            txt = f.read_text(encoding="utf-8", errors="replace")
            # ID = filename stem
            id_ = f.stem
            # Title = first H1
            m = re.search(r"^#\s+(.+?)$", txt, re.MULTILINE)
            title = m.group(1).strip() if m else id_
            # Priority + Status from the metadata table at the top
            pri = re.search(r"\*\*Priority[:\*\s]+(P\d)\b", txt)
            status = re.search(r"\*\*Status[:\*\s]+`?(\w[\w\s_-]*)`?", txt)
            owner = re.search(r"\*\*Owner[:\*\s]+([^*\n]+)", txt)
            cat_guess = cat
            out[id_] = {
                "id": id_,
                "title": title,
                "category": cat_guess,
                "priority": pri.group(1) if pri else "P?",
                "status": status.group(1).strip() if status else "planned",
                "owner": owner.group(1).strip() if owner else "—",
                "filename": f.name,
            }
    return out

# ---------- 3. build HTML ----------
def make_html(ideas):
    """Return final HTML string for /ideas.html"""
    # Status color map
    sc = {
        "shipped": "#22c55e",
        "shipped_waiting_on_wes": "#84cc16",
        "decided": "#06b6d4",
        "confirmed": "#0ea5e9",
        "in_progress": "#eab308",
        "ongoing": "#eab308",
        "partial": "#f97316",
        "planned": "#94a3b8",
        "research_needed": "#a855f7",
    }
    pc = {"P0": "#ef4444", "P1": "#f97316", "P2": "#eab308", "P3": "#94a3b8"}

    # Group by category
    by_cat = {c: [] for c in CATEGORIES}
    for idea in ideas.values():
        by_cat.setdefault(idea["category"], []).append(idea)
    for cat in by_cat:
        by_cat[cat].sort(key=lambda x: (x["priority"], x["id"]))

    # Stats
    total = len(ideas)
    by_pri = {"P0": 0, "P1": 0, "P2": 0, "P3": 0, "P?": 0}
    by_st = {}
    for idea in ideas.values():
        by_pri[idea["priority"]] = by_pri.get(idea["priority"], 0) + 1
        by_st[idea["status"]] = by_st.get(idea["status"], 0) + 1

    # Build sidebar nav
    nav_html = []
    nav_html.append('<li class="nav-cat" data-cat="all"><span class="nav-count">' + str(total) + '</span>All ideas</li>')
    for cat in CATEGORIES:
        n = len(by_cat.get(cat, []))
        nav_html.append(f'<li class="nav-cat" data-cat="{cat}"><span class="nav-count">{n}</span>{html.escape(CATEGORY_LABELS[cat])}</li>')

    # Build idea cards
    cards = []
    for cat in CATEGORIES:
        for idea in by_cat.get(cat, []):
            s_color = sc.get(idea["status"], "#94a3b8")
            p_color = pc.get(idea["priority"], "#94a3b8")
            title = html.escape(idea["title"])
            cards.append(f"""
<article class="idea" data-cat="{idea['category']}" data-pri="{idea['priority']}" data-status="{idea['status']}">
  <div class="idea-head">
    <span class="idea-id">{html.escape(idea['id'])}</span>
    <span class="badge pri" style="background:{p_color}">{idea['priority']}</span>
    <span class="badge status" style="background:{s_color};color:#000">{html.escape(idea['status'].replace('_', ' '))}</span>
  </div>
  <h3 class="idea-title">{title}</h3>
  <div class="idea-meta">owner: {html.escape(idea['owner'])}</div>
</article>""")
    cards_html = "\n".join(cards)

    stats_html = "".join([
        f'<div class="stat"><div class="stat-num" style="color:{pc.get(p, "#94a3b8")}">{n}</div><div class="stat-lbl">{p}</div></div>'
        for p, n in by_pri.items() if n > 0
    ])

    body = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>LQV Ideas — Wesley's 76-idea catalog</title>
<meta name="description" content="Wesley van de Camp's 76 idea catalog for La Quebrada Viva (Riverstone Valley) — housing park + restaurant + amenities in Escobar, Paraguay. Filterable by category, priority, and status.">
<link rel="canonical" href="https://lqv-walkthrough.pages.dev/ideas.html">
<meta property="og:title" content="LQV Ideas — Wesley's 76-idea catalog">
<meta property="og:description" content="Wesley van de Camp's 76 idea catalog for La Quebrada Viva. Housing park + restaurant + amenities in Paraguay.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://lqv-walkthrough.pages.dev/ideas.html">
<meta name="theme-color" content="#0b1020">
<style>
:root {{
  --bg: #0b1020;
  --bg-2: #131a2e;
  --bg-3: #1a2342;
  --fg: #e5e7eb;
  --fg-2: #94a3b8;
  --accent: #38bdf8;
  --border: #1f2937;
}}
* {{ box-sizing: border-box; }}
html, body {{ margin: 0; padding: 0; background: var(--bg); color: var(--fg); font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', system-ui, sans-serif; }}
body {{ min-height: 100vh; }}
header {{ padding: 18px 24px; border-bottom: 1px solid var(--border); background: var(--bg-2); position: sticky; top: 0; z-index: 10; }}
header h1 {{ margin: 0; font-size: 1.2rem; color: var(--accent); font-weight: 600; }}
header .sub {{ font-size: 0.85rem; color: var(--fg-2); margin-top: 4px; }}
header .crumbs {{ margin-top: 8px; font-size: 0.8rem; }}
header .crumbs a {{ color: var(--accent); text-decoration: none; }}
header .crumbs a:hover {{ text-decoration: underline; }}

main {{ display: grid; grid-template-columns: 240px 1fr; gap: 24px; padding: 24px; max-width: 1400px; margin: 0 auto; }}
@media (max-width: 768px) {{ main {{ grid-template-columns: 1fr; }} }}

aside {{ background: var(--bg-2); border: 1px solid var(--border); border-radius: 8px; padding: 14px; height: fit-content; position: sticky; top: 110px; }}
@media (max-width: 768px) {{ aside {{ position: static; }} }}
aside h2 {{ font-size: 0.75rem; text-transform: uppercase; letter-spacing: 0.05em; color: var(--fg-2); margin: 8px 0 6px; }}
aside ul {{ list-style: none; padding: 0; margin: 0 0 16px; }}
aside li.nav-cat {{ padding: 8px 10px; cursor: pointer; border-radius: 6px; font-size: 0.9rem; display: flex; justify-content: space-between; align-items: center; transition: background 0.1s; }}
aside li.nav-cat:hover {{ background: var(--bg-3); }}
aside li.nav-cat.active {{ background: var(--bg-3); color: var(--accent); font-weight: 600; }}
aside .nav-count {{ background: var(--bg); color: var(--fg-2); font-size: 0.75rem; padding: 2px 8px; border-radius: 10px; }}

.filter-bar {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }}
.filter-bar input, .filter-bar select {{ background: var(--bg-2); color: var(--fg); border: 1px solid var(--border); padding: 8px 12px; border-radius: 6px; font-size: 0.9rem; }}
.filter-bar input {{ flex: 1; min-width: 200px; }}

.stats {{ display: flex; gap: 12px; margin-bottom: 16px; flex-wrap: wrap; }}
.stat {{ background: var(--bg-2); padding: 10px 16px; border-radius: 8px; border: 1px solid var(--border); flex: 1; min-width: 80px; text-align: center; }}
.stat-num {{ font-size: 1.5rem; font-weight: 700; }}
.stat-lbl {{ font-size: 0.7rem; color: var(--fg-2); text-transform: uppercase; letter-spacing: 0.05em; }}

.grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 12px; }}
.idea {{ background: var(--bg-2); border: 1px solid var(--border); border-radius: 8px; padding: 14px; transition: border-color 0.15s; }}
.idea:hover {{ border-color: var(--accent); }}
.idea-head {{ display: flex; align-items: center; gap: 6px; margin-bottom: 8px; flex-wrap: wrap; }}
.idea-id {{ font-size: 0.7rem; color: var(--fg-2); font-family: monospace; background: var(--bg); padding: 2px 6px; border-radius: 4px; }}
.badge {{ font-size: 0.7rem; padding: 2px 8px; border-radius: 10px; color: #fff; font-weight: 600; text-transform: uppercase; letter-spacing: 0.03em; }}
.idea-title {{ font-size: 0.95rem; margin: 4px 0 6px; line-height: 1.35; }}
.idea-meta {{ font-size: 0.75rem; color: var(--fg-2); }}

.idea.hidden {{ display: none; }}
.empty {{ padding: 40px; text-align: center; color: var(--fg-2); }}

footer {{ padding: 20px 24px; border-top: 1px solid var(--border); text-align: center; color: var(--fg-2); font-size: 0.8rem; }}
footer a {{ color: var(--accent); text-decoration: none; }}
</style>
</head>
<body>

<header>
  <h1>La Quebrada Viva — Idea Catalog</h1>
  <div class="sub">Wesley van de Camp's {total}-idea brainstorm for Riverstone Valley · housing park + restaurant + amenities in Escobar, Paraguay</div>
  <div class="crumbs"><a href="./index.html">← Walkthrough home</a> · <a href="./mapa.html">Interactive map →</a></div>
</header>

<main>
  <aside>
    <h2>Categories</h2>
    <ul>
      {''.join(nav_html)}
    </ul>
    <h2>Status legend</h2>
    <ul style="font-size:0.8rem; color:var(--fg-2);">
      <li>● shipped · live</li>
      <li>● in_progress · building now</li>
      <li>● planned · queued</li>
      <li>● research_needed · blocking</li>
      <li>● decided · closed</li>
    </ul>
    <h2>Read first</h2>
    <ul style="font-size:0.8rem;">
      <li><a href="./mapa.html" style="color:var(--accent)">Interactive site map</a></li>
      <li><a href="./escobar3d.html" style="color:var(--accent)">3D viewer</a></li>
    </ul>
  </aside>

  <section>
    <div class="stats">{stats_html}</div>
    <div class="filter-bar">
      <input id="search" type="search" placeholder="Search ideas by title or ID…" autocomplete="off">
      <select id="pri-filter">
        <option value="">All priorities</option>
        <option value="P0">P0 only</option>
        <option value="P1">P1 only</option>
        <option value="P2">P2 only</option>
        <option value="P3">P3 only</option>
      </select>
      <select id="status-filter">
        <option value="">All statuses</option>
        <option value="shipped">Shipped</option>
        <option value="in_progress">In progress</option>
        <option value="planned">Planned</option>
        <option value="research_needed">Research needed</option>
        <option value="decided">Decided</option>
      </select>
    </div>

    <div class="grid" id="grid">
      {cards_html}
    </div>
    <div class="empty hidden" id="empty">No ideas match your filter.</div>
  </section>
</main>

<footer>
  La Quebrada Viva · Escobar, Paraguarí, Paraguay · Built by Erebus · {total} ideas across 10 categories
</footer>

<script>
(function() {{
  const cards = Array.from(document.querySelectorAll('.idea'));
  const search = document.getElementById('search');
  const priFilter = document.getElementById('pri-filter');
  const statusFilter = document.getElementById('status-filter');
  const navCats = Array.from(document.querySelectorAll('li.nav-cat'));
  const empty = document.getElementById('empty');
  let activeCat = 'all';

  function applyFilters() {{
    const q = (search.value || '').toLowerCase();
    const pri = priFilter.value;
    const st = statusFilter.value;
    let visible = 0;
    for (const c of cards) {{
      const title = c.querySelector('.idea-title').textContent.toLowerCase();
      const id = c.dataset.id || c.querySelector('.idea-id').textContent.toLowerCase();
      const matchSearch = !q || title.includes(q) || id.includes(q);
      const matchCat = activeCat === 'all' || c.dataset.cat === activeCat;
      const matchPri = !pri || c.dataset.pri === pri;
      const matchSt = !st || c.dataset.status === st;
      const show = matchSearch && matchCat && matchPri && matchSt;
      c.classList.toggle('hidden', !show);
      if (show) visible++;
    }}
    empty.classList.toggle('hidden', visible > 0);
  }}

  for (const li of navCats) {{
    li.addEventListener('click', () => {{
      navCats.forEach(x => x.classList.remove('active'));
      li.classList.add('active');
      activeCat = li.dataset.cat;
      applyFilters();
    }});
  }}
  search.addEventListener('input', applyFilters);
  priFilter.addEventListener('change', applyFilters);
  statusFilter.addEventListener('change', applyFilters);

  // Activate "All" by default
  navCats[0].classList.add('active');
}})();
</script>

</body>
</html>"""

    return body


def main():
    ideas = parse_idea_files()
    print(f"Parsed {len(ideas)} per-idea files")
    out = make_html(ideas)
    OUT_PATH.write_text(out, encoding="utf-8")
    print(f"Wrote {OUT_PATH} ({len(out)} bytes)")


if __name__ == "__main__":
    main()
