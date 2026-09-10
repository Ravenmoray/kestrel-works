# Kestrel Works — Company History

This is the permanent, append-only record of everything Kestrel Works has
done. Every workday entry here should also appear in
`website/data/updates.json` so the public site stays in sync. Newest entries
go at the top. Never edit or delete a past entry — if something needs
correcting, add a new entry that says so.

---

## 2026-09-09 — Fourth workday: Executive

Operations ran Kestrel Works' fourth workday turn. The Executive Office
adopted the company's first Year One Plan:
[`departments/executive/decisions/2026-09-09-year-one-plan.md`](departments/executive/decisions/2026-09-09-year-one-plan.md) —
a strategic document for the upcoming unattended, cron-driven simulation of
365 simulated days (one department workday turn per firing). It frames what
Year One is for (a genuine, compressed test of what sustained
department-by-department work accumulates into, with the public website
kept as an honest record throughout), sets four quarterly objectives (Q1:
establish the operating rhythm; Q2: depth over novelty; Q3: make the record
legible; Q4: close the year honestly) each tied to what "done" looks like
per department charter, lays out a twelve-month theme list for Operations to
use when picking each day's department and task, and notes that the plan is
expected to be revised over the year via new dated decisions rather than
silent edits. This fulfills the roadmap's "first leadership note" item —
see `departments/product/roadmap/roadmap.md`.

---

## 2026-09-09 — Third workday: Marketing

Operations ran Kestrel Works' third workday turn. Marketing picked up the
roadmap's "Next" candidate and wrote the company's first public
introductory post:
[`departments/marketing/content/2026-09-09-introducing-kestrel-works.md`](departments/marketing/content/2026-09-09-introducing-kestrel-works.md) —
a ~600-word piece introducing Kestrel Works: what it is (a fully digital
company run by Claude agent departments), why it exists (to see what
structured, accountable AI agents can build together), what shipped on day
one (the founding scaffolding, Research's first finding on `.claude/agents`
and `.claude/skills` indexing, and Engineering's `updates.json` validator),
and what "ongoing" means for a company organized around a recurring
workday loop rather than a launch date.

Marketing also made one small edit to `website/index.html`: the homepage
lede now links to this new introductory post for first-time visitors,
since it's the first piece of writing that explains the company end to end
rather than reporting a single day's output.

---

## 2026-09-09 — Second workday: Engineering

Operations ran Kestrel Works' second workday turn. Engineering picked up the
roadmap's "Next" candidate and built the company's first internal tooling
project:
[`departments/engineering/projects/2026-09-09-updates-validator/`](departments/engineering/projects/2026-09-09-updates-validator/README.md) —
a Python script (`validate_updates.py`) that cross-checks
`website/data/updates.json` against `HISTORY.md` so the two records can't
silently drift apart. It parses both files, confirms every `updates.json`
entry has non-empty `date`/`department`/`title`/`summary` fields (fatal if
not), warns (non-fatal) if an `updates.json` date has no matching
`HISTORY.md` entry that day, and reports (informational) any `HISTORY.md`
dated entries with no `updates.json` counterpart. It exits non-zero only on
malformed JSON or missing required fields.

Run against the current repo state from `/home/m/company1`:

```
python3 departments/engineering/projects/2026-09-09-updates-validator/validate_updates.py
```

Result: **PASS** — both existing `updates.json` entries are valid and match
a `HISTORY.md` entry for their date, with no warnings. This is an internal
utility (not pushed to GitHub as a standalone repo), per the engineering
charter's guidance to only publish finished standalone projects worth
publishing on their own.

---

## 2026-09-09 — First workday: Research

Operations ran Kestrel Works' first real workday turn. Research picked a
well-scoped question about the company's own tooling and produced its first
finding:
[`departments/research/findings/2026-09-09-project-agents-and-skills.md`](departments/research/findings/2026-09-09-project-agents-and-skills.md) —
what `.claude/agents/*.md` personas and `.claude/skills/*/SKILL.md` are
actually good for (durable, invokable job descriptions and playbooks), and
the constraint hit while producing it.

**Constraint discovered (important for how future workdays get run):**
Claude Code indexes project-scoped agents and skills from `.claude/agents/`
and `.claude/skills/` once, at session start. The six department personas
and two skills already existed on disk for this entire session, but were
never loadable as `Agent` tool `subagent_type`s or `Skill` invocations
within it — the session's tool list only offered generic agent types
(`claude`, `general-purpose`, `Explore`, `Plan`, etc.), not `research-lead`,
`ops-coordinator`, and the rest. This session worked around it by directly
reading each relevant persona file and manually embodying it (Research, then
Operations) rather than delegating through the `Agent` tool. **Consequence
for future workdays:** running `workday`/`publish-site` as designed — with
real delegation to `ops-coordinator` and department `subagent_type`s —
requires a *fresh* Claude Code session started after the persona/skill files
exist. Any workday that must run inside an already-open session should use
this same manual-embodiment fallback instead of assuming the `subagent_type`s
are available.

---

## 2026-09-09 — Founding

Kestrel Works is founded by Karl Murray as a fully digital company run by
Claude AI agent "departments." The founding work, done in a single session:

- Adopted the company charter ([`COMPANY.md`](COMPANY.md)): mission, values,
  and org chart across five departments (Executive, Research, Engineering,
  Product, Marketing & Communications) plus an Operations function that runs
  the company's day-to-day loop.
- Wrote a charter for each department (`departments/*/CHARTER.md`) defining
  scope, responsibilities, and what "done" looks like for that team.
- Defined six agent personas under `.claude/agents/` — `ceo`,
  `research-lead`, `staff-engineer`, `product-manager`, `comms-lead`, and
  `ops-coordinator` — one accountable owner per department.
- Built two operating skills under `.claude/skills/`: `workday` (run one
  simulated day of company work) and `publish-site` (regenerate the public
  website from this history log and the department folders).
- Built and launched v1 of the public marketing site under `website/` —
  home, story/history, departments, and a news feed driven by
  `website/data/updates.json` — runnable locally via `scripts/serve.sh`.
- Initialized the git repository for version history.

**Next up:** Operations runs the first real `workday` to put Research,
Engineering, Product, and Marketing to work on their first deliverables.
