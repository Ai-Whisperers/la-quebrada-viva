#!/usr/bin/env bash
# Post-signing finalize — La Quebrada Viva escritura 2026-06-27
#
# DO NOT RUN UNTIL THE ESCRITURA HAS ACTUALLY BEEN SIGNED.
#
# What this does (in order, idempotent, dry-run by default):
#   1. Verify repo state: master, clean, in sync with origin.
#   2. Verify the pre-event tag `escritura-2026-06-27` exists and points at the
#      pinned print-pack commit `0081129` (full SHA 00811297c5ec2dbfa77cdd2e5a04fea34a8fb702).
#   3. Create annotated tag `escritura-signed-2026-06-27` on the same commit,
#      with a message templated from CLI flags (--time / --notes).
#   4. Push the tag to origin.
#   5. Emit a stub memory file at /tmp/lqv_project_state_2026_06_27_signed.md for
#      human review before promotion to ~/.claude/projects/.../memory/.
#   6. Print a checklist of MASTER_TODO P0b.2 rows that the caller now needs to
#      tick in the next commit (tag promote ✓, memory update pending review,
#      Wesley followup, freeze lift).
#
# Naming convention: matches the CONTINGENCIES escritura-<state>-<date> family
# (escritura-sent-*, escritura-errata-v2-*, escritura-signed-*, escritura-postponed-*).
#
# Flags:
#   --time HH:MM       Local -03 signing time. Default: 10:00
#   --notes TEXT       Free-form note appended to the tag annotation.
#   --apply            Actually do it. Without this, dry-run only.
#
# Usage (dry-run first, ALWAYS):
#   bash scripts/post_signing_finalize.sh
#   bash scripts/post_signing_finalize.sh --time 10:18 --notes "Cl. OCTAVA ratificada verbal"
#   bash scripts/post_signing_finalize.sh --apply --time 10:18 --notes "..."

set -euo pipefail

PINNED_COMMIT="00811297c5ec2dbfa77cdd2e5a04fea34a8fb702"
PRE_TAG="escritura-2026-06-27"
SIGNED_TAG="escritura-signed-2026-06-27"
BUNDLE_SHA="9ce96b859620201bee7dadc7e8f164c4177613e69e7fb66e30bc14085724a53c"
DECK_SHA="2e4c265cd2795d7b43e88c145274bf5ea9a4c6517d337a1e2eba5c0860701137"
MEMORY_STUB="/tmp/lqv_project_state_2026_06_27_signed.md"

SIGN_TIME="10:00"
NOTES=""
APPLY=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --time)  SIGN_TIME="$2"; shift 2 ;;
    --notes) NOTES="$2"; shift 2 ;;
    --apply) APPLY=1; shift ;;
    -h|--help) sed -n '1,40p' "$0"; exit 0 ;;
    *) echo "unknown flag: $1" >&2; exit 2 ;;
  esac
done

step() { printf "\n\033[1m[%s]\033[0m %s\n" "$1" "$2"; }
ok()   { printf "  \033[32mOK\033[0m %s\n" "$1"; }
fail() { printf "  \033[31mFAIL\033[0m %s\n" "$1" >&2; exit 1; }
note() { printf "  • %s\n" "$1"; }

cd "$(git rev-parse --show-toplevel)"

step 1 "Repo state checks"
[[ "$(git rev-parse --abbrev-ref HEAD)" == "master" ]] || fail "not on master"
ok "on branch master"

[[ -z "$(git status --short)" ]] || fail "working tree dirty; commit or stash first"
ok "git status clean"

git fetch --quiet origin master
[[ -z "$(git log @{u}..HEAD --oneline)" ]] || fail "local ahead of origin/master; push first"
[[ -z "$(git log HEAD..@{u} --oneline)" ]] || fail "origin/master ahead of local; pull/rebase first"
ok "master at parity with origin/master"

step 2 "Pre-event tag check"
git rev-parse --verify "$PRE_TAG" >/dev/null 2>&1 || fail "tag $PRE_TAG not found"
actual=$(git rev-list -n1 "$PRE_TAG")
[[ "$actual" == "$PINNED_COMMIT" ]] || fail "$PRE_TAG points at $actual, expected $PINNED_COMMIT"
ok "$PRE_TAG → $PINNED_COMMIT (= pinned 0081129)"

if git rev-parse --verify "$SIGNED_TAG" >/dev/null 2>&1; then
  note "$SIGNED_TAG already exists locally — skipping create"
  EXISTS_LOCAL=1
else
  EXISTS_LOCAL=0
fi

step 3 "Bundle + deck SHA re-verify (defense in depth)"
actual_bundle=$(sha256sum dist/wesley_bundle_20260616-1715.zip | awk '{print $1}')
[[ "$actual_bundle" == "$BUNDLE_SHA" ]] || fail "bundle SHA drift: $actual_bundle"
ok "bundle SHA matches pinned $BUNDLE_SHA"

actual_deck=$(sha256sum docs/escritura_deck/escritura_deck_v6.pdf | awk '{print $1}')
[[ "$actual_deck" == "$DECK_SHA" ]] || fail "deck SHA drift: $actual_deck"
ok "deck SHA matches pinned $DECK_SHA"

step 4 "Build tag annotation"
TAG_MSG=$(cat <<EOF
Escritura signed at Escribanía Cynthia Andrea Peña Ros, Asunción.
6 padrones, 62 Ha 5737 m² 4704 cm², total Gs. 2.503.000.000.
Signed 2026-06-27 ${SIGN_TIME} -03.
${NOTES:+Notes: ${NOTES}}
Anchor commit: ${PINNED_COMMIT}
Bundle SHA-256: ${BUNDLE_SHA}
Deck SHA-256:   ${DECK_SHA}
EOF
)
echo "---- tag annotation preview ----"
echo "$TAG_MSG"
echo "--------------------------------"

step 5 "Emit memory stub at $MEMORY_STUB"
cat > "$MEMORY_STUB" <<MSTUB
---
name: project-state-2026-06-27-signed
description: Escritura signed 2026-06-27 — outcome, anchor commit, post-event constraints
metadata:
  type: project
---

Escritura signed 2026-06-27 ${SIGN_TIME} -03 at Escribanía Cynthia Andrea Peña Ros, Asunción.

**Why:** Anchors the 62-ha La Quebrada Viva parcel (Escobar/Paraguarí) under Wesley van de Camp (75%) + Thijs (25%) and closes the T0.x escritura sprint. ${NOTES}

**How to apply:**
- Post-event commits are not gated by the renderer byte-freeze at \`85e86aa\` — \`build_scene.py\` is free to evolve. Confirm explicitly before the first edit, however.
- Anchor commit \`${PINNED_COMMIT}\` (pinned \`0081129\`) carries both \`${PRE_TAG}\` and \`${SIGNED_TAG}\`; archive the print pack as immutable.
- BoQ catálogo headline figure \$268,685 (Gs. 1.961.403.785 @ TC 7300) is the as-signed reference for phase-2 financial planning. See [[feedback_boq_scope_filter]].
- Cl. OCTAVA (ii) vendor comprobantes deadline: 5 hábiles from 2026-06-27. Track in \`docs/OCTAVA_VENDOR_TRACKER.md\`.
- Phase-2 ramp begins per \`docs/MASTER_TODO.md\` P1.B.4 → P1.C → P2 chain. The 78433a7 polish wave is the live forward base; \`85e86aa\` remains the historical render anchor for the 18 finals.
- Supersedes [[project_state_2026_06_17]].
MSTUB
ok "memory stub written ($(wc -l < "$MEMORY_STUB") lines)"
note "review then move to /home/ai-whisperers/.claude/projects/-home-ai-whisperers-blender-projects/memory/project_state_2026_06_27_signed.md"
note "remember to add the MEMORY.md index pointer"

step 6 "Apply (tag create + push)"
if [[ "$APPLY" -ne 1 ]]; then
  note "DRY-RUN: skipping tag create + push. Re-run with --apply to execute."
  exit 0
fi

if [[ "$EXISTS_LOCAL" -eq 0 ]]; then
  git tag -a "$SIGNED_TAG" "$PINNED_COMMIT" -m "$TAG_MSG"
  ok "created annotated tag $SIGNED_TAG on $PINNED_COMMIT"
fi

git push origin "$SIGNED_TAG"
ok "pushed $SIGNED_TAG to origin"

step 7 "Next steps for the caller"
note "tick MASTER_TODO P0b.2 row 'Tag promote' as closed, citing $SIGNED_TAG → $PINNED_COMMIT"
note "review $MEMORY_STUB → move to memory/ → add MEMORY.md index pointer → tick 'Memory update' row"
note "open Wesley followup conversation per P0b.2 row"
note "lift build_scene.py freeze per P0b.2 row (confirm with Ivan before first edit)"
note "T+30 archive pass: see docs/ARCHIVE_RUNBOOK.md"
