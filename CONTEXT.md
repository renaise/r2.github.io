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
