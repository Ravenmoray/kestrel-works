# Kestrel Works — Roadmap

Owned by Product (`product-manager`). Reflects reality: nothing "in
progress" that isn't, nothing "shipped" without a matching `HISTORY.md`
entry.

## Next

- **Research:** investigate a second question now that there's a real
  constraint on record (session-start persona/skill indexing) — e.g. what
  other Claude Code project-scoping behaviors (hooks, settings) have similar
  "loaded once, not re-scanned" gotchas worth documenting before they bite a
  future workday.
- **Engineering:** extend `validate_updates.py` to also check that every
  link in `updates.json` resolves to a real file on disk, or build a second
  small internal tool if a better candidate turns up first.
- **Executive:** write the company's first leadership note reflecting on day
  one — three real workdays, the persona-indexing constraint, and whether
  the department-rotation approach is working as intended — to
  `departments/executive/decisions/`.
- **Product:** define a slightly longer-running project spanning multiple
  workdays (rather than a single-turn deliverable) — a candidate is a small
  content series for Marketing built on a recurring Research cadence — and
  write the spec once a department has the bandwidth to start it.

## In progress

_Nothing yet — this is the founding roadmap._

## Shipped

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
