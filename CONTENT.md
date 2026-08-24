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

## Decided 2026-08-24

**Case study lives once, on studioartifice.com, for the six engagements that
have one.** renaise.com carries Overview, Selected outcomes and Role +
collaborators, then hands off. Those three nodes are the personal claim, which
the studio site does not make and cannot: on studioartifice.com the actor is the
studio, here it is Renaise, in a named role, with named collaborators. The long
read is the same story either way, and two copies of one story is the drift this
repo keeps paying for.

**Three projects need full authoring here, case study included**, because
nothing upstream exists: ARTIFACTORY, the Artifact Index, and the Artifice brand
identity. The `studio-artifice` card is the studio's own site, which is the
artifact; it links to itself and needs no case study.

### Should studioartifice.com and renaise.com share one CMS? No.

The overlap is smaller than it looks, and the non-overlap is the reason.

| | Projects |
|---|---|
| Both sites | idler, soot, osmosis, industrial-lighting, lighthouse, depictions-of-original-sin |
| renaise.com only | artifactory, the-artifact-index, artifice-brand, studio-artifice |
| studioartifice.com only | sensitive-subjects, flora |

Three reasons a shared record is wrong here.

**The entity wall.** renaise.com's four exclusives span three entities: Codex
(ARTIFACTORY), Artifice NYC 501(c)(3) (the Artifact Index, the brand identity),
and the LLC itself. That is correct for a person's portfolio and illegitimate for
the LLC's, which may only carry commercial work. A shared record set would put
nonprofit programme work one tag away from the studio's sales surface, and a tag
is not a wall.

**The two sites make different claims about the same project.** SOOT credits
`SOOT (Jake Harper, Noa Chazan), UNNAMED, Two.much Studio` and does not list
Studio Artifice at all; here it is Renaise as Lead Product Designer. One record
cannot hold both without per-site views, at which point it is two records with
extra machinery.

**This repo has no build step, by design.** `CLAUDE.md` states it: self-contained,
hand-edit, push. Pulling from `projects.ts` means giving renaise.com a build,
which trades a documented simplicity for a coupling that only serves six rows.

### What to share instead

The facts that must not drift, not the record: client name, year, collaborators,
links. `projects.ts` is upstream for those six; this repo copies them
deliberately. A check that diffs the shared fields across both and reports
divergence buys the drift detection without the coupling.

## Copy rules for this tree

Per `CLAUDE.md`: no em dashes, `+` over "and" in noun joins, quiet editorial
register. Outcomes are sentences, not feature lists; a list is the tell that the
node was written to fit a card.
