#!/usr/bin/env python3
"""Build the GitHub Pages site and the identical private-preview bundle.

Uses only the Python standard library. All editorial content lives in content.json.
The current public branch is never changed by this script.
"""
from pathlib import Path
from html import escape as esc
from datetime import datetime, date
from zoneinfo import ZoneInfo
import argparse
import json
import shutil
import re

ROOT = Path(__file__).resolve().parent.parent
DATA = json.loads((ROOT / 'site/content.json').read_text())
parser = argparse.ArgumentParser()
parser.add_argument('--publish', action='store_true', help='Build the public launch; allowed from the launch date.')
args = parser.parse_args()
now = datetime.now(ZoneInfo(DATA['launchTimezone']))
if args.publish and now.date() < date.fromisoformat(DATA['launchDate']):
    parser.error('The public launch is scheduled for ' + DATA['launchDate'] + '; build a preview without --publish.')
PUBLIC = args.publish
ORIGIN = 'https://keke-long.github.io'
PAGES = {}
DIRECTIONS = DATA['directions']
NAME = DATA['name'] + (' · ' + DATA['chineseName'] if DATA['chineseName'] else '')

def a(url, text, cls=''):
    return f'<a href="{esc(url, quote=True)}"' + (f' class="{cls}"' if cls else '') + f'>{esc(text)}</a>'

def image(path, alt, cls='', eager=False):
    return f'<img src="/{esc(path)}" alt="{esc(alt, quote=True)}" class="{cls}" loading="{"eager" if eager else "lazy"}" decoding="async">'

def shell(path, title, description, body, active):
    if DATA['people'] and active == 'about':
        active = 'people'
    nav = [('Home','/','home'),('Research','/research/','research'),('About Me','/about/','about')]
    if DATA['people']:
        nav[2] = ('People','/people/','people')
    if DATA['courses']:
        nav.append(('Teaching','/teaching/','teaching'))
    nav.append(('Join Us','/join/','join'))
    links = ''.join(f'<a href="{href}"' + (' aria-current="page"' if key == active else '') + (' class="nav-join"' if key=='join' else '') + f'>{label}</a>' for label,href,key in nav)
    mark = image(DATA['logo'], 'Rutgers University', 'university-logo', True) if DATA['logo'] else ''
    fulltitle = f'{title} | {NAME}' if path != '/' else f'{DATA["labName"]} | {NAME} | Rutgers University'
    robots = 'index, follow, noimageindex' if PUBLIC else 'noindex, nofollow, noimageindex'
    structured = {'@context':'https://schema.org','@type':'Person','name':DATA['name'],'url':ORIGIN+'/about/','sameAs':[DATA['scholar'],DATA['github'],'https://catslab.engr.wisc.edu/staff/long-keke/']}
    if DATA['chineseName']:
        structured['alternateName'] = DATA['chineseName']
    if PUBLIC:
        structured.update(jobTitle='Assistant Professor',affiliation={'@type':'Organization','name':'Rutgers University'})
    year = now.year if PUBLIC else 2026
    page = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(fulltitle)}</title><meta name="description" content="{esc(description, quote=True)}">
<meta name="robots" content="{robots}"><link rel="canonical" href="{ORIGIN}{path}">
<meta property="og:site_name" content="{esc(DATA['labName'])}"><meta property="og:title" content="{esc(fulltitle, quote=True)}"><meta property="og:description" content="{esc(description, quote=True)}">
<link rel="icon" href="/favicon.svg?v=20260908-r" type="image/svg+xml"><link rel="stylesheet" href="/style.css?v=20260908-teal-type">
<script type="application/ld+json">{json.dumps(structured,ensure_ascii=False).replace('</','<\\/')}</script>
<script src="/site.js" defer></script></head><body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header"><div class="header-inner"><a class="identity" href="/" aria-label="{esc(DATA['labName'], quote=True)} home">{mark}<span class="identity-text"><strong>{esc(DATA['labName'])}</strong><span>Rutgers University</span></span></a>
<button class="menu-toggle" type="button" aria-expanded="false" aria-controls="navigation">Menu <span aria-hidden="true">☰</span></button>
<nav id="navigation" aria-label="Main navigation">{links}</nav></div></header>
<main id="main">{body}</main>
<footer class="site-footer"><div class="footer-inner"><div><strong>{esc(DATA['labName'])} @ Rutgers University</strong><p class="footer-address">Department of Civil and Environmental Engineering<br>Rutgers University–New Brunswick<span class="footer-location">Piscataway, NJ, USA</span></p></div><div class="footer-meta"><div class="footer-links">{a(DATA['scholar'],'Google Scholar')}{a(DATA['github'],'GitHub')}{a('/about/','About Keke Long')}</div><p class="copyright">© {year} {esc(NAME)}</p></div></div></footer>
</body></html>'''
    PAGES[path] = page

def research_cards():
    illustrations = [DIRECTIONS[0]['projects'][1], DIRECTIONS[1]['projects'][0], DIRECTIONS[2]['projects'][0]]
    tags = ['Physics-enhanced learning · VLMs', 'Field testing · Safety evaluation', 'Traffic sensing · Digital twins']
    cards = []
    for i, d in enumerate(DIRECTIONS):
        p=illustrations[i]
        cards.append(f'''<a class="direction-card" href="/research/{d['slug']}/">
<div class="card-figure">{image(p['image'],p['alt'])}</div><div class="card-copy"><span class="eyebrow">Research / 0{i+1}</span><h3>{esc(d['title'])}</h3><p>{esc(d['description'])}</p><span class="card-tags">{tags[i]}</span><span class="text-link">Explore this direction <span aria-hidden="true">↗</span></span></div></a>''')
    return '<div class="direction-grid">'+''.join(cards)+'</div>'

def project_links(p):
    return '<div class="project-links">'+''.join(a(l['url'],l['label'],'resource-link') for l in p['links'])+'</div>'

def project_row(p):
    publication = f'<p class="publication">{esc(p["publication"])}</p>' if p['publication'] else ''
    return f'''<article class="project-row"><figure class="project-image">{image(p['image'],p['alt'])}</figure><div class="project-copy"><span class="eyebrow">{esc(p['kind'])}</span><h2>{esc(p['title'])}</h2>{publication}{project_links(p)}</div></article>'''

hero = '''<section class="hero wrap" aria-labelledby="hero-title"><div class="hero-copy"><p class="eyebrow">Physics-Enhanced AI · CAVs · ITS</p><h1 id="hero-title">Building Transportation AI<br>that can be <em>Trusted.</em></h1><p class="hero-description">Physics-enhanced learning, connected and automated vehicles, and intelligent transportation systems.</p></div>
<div class="concept" role="img" aria-label="Safety and Mobility at the center of Control, Reason, Perception, and Validate."><div class="loop"><div class="core">Safety &amp;<br>Mobility</div><span class="lab la">Control</span><span class="lab lb">Reason</span><span class="lab lc">Perception</span><span class="lab ld">Validate</span></div></div></section>'''
def news_paragraph(text):
    """One editable paragraph; Markdown links keep news maintenance simple."""
    parts = []
    position = 0
    for match in re.finditer(r'\[([^\]]+)\]\((https?://[^)\s]+)\)', text):
        parts.append(esc(text[position:match.start()]))
        parts.append(a(match.group(2), match.group(1)))
        position = match.end()
    parts.append(esc(text[position:]))
    return ''.join(parts)

news_rows = []
for item in DATA.get('news', []):
    label = datetime.strptime(item['date'], '%Y-%m').strftime('%B %Y')
    news_rows.append(f'<article class="news-row"><time datetime="{esc(item["date"])}">{label}</time><p>{news_paragraph(item["text"])}</p></article>')
news = '<section class="news-section wrap" id="news"><div class="section-heading"><h2>News</h2></div>' + ''.join(news_rows) + '</section>'

home = hero + '<section class="research-section wrap" id="research"><div class="section-heading"><h2>Research Directions</h2></div>'+research_cards()+'</section>'+news
shell('/','Home','Keke Long’s Lab: physics-enhanced AI, connected and automated vehicles, and intelligent transportation systems. Selected research, datasets, and platforms.',home,'home')

research = '<div class="wrap"><header class="page-heading"><p class="eyebrow">Research</p><h1>Three connected directions.</h1><p>Developing physically consistent AI methods, evaluating connected and automated vehicles, and connecting people, vehicles, and infrastructure.</p></header>'+research_cards()+'<p class="scholar-note">'+a(DATA['scholar'],'Full publication record on Google Scholar')+'</p></div>'
shell('/research/','Research','Explore Keke Long’s three research directions, with selected papers, datasets, and platforms.',research,'research')
for i,d in enumerate(DIRECTIONS):
    body=f'''<div class="wrap"><header class="page-heading"><div class="breadcrumb">{a('/research/','Research')}<span>/</span><span>0{i+1}</span></div><h1>{esc(d['title'])}</h1><p>{esc(d['description'])}</p></header><div class="projects">{''.join(project_row(p) for p in d['projects'])}</div><nav class="direction-switch" aria-label="Other research directions">{''.join(a('/research/'+o['slug']+'/',o['title']) for o in DIRECTIONS if o!=d)}</nav></div>'''
    shell('/research/'+d['slug']+'/',d['title'],d['description'],body,'research')

bio = ('I am an Assistant Professor in the Department of Civil and Environmental Engineering at Rutgers University.' if PUBLIC else 'I am a postdoctoral Research Associate at the University of Wisconsin–Madison. I will join the Department of Civil and Environmental Engineering at Rutgers University as an Assistant Professor in January 2027.')
location_html = '<p>Madison, WI, USA</p>' if not PUBLIC else ''
appointment = '<div class="appointment"><span class="eyebrow">'+('Rutgers University' if PUBLIC else 'Incoming appointment · January 2027')+'</span><p>Assistant Professor<br>Civil and Environmental Engineering<br>Rutgers University</p></div>'
about = f'''<div class="wrap"><header class="about-heading"><div><p class="eyebrow">About Me</p><h1>{esc(NAME)}</h1><p>{bio}</p><p>My research develops physics-enhanced AI for intelligent transportation systems, with applications in CAV decision-making, control, perception, and safety evaluation.</p><div class="project-links">{a(DATA['scholar'],'Google Scholar','resource-link')}{a(DATA['github'],'GitHub','resource-link')}</div></div>{image('assets/images/profile.jpg','Keke Long','portrait',True)}</header><div class="about-grid"><aside>{appointment}<div class="contact-block"><h2>Contact</h2>{location_html}<p>klong23 AT wisc . edu</p>{a('/join/','Prospective students','text-link')}</div></aside><div class="profile-content">'''
if not PUBLIC:
    about += '<section id="affiliation">'+DATA['profileSections']['affiliation']+'</section>'
for section in ['education','teaching','service']:
    about += '<section id="'+section+'">'+DATA['profileSections'][section]+'</section>'
about += '</div></div></div>'
shell('/about/','About Me','Keke Long’s academic background, research interests, teaching experience, and service.',about,'about')

widths=[118,117,117,118,118,117,117,118,118,117]
slices=''.join(f'<img src="/assets/images/notice-slices/notice-{i:02}.png" alt="" aria-hidden="true" width="{w}" height="331" style="flex:{w} 0 0">' for i,w in enumerate(widths,1))
join=f'''<div class="wrap join-page"><header class="page-heading"><p class="eyebrow">Join us</p><h1>Explore what comes next.</h1><p>Research opportunities at {esc(DATA['labName'])}.<br>Rutgers University · Civil and Environmental Engineering</p></header><div class="announcement-viewport" tabindex="0" aria-label="Research group announcement. Scroll horizontally on small screens to read the full announcement."><div class="notice-strip" role="img" aria-label="Research group announcement">{slices}</div></div><p class="mobile-note">Swipe across the announcement to read it in full.</p><div class="join-research"><h2>Get to know the research.</h2><p>Explore the three research directions and the selected work within each.</p>{a('/research/','Explore research','text-link')}</div></div>'''
shell('/join/','Join Us','Research opportunities at Keke Long’s Lab, Rutgers University.',join,'join')

# Optional sections appear only after real records have been added.
if DATA['people']:
    members = '<article class="member">'+'<a href="/about/">'+image('assets/images/profile.jpg','Keke Long')+'</a><h2>'+a('/about/',NAME)+'</h2><p>Faculty</p></article>'
    for m in DATA['people']:
        members += '<article class="member">'+(('<a href="'+esc(m['url'],quote=True)+'">'+image(m['image'],m['name'])+'</a>') if m.get('image') and m.get('url') else (image(m['image'],m['name']) if m.get('image') else ''))+'<h2>'+ (a(m['url'],m['name']) if m.get('url') else esc(m['name']))+'</h2><p>'+esc(m['role'])+'</p></article>'
    shell('/people/','People','Members of Keke Long’s Lab.','<div class="wrap"><header class="page-heading"><p class="eyebrow">People</p><h1>Our team.</h1></header><div class="member-grid">'+members+'</div></div>','people')
if DATA['courses']:
    courses=''.join('<article class="course"><p class="eyebrow">'+esc(c['term'])+'</p><h2>'+a(c['url'],c['title'])+'</h2><p>'+esc(c['description'])+'</p></article>' for c in DATA['courses'])
    shell('/teaching/','Teaching','Courses taught by Keke Long at Rutgers University.','<div class="wrap"><header class="page-heading"><p class="eyebrow">Teaching</p><h1>Courses.</h1></header>'+courses+'</div>','teaching')

# Preserve the old direction URL and old homepage anchor entrypoints.
shell('/research/trustworthy-ai/','Physics-Enhanced AI for Transportation','Physics-enhanced AI research by Keke Long.','<div class="wrap"><header class="page-heading"><h1>Physics-Enhanced AI for Transportation</h1><p>'+a('/research/physics-enhanced-learning/','Continue to Physics-Enhanced AI for Transportation')+'</p></header></div>','research')
PAGES['/research/trustworthy-ai/'] = PAGES['/research/trustworthy-ai/'].replace('</head>', '<meta http-equiv="refresh" content="0; url=/research/physics-enhanced-learning/"></head>').replace(ORIGIN+'/research/trustworthy-ai/', ORIGIN+'/research/physics-enhanced-learning/')
shell('/404.html','Page not found','Find research and information from Keke Long’s Lab.','<div class="wrap"><header class="page-heading"><p class="eyebrow">404</p><h1>Page not found.</h1><p>'+a('/','Return to the homepage')+' or '+a('/research/','explore the research')+'.</p></header></div>','')

dist=ROOT/'dist'
dist.mkdir(exist_ok=True)
for path,content in PAGES.items():
    file=path.strip('/')+'/index.html' if path!='/' else 'index.html'
    if path.endswith('.html'): file=path.lstrip('/')
    for target in [ROOT/file,dist/file]:
        target.parent.mkdir(parents=True,exist_ok=True)
        target.write_text(content)
for f in ['style.css','site.js','favicon.svg','googlef00f54f7e6fde37a.html']:
    if (ROOT/f).exists(): shutil.copy2(ROOT/f,dist/f)
shutil.copytree(ROOT/'assets',dist/'assets',dirs_exist_ok=True)
robots='User-agent: *\nAllow: /\nSitemap: '+ORIGIN+'/sitemap.xml\n' if PUBLIC else 'User-agent: *\nDisallow: /\n'
sitemap='<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join('<url><loc>'+ORIGIN+p+'</loc></url>' for p in PAGES if p not in ['/404.html','/research/trustworthy-ai/'])+'</urlset>\n'
for folder in [ROOT,dist]:
    (folder/'robots.txt').write_text(robots)
    (folder/'sitemap.xml').write_text(sitemap)
    (folder/'.nojekyll').write_text('')
print(f'Built {len(PAGES)} pages in '+('PUBLIC' if PUBLIC else 'PREVIEW')+' mode.')
