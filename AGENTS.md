# AGENTS.md

Guidance for AI coding agents working in this folder. Humans: see `README.md` for the app
itself and `tools/README.md` for the converters.

## What this is

Minimap is a single-file mind-mapping app (`mindmap.html`). Maps live in the browser's
`localStorage`, never in the HTML. Alongside it, this folder ships three skills and two
scripts that let an agent **author a map as markdown and hand back an importable JSON file**.

```
mindmap.html          the app — open it in a browser, no build step, no network
skills/               three skills an agent follows (see below)
tools/                md2minimap.py, graft.py — markdown to importable JSON
maps/                 where generated maps land
```

## The one rule that matters

**Never hand-write Minimap JSON.** The format is a flat id-keyed node map with `children`
arrays and separate link records; ids are easy to collide and cross-references are easy to
break, and the app rejects or silently mangles a malformed file. Always write markdown and
run it through `tools/md2minimap.py`.

```bash
python3 tools/md2minimap.py draft.md maps/Topic.json --name "Topic"
```

The converter prints a shape report — node count, depth, per-branch share, labels over 40
characters, unresolved connections. **Read it.** It is how the skills' size and legibility
rules get checked rather than merely hoped for.

To add to a map that already exists, use `tools/graft.py` instead; it writes a backup first
and reports which branch shares moved.

## The three skills

| Skill | Produces | Use when |
|---|---|---|
| `skills/minimap-map` | `maps/<Topic>.json` | Mapping a field, a domain, a learning path |
| `skills/minimap-decide` | `maps/decision-<slug>.json` | Weighing one specific choice |
| `skills/minimap-concept` | a branch grafted into an existing map | Explaining one concept, then keeping it |

Each `SKILL.md` is self-contained: read the whole file before drafting. They are not
interchangeable — `minimap-map` structures a *field*, `minimap-decide` structures a *choice*,
and swapping them produces a map with the wrong shape.

### Installing them

`SKILL.md` is an open format, so the `skills/` folder is read by most agents as it stands. Two
install it in one command, converters included:

```bash
# Claude Code — this repo is its own marketplace
/plugin marketplace add zurara/minimap
/plugin install minimap@minimap

# Gemini CLI
gemini extensions install https://github.com/zurara/minimap
```

Installed that way, `${CLAUDE_PLUGIN_ROOT}/tools/` (or the extension's own directory) holds the
converters, and maps are written to `maps/` in the working directory.

Working from this folder instead, symlink rather than copy, so there is one source of truth:

```bash
ln -s "$PWD/skills/minimap-map" ~/.claude/skills/minimap-map
ln -s "$PWD/skills/minimap-decide" ~/.claude/skills/minimap-decide
ln -s "$PWD/skills/minimap-concept" ~/.claude/skills/minimap-concept
```

Then `tools/` and `maps/` resolve relative to this folder, so run with it as the working
directory.

## Things agents get wrong here

**`[[Wiki-links]] are in-map, not cross-file.** In a notes vault `[[X]]` opens another file,
and a link to something that doesn't exist yet is a useful invitation. In Minimap, `[[X]]` in
a node's *note* jumps to another node **in the same map**, matched on exact title, and
renders greyed out if nothing matches. Linking a topic that isn't in the map produces a dead
end, not a promise.

**Editing a JSON file does not change an open map.** The app loaded it into `localStorage`.
After any edit or graft, the user must **Files ▾ → Import** the file again — and then delete
the stale copy, because importing adds a second map rather than updating the first. Say this
every time; it's the step that makes an edit look like it did nothing.

**Structure follows the subject.** Don't open every map with `Concepts / Mechanisms /
Practices / Traps` as top-level branches. That template makes every map feel the same. The
exception is `minimap-decide`, where a fixed eight-facet shape is the point, because it makes
two decisions comparable.

**Connections are not decoration.** A map with only parent-child edges is a tree, and the app
already draws trees. 2–6 cross-branch connections are what make it a map.

**Black and white is the default.** Colour is one semantic axis per map at most, and status
tags belong only on maps that will actually be worked through.

**Long titles wrap into tall cards and turn the canvas to mush.** Keep node titles under
~40 characters; put the elaboration in the node's note. The converter lists every label that
breaks this.

## If you can't ask the user

The skills contain questions meant for a human — which tier, which language, which facts are
missing. Running unattended, don't stall and don't silently guess: take the documented
default, record it in the map's attribution line (the root node's note), and state in your
report which defaults you took and what would change if they're wrong. For missing *facts*
specifically, put the gap in the map as a node rather than inventing a value.

## Verifying your output

The report from `md2minimap.py` is the first check. To confirm a file actually loads, open
`mindmap.html` over `http://` rather than `file://` (some browsers block `localStorage` on
`file://`; the app then shows "no autosave"):

```bash
python3 -m http.server 8781
```

Then **Files ▾ → Import**. A map that imports, fits on screen, and shows its connections is
working; there is no separate test suite.
