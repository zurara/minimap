---
name: minimap-decide
description: Build a decision map as an importable Minimap JSON file that surfaces tradeoffs, hidden costs, exit options, and legal exposure for a specific choice - without ever making the decision for the user. Use whenever they are weighing a purchase, signing a contract, committing time, taking a job, or making any meaningful choice where they'd benefit from seeing what's NOT on the price tag, and want it on the Minimap canvas rather than in chat. Trigger on "/minimap-decide", "decision map for X", "should I buy/sign/take/commit", "help me decide whether", "weighing X", or any framing where a specific choice is on the table. Distinct from /minimap-map - that structures a field of knowledge, this structures a specific choice.
---

# minimap-decide

Build a decision map for a specific choice, as an importable Minimap JSON file at
`maps/decision-<slug>.json`. The user opens it with **Files ▾ → Import** and sits with it on
the canvas.

The skill's job is to surface what's *not* on the price tag: hidden costs, time costs, exit
options, legal traps, alternatives they may not be weighing. It does **NOT** make the
decision for them.

---

## Setup

Paths are relative to the Minimap folder — the one holding the app
(`index.html`, or `mindmap.html` in a shared copy) alongside `tools/` and `maps/`:

| | |
|---|---|
| Decision maps | `maps/decision-<slug>.json` |
| Converter | `tools/md2minimap.py` |

Installed through an agent there is no such folder. The converters still ship alongside the
skills, so every `tools/...` path below means `${CLAUDE_PLUGIN_ROOT}/tools/...` in Claude Code,
and elsewhere `tools/` resolved from this file's own location — `../../tools/`. `maps/` is then
a folder in the working directory; create it if it is not there.

**Jurisdiction matters for the Legal facet.** If the user's jurisdiction is known from
context, use it and name it. If it isn't, ask — or, if you can't ask, write the Legal facet
in terms of clause *categories* only and flag the jurisdiction as an open question. Never
assert the law of a country you're guessing at.

---

## The core principle — never decide for them

This is the most important rule in the skill and the easiest to violate.

The skill **lists possibilities, surfaces tradeoffs, and names hidden factors**. It does NOT:
- Recommend doing or not doing the thing
- Score options or produce verdicts
- Use language like "I'd suggest you..." or "the better choice is..."
- Conclude with a summary that tilts toward one option

When asked "so should I do it?" after seeing the map, **mirror back the decision shape —
don't give a verdict**:

> "Based on the map, the decision hinges mostly on [the one or two facets that most
> differentiate the options]. The strongest factor for is [X]; the strongest against is [Y].
> What do you weight most heavily?"

Never say "I think you should..." or "the answer is..." Even under pressure. Especially
under pressure — that's exactly when the reflection is worth more than a verdict.

**Exception for honesty:** if a section reveals something objectively concerning (a clearly
predatory clause, an obviously hidden cost, a badly under-disclosed risk), name it plainly.
"This clause auto-renews and requires 90 days' written notice to cancel — easy to miss" is a
fact, not a verdict.

### The visual corollary — colour must not smuggle in a verdict

Minimap gives you colour and status tags. Used carelessly they become scoring by other
means: green "pros" against red "cons" is a verdict in disguise, and it lands harder than a
sentence would because it's read at a glance before anything is read carefully.

**Colour encodes epistemic status, never valence.** The only permitted scheme:

| Token | Meaning | Where |
|---|---|---|
| `rose` | **An unverified assumption or a gap** — something the map asserts that should be checked before being relied on | any facet |
| `iris` | **A legal red flag** — a clause category worth pausing on | Legal exposure only |
| *(no colour)* | everything else | everywhere |

No colour for "good" and no colour for "bad". If you catch yourself colouring a node because
it argues for or against, stop — that's the skill's hard line being crossed through the
palette.

**Status tags turn the map into a pre-decision checklist**, which is the one thing chat
output can't do:

| Status | Meaning |
|---|---|
| `To do` | a fact to verify or obtain before deciding |
| `In progress` | being chased |
| `Blocked` | can't be found out — the decision has to be made without it |
| `Done` | verified |

Tag only nodes that are genuinely actionable-before-deciding. A map where every node is
`To do` is noise.

---

## Authoring pipeline — markdown in, JSON out

Do **not** hand-write the JSON.

1. Write the map as markdown to a scratch file.
2. Convert:

```bash
python3 tools/md2minimap.py <scratch>.md maps/decision-<slug>.json --name "<Decision as a question>"
```

3. Read the shape report. Two numbers matter:
   - **Branch balance** — if one facet holds more than ~40% of the map, the space itself is
     an implied verdict. Trim it, or deepen the thin ones.
   - **Total nodes** — see the size budget below.
4. Hand over the path and the **Files ▾ → Import** step.

### Size, and why a decision map is smaller than a knowledge map

**Budget: 30–45 nodes, depth 3.** A knowledge map is a reference you return to; a decision
map is something to hold in your head at the moment of deciding. Past roughly 45 nodes it
stops being a map of a decision and becomes a research report that happens to be drawn as a
tree — and a map you can't take in at a glance has failed at its one job.

If a facet needs more than that, the extra belongs in a **note** on a node, not in more
nodes. Notes are read on demand; nodes are read all at once.

**Group inside a facet — don't flatten it.** Eight siblings under "Real cost" is a list. The
same eight under `Sticker` / `Hidden ongoing` / `Time cost` / `Opportunity cost` is a
structure that shows which kind of cost is which, and it's what makes two decision maps
comparable to each other. Depth 3 (facet → group → item) is the working shape; depth 2
across the whole map means the grouping step was skipped.

### The markdown dialect

```markdown
# <Decision stated as a question>
decision type: <primary> · reversibility: Type <1|2> · mode: <single-option|comparison>

## What you're actually getting
- <factual core>
  > <a note with detail, if it needs one>

## Real cost
- Sticker
  - <price> `Done`
- Hidden ongoing
  - <item>: <estimate> {rose}
  - <item>: <estimate>

## Connections
- <From node title> -> <To node title> (<label>)
```

Two spaces per indent level. `## Heading` is a facet. `` `Label` `` sets status, `{token}`
sets colour, `> ` lines are notes. The attribution line goes in the prose under `# `, which
becomes the root node's note.

### Connections — the thing chat output couldn't do

A decision's real shape is in how facets *interact*, and a linear document can only hint at
it. Draw 2–5 connections across facets, labelled with the interaction:

```markdown
## Connections
- Realistic probability -> Opportunity cost (if you don't follow through, this is what it cost)
- Type 1 — one-way door -> Termination and notice terms (no ordinary exit, so this clause carries the weight)
- Resale value -> Depreciation is front-loaded (the exit price is set here)
```

This is the strongest reason to put a decision on a canvas rather than in chat. A map with
no connections is a checklist; the connections are what make the tradeoffs visible.

---

## The universal facet set (eight facets, all always present)

All eight, in this order, as the eight top-level branches. The order matters — Reversibility
second sets the weight on everything else; Counterfactuals last forces explicit comparison
to alternatives including doing nothing.

*(Unlike `/minimap-map`, where a fixed facet template is an anti-pattern, here the fixed set
is the point: decisions are worth comparing to each other, and that needs a stable shape.)*

**A facet may be brief if there's genuinely little to say** — but it must be present, and a
brief facet must say *why* ("No significant legal exposure — informal arrangement, no
written contract") rather than be omitted. Omitting a facet hides exactly the thing the
skill exists to surface. On a canvas an omitted facet is worse than in a document: the map
reads as complete, so a missing branch looks like a settled question rather than a gap.

### 1. What you're actually getting
- The core thing, stripped of marketing language
- What the seller emphasizes vs. what will actually be used
- One or two nodes, factual

### 2. Reversibility
- **Type 1 (one-way door)** or **Type 2 (two-way door)**?
- Type 1 = hard or expensive to reverse (a multi-year commitment, a major relocation, a
  custom-fitted purchase, anything with no ordinary right of termination)
- Type 2 = easy to reverse (most purchases, most subscriptions, refundable bookings)
- Name *which* and *why* — this sets the weight on everything below
- If Type 1, be more thorough on Legal and Risk; if Type 2, brevity is fine

### 3. Real cost
- **Sticker price** — the obvious number. Check whether it's quoted net or gross of tax;
  that alone can move the total by a double-digit percentage.
- **Hidden ongoing costs** — maintenance, insurance, fees, subscriptions, taxes, fuel,
  storage, upgrade pressure
- **Time cost** — hours required to extract the value, including travel
- **Opportunity cost** — concrete and specific to this person's situation, not abstract

The total cost picture should make the sticker price look small if it should — and it
usually should.

### 4. Value you'll actually capture
Distinct from value on offer. A course offers X hours of instruction; that value is captured
only if they attend and engage.
- **What they'd need to do** to realize it — concrete actions
- **Realistic probability they'll do those things** — honest, using past patterns if the
  user has shared them. Use only patterns they actually told you; don't invent a history.
- **Where value erodes** — over time, with neglect, if conditions change

### 5. Exit options
- **Resale value curve** — depreciation pattern
- **Cancellation / termination terms** — notice periods, fees, conditions
- **Lock-in** — switching costs, data lock-in, contract lock-in

Brief for Type 2; for Type 1 it's the most important facet after Legal.

### 6. Risk
What could go wrong, with rough likelihood — one node per risk, mitigation in its note:
**Mechanical / quality**, **Financial**, **Counterparty**, **Relational / social**.

### 7. Legal exposure
**The first node of this facet is always:** `Not a lawyer — verify anything significant with one`

Then:
- **Clause categories to look for** — auto-renewal, termination and notice, jurisdiction,
  liability caps, indemnification, exclusivity, IP assignment, non-compete
- **Jurisdiction-specific traps** — only if the jurisdiction is known. Typical axes worth
  checking: statutory caps on contract term and renewal, minimum notice periods, cooling-off
  or withdrawal rights, consumer-vs-business status (protections often apply only to
  consumers), and tax treatment that turns on employment status.
- **Red flags worth pausing on** — mark these `{iris}`

The skill surfaces categories and flags; it does not interpret specific clauses as legal or
illegal.

### 8. Counterfactuals
- **Do nothing** — what happens if they don't do this at all?
- **Cheaper version** — is there a 70%-as-good option for 30% of the cost?
- **Wait** — does 3/6/12 months change the picture?
- **Different option entirely** — the adjacent thing people choose instead

At least 2–3. The do-nothing option is almost always relevant and almost always missed.

---

## Decision types

Most decisions blend types. Identify the primary type, emphasize its facets, always cover
all eight.

| Type | Examples | Facets to emphasize |
|---|---|---|
| **purchase** | a vehicle, a laptop, equipment, furniture | Real cost (depreciation), Exit (resale), Risk (mechanical) |
| **subscription / recurring** | a gym, software, platform fees | Real cost (true annual), Value capture (usage threshold), Exit (cancellation) |
| **contract / commitment** | a lease, employment, partnership | Reversibility (often Type 1), Legal, Exit (termination) |
| **investment of time** | a course, a language, a project, a certification | Time cost, Value capture (follow-through), Counterfactuals |

Name the primary type in the attribution line (the root note).

---

## Modes

**Single-option (default).** The map analyzes one option on its merits; do-nothing is covered
in Counterfactuals.

**Comparison.** Triggered by an explicit comparison ("X vs Y", "this job vs my current one").
The eight facets stay, and each holds side-by-side analysis:

```markdown
## Real cost
- Option A
  - Sticker: …
  - Insurance: …
- Option B
  - Sticker: …
  - Insurance: …
```

**Keep the two sub-branches the same size.** In a document, unequal length reads as
thoroughness; on a canvas it reads as a recommendation. If one option genuinely has less to
say, say *that* in a node rather than letting the whitespace argue.

The skill still does not pick a winner.

---

## Pre-flight check (BEFORE drafting)

**If you can't ask the gap-filling questions** — running unattended, or in a background
agent — don't stall. Put each unknown into the map as a `{rose}` node tagged `To do`, and
say in your report which answers would most change the picture. An unasked question is a
node; it is never an invented fact.

1. **What is the specific decision?** State it as a yes/no or A-vs-B question, not a vague
   topic. This becomes the root node title, so keep it under ~60 characters and put the full
   framing in the root note.
2. **What decision type?** (purchase / subscription / contract / time-investment, or blend)
3. **Type 1 or Type 2?** This affects depth and tone.
4. **What has the user already told you?** Use context they've given — budget, constraints,
   past similar decisions. Don't infer personal facts they haven't stated.
5. **What's the do-nothing baseline?**
6. **Are there obvious factual gaps?** Name them as gaps; don't invent.
7. **Which 2–5 cross-facet interactions become connections?**

Hallucinating specifics — contract clauses, product defects, tax rates — is the worst
failure mode. Better to flag the gap.

---

## When to web-search

Decisions benefit from search more than knowledge maps do, because they are situated in *now*
and *here*. Search when current prices or fees matter, when jurisdiction-specific law
applies, when it's a specific product with known issues, when recent reviews matter, or when
the counterparty is an unfamiliar company.

Don't search when the decision is purely personal (career fit, relationships, time
priorities) or when the structure of the decision is what matters rather than external facts.

When in doubt, search once. A 30-second search beats a 30-minute regret.

---

## Ephemerality — enforced, not automatic

Decision maps are **tools for a moment, not knowledge artifacts** — the decision happens in
the user's head, not in their notes. Because this one writes a file, the ephemerality has to
be deliberate:

- Write to `maps/decision-<slug>.json` — the `decision-` prefix marks it as disposable and
  keeps it sorted away from knowledge maps.
- When handing it over, say once that it's disposable: after deciding, delete it from
  **Files ▾** (the trash icon on its row) and delete the JSON.
- **Never** offer to keep it, expand it into a knowledge map, or link it from one.

---

## Refinement loop

After the map, **invite challenge**:

> Things you might want to push back on:
> - Anything I got factually wrong (prices, terms, clauses)
> - A facet that feels under-developed (often Legal or Risk)
> - A counterfactual I missed
> - Something that should be weighted higher than I've implied by space alone
> - A connection that isn't real, or one I missed

When they push back on a facet, regenerate just that branch and re-convert. Re-importing
adds a new map rather than updating the open one, so the previous one should be deleted from
Files ▾ — say this once, on the first refinement.

**If pressed for a verdict**, do not give one:

> "Based on the map, the decision hinges on [the 1-2 facets that most differentiate this].
> Strongest factor *for*: [X]. Strongest *against*: [Y]. What do you weight most?"

Hard line. The skill never crosses it.

---

## What this skill does NOT do

- **Make the decision.** Ever. Even when asked. Mirror back instead.
- **Score options.** No 7/10s, no pros-and-cons tallies, no winners — and no colour-coding
  that does it visually.
- **Pad empty facets.** If Legal really doesn't apply, say so briefly.
- **Hide gaps.** Missing fact → a `{rose}` node tagged `To do`, never a confabulation.
- **Infer personal facts.** Employment status, income, health, household — use only what the
  user has stated. A guess in a decision map propagates into every facet that depends on it.
- **Keep the map.** Disposable by design; remind them to delete it once decided.
- **Write JSON by hand.** Always through `tools/md2minimap.py`.

---

## Quick reference — invocation flow

1. **Hear the request** — "/minimap-decide", "should I buy/sign/take X", or contextual weighing
2. **State the decision as a question** — this is the root node
3. **Identify decision type** and **reversibility** (Type 1 / 2)
4. **Identify gaps** — ask, or web-search, or flag them as `{rose}` + `To do`
5. **Run the pre-flight check** — seven questions, including connections
6. **Write the markdown** — eight facets in order, grouped not flat, attribution in the root note, statuses on what must be verified, `{rose}` on gaps, `{iris}` on legal red flags
7. **Convert** into `maps/decision-<slug>.json`
8. **Read the shape report** — 30–45 nodes, depth 3, no facet over 40%. An oversized facet
   is an implied verdict; a flat facet is an ungrouped list; an oversized map is a report.
9. **Hand over the path**, the Files ▾ → Import step, and the once-only note that it's disposable
10. **Invite challenge**; refine single facets and re-convert
11. **If pressed for a verdict** — mirror back the decision shape, never give one

---

## Optional close-out — the decision retrospective

The map itself is disposable. But judgment is worth systematizing — so after the user has
actually decided (not before, and only if they tell you the outcome), offer once to log it:
one line on what was chosen, two on why, and one falsifiable check-back question with a date.

If yes, append a short entry (5 lines max) to `maps/decisions.md` — a plain markdown log,
**not** a map. If no, drop it — never nag, never save silently.
