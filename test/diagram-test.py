#!/usr/bin/env python3
"""Check branch meaning and grouping independently of text overflow checks."""
import importlib.util
import json
import unittest
import xml.etree.ElementTree as E
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('diagrams',ROOT/'scripts/render-diagrams.py')
diagrams=importlib.util.module_from_spec(spec);spec.loader.exec_module(diagrams)
NS={'s':'http://www.w3.org/2000/svg'}

class DiagramTests(unittest.TestCase):
    def test_grouped_layout_preserves_edges_and_separates_paths(self):
        for graph in json.loads((ROOT/'design/diagrams.json').read_text()):
            if not graph.get('branch_paths'):continue
            for mobile in ([False,True] if graph.get('branch_desktop') else [True]):
                with self.subTest(graph=graph['slug'],mobile=mobile):
                    svg=E.fromstring(diagrams.render(graph,mobile))
                    edges=[p.attrib['data-edge'].split() for p in svg.findall('s:path',NS) if 'data-edge' in p.attrib]
                    self.assertEqual(sorted(edges),sorted(graph['edges']))
                    boxes={g.attrib['data-node']:g.find('s:rect',NS).attrib for g in svg.findall('s:g',NS)}
                    panels=[r.attrib for r in svg.findall('s:rect',NS) if r.attrib.get('data-branch-panel')]
                    self.assertEqual(len(panels),len(graph['branch_paths']))
                    def contains(panel,box):
                        return (float(box['x'])>=float(panel['x']) and float(box['y'])>=float(panel['y'])
                            and float(box['x'])+float(box['width'])<=float(panel['x'])+float(panel['width'])
                            and float(box['y'])+float(box['height'])<=float(panel['y'])+float(panel['height']))
                    for index,path in enumerate(graph['branch_paths']):
                        for node in path:
                            self.assertTrue(contains(panels[index],boxes[node]))
                            self.assertFalse(any(contains(p,boxes[node]) for j,p in enumerate(panels) if j!=index))

    def test_missing_or_extra_semantic_edge_is_rejected(self):
        graph=next(g for g in json.loads((ROOT/'design/diagrams.json').read_text()) if g.get('branch_paths'))
        for edges in (graph['edges'][:-1],graph['edges']+[graph['edges'][0][::-1]]):
            with self.assertRaises(ValueError):diagrams.render({**graph,'edges':edges},True)

if __name__=='__main__':unittest.main()
