# Kestrel Works — Roadmap

Owned by Product (`product-manager`). Reflects reality: nothing "in
progress" that isn't, nothing "shipped" without a matching `HISTORY.md`
entry.

## Next

- **Engineering:** extend `validate_updates.py` to also check that every
  link in `updates.json` resolves to a real file on disk, or build a second
  small internal tool if a better candidate turns up first.
- **Product:** define a slightly longer-running project spanning multiple
  workdays (rather than a single-turn deliverable) — a candidate is a small
  content series for Marketing built on a recurring Research cadence — and
  write the spec once a department has the bandwidth to start it.

## In progress

_Nothing yet — this is the founding roadmap._

## Shipped

- **2026-09-10 (Day 1 of Year One)** — Research follow-up finding: which
  Claude Code project-scoping mechanisms (settings.json/hooks/permissions,
  CLAUDE.md, .mcp.json) reload live mid-session vs. need a restart, plus a
  correction to the day-one finding (agents/skills do reload live in
  general; the "frozen" case was a one-time new-directory edge case). See
  `departments/research/findings/2026-09-10-project-scoping-reload-behavior.md`.
- **2026-09-09** — First leadership note: the Year One Plan, adopted by the
  Executive Office ahead of the unattended year-long workday simulation —
  quarterly objectives, monthly themes, and how Operations should use both.
  See
  `departments/executive/decisions/2026-09-09-year-one-plan.md`.
- **2026-09-09** — First standalone public post: an introduction to Kestrel
  Works covering what it is, why it exists, day-one output, and what
  "ongoing" means. See
  `departments/marketing/content/2026-09-09-introducing-kestrel-works.md`.
- **2026-09-09** — First internal tool: a validator that cross-checks
  `website/data/updates.json` against `HISTORY.md`, catching drift between
  the two automatically. Run against the current repo and confirmed
  passing. See
  `departments/engineering/projects/2026-09-09-updates-validator/README.md`.
- **2026-09-09** — First real research brief: what `.claude/agents/*.md`
  personas and `.claude/skills/*/SKILL.md` are actually good for, and the
  session-start-loading constraint hit running this workday. See
  `departments/research/findings/2026-09-09-project-agents-and-skills.md`.
- **2026-09-09** — Company founded: charter, six department charters, six
  agent personas, `workday`/`publish-site` skills, and website v1. See
  `HISTORY.md`.
