# renaise.com — context log

## 2026-10-04 · Aputure: context, sections, /aputure

- Slug `industrial-lighting` → `aputure` (card, #cs-data, search terms, `stage/aputure/`,
  `assets/logos/aputure.svg`, route page). `/industrial-lighting/` is a noindex refresh to `/aputure/`
  so old links land. The card still links out to studioartifice.com/work/industrial-lighting/.
  The Seance CMS still keys this project as `industrial-lighting`, so its year/medium/status no longer
  apply here (baked values stand).
- New case-study component: `briefs` = [{label, pairs:[[term, def]]}], rendered after Problem as
  labeled `cs-pairs wide` sections. Aputure carries Goals, Measure, Scope, Direction, from Renaise's
  brief, kickoff notes and SOW scope (8-week design, 4-month build; Aputure/amaran/Deity/Sidus Link).
- Measure is deliberately general (no Q1 CVR, funnel percentages or revenue projection): those are
  the client's internal figures. Exact numbers are in the 2026-10-04 conversation if cleared to publish.
- Open: year. renaise.com says 2024, studioartifice.com llms.txt says 2025.

## 2026-09-30 · AFXHQ cover in dark mode

Re-recorded the Archive walkthrough with the dashboard in dark mode (same path and redactions; cursor
inverted to white). The shell only picks up `afxhq-theme` on a full load, so the recorder sets the key
and reloads; setting it and changing the hash left the shell light and only the embed dark.

## 2026-09-30 · Copy pass

- **One title per project.** Cards (Sept retitles) and case studies disagreed for Osmosis, Studio
  Artifice and Aputure, and the Seance CMS overrode Idler's panel title with a July one. Case data now
  matches the cards, and the CMS overrides only `year`, `medium`, `status` (+ order). Name/title/role
  are authored here; the store's rows for them are stale. Update titles in index.html, not the CMS.
- Statement: "practice from web to world". Information: dropped the sentence that repeated footnote 1;
  "speculative fiction" once, not science fiction + speculative fiction; "Founder + creative director".
- Case copy: SOOT WORLD spelled one way; SOOT's principle quoted; FLORA "Hieronymus" (matches the
  artifact tile) without naming Bosch twice; Osmosis "match" frontier models (hook and problem agreed
  on match); Idler's dark-category point made once; Studio Artifice impact out of third person;
  Lighthouse process/impact untangled; Veo 3 named consistently; ARTIFACTORY numerals; AFXHQ impact
  no longer repeats the token point.

## 2026-09-30 · AFXHQ case study

- New card + case study: **AFXHQ · Infrastructure for Interoperability** (Artifice NYC's internal
  operations dashboard, afxhq.pages.dev, behind Cloudflare Access). Product filter (All 13 / Product 6),
  Artifice glyph + name, tag Infrastructure, route page `/afxhq/`.
- CTA: new `contact` field on a case study ({label, email}) renders the ledger capsule as a mailto;
  AFXHQ reads "Contact to Learn More" → admin@artificenyc.org. Takes precedence over live/status.
- Cover: a real-time Playwright recording (not the shared browse daemon, which reset mid-capture)
  scrolling the Archive view only, from the chapters to nodes:i, cursor drawn in-page, 0.35s
  crossfade loop. Redacted in-frame: team roster, War Room nav item, chapter gross figures, the
  ONX "(50/50)" term; "ONX Studio" lowercased per partner naming. Views ruled out as sensitive:
  Intelligence/Profiles (CRM), Websites (tokens/repos), Departments (staff), Routines, Interviews
  (unannounced Ch006). Recorder: scratch `afx/rec/rec.cjs`.
- 13 cards leave a single card on the last desktop row.

## 2026-09-30 · Phone socials move to the page foot

Under 900px the six icon links leave the header and close the page, under the footnotes (a dotted
rule above them). One set of links is moved between `.acts` and `nav.socials` by a matchMedia
script, not duplicated; desktop keeps the labelled rail links. Clock + switch stay in the header.

## 2026-09-30 · Phone rail icons

Are.na's icon is now its official mark (from are.na/favicon.svg, fill → currentColor) instead of
the drawn approximation. Phone rail icons 18px → 15px; the 40px tap targets are unchanged.

## 2026-09-30 · Desktop filter pills

Four pills crowded the 234px rail. Counts now show only under 900px, where the pills get the full
width; the status line still announces the shown count.

## 2026-09-28 · The open list, fixed

- Case-study routes are real files: `scripts/build-routes.py` writes `/<slug>/index.html` from
  #cs-data (200, own title/description/cover as og:image, canonical), then forwards to `/?p=<slug>`
  like 404.html. **Re-run it whenever #cs-data or a cover changes.**
- Filters are what a client buys: All 12 / Identity 5 / Product 5 / Site 5 (cards carry
  multi-value data-cat). Depictions is `irl` and lives under All; its crumb reads IRL and hands
  back All. Crumb shows the card's first kind in title case.
- Names: The Artifact Index takes the glyph treatment (Artifice glyph, `assets/logos/artifice-glyph.svg`,
  + name) so it no longer shows the same ARTIFICE wordmark as Artifice Brand Identity. Doubled
  `.nmw` wrappers removed from seven cards.
- Phones: rail links are a 3-across grid of 40px dotted capsules (the filter pills' shape).
- Cards: `.media` is aria-hidden and hover `.sys` images have empty alt, so each link's name is its
  card text. Search reads "Search work" (it only searches the grid).
- Dead code out: smoothLoop (no data-smooth anywhere), .proj .ext, .k-re/.k-ai, stale donate
  comment, duplicate .cs-sw and .cs-shot rules.
- DESIGN.md + CLAUDE.md synced to the build (dark default, Diatype + Redaction, no brand hue).

## 2026-09-28 · /pd + /cd pass; System block standardized

Renaise: "the guidelines needs to be a button and the typography needs to be standardized."
- System block: the guidelines link is now the live-site CTA capsule ("Open the guidelines ↗";
  SOOT's reads "Open Library ↗"), closing the section. The dt/dd row is gone.
- System + Compare type is two roles only. Label: .62rem caps, .1em, --sw4 (table heads, hex,
  tokens, ramp codes). Value: .72rem, 400, --sw2 (names, steps, cells). Hex/token tracking was
  .06em against .1em on table heads; the guidelines dd was weight 300. Face tokens drop the CSS
  "--" prefix ("--institutional" read as "- -INSTITUTIONAL").
- Case study honors reduced motion (plate no longer autoplays, films don't auto-run); the plate
  video carries the card's label.
- Phone search field on the 40px floor; browser theme color matches --bg1 (#e9e9e9); Mythra icon
  outline dotted; the switch uses the site-wide focus ring.

Open (recommended, not shipped): case-study URLs (/soot, /idler…) return HTTP 404 via 404.html,
so shared links preview badly; rail link touch targets on phones; URL 11 / IRL 1 filter carries
little signal; four card videos lack labels and seven cards double-wrap .nmw; DESIGN.md + CLAUDE.md
describe the old cream/Favorit build.

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

## 2026-09-25 · Artifacts become a section

Four pills read wrong, and Artifacts isn't a filter over projects; it's a different kind of thing.
Moved out of the rail pills into its own section after the work grid, in the CV row anatomy
(label left, 3×3 grid in the body column, two across on phones). Rail filters back to All / URL / IRL.
The section's row rule is its only divider (card border dropped to avoid parallel lines).

## 2026-09-25 · Copy pass, Information, SOOT artifact

- Deslop: rail statement (dropped "industrial knowledge worker", "bespoke"), Information paragraph and
  footnote 1 no longer repeat the "made-up artifact tests the idea" line; slogan-shaped sentences
  rewritten in Studio Artifice, Artifice brand, Idler and Lighthouse case studies; ARTIFACTORY title case.
- Information: all text in --prose-ink; company logos inline at full strength (--accent) with a
  word-space either side.
- SOOT artifact: the Spaces rail (+ and four Space avatars from SOOT's own UI, cover frame) replaces Trail.
- Every case study opens with a See live site CTA (SOOT → soot.com); Veo shows In production.
- Card/case titles can be overridden at runtime by the Seance CMS store; repo edits to titles may not show if the CMS has its own.
