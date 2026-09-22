# tools

Two scripts for building Minimap maps from markdown, used by the `minimap-map`,
`minimap-decide` and `minimap-concept` skills. Both are stdlib-only Python 3.

## md2minimap.py — markdown to a new map

```bash
python3 tools/md2minimap.py source.md maps/Topic.json --name "Topic"
```

Prints a shape report: node count, depth, per-branch share, labels over 40 characters,
and any connection whose endpoints didn't resolve. Load the result with **Files ▾ →
Import**.

The dialect is a superset of Minimap's own **Export ▾ → Markdown**, so an existing map can
be exported, edited, and converted back in:

```markdown
# Root title
Plain prose here becomes the root node's note.

## A top-level branch
- a node
  > a note on that node
  - a child node
- a node with a status `To do`
- a node with a colour {blue}

## Connections
- Some node -> Another node (label)
```

Two spaces of indent per level. Statuses match the map's presets by label (To do, In
progress, Blocked, Done) and any other label creates a new preset. Colours are the app's
accent tokens: grey, blue, pumpkin, lime, aqua, rose, iris, butter. Connection endpoints
match node titles exactly, case-insensitively.

## graft.py — markdown into a map that already exists

```bash
python3 tools/graft.py maps/Topic.json --list
python3 tools/graft.py maps/Topic.json fragment.md --under "Parent node title" --dry-run
```

Same dialect, minus the `# Root` line. The fragment's top-level items become children of
`--under`. Connections in the fragment resolve against the *merged* map, so a new node can
be linked to one that was already there. Writes `<map>.bak.json` before changing anything.

## Re-importing

Minimap keeps maps in the browser's `localStorage`, so editing a JSON file on disk does not
change a map that is already open. Import the edited file again and delete the stale copy
from **Files ▾** — otherwise you end up with two maps of the same name.
