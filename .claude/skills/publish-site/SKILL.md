---
name: publish-site
description: Regenerate/verify Kestrel Works' local marketing website so it matches HISTORY.md and department output — sync website/data/updates.json, check page copy for stale or placeholder claims, and confirm the site still runs. Use after a workday lands new work, or whenever asked to update, refresh, or publish the company website.
---

# Publish site

Bring `website/` back in sync with the source of truth (`HISTORY.md` and the
`departments/*/` folders). This is Marketing/Engineering's shared
responsibility — Marketing owns the words, Engineering owns the markup.

## Steps

1. Read the most recent entries in `HISTORY.md` that aren't yet reflected in
   `website/data/updates.json` (compare dates/titles).
2. For each missing entry, append an object to the JSON array in
   `website/data/updates.json` with the same shape as existing entries:
   `{ "date": "YYYY-MM-DD", "department": "...", "title": "...",
   "summary": "...", "link": "..." }`. `link` should point to the real file
   the work lives in (relative path into the repo, or a GitHub URL for
   Engineering projects), or be `null` if there isn't a single file to point
   to. Keep the array sorted newest-first.
3. Skim `website/index.html`, `website/story.html`, and
   `website/departments.html` for any claim that no longer matches reality
   (stale counts, placeholder text) and fix it directly.
4. Verify the site actually runs: start it with `./scripts/serve.sh` (or
   confirm it's already running), fetch `http://localhost:8765/` and
   `http://localhost:8765/data/updates.json` to confirm they respond, then
   stop the server if you started it just for this check.
5. Report what changed — new update entries added, any copy fixed.

## Notes

- Never write a claim to the site that isn't backed by something real in
  `HISTORY.md` or a department folder — no placeholder content in
  production.
- Don't restructure pages here; structural/markup changes are Engineering's
  job (delegate to `staff-engineer` if one is needed).
