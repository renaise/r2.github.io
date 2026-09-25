# renaise.com — context log

## 2026-09-25 · /pd visual hierarchy pass (+ /cd)

JTBD: a prospective client or collaborator judges the work in one scroll, then opens a case study.
Verdict: patchable. Spine holds (rail → grid → case panel); accretion was in spacing and dead CSS.

Fixed and shipped:
- Rail filter pills overflowed the rail (266px in 234px) once Artifacts joined; tightened type/padding to fit one row.
- Grid row gap 4.4rem → `--row-gap` 3.2rem, shared by projects and artifacts (cards lost their description line).
- Artifact names moved onto the card-title step (.96rem/450) with the same accent hover; source line on the .1em caps tracking.
- Artifact media marked decorative (caption names the link); dropped hardcoded #000 grounds for `--tile`; merged duplicate .art rules.
- Case-study prose and definition text on `--prose-ink`, one voice with the rail bio and CV.
- Guidelines link moved to the end of the System section instead of splitting the specimens.
- Type table: sizes normalized to "4.5rem / 72px" at render time (Idler system is fetched live, so data edits alone don't stick); tabular-nums off there (it widened spaces).
- Phones: 40px touch floor on pills and search.
- Dead CSS removed: .brand sup, .wm .pn, .cs-live*, stale description comments.

Left as is (documented choices): rail links at 1.44rem (DESIGN.md, 2026-08-26); search focus stays off accent (DESIGN comment).
Open: mobile rail links are ~15px tall touch targets; widening them changes the one-row link layout, so it needs a design call.

## 2026-09-25 · Artifacts refine

- One illustration per project (8). Grid goes four across on wide screens so they land as two full rows; two across below 1240px.
- The Idler Shell loop was the one bright tile, and cover-fit clipped the cube. Re-rendered with its #F3F5F2 ground keyed out onto the tile color (#101010), shown whole (contain). Source: ~/Desktop/idler-shell-recording-2026-08-19.mp4.

## 2026-09-25 · Artifacts route to their case study

Each case study now carries an Artifact section (after the written case, before the shots) rendering
the same piece as the index tile. A tile click opens the case study scrolled to that section; tiles
link to `/<slug>#artifact` so a new tab or shared link lands there too. Card clicks still open at the top.

## 2026-09-25 · Vector joins Artifacts

- ARTIFACTORY's artifact is Vector (artifactory-vector.pages.dev); its case-study Artifact section links "Open Vector ↗".
- Tile image is the tool's panel (unit set + motion modes). The 3D stage could not be captured: headless Chrome (swiftshader and metal) renders an empty WebGL stage, and a headed CDP Chrome closed its tabs. Swap in a real Capture/Download from the tool when available.
- Artifact grid column count now follows the count (4 when divisible by 4, else 3) so rows fill.
- Open with Renaise: whether artifacts should carry provenance ("made in Vector / ARTIFACTORY") with tools as instruments.

## 2026-09-25 · The Shell + Sequencer

Vector is the tool that made the Idler Shell (Renaise). The tool keeps its name (live site
unchanged). On renaise.com its tile carries a descriptor only, "Sequencer for the Shell", and sits
right after the Shell; the Shell's caption reads "Idler · 2026 · Made in Vector" and the Idler case
study's Artifact caption links to the tool.
