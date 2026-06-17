# Share links — bundle distribution (T-1 → T-0)

Bundle (266 MB) is too large for direct email attachment. The deck (10.8 MB) is fine inline; the bundle ships via shared link.

## Primary: Google Drive

- Folder: `La Quebrada Viva — escritura 2026-06-27`
- Path: `Drive > Ai-Whisperers > Clients > Wesley van de Camp > escritura_2026-06-27`
- Sharing: link-restricted, viewer permission, recipients = `wesley@...`, `thijs@...`, `pena@...`, optionally `burgos@...` if asked.
- Link expiry: 2026-09-27 (90 days post-signing). Renew once if Wesley still needs it after that.
- Files in the share folder:
  - `wesley_bundle_20260616-1715.zip` (266 MB)
  - `wesley_bundle_20260616-1715.zip.sha256` (separate sidecar, 1 KB)
  - `wesley_bundle_20260616-1715.manifest.txt` (per-file SHA, 12 KB)
  - `escritura_deck_v6.pdf` (10.8 MB) — duplicate for one-stop reference

## Fallback 1: WeTransfer

- Use if Drive link is blocked on recipient's network or recipient is not on Google.
- Plan: free tier (7-day expiry) is enough; send T-1 evening so it expires after the funds receipt window.
- Same 3-file payload, zipped as `wesley_bundle_20260616-1715_share.zip` if WeTransfer rejects the .sha256 sidecar (rare).
- Email body must include the SHA-256 inline so the recipient can verify even if the sidecar is lost.

## Fallback 2: USB hand-off only

- If all networks fail: bring the USB to the 09:45 -03 meet. The bundle + sidecar live at `dist/wesley_bundle_20260616-1715.zip`.
- USB content: bundle + sidecar + manifest + a printed cover sheet with the SHA-256 (so verification doesn't depend on having the laptop open).

## Pinned hashes (must match exactly in every message body)

- Bundle SHA-256: `9ce96b859620201bee7dadc7e8f164c4177613e69e7fb66e30bc14085724a53c`
- Deck SHA-256: `2e4c265cd2795d7b43e88c145274bf5ea9a4c6517d337a1e2eba5c0860701137`

## Send timing

- T-1 evening (2026-06-26, ~20:00 -03): share link created and tested from a private/incognito session (verify the link actually opens and the download starts).
- T-0 (2026-06-27, ~07:30 -03): include the share link in the Pena/Wesley/Thijs emails alongside the inline deck attachment. Burgos gets deck only (no bundle) unless he asks.
- T-0 (~09:30 -03): re-test the link from mobile data (Tigo 4G) to confirm field accessibility.

## Verification line for recipients (paste into email body)

> Para verificar la integridad del bundle: `sha256sum wesley_bundle_20260616-1715.zip` debe devolver `9ce96b859620201bee7dadc7e8f164c4177613e69e7fb66e30bc14085724a53c`. El archivo `.sha256` en el mismo enlace permite verificación automática (`sha256sum -c wesley_bundle_20260616-1715.zip.sha256`).

(English equivalent in `wesley_en.md`.)
