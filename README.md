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

## Year One simulation (unattended, persistent)

A crontab entry (`*/15 * * * * scripts/simulate-day.sh`) runs one simulated
day every ~15 minutes, headlessly (`claude -p --dangerously-skip-permissions`
— no human is present to answer permission prompts, per explicit sign-off).
Each simulated day advances `departments/operations/state/sim-clock.json`,
has one department (rotating) produce one real deliverable guided by the
[Year One Plan](departments/executive/decisions/2026-09-09-year-one-plan.md),
logs it, and pushes to GitHub. The homepage shows live progress.

It stops itself (removes its own crontab entry) when it finishes all 365
simulated days, or when a run fails or shows usage/rate-limit signals —
see `scripts/simulate-day.sh`. Logs land in `scripts/logs/` (gitignored,
local only).

**To check on it:** `crontab -l` (present = still running), or read
`departments/operations/state/sim-clock.json`.
**To stop it:** `crontab -l | grep -v simulate-day.sh | crontab -`, or
`touch departments/operations/state/simulation.stopped`.
**To resume after a stop:** fix whatever caused it, edit
`sim-clock.json` back to `"status": "running"`, remove
`departments/operations/state/simulation.stopped` if present, and
re-install the crontab line above.

## Layout

- `COMPANY.md` — charter, mission, org chart
- `HISTORY.md` — permanent, append-only record of everything shipped
- `departments/` — one folder per department: a `CHARTER.md` plus its work
- `.claude/agents/` — the six department agent personas
- `.claude/skills/` — `workday` (run one turn) and `publish-site` (sync the
  website with `HISTORY.md`)
- `website/` — the local marketing site (static HTML/CSS/JS, no build step)
- `scripts/` — operating scripts (`serve.sh` runs the site)
