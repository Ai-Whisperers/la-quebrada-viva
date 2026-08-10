# How AI Whisperers + Wes Work Together

> **For Wesley + Ivan + Kiki + Sonja.** The explicit working agreement
> between the 3 humans (Wes, Ivan, Kiki) and the AI (Erebus). Covers
> channels, cadence, what each person does, and how we handle disagreement.
>
> **Last updated:** 2026-07-03

---

## The team

| Person | Role | Time commitment | What they own |
|---|---|---|---|
| **Wes** | Founder, 75% owner, decision-maker | Part-time (15-25 hr/week) | Strategic decisions, NL-side actions, design authority |
| **Thijs** | Co-founder, 25% owner | Part-time | Operational partner, on-site periodically |
| **Ivan** | AI Whisperers founder, project manager | Full-time | Project coordination, AI prompt engineering, repo maintenance, legal liaison |
| **Kiki** | AI Whisperers — sales + NL+PY network | Full-time | NL+PY accountant referrals, sales pipeline, Booking.com setup |
| **Erebus** | AI agent (run by Ivan, 24/7) | Always-on | Repo commits, doc organization, research sprint execution, summaries |
| **Sonja** | Cultural + worker + price authority (Rule 5) | Async / on-demand | Worker salary bands, hiring intros, PY-specific norms |

## Channels

### Messaging (primary, real-time)

- **Wes ↔ Ivan** = main channel for day-to-day
- **Wes ↔ Kiki** = NL network + sales pipeline
- **Ivan ↔ Kiki** = internal AI Whisperers coordination
- **Erebus ↔ Ivan** = via the chat platform (this session)

**Cadence:** Wes responds when he can. Ivan responds within 4 hours
during PY business hours (8am-6pm PYT). Erebus responds immediately.

### The repo (async, structured)

- **Wes** records audios → Erebus transcribes → commits canon docs
- **Wes** answers questions in chat → Erebus updates decisions log
- **Ivan** prompts Erebus for research → results committed to `docs/research/RESULTS/`

**Cadence:** each Erebus turn = 1 commit. Wes can review commits at
any pace. Latest commit is at the top of every chat.

### Email (formal, slow)

- **Wes ↔ Escribana** (notary) = escritura-related
- **Wes ↔ Attorney** (post-W0.1) = legal opinion exchanges
- **Kiki ↔ NL investors** = investment decks, formal pitches

**Cadence:** expect 24-72 hour response time on email.

### Site visits (in-person, infrequent)

- Wes visits PY ~4-6 times per year (2 weeks each)
- Ivan visits NL ~2 times per year (1 week each, for Wes sync)

## Cadence: what happens in a typical week

| Day | What | Who |
|---|---|---|
| **Mon** | Erebus weekly digest (cron) → Wes reads on Monday morning | Erebus → Wes |
| **Mon–Fri** | Erebus runs research sprints, writes docs, commits | Erebus |
| **Wed** | Ivan sync with Erebus, review commits, prompt direction | Ivan + Erebus |
| **Wed–Fri** | Wes responds to outstanding questions from Erebus | Wes |
| **Fri** | Ivan writes status report, sends to Wes if requested | Ivan |

**Average week:** 3-5 Erebus commits, 1-3 Ivan prompts, 1-2 Wes
audio messages or chat replies.

## What each person does (and doesn't do)

### Wes (you)

✅ **Decides:**
- Project name (W0.6)
- 5-of-15 materials topics (W0.5)
- Fase 1 ownership choice (W0.4)
- Final cabin designs (after AI generates options)
- Pricing, target market, positioning

✅ **Actions only Wes can do:**
- NL+PY attorney call (W0.1)
- Sonja questionnaire call (W0.2)
- Anexo I chase to Escribana (W0.3)
- Major NL investor introductions (via Wes's network)

❌ **Wes does NOT do:**
- Research sprints (Erebus does)
- Repo maintenance (Erebus does)
- Day-to-day project management (Ivan does)
- Construction crew management (Sonja does)
- Tax filings (attorney + accountant does)

### Ivan

✅ **Owns:**
- Repo structure + commit hygiene
- AI prompt engineering + research sprint direction
- Coordination between Wes ↔ Erebus ↔ Kiki
- Legal liaison (when attorney is engaged post-W0.1)
- Weekly status digest

❌ **Ivan does NOT do:**
- Final design decisions (Wes does)
- Construction worker hiring (Sonja does)
- Sales pipeline (Kiki does)
- Major NL investor pitches (Wes + Kiki do)

### Kiki

✅ **Owns:**
- NL+PY accountant / attorney referrals
- NL investor pipeline (Booking.com setup, etc.)
- NL-side marketing materials
- Sales-related contracts

❌ **Kiki does NOT do:**
- Repo docs (Ivan/Erebus do)
- Construction decisions (Wes/Sonja do)
- Tax/legal opinion (attorney does)

### Erebus (AI)

✅ **Owns:**
- Doc organization + commits
- Research sprint execution
- Transcription + audio synthesis
- Initial drafts of decisions / briefs / questionnaires
- Cron jobs (weekly digest, nightly backup, etc.)
- Tool automation (scripts/, .github/workflows/)

❌ **Erebus does NOT do:**
- Final decisions (always asks Wes)
- Outbound communications without Ivan's ✅
- Modify byte-frozen code (renderer at `85e86aa`)
- Push to main without user confirmation

### Sonja (on-the-ground authority per Rule 5)

✅ **Owns:**
- Worker salary bands + hiring recommendations
- PY cultural norms (tereré etiquette, Municipalidad practices, ANDE applications)
- Local construction crew coordination
- On-site reality-checks

❌ **Sonja does NOT do:**
- Repo docs
- NL legal / tax work
- Design decisions (those go through Wes)

## How we handle disagreement

| Type of disagreement | First escalation | If still stuck |
|---|---|---|
| Doc inaccuracy | Tell Erebus, fix in next commit | Mention to Ivan |
| Design choice | Wes ↔ Sonja (Rule 5) | Wes decides |
| Legal interpretation | Attorney (W0.1) | Wes decides based on advice |
| Cost / scope | Ivan ↔ Erebus (research) | Ivan arbitrates |
| Strategic direction | Wes ↔ Ivan | Wes decides |
| Personal style (cadence, format) | Mention in chat, adjust | Ivan arbitrates |

## What NOT to expect

- ❌ Erebus doesn't run 24/7 cron jobs without checking first
- ❌ Ivan doesn't message Wes unprompted (Wes initiates or Erebus prompts)
- ❌ Wes doesn't review every commit (only the major ones; trust Ivan/Erebus to keep small stuff clean)
- ❌ No "weekly meeting" — async by default
- ❌ No formal project management tool (GitHub Issues + the repo is the source of truth)
- ❌ No Slack / Discord / Notion (everything in the repo + Messaging)

## What TO expect

- ✅ **Cadence:** ~3-5 commits per week from Erebus
- ✅ **Response times:** Ivan 4h PY business, Erebus immediate, Wes when he can
- ✅ **Transparency:** every decision logged in `_reconciled/OPEN_DECISIONS.md` or `people/DECISIONS_LOG.md`
- ✅ **Reversibility:** Wes can change his mind; we update the canon docs
- ✅ **Source-of-truth:** the repo > chat > memory > hearsay
- ✅ **One-thing-at-a-time:** each Erebus turn is small; Wes answers one question at a time

---

## Onboarding a new person to this working style

If you (Wes) bring on a new person — investor, partner, family member,
new AI Whisperers hire — point them at:

1. **`docs/WES_INDEX.md`** — what's in the repo, 5-min read
2. **`docs/WES_FAQ.md`** — common questions
3. **`docs/WES_GLOSSARY.md`** — vocabulary
4. **`docs/WES_WARNINGS.md`** — what might surprise them
5. **This doc** — how we work together
6. **`docs/audios/.../final/SYNTHESIS.md`** — the actual vision
7. **`docs/POST_ESCRITURA_NOW.md`** — what's blocking right now
8. **`docs/people/WES_ACTIONS.md`** — the action checklist (Wes's view)

Total: ~45 min read. After that, they can participate meaningfully.

---

*Working agreement as of 2026-07-03. Last revised after the post-escritura
audio synthesis (5 audios, 3h 19m). If something doesn't match your
experience, tell Erebus and we'll update.*