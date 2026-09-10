# Kestrel Works — Company History

This is the permanent, append-only record of everything Kestrel Works has
done. Every workday entry here should also appear in
`website/data/updates.json` so the public site stays in sync. Newest entries
go at the top. Never edit or delete a past entry — if something needs
correcting, add a new entry that says so.

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
