# Kestrel Works — website

The public-facing marketing site for Kestrel Works. Static HTML/CSS/vanilla
JS, no build step, no external dependencies — it fetches its content live
from the company's own records (`HISTORY.md`, `departments/*/CHARTER.md`,
`data/updates.json`) so the site can never drift far from reality.

## Run it

From the project root:

```
./scripts/serve.sh
```

Then open http://localhost:8765/website/

It must be served over HTTP (not opened as a `file://` URL) because the
pages `fetch()` other files in the repo — Chrome blocks that under `file://`.

## Structure

- `index.html` — home page, latest updates
- `story.html` — renders `HISTORY.md` live
- `departments.html` — renders each department's `CHARTER.md` live
- `updates.html` — full update feed from `data/updates.json`
- `data/updates.json` — the update feed; Operations appends to this after
  every workday (see `.claude/skills/publish-site`)
- `css/style.css`, `js/site.js` — shared styling and the tiny markdown
  renderer used to display `.md` files without a build step

## Ownership

Marketing owns the copy and the content of `data/updates.json`. Engineering
owns the HTML/CSS/JS structure. See `departments/marketing/CHARTER.md` and
`departments/engineering/CHARTER.md`.
