# renaise.com — CMS

Spec supplied by Renaise 2026-08-25. Recorded here because it answers the open
question `CONTENT.md` leaves at "Should studioartifice.com and renaise.com share
one CMS?" — the answer is the model below, and `CONTENT.md` is superseded on that
point once this ships. Nothing in this repo implements it yet.

The Renaise publishing spec, translated into a working content model.
Artifact-first routing under `/work/`. Astro content collections, static build,
Cloudflare Pages. Its own repo, outside AFXHQ.

```
npm install
npm run validate     # editorial rules
npm run build        # validate, then build
npm run dev
```

## The model

Two collections, one relation.

```
artifacts/          the parent record — one permanent page per artifact
  └── entries/      LAB and STAGE entries, each belonging to exactly one artifact
```

`entry.artifact` is a real `reference("artifacts")`, not a tag. Astro resolves it
at build time and fails the build on a broken id. `mode` is a field on the entry,
not a second collection: LAB and STAGE are states of the artifact, so they live on
one timeline and sort by date together, which lets an artifact return to LAB after
a public encounter without special handling.

### Files

| Path | Holds |
|---|---|
| `src/content/artifacts/<slug>.json` | One artifact. Filename is the slug and the URL segment. |
| `src/content/entries/<slug>/<mode>-<nn>.mdx` | One entry. The folder is the relation, visible on disk. |
| `src/content.config.ts` | Both schemas, enums, validation. |
| `src/lib/archive.ts` | Queries and the display rules (`ARTIFACT 001 · …`). |
| `scripts/validate-content.mjs` | Cross-file editorial rules. Runs before every build. |

### Artifact fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `name` | string | yes | The subject. Distinct from any entry title. |
| `summary` | string <=200 | yes | What it is. Not a pitch. |
| `practice` | `Studio Artifice` / `Artifice` / `Independent` | yes | Enum, enforced. |
| `year` | number | yes | |
| `number` | `"001"` | yes | 3 digits. Unique across the archive. |
| `slug` | kebab-case | yes | Must equal the filename. |
| `cover` | image | | Optimized by Astro; lives in `src/assets/`. |
| `credits` | string[] | yes | At least one. |
| `external_url` | url / null | | Renders the `[OVERVIEW]` link. Omitted when null. |
| `draft` | boolean | | Hidden in production, visible in dev. |

### Entry fields

| Field | Type | Required | Notes |
|---|---|---|---|
| `artifact` | reference | yes | Build fails if it doesn't resolve. |
| `mode` | `LAB` / `STAGE` | yes | |
| `number` | `"01"` | | Omit for a lone STAGE entry: renders as `STAGE · STUDIO ARTIFICE`. |
| `title` | string | yes | The decision or question. Never the artifact name. |
| `date` | date | yes | Sorts the timeline. |
| `excerpt` | string <=280 | yes | The editorial argument. |
| `content` | MDX body | yes | |
| `publish_to_substack` | boolean | | LAB only. |
| `substack_url` | url / null | | Backfilled after the send. |
| `draft` | boolean | | |

## Routes

| URL | Page |
|---|---|
| `/work/` | The Artifact Index |
| `/work/<artifact>/` | The artifact page, entries beneath it, chronological |
| `/work/<artifact>/<mode>-<nn>/` | The canonical entry page |
| `/lab/` | LAB across all artifacts |
| `/stage/` | STAGE across all artifacts |

`/lab/` and `/stage/` are views, not brands: every item links back to its canonical
entry under `/work/`. `public/_redirects` maps old `/stage/<slug>` detail pages onto
their artifact pages, one line per artifact as they migrate.

## The editorial rules, as code

The schema catches one file at a time. Everything that only shows up across files is
in `scripts/validate-content.mjs`, wired into `npm run build`:

- an entry whose title repeats its artifact name
- an entry filed under a folder that doesn't match its `artifact`
- a duplicate `LAB 01` within one artifact, or a reused artifact number
- `publish_to_substack: true` on a STAGE entry
- a `substack_url` with no corresponding send flag
- the string "coming soon" anywhere

Empty states aren't a field and aren't a flag. The artifact page renders its entry
list only when entries exist, and the `[OVERVIEW]` link only when `external_url` is
set. Nothing announces absence.

## Substack

`publish_to_substack` marks an entry for the send; `substack_url` is filled in
afterward, which turns the pair into a mirror log: anything flagged with a null URL
is still owed. The entry page here is canonical and links out to the Substack copy;
the Substack post links back here. Editorial copy is mirrored, never re-authored.

Cross-references to studioartifice.com and artificenyc.org are links, not duplicated
copy. The same artifact may appear on all three; only one of them carries the
editorial text.

## Porting this elsewhere

| Here | Sanity | Payload | Framer / Webflow |
|---|---|---|---|
| `defineCollection` | `defineType` document | `CollectionConfig` | CMS Collection |
| `reference("artifacts")` | `type: "reference"` | `relationship` | Reference field |
| `z.enum(PRACTICE)` | `options.list` | `select` options | Option field |
| `draft` | draft perspective | `versions.drafts` | Draft state |
| glob loader | dataset | database | CMS store |
| `validate-content.mjs` | document validation rules | `beforeValidate` hook | manual review |

Preserve through any port: `artifact` stays a reference field. If it becomes a text
tag, nothing enforces that an entry belongs to exactly one artifact.

---

# Collisions with renaise.com as it stands today

Recorded 2026-08-25, before any build. Three things in this repo contradict the
spec above. None are reasons not to do it; all three need a decision first.

## 1. `/stage/` is already a directory of assets on the live site

The spec routes `/stage/` to the STAGE feed. This repo serves every card's video
and poster from `/stage/<slug>/cover.mp4`, and all ten are live right now:

```
/stage/artifactory/  artifice-brand/  depictions-of-original-sin/  flora/
       idler/  industrial-lighting/  lighthouse/  osmosis/  soot/
       studio-artifice/  the-artifact-index/
```

A STAGE route at `/stage/` and an asset tree at `/stage/` cannot both hold that
segment. The spec's `_redirects` line assumes `/stage/<slug>` was a detail page; here
it is a directory of media. Either the assets move (to `/media/` or Astro's
`src/assets/`, which the spec already implies for `cover`) or the feed moves.

## 2. This repo is a no-build site, on purpose

`CLAUDE.md` states it: `index.html` is the whole site, self-contained, hand-edit and
push. `CONTENT.md` then argues against a shared CMS partly on those grounds, that
pulling from `projects.ts` "means giving renaise.com a build." The spec introduces
Astro, a validate step and a build. That is a deliberate reversal, and worth making
knowingly rather than discovering later.

## 3. The card grid has no home in the route table

The live homepage is ten project cards. The spec's `/work/` is the Artifact Index and
`/work/<artifact>/` the artifact page, but nothing says what `/` becomes: the card
grid kept as a separate homepage, or `/` redirecting to `/work/`, or the grid
rebuilt as the index. The ten cards also carry fields with no home in the artifact
schema — `tag` (Identity + Site, Product, Global Site), the role line
(Lead Product Designer), and the serif blurb. `credits` covers the role; `summary`
covers the blurb; `tag` has no field.
