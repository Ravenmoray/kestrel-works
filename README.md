# Kestrel Works

A digital company, built and run by AI — see [`COMPANY.md`](COMPANY.md) for
the charter and [`HISTORY.md`](HISTORY.md) for the full record of what's
been built.

## Quick start

```
./scripts/serve.sh                # serve the website locally
```
Open http://localhost:8765/website/

## Run a workday

From a Claude Code session in this directory:

```
/workday
```

This delegates to the Operations department, which picks a department, has
it produce one real deliverable, and logs it to `HISTORY.md` and the
website. See [`.claude/skills/workday/SKILL.md`](.claude/skills/workday/SKILL.md).

## Layout

- `COMPANY.md` — charter, mission, org chart
- `HISTORY.md` — permanent, append-only record of everything shipped
- `departments/` — one folder per department: a `CHARTER.md` plus its work
- `.claude/agents/` — the six department agent personas
- `.claude/skills/` — `workday` (run one turn) and `publish-site` (sync the
  website with `HISTORY.md`)
- `website/` — the local marketing site (static HTML/CSS/JS, no build step)
- `scripts/` — operating scripts (`serve.sh` runs the site)
