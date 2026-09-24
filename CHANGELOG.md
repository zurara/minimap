# Changelog

## 1.0.2 — 2026-09-24

### Search

- ⌘K search sits at the bottom centre of the screen, with results above the input.
- Search finds free nodes and their children too.
- When you type something, the first row is always **Create "…"**. It makes a free node with
  that title in the middle of the view. The highlight starts on the best match, so Enter still
  jumps; press ↑ to reach Create.

### Connections

- When you finish connecting, the source node stays selected, its detail panel opens, and the
  cursor is in the new connection's label field.
- ⌘-click (or ⌘Enter) while connecting links that node and keeps you connecting, so you can link
  several nodes in one go. A plain click or Enter links the last one; Esc finishes and keeps
  every link made.
- Start typing while connecting to search for the target. **Create and connect "…"** makes a free
  node beside the source and links it.
- The "Pick a target" hint stays on screen for as long as you are connecting.

## 1.0.1 — 2026-09-24

### Notes

- ⌘-click (Ctrl-click) a link in the note editor to open it; ⌘-click a `[[wiki link]]` to jump to
  that node. Holding ⌘ underlines what is clickable.
- The same ⌘-click opens links in notes shown on the map.
- With **Show notes on map** on, the whole note is shown instead of only 3 lines.
- Exported SVG / PNG no longer lets note text spill out of the node box. Long URLs wrap.

### Connections

- The label field suggests labels already used in the map, and lets you create a new one when
  nothing matches. The field is also bigger.
- Connections are faint lines by default. Hover or select a node to draw its connections clearly,
  with their labels.
- The line is now thinner and dash-dot.
- Each label sits in a pill with an arrow that shows which way the connection points.
- Selecting a node opens a connection list on the left, one line per connection (`A label → B`).
  Click a name to jump to it. A button in the top bar hides or shows the list.

### Canvas

- A level slider in the bottom right expands or collapses the whole map to a chosen level.
- Free nodes: ⌘-click an empty spot on the canvas to start one. Connected to a node in the main
  tree, it follows that node and folds with it. Drag it anywhere; drop it on a tree node to make
  it a normal child.
- The **Start here** map now includes a free node, so first-time visitors see one.

### Fixed

- Confirming an empty title with `Enter` could confirm twice and throw an error.

## 1.0.0 — 2026-09-22

First public release.

- One self-contained `mindmap.html`: no install, no account, no network. Maps autosave to the
  browser's `localStorage`.
- Keyboard-first mapping (`Tab`, `Enter`, `Space`, arrows), drag to reorder or reparent, Map and
  Outline views.
- Markdown notes, statuses, tags, cross-branch connections (`⌘L`), search (`⌘K`), fold, undo/redo.
- Light / dark / auto theme; responsive layout with a bottom action bar on phones.
- Export JSON, Markdown, SVG, PNG; import JSON.
- Three agent skills (`minimap-map`, `minimap-decide`, `minimap-concept`) plus the `md2minimap.py`
  and `graft.py` converters, installable on Claude Code, Gemini CLI and Codex.
