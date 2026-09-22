#!/usr/bin/env python3
"""Convert a markdown outline into a Minimap-importable JSON document.

Accepts two dialects at once, so both hand-written maps and Minimap's own
Markdown export parse without editing:

  # Root title            -> root node
  (plain lines after it)  -> root note
  ## Branch               -> a top-level branch (child of root)
  - node                  -> node; two spaces of indent per level
    > note line           -> note on the node above
  - node `Done`           -> trailing backtick tag sets the node's status
  - node {blue}           -> trailing braces set the node's colour token
  ## Connections          -> cross-branch links: "- A -> B (label)"

Usage:  md2minimap.py in.md [out.json] [--name "Map name"]
Writes JSON and prints a shape report (node count, depth, branch balance).
"""
import json, random, re, string, sys, time

ACCENTS = {'grey','blue','pumpkin','lime','aqua','rose','iris','butter'}
DEF_STATUS = [
    {'id':'todo','label':'To do','color':'grey'},
    {'id':'doing','label':'In progress','color':'blue'},
    {'id':'blocked','label':'Blocked','color':'rose'},
    {'id':'done','label':'Done','color':'lime'},
]
SPARE = ['pumpkin','aqua','iris','butter']


def uid(seen):
    alphabet = string.ascii_lowercase + string.digits
    while True:
        u = ''.join(random.choice(alphabet) for _ in range(7))
        if u not in seen:
            seen.add(u)
            return u


class Build:
    def __init__(self):
        self.seen = set()
        self.nodes = {}
        self.statuses = [dict(s) for s in DEF_STATUS]
        self.by_label = {s['label'].lower(): s['id'] for s in self.statuses}

    def node(self, title, status=None, color=None):
        i = uid(self.seen)
        self.nodes[i] = {'id': i, 'title': title, 'note': '', 'children': [],
                         'collapsed': False, 'color': color, 'side': None,
                         'status': status}
        return i

    def status_id(self, label):
        key = label.strip().lower()
        if key in self.by_label:
            return self.by_label[key]
        sid = re.sub(r'[^a-z0-9]+', '-', key).strip('-') or uid(self.seen)
        color = SPARE[len(self.statuses) % len(SPARE)]
        self.statuses.append({'id': sid, 'label': label.strip(), 'color': color})
        self.by_label[key] = sid
        return sid


def strip_frontmatter(lines):
    if lines and lines[0].strip() == '---':
        for i in range(1, len(lines)):
            if lines[i].strip() == '---':
                return lines[i + 1:]
    return lines


def parse_suffix(text, b):
    """Pull a trailing `Status` tag and/or {color} token off a node title."""
    status = color = None
    for _ in range(2):
        m = re.search(r'\s*\{([a-z]+)\}\s*$', text)
        if m and m.group(1) in ACCENTS:
            color = m.group(1)
            text = text[:m.start()]
            continue
        m = re.search(r'\s*`([^`]+)`\s*$', text)
        if m:
            status = b.status_id(m.group(1))
            text = text[:m.start()]
            continue
        break
    return text.strip(), status, color


def convert(md, name=None):
    b = Build()
    lines = strip_frontmatter(md.splitlines())

    root = None
    root_note = []
    stack = []          # [(indent, node_id)] for list nesting
    branch = None       # current "## Branch" node, if any
    last = None         # node that a "> note" line attaches to
    conn_mode = False
    conns = []          # (from_title, to_title, label)

    for raw in lines:
        line = raw.rstrip()
        if not line.strip():
            continue
        indent = len(line) - len(line.lstrip(' '))
        s = line.strip()

        m = re.match(r'^#\s+(.*)$', s)
        if m:
            title, st, col = parse_suffix(m.group(1), b)
            root = b.node(title, st, col)
            stack, branch, last, conn_mode = [], None, root, False
            continue

        m = re.match(r'^##\s+(.*)$', s)
        if m:
            head = m.group(1).strip()
            if head.lower().strip(':') in ('connections', 'links'):
                conn_mode = True
                stack, branch, last = [], None, None
                continue
            if root is None:
                root = b.node('Untitled map')
            title, st, col = parse_suffix(head, b)
            branch = b.node(title, st, col)
            b.nodes[root]['children'].append(branch)
            stack, last, conn_mode = [], branch, False
            continue

        m = re.match(r'^[-*+]\s+(.*)$', s)
        if m:
            body = m.group(1)
            if conn_mode:
                cm = re.match(r'^(.*?)\s*(?:->|→|-->)\s*(.*?)\s*(?:\(([^()]*)\))?\s*$', body)
                if cm:
                    conns.append((cm.group(1).strip(), cm.group(2).strip(),
                                  (cm.group(3) or '').strip()))
                continue
            if root is None:
                root = b.node('Untitled map')
            if re.match(r'^\[[ xX]\]\s', body) is None:
                title, st, col = parse_suffix(body, b)
            else:
                title, st, col = body.strip(), None, None
            nid = b.node(title, st, col)
            while stack and stack[-1][0] >= indent:
                stack.pop()
            parent = stack[-1][1] if stack else (branch if branch else root)
            b.nodes[parent]['children'].append(nid)
            stack.append((indent, nid))
            last = nid
            continue

        m = re.match(r'^>\s?(.*)$', s)
        if m:
            if last:
                note = b.nodes[last]['note']
                b.nodes[last]['note'] = (note + '\n' if note else '') + m.group(1)
            continue

        # Plain prose directly under "# Root" becomes the root's note.
        if root is not None and not stack and branch is None and last == root:
            root_note.append(s)

    if root is None:
        raise SystemExit('No "# Title" line found — a map needs a root.')
    if root_note:
        b.nodes[root]['note'] = '\n'.join(root_note)

    # Balance the root's children across the two sides.
    kids = b.nodes[root]['children']
    for i, c in enumerate(kids):
        b.nodes[c]['side'] = 'right' if i % 2 == 0 else 'left'

    # Resolve connections by exact title (case-insensitive), first match wins.
    index = {}
    for i, n in b.nodes.items():
        index.setdefault(n['title'].strip().lower(), i)
    links, unresolved = [], []
    for a, z, label in conns:
        fa, fz = index.get(a.lower()), index.get(z.lower())
        if fa and fz and fa != fz:
            links.append({'id': uid(b.seen), 'from': fa, 'to': fz, 'label': label})
        else:
            unresolved.append((a, z))

    used = {n['status'] for n in b.nodes.values() if n['status']}
    doc = {
        'id': uid(b.seen),
        'name': name or b.nodes[root]['title'],
        'created': int(time.time() * 1000),
        'updated': int(time.time() * 1000),
        'root': root,
        'nodes': b.nodes,
        'statuses': [s for s in b.statuses
                     if s['id'] in used or s['id'] in ('todo','doing','blocked','done')],
        'links': links,
        'view': None,
    }
    return doc, unresolved


def report(doc, unresolved):
    nodes, root = doc['nodes'], doc['root']
    depth = {}

    def walk(i, d):
        depth[i] = d
        for c in nodes[i]['children']:
            walk(c, d + 1)
    walk(root, 0)

    assert root in nodes, 'root missing from nodes'
    for i, n in nodes.items():
        for c in n['children']:
            assert c in nodes, f'node {i} points at missing child {c}'
    assert len(depth) == len(nodes), \
        f'{len(nodes) - len(depth)} orphan node(s) unreachable from the root'

    total = len(nodes)
    out = [f'{total} nodes · depth {max(depth.values())} · {len(doc["links"])} connections']
    kids = nodes[root]['children']
    if kids:
        for c in kids:
            n = sum(1 for i in depth if i == c or _under(nodes, c, i))
            share = 100 * n / max(total - 1, 1)
            flag = ('  <- over 40% of the map, consider splitting'
                    if share > 40 and total >= 20 else '')
            out.append(f'  {nodes[c]["title"][:44]:<46} {n:>3} nodes  {share:4.0f}%{flag}')
    long = [n['title'] for n in nodes.values() if len(n['title']) > 40]
    if long:
        out.append(f'{len(long)} label(s) over 40 chars: ' + '; '.join(t[:50] for t in long[:3]))
    if unresolved:
        out.append('unresolved connections (no node with that exact title): '
                   + '; '.join(f'{a} -> {z}' for a, z in unresolved))
    return '\n'.join(out)


def _under(nodes, top, target):
    stack = list(nodes[top]['children'])
    while stack:
        i = stack.pop()
        if i == target:
            return True
        stack.extend(nodes[i]['children'])
    return False


if __name__ == '__main__':
    args = [a for a in sys.argv[1:]]
    name = None
    if '--name' in args:
        k = args.index('--name')
        name = args[k + 1]
        del args[k:k + 2]
    if not args:
        raise SystemExit(__doc__)
    src = args[0]
    dst = args[1] if len(args) > 1 else re.sub(r'\.md$', '', src) + '.json'
    with open(src) as f:
        doc, unresolved = convert(f.read(), name)
    with open(dst, 'w') as f:
        json.dump(doc, f, indent=2, ensure_ascii=False)
    print(dst)
    print(report(doc, unresolved))
