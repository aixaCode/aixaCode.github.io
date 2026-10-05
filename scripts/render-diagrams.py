#!/usr/bin/env python3
"""Render editable graph specifications as responsive notebook SVGs."""
import base64
import html
import json
import math
import textwrap
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
PALETTE={'paper':'#fff8ef','ink':'#4c332c','edge':'#84685b',
         'blue':'#e0eaf0','sage':'#e5eadb','rose':'#f3ddd1'}
METRICS=json.loads((ROOT/'design/font-metrics.json').read_text())
FONT=base64.b64encode((ROOT/'site/assets/fonts/dm-sans-latin.woff2').read_bytes()).decode()

def lines(label,width,font=30):
    result=[]
    def measure(text):return sum(METRICS.get(c,.7) for c in text)*font
    for part in label.split(' / '):
        line=''
        for word in part.split():
            candidate=(line+' '+word).strip()
            if line and measure(candidate)>width:
                result.append(line);line=word
            else:line=candidate
        if line:result.append(line)
    return result

def render(graph,mobile):
    nodes=graph['nodes']; ids=[n['id'] for n in nodes]
    rank={i:0 for i in ids};forward=[];returns=[]
    # Source order records the original reading direction; feedback arrows return.
    for a,b in graph['edges']:
        (returns if ids.index(a)>=ids.index(b) else forward).append((a,b))
    for i in ids:
        incoming=[rank[a]+1 for a,b in forward if b==i]
        if incoming:rank[i]=max(incoming)
    if not graph['edges']:
        rank={i:j for j,i in enumerate(ids)} if mobile else {i:0 for i in ids}
    levels=max(rank.values())+1
    stacked=mobile or levels>4
    positions={};labels={};font=34 if mobile else (26 if stacked else 30)
    if stacked:
        width=650 if mobile else 1000; y=150
        for n in sorted(nodes,key=lambda n:(rank[n['id']],ids.index(n['id']))):
            label=lines(n['label'],455 if mobile else 780,font); h=max(118,len(label)*(44 if mobile else 39)+42)
            positions[n['id']]=(115 if mobile else 130,y,495 if mobile else 820,h);labels[n['id']]=label;y+=h+(68 if mobile else 48)
        height=y+45
    else:
        levels=max(rank.values())+1; width=max(1040,levels*360+110);max_count=max(list(rank.values()).count(i) for i in set(rank.values()))
        for level in range(levels):
            group=[n for n in nodes if rank[n['id']]==level]
            y=155
            for n in group:
                label=lines(n['label'],270 if levels>1 else 850,font);w=300 if levels>1 else 890
                h=max(142,len(label)*39+44)
                positions[n['id']]=(75+level*360,y,w,h);labels[n['id']]=label;y+=h+55
        height=max(y+h for x,y,w,h in positions.values())+95
    titlelines=lines(graph['title'],555 if mobile else width-120,38)
    headheight=len(titlelines)*44
    shift=max(0,headheight+65-150)
    positions={i:(x,y+shift,w,h) for i,(x,y,w,h) in positions.items()};height+=shift
    esc=html.escape;parts=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-labelledby="title desc">',f'<title id="title">{esc(graph["title"])}</title>',f'<desc id="desc">{esc("; ".join(n["label"] for n in nodes))}. {esc("; ".join(a+" leads to "+b for a,b in graph["edges"]))}</desc>',f'<defs><style>@font-face{{font-family:Diagram;src:url(data:font/woff2;base64,{FONT})}}text{{font-family:Diagram,Arial,sans-serif}}</style><marker id="arrow" viewBox="0 0 12 12" refX="10" refY="6" markerWidth="9" markerHeight="9" orient="auto"><path d="M2 2 L10 6 L2 10" fill="none" stroke="{PALETTE["edge"]}" stroke-width="1.7" stroke-linecap="round"/></marker></defs>',f'<rect width="{width}" height="{height}" rx="16" fill="{PALETTE["paper"]}"/>']
    for i,line in enumerate(titlelines):parts.append(f'<text x="{45 if mobile else 60}" y="{61+i*44}" font-size="{36 if mobile else 36}" fill="{PALETTE["ink"]}" font-weight="600">{esc(line)}</text>')
    ordered=sorted(ids,key=lambda i:positions[i][1])
    for a,b in forward+returns:
        x,y,w,h=positions[a];tx,ty,tw,th=positions[b]
        if stacked:
            if ordered.index(b)==ordered.index(a)+1 and (a,b) not in returns:
                d=f'M{x+w/2} {y+h+4} L{tx+tw/2} {ty-8}'
            else:
                lane=62 if (a,b) not in returns else 30
                d=f'M{x} {y+h/2} H{lane} V{ty+th/2} H{tx-8}'
        elif rank[b]>rank[a]:
            d=f'M{x+w+3} {y+h/2} C{x+w+30} {y+h/2} {tx-35} {ty+th/2} {tx-8} {ty+th/2}'
        else:
            lane=height-38
            d=f'M{x+w/2} {y+h+3} V{lane} H{tx+tw/2} V{ty+th+8}'
        parts.append(f'<path d="{d}" fill="none" stroke="{PALETTE["edge"]}" stroke-width="3" stroke-linejoin="round" marker-end="url(#arrow)"/>')
    for index,n in enumerate(nodes):
        x,y,w,h=positions[n['id']];label=labels[n['id']]
        fill=PALETTE[['blue','sage','rose'][index%3]]
        parts.append(f'<g data-node="{esc(n["id"])}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{PALETTE["edge"]}" stroke-width="2.2"/>')
        start=y+h/2-(len(label)-1)*(44 if mobile else 39)/2+font*.32
        for j,line in enumerate(label):
            text=esc(line)
            if graph['slug']=='changing-constraint':
                for active in ['RETENTION','STABILITY']:
                    text=text.replace(active,'<tspan font-weight="700" fill="#a04637">'+active+'</tspan>')
            parts.append(f'<text x="{x+w/2}" y="{start+j*(44 if mobile else 39)}" fill="{PALETTE["ink"]}" font-size="{font}" text-anchor="middle">{text}</text>')
        parts.append('</g>')
    parts.append('</svg>');return '\n'.join(parts)

if __name__=='__main__':
    graphs=json.loads((ROOT/'design/diagrams.json').read_text())
    for graph in graphs:
        for mobile in (False,True):
            filename=graph['slug']+('-mobile' if mobile else '')+'-v4.svg'
            (ROOT/'site/assets'/graph['folder']/filename).write_text(render(graph,mobile))
    print(f'Rendered {len(graphs)*2} diagrams from design/diagrams.json')
