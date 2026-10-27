# -*- coding: utf-8 -*-
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json
ROOT=Path(__file__).resolve().parents[1];SITE=ROOT/'site'
class Doc(HTMLParser):
 def __init__(self,text):
  super().__init__();self.links=[];self.ids=set();self.h1=0;self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  if tag=='h1':self.h1+=1
  if tag in ['a','link','script']:
   url=a.get('href') if tag!='script' else a.get('src')
   if url:self.links.append(url)
lessons=json.loads((ROOT/'content/lessons.json').read_text())
assert len({c['id'] for c in lessons})==len(lessons)
assert len(lessons)>=24
for c in lessons:
 assert c['category'] in ['start','formats','matchday','skills','tactics','practice']
 assert len(c['sections'])>=3 and all(s['title'] and s['text'] for s in c['sections'])
 assert len(c['quiz']['options'])==3 and c['quiz']['answer'] in range(3)
 assert c['sources'] and all(urlsplit(s['url']).scheme=='https' for s in c['sources'])
 assert (SITE/'learn'/(c['id']+'.html')).is_file()
docs={p:Doc(p.read_text()) for p in SITE.rglob('*.html')}
errors=[]
for p,d in docs.items():
 if d.h1!=1:errors.append(str(p)+': expected one h1')
 for raw in d.links:
  u=urlsplit(raw)
  if u.scheme or u.netloc:continue
  target=(p.parent/unquote(u.path)).resolve() if u.path else p.resolve()
  if target.is_dir():target=target/'index.html'
  if not target.is_relative_to(SITE.resolve()):errors.append(str(p)+': escaped site root '+raw);continue
  if not target.is_file():errors.append(str(p)+': missing '+raw);continue
  if u.fragment and target.suffix=='.html':
   other=docs.get(target) or Doc(target.read_text())
   if unquote(u.fragment) not in other.ids:errors.append(str(p)+': missing anchor '+raw)
assert not errors,'\n'.join(errors)
print('PASS:',len(docs),'pages;',len(lessons),'lessons; local links, anchors, sources, quiz schemas, unique IDs and page headings checked.')
