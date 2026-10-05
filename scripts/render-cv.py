#!/usr/bin/env python3
"""Render the public CV PDF from the same HTML body used on the website."""
from html.parser import HTMLParser
from pathlib import Path
import hashlib
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Frame, KeepTogether
from reportlab.lib.pagesizes import A4

ROOT=Path(__file__).resolve().parent.parent
class Node:
    def __init__(self,tag='',attrs=None): self.tag=tag;self.attrs=dict(attrs or []);self.children=[]
    def text(self): return ' '.join(' '.join(c.text() if isinstance(c,Node) else c for c in self.children).split())
    def has(self,name):return name in self.attrs.get('class','').split()
    def find(self,predicate):
        if predicate(self):return self
        for child in self.children:
            if isinstance(child,Node):
                found=child.find(predicate)
                if found:return found
class Tree(HTMLParser):
    def __init__(self):super().__init__();self.root=Node();self.stack=[self.root]
    def handle_starttag(self,tag,attrs):
        node=Node(tag,attrs);self.stack[-1].children.append(node)
        if tag not in ['meta','link','img','source','br','hr','input']:self.stack.append(node)
    def handle_endtag(self,tag):
        for i in range(len(self.stack)-1,0,-1):
            if self.stack[i].tag==tag:self.stack=self.stack[:i];break
    def handle_data(self,data):self.stack[-1].children.append(data)

ink=HexColor('#4c332c');accent=HexColor('#a04637')
body=ParagraphStyle('body',fontName='Helvetica',fontSize=8.7,leading=11.25,textColor=ink,spaceAfter=3)
heading=ParagraphStyle('heading',parent=body,fontName='Helvetica-Bold',fontSize=10.1,leading=13,textColor=accent,spaceBefore=10,spaceAfter=5,keepWithNext=True)
strong=ParagraphStyle('strong',parent=body,fontName='Helvetica-Bold',spaceBefore=5,keepWithNext=True)
meta=ParagraphStyle('meta',parent=body,fontSize=7.9,leading=10,textColor=HexColor('#765d51'),keepWithNext=True)
bullet=ParagraphStyle('bullet',parent=body,leftIndent=8,firstLineIndent=-8,spaceAfter=3)

def paragraph(node,style):
    text=node.text().replace('—','-').replace('–','-').replace('‑','-')
    return Paragraph(escape(text),style)

def story(node):
    result=[]
    for child in node.children:
        if not isinstance(child,Node):continue
        if child.has('role') or child.has('project'):
            title=child.find(lambda n:n.has('role-title') or n.has('project-title'))
            detail=child.find(lambda n:n.has('role-dates') or n.has('meta'))
            listing=child.find(lambda n:n.tag=='ul')
            items=[n for n in listing.children if isinstance(n,Node) and n.tag=='li']
            intro='<b>'+escape(title.text())+'</b><br/><font size="7.9" color="#765d51">'+escape(detail.text())+'</font><br/>• '+escape(items[0].text().replace('—','-').replace('–','-'))
            result.append(Paragraph(intro,body))
            for item in items[1:]:result.append(Paragraph('• '+escape(item.text().replace('—','-').replace('–','-')),bullet))
            result.append(Spacer(1,4))
        elif child.tag=='h2':result.append(paragraph(child,heading))
        elif child.tag=='li':result.append(Paragraph('• '+escape(child.text().replace('—','-').replace('–','-')),bullet))
        elif child.tag=='p' or child.has('blk'):result.append(paragraph(child,body))
        elif child.has('role-title') or child.has('project-title'):result.append(paragraph(child,strong))
        elif child.has('role-dates') or child.has('meta'):result.append(paragraph(child,meta))
        else:result.extend(story(child))
    return result

if __name__=='__main__':
    parser=Tree();parser.feed((ROOT/'site/cv.html').read_text());main=parser.root.find(lambda n:n.tag=='main')
    left=story(main.find(lambda n:n.has('left')));right=story(main.find(lambda n:n.has('right')))
    width,height=A4
    c=canvas.Canvas(str(ROOT/'site/cv.pdf'),pagesize=A4,invariant=1)
    c.setTitle('Agnieszka Besz - CV');c.setAuthor('Agnieszka Besz')
    page=1
    while left or right:
        c.setFillColor(HexColor('#fff8ef'));c.rect(0,0,width,height,fill=1,stroke=0)
        c.setFillColor(ink)
        if page==1:
            c.setFont('Times-Roman',29);c.drawString(30,height-43,'Agnieszka Besz')
            c.setFont('Helvetica',10);c.drawString(31,height-64,'VP of Engineering')
            c.setFont('Helvetica',8)
            contacts=main.find(lambda n:n.has('contact'));y=height-81
            c.drawString(31,y,'London, United Kingdom  |  aga@besz.me  |  https://besz.me/')
            c.drawString(31,y-12,'linkedin.com/in/agabesz  |  github.com/aixaCode  |  gbfactory.uk')
            c.linkURL('https://besz.me/',(245,y-2,335,y+9),relative=0)
            top=height-111
        else:
            c.setFont('Helvetica-Bold',10);c.drawString(30,height-34,'Agnieszka Besz / VP of Engineering')
            top=height-50
        c.setStrokeColor(HexColor('#decfc1'));c.line(397,40,397,top)
        Frame(30,39,354,top-39,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0).addFromList(left,c)
        Frame(412,39,153,top-39,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0).addFromList(right,c)
        c.setFillColor(HexColor('#765d51'));c.setFont('Helvetica',7.5);c.drawString(30,22,'besz.me');c.drawRightString(width-30,22,str(page))
        c.showPage();page+=1
        if page>5:raise RuntimeError('Unexpected CV overflow')
    c.save()
    (ROOT/'content/cv-pdf-source.sha256').write_text(hashlib.sha256((ROOT/'site/cv.html').read_bytes()).hexdigest()+'\n')
    print(f'Rendered CV from HTML: {page-1} pages')
