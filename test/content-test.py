#!/usr/bin/env python3
"""Verify metadata generation and release checks without external services."""
import importlib.util
import tempfile
import unittest
import xml.etree.ElementTree as E
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
spec=importlib.util.spec_from_file_location('build',ROOT/'scripts/build-site.py');build=importlib.util.module_from_spec(spec);spec.loader.exec_module(build)
metadata=build.metadata

class ContentTests(unittest.TestCase):
    def test_reading_body_excludes_navigation_and_diagram_captions(self):
        parser=metadata.BodyText()
        parser.feed('<nav>not counted</nav><div class="article-body"><p>Real body.</p><figure><img src="x"><figcaption>not counted</figcaption></figure><p>Another paragraph.</p></div><footer>not counted</footer>')
        self.assertEqual(' '.join(parser.words),'Real body. Another paragraph.')

    def test_feed_original_dates_and_sitemap_exclusions(self):
        essays=metadata.inventory();output=metadata.outputs(essays,['index.html','404.html','posts/example.html'])
        feed=E.fromstring(output['feed.xml']);items=feed.findall('./channel/item')
        self.assertEqual(len(items),8)
        self.assertEqual({i.findtext('guid') for i in items},{e['url'] for e in essays})
        self.assertTrue(all(i.findtext('pubDate').endswith('+0000') for i in items))
        sitemap=E.fromstring(output['sitemap.xml']);ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
        urls=[e.text for e in sitemap.findall('.//s:loc',ns)]
        self.assertIn('https://besz.me/',urls)
        self.assertFalse(any('404.html' in url for url in urls))

    def test_broken_generated_output_references_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp).resolve();page=root/'index.html'
            for markup in ['<a href="feed.xml">missing</a>','<a href="#absent">missing</a>','<img srcset="missing.webp 768w">','<a href="../escape.html">outside</a>']:
                page.write_text(markup)
                with self.subTest(markup=markup),self.assertRaises(ValueError):build.check([page],root,generated=False)

    def test_generated_byline_uses_inventory_publication_date(self):
        essay=metadata.inventory()[0]
        page='<h1>Old</h1><p class="deck">Old</p><p class="article-byline">Old</p></head>'
        output=metadata.page_metadata(page,[essay],'posts/'+essay['slug']+'.html')
        self.assertIn('datetime="'+essay['published']+'"',output)
        self.assertIn(str(essay['minutes'])+' min read',output)
        self.assertNotIn('>Old<',output)

if __name__=='__main__':unittest.main()
