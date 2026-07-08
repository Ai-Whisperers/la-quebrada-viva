# CF Pages Custom Domain Status (2026-07-08)

## Current state

The LQV walkthrough viewer is served at:

| URL | Type | Status |
|---|---|---|
| `https://lqv-walkthrough.pages.dev` | CF Pages default subdomain | ✅ Live |
| `https://lqv-walkthrough.com` | **Custom domain** | ❌ Not registered |
| `https://lqv-walkthrough.co` | Custom domain alternative | ❌ Not registered |
| `https://la-quebrada-viva.com` | Brand-primary custom domain | ❌ Not registered |

The CF Pages project (`lqv-walkthrough`) accepts custom domains via Settings →
Custom domains in the Cloudflare dashboard. Adding one requires the domain
DNS to already be pointing to Cloudflare nameservers, which requires the
domain to be **registered at a registrar** and **added to a Cloudflare zone**.

## To make `lqv-walkthrough.com` (or `la-quebrada-viva.com`) work

Three-step process requiring Ivan's authorization for capex:

1. **Register** the domain at a registrar — Namecheap / Cloudflare Registrar / GoDaddy / Porkbun / etc.
   - `.com`: $9–13 USD/year (no residency restrictions for Paraguay-based owners).
   - `.com.py`: ~$80 USD/year if Wes has a Paraguayan company (NIC.py).
   - `.paraguay`: no public registration (not a real TLD).
   - **Recommendation**: Use Cloudflare Registrar (at-cost, no markup) if the registrar is approved by Ivan for the AI-Whisperers side. Otherwise Namecheap is the cheapest mainstream option.

2. **Add the domain to Cloudflare** — free tier is fine.
   - Cloudflare scans existing DNS records automatically.
   - Nameservers are assigned.

3. **Update nameservers at the registrar** to point to Cloudflare-assigned NS.

4. **Wait for DNS propagation** — 5 minutes to 48 hours, usually 30 minutes.

5. **Attach the domain to the CF Pages project**:
   - Cloudflare dashboard → Pages → lqv-walkthrough → Settings → Custom domains → Set up a custom domain → enter `lqv-walkthrough.com`.
   - CF automatically creates the CNAME record.
   - HTTPS provisioning is automatic (CF Pages integrates with Universal SSL).

## Total cost

| Item | Cost | Recurring? |
|---|---|---|
| Domain registration (.com) | $9–13 USD/year | Annual |
| Cloudflare hosting (free tier) | $0 | — |
| Universal SSL | $0 | — |
| **Total first year** | **$9–13 USD** | **$9–13/year after** |

## Decision criteria

**Pro custom domain**:
- Looks more professional to European tourists (Wes's target demographic).
- Removes the `.pages.dev` suffix (it currently reads as "preview").
- `la-quebrada-viva.com` matches the brand name in the docs (HOUSING_PARK_CONCEPT).
- Email addresses on the domain (ivan@la-quebrada-viva.com) for outbound sales.

**Con**:
- Another annual charge to track.
- Breaks any existing bookmarks to `lqv-walkthrough.pages.dev` — would need 301 redirect at the CF zone level.
- Wes hasn't explicitly requested this. Should be a Wes/Ivan decision.

## Recommendation

Defer to Ivan. If greenlit, recommend:
1. Register `la-quebrada-viva.com` (brand-primary) at Cloudflare Registrar.
2. ALSO register `lqv-walkthrough.com` (current preview project name) and redirect it to `la-quebrada-viva.com` via 301 — keeps backward compat.
3. Total: ~$25/year. Decision time: 5 minutes.

## Tasks awaiting Ivan's authorization

- [ ] **Capex approval**: $25–30 USD/year for two `.com` domains
- [ ] **Brand decision**: which is primary — `la-quebrada-viva.com` (matches branding) or `lqv-walkthrough.com` (matches current preview URL)?
- [ ] **Registrar choice**: Cloudflare Registrar at-cost vs Namecheap vs Porkbun

Author: Erebus / Ai-Whisperers
Date: 2026-07-08
