"""GBIF species occurrences — what wildlife is documented in the region.

Free API, no auth. Uses GBIF occurrence search to find species documented
in the 3.3 km bbox around the property. Deduplicates to species level.

Outputs:
  - docs/site_data/gbif/species_list.json   (all species)
  - docs/site_data/gbif/species_summary.txt (human-readable summary)
  - docs/site_data/gbif/species_markdown.md (markdown table for docs)
"""
import json
import sys
from collections import Counter
from pathlib import Path

import requests
from dotenv import load_dotenv

HERE = Path('/home/ai-whisperers/blender-projects/house-field')
load_dotenv(dotenv_path=HERE / '.env.local')

BBOX = {'south': -25.645, 'north': -25.615, 'west': -57.045, 'east': -57.015}
OUT_DIR = HERE / 'docs' / 'site_data' / 'gbif'
OUT_DIR.mkdir(parents=True, exist_ok=True)

GBIF_OCC = 'https://api.gbif.org/v1/occurrence/search'

PER_PAGE = 300
MAX_TOTAL = 2000


def fetch_occurrences():
    """Fetch occurrence records from GBIF for the bbox, paginated."""
    all_records = []
    offset = 0
    seen_keys = set()

    # WKT polygon bbox — GBIF expects lat,lon order (lat first in coordinates)
    wkt = f'POLYGON(({BBOX["west"]} {BBOX["south"]},{BBOX["west"]} {BBOX["north"]},{BBOX["east"]} {BBOX["north"]},{BBOX["east"]} {BBOX["south"]},{BBOX["west"]} {BBOX["south"]}))'

    print('  fetching occurrences (paginated)…', end=' ', flush=True)
    while offset < MAX_TOTAL:
        params = {
            'geometry': wkt,
            'limit': PER_PAGE,
            'offset': offset,
        }
        r = requests.get(GBIF_OCC, params=params, timeout=30)
        r.raise_for_status()
        data = r.json()
        results = data.get('results', [])
        if not results:
            break

        new_count = 0
        for rec in results:
            key = rec.get('speciesKey') or rec.get('key')
            if key and key not in seen_keys:
                seen_keys.add(key)
                all_records.append(rec)
                new_count += 1

        print(f'{len(all_records)}…', end=' ', flush=True)
        if len(results) < PER_PAGE:
            break
        offset += PER_PAGE

    print(f'done ({len(all_records)} unique species)')
    return all_records


def extract_species(records):
    """Deduplicate records to species level with taxonomy info."""
    seen = set()
    species_list = []

    for rec in records:
        sk = rec.get('speciesKey')
        if not sk or sk in seen:
            continue
        seen.add(sk)

        vernacular = ''
        vn = rec.get('vernacularName') or rec.get('vernacularNames')
        if isinstance(vn, list) and vn:
            vernacular = vn[0].get('vernacularName', '') if isinstance(vn[0], dict) else str(vn[0])
        elif isinstance(vn, str):
            vernacular = vn

        species_list.append({
            'species': rec.get('scientificName', ''),
            'canonicalName': rec.get('canonicalName', rec.get('scientificName', '')),
            'commonName': vernacular,
            'kingdom': rec.get('kingdom', ''),
            'phylum': rec.get('phylum', ''),
            'class': rec.get('class', ''),
            'order': rec.get('order', ''),
            'family': rec.get('family', ''),
            'genus': rec.get('genus', ''),
            'iucnRedList': rec.get('iucnRedListCategory', ''),
            'gbifKey': sk,
            'occurrenceCount': rec.get('occurrenceCount', 1),
            'firstSeen': rec.get('firstObserved', '') or rec.get('eventDate', ''),
        })

    return species_list


def main():
    print('=' * 70)
    print('GBIF species — Escobar / Mbopicua, PY')
    print(f'Bbox: W={BBOX["west"]} S={BBOX["south"]} E={BBOX["east"]} N={BBOX["north"]}')
    print('=' * 70)

    records = fetch_occurrences()
    species = extract_species(records)
    print(f'\nTotal species: {len(species)}')

    out_json = OUT_DIR / 'species_list.json'
    with open(out_json, 'w') as f:
        json.dump(species, f, indent=2, default=str)
    print(f'  JSON → {out_json}')

    md = ['# GBIF Species — La Quebrada Viva Region\n']
    md.append(f'Bbox: {BBOX["south"]}°S to {BBOX["north"]}°S, {BBOX["west"]}°W to {BBOX["east"]}°W\n')
    md.append(f'## Species ({len(species)} records)\n')
    md.append('| # | Species | Common Name | Class | Family | IUCN |')
    md.append('|---|---------|-------------|-------|--------|------|')
    for i, sp in enumerate(sorted(species, key=lambda x: x.get('class', 'zz')), 1):
        cn = sp['commonName'] or '—'
        iucn = sp['iucnRedList'] or '—'
        cls = sp.get('class', '') or sp.get('kingdom', '')
        md.append(f"| {i} | *{sp['canonicalName']}* | {cn} | {cls} | {sp['family']} | {iucn} |")

    out_md = OUT_DIR / 'species_markdown.md'
    with open(out_md, 'w') as f:
        f.write('\n'.join(md))
    print(f'  Markdown → {out_md}')

    class_counts = Counter(sp.get('class', 'Other') or 'Other' for sp in species)
    summary = ['GBIF Species Summary', '=' * 40]
    summary.append(f'Total unique species: {len(species)}')
    summary.append(f'Bbox: {BBOX["south"]}°S to {BBOX["north"]}°S, {BBOX["west"]}°W to {BBOX["east"]}°W')
    summary.append('')
    summary.append('By class:')
    for cls, cnt in sorted(class_counts.items(), key=lambda x: -x[1]):
        summary.append(f'  {cls}: {cnt}')
    summary.append('')
    summary.append('Source: GBIF.org, accessed 2026-06-10')

    out_sum = OUT_DIR / 'species_summary.txt'
    with open(out_sum, 'w') as f:
        f.write('\n'.join(summary))
    print(f'  Summary → {out_sum}')
    print('\nDONE.')
    return 0


if __name__ == '__main__':
    sys.exit(main())