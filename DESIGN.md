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

Two families, opposed jobs. The tension between them *is* the identity: a literary,
reproduction-degraded serif on the wordmark against an unsentimental grotesk on everything
else. Cultural register, commercial delivery.

| Role | Token | Face | File |
|---|---|---|---|
| Display / wordmark | `--display` | Redaction (Kaphar/Betts, MCKL — OFL) | `fonts/Redaction-Regular.woff2` |
| Body / statement | `--sans` | Diatype Variable (Dinamo) | `fonts/Cargo-DiatypePlusVariable.woff2` |
| Technical label | `--mono` | Favorit Mono | `ABCFavoritMono-Light-Trial.otf` |

Redaction is only ever used at weight 400 — the Bold face is not loaded.

`--mono` must resolve to a **real monospace**; the clock's digits depend on it. It once
pointed at a `"Diatype Mono Variable"` alias of the *proportional* body binary, which
shadowed Favorit Mono and made the digits jitter every second. Never alias a proportional
face into the mono role.

Sizes: body and rail nav `.72rem` (they match deliberately) · statement `.95rem`/1.1 ·
h1 `clamp(3.6rem,12vw,11rem)` · clock `.68rem`.

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

- Sticky rail, `280px`, `100vh`: mark → statement → nav → links, switch, clock pinned bottom.
- Main column `max-width:1040px`. First card `padding-top:1.5rem` to sit level with the mark.
- Work index is a **2-up grid** (`gap:3.2rem 2rem`), collapsing to one column under 900px.
- Project rows `1fr 3fr`. Plates locked to `aspect-ratio:16/9`, `border-radius:4px`.
- Rail unpins to a stacked header under 900px.

**Every rule on the page is dotted, on `--sw3`.** Zero solid borders, zero box-shadows.
A dotted border paints roughly half its length, so it reads about half as strong as a solid
rule of the same colour — it needs a far heavier tier than a hairline would. At `--sw5` the
dots were effectively invisible (1.58:1).

## The plate

Behind every cover sits a blurred `scale(1.25)` copy of the same asset — the frost — so
non-16:9 covers never sit on dead space. Covers are `object-fit:contain`, 6% padding,
butted bottom.

**Exception:** native 16:9 compositions take `.fill` (`object-fit:cover`, no padding) and
go edge to edge. SOOT's cover is 1920×1080 and is the only `.fill` user. Check the source
dimensions before assuming a cover should be contained.

`data-smooth` opts a video into `smoothLoop`, which clones it and crossfades the loop seam.
The clone copies `className`, so `.fill` carries across — without that, the two copies would
render at different sizes and the loop would jump. SOOT and Lighthouse use it.

## Motion

One curve: `cubic-bezier(.2,.7,.2,1)`. Entrances only — things arrive and stay; nothing is
scroll-linked. The statement settles up on load, carrying its dotted rule with it. Project
entries ease in once, then unobserve. Plates fade a dotted outline on hover — the outline is
present but `transparent` at rest, because `outline-style` none→dotted is discrete and would
otherwise pop.

Exactly one living element: **a clock that serves no function.** It is proof the page is
running. One dynamic element is charisma; three is a dashboard.

Every animation has a `prefers-reduced-motion` escape.

## Content

Order and copy come from the Seance CMS store (D1 kv `renaise_cms`, served at
`seance.pages.dev/api/renaise-cms`, CORS-scoped to renaise.com). A runtime script reorders
the DOM to match. The authored HTML is the fallback when that fetch fails and **must be kept
in CMS order** — so the script's "already correct" early-return fires and nothing reshuffles
on load. Slugs are immutable (citations + provenance).

Current order: soot · flora · osmosis · industrial-lighting · lighthouse ·
depictions-of-original-sin.

The CMS carries `problem`, `solution`, `impact`, and `process` for every project. The site
renders **only `hook`**. That withholding is deliberate: the case study lives on
studioartifice.com. renaise.com establishes standing and routes to the studio.

Card fields map `name · year · title · role · medium · hook`, with `status` appended to
medium only when it is not `Live`.

## Voice

Title work by its **commercial outcome**, not its craft — "Enterprise Identity Built to Be
Bought", not "A brand for an immigration startup". No em dashes. `+` over "and". The
wordmark is the first name alone.

## Kill-list

No second hue. No filled accent. No solid rule anywhere. No third typeface. No framework,
build step, or CDN. No scroll-linked motion. No adjective that survives deletion. No case
study on this site — route to the studio.

## Open

- `ABCFavoritMono-Light-Trial.otf` is a **trial licence** served publicly from a live
  commercial domain, and the mono role now depends on it. Needs a purchased licence or a
  replacement face.
- `covers/sensitive-subjects.png` is still in the repo but the project is not in the CMS and
  not on the site. Either it returns to the CMS or the asset goes.
- Root `CLAUDE.md` still describes a cream page, Neue Haas Grotesk, and a `#FF2A00` accent.
  None have ever existed in this build.
