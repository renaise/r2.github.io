# renaise.com — design system

Editorial CV. One hand-authored `index.html`. No build step, no framework, no CDN.
This file describes what is actually in the build. If they disagree, the build wins — fix
this file.

## Positioning

One sentence, and it is the whole site:

> Renaise is a brand and product designer in New York, working across culture and venture:
> consumer media, creative tools, and deep tech.

No adjectives of quality. If a line could sit on any designer's site, it does not belong here.

## Type

**Diatype carries the interface** — body, nav, labels, years, the clock. Times sets running
copy. Newsreader sets the wordmark alone. There is no mono role.

| Role | Token | Face | File |
|---|---|---|---|
| Everything | `--sans` | Diatype Variable (Dinamo) | `fonts/Cargo-DiatypePlusVariable.woff2` |
| Wordmark only | `--display` | Newsreader Variable (OFL) | `fonts/Newsreader-Variable.woff2` |
| Running copy | `--serif` | Times New Roman | system, no request |

**Redaction is no longer loaded.** The wordmark ran in Times until 2026-08-26, when it moved
to Newsreader at **weight 300** with `letter-spacing:-.042em`. Times ships Regular and Bold
only, so a lighter wordmark was impossible in it: `font-weight` had nowhere to go. Newsreader
carries 200–800 and was already sitting in `fonts/`, referenced by nothing.

The two hand-kerned pairs on the wordmark (`.k-re`, `.k-ai`) are now **zero**. They were
tuned against Times; Newsreader carries its own kern tables and the hand values fought it.

Diatype's default figures are **proportional** (ten distinct advances), so anything showing
numbers that change in place needs `font-variant-numeric:tabular-nums` or it jitters. The
clock and the CV years set it. This is the constraint the old mono role used to absorb.

Sizes: body `.72rem` · statement `.95rem`/1.1 · h1 `clamp(3.6rem,12vw,11rem)` ·
clock `.68rem` · **rail links `1.44rem`** (doubled 2026-08-26, two columns, the trailing
arrow held in flow at `opacity:0` and revealed on hover so nothing reflows under the pointer).

## Color

One ink, three alphas, flat page. **No brand hue exists.** A fourth colour means a
hierarchy problem.

| Token | Light | Dark |
|---|---|---|
| `--ink` | `#5c5c5c` | `#a8a8a8` |
| `--sw2` — body, nav (α .90) | renders `#6a6a6a` · 4.54:1 | 6.19:1 |
| `--sw3` — labels, **every rule** (α .72) | renders `#848484` · 3.14:1 | 4.41:1 |
| `--sw4` — descriptions, h1, clock (α .58) | 2.36:1 | — |
| `--accent` | `#2e2e2e` | `#ffffff` |
| `--bg1` | `#ebebeb` | `#1a1a1a` |
| `--tile` | `#100f0e` | `#100f0e` — **dark in both** |

Accent is hover and outlines only — **never fill an area with it.** `--tile` backs the
project plates, whose covers are composed for a dark ground, so it does not invert.

Light mode has no headroom: body sits at 4.54:1 against a 4.5 floor. A lighter page or
lighter type drops it below AA. The only way to lift the scale is to darken `--ink`.
`--sw4` (2.36:1) is knowingly sub-AA — recessive by design, the h1 included.

Theme resolves in a `<head>` script before first paint and always writes an explicit
`data-theme`, so the switch knob can never disagree with the page. No stored choice follows
the OS; choosing opts out permanently. Without JS the switch is hidden and
`prefers-color-scheme` still applies.

## Layout

- Sticky rail, `280px`, `100vh`: mark → statement → **search** → marquee → donate → links,
  switch, clock pinned bottom. Rail children sit on a `1.25rem` gap (was `1.9rem`).
- **Search** filters the work grid and nothing else on the page. It reports a count, offers a
  clear control, answers Escape, and renders "Nothing matches that." at zero results, because
  a grid that silently empties reads as broken. Matches are wrapped in `<mark>`, which is
  accent **ink only** — never a fill. Hidden without JS.
- **Rules meet the rail.** Every horizontal divider used to stop at x=302.4 while the rail's
  vertical rule sat at x=280, one gutter short. `.card` and `.cv .sec` now reach back over the
  gutter with a negative margin and put the content back with matching padding; `.side .foot`
  does the same rightward. Reset at the mobile breakpoint, where the rail has no vertical rule.
- Case study pages (`/work/<slug>/`) carry a breadcrumb: Renaise / Work / <name>, separator
  generated in CSS so it never trails the last item.
- Main column `max-width:1040px`. First card `padding-top:1.5rem` to sit level with the mark.
- Work index is a **2-up grid** (`gap:3.2rem 2rem`), collapsing to one column under 900px.
- Project rows `1fr 3fr`. Plates locked to `aspect-ratio:16/9`, `border-radius:4px`.
- Rail unpins to a stacked header under 900px.

**Every rule on the page is a 1px dotted border on `--line`.** Zero solid borders, zero
box-shadows. Straight rules and curves alike — the switch track, the plate hover outline and
the page dividers all render with the same UA dot algorithm, which is what makes them read as
one family.

Corrected 2026-08-31: this section used to describe a repeating radial-gradient painted from
a `--rule` token, chosen so the dot pitch could be spaced to 7px. **No such token exists and
`index.html` contains zero `radial-gradient`.** The build has always used dotted borders on
`--line`; the pitch is the browser's and cannot be spaced. That is the trade.

## The plate

Behind every cover sits a blurred `scale(1.25)` copy of the same asset — the frost — so
non-16:9 covers never sit on dead space. Covers are `object-fit:contain`, 6% padding,
butted bottom.

**As of 2026-08-25 every cover is `.fill`** (`object-fit:cover`, no padding), edge to edge,
and every cover is a 5.000s video recorded or cut to close its own loop. The contained
treatment and its frost remain in the CSS for any future non-16:9 asset, but nothing uses
them. Check source dimensions before assuming a cover should be contained.

`data-smooth` opts a video into `smoothLoop`, which clones it and crossfades the loop seam.
**No card uses it any more.** It existed to hide hard cuts and white re-buffer frames in
covers that could not close their own loops; on a seamless clip it adds an unnecessary jump
to the clip midpoint and plays the whole thing at 0.7x. The function stays for assets that
need it.

## Motion

One curve: `cubic-bezier(.2,.7,.2,1)`. Entrances only — things arrive and stay; nothing is
scroll-linked. The statement settles up on load, carrying its dotted rule with it. Project
entries ease in once, then unobserve. Plates fade a dotted outline on hover — the outline is
present but `transparent` at rest, because `outline-style` none→dotted is discrete and would
otherwise pop.

The marquee runs `110s` (was `64s`).

Exactly one living element: **a clock that serves no function.** It is proof the page is
running. One dynamic element is charisma; three is a dashboard.

Every animation has a `prefers-reduced-motion` escape.

## Content

Order and copy come from the Seance CMS store (D1 kv `renaise_cms`, served at
`seance.pages.dev/api/renaise-cms`, CORS-scoped to renaise.com). A runtime script reorders
the DOM to match. The authored HTML is the fallback when that fetch fails and **must be kept
in CMS order** — so the script's "already correct" early-return fires and nothing reshuffles
on load. Slugs are immutable (citations + provenance).

Authored order as of 2026-08-31: idler · artifactory · soot · the-artifact-index · osmosis ·
industrial-lighting · lighthouse · depictions-of-original-sin · artifice-brand ·
studio-artifice. Ten cards. `flora` and `sensitive-subjects` are not on the site.

The CMS carries `problem`, `solution`, `impact`, and `process` for every project. The card
renders **only `hook`**. The card is still a hook rather than a summary, but the withholding
no longer routes offsite: **case studies live here now**, at `/work/<slug>/`, per Renaise
2026-08-25 and the model in `CMS.md`. SOOT is the first. Cards for projects with a page here
link to it; the rest still link out.

Card fields map `name · year · title · role · medium · hook`, with `status` appended to
medium only when it is not `Live`.

## Voice

Title work by its **commercial outcome**, not its craft — "Enterprise Identity Built to Be
Bought", not "A brand for an immigration startup". No em dashes. `+` over "and". The
wordmark is the first name alone.

## Kill-list

No second hue. No filled accent. No solid rule anywhere. **No second typeface** — Diatype
carries everything, Redaction is the wordmark alone. No `dotted` border on a straight rule
(pitch is unspaceable — use `--rule`). No framework, build step, or CDN. No scroll-linked
motion. No adjective that survives deletion.

Struck 2026-08-25: *"No case study on this site — route to the studio."* Reversed by
Renaise. Case studies live here now, at `/work/<slug>/`.

## Open

- The trial mono is gone — that path now 404s. Item closed 2026-08-31.
- **`covers/` is 9.5MB of dead weight.** All six PNGs (flora, industrial-lighting, lighthouse,
  osmosis, sensitive-subjects, soot) are referenced by nothing; `stage/<slug>/cover.jpg`
  superseded them. Served publicly on every deploy.
- **Five of the seven font files are unreferenced**: both Diatype Widths variables, Diatype
  Italic, and Redaction Regular + Bold. The Diatype files are licensed commercial faces being
  served publicly for no reason. Worth pruning; kept for now because deleting licensed
  originals is Renaise's call, not mine.
- Root `CLAUDE.md` still describes a cream page, Neue Haas Grotesk, and a `#FF2A00` accent.
  None have ever existed in this build.
