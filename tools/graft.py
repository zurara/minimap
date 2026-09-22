#!/usr/bin/env python3
"""Graft a markdown fragment into an existing Minimap JSON map, in place.

Where md2minimap.py creates a new map, this one adds a branch to a map that
already exists — so a concept explanation can join the map it belongs to
instead of becoming a new orphan file.

Usage:
  graft.py <map.json> <fragment.md> --under "<Parent node title>" [--dry-run]
  graft.py <map.json> --list                 # print the map's node titles

The fragment uses the same dialect as md2minimap.py, minus the "# Root" line:

  - Concept name {blue}
    > A note. [[Another node in this map]] links resolve after grafting.
    - child
  ## Connections
  - Concept name -> Some existing node (relates to)

--under matches a node title exactly (case-insensitive); the fragment's
top-level items become that node's children. A backup is written alongside
as <map>.bak.json before anything is changed.
"""
import json, re, shutil, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from md2minimap import convert, report, uid  # same dialect, same id space


def load(path):
    with open(path) as f:
        return json.load(f)


def branch_shares(doc):
    """Node count under each top-level branch, for a before/after comparison."""
    nodes, out = doc['nodes'], {}
    for c in nodes[doc['root']]['children']:
        seen, stack = 0, [c]
        while stack:
            i = stack.pop()
            seen += 1
            stack.extend(nodes[i]['children'])
        out[nodes[c]['title']] = seen
    return out


def find(doc, title):
    want = title.strip().lower()
    for i, n in doc['nodes'].items():
        if (n.get('title') or '').strip().lower() == want:
            return i
    return None


def main(argv):
    if not argv:
        raise SystemExit(__doc__)
    map_path = argv[0]
    doc = load(map_path)

    if '--list' in argv:
        def walk(i, d):
            print('  ' * d + (doc['nodes'][i]['title'] or '(untitled)'))
            for c in doc['nodes'][i]['children']:
                walk(c, d + 1)
        walk(doc['root'], 0)
        return

    if len(argv) < 2 or '--under' not in argv:
        raise SystemExit(__doc__)
    frag_path = argv[1]
    parent_title = argv[argv.index('--under') + 1]
    dry = '--dry-run' in argv

    parent = find(doc, parent_title)
    if not parent:
        titles = ', '.join(sorted((n['title'] or '?') for n in doc['nodes'].values())[:12])
        raise SystemExit(f'No node titled {parent_title!r}. Try --list. First few: {titles}')

    with open(frag_path) as f:
        frag_md = f.read()

    before = branch_shares(doc)
    before_total = max(len(doc['nodes']) - 1, 1)

    # Parse the fragment as a throwaway map under a synthetic root, then move
    # its top-level children onto the real parent.
    sub, unresolved = convert('# __graft_root__\n' + frag_md)

    taken = set(doc['nodes']) | set(sub['nodes'])
    remap = {}
    for i in sub['nodes']:
        remap[i] = i if i not in doc['nodes'] else uid(taken)

    sub_root = sub['root']
    added = []
    for old, new in remap.items():
        if old == sub_root:
            continue
        n = sub['nodes'][old]
        n['id'] = new
        n['children'] = [remap[c] for c in n['children']]
        n['side'] = None
        doc['nodes'][new] = n
        added.append(new)

    new_kids = [remap[c] for c in sub['nodes'][sub_root]['children']]
    doc['nodes'][parent]['children'].extend(new_kids)

    # Connections in the fragment may point at nodes that already existed in
    # the map, so resolve them against the merged document rather than the
    # fragment alone.
    index = {}
    for i, n in doc['nodes'].items():
        index.setdefault((n['title'] or '').strip().lower(), i)
    still = []
    for a, z in unresolved:
        fa, fz = index.get(a.lower()), index.get(z.lower())
        if fa and fz and fa != fz:
            doc['links'].append({'id': uid(taken), 'from': fa, 'to': fz, 'label': ''})
        else:
            still.append((a, z))
    for l in sub['links']:
        doc['links'].append({'id': uid(taken), 'from': remap[l['from']],
                             'to': remap[l['to']], 'label': l['label']})

    have = {s['id'] for s in doc['statuses']}
    for s in sub['statuses']:
        if s['id'] not in have:
            doc['statuses'].append(s)

    # Any status the fragment invented must exist on the doc, or Minimap's
    # normalize() silently clears it from the node.
    have = {s['id'] for s in doc['statuses']}
    for i in added:
        if doc['nodes'][i]['status'] and doc['nodes'][i]['status'] not in have:
            doc['nodes'][i]['status'] = None

    print(f'grafting {len(added)} node(s) under {doc["nodes"][parent]["title"]!r}')
    print(report(doc, still))

    # A graft can shift the map's centre of gravity without tripping the 40%
    # guardrail, so show the branch shares that moved.
    after = branch_shares(doc)
    after_total = max(len(doc['nodes']) - 1, 1)
    moved = [(t, 100 * before.get(t, 0) / before_total, 100 * n / after_total)
             for t, n in after.items()
             if abs(100 * n / after_total - 100 * before.get(t, 0) / before_total) >= 1]
    if moved:
        print('branch share shifted:')
        for t, a, b in moved:
            print(f'  {t[:44]:<46} {a:4.0f}% -> {b:4.0f}%')
    if dry:
        print('(dry run — nothing written)')
        return
    shutil.copy(map_path, re.sub(r'\.json$', '', map_path) + '.bak.json')
    doc['updated'] = int(__import__('time').time() * 1000)
    with open(map_path, 'w') as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
    print(f'wrote {map_path}  (backup: {re.sub(r".json$", "", map_path)}.bak.json)')


if __name__ == '__main__':
    main(sys.argv[1:])
