---
name: minimap-map
description: Build a knowledge-domain mind map as an importable Minimap JSON file (saved to maps/<Topic>.json), sized to a tier and structured for learning AND doing - never pure taxonomy. Use whenever the user wants to map a field, build a domain overview, plan a learning path, or create a navigation artifact for systematic study in the Minimap app. Trigger on "/minimap-map", "map [topic] for minimap", "build me a minimap of X", "draw the structure of [field]", "mindmap for [topic]", or any request to systematize a field into a navigable artifact they will open in Minimap. Distinct from /minimap-decide, which structures a specific choice rather than a field. Default to this skill whenever a Minimap-ready knowledge artifact is the natural deliverable.
---

# minimap-map

Build a mind map of a knowledge domain as **importable Minimap JSON**, written to
`maps/<Topic>.json`. The map is **structured for learning + doing, never pure taxonomy** —
its job is to support systematic engagement with a field, not to be a Wikipedia tree.

---

## Setup

Paths are relative to the Minimap folder — the one holding the app
(`index.html`, or `mindmap.html` in a shared copy) alongside `tools/` and `maps/`:

| | |
|---|---|
| Maps | `maps/<Topic>.json` |
| Converter | `tools/md2minimap.py` |
| Scratch markdown | anywhere temporary — it is an intermediate, not a deliverable |

Installed through an agent there is no such folder. The converters still ship alongside the
skills, so every `tools/...` path below means `${CLAUDE_PLUGIN_ROOT}/tools/...` in Claude Code,
and elsewhere `tools/` resolved from this file's own location — `../../tools/`. `maps/` is then
a folder in the working directory; create it if it is not there.

If a sibling skill in this environment writes maps into a notes vault instead, that one owns
the vault and this one owns `maps/`. Never write to both from one invocation.

---

## What Minimap changes

Minimap is **one self-contained file per map**, not a vault of cross-linked notes. If you
are adapting habits from a file-based outliner, three things differ:

| A vault of notes | Minimap |
|---|---|
| `[[Wiki Link]]` opens **another file** | `[[Node title]]` in a **note** jumps to **another node in this same map** — exact title match, greyed out if nothing matches |
| Stub links build a graph across files | There is no vault. A link to a map that doesn't exist yet is a dead end, not a promise |
| Cross-topic structure lives in the graph | Cross-branch structure lives in **connections** (dashed arrows) inside the one map |
| Metadata in a footer or frontmatter | Attribution goes in the **root node's note** — there is no page footer |
| The markdown file is the artifact | The markdown is the intermediate; the **JSON** is the deliverable |

Three rules follow, and they are the ones most easily got wrong:

1. **Never write `[[X]]` for a node that isn't in this map.** Elsewhere a red link is an
   invitation; here it renders greyed out and goes nowhere. If a subtopic deserves its own
   map later, say so in the node's **note** as plain prose ("big enough for its own map"),
   not as a wiki-link.
2. **Use `[[X]]` freely for nodes that *are* in this map.** This is Minimap's real advantage
   over a static outline: a note on a practice node can point at the trap it avoids. Prefer
   a `[[wiki-link]]` in a note for a soft reference, and a **connection** for a structural
   relationship you want drawn on the canvas.
3. **Connections replace the vault graph.** Every map should carry 2–6 connections that cut
   across top-level branches — mechanism → trap, decision → practice. A map with zero
   connections is a tree, and Minimap already draws trees; the connections are what make it
   a map.

---

## Authoring pipeline — markdown in, JSON out

Do **not** hand-write the JSON. Node ids, children arrays and link endpoints are easy to get
subtly wrong, and the app will reject or silently mangle the result. Instead:

1. Write the map as markdown to a scratch file (dialect below).
2. Convert:

```bash
python3 tools/md2minimap.py <scratch>.md maps/<Topic>.json --name "<Topic>"
```

3. Read the shape report it prints — node count, depth, per-branch share, over-long labels,
   unresolved connections. **Check it against the tier budget** and fix the markdown if it
   is out of range. The report is the skill's self-check; don't skip it.
4. Tell the user the path and how to load it: **Files ▾ → Import**, pick the JSON.

The converter is also the round-trip: Minimap's own **Export ▾ → Markdown** produces this
same dialect, so an existing map can be exported, edited, and converted back in.

### The markdown dialect

```markdown
# <Topic>
<plain prose here becomes the root node's note — put the attribution line here>

## <Natural top-level branch>
- <node>
  > <a note on that node, one `>` line per line of note>
  - <child node>
- <node> `To do`
- <node> {blue}

## Connections
- <From node title> -> <To node title> (<label>)
```

- Two spaces of indent per level. `## Heading` is a top-level branch (a child of the root).
- A trailing `` `Label` `` sets the node's **status**. `To do` / `In progress` / `Blocked` /
  `Done` map to the built-in presets; any other label creates a new preset.
- A trailing `{token}` sets the node's **colour** — grey, blue, pumpkin, lime, aqua, rose,
  iris, butter.
- `## Connections` is special: it becomes the dashed cross-branch arrows. Titles must match
  an existing node exactly; the report names any that don't resolve.
- Notes take Minimap's markdown subset: `**bold**`, `*italic*`, `` `code` ``,
  `==highlight==`, `~~strike~~`, lists, `- [ ]` checkboxes, quotes, code fences, links, and
  `[[Node title]]`.

### Colour and status, used with restraint

Minimap is black and white by default and that is the point — colour is a shared palette
used only by node text and status tags. So:

- **Status** is for maps the user will *work* through — a learning path where nodes get
  marked Done. Set statuses only if the map has that character; otherwise leave every node
  statusless.
- **Colour** is for one semantic axis per map at most — e.g. traps in `rose`, or the
  mechanism spine in `blue`. Never colour by branch (the layout already shows that) and
  never colour more than about a third of the nodes.

---

## The core anti-pattern this skill fights

The failure mode: ask for "ETF" and get back a Wikipedia tree (Definition → History → Types
→ Largest providers → Tax). True, navigable, useless for doing — and bad for learning,
because real understanding lives in mechanisms, decisions, and traps, not taxonomy.

**Every map must pass the "is this just taxonomy?" check** before it's written. If the
answer is yes, the map is wrong and needs re-planning.

---

## The framework — three layers

### Layer 1 — Topic Type (decides the facet set)

| Type | Examples | Type-specific facets |
|---|---|---|
| **practice-domain** | ETF investing, resistance training, design tokens | Mechanism · Decisions · Practices |
| **idea** | Finite & Infinite Games, A Pattern Language, Sapir-Whorf | Core moves · Lineage · Applications · Counter-positions |
| **field** | Cognitive science, macroeconomics, compiler design | Subfields · Canonical works · Open questions · Methods |
| **place** | A city, a region, a neighbourhood | Geography · History · Rhythms · Subcultures |
| **language** | German B1, Mandarin idioms | Patterns · Exposure paths · Mechanics |
| **tool** | An editor, a design tool, a CLI | Capabilities · Alternatives · Ecosystem · History |

If the topic genuinely doesn't fit, **say so explicitly** and propose what it most resembles
— don't silently force-fit it.

**The examples in that table are illustrative, not binding.** The same subject maps
differently depending on what the user wants from it: a discipline is a *field* to someone
surveying it and a *practice-domain* to someone about to run a project in it. The "what will
you do with this map" question below decides; the table only suggests. When you override the
table, **name the override in the attribution line** so the choice is visible and
challengeable.

### Layer 2 — Universal Floor (every map has these)

- **Core ideas** — the 3–5 things you must hold to understand anything else
- **A "where this gets misunderstood" branch** — phrased per type:

| Topic type | Branch heading |
|---|---|
| **practice-domain** | "Where this gets misunderstood" / "Common traps" |
| **idea** | "Counter-positions" / "Where this framework breaks" |
| **field** | "Open questions and live debates" |
| **place** | "What outsiders get wrong" |
| **language** | "False friends and common errors" |
| **tool** | "Foot-guns" / "Where users get stuck" |

Non-negotiable. A map without it is a textbook. If you can't think of any traps, you haven't
engaged with the topic deeply enough to map it yet.

### Layer 3 — Borrowed facets and hybrid types

**Pick one primary type, then borrow facets from secondary types as needed.** Don't maintain
two complete facet sets. Name each borrow in the attribution line (in the root note):

```
type: practice-domain · tier: L3 · facets: core, mechanism, decisions, practices, traps + lineage (borrowed from idea)
```

Choosing the primary type when a topic could be two: ask what the user wants to *do* with
the map. Do/build → practice-domain. Think with → idea. Use / pick between alternatives →
tool. Default tiebreaker: practice-domain.

**Facet overlap:** when a node could go in two branches, pick the one matching how it would
be *used* — consulted while deciding → Decisions; consulted while doing → Practices. Don't
duplicate the node. If a whole branch feels facet-confused, the topic is probably one tier
too high.

---

## Tiering — node budget + soft depth ceiling

| Tier | Example | Total nodes | Depth | Character |
|---|---|---|---|---|
| **L1 — Domain** | A whole discipline | 20–35 | 2 (max 3) | Orientation. Mostly pointers to maps built later — as prose in notes, **not** wiki-links. |
| **L2 — Field** | A working subfield | 35–55 | 3 (max 4) | The "real" working map. Most maps live here. |
| **L3 — Topic** | One topic in depth | 45–70 | 3–4 | Deep dive. Mechanism and practice nodes get genuinely detailed. |
| **L4 — Sub-topic** | A narrow slice of an L3 | 25–40 | 2–3 | Narrow but dense. Usually grows out of an L3. |

**Announce the tier in the first line of your response, before drafting.** Only stop and ask
if two tiers are equally plausible AND would produce meaningfully different maps.

```
Drafting <Topic> as L3 (deep dive, ~55 nodes). Say "make it L2" if you'd rather have it placed in a broader context.
```

### Guardrails — all three are checked by the converter's report

- **Label legibility.** Soft ~40-character ceiling on any node title; Minimap wraps long
  titles into taller cards and the map gets mushy. Longer → break into parent + child, or
  move the detail into the node's note. The report lists every label over 40.
- **Branch balance.** No single top-level branch should hold more than ~40% of the nodes.
  The report prints each branch's share and flags this.
- **Connections resolve.** The report names any connection whose endpoint title doesn't
  match a node. An unresolved connection is silently dropped — always fix it.

### "Not on this map"

Every map ends with a real `## Not on this map` branch listing 3–5 things deliberately
excluded and why. It renders as a real branch on the canvas, doubles as a navigation aid,
and keeps the skill honest about scope. Here it matters *more* than in a vault, because
there is no elsewhere to absorb what you left out.

**Put the reason in the node's note, not in the title.** `Thing — why it's excluded` on one
line blows the 40-character budget every time.

---

## Structure — facets as metadata, not top-level branches

**Structure follows the field, not a fixed facet template.** Don't open every map with
`Concepts / Mechanisms / Practices / Traps` as the top-level branches — that produces maps
that all feel the same and forces the topic into a mould.

Bad (facets as top-level branches):

```
ETF
├── Concepts
├── Mechanisms
├── Practices
└── Traps
```

Good (structure follows the field, facets embedded):

```
ETF
├── What it is
│   ├── Basket of assets traded like a stock
│   └── Pricing: NAV vs market price
├── How it works
│   └── Creation/redemption arbitrage — why price tracks NAV
├── Types
├── Building a portfolio
│   ├── Asset allocation first, products second
│   └── TER as primary filter
└── Where this gets misunderstood
    ├── Tracking error vs tracking difference
    └── Volume ≠ liquidity — look at the underlying
```

The second map *uses* every facet, but embedded in the topic's natural structure.

---

## Pre-flight check (before writing any markdown)

1. **Topic type?** (one of six; name borrows)
2. **Tier?** (L1–L4)
3. **The 3–5 core ideas a learner must hold?**
4. **The mechanism / move / structure that, once understood, makes everything click?** Every
   domain has one.
5. **For practice-domains / fields / tools: 2–3 decisions a practitioner faces repeatedly?**
6. **For practice-domains / languages / tools: 2–3 recurring practices?**
7. **2–3 traps — where does intuition lead people wrong?**
8. **Which 2–6 relationships cut across branches?** These become the connections. If you
   can't name any, the branches probably aren't interacting and the map may be taxonomy
   after all.

**If you can't answer the applicable questions** (type, tier, core ideas, mechanism, traps
are always required), do not draft. Ask, or web-search first, or say honestly that the topic
needs more grounding. Hallucinating plausible-sounding nodes for a field you don't know is
the worst failure mode of this skill.

---

## Language convention

**Ask at invocation time** which to use for this map:
- English labels (default for technical/academic topics)
- Bilingual labels: `Term / translation`, when the user works across two languages
- Labels in the user's own language (for culturally-rooted topics)

Bilingual labels eat the 40-character budget fast. If bilingual is chosen, keep the primary
label short and put the fuller gloss in the node's note.

**If you can't ask** — running unattended, or in a background agent with no one to answer —
don't stall and don't silently guess. Take the documented default (English for technical
topics; otherwise match the convention of the maps already in `maps/`), record it in the
attribution line, and say in your report which defaults you took and what would change if
they're wrong. The same applies to the tier question.

---

## Existing maps

Before drafting, check `maps/` for a JSON file on the same or an overlapping topic. If one
exists, say so and ask whether to extend it (export, edit the markdown, re-convert) or start
fresh — don't silently produce a near-duplicate.

There is no vault-wide graph to maintain, so there is **no parent-map gloss update step**.

---

## When to web-search

Enough from training data: stable technical fields, books and ideas with long-standing
reception, languages, places with stable character.

**Requires search first:** "current state of X" framing, tools / products / startups, niche
academic subfields, anything you don't already have a clear mental model of. When in doubt,
search.

---

## Refinement loop

The first draft is a proposal. After producing the map, **invite challenge**:

> Here's a first draft at `maps/<Topic>.json` — Files ▾ → Import to open it.
> Things you might want to push back on:
> - Type classification (I called this a [type] — right?)
> - Tier (I chose L<N> — too shallow / too deep?)
> - Branches that feel forced or missing
> - Connections: too few, wrong ones, or ones I missed
> - Anything in "Not on this map" that should actually be in

When the user pushes back on one branch, **regenerate just that subtree** in the markdown
and re-run the converter — don't redraft the whole map. Keep the scratch markdown for the
length of the conversation so refinement is cheap.

Note the re-import caveat: importing the regenerated JSON adds a **new** map rather than
updating the one they have open, so the old one should be deleted from Files ▾. Say this
once, on the first refinement — not on every turn.

---

## What this skill does NOT do

- **Write JSON by hand.** Always through the converter.
- **Wiki-link nodes that aren't in the map.** Greyed-out dead links, not promises.
- **Pure taxonomy trees.** If the draft looks like a Wikipedia outline, stop and revisit the
  pre-flight check.
- **Force facets where they don't fit.** If a topic has no Decisions axis, leave it out and
  say so in the attribution line.
- **Edit `index.html`.** The app is not the skill's business.
- **Colour or tag everything.** Black and white is the default for a reason.

---

## Quick reference — invocation flow

1. **Hear the request** ("/minimap-map X", "build me a minimap of X")
2. **Identify topic type** — ask if genuinely ambiguous
3. **Announce the tier** in your first line
4. **Confirm the language convention**
5. **Check `maps/`** for an existing map on the topic
6. **Run the pre-flight check** — eight questions, including connections; web-search if needed
7. **Write the markdown** to a scratch file — structure follows the field, traps branch present, "Not on this map" present, attribution in the root note
8. **Convert** with `tools/md2minimap.py` into `maps/<Topic>.json`
9. **Read the shape report** — node count vs tier budget, branch balance, long labels, unresolved connections. Fix and re-run if out of range.
10. **Hand over the path** and the Files ▾ → Import step
11. **Invite challenge**; refine single subtrees and re-convert
