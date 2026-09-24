# Minimap

[![Minimap](https://zurara.github.io/minimap/screenshot.png)](https://zurara.github.io/minimap/)

`mindmap.html` is the whole app: one file, no install, no account, no internet.

Project page: <https://zurara.github.io/minimap/>. Anything broken:
<https://github.com/zurara/minimap/issues>. What changed in each version: `CHANGELOG.md`.

**Open it** by double-clicking. It works offline — everything, including the icons, is inside that
one file. Nothing is ever sent anywhere.

The top bar shows **Saved locally** — hover it to see exactly where your work is kept, and what
that does and does not guarantee.

**Your maps live in your own browser** (`localStorage`), not in the file and not on a server. That
means:

- Maps you make are visible only to you, on that browser, on that machine.
- Sending this file to someone else sends the app, never your maps.
- Clearing site data, or opening it in a different browser, gives you an empty start.

So for anything you care about, use **Export ▾ → JSON**. That file is the real backup, and
**Import JSON** brings it back — including on someone else's copy, which is how you hand a map to
another person.

## Building maps with an AI agent

This folder also carries three skills and two small Python scripts, so an agent can write a map
for you instead of you typing it node by node. It drafts the map as an indented outline, converts
it, and hands you a JSON file to **Import**.

- `skills/minimap-map` — map a field
- `skills/minimap-decide` — map one decision, without it picking for you
- `skills/minimap-concept` — explain one concept, then add it to a map you already have

Point your agent at **`AGENTS.md`**; it explains the format, the scripts, and the mistakes agents
usually make here. Nothing in this is required — the app works on its own.

### Installing the skills

`SKILL.md` is an open format that around forty agents now read, so the `skills/` folder works
anywhere. The shortest line per tool:

```bash
# Claude Code — this repo is its own marketplace
/plugin marketplace add zurara/minimap
/plugin install minimap@minimap

# Gemini CLI
gemini extensions install https://github.com/zurara/minimap

# Codex — one directory per skill under ~/.codex/skills
mkdir -p ~/.codex/skills && git clone https://github.com/zurara/minimap ~/.minimap && ln -s ~/.minimap/skills/* ~/.codex/skills/

# anything else
git clone https://github.com/zurara/minimap
```

However it lands, the converters in `tools/` come along — that is the part the skills actually
need. Point the agent at `AGENTS.md` and it will find them.

Chrome and Firefox both autosave for a file opened from disk, so double-clicking is enough.

If the top bar says **No autosave**, the page was not opened as a real page — usually it is still an
attachment or a preview, which browsers give no origin and therefore no storage. Save the file
somewhere on your computer first, then open that file. (Safari does not allow storage for local
files at all; use Chrome or Firefox.)

## Getting started

The map you see on first run explains itself. The short version:

| | |
|---|---|
| `Tab` | new child |
| `Enter` | new sibling |
| `Space` | rename — or just start typing |
| `⌘Enter` | notes (markdown) |
| `⌘L` | connect two nodes across branches |
| `⌘`-click canvas | start a free node |
| `⌘`-click a link | open it, or jump to a `[[wiki link]]` |
| `?` | every shortcut |

Drag a node above or below another to reorder it, or onto it to make it a child.

## On a phone or tablet

The app is responsive: below 640px the top bar keeps Files, the map name and Map/Outline, and
everything else moves into the **⋯** menu. A **bottom action bar** replaces the keyboard — child,
sibling, indent, outdent, fold, detail, link, delete, undo, redo, find, fit. It scrolls sideways,
and it swaps to Done / Sibling / Child while you are typing a title, so you can outline a whole
tree with one thumb.

| | |
|---|---|
| tap | select a node |
| tap it again | edit the title |
| **hold** a node | open the detail panel |
| drag a node | reorder or reparent |
| **hold** a row | pick it up in Outline (a plain drag scrolls the list) |
| drag the canvas | pan |
| pinch | zoom — two fingers also pan |

## License

MIT — see `LICENSE`.

Two things in here are not mine: the app's interface icons are
[RemixIcon](https://remixicon.com) 4.6.0 (Apache-2.0), inlined into `mindmap.html`, and the
drawings on the project page are [Khushmeen's](https://khushmeen.com/icons.html).
