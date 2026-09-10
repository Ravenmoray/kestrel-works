#!/usr/bin/env python3
"""
validate_updates.py — cross-check website/data/updates.json against HISTORY.md

Kestrel Works keeps two records of every workday's output:
  - HISTORY.md              (permanent, append-only, human-readable log)
  - website/data/updates.json (machine-readable feed the public site reads)

They're supposed to stay in sync, but nothing enforces that automatically —
it's easy for one to get updated and not the other. This script checks both
files consistently, without editing either one.

Checks performed:
  1. updates.json must be valid JSON, and a top-level array of objects.
  2. Every updates.json entry must have non-empty date/department/title/
     summary fields. (FATAL if missing/empty — these are required fields.)
  3. Every updates.json entry's date must have at least one matching
     "## YYYY-MM-DD — Title" entry in HISTORY.md for that same date.
     (WARNING, non-fatal, if not — dates drift more easily than content.)
  4. Any HISTORY.md dated entry with no corresponding updates.json entry on
     that date is reported informationally (not an error) — HISTORY.md is
     allowed to record things the public site chooses not to surface.

Exit code is non-zero ONLY for actual malformed JSON or missing/empty
required fields (#1 and #2). Warnings and info notes (#3 and #4) are
reported but do not fail the run.

Usage (from repo root):
    python3 departments/engineering/projects/2026-09-09-updates-validator/validate_updates.py

Optional arguments let it be pointed at a different checkout:
    python3 validate_updates.py [path/to/repo/root]
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

REQUIRED_FIELDS = ("date", "department", "title", "summary")
HISTORY_HEADER_RE = re.compile(
    r"^##\s+(\d{4}-\d{2}-\d{2})\s+—\s+(.+?)\s*$", re.MULTILINE
)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class ValidationError(Exception):
    """Raised for fatal problems: malformed JSON or missing required fields."""


def load_updates(updates_path: Path) -> list[dict]:
    if not updates_path.exists():
        raise ValidationError(f"updates.json not found at {updates_path}")

    raw = updates_path.read_text(encoding="utf-8")
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ValidationError(f"updates.json is not valid JSON: {exc}") from exc

    if not isinstance(data, list):
        raise ValidationError(
            f"updates.json must be a JSON array at the top level, got {type(data).__name__}"
        )

    for i, entry in enumerate(data):
        if not isinstance(entry, dict):
            raise ValidationError(f"updates.json entry #{i} is not a JSON object")

    return data


def check_required_fields(entries: list[dict]) -> list[str]:
    """Returns nothing on success; raises ValidationError on the first
    missing/empty required field found (fatal, per spec)."""
    problems = []
    for i, entry in enumerate(entries):
        label = entry.get("title") or f"entry #{i}"
        for field in REQUIRED_FIELDS:
            value = entry.get(field)
            if not isinstance(value, str) or not value.strip():
                problems.append(
                    f"updates.json entry #{i} ({label!r}) is missing or has an "
                    f"empty required field: {field!r}"
                )
    return problems


def load_history_dates(history_path: Path) -> dict[str, list[str]]:
    """Returns {date: [titles...]} for every '## YYYY-MM-DD — Title' header
    found in HISTORY.md."""
    if not history_path.exists():
        raise ValidationError(f"HISTORY.md not found at {history_path}")

    text = history_path.read_text(encoding="utf-8")
    by_date: dict[str, list[str]] = {}
    for match in HISTORY_HEADER_RE.finditer(text):
        date, title = match.group(1), match.group(2)
        by_date.setdefault(date, []).append(title)
    return by_date


def main(argv: list[str]) -> int:
    repo_root = Path(argv[1]).resolve() if len(argv) > 1 else Path.cwd()

    updates_path = repo_root / "website" / "data" / "updates.json"
    history_path = repo_root / "HISTORY.md"

    warnings: list[str] = []
    infos: list[str] = []

    try:
        entries = load_updates(updates_path)
        field_problems = check_required_fields(entries)
        if field_problems:
            raise ValidationError(
                "Required-field validation failed:\n  - " + "\n  - ".join(field_problems)
            )

        history_dates = load_history_dates(history_path)

        updates_dates = set()
        for i, entry in enumerate(entries):
            date = entry["date"].strip()
            if not DATE_RE.match(date):
                warnings.append(
                    f"updates.json entry #{i} ({entry.get('title')!r}) has a date "
                    f"that doesn't look like YYYY-MM-DD: {date!r}"
                )
                continue
            updates_dates.add(date)
            if date not in history_dates:
                warnings.append(
                    f"updates.json entry #{i} ({entry.get('title')!r}) has date "
                    f"{date} with no matching HISTORY.md '## {date} — ...' entry"
                )

        history_only = sorted(set(history_dates) - updates_dates)
        for date in history_only:
            for title in history_dates[date]:
                infos.append(
                    f"HISTORY.md has '## {date} — {title}' with no updates.json "
                    f"entry on that date (informational; not required to match)"
                )

    except ValidationError as exc:
        print("FAIL: updates.json validation failed.\n")
        print(str(exc))
        return 1

    # --- Summary ---
    print(f"Checked {len(entries)} updates.json entries against "
          f"{sum(len(v) for v in history_dates.values())} HISTORY.md dated entries.\n")

    if infos:
        print(f"INFO ({len(infos)}):")
        for msg in infos:
            print(f"  - {msg}")
        print()

    if warnings:
        print(f"WARNING ({len(warnings)}, non-fatal):")
        for msg in warnings:
            print(f"  - {msg}")
        print()
        print("PASS (with warnings): required fields are all present and "
              "updates.json is valid JSON. See warnings above for date drift.")
    else:
        print("PASS: updates.json is valid, all required fields present, and "
              "every entry's date matches a HISTORY.md entry.")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
