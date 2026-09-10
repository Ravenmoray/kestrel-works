# updates.json validator

An internal Engineering script that catches drift between
`HISTORY.md` (the permanent, human-written company record) and
`website/data/updates.json` (the machine-readable feed the public site
reads). Nothing previously enforced that these two stayed in sync — this
closes that gap.

## What it checks

1. `website/data/updates.json` is valid JSON and a top-level array of
   objects. **Fatal** if not.
2. Every entry has non-empty `date`, `department`, `title`, and `summary`
   fields. **Fatal** if any are missing or empty.
3. Every entry's `date` has at least one matching `## YYYY-MM-DD — Title`
   header in `HISTORY.md` for that same date. **Warning, non-fatal** — dates
   are expected to line up, but a mismatch shouldn't block anything, just
   get flagged.
4. Any `HISTORY.md` dated entry with no corresponding `updates.json` entry
   on that date is listed **informationally** — `HISTORY.md` may legitimately
   record things (like this validator's own workday note) that don't need
   their own updates.json row until Operations adds one.

The script never edits either file — it's read-only, safe to run anytime.

## How to run it

From the repo root (`/home/m/company1`):

```bash
python3 departments/engineering/projects/2026-09-09-updates-validator/validate_updates.py
```

Or point it at a different checkout:

```bash
python3 departments/engineering/projects/2026-09-09-updates-validator/validate_updates.py /path/to/other/checkout
```

## Exit codes

- `0` — pass (possibly with non-fatal warnings printed).
- `1` — fail: malformed JSON, or an entry missing a required field. Only
  these two conditions are treated as real errors.

## Why this shape

Date-matching is deliberately a warning rather than a hard failure: the two
files serve different audiences (an append-only internal log vs. a curated
public feed), so a HISTORY.md-only entry is normal and shouldn't break CI or
block a workday. What must never happen is a structurally broken or
incomplete `updates.json` shipping to the public site — those are the only
conditions that exit non-zero.
