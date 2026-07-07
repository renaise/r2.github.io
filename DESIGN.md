# renaise.com — Design System

Editorial portfolio, Cargo "N690" lineage, re-themed light to sit alongside studioartifice.com.
Single self-contained `index.html` (no build step). Source of truth for all visual decisions.

## Color
| Token | Value | Use |
|---|---|---|
| `--bg1` → `--bg2` | `#1b1a18` → `#3b3835` | Page background, `linear-gradient(168deg …)`, fixed. Neutral stone gray, dark to mid. |
| `--ink` | `#d6d4d0` | Headings, wordmark, emphasized text (light gray — all type is light gray) |
| `--sw1…--sw6` | `rgba(214,212,208, .95 / .82 / .60 / .45 / .30 / .16)` | Text tiers, light-gray base |
| `--accent` | `#ffffff` | Highlight: white on hover (title + media outline). Never fills areas. |
| `--tile` | `#100f0e` | Project media tiles |

Hero (`.statement`) is `min-height: 52vh` so the first case-study video reveals in the fold — work leads, not the statement.

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
1. Centered statement (full-viewport), reveal animation on load (fade + rise + deblur).
2. Work — the six live Studio Artifice case studies (No. 001–006), each an `<a>` linking to
   `studioartifice.com/work/<slug>/`, leading with the real cover video from
   `studioartifice.com/stage/<slug>/cover.mp4` (sensitive-subjects uses cover.png). Media is
   pulled hot from studioartifice.com (not copied). Hover = accent outline on media + accent title.
3. CV footer — Information / Recognition / Studios + Roles, under the Redaction wordmark.

## Wordmark
`h1` "Renaise Kim" is **Redaction** (Kaphar/Betts, MCKL, OFL), self-hosted from `/fonts/`, serif, 3.6rem/400.

## Voice (house rules — non-negotiable)
- **No em dashes.** Use periods, commas, or restructure.
- **`+` over "and"** in positioning lines (culture + venture; Studios + Roles).
- Editorial, precise, quiet. Frame work as the decision made, not the pixels. No strong language unless asked.

## Media gap (open)
Only SOOT and Aputure carry motion; the other 10 are logo marks on dark tiles. Real project stills/video are the highest-leverage next input — this format leads with the image.
