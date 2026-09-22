---
name: minimap-concept
description: Structured explanations of technical concepts - bilingual when the user works across two languages - ending - for full explanations - in an offer to graft the concept into one of the user's Minimap maps. Three modes, always ask first, quick snippet (definition, characteristics, applications, cross-domain), story mode (reveal-last narrative), or full 8-section deep dive. Trigger on "/minimap-concept", "explain this term", "what is X", unfamiliar terminology in a paper or article, requests to help understand a paper, concept comparisons ("A vs B"), or new vocabulary the user shares, when the concept should end up on a Minimap canvas. Distinct from /minimap-map, which maps a whole field - this skill handles ONE concept in one sitting.
---

# minimap-concept

Provide structured, bilingual explanations of technical concepts, and give the good ones a
home on the Minimap canvas instead of letting them evaporate in chat.

---

## Setup

Paths are relative to the Minimap folder — the one holding the app
(`index.html`, or `mindmap.html` in a shared copy) alongside `tools/` and `maps/`:

| | |
|---|---|
| Existing maps | `maps/*.json` |
| Graft tool | `tools/graft.py` |

Installed as a plugin there is no such folder: the converters ship with the skill, so every
`tools/...` path below means `${CLAUDE_PLUGIN_ROOT}/tools/...`, and `maps/` is a folder in the
working directory — create it if it is not there.

**Second language.** This skill can run bilingually — giving each term in the user's
working language and in a second one. Set that second language from what the user actually
uses; if they work in one language only, drop the bilingual parts entirely rather than
translating into a language nobody reads.

**Cross-domain connections** (Section 4) are the skill's signature move: every concept gets
tied to two or three domains beyond the one it came from. Pick the domains from what the
user actually works across — their existing maps in `maps/` are the best evidence. If you
have nothing to go on, use the domains the concept itself most naturally reaches and say so.

---

## Core Workflow

### 1. Initial Assessment

When the user presents a new term or concept, **always ask first:**

**"Quick snippet, story, or full explanation?"**

- **Quick snippet** = Sections 1–4 only (faster, vocabulary building)
- **Story** = illustrative narrative that reveals the concept at the end
- **Full explanation** = all 8 sections (deep dive, research context)

**If you can't ask** — running unattended, or the mode was already named in the request —
take the named mode, or default to the quick snippet, and say which you took. Never default
to the full explanation on silence: it's the longest output and the only one that triggers a
graft offer.

### 2. Response Format

Everything below is delivered **in chat**. Nothing touches a map until Section 8's offer, and
only for full explanations.

#### Quick Snippet (Sections 1–4)

**Section 1: Core Definition** — the term in both languages, a clear explanation
in both, and its context in the field.

**Section 2: Key Characteristics** — 3–5 defining features, technical
specifications where applicable, bilingual bullets.

**Section 3: Application Domains** — real-world use cases, industry examples,
current implementations.

**Section 4: Cross-Domain Relevance** — connections to the adjacent domains
identified in Setup, and where they intersect.

#### Story Mode

Identify a **somewhat niche but genuinely useful** aspect of the concept — one an early
student wouldn't know but an advanced practitioner would. Write a 3-paragraph story that
fully embodies the concept **without naming it**, then reveal.

1. **Paragraph 1** — set the scene; characters/situation that will embody the concept
2. **Paragraph 2** — develop tension that makes the concept's logic visible
3. **Paragraph 3** — resolution demonstrating the concept's consequence
4. **Reveal** — name it bilingually, explain directly, point at exactly how the story showed it

Pick a niche angle, not the obvious definition. Keep it concrete: real professions, plausible
scenarios, specific numbers. Someone who doesn't know the concept should finish thinking "oh,
*that's* what this means."

#### Full Explanation (All 8 Sections)

Sections 1–4 as above, then:

**Section 5: Technology Maturity** — current state (lab / prototype /
commercial), realistic timeline, key challenges. Distinguish lab demos from shipped products;
name hype where it's hype.

**Section 6: Related Concepts** — 3–5 connected terms, how they relate, a suggested
learning sequence.

**Section 7: Extension Reading** — foundational papers, recent advances, reviews,
industry reports. See the link rule below — never cite from memory.

**Section 8: Knowledge Graph Nodes** — here, Section 8 is not decorative. It is
the draft of the branch that will be grafted, so write it as one:

```
[Concept]
├── What it is — <one line>
├── The mechanism — <the thing that makes the rest click>
├── Where it shows up — <2-3 domains>
└── Where it gets misunderstood — <1-2 traps>
```

Then: **next concepts to explore**, grouped by which direction the user might go.

### 3. Follow-up Context

End full explanations with: "What context were you reading about [concept]?" This reveals the learning path and, practically, tells you which map the concept
belongs in.

---

## The Minimap ending (full explanations only)

After a full explanation, offer **once**:

> "Want this grafted onto one of your maps?"

Quick snippets and stories are **never** grafted. Never graft silently, and never nag.

### If yes

1. **Find the home.** List what's there:

```bash
ls maps/
python3 tools/graft.py maps/<Map>.json --list
```

   Propose a specific parent node from that listing — "this belongs under *How it works* in
   `<Map>.json`" — and let the user correct it. Never guess at a title you haven't seen in
   the `--list` output; the graft fails on a title that doesn't match exactly.

2. **Write a compressed fragment**, not the eight sections. A graft is a branch, not a
   document:

```markdown
- <Concept> / <translated term, if the map is bilingual>
  > <2-3 line core definition, bilingual>
  > <1 verified reference, or the search terms if you couldn't verify one>
  - <mechanism — the thing that makes the rest click>
  - <key characteristic>
  - <where it gets misunderstood> {rose}

## Connections
- <Concept> -> <an existing node in that map> (<how they relate>)
```

3. **Check what the graft does to the map's shape.** A concept branch can move a map's centre
   of gravity without tripping the 40% guardrail. `graft.py` prints the branch shares that
   shifted — if a branch jumps by more than about ten points, say so and offer to trim the
   fragment rather than quietly reweighting a map built for other reasons.

4. **Graft it:**

```bash
python3 tools/graft.py maps/<Map>.json <fragment>.md --under "<Parent title>" --dry-run
```

   Read the shape report, then re-run without `--dry-run`. It writes a `.bak.json` alongside,
   so a bad graft is recoverable.

5. **Tell them to re-import.** Minimap holds maps in the browser's localStorage, so editing
   the JSON on disk does **not** change the map they have open. They need **Files ▾ →
   Import** on the edited file, then to delete the stale copy from Files ▾. Say this every
   time — it's the step that silently makes a graft look like it did nothing.

### If no existing map fits

Say so plainly and offer the alternative: "there's no map this belongs to yet — want me to
build one with `/minimap-map`?" Do **not** create a one-concept map as a consolation prize.
A map of a single concept is a note with extra steps, and it clutters `maps/`.

### Minimap-specific writing rules for the fragment

- **`[[Wiki-links]] only to nodes that exist in that map.** Elsewhere a red link is an
  invitation; in Minimap it renders greyed out and goes nowhere. Check `--list` first.
- **Titles under ~40 characters.** A bilingual label eats that fast — short form in the
  title, full gloss in the note.
- **Colour is for traps only** (`{rose}`), if at all. The map is black and white by design.
- **Statuses only if that map uses them.** Don't introduce a tag vocabulary into a map that
  doesn't have one.
- **At least one connection** to something already in the map. A concept grafted with no
  connection is a leaf nobody will find again — the connection is the whole reason to put it
  on a canvas rather than in a note.

---

## Critical Guidelines

### Bilingual Approach (only when a second language is in play)
- Give the term in both languages **in the chat explanation**
- Explain key concepts in both; use standard academic translations for technical terms
- Code-switching is natural and encouraged for clarity
- If the user works in one language only, skip this entirely

**In a graft, the target map's convention wins.** A map records its language convention in
the root note, and its existing node titles show it. Don't drop a bilingual title into a map
whose other fifty nodes are in one language — short form in the title, translated term in
the note. Read
the root note before writing the fragment, and say which convention you followed.

### Link References
**Never cite a link from memory.** For Extension Reading and any URL, use web search / fetch
to verify the paper, link, and year actually exist — a hallucinated DOI is worse than a
search suggestion. If search is unavailable, give search terms instead of links.

Verified links belong in the fragment's note when grafting; unverified ones belong nowhere.

**Format:**
```
Author (Year) - "Title"
Link: https://example.com/paper
Brief: [One sentence]
```

**Search suggestions** when a specific paper isn't available:
```
Search: "<exact phrase>" (2022-2024)
Where: Google Scholar, arXiv, IEEE Xplore
Key authors: <names>
```

### Cross-Domain Connections
Always *try* the adjacent domains identified in Setup, and highlight where they intersect.
These are the best candidates for graft connections, because they're the links a pure
taxonomy would miss.

**A forced domain link is worse than a missing one.** Some concepts genuinely don't reach
every domain. When the connection is a metaphor rather than a mechanism, say so in that many
words — "this one is analogy, not mechanism" — and keep it out of the graft. Dressing a
metaphor up as a cross-domain finding is the failure this section is most prone to, because
an instruction to cover N domains reads like a quota.

### Technology Maturity
Be realistic and specific. Lab demo vs commercial product. Hype vs deployment. Genuine
technical barriers. Evidence-based timelines.

### Tone
Concise but comprehensive · technical but accessible · honest about limitations.

---

## Boundaries with sibling skills

- **One concept, one sitting** — that is this skill. Multi-session learning with lessons and
  progress records belongs to a teaching skill, if one exists in this environment.
- If the "concept" is really a whole field to survey, suggest `/minimap-map` instead — or
  give the quick snippet, then offer the map.
- Paper analysis stays here (Special Cases below) unless it becomes an ongoing project.

---

## Anti-Patterns to Avoid

- Don't give a full explanation when a quick snippet was asked for
- Don't cite sources without links or search guidance
- Don't graft quick snippets or stories
- Don't graft the whole eight sections — a branch is compressed, or it swamps the map
- Don't invent a parent node title; read `--list` first
- Don't wiki-link nodes that aren't in the target map
- Don't create a single-concept map as a fallback
- Don't forget to say the map must be re-imported
- Don't present all concepts as equally mature
- Don't create isolated knowledge — always show connections

---

## Special Cases

### Scientific Paper Analysis
1. Summarize methodology · 2. Key findings (bilingual) · 3. Broader impact · 4. Connect to
what's already mapped · 5. Related papers (verified links). Offer the graft only if the paper
introduced a concept worth keeping, not for every paper.

### Concept Comparison ("A vs B")
1. Define both clearly · 2. Comparison table · 3. Use cases for each · 4. When to choose one
over the other. If grafted, both concepts go in as **siblings under one parent** with a
connection between them labelled with the axis they differ on — that's what makes the
comparison survive on the canvas.

### Implementation Questions ("how to implement X")
1. Theoretical foundation · 2. Practical approach · 3. Frameworks/tools with doc links ·
4. Example applications · 5. Pitfalls. Pitfalls are the part worth grafting.

---

## Example Interaction Pattern

**User:** "<term>"
**Claude:** "Quick snippet, story, or full explanation?"
**User:** "story"
**Claude:** [3-paragraph story] → **Reveal:** <term> — [one paragraph]
*(no graft offer — stories are never grafted)*

---

**User:** "full"
**Claude:** [all 8 sections, Section 8 written as a graftable branch]
"What context were you reading about [concept]?"
"Want this grafted onto one of your maps?"
**User:** "yes, the <X> one"
**Claude:** [`--list` on that map → proposes a parent → writes the fragment → `--dry-run` →
grafts → reports the path, the branch-share shift, and the re-import step]

---

Remember: this skill builds a knowledge graph the user can actually *see*. Every concept
should connect to something already on the canvas, and suggest clear next steps.
