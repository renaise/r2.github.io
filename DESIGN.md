# renaise.com — Design System

Editorial portfolio, Cargo "N690" lineage, re-themed light to sit alongside studioartifice.com.
Single self-contained `index.html` (no build step). Source of truth for all visual decisions.

## Color
| Token | Value | Use |
|---|---|---|
| `--bg1` → `--bg2` | `#fcfaf5` → `#f2ebdd` | Page background, `linear-gradient(168deg …)`, fixed. Matches studioartifice.com cream. |
| `--ink` | `#151310` | Headings, wordmark, emphasized text |
| `--sw1…--sw6` | `rgba(21,19,16, .92 / .78 / .56 / .40 / .26 / .13)` | Text tiers (ink on cream, not white on dark) |
| `--accent` | `#FF2A00` | Sparingly: marquee separators, link hover. Never fills areas. |
| `--tile` | `#141310` | Project media tiles (dark tiles on cream is deliberate) |

## Type
- **Body / UI** — Neue Haas Grotesk (Display Pro → Neue Haas Grotesk → Helvetica Neue). Weight 500, `0.98rem`, line-height 1.12.
- **Wordmark (`h1` "Renaise Kim")** — Helvetica Now Display → Helvetica Neue. `4.4rem`, weight 700, tight `-0.035em`.
- **Statement (`h2`)** — Neue Haas Grotesk, `2.0rem`, max 24ch, centered.
- **Meta / clock / marquee / footer** — Favorit Mono (`ABCFavoritMono-Light-Trial.otf`, self-hosted), uppercase, `0.92rem`.
- Licensing: NHG and Helvetica Now Display are licensed (Monotype); without the webfonts they render as Helvetica Neue, the same design lineage. Drop licensed webfonts into `/fonts/` and add `@font-face` to make them exact. (Diatype was trialed and removed.)

## Scale & layout
- Content column: `max-width: 56%`, left-aligned, centered in viewport. Full-width under 900px.
- Global scale intentionally restrained ("a tad smaller"): wordmark 4.4rem, statement 2rem, body 0.98rem, meta 0.92rem.
- Pinned header (`Renaise®` / About · Index) and footer (Top ↑ / Email · LinkedIn). Live mono clock, top-center.

## Structure (top → bottom)
1. Centered statement + marquee (phrases sourced from studioartifice.com: Strategic Visual Studio / Narrative-Sensitive Brands / Strategy / Identity / Design / Production / Worldsite Pipeline / New York).
2. Stacked project entries — media on top, then `[Name · Year]  [Title · Role · Category · dim description]`.
3. CV footer — Information / Recognition / Studios + Roles, under the big wordmark.

## Voice (house rules — non-negotiable)
- **No em dashes.** Use periods, commas, or restructure.
- **`+` over "and"** in positioning lines (culture + venture; Studios + Roles).
- Editorial, precise, quiet. Frame work as the decision made, not the pixels. No strong language unless asked.

## Media gap (open)
Only SOOT and Aputure carry motion; the other 10 are logo marks on dark tiles. Real project stills/video are the highest-leverage next input — this format leads with the image.
