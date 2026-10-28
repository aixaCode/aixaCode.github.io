#!/usr/bin/env python3
"""Render editable graph specifications as responsive notebook SVGs."""
import base64
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VERSION = 'v6'
METRICS = json.loads((ROOT / 'design/font-metrics.json').read_text())
FONT = base64.b64encode((ROOT / 'site/assets/fonts/dm-sans-latin.woff2').read_bytes()).decode()
INK, MUTED, EDGE, ACCENT, PAPER = '#4c332c', '#6f5649', '#84685b', '#a04637', '#fff8ef'
# Colour carries meaning: what a box is, never where it sits.
ROLES = {
    'input': ('#e0eaf0', EDGE, ''),      # sources and starting points
    'step': ('#fdf2e6', EDGE, ''),       # ordinary process step
    'human': ('#e9e1f1', EDGE, ''),      # a person decides or verifies
    'safe': ('#e3ead8', EDGE, ''),
    'caution': ('#f6e9c9', EDGE, ''),
    'risk': ('#f3d9cf', EDGE, ''),
    'key': ('#f7ddd2', ACCENT, ''),      # the one node the reader should remember
    'open': (PAPER, EDGE, '9 7'),        # unanswered or optional
    'excluded': ('url(#hatch)', EDGE, '9 7'),
}
esc = html.escape


def measure(text, size, bold=False):
    return sum(METRICS.get(c, .7) for c in text) * size * (1.06 if bold else 1)


def wrap(text, width, size, bold=False):
    out = []
    for part in text.split(' / '):
        line = ''
        for word in part.split():
            candidate = (line + ' ' + word).strip()
            if line and measure(candidate, size, bold) > width:
                out.append(line)
                line = word
            else:
                line = candidate
        if line:
            out.append(line)
    return out


class Canvas:
    def __init__(self, mobile):
        self.mobile = mobile
        self.h_size, self.d_size = (34, 29) if mobile else (29, 25)
        self.h_step, self.d_step = (42, 37) if mobile else (37, 32)
        self.boxes, self.paths, self.extra = {}, [], []

    def box_size(self, node, width):
        head = wrap(node['label'], width - 44, self.h_size, True)
        detail = wrap(node.get('detail', ''), width - 44, self.d_size)
        height = 44 + len(head) * self.h_step + (len(detail) * self.d_step + 6 if detail else 0)
        return head, detail, max(height, 104 if self.mobile else 96)

    def place(self, node, x, y, width, height=None):
        head, detail, h = self.box_size(node, width)
        self.boxes[node['id']] = dict(x=x, y=y, w=width, h=height or h, head=head, detail=detail,
                                      role=node.get('role', 'step'))
        return height or h

    def arrow(self, d, dashed=False, edge=None):
        self.paths.append((d, dashed, edge))


def edge_list(graph):
    return [(e[0], e[1], len(e) > 2 and e[2] == 'optional') for e in graph['edges']]


def ranks(graph):
    ids = [n['id'] for n in graph['nodes']]
    forward = [(a, b) for a, b, _ in edge_list(graph) if ids.index(a) < ids.index(b)]
    rank = {i: 0 for i in ids}
    for i in ids:
        incoming = [rank[a] + 1 for a, b in forward if b == i]
        if incoming:
            rank[i] = max(incoming)
    # Pull pure sources next to the node they feed so side inputs do not cross other columns.
    for i in ids:
        targets = [rank[b] for a, b in forward if a == i]
        if targets and not any(b == i for a, b in forward):
            rank[i] = min(targets) - 1
    return rank


def flow(graph, c):
    nodes = graph['nodes']
    ids = [n['id'] for n in nodes]
    rank = ranks(graph)
    levels = max(rank.values()) + 1
    groups = [[n for n in nodes if rank[n['id']] == r] for r in range(levels)]
    top = 150
    stacked = set()
    if c.mobile:
        width, y = 650, top
        for r, group in enumerate(groups):
            k = len(group)
            w = (520 - (k - 1) * 22) / k
            words = [x for n in group for x in (n['label'] + ' ' + n.get('detail', '')).split()]
            if k > 3 or (k > 1 and max(measure(x, c.h_size, True) for x in words) > w - 40):
                stacked.add(r)
                for n in group:
                    y += c.place(n, 90, y, 520) + 34
                y += 26
                continue
            tallest = max(c.box_size(n, w)[2] for n in group)
            for j, n in enumerate(group):
                c.place(n, 90 + j * (w + 22), y, w, tallest)
            y += tallest + 60
        height = y + 10
    elif levels > 4:
        # Two-row reading path: left to right, then right to left.
        cols, cw, gap = 3, 300, 90
        width = 90 + cols * cw + (cols - 1) * gap
        y = top
        for row in range((levels + cols - 1) // cols):
            span = range(row * cols, min(levels, (row + 1) * cols))
            heights = {}
            for r in span:
                col = r % cols if row % 2 == 0 else cols - 1 - r % cols
                cy = y
                for n in groups[r]:
                    cy += c.place(n, 45 + col * (cw + gap), cy, cw) + 24
                heights[r] = cy - y - 24
            row_h = max(heights.values())
            for r in span:   # centre each cell in its row
                for n in groups[r]:
                    c.boxes[n['id']]['y'] += (row_h - heights[r]) / 2
            y += row_h + 95
        height = y - 40
    else:
        width = 1100
        avail = width - 90 - (levels - 1) * 80
        need = [max(measure(w, c.h_size, True) for n in g for w in n['label'].split()) + 50 for g in groups]
        fixed = [r for r in range(levels) if need[r] > avail / levels]
        share = (avail - sum(need[r] for r in fixed)) / max(1, levels - len(fixed))
        cws = [need[r] if r in fixed else share for r in range(levels)]
        heights = []
        for r, group in enumerate(groups):
            cy, x = 0, 45 + sum(cws[:r]) + r * 80
            for n in group:
                cy += c.place(n, x, top + cy, cws[r]) + 30
            heights.append(cy - 30)
        tallest = max(heights)
        for r, group in enumerate(groups):
            for n in group:
                c.boxes[n['id']]['y'] += (tallest - heights[r]) / 2
        height = top + tallest + 70
    for a, b, optional in edge_list(graph):
        s, t = c.boxes[a], c.boxes[b]
        if ids.index(a) > ids.index(b):   # feedback loop
            if c.mobile:
                d = f'M{s["x"] + s["w"] / 2} {s["y"] + s["h"] + 4} V{s["y"] + s["h"] + 26} H40 V{t["y"] + t["h"] / 2} H{t["x"] - 8}'
            else:
                lane = height - 10
                height += 25
                d = f'M{s["x"] + s["w"] / 2} {s["y"] + s["h"] + 4} V{lane} H{t["x"] + t["w"] / 2} V{t["y"] + t["h"] + 8}'
            c.arrow(d, True)
            continue
        vertical = c.mobile or (levels > 4 and abs(s['x'] - t['x']) < 5)
        fanned = c.mobile and rank[b] in stacked and len(groups[rank[b]]) > 1
        if vertical and c.mobile and (rank[b] - rank[a] > 1 or fanned):
            d = f'M{s["x"]} {s["y"] + s["h"] / 2} H52 V{t["y"] + t["h"] / 2} H{t["x"] - 8}'
        elif vertical:
            sx, tx = s['x'] + s['w'] / 2, t['x'] + t['w'] / 2
            mid = (s['y'] + s['h'] + t['y']) / 2
            d = (f'M{sx} {s["y"] + s["h"] + 4} V{mid} H{tx} V{t["y"] - 8}' if abs(sx - tx) > 2
                 else f'M{sx} {s["y"] + s["h"] + 4} V{t["y"] - 8}')
        else:
            leftward = t['x'] < s['x']
            sx = s['x'] - 4 if leftward else s['x'] + s['w'] + 4
            tx = t['x'] + t['w'] + 8 if leftward else t['x'] - 8
            sy, ty = s['y'] + s['h'] / 2, t['y'] + t['h'] / 2
            bend = (tx - sx) / 2
            d = f'M{sx} {sy} C{sx + bend} {sy} {tx - bend} {ty} {tx} {ty}'
        c.arrow(d, optional)
    return width, height


def branches(graph, c):
    nodes = {n['id']: n for n in graph['nodes']}
    prefix, paths = graph.get('branch_prefix', []), graph['branch_paths']
    suffix, labels = graph.get('branch_suffix', []), graph.get('branch_labels', [])
    expected = set(zip(prefix, prefix[1:])) | set(zip(suffix, suffix[1:]))
    for path in paths:
        if prefix:
            expected.add((prefix[-1], path[0]))
        if suffix:
            expected.add((path[-1], suffix[0]))
        expected |= set(zip(path, path[1:]))
    if expected != {(a, b) for a, b, _ in edge_list(graph)}:
        raise ValueError(graph['slug'] + ': branch layout must preserve every semantic edge')
    if sorted(prefix + suffix + [i for p in paths for i in p]) != sorted(nodes):
        raise ValueError(graph['slug'] + ': every node must appear once in branch layout')
    y = 150
    if c.mobile:
        # Each path becomes one card: its first node (or lane label) is the heading.
        width, trunk = 650, 52
        for i in prefix:
            y += c.place(nodes[i], 90, y, 520) + 56
        start = y - 56
        cards = []
        for j, path in enumerate(paths):
            rest = path if labels else path[1:]
            lines = [] if labels or not nodes[path[0]].get('detail') else [nodes[path[0]]['detail']]
            card = {'id': f'lane{j}', 'label': labels[j] if labels else nodes[path[0]]['label'],
                    'detail': ' / '.join(lines + ['→ ' + nodes[i]['label'] + (': ' + nodes[i]['detail'].replace(' / ', ', ').lower() if nodes[i].get('detail') else '') for i in rest]),
                    'role': 'step' if labels else nodes[path[0]].get('role', 'step')}
            y += c.place(card, 90, y, 520) + 30
            c.boxes[card['id']]['holds'] = path
            cards.append(c.boxes[card['id']])
        y += 26
        for i in suffix:
            y += c.place(nodes[i], 90, y, 520) + 56
        if prefix:
            c.extra.append(f'<path d="M{trunk} {start} V{cards[-1]["y"] + cards[-1]["h"] / 2}" fill="none" stroke="{EDGE}" stroke-width="3"/>')
            c.extra.append(f'<path d="M{c.boxes[prefix[-1]]["x"]} {start - 30} H{trunk} V{start}" fill="none" stroke="{EDGE}" stroke-width="3"/>')
            for card in cards:
                c.arrow(f'M{trunk} {card["y"] + card["h"] / 2} H{card["x"] - 8}')
        if suffix:
            last, s = cards[-1], c.boxes[suffix[0]]
            c.arrow(f'M{last["x"] + last["w"] / 2} {last["y"] + last["h"] + 4} V{s["y"] - 8}')
        return width, y - 20
    width = 1150
    for i in prefix:
        y += c.place(nodes[i], 300, y, 550) + 70
    lane_w = (width - 90 - (len(paths) - 1) * 26) / len(paths)
    lane_top = y + (70 if labels else 30)
    bottoms = []
    for j, path in enumerate(paths):
        x, cy = 45 + j * (lane_w + 26), lane_top
        for i in path:
            cy += c.place(nodes[i], x + 18, cy, lane_w - 36) + 60
        bottoms.append(cy)
    bottom = max(bottoms)
    for j in range(len(paths)):
        x = 45 + j * (lane_w + 26)
        c.extra.append(f'<rect data-branch-panel="{j}" x="{x}" y="{lane_top - (52 if labels else 20)}" width="{lane_w}" height="{bottom - lane_top + (40 if labels else 8)}" rx="18" fill="none" stroke="#d9c6b7" stroke-width="2" stroke-dasharray="8 8"/>')
        if labels:
            c.extra.append(f'<text x="{x + 20}" y="{lane_top - 16}" font-size="20" fill="{ACCENT}" font-weight="600" letter-spacing="1">{esc(labels[j].upper())}</text>')
    y = bottom + (40 if suffix else 0)
    for i in suffix:
        y += c.place(nodes[i], 300, y, 550) + 70
    for a, b, optional in edge_list(graph):
        s, t = c.boxes[a], c.boxes[b]
        sx, tx = s['x'] + s['w'] / 2, t['x'] + t['w'] / 2
        if abs(sx - tx) < 2:
            d = f'M{sx} {s["y"] + s["h"] + 4} V{t["y"] - 8}'
        else:
            if a in prefix:
                mid = lane_top - (80 if labels else 45)
            else:
                mid = t['y'] - 34 if b in suffix else s['y'] + s['h'] + 30
            d = f'M{sx} {s["y"] + s["h"] + 4} V{mid} H{tx} V{t["y"] - 8}'
        c.arrow(d, optional, (a, b))
    return width, (y - 10 if suffix else bottom + 10)


def phone_bars(graph, c):
    y, top = 150, max(v for r in graph['rows'] for _, v, _ in r['parts'])
    for row in graph['rows']:
        c.extra.append(f'<text x="45" y="{y + 28}" font-size="30" fill="{INK}" font-weight="600">{esc(row["label"])}</text>')
        y += 52
        for i, (label, value, role) in enumerate(row['parts']):
            c.extra.append(f'<text x="45" y="{y + 22}" font-size="{c.d_size - 3}" fill="{MUTED}">{esc(label)}</text>')
            c.boxes[f'{row["label"]}{i}'] = dict(x=45, y=y + 34, w=max(30, 560 * value / top), h=34, head=[], detail=[], role=role)
            y += 84
        y += 22
    for line in wrap(graph.get('note', ''), 560, 24):
        c.extra.append(f'<text x="45" y="{y + 12}" font-size="24" fill="{MUTED}" font-style="italic">{esc(line)}</text>')
        y += 32
    return 650, y + 30


def bars(graph, c):
    if c.mobile:
        return phone_bars(graph, c)
    width = 650 if c.mobile else 1100
    left, right = (45, 605) if c.mobile else (230, 1055)
    y = 150
    for row in graph['rows']:
        if c.mobile:
            c.extra.append(f'<text x="{left}" y="{y + 28}" font-size="30" fill="{INK}" font-weight="600">{esc(row["label"])}</text>')
            y += 48
        x, segs = left, []
        for label, value, role in row['parts']:
            w = (right - left) * value / 100
            segs.append((x, w, wrap(label, w - 20, c.d_size), role))
            x += w
        h = max(96, max(len(s[2]) for s in segs) * c.d_step + 40)
        if not c.mobile:
            c.extra.append(f'<text x="45" y="{y + h / 2 + 10}" font-size="29" fill="{INK}" font-weight="600">{esc(row["label"])}</text>')
        for i, (x, w, lines, role) in enumerate(segs):
            c.boxes[f'{row["label"]}{i}'] = dict(x=x + 3, y=y, w=w - 6, h=h, head=[], detail=lines, role=role)
        y += h + (44 if c.mobile else 36)
    for line in wrap(graph.get('note', ''), right - left, 24):
        c.extra.append(f'<text x="{left}" y="{y + 12}" font-size="24" fill="{MUTED}" font-style="italic">{esc(line)}</text>')
        y += 32
    return width, y + 30


def sketch_box(b):
    fill, stroke, dash = ROLES[b['role']]
    x, y, w, h = b['x'], b['y'], b['w'], b['h']
    weight = 3.2 if b['role'] == 'key' else 2.2
    dash = f' stroke-dasharray="{dash}"' if dash else ''
    # A faint offset second stroke gives the pencil feel without hurting legibility.
    return [f'<rect x="{x + 3}" y="{y + 3}" width="{w}" height="{h}" rx="16" fill="none" stroke="{stroke}" stroke-opacity=".28" stroke-width="1.6"{dash}/>',
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{fill}" stroke="{stroke}" stroke-width="{weight}"{dash}/>']


def text_block(b, c, emphasis):
    lines = [(t, True) for t in b['head']] + [(t, False) for t in b['detail']]
    total = sum(c.h_step if bold else c.d_step for _, bold in lines) + (6 if b['head'] and b['detail'] else 0)
    y = b['y'] + (b['h'] - total) / 2 + (c.h_step if lines and lines[0][1] else c.d_step) * .72
    out = []
    for i, (line, bold) in enumerate(lines):
        if i and not bold and lines[i - 1][1]:
            y += 6
        text = esc(line)
        for word in emphasis:
            text = text.replace(word, f'<tspan font-weight="700" fill="{ACCENT}">{word.title()}</tspan>')
        size = c.h_size if bold else c.d_size
        weight = ' font-weight="600"' if bold else ''
        colour = INK if bold or not b['head'] else MUTED
        out.append(f'<text x="{b["x"] + b["w"] / 2}" y="{y:.1f}" font-size="{size}"{weight} fill="{colour}" text-anchor="middle">{text}</text>')
        y += c.h_step if bold else c.d_step
    return out


def render(graph, mobile):
    c = Canvas(mobile)
    if graph.get('kind') == 'bars':
        width, height = bars(graph, c)
        desc = '; '.join(r['label'] + ': ' + ', '.join(p[0] for p in r['parts']) for r in graph['rows'])
    else:
        if graph.get('branch_paths') and (mobile or graph.get('branch_desktop')):
            width, height = branches(graph, c)
        else:
            width, height = flow(graph, c)
        desc = '; '.join(n['label'] + (': ' + n['detail'].replace(' / ', ', ') if n.get('detail') else '') for n in graph['nodes'])
    title = wrap(graph['title'], width - 200, 36, True)
    shift = (len(title) - 1) * 44
    width, height = int(width), int(height + shift)
    tw = min(measure(title[0], 36, True), 260)
    uy = 80 + shift
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',
        f'<title id="title">{esc(graph["title"])}</title><desc id="desc">{esc(desc)}</desc>',
        f'<defs><style>@font-face{{font-family:Diagram;src:url(data:font/woff2;base64,{FONT})}}text{{font-family:Diagram,Arial,sans-serif}}</style>'
        f'<pattern id="dots" width="24" height="24" patternUnits="userSpaceOnUse"><circle cx="2" cy="2" r="1.5" fill="#e8d9c8"/></pattern>'
        f'<pattern id="hatch" width="12" height="12" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="12" height="12" fill="{PAPER}"/><line x1="0" y1="0" x2="0" y2="12" stroke="#e4d2c3" stroke-width="5"/></pattern>'
        f'<marker id="arrow" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="9" markerHeight="9" orient="auto"><path d="M2 2 L10 6 L2 10" fill="none" stroke="{EDGE}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>',
        f'<rect width="{width}" height="{height}" rx="18" fill="{PAPER}"/><rect width="{width}" height="{height}" rx="18" fill="url(#dots)"/>',
        f'<rect x="{width - 170}" y="10" width="120" height="30" rx="3" fill="#e9b9a5" fill-opacity=".55" transform="rotate(4 {width - 110} 25)"/>',
    ]
    for i, line in enumerate(title):
        parts.append(f'<text x="45" y="{64 + i * 44}" font-size="36" fill="{INK}" font-weight="600">{esc(line)}</text>')
    parts.append(f'<path d="M46 {uy} C{46 + tw * .3} {uy + 7} {46 + tw * .6} {uy - 5} {46 + tw} {uy + 3}" fill="none" stroke="{ACCENT}" stroke-width="3.2" stroke-linecap="round" opacity=".75"/>')
    parts.append(f'<g transform="translate(0 {shift})">')
    parts += c.extra
    for d, dashed, edge in c.paths:
        dash = ' stroke-dasharray="10 8"' if dashed else ''
        tag = f' data-edge="{esc(" ".join(edge))}"' if edge else ''
        parts.append(f'<path{tag} d="{d}" fill="none" stroke="{EDGE}" stroke-width="3" stroke-linejoin="round" stroke-linecap="round"{dash} marker-end="url(#arrow)"/>')
    for key, b in c.boxes.items():
        holds = f' data-holds="{esc(" ".join(b["holds"]))}"' if b.get('holds') else ''
        parts.append(f'<g data-node="{esc(key)}"{holds}>')
        parts += sketch_box(b) + text_block(b, c, graph.get('emphasis', []))
        parts.append('</g>')
    parts.append('</g></svg>')
    return '\n'.join(parts)


if __name__ == '__main__':
    graphs = json.loads((ROOT / 'design/diagrams.json').read_text())
    for graph in graphs:
        for mobile in (False, True):
            name = graph['slug'] + ('-mobile' if mobile else '') + f'-{VERSION}.svg'
            (ROOT / 'site/assets' / graph['folder'] / name).write_text(render(graph, mobile))
    print(f'Rendered {len(graphs) * 2} diagrams from design/diagrams.json')
