"""Independent homepage exploration; preserves all approved words and link targets."""
from pathlib import Path
import re
import shutil
ROOT = Path(__file__).resolve().parent.parent
html = (ROOT/'index.html').read_text()
assert 'class="home-exploration"' not in html, 'Run site/build.py to regenerate the base homepage first.'
html = html.replace('<body>', '<body class="home-exploration">')
html = html.replace('</head>', '<link rel="stylesheet" href="/home-design.css?v=1"></head>')
# Recompose each research direction without changing any of its content.
pattern = re.compile(r'(<a class="direction-card"[^>]*>)(.*?)</a>', re.S)
def direction(match):
    body=match.group(2)
    figure=re.search(r'<div class="card-figure">.*?</div>', body, re.S).group(0)
    copy=re.search(r'<div class="card-copy">(.*)</div>', body, re.S).group(1)
    split=copy.index('<span class="card-tags">')
    return match.group(1)+'<div class="card-copy">'+copy[:split]+'</div>'+figure+'<div class="card-resources">'+copy[split:]+'</div></a>'
html=pattern.sub(direction,html)
html=html.replace('<section class="research-section wrap"', '<div class="research-surface"><section class="research-section wrap"')
html=html.replace('</section><section class="news-section', '</section></div><section class="news-section')
(ROOT/'index.html').write_text(html)
(ROOT/'dist/index.html').write_text(html)
shutil.copy2(ROOT/'home-design.css',ROOT/'dist/home-design.css')
