# renaise.com — Design System

Editorial portfolio, Cargo "N690" lineage, re-themed light to sit alongside studioartifice.com.
Single self-contained `index.html` (no build step). Source of truth for all visual decisions.

## Color
| Token | Value | Use |
|---|---|---|
| `--bg1` → `--bg2` | `#171a1f` → `#363b42` | Page background, `linear-gradient(168deg …)`, fixed. Cool dark-to-mid gray. |
| `--ink` | `#f3f5f8` | Headings, wordmark, emphasized text (cool near-white) |
| `--sw1…--sw6` | `rgba(243,245,248, .92 / .76 / .54 / .38 / .24 / .13)` | Text tiers (light on dark) |
| `--accent` | `#FF2A00` | Sparingly: link hover only. Never fills areas. |
| `--tile` | `#0e1013` | Project media tiles |

## Type
Typeface is **Diatype (Dinamo)** — the actual Cargo N690 face, self-hosted 1:1 from `/fonts/`. Deliberately small scale.
- **Body / UI + Statement (`h2`)** — Diatype Variable. Body weight 500 `0.86rem`; statement `1.5rem`, max 24ch, centered.
- **Wordmark (`h1` "Renaise Kim")** — Diatype Compressed Variable, `3.4rem`, weight 700, `font-stretch:59%`.
- **Meta / clock / footer** — Diatype Mono Variable → Favorit Mono (`ABCFavoritMono-Light-Trial.otf`), `0.78rem`.
- Fonts self-hosted in `/fonts/` (Cargo-DiatypePlusVariable.woff2, CargoDiatypeWidthsVariable.woff2) so they load same-origin, no referrer lock. Helvetica Neue is the fallback.

## Scale & layout
- Content column: `max-width: 56%`, left-aligned, centered in viewport. Full-width under 900px.
- Global scale intentionally restrained ("a tad smaller"): wordmark 4.4rem, statement 2rem, body 0.98rem, meta 0.92rem.
- Pinned header (`Renaise®` / About · Index) and footer (Top ↑ / Email · LinkedIn). Live mono clock, top-center.

## Structure (top → bottom)
1. Centered statement (full-viewport).
2. Stacked project entries — media on top, then `[Name · Year]  [Title · Role · Category · dim description]`.
3. CV footer — Information / Recognition / Studios + Roles, under the big wordmark.

## Voice (house rules — non-negotiable)
- **No em dashes.** Use periods, commas, or restructure.
- **`+` over "and"** in positioning lines (culture + venture; Studios + Roles).
- Editorial, precise, quiet. Frame work as the decision made, not the pixels. No strong language unless asked.

## Media gap (open)
Only SOOT and Aputure carry motion; the other 10 are logo marks on dark tiles. Real project stills/video are the highest-leverage next input — this format leads with the image.
