# renaise.com — content model

Canonical structure for Work, from Renaise 2026-08-24. Build against this tree;
if the code and the tree disagree, the tree is right.

```
Work
└── Project
    ├── Overview
    ├── Selected outcomes
    ├── Role + collaborators
    ├── Case study
    └── LAB / STAGE entries
```

## Where the build stands against it

**Project does not exist as a page.** The site is one `index.html` carrying ten
project cards, and every card links away: seven to `studioartifice.com/work/…`,
the rest to `index.artificenyc.org`, `artifactory.pages.dev` and
`brand.artificenyc.org`. There is no route on renaise.com that a Project node
could render into, so every node below is unbuilt.

The card is the only Project surface today, and it carries four fields:

| Card field | Maps to |
|---|---|
| `.t` title | Overview, compressed to one line |
| `.m` role | Role, without collaborators |
| `.d` blurb | Overview, compressed to one sentence |
| `.tag` | Discipline, not a node in this tree |

## The nodes

**Overview** — what the work is and the condition it answered. The card blurb is
this node truncated; the full node is the place the compression is currently
throwing away.

**Selected outcomes** — what shipped, stated as results rather than a feature
list. This is the node the old card copy kept reaching for and getting wrong
(`Preset library, live tuning, self-contained embed export.`), because a card has
no room for it and a list is what you write when you have no room.

**Role + collaborators** — the card holds the role and drops the collaborators
entirely. Studio Artifice's `projects.ts` already carries a `contributors` field
for the same engagements (e.g. `SOOT (Jake Harper, Noa Chazan), UNNAMED,
Two.much Studio`), so this node has a source to pull from rather than needing to
be authored twice.

**Case study** — the long-form read. For the seven projects that link to
`studioartifice.com/work/…`, that case study already exists on another domain.
Decide per project whether renaise.com hosts its own, or points at the studio's.
Doing both means maintaining two versions of one story.

**LAB / STAGE entries** — process and public showing, per the WHITEBOX / BLACKBOX
split. A Project may carry entries of either kind, or none. Nothing in this repo
models them yet.

## Open before building

1. **Does renaise.com host case studies, or link to them?** This decides whether
   Project is a full page type or a richer card that still hands off.
2. **What is the source of truth?** Studio Artifice's `projects.ts` already holds
   overview, outcome, role and contributors for the overlapping engagements.
   Duplicating that here creates a second record to keep in sync; the alternative
   is pulling from it at build time.
3. **Which projects get the full tree?** ARTIFACTORY, the Artifact Index and the
   Artifice identity are Renaise's own work with no studio case study behind them,
   so they need authoring here regardless of what happens to the other seven.

## Copy rules for this tree

Per `CLAUDE.md`: no em dashes, `+` over "and" in noun joins, quiet editorial
register. Outcomes are sentences, not feature lists; a list is the tell that the
node was written to fit a card.
