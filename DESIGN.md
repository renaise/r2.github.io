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

**The card description recedes until you hover its card** (Renaise 2026-09-10). `--card-body-rest`
is `--card-body`'s alpha at a quarter of it; hover and focus-visible restore the full value.
Colour only, so nothing in the layout moves because a pointer crossed it. Measured: **1.55:1 at
rest and 6.70:1 on hover in dark, 1.44:1 and 6.05:1 in light.** The rest state is far below any
floor and is a deliberate reveal, not an oversight — but it is the hook, the only sentence the
card carries, so if it should be legible without a pointer the alpha is the dial. Without a
pointer there is no reveal, so `@media(hover:none)` never dims it at all.

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

**As of 2026-08-25 every cover is `.fill`** (`object-fit:cover`, no padding), edge to edge.
Most are a video recorded or cut to close its own loop; `lighthouse` and `artifice-brand` are
stills, so check the element before assuming a card has a video to drive. Durations are no
longer all 5.000s: FLORA's is 14.4s.

`the-artifact-index`'s cover was re-recorded on 2026-09-10 off the live
`index.artificenyc.org`. The old clip opened mid-scroll with the intro paragraph sitting over
the masthead, and its copy was two revisions stale — the site now says the Index "documents how
experimental work gets made," not "is the record of work made." Recorded at 1280x720, 150 frames
at 30fps, held at the top, eased down 560px and back, held again: 5.000s that starts and ends on
the same frame (seam diff 0.09 of 255) and whose every frame is a settled composition. The
poster is frame 0. **A cover cut from a live site carries that site's copy; re-shoot it when the
copy moves.**

FLORA's cover changed on 2026-09-10 from Flora's marketing site to the product's own home
screen. It went still for an hour and is a video again, cut from `floragif01.gif` — the same
1296x720 source as the still, frame 0 identical — so the thumbnail moves. 25MB of GIF is 1.4MB
of h264. First and last frames both sit dark (luma 19 and 14), so it closes its own loop. The
contained
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

**`biota` was added last on 2026-09-10 and the store does not carry it.** The reorder script
only applies an order that accounts for every card on the page, so with twelve cards and eleven
rows in the store the guard fires and the **authored order now stands permanently**. That is the
intended fail-safe and it puts BIOTA last, which is where it belongs, but the CMS has stopped
driving order until a `biota` row exists. Add one to hand control back.

The rail's filter counts are authored, not derived: `All 12 · URL 11 · IRL 1`. A thirteenth card
means editing them by hand.

The CMS carries `problem`, `solution`, `impact`, and `process` for every project. The card
renders **only `hook`**. The card is still a hook rather than a summary, but the withholding
no longer routes offsite: **case studies live here now**, at `/work/<slug>/`, per Renaise
2026-08-25 and the model in `CMS.md`. SOOT is the first.

**Marks are lockups, except one.** Every `.cl` mark is a horizontal lockup with the name drawn
into it, which is why `.c0 .nmw:has(.cl) b` hides the set name as redundant. Codex Foundry has
no such file: every asset on disk is a square glyph or a portrait stack whose wordmark would
render about four pixels tall at `1.02em`. So ARTIFACTORY's row carries the glyph *beside* the
name, and `.glyph` on the wrapper opts that one row out of the hide. If a horizontal Codex
lockup is ever drawn, drop the class and the row rejoins the rule.

**Every card opens the case study panel** (2026-09-10). A click transitions the case study in
from the right, and it takes **the right pane entirely**: `left:var(--rail)` to `right:0`, full
height, butted against the rail's own vertical rule. The rail stays; the work grid does not.
It took two corrections the same day — it shipped as a 720px drawer over the grid, went
full-bleed over the rail as well, and landed here. A drawer is a floating card on a grey page;
covering the rail loses the frame. **The seam carries one rule, the rail's own `border-right`.**
The panel drew a second dotted rule a pixel away from it, which read as a double divider. Below 900px the rail unpins into a stacked header and has no
column to sit beside, so the panel takes the width.

Inside, the header and body sit on the index's own 1040px measure, taken off the **pane** and not
the viewport, so the case study is that column arriving in a different frame. Nothing navigates
and nothing on the index moves. It replaces the eight cards that routed to
`studioartifice.com/work/<slug>/`.

**What is revealed is the full case study.** There is no fuller one to page through to, so the
footer never offers one: no "Full case study" link to a `/work/<slug>/` page and no
`studioartifice.com/work/<slug>/` link handing back the offsite trip the panel exists to remove.
The footer carries the live surface and the guidelines, and nothing else — for six of the eleven
it carries nothing, and renders no rule.

`--rail` (280px) is read by the rail and by the panel that meets it. Two hardcoded 280s drift the
first time one of them moves.

**The way out is the breadcrumb**, not a Close control (2026-09-10). It is the same three-item
crumb the `/work/<slug>/` pages carry — `Renaise / Work / <Name>`, separator generated, the
current item not a link — so moving between a panel and a page never changes how you get back.
Renaise closes to the top of the index; Work closes to the grid. Escape still closes.

**Motion: a translation, not a push.** It travelled its own width across the grid, which is a
shove — an opaque block crossing 1160px while the thing underneath sits still. The two states
cross instead. The grid steps `--cs-slide` (28px) left and dissolves out; the case study arrives
from 28px right and dissolves in. **The rail never moves**, so the frame holds while its contents
change. The distance is small on purpose: a translation is legible at 28px, and anything further
starts reading as travel again.

Both opacities run the same window on `linear`, so they always sum to about one — measured at
1.00 across every sampled frame. Staggering them (grid out fast, panel in delayed) left the pane
empty for ~140ms, which reads as a blink; overlapping them at full strength puts two live layers
on screen at once. A symmetric cross-dissolve is the only version with neither. Transform keeps
the site's one curve; only opacity is `linear`, because a cross-dissolve on an eased curve dips.

`--cs-dur` is `.42s`. The body no longer carries its own delayed settle: at 28px the panel is not
travelling far enough for the content to arrive ahead of its frame.

Three defects fixed the same day, all of them things that only show up in motion:

- **One `requestAnimationFrame` is not enough** to guarantee the pre-transition style was
  committed. When it wasn't, the panel snapped straight to its end value with no animation.
  Forced reflow plus a double rAF.
- **`inert` and focus were released the instant close began**, so the index scrolled back under
  a panel still on screen. Both now happen at the end, and every `focus()` passes
  `preventScroll`.
- **The close duration was a second copy of the CSS number.** `transitionend` on the panel's
  `transform` is the truth now, with `--cs-dur` read out of the computed style as the guard for
  the case where no transition fires. A duration written twice is a duration that drifts.

Reopening inside the close cancels both the pending hide and its listener; without that the
stale timeout fires over the panel that just arrived and leaves `cs-open` on a `display:none`
element.

The hrefs stay on the anchors, so the panel is an enhancement: no JS, a middle-click, or any
modified click still goes where the card always went. State is a `#case=<slug>` hash, so a
panel is shareable, Back closes it, and a shared link opens straight into it. `.app` goes
`inert` while it is open — `aria-modal` is a claim, `inert` is the enforcement.

A project may carry `shots`: extra plates that render under the prose, each with its own
`ratio` and caption. A 1508/600 diagram cropped into a 16:9 hole loses both its ends, and a
plate with no line under it makes the reader guess what they are looking at. FLORA carries
three — the brand film, the empty canvas, the chained workflow.

A shot whose `src` ends `.mp4` renders as a film. **It does not loop.** The card covers are cut
to close their own loop; FLORA's film runs bright to dark and ends on the lockup, so looping it
flashes on every seam and throws the ending away. It carries no audio track at all, is
`preload="none"` so 3.2MB does not download because a panel opened, and starts on an
IntersectionObserver at .25 when it reaches the viewport — an entrance, like the cards, then
unobserved. Click the plate to run it again.

Copy comes from the store, with a baked `#cs-data` block as the fallback, the same
arrangement the card order uses. Four sections where the store has the four-part text;
where it does not, the hook is the Overview and that is the whole entry. Nothing is
authored twice and nothing announces the absence.

**Three projects carry their system inline.** Idler renders the accents, the twelve-step
neutral scale, the six Matter units and the type ladder from `id-idler.pages.dev`; Artifice
renders carbon, chalk, cobalt on both grounds, the mark minimums, WHITEBOX/BLACKBOX and the
type ladder from `brand.artificenyc.org`. Values are read off the live guidelines and checked
against them, never transcribed from a picture. The Matter units are drawn from a form-and-state
pair rather than shipped as six files, so there can be a sixth and not a seventh. Both link out
under **Open the guidelines**.

**Idler's system is pulled at runtime, not copied.** `id-idler.pages.dev` serves
`access-control-allow-origin: *`, so the panel fetches the guidelines and reads the values off
the document. The page has a real contract for them: every accent is `button.sw[data-hex]`
carrying its name in `aria-label` and its state in `.role`, every neutral step is
`button.rstep[data-hex]`, every Matter unit is a `.acell` with `.ameans` and `.aname`. Those
three are pulled. Units are accepted only at exactly six, because six and no seventh is the
argument the block makes; any other count means the parse is wrong, not the system.

**The Matter units are the client's art, not a drawing of it.** They were hand-drawn SVG paths
built from the form-and-state pair, and the drawing was wrong in a way that misstated the system:
the hole state is a small circular aperture *inside* the form, and the drawing rendered the form
knocked out of a plate, which is its inverse. The forms are also rounded, not sharp-cornered.
The six PNGs in `stage/idler/atoms/` are id-idler's own `/assets/atoms/`, used as supplied.
**A brand primitive is fixed art; deriving one from a rule is how you publish a wrong one.**

The neutral ramp carries its `01`–`12` step numbers, as the Grayscale section does. Each number's
colour is chosen from its own swatch by asking which of ink or paper wins on it — a fixed
luminance threshold left the crossover step at 2.3:1, and `mix-blend-mode:difference` went
invisible across six of the twelve. Every step now measures 4.6:1 or better.

The type table's last row carries no bottom rule. It and the footer's top rule sat as two
parallel dotted lines with the section's padding between them, and the footer already closes
the block.

**The type ladder is not pulled.** It is split across several grouped `.ttable`s with a Preview
column, and a naive parse of that returns garbage rather than nothing, which is worse than a
copy. It stays baked until id-idler publishes the scale as data.

Every pull is a merge over the baked block, never a replacement, and the result is cached for a
day. A fetch that fails, is blocked, or returns an unrecognised shape leaves the panel exactly
as it renders offline — verified by aborting the request and confirming all four counts hold.
That it is genuinely reading the document rather than its own copy is verified the other way:
serve the real guidelines with one accent and one unit renamed, and both renames appear in the
panel.

The block states no claim about its own accuracy: both systems opened on a line saying the
values were read off the live document rather than transcribed from it, which asserted exactly
the thing the swatches and tables are there to demonstrate, and ran the same
not-X-but-Y shape twice. Cut. Idler's table keeps a Face column because it runs two faces;
Artifice's carried one family five times, so the family is a single **Typeface** spec line and
the column is gone.

**FLORA's is Hieronymous**, named for the Bosch panel that opens its reference board. There is
no published guidelines document to pull from — the system exists as a campaign set and that
board — so the block carries the board and the four names on it and nothing invented around
them: Hieronymus Bosch, Nam June Paik, Iris van Herpen, Gisela Colón.

**The board image spells two of the four wrong** ("Hieronymous Bosch", "Giesela Colon"). The
names in the reference line are the artists' own spellings. A real person's name is not a place
to reproduce a typo, so the two disagree on purpose until the source file is fixed.

The panel's swatch chips carry a dotted `--line` border: `#0E0E0E` on the dark ground is a
chip you cannot otherwise see, and a dotted edge joins the one rule family rather than
introducing a second. There is no `--veil` token any more — nothing shows through a full-bleed
panel, so a scrim behind it was a control that did nothing.

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
Renaise. Case studies live here now, at `/work/<slug>/`, and as of 2026-09-10 every card
opens one in the panel rather than routing to a studioartifice.com subpage.

## Open

- The trial mono is gone — that path now 404s. Item closed 2026-08-31.
- Unreferenced assets **stay**, by Renaise 2026-08-31. `covers/` (six superseded PNGs, 9.5MB)
  and five unused font files (both Diatype Widths variables, Diatype Italic, Redaction Regular
  + Bold) are committed and served but referenced by nothing. This is a decision, not an
  oversight: do not raise it again or prune them.
- Root `CLAUDE.md` still describes a cream page, Neue Haas Grotesk, and a `#FF2A00` accent.
  None have ever existed in this build.
