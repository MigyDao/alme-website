"""Extend the existing visual system; extract process artwork without redrawing it."""
from pathlib import Path
from copy import deepcopy
import hashlib, json, sys, shutil
from PIL import Image
from bs4 import BeautifulSoup

root = Path(__file__).resolve().parents[1]
assets = root / 'public/assets/v3'
board = Path(sys.argv[1])
reference = root / 'docs/v3-extension'
reference.mkdir(exist_ok=True)
if board.resolve() != (reference / board.name).resolve():
    shutil.copyfile(board, reference / board.name)
im = Image.open(board)
names = ['understand','design','prototype','coordinate','build','improve']
# Exact 66px circular nodes from the full-size supplied board's How We Work row.
boxes = [(968,226,1034,292),(1058,226,1124,292),(1152,226,1218,292),
         (1247,226,1313,292),(1342,226,1408,292),(1436,226,1502,292)]
for name, box in zip(names, boxes):
    im.crop(box).save(assets / f'process-{name}.png')
csspath = assets / 'visual-system.css'
css = csspath.read_text(encoding='utf8').replace('Approved first V3 slice. Loaded only by Home and Solutions.', 'Shared approved V3 visual system across the public pages.')
css = css.split('/* Exact approved board nodes')[0].rstrip()+'\n'
css += '''
/* Exact approved board nodes retain their beige backing in both themes. */
.v3-node{background:transparent}
.v3-node img{width:66px;height:66px;border-radius:50%;display:block}
.v3-support .card,.v3-support .callout{background:var(--cream);border:1px solid var(--line);border-radius:.8rem}
.v3-support .card{transition:border-color 160ms ease,box-shadow 180ms ease}
.v3-support .card:focus-within{border-color:var(--green)}
@media(hover:hover){.v3-support .card:hover{border-color:var(--green);box-shadow:0 3px 12px #073b2218}}
.v3-card-cue{display:inline-flex;align-items:center;gap:.6rem;margin:0 0 .8rem;color:var(--green)}
.v3-card-cue .v3-icon{width:28px;height:28px}
.v3-support .hero>.v3-offering-art{float:right;margin:0 0 1rem 1.5rem}
[data-theme="dark"] .v3-card-cue{color:var(--ink)}
@media(max-width:540px){.v3-support .hero>.v3-offering-art{float:none;margin:0 0 1rem}}
@media(prefers-reduced-motion:reduce){.v3-support .card{transition:none}}
'''
csspath.write_text(css, encoding='utf8')
version = hashlib.sha256(css.encode()).hexdigest()[:12]
home = BeautifulSoup((root/'public/index.html').read_text(encoding='utf8'),'html.parser')
nav = home.select_one('.primary-nav')
footer = home.select_one('.footer-contact')
process = deepcopy(home.select_one('.v3-process'))
for node,name in zip(process.select('.v3-node'),names):
    node.clear()
    node.append(BeautifulSoup(f'<img src="/assets/v3/process-{name}.png" alt="" width="66" height="66">','html.parser').img)
routes=['index.html']+[f'{r}/index.html' for r in ['solutions','shop','work','about','community','research','start-a-project']]
for route in routes:
    path=root/'public'/route
    soup=BeautifulSoup(path.read_text(encoding='utf8'),'html.parser')
    style=soup.select_one('link[href^="/assets/v3/visual-system.css"]')
    if not style:
        style=soup.new_tag('link',rel='stylesheet')
        soup.head.append(style)
        script=soup.new_tag('script')
        script.string="document.documentElement.classList.add('js');"
        soup.head.insert(0,script)
        soup.body['class']=soup.body.get('class',[])+['v3-support']
        replacement=deepcopy(nav)
        for a in replacement.select('a'):
            a.attrs.pop('aria-current',None)
            if a['href']==('/'+route.removesuffix('index.html')): a['aria-current']='page'
        soup.select_one('.primary-nav').replace_with(replacement)
        for link in soup.select('.footer-contact a'):
            match=footer.find('a',href=link.get('href'))
            if match and match.svg: link.insert(0,deepcopy(match.svg))
        for cta in soup.select('.closing-cta'): cta['class'].append('v3-photo-cta')
        key={'shop':'Shop','work':'Work','about':'About','community':'Community','research':'Research','start-a-project':'Start a Project'}[path.parent.name]
        cue=next(a.svg for a in nav.select('a') if a.get_text(strip=True)==key)
        for card in soup.select('main .card'):
            span=soup.new_tag('span',attrs={'class':'v3-card-cue','aria-hidden':'true'})
            span.append(deepcopy(cue))
            media=card.select_one('.project-media')
            if media: media.insert_after(span)
            else: card.insert(0,span)
        if path.parent.name in ['shop','start-a-project']:
            art=deepcopy(home.select('.v3-offering-art')[3 if path.parent.name=='shop' else 2])
            soup.select_one('.hero').insert(0,art)
    style['href']=f'/assets/v3/visual-system.css?v={version}'
    for old in soup.select('.v3-process'): old.replace_with(deepcopy(process))
    if path.parent.name=='about' and not soup.select_one('.v3-process'):
        section=soup.new_tag('section',attrs={'class':'section','aria-labelledby':'v3-process-title'})
        content=soup.new_tag('div',attrs={'class':'container'})
        heading=soup.new_tag('h2',id='v3-process-title');heading.string='How we work'
        content.append(heading);content.append(deepcopy(process));section.append(content)
        soup.select_one('.closing-cta').insert_before(section)
    for svg in soup.select('svg[viewbox]'): svg['viewBox']=svg.attrs.pop('viewbox')
    path.write_text(str(soup),encoding='utf8')
(reference/'artwork-provenance.json').write_text(json.dumps({'source':board.name,'sha256':hashlib.sha256(board.read_bytes()).hexdigest(),'sourceDimensions':list(im.size),'processCrops':dict(zip(names,boxes)),'treatment':'Exact source pixels including original circular backing; no redrawing or generated artwork.','routes':routes},indent=2))
