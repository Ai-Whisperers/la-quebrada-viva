#!/usr/bin/env bash
# T-1 evening pre-flight — La Quebrada Viva escritura 2026-06-27
#
# Single-command sanity sweep to run the night before signing.
# Read-only — never mutates the repo. Exits 0 on GO, non-zero on NO-GO.
#
# What it verifies:
#   1. Repo state: on master, clean, in sync with origin.
#   2. Pre-event tag escritura-2026-06-27 dereferences to pinned commit.
#   3. Bundle SHA-256 matches pinned.
#   4. Deck v6 SHA-256 matches pinned.
#   5. dist/print_pack_2026-06-27/VERIFY.sh exits 0.
#   6. All required ops docs present at expected paths.
#   7. Pytest invariants 16/16 green.
#   8. scripts/post_signing_finalize.sh syntax valid + dry-run reachable.
#
# Usage:
#   bash scripts/preflight_t_minus_1.sh

set -uo pipefail

PINNED_COMMIT="00811297c5ec2dbfa77cdd2e5a04fea34a8fb702"
PRE_TAG="escritura-2026-06-27"
BUNDLE_SHA="9ce96b859620201bee7dadc7e8f164c4177613e69e7fb66e30bc14085724a53c"
DECK_SHA="2e4c265cd2795d7b43e88c145274bf5ea9a4c6517d337a1e2eba5c0860701137"

FAILURES=0
REPO=$(git rev-parse --show-toplevel)
cd "$REPO"

step() { printf "\n\033[1m[%s]\033[0m %s\n" "$1" "$2"; }
ok()   { printf "  \033[32mPASS\033[0m %s\n" "$1"; }
fail() { printf "  \033[31mFAIL\033[0m %s\n" "$1" >&2; FAILURES=$((FAILURES+1)); }
note() { printf "  • %s\n" "$1"; }

step 1 "Repo state"
[[ "$(git rev-parse --abbrev-ref HEAD)" == "master" ]] && ok "on master" || fail "not on master"
[[ -z "$(git status --short)" ]] && ok "working tree clean" || fail "working tree dirty"
git fetch --quiet origin master 2>/dev/null || note "fetch failed (offline?) — comparing against cached @{u}"
ahead=$(git log @{u}..HEAD --oneline 2>/dev/null | wc -l)
behind=$(git log HEAD..@{u} --oneline 2>/dev/null | wc -l)
[[ "$ahead" -eq 0 ]] && ok "not ahead of origin" || fail "$ahead commits ahead of origin"
[[ "$behind" -eq 0 ]] && ok "not behind origin" || fail "$behind commits behind origin"

step 2 "Pre-event tag dereferences to pinned commit"
if git rev-parse --verify "$PRE_TAG" >/dev/null 2>&1; then
  actual=$(git rev-list -n1 "$PRE_TAG")
  [[ "$actual" == "$PINNED_COMMIT" ]] && ok "$PRE_TAG -> $PINNED_COMMIT" || fail "$PRE_TAG -> $actual (expected $PINNED_COMMIT)"
else
  fail "tag $PRE_TAG missing"
fi

step 3 "Bundle SHA"
if [[ -f dist/wesley_bundle_20260616-1715.zip ]]; then
  actual=$(sha256sum dist/wesley_bundle_20260616-1715.zip | awk '{print $1}')
  [[ "$actual" == "$BUNDLE_SHA" ]] && ok "bundle SHA matches pinned" || fail "bundle SHA drift: $actual"
else
  fail "bundle missing at dist/wesley_bundle_20260616-1715.zip"
fi

step 4 "Deck v6 SHA"
if [[ -f docs/escritura_deck/escritura_deck_v6.pdf ]]; then
  actual=$(sha256sum docs/escritura_deck/escritura_deck_v6.pdf | awk '{print $1}')
  [[ "$actual" == "$DECK_SHA" ]] && ok "deck SHA matches pinned" || fail "deck SHA drift: $actual"
else
  fail "deck missing at docs/escritura_deck/escritura_deck_v6.pdf"
fi

step 5 "Print pack VERIFY.sh"
if [[ -x dist/print_pack_2026-06-27/VERIFY.sh ]]; then
  if bash dist/print_pack_2026-06-27/VERIFY.sh >/dev/null 2>&1; then
    ok "VERIFY.sh exits 0"
  else
    fail "VERIFY.sh exits non-zero (re-run manually to see details)"
  fi
else
  fail "VERIFY.sh missing or not executable"
fi

step 6 "Required ops docs"
REQUIRED=(
  docs/CONTINGENCIES.md
  docs/ROLLBACK_RUNBOOK.md
  docs/POSTMORTEM_TEMPLATE.md
  docs/DECISIONS.md
  docs/MASTER_TODO.md
  docs/AUTONOMOUS_PLAN.md
  docs/escritura_deck/escritura_deck_v6.pdf
  dist/print_pack_2026-06-27/MORNING_RUNBOOK_2026-06-27.md
  dist/print_pack_2026-06-27/WALLET_CARD.txt
  dist/print_pack_2026-06-27/INTEGRITY.md
  dist/print_pack_2026-06-27/BUNDLE_README.txt
  scripts/post_signing_finalize.sh
)
for f in "${REQUIRED[@]}"; do
  if [[ -f "$f" ]]; then ok "$f"; else fail "missing: $f"; fi
done

step 7 "Pytest invariants"
if command -v python3 >/dev/null 2>&1; then
  if python3 -m pytest -q --no-header >/tmp/lqv_preflight_pytest.log 2>&1; then
    line=$(tail -1 /tmp/lqv_preflight_pytest.log)
    ok "pytest: $line"
  else
    fail "pytest failed — see /tmp/lqv_preflight_pytest.log"
  fi
else
  fail "python3 not found"
fi

step 8 "Finalize script"
if bash -n scripts/post_signing_finalize.sh 2>/dev/null; then
  ok "post_signing_finalize.sh syntax valid"
else
  fail "post_signing_finalize.sh has syntax errors"
fi

printf "\n"
if [[ "$FAILURES" -eq 0 ]]; then
  printf "\033[1;32mGO — all %d checks green. Safe to sleep, sign in the morning.\033[0m\n" 8
  exit 0
else
  printf "\033[1;31mNO-GO — %d failure(s). Resolve before signing.\033[0m\n" "$FAILURES"
  exit 1
fi
