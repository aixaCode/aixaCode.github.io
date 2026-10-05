#!/usr/bin/env python3
"""Generate metadata from dated essay inventory and body-only reading times."""
import email.utils
import html
import json
import math
import re
import xml.etree.ElementTree as E
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
BASE='https://besz.me'

class BodyText(HTMLParser):
    def __init__(self):
        super().__init__();self.depth=0;self.body=None;self.excluded=None;self.words=[]
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if attrs.get('class')=='article-body':self.body=self.depth
        if self.body is not None and tag in ('figure','script','style'):self.excluded=self.depth
        if tag not in ('img','source','br','hr','meta','link','input'):self.depth+=1
    def handle_endtag(self,tag):
        if tag not in ('img','source','br','hr','meta','link','input'):self.depth-=1
        if self.excluded==self.depth:self.excluded=None
        if self.body==self.depth:self.body=None
    def handle_data(self,data):
        if self.body is not None and self.excluded is None:self.words.append(data)

def inventory():
    essays=json.loads((ROOT/'content/essays.json').read_text())
    for essay in essays:
        page=(ROOT/'site/posts'/f'{essay["slug"]}.html').read_text()
        parser=BodyText();parser.feed(page)
        count=len(re.findall(r"\b[\w’'-]+\b",' '.join(parser.words)))
        if not count:raise ValueError('Missing body text: '+essay['slug'])
        essay['minutes']=max(1,math.ceil(count/220))
        essay['url']=BASE+'/posts/'+essay['slug']+'.html'
    return essays

def page_metadata(page,essays,relative):
    for essay in essays:
        slug=essay['slug'];minutes=essay['minutes']
        date=datetime.fromisoformat(essay['published']).strftime('%b %d, %Y').replace(' 0',' ')
        if relative == 'posts/'+slug+'.html':
            page=re.sub(r'<h1>.*?</h1>', '<h1>'+html.escape(essay['title'])+'</h1>', page, flags=re.S)
            page=re.sub(r'<p class="deck">.*?</p>', '<p class="deck">'+html.escape(essay['description'])+'</p>', page, flags=re.S)
            page=re.sub(r'<p class="article-byline">.*?</p>',f'<p class="article-byline">Agnieszka Besz · <time datetime="{essay["published"]}">{date}</time> · {minutes} min read</p>',page,flags=re.S)
            page=re.sub(r'<title>.*?</title>','<title>'+html.escape(essay['title'])+' — Agnieszka Besz</title>',page,flags=re.S)
            for selector,value in [('property="og:title"',essay['title']),('name="twitter:title"',essay['title']),('name="description"',essay['description']),('property="og:description"',essay['description']),('name="twitter:description"',essay['description'])]:
                page=re.sub(r'(<meta '+re.escape(selector)+r' content=")[^"]*(">)',lambda m:m[1]+html.escape(value,quote=True)+m[2],page)
            if 'property="article:published_time"' not in page:
                page=page.replace('</head>',f'<meta property="article:published_time" content="{essay["published"]}"></head>')
        # Match a complete containing article/card, not unrelated neighbouring entries.
        for tag in ('article','li'):
            pattern=rf'<{tag}\b[^>]*>.*?</{tag}>'
            def card(match):
                content=match.group(0)
                if f'posts/{slug}.html' in content:
                    content=re.sub(r'\d+\s*(?:minute|min)\s*read',f'{minutes} min read',content,flags=re.I)
                    content=re.sub(r'\d+\s*MIN READ',f'{minutes} MIN READ',content)
                return content
            page=re.sub(pattern,card,page,flags=re.S)
        # Featured essay byline is a dedicated component.
        if essay['slug']=='use-ai-to-find-evidence-not-score-engineers':
            page=re.sub(r'(<(?:span|div)[^>]*>)10 minute read(</(?:span|div)>)',rf'\g<1>{minutes} min read\2',page)
            if relative=='index.html':page=page.replace('10 minute read',f'{minutes} min read')
    for asset in ['site.css','content.css','site.js']:
        import hashlib
        digest=hashlib.sha256((ROOT/'site/assets'/asset).read_bytes()).hexdigest()[:10]
        page=re.sub(r'(assets/'+re.escape(asset)+r')\?v=[a-f0-9]+',rf'\1?v={digest}',page)
    return page

def outputs(essays,files):
    rss=E.Element('rss',version='2.0');channel=E.SubElement(rss,'channel')
    for key,value in [('title','Agnieszka Besz — The notebook'),('link',BASE+'/writing.html'),('description','Engineering, product direction, AI and leadership. Written from experience.'),('language','en-gb')]:E.SubElement(channel,key).text=value
    for essay in sorted(essays,key=lambda e:(e['published'],e['slug']),reverse=True):
        item=E.SubElement(channel,'item')
        for key,value in [('title',essay['title']),('link',essay['url']),('guid',essay['url']),('description',essay['description']),('pubDate',email.utils.format_datetime(datetime.fromisoformat(essay['published']).replace(tzinfo=timezone.utc)))]:E.SubElement(item,key).text=value
    updates=json.loads((ROOT/'content/page-updates.json').read_text())
    ns='http://www.sitemaps.org/schemas/sitemap/0.9';E.register_namespace('',ns);sitemap=E.Element('{'+ns+'}urlset')
    for path in sorted(p for p in files if p.endswith('.html') and p!='404.html'):
        item=E.SubElement(sitemap,'{'+ns+'}url');E.SubElement(item,'{'+ns+'}loc').text=BASE+('/' if path=='index.html' else '/'+path)
        if path in updates:E.SubElement(item,'{'+ns+'}lastmod').text=updates[path]
    return {'feed.xml':E.tostring(rss,encoding='utf-8',xml_declaration=True),'sitemap.xml':E.tostring(sitemap,encoding='utf-8',xml_declaration=True)}
