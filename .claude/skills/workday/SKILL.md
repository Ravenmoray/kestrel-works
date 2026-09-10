---
name: workday
description: Run one simulated workday for Kestrel Works — pick a department with useful next work, have its agent persona produce one real deliverable, log it to HISTORY.md and the website, and republish the site. Use when asked to run a company workday, advance the virtual company, simulate a day of work, or keep Kestrel Works' ongoing operations moving.
---

# Workday

Run exactly one workday turn for Kestrel Works, the virtual company rooted in
this repository (`COMPANY.md` has the full charter).

## Steps

1. Delegate the whole turn to the `ops-coordinator` agent persona via the
   Agent tool (`subagent_type: "ops-coordinator"`). Give it this brief:

   > Run one Kestrel Works workday turn per your charter in
   > `departments/operations/CHARTER.md`: read `HISTORY.md` and
   > `departments/product/roadmap/roadmap.md`, pick the department with the
   > most useful next work (rotate fairly across departments — check recent
   > `departments/operations/logs/` entries to see who went last), delegate
   > to that department's persona with a concrete task, verify its output
   > landed on disk, log it in `HISTORY.md` and
   > `website/data/updates.json`, republish the site, and write today's
   > entry in `departments/operations/logs/`. Report back a short summary.

2. When it reports back, relay a concise summary to whoever asked for the
   workday to run: which department worked, what it produced (with file
   path), and confirmation the history/site/log are updated.

## Notes

- This is one turn, one department, one deliverable — not a full simulated
  week. Run it again (or set up a recurring schedule) for more turns.
- If this is the very first workday, there's no "last department" to rotate
  from — Operations should just pick whichever department has the clearest
  next step (usually Research or Product, to seed something the others can
  build on).
- If `roadmap.md` doesn't exist yet, Product's first turn should be to
  create it.
