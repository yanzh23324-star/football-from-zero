# -*- coding: utf-8 -*-
from pathlib import Path
from html import escape
import json,shutil,re
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'site';DATE='2026-10-27'
CATS=[('start','认识足球','先知道这场比赛在做什么。','从进球、球场线条到越位和重开，建立第一张足球地图。'),('formats','赛制与规则','先问清，今天踢哪一种？','五人、七人、八人、十一人，以及正式 futsal 与草地小场的区别。'),('matchday','第一次上场','从装好球包，到加入一场球。','准备装备、确认规则、和队友沟通，给第一次比赛一个小目标。'),('skills','基础技术','把每一次触球，变得更可控。','停、传、带、射与接球前观察，从容易做到的动作开始。'),('tactics','跑位与配合','没有拿球时，你也在参与。','理解接应、传后移动、宽度、纵深，以及防守时的保护。'),('practice','训练与复盘','练一件事，再带到比赛里。','按一个人、两个人和赛后复盘选择练习，把模糊感觉变成具体问题。')]
META={x[0]:dict(id=x[0],name=x[1],short=x[2],desc=x[3],number=f'{i+1:02}') for i,x in enumerate(CATS)}
LESSONS=json.loads((ROOT/'content/lessons.json').read_text());LESSONS.sort(key=lambda x:list(META).index(x['category']));BYID={x['id']:x for x in LESSONS}
E=lambda s:escape(str(s),quote=True)
def pitch(mode='static',light=False):
 stroke='#88a78c' if not light else '#78947b';bg='#173e36' if not light else '#e7ebdb'
 field=f'<rect x="22" y="25" width="596" height="350" rx="3" fill="{bg}" stroke="{stroke}" stroke-width="1.5"/><path d="M320 25V375 M22 120H100V280H22 M618 120H540V280H618 M22 157H57V243H22 M618 157H583V243H618" fill="none" stroke="{stroke}" stroke-width="1.4"/><circle cx="320" cy="200" r="50" fill="none" stroke="{stroke}"/><circle cx="320" cy="200" r="3" fill="{stroke}"/>'
 if mode=='formats':extra='<g data-players></g>';attrs=' data-format-svg'
 elif mode in ['support','cover']:
  extra='<line data-pass-line x1="190" y1="210" x2="390" y2="210" stroke="#d7ef9d" stroke-dasharray="6 5" stroke-width="2"/><circle cx="190" cy="210" r="17" fill="#d7ef9d"/><text x="190" y="215" text-anchor="middle" font-size="12" fill="#173e36">友</text><g data-opponent transform="translate(305 210)"><circle r="17" fill="#d9704e"/><text y="5" text-anchor="middle" font-size="12" fill="white">对</text></g><g data-you transform="translate(390 210)"><circle r="18" fill="#f6f4ea" stroke="#d7ef9d" stroke-width="3"/><text y="5" text-anchor="middle" font-size="12" fill="#173e36">你</text></g><circle cx="177" cy="228" r="6" fill="#f6f4ea" stroke="#173e36" stroke-width="2"/><text x="40" y="352" font-size="11" fill="#b8cdb8">教学情景示意 · 不按实际比例</text>'
  attrs=''
 elif mode=='labels':
  extra='<g font-size="12" fill="#173e36"><text x="150" y="18">边线</text><text x="324" y="60">中线</text><text x="109" y="146">罚球区</text><text x="55" y="310">球门线</text><text x="340" y="265">中圈</text><text x="580" y="214">球门</text></g>';attrs=''
 else:
  extra='<path d="M185 235L330 115L440 250Z" fill="none" stroke="#d7ef9d" stroke-dasharray="6 6" stroke-width="2"/><path d="M330 115Q410 95 470 145" fill="none" stroke="#edbc6e" stroke-width="2"/><circle cx="185" cy="235" r="18" fill="#d7ef9d"/><circle cx="330" cy="115" r="18" fill="#d7ef9d"/><circle cx="440" cy="250" r="18" fill="#d7ef9d"/><circle cx="300" cy="220" r="17" fill="#d9704e"/><circle cx="390" cy="175" r="17" fill="#d9704e"/><circle cx="172" cy="255" r="7" fill="#f6f4ea"/><g font-size="12" fill="#173e36" text-anchor="middle"><text x="185" y="240">A</text><text x="330" y="120">B</text><text x="440" y="255">你</text></g>';attrs=''
 return f'<svg{attrs} viewBox="0 0 640 400" role="img" aria-label="足球场空间与球员示意">{field}{extra}</svg>'
def formats_widget():
 return '<div class="diagram-box" data-formats><h2>点一下，看看场上人数怎么变</h2><div class="diagram-controls">'+''.join(f'<button data-format-n="{n}" aria-pressed="{str(n==5).lower()}">{n} 人</button>' for n in [5,7,8,11])+'</div>'+pitch('formats')+'<p class="formats-summary" data-format-summary aria-live="polite"></p><p class="muted">黄点是门将，绿／橙分别代表两队。图示仅用于数人数，不是推荐阵型，也不表示统一场地尺寸。</p></div>'
def scenario_widget(mode='support'):
 return f'<div class="diagram-box" data-scenario="{mode}"><h2>把场景停下来，看一种可能的选择</h2>'+pitch(mode)+'<div class="diagram-controls">'+''.join(f'<button data-scene-step="{i}" aria-pressed="{str(i==0).lower()}">{name}</button>' for i,name in enumerate(['① 先观察','② 调整位置','③ 再看变化']))+'</div><p class="diagram-caption" data-scenario-caption aria-live="polite"></p></div>'
def header(base,active):
 links=[('home','index.html','首页'),('catalog','catalog.html','全部课程'),('path','path.html','从零开始'),('sources','sources.html','资料来源'),('notebook','notebook.html','我的学习')]
 nav=''.join(f'<a href="{base}{url}"'+(' aria-current="page"' if active==key else '')+(' class="nav-book"' if key=='notebook' else '')+f'>{name}</a>' for key,url,name in links)
 return f'<a class="skip" href="#main">跳到正文</a><header class="site-header"><div class="wrap header-inner"><a class="brand" href="{base}index.html" aria-label="第一脚 首页"><span class="brand-mark">1</span><span><b>第一脚</b><small>THE FIRST KICK · FOOTBALL GUIDE</small></span></a><nav aria-label="主导航">{nav}</nav></div></header>'
def footer(base):
 return f'<footer class="wrap footer"><div><strong>第一脚 · 从零开始踢足球</strong><br>把问题拆小，把第一步走出来。<br>独立学习资料站 · 非 FIFA、IFAB 或足协官方网站</div><div class="footer-links"><a href="{base}catalog.html">课程目录</a><a href="{base}sources.html">来源与编辑说明</a><a href="{base}notebook.html">本地学习笔记</a><a href="https://github.com/yanzh23324-star/football-from-zero" target="_blank" rel="noopener">GitHub ↗</a></div></footer>'
def shell(title,body,path,active='',lesson=None,desc='面向零基础球员的中文足球入门手册：规则、赛制、基础技术、跑位与训练。'):
 depth=len(Path(path).parts)-1;base='../'*depth
 html=f'''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="description" content="{E(desc)}"><meta name="theme-color" content="#173e36"><title>{E(title)} · 第一脚</title><link rel="icon" href="{base}assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{base}assets/style.css"><script defer src="{base}assets/course-data.js"></script><script defer src="{base}assets/app.js"></script></head><body data-base="{base}"{f' data-lesson="{lesson}"' if lesson else ''}>{header(base,active)}<main class="wrap" id="main">{body}</main>{footer(base)}</body></html>'''
 f=OUT/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(html)
def crumb(parts,base=''):
 return '<div class="crumb" aria-label="面包屑导航"><a href="'+base+'index.html">首页</a>'+''.join(' <span>/</span> '+(f'<a href="{E(url)}">{E(label)}</a>' if url else f'<span>{E(label)}</span>') for label,url in parts)+'</div>'
def card(c,base='',index=None):
 words=' '.join([c['title'],c['lead'],META[c['category']]['name']]+[x['text'] for x in c['sections']])
 idx=f'{index:02}' if index is not None else '↗'
 return f'<a class="lesson-card" href="{base}learn/{c["id"]}.html" data-course="{c["id"]}" data-category="{c["category"]}" data-search="{E(words)}"><span class="lesson-index">{idx}</span><div><span class="card-label">{META[c["category"]]["name"]}</span><h3>{E(c["title"])}</h3><p>{E(c["lead"])}</p><small>约 3 分钟 · 图文＋自测 <span data-read-badge class="complete-badge"></span></small></div></a>'
def section_head(en,title,link=None):
 return f'<div class="section-head"><div><div class="eyebrow">{en}</div><h2>{title}</h2></div>'+ (f'<a class="text-link" href="{link[0]}">{link[1]} ↗</a>' if link else '')+'</div>'
def homepage():
 b='<section class="hero"><div><div class="eyebrow">A BEGINNER’S FIELD GUIDE</div><h1>从不知所措，<br>到踢出<em>第一脚。</em></h1><p>不懂规则、停不住球、不知道往哪跑？<br>把足球拆成一个个能看懂、能试一试的小问题。<br>这是你的第一本上场手册。</p><div class="hero-actions"><a class="btn" href="path.html">跟着路线，从零开始 <span>↗</span></a><a class="btn secondary" href="catalog.html">找一个具体问题</a></div><div class="small-rule"><span>● 中文原创讲解</span><span>● 官方来源可追溯</span><span>● 无需注册</span></div></div><div class="hero-board"><div class="sticker">先懂一点<br>再去试试</div><div class="board-top"><span>FIELD NOTES / 01</span><span>YOU BELONG ON THE PITCH</span></div><h3>接应，从给队友一个选择开始。</h3>'+pitch()+'<div class="board-note">球不在你脚下时，观察和移动也能帮助球队。<br><a href="learn/support-space.html">看看“我该往哪跑”这一课 ↗</a></div></div></section>'
 b+='<div class="intro-strip"><span><strong>06</strong> 大板块，按问题进入</span><span><strong>'+str(len(LESSONS))+'</strong> 节短课，逐篇学习</span><span><strong>01</strong> 次练一个小目标</span></div>'
 b+='<section class="section">'+section_head('CHOOSE YOUR CHAPTER','你想先弄明白什么？',('catalog.html','查看全部课程'))+'<div class="topic-grid">'
 for cat in META.values():
  n=sum(c['category']==cat['id'] for c in LESSONS)
  b+=f'<a class="topic-card" href="topics/{cat["id"]}.html"><span class="topic-num">{cat["number"]}</span><span class="topic-arrow">↗</span><h3>{cat["name"]}</h3><p>{cat["desc"]}</p><div class="topic-bottom"><span>{n} 节入门课</span><span>进入板块 →</span></div></a>'
 b+='</div></section><section class="route-band"><div><div class="eyebrow">YOUR FIRST LEARNING ROUTE</div><h2>什么都不懂，<br>就从这一条路线走。</h2><p>先认识比赛，再完成一次简单配合。<br>不用一口气学完，按自己的节奏来。</p><a class="text-link" href="path.html">打开完整学习路线 ↗</a></div><div class="route-mini"><a href="learn/how-game-works.html"><span>01</span>认识比赛<br>先看懂目标</a><a href="learn/first-touch.html"><span>02</span>接住来球<br>准备下一步</a><a href="learn/support-space.html"><span>03</span>没有拿球<br>也参与配合</a></div></section>'
 b+='<section class="section">'+section_head('TWO QUESTIONS TO START WITH','新手常问的两个问题')+'<div class="feature-grid"><a class="feature" href="learn/formats-compared.html"><div class="eyebrow">5 / 7 / 8 / 11</div><h3>人数不同，<br>比赛到底哪里不一样？</h3><p>人数包括门将吗？七人有没有越位？<br>先把赛制和实际约定分开看。</p><span class="text-link">打开赛制对比课 ↗</span></a><a class="feature alt" href="learn/after-pass.html"><div class="eyebrow">OFF THE BALL</div><h3>我把球传出去了，<br>然后呢？</h3><p>再接应、向前跑、留下保护，<br>怎么根据局面做选择？</p><span class="text-link">打开传后移动课 ↗</span></a></div></section>'
 shell('从零开始踢足球',b,'index.html','home')
def category_pages():
 for cid,cat in META.items():
  rows=[c for c in LESSONS if c['category']==cid]
  graphic=formats_widget() if cid=='formats' else '<div class="category-graphic">'+pitch('labels' if cid=='start' else 'static',True)+'</div>'
  if cid=='formats':graphic='<div>'+graphic+'</div>'
  b=crumb([(cat['name'],None)],'../')+f'<section class="category-cover"><div><div class="eyebrow">CHAPTER {cat["number"]} / {len(rows)} LESSONS</div><h1>{cat["name"]}</h1><p>{cat["short"]}<br>{cat["desc"]}</p><span class="page-meta">零基础友好 · 每篇约 3 分钟 · 独立课程页面</span></div>{graphic}</section><div class="lesson-list">'+''.join(card(c,'../',i+1) for i,c in enumerate(rows))+'</div>'
  b+='<div class="notice">怎么使用：选一篇感兴趣的课，读完做一道自测，再带着一个小任务去练习。战术示意是帮助观察的例子，实际分工要结合队友和比赛规则。</div>'
  shell(cat['name'],b,'topics/'+cid+'.html','catalog')
def comparison():
 return '<div class="table-scroll"><table class="comparison-table"><caption class="muted" style="text-align:left;margin-bottom:10px">先看人数，再核对你参加的实际规则。</caption><thead><tr><th>形式</th><th>每队通常人数</th><th>规则该看什么</th><th>开场前重点确认</th></tr></thead><tbody><tr><td>正式 futsal</td><td>4 名场上球员＋1 名门将</td><td>FIFA futsal 专项规则</td><td>踢入球、门将及换人规则</td></tr><tr><td>普通五人小场</td><td>4＋1</td><td>当地赛事／组织者规程</td><td>不要默认等同 futsal</td></tr><tr><td>七人</td><td>6＋1</td><td>当地赛事／组织者规程</td><td>越位、出界、换人</td></tr><tr><td>八人</td><td>7＋1</td><td>当地赛事／组织者规程</td><td>越位、出界、换人</td></tr><tr><td>十一人</td><td>10＋1</td><td>IFAB 规则及赛事规程</td><td>比赛时间、换人及赛事调整</td></tr></tbody></table></div>'
def article_pages():
 for i,c in enumerate(LESSONS):
  cat=META[c['category']];base='../';toc=[(f's{j+1}',x['title']) for j,x in enumerate(c['sections'])]+[('practice','试一试'),('quiz','一道自测'),('sources','参考来源')]
  b=crumb([(cat['name'],'../topics/'+cat['id']+'.html'),('课程',None)],base)+'<div class="article-layout"><aside class="article-side"><div class="sticky-toc"><p class="toc-title">IN THIS LESSON</p><nav class="toc" aria-label="本课目录">'+''.join(f'<a href="#{id}">{E(title)}</a>' for id,title in toc)+'</nav><p class="muted" style="margin-top:20px">每次只带走一个<br>能在场上试的想法。</p></div></aside><article><header class="article-intro"><div class="eyebrow">'+cat['name']+' / LESSON '+f'{i+1:02}'+f'</div><h1>{E(c["title"])}</h1><p class="lead">{E(c["lead"])}</p><span class="page-meta">约 3 分钟 · 中文原创整理 · 核验 {DATE}</span></header><div class="article-tools"><button class="tool-btn" data-save-button="{c["id"]}" aria-pressed="false">☆ 收藏这课</button><button class="tool-btn" data-read-button="{c["id"]}" aria-pressed="false">标记为已读</button><a class="tool-btn" href="../notebook.html">写一条学习笔记 ↗</a></div>'
  if c['id']=='formats-compared':b+=formats_widget()+comparison()
  if c['id']=='pitch-lines':b+='<figure class="figure-static">'+pitch('labels',True)+'<figcaption>十一人制球场的简化示意，不按实际比例。球门线是球场短边边界，球门位于其上；小场标线可能不同。</figcaption></figure>'
  if c['id'] in ['support-space','after-pass','width-depth']:b+=scenario_widget()
  if c['id']=='defend-cover':b+=scenario_widget('cover')
  for j,s in enumerate(c['sections']):b+=f'<section class="lesson-section" id="s{j+1}"><h2>{j+1:02} / {E(s["title"])}</h2><p>{E(s["text"])}</p></section>'
  b+=f'<aside class="takeaway"><small>TAKE THIS WITH YOU</small><p>{E(c["takeaway"])}</p></aside><section class="practice-box" id="practice"><h2>带到练习里，试一试</h2><p>{E(c["practice"])}</p><p class="muted" style="margin-top:12px">练习任务为本站入门编排／改编。按人数、场地和熟悉程度调整；这里的次数与距离不是统一要求。</p></section>'
  q=c['quiz'];b+=f'<form class="quiz" id="quiz" data-answer="{q["answer"]}" data-explanation="{E(q["explanation"])}"><h2>一道自测</h2><fieldset><legend>{E(q["question"])}</legend>'+''.join(f'<label><input type="radio" name="answer" value="{j}"><span>{E(text)}</span></label>' for j,text in enumerate(q['options']))+'</fieldset><button class="btn" type="submit">看看解释 →</button><p class="quiz-result" aria-live="polite"></p></form>'
  b+='<section class="source-box" id="sources"><h2>本课参考来源</h2>'+''.join(f'<a href="{E(s["url"])}" target="_blank" rel="noopener">{E(s["title"])} ↗</a>' for s in c['sources'])+'<p>正文为本站原创中文整理，训练任务与示例可能经过入门改编；来源中的年龄、赛制与专业训练背景不应直接照搬。规则以相应赛事适用版本为准。<a href="../sources.html">查看资料选择与编辑方式</a></p></section>'
  prev=LESSONS[i-1] if i else None;nxt=LESSONS[i+1] if i+1<len(LESSONS) else None
  b+='<nav class="next-prev" aria-label="课程翻页">'+(f'<a href="{prev["id"]}.html"><small>← 上一课</small>{E(prev["title"])}</a>' if prev else '<a href="../path.html"><small>回到路线</small>从零开始的学习地图</a>')+(f'<a href="{nxt["id"]}.html"><small>下一课 →</small>{E(nxt["title"])}</a>' if nxt else '<a href="../notebook.html"><small>去记录 →</small>写下下次想试的一件事</a>')+'</nav></article></div>'
  shell(c['title'],b,'learn/'+c['id']+'.html','catalog',c['id'],c['lead'])
def catalog():
 b=crumb([('全部课程',None)])+'<section class="page-intro"><div class="eyebrow">THE FULL HANDBOOK</div><h1>从一个问题，找到一节课。</h1><p>可以按板块浏览，也可以搜索“越位”“停球”“跑位”等关键词。每张卡片都会打开独立课程页面。</p></section><label class="read-small" for="course-search">搜索课程</label><input class="search-box" id="course-search" type="search" placeholder="你想弄明白什么？"><div class="toolbar"><button class="filter active" data-category-filter="all" aria-pressed="true">全部</button>'+''.join(f'<button class="filter" data-category-filter="{x[0]}" aria-pressed="false">{x[1]}</button>' for x in CATS)+'<label class="muted" style="margin-left:auto"><input id="only-saved" type="checkbox"> 只看收藏</label></div><p class="result-count" id="result-count">'+str(len(LESSONS))+' 节课程</p><div class="lesson-list">'+''.join(card(c,'',i+1) for i,c in enumerate(LESSONS))+'<p class="empty" id="no-results" hidden>暂时没有匹配课程。试试更短的关键词，或取消筛选。还没有的选题可以在制作对话中提出。</p></div>'
 shell('全部课程',b,'catalog.html','catalog')
def pathpage():
 steps=[('先认识这场比赛','不用先背完所有规则，先弄懂目标和你要参加的形式。',['how-game-works','formats-compared','local-rules']),('把第一次上场准备好','明确装备与约定，再给自己一个小目标。',['equipment','first-match']),('从能接住、能传稳开始','先处理简单的来球，再把观察带进接球前。',['first-touch','short-pass','scan-before-receive']),('没拿球，也能帮助球队','从一个接应角度和一次传后观察开始。',['support-space','after-pass','defend-cover']),('练一次，回到比赛验证','用适合人数的练习尝试，赛后只记一个具体片段。',['solo-practice','pair-practice','match-review'])]
 b=crumb([('从零开始',None)])+'<section class="page-intro"><div class="eyebrow">START SMALL. KEEP PLAYING.</div><h1>一条可以慢慢走的入门路线。</h1><p>顺序是建议，速度由你决定。读过不代表已经掌握；用练习与比赛，检验自己是否能用出来。</p></section><div class="path-layout"><div>'
 for i,(title,desc,ids) in enumerate(steps):
  b+=f'<section class="path-step"><span class="step-num">{i+1:02}</span><div><h2>{title}</h2><p>{desc}</p>'+''.join(f'<a href="learn/{id}.html" data-course="{id}">{E(BYID[id]["title"])} <span data-read-badge class="complete-badge"></span> ↗</a>' for id in ids)+'</div></section>'
 b+='</div><aside class="path-aside"><div class="eyebrow">YOUR OWN PACE</div><h2 style="font-size:26px;margin:15px 0">今天，只带走<br>一个小目标。</h2><p>例如：“传球后，我再观察一次。”<br>做到一次，就是一个可以记录的片段。</p><div class="progress-track"><span data-progress-bar></span></div><p data-progress-count>0 / 24 课已读</p><a class="btn lime" data-continue href="learn/how-game-works.html">从第一课开始 ↗</a><p class="muted" style="margin-top:18px;color:#c3d0bc">进度只保存在当前浏览器，不需要注册。</p></aside></div>'
 shell('从零开始',b,'path.html','path')
def notebook():
 b=crumb([('我的学习',None)])+'<section class="page-intro"><div class="eyebrow">YOUR FIELD NOTES</div><h1>把一次踢球，变成下一次的线索。</h1><p>这里保存你的收藏、阅读记录和小复盘。只有当前浏览器可以看到，不会上传到服务器。</p><p class="muted" data-storage-status>清理浏览器数据或换设备后不会自动同步；可以导出笔记留存。最多保留 50 条复盘。</p></section><div class="notice"><strong data-progress-count>0 / 24 课已读</strong> · 已读是阅读记录，不是能力评分。 <a class="text-link" data-continue href="path.html">回到学习路线 ↗</a></div><section class="section" style="padding-top:20px">'+section_head('SAVED LESSONS','我收藏的课程')+'<div class="lesson-list" id="saved-courses"></div></section><section class="section">'+section_head('ONE SCENE. ONE NEXT STEP.','写一个具体片段')+'<div class="notebook-grid"><form class="note-form" id="note-form"><label for="note-date">踢球／学习日期</label><input type="date" id="note-date" required><label for="note-scene">发生了什么？</label><textarea id="note-scene" maxlength="600" required placeholder="例如：队友在右边拿球，我站在防守人身后，一直没接到传球。"></textarea><label for="note-next">下次想尝试什么？</label><textarea id="note-next" maxlength="600" required placeholder="例如：先侧移打开角度，再看队友能否传到。"></textarea><button class="btn" type="submit">保存这条笔记 →</button><p id="note-status" class="muted" aria-live="polite" style="margin-top:12px"></p></form><div><button class="tool-btn" id="export-notes">↓ 导出笔记与阅读记录</button><div class="note-history" id="note-history"></div></div></div></section>'
 shell('我的学习',b,'notebook.html','notebook')
def sources():
 registry={}
 for c in LESSONS:
  for s in c['sources']:
   if s['url'] not in registry:registry[s['url']]={'title':s['title'],'courses':[]}
   registry[s['url']]['courses'].append(c)
 b=crumb([('资料来源',None)])+'<section class="page-intro"><div class="eyebrow">READ. CHECK. EXPLAIN.</div><h1>每一课，都能找到来处。</h1><p>优先使用 IFAB 规则、FIFA Training Centre 与足协官方教学。我们把概念整理成中文问题、原创示意图和练习任务，保留原始链接供继续学习。</p></section><div class="notice">首版核验日期：'+DATE+'。教学内容按专题编辑，不自动把搜索结果发布为课程。官方规则、教学原则与本站编排的练习会分开说明；青少年或精英训练资料只取适用原则，不照搬训练量。外部页面可能使用英文或需要登录，站内正文不依赖这些页面才能阅读。</div><div class="source-grid">'
 for i,(url,s) in enumerate(registry.items()):
  host=url.split('/')[2]
  b+=f'<article class="source-entry"><span class="eyebrow">SOURCE {i+1:02} / {E(host)}</span><h2 style="margin-top:13px">{E(s["title"])}</h2><a href="{E(url)}" target="_blank" rel="noopener">打开原始资料 ↗</a><div class="related">用于课程：'+ '、'.join(f'<a href="learn/{c["id"]}.html">{E(c["title"])}</a>' for c in s['courses'])+'</div></article>'
 b+='</div><div class="notice">后续扩充：在制作对话中提出问题，我们会查找来源、核验适用范围、补充独立课程，再更新目录和学习路线。当前版本没有自动抓取自媒体教学，也没有把机器生成内容直接上线。</div>'
 shell('资料来源与编辑说明',b,'sources.html','sources')
def build():
 OUT.mkdir(exist_ok=True);(OUT/'assets').mkdir(exist_ok=True)
 for name in ['style.css','app.js']:shutil.copyfile(ROOT/'assets'/name,OUT/'assets'/name)
 (OUT/'assets/favicon.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64"><rect width="64" height="64" rx="18" fill="#173e36"/><circle cx="32" cy="32" r="24" fill="none" stroke="#d7ef9d"/><text x="31" y="46" fill="#d7ef9d" font-size="42" font-family="Georgia" font-style="italic" text-anchor="middle">1</text></svg>')
 meta=[dict(id=c['id'],title=c['title'],category=c['category'],categoryName=META[c['category']]['name']) for c in LESSONS]
 (OUT/'assets/course-data.js').write_text('window.FOOTBALL_COURSES='+json.dumps(meta,ensure_ascii=False).replace('<','\\u003c')+';')
 homepage();category_pages();article_pages();catalog();pathpage();notebook();sources();(OUT/'.nojekyll').touch()
 print(f'Built {len(list(OUT.rglob("*.html")))} pages, {len(LESSONS)} lessons, {len(META)} chapters.')
if __name__=='__main__':build()
