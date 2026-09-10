# Kestrel Works

**A digital company, built and run by AI.**

## What this is

Kestrel Works is a virtual company. Every department is a Claude agent persona,
every meeting is a prompt, and every product is a digital artifact — a research
brief, a small tool, an essay, a dataset. Nothing physical is made and nothing
is sold. The company exists to explore what a small team of autonomous AI
agents can build together when they're organized like a real organization:
with a charter, departments, a history, and a public face.

The human founder (Karl Murray) set the company in motion and owns the
outcome. Day-to-day work — research, writing, small engineering projects,
comms — is carried out by department agents defined in `.claude/agents/`,
coordinated through skills in `.claude/skills/`, and logged permanently in
[`HISTORY.md`](HISTORY.md).

## Mission

Simulate a working company end-to-end — strategy, research, building,
shipping, and telling the story of the work — using nothing but Claude agents,
skills, and scheduled loops. Do it transparently: every decision and every
output is written down where the public-facing website can show it.

## Values

- **Ship small, ship often.** A one-page research brief shipped today beats a
  perfect report shipped never.
- **Write it down.** If it isn't in `HISTORY.md` or a department log, it
  didn't happen. The website only ever shows what's on record.
- **Departments own their lane.** Each department has a charter and a single
  agent persona accountable for it; departments don't reach into each other's
  files.
- **Digital only.** Everything Kestrel Works makes is a file: markdown,
  code, data, or prose. Code goes to GitHub; everything else lives in this
  repo.

## Org chart

```
                    ┌─────────────────────┐
                    │   Executive Office   │
                    │   (agent: ceo)       │
                    └──────────┬──────────┘
                               │
        ┌───────────┬─────────┼─────────┬───────────┐
        │            │                    │           │
  ┌─────▼─────┐┌─────▼─────┐      ┌───────▼──────┐┌───▼────────┐
  │  Research  ││ Engineering│      │   Product    ││ Marketing &│
  │ (research- ││  (staff-   │      │  (product-   ││ Comms      │
  │   lead)    ││  engineer) │      │   manager)   ││(comms-lead)│
  └────────────┘└────────────┘      └──────────────┘└────────────┘
                               │
                     ┌─────────▼─────────┐
                     │    Operations      │
                     │ (ops-coordinator)  │
                     │ runs the workday   │
                     │ loop, keeps the    │
                     │ site + history in  │
                     │ sync               │
                     └────────────────────┘
```

See each department's `CHARTER.md` under `departments/<name>/` for scope and
current responsibilities:

- [`departments/executive/CHARTER.md`](departments/executive/CHARTER.md)
- [`departments/research/CHARTER.md`](departments/research/CHARTER.md)
- [`departments/engineering/CHARTER.md`](departments/engineering/CHARTER.md)
- [`departments/product/CHARTER.md`](departments/product/CHARTER.md)
- [`departments/marketing/CHARTER.md`](departments/marketing/CHARTER.md)
- [`departments/operations/CHARTER.md`](departments/operations/CHARTER.md)

## How work happens

1. **Operations runs a "workday"** (`.claude/skills/workday`), on demand or on
   a schedule. It picks a department with open work, hands it to that
   department's agent, and records what came out.
2. **The department agent does one piece of real work** — a brief, a spec, a
   script, a post — and saves it under its own `departments/<name>/` folder.
3. **Operations logs the result** as a dated entry in `HISTORY.md` and in
   `website/data/updates.json`.
4. **Marketing keeps the website current** (`.claude/skills/publish-site`),
   regenerating the news feed and story pages from that same log so the
   public site always reflects what's actually been produced.
5. Code produced by Engineering is pushed to GitHub; everything else stays in
   this repository.

## Running the website locally

```
./scripts/serve.sh
```

Then open http://localhost:8765 — see [`website/README.md`](website/README.md).

## Founding

Founded 2026-09-09 by Karl Murray. See [`HISTORY.md`](HISTORY.md) for the full,
ongoing record.
