# WhatsApp message draft — for Ivan to send to Wes's group

> **Read this first:** I (Erebus) cannot send WhatsApp messages on your
> behalf, and I don't have Wes's phone number / group ID in the repo to
> verify the recipient. **You need to send this manually** via WhatsApp
> Web or your phone.
>
> This draft is structured so you can:
> 1. **Verify the group** is the right one (e.g., "Wes + Ivan" or
>    "Wes + Ivan + Kiki" or your team channel — pick the right group!)
> 2. **Copy the message body** below
> 3. **Edit anything** you want to personalize or shorten
> 4. **Send via WhatsApp**

---

## ⚠️ Before sending — verify the group

**Steps:**
1. Open WhatsApp Web (web.whatsapp.com) or your phone
2. Look at your chat list — find the Wes group (you'll know it by name)
3. Click into the group, verify the participants include Wes
4. (If unsure which group: ask Wes via WhatsApp first, "which group should
   I send the big RV update to?")
5. Once verified: copy the message below, paste, send

**Group verification questions to ask Wes first (if needed):**
- "Which group should I send this update to? The one with just you and me,
  or the bigger team one?"
- "Want it in English or Dutch?"

---

## Message body (recommended — copy-paste this)

```
Hey Wes — quick big update on RV (the repo is now Riverstone Valley
internally, more on that below).

I've been running the repo through 4 restructure passes + 2 polish
passes + a Wes-facing onboarding stack + a full rename. Here's
what changed in the last session, organized by what you actually
care about:

---

## 1. The name (BIG, READ THIS FIRST)

The repo content has been renamed from "La Quebrada Viva" →
"Riverstone Valley" in 307 user-facing files. I did this because
that's your first instinct from audio E ("stolen from
Yellowstone, it's Riverstone Valley. Boom. Boom. Boom.").

BUT — important:
- This is PROVISIONAL pending your W0.6 decision
- You said "voorkeur voor 'mooi Spaans' boven 'yellowstone-achtig'"
- I built you 100 candidates + 3 top picks with critic-roast in
  docs/people/PROJECT_NAME_CANDIDATES.md
- My honest pick: "Villa del Cielo" (matches your stated preference)
- Runner-up: "Riverstone Valley" (your first instinct)
- Dark horse: "Valle de Lapachos" (PY authenticity)

What's NOT renamed (preserved for safety):
- The repo URL (github.com/Ai-Whisperers/la-quebrada-viva)
- The legal name on the escritura
- The lqv/ Python package
- License files, scripts, data refs

Revert is one `git revert` away. Your call.

---

## 2. 6 new Wes-facing docs (the onboarding stack)

You now have a complete 10-doc reading stack. Total: ~30-45 min read.

Priority order:
1. docs/WES_INDEX.md — your 1-page nav (already existed)
2. docs/WES_FAQ.md — 12 first-timer questions, plain language
3. docs/WES_GLOSSARY.md — NL/ES/EN vocabulary, ~90 terms
4. docs/WES_NEXT_30_DAYS.md — your calendar, week by week
5. docs/WES_WARNINGS.md — 14 things that might surprise you
6. docs/WES_HOW_WE_WORK.md — how AI Whisperers + Wes collaborate
7. docs/POST_ESCRITURA_NOW.md — what's blocking Fase 1
8. docs/CRITIQUE_FOR_WES.md — short roast
9. docs/people/WES_ACTIONS.md — the 5 things only you can do
10. audios/.../final/SYNTHESIS.md — the full vision, distilled

I also wrote 2 new docs you'll want:
- docs/people/WES_PROFILE.md — full client analysis of YOU
  (how you think, how you decide, what speeds you up vs slows
  you down, your 10 working rules)
- docs/people/PROJECT_NAME_CANDIDATES.md — the 100 names

---

## 3. The repo is now clean

- 0 broken links across 442 .md files
- 16/16 pytest invariants green
- All READMEs and INDEXes regenerate from disk state
- Every cross-reference resolves

The 5 restructure passes + 2 polish passes + 1 link sweep + 1
rename = 15 commits this session. Repo went from:
- 2,368 → 1,861 tracked files (-21%)
- 696 MB → 359 MB tracked (-48%)
- 80 → 59 top-level docs (-26%)
- 109 → 63 idea files (46 auto-fill archived)

---

## 4. Your 5 actions this week (unchanged)

From docs/people/WES_ACTIONS.md:
1. W0.1 — book NL+PY attorney call
2. W0.2 — schedule Sonja questionnaire call
3. W0.3 — send Anexo I chase to Escribana
4. W0.4 — decide Fase 1 ownership (personal/BV3/hybrid)
5. W0.5 — pick 5 of 15 materials topics for AI research sprint

Plus the new one I added:
6. W0.6 — pick the project name (Villa del Cielo vs Riverstone
   Valley vs your pick from the 100)

---

## 5. What I need from you

Just the W0.6 name pick, ideally by Tuesday 2026-07-21 (next week
per WES_NEXT_30_DAYS.md). When you pick, I'll re-run the rename
to whatever you choose.

If you want to skip the rename and just stay with La Quebrada
Viva: that's fine too. Tell me and I'll `git revert` the commit.

Otherwise: open docs/people/PROJECT_NAME_CANDIDATES.md, read the
top 3, and reply with A/B/C/Other.

---

— Ivan (sent via Erebus)
```

---

## Shorter alternative (if the above is too long)

```
Hey Wes — big RV update in the repo. Two things:

1. The repo content has been renamed to "Riverstone Valley" in 307
   files (provisional, pending your W0.6 name decision). Revert is
   one `git revert` away. You have 100 name candidates + my top 3
   picks (Villa del Cielo, Riverstone Valley, Valle de Lapachos)
   in docs/people/PROJECT_NAME_CANDIDATES.md.

2. 6 new Wes-facing docs added (FAQ, Glossary, Calendar, Warnings,
   How-We-Work, plus WES_PROFILE.md about you). ~30-45 min total
   read. Start at docs/WES_INDEX.md.

Repo is clean: 0 broken links, 16/16 tests green. Your 5 actions
this week (W0.1-W0.5) plus the new W0.6 name pick are in
docs/people/WES_ACTIONS.md.

Reply when you've picked the name (or want to stay with La
Quebrada Viva).

— Ivan
```

---

## Even shorter version (just the essentials)

```
Wes — RV update. Renamed 307 files to "Riverstone Valley" (your
first instinct), but it's provisional until you pick W0.6. 100
name candidates + my top 3 (Villa del Cielo / Riverstone Valley /
Valle de Lapachos) in docs/people/PROJECT_NAME_CANDIDATES.md. 6 new
Wes-facing docs (FAQ, Glossary, Calendar, Warnings, How-We-Work,
profile) all at docs/WES_INDEX.md. Repo is clean. Just need your
W0.6 name pick — A/B/C/Other. — Ivan
```

---

## Notes for Ivan (don't send to Wes)

1. **Verify the group first.** Don't blast this to the wrong Wes or
   to a customer/stranger. Open WhatsApp, find the right group,
   confirm it's Wes.

2. **Consider the tone.** The message above is structured for clarity
   (heavy use of headers + bullets). If Wes prefers conversational
   tone, edit down. The shorter versions might land better in chat.

3. **The "My honest pick: Villa del Cielo" might surprise him.** It
   explicitly contradicts his first instinct (Riverstone Valley).
   He's a "visionary-doer" who wants honest critique — so this
   framing works. But if you want to soften, change to: "Top 3 with
   critic-roast in docs/people/PROJECT_NAME_CANDIDATES.md."

4. **Don't promise the rename is final.** It's provisional. Wes might
   pick something else entirely. The message correctly says "revert is
   one git revert away" which gives him control.

5. **If you're sending on a Sunday night or early Monday, consider
   that Wes reads weekly digest on Monday 8am PY.** The message will
   be seen then, which is good timing.

6. **Save the message to drafts first.** Open WhatsApp Web → your
   Wes group → attach file (paste from clipboard) or just paste the
   message → don't send yet → review one more time → send.

---

*Generated 2026-07-03 by Erebus. Drafted for manual sending by Ivan.*
*Ideally sent Monday morning after Wes reads the weekly digest.*