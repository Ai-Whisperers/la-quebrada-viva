# Client — La Quebrada Viva

> Source of truth for *who* the project is for. Last updated: 2026-06-10.

## Client (legal owner of the land and the buyer we work for)

| | Wesley Manuel van de Camp |
|---|---|
| Nationality | Neerlandés (Dutch) |
| Civil status | Soltero |
| ID | Pasaporte N.º NWF23H565 |
| Legal share of purchase | 75% (G. 1.877.250.000) |
| Acted through | Thijs Adrianus Hendricus as **gestor de negocios ajenos** (Art. 1.808 CC PY) at signing |

**Domicilio especial:** Calle 16 y Río Paraguay, barrio Laurelty, San Lorenzo, Paraguay.

Wesley is the principal. All client communication, deliverables, and concept art route through him.

## Co-buyer (financial partner; not the design client)

| | Thijs Adrianus Hendricus |
|---|---|
| Nationality | Neerlandés (Dutch) |
| ID | Pasaporte NP19HPFP6 |
| Legal share | 25% (G. 625.750.000) |
| Role in transaction | Self + gestor for Wesley (per boleto §head) |

Thijs is Wesley's partner in the land purchase but is **not** the design client. Concept art, design decisions, and any digital deliverables flow to Wesley.

## Sellers (transferors)

- **Justiniano Torrasca Delgado** — C.I. 448.802 (paraguayo, casado)
- **María Teresa Medina de Torrasca** — C.I. 540.636 (paraguaya, casada)

Bienes gananciales — both signatures required. Esposa consintió en el acto.

## Notary / Escrow

- **Escribana Pública Cynthia Andrea Peña Ros** — holds the G. 250.300.000 seña in depósito notarial until escritura signs.

## Intermediary (real estate agent)

- **Juan José Burgos Armoa** — C.I. 4.580.315
- Commission: G. 313.000.000 (paid from seña remanente + direct top-up by Wesley + Thijs at signing).

## Our side — AI Whisperers

**AI Whisperers** is the agency providing digital support to Wesley. Specifically:

- **Research** — site analysis, climate, flora, construction methods, regulatory
- **Planning** — concept design, phasing, technical decisions, vendor sourcing
- **Digital help** — this 3D Blender visualization, technical documentation, ongoing tooling

**Lead on this project: Ivan Weiss Van Der Pol** (per `MASTER_BRIEF.md:4`). The "Owner" line there is misleading — Ivan is **not** the legal owner of the land. Wesley is. The line should be read as "project lead / architect of the digital deliverables", not "landowner."

## What we're doing right now (per Ivan, 2026-06-10)

> "for now we are modeling the place in 3d so we can build example houses in blender so the client can use as concept art etc"

So the **current scope** is:

1. **3D model of the place** — the actual 62-ha site in Escobar, Paraguarí (topography, stream, terraces, escarpment, forest, existing structures, climate)
2. **Example houses** in Blender — variant concept designs the client (Wesley) can review as concept art
3. **Concept-art-grade renders** — presentation material, not engineering drawings

**Implications:**

- The site model is the durable deliverable. It does not need to be redone per house variant.
- The cob/bottle design currently in `lqv/` (`lqv/house/cob.py`, `bottle_wall.py`, `tatakua.py`) is the **first example house**. It's the most-researched option (628 lines of site research in `paraguay_clay_house_research.md` point to it). Other example houses may be added later as separate modules — same site, different house.
- "Barro house idea is scrapped" (Ivan, earlier message) — reframed: the cob/earthen approach is **not being scrapped**; it's the *first* example house. Additional example houses on the same site may follow if the client wants options.
- The 10 design rules in `MASTER_BRIEF.md §14` apply to the *current* example house (the cob/bottle one). If we add a second example house (e.g. timber frame, modern minimalist) the rules may need to be re-scoped — but that's not on the table right now.

## Land — the actual subject of the project

See [`docs/contract_summary.md`](./contract_summary.md) for the parcel-level breakdown.

| | |
|---|---|
| District | Escobar (Gral. Patricio Escobar) |
| Department | Paraguarí |
| Country | República del Paraguay |
| Total area | 62 Has. 5.737 m² 4.704 cm² |
| Comprised of | 6 fincas (5 in Mbopicua, 1 in Ybyraty) |
| Price | G. 2.503.000.000 (G. 40M/ha) |
| Seña paid | G. 250.300.000 (10%) — held by Escribana Peña |
| Saldo at signing | G. 2.190.000.000 net to sellers + G. 313M commission to Burgos |

## Critical dates

| Date | Event | Status |
|---|---|---|
| 2026-04-28 | Boleto privado signed | ✅ done |
| 2026-04-28 | Seña G. 250.3M deposited with Escribana Peña | ✅ done |
| 2026-06-27 | **Escritura pública deadline** (60 días corridos) | ⚠ **17 days from today (2026-06-10)** |
| 27-Jun onward | If sellers default: penalty G. 500.600.000 to buyers | conditional |
| 27-Jun onward | If buyers default: forfeit seña to sellers (less notary costs) | conditional |

The closing deadline is the binding date for everything else. If the land doesn't close, the concept art is for a project that may not happen.

## Documents for client work

- **Contract**: [`docs/2026-04-28_boleto_compraventa_torrasca-vandecamp.pdf`](./2026-04-28_boleto_compraventa_torrasca-vandecamp.pdf) (original borrador, 5 pages)
- **Contract summary**: [`docs/contract_summary.md`](./contract_summary.md) (quick-reference, greppable)
- **Site research**: [`docs/paraguay_clay_house_research.md`](./paraguay_clay_house_research.md) (site-confirmed v2, authoritative)
- **Design brief**: [`docs/MASTER_BRIEF.md`](./MASTER_BRIEF.md) (zones, climate, flora, 10 rules)
- **Render manifest**: [`STATUS.md`](../STATUS.md) (what's delivered, what's pending)

## Open items before 27 June (chase items, not open questions for the client)

1. Sellers' entrega of: títulos de propiedad, planos, informes periciales, comprobantes de pago de impuestos inmobiliarios (Cl. OCTAVA ii) — **due within 5 business days of 2026-04-28 ≈ 2026-05-06**; should already be in hand.
2. Anexo I — the technical descriptions of each finca.
3. Confirmación con Escribana Peña de que retendrá y distribuirá los fondos conforme a Cl. CUARTA.
4. Designación formal de la escribana para la escritura (Cl. SEXTA — buyers designan, presumably Peña given the seña deposit).
5. Verificación de **certificados catastrales-registrales** de cada finca (libre de gravamen, inhibiciones, embargos).

For the T-7 / T-5 / T-2 / signing-day / T+30 day-by-day action sequence with a risk register, see [`CLOSING_DAY_PREP.md`](./CLOSING_DAY_PREP.md).
