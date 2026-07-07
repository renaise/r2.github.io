# renaise.com — repo instructions (system prompt)

This repo (`renaise/r2.github.io`) **is** the live renaise.com. GitHub Pages serves it from `main`
via the `CNAME` (renaise.com). **A push to `main` publishes to the live domain** — treat every push
as a production deploy: confirm before pushing outward-facing changes, and verify after.

## What's here
- `index.html` — the whole site. Self-contained, no build step. Hand-edit + push.
- `DESIGN.md` — the design system. Read it before any visual change; keep it in sync.
- `assets/projects/` — project marks/imagery referenced by root-absolute paths (`/assets/projects/…`).
- `fonts/` + `ABCFavoritMono-Light-Trial.otf` — self-hosted webfonts.
- `CNAME` — `renaise.com`. Never delete it.

## Design & voice
Follow `DESIGN.md` exactly (cream gradient, Neue Haas Grotesk body, Helvetica Now Display wordmark,
Favorit Mono meta, `#FF2A00` accent used sparingly). Copy rules: **no em dashes**, `+` over "and",
quiet editorial register. Marquee phrases are sourced from studioartifice.com.

## Deploy
```bash
git add -A && git commit -m "…" && git push origin main   # = live renaise.com in ~1 min
```
Then verify: `curl -sL https://renaise.com | grep …`. Roll back with a revert commit, not a re-upload.

## Not this repo
The Astro project at `renaise/renaise.github.io` was an earlier "Showroom" direction and is **superseded**
by this editorial build for the live domain. Don't edit it expecting renaise.com to change.
The 100k gag page now lives at renaise.pages.dev.
