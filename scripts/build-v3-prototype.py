"""Build an isolated static prototype; never write to production public/."""
from pathlib import Path
import shutil, hashlib, json
from bs4 import BeautifulSoup
from PIL import Image

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'prototypes/v3/public'
BOARD = ROOT / 'prototypes/v3/reference/Eco Brand Website V3 Design Board(1).png'
OUT.mkdir(parents=True, exist_ok=True)
shutil.copytree(ROOT / 'public', OUT, dirs_exist_ok=True)
assets = OUT / 'assets/v3'
assets.mkdir(exist_ok=True)
shutil.copyfile(ROOT / 'scripts/v3-prototype.css', assets / 'prototype.css')
board = Image.open(BOARD)
# Extract only approved offering illustrations, never the logo or example photos.
for i, box in enumerate([(72,226,222,346),(302,226,430,346),(536,226,674,339),(762,226,898,346)]):
    board.crop(box).save(assets / f'offering-{i}.png')
paths = {
 'home':'M3 11 12 3l9 8M5 10v11h5v-7h4v7h5V10',
 'solutions':'M3 3h7v7H3zM14 3h7v7h-7zM3 14h7v7H3zM14 14h7v7h-7z',
 'work':'M3 4h18v16H3zM3 17l6-6 4 4 3-3 5 5M7 8h.01',
 'shop':'M2 3h3l3 13h11l3-10H6M9 21h.01M18 21h.01',
 'research':'M12 5v16M12 5C8 2 4 3 2 4v16c4-2 7-1 10 1 3-2 6-3 10-1V4c-4-2-7-1-10 1',
 'community':'M8 14c-5 0-6 3-6 7M16 14c5 0 6 3 6 7M7 21v-3c0-6 10-6 10 0v3M9 7a3 3 0 1 0 6 0 3 3 0 1 0-6 0M2 8a2 2 0 1 0 4 0 2 2 0 1 0-4 0M18 8a2 2 0 1 0 4 0 2 2 0 1 0-4 0',
 'send':'m2 10 20-8-8 20-3-9-9-3zm9 3L22 2',
 'understand':'M9 18h6M10 22h4M8 15C0 5 10-2 17 4c5 5-1 10-2 11v3H9v-3',
 'design':'m3 17 13-13 4 4L7 21H3v-4zm10-10 4 4M3 17l4 4',
 'prototype':'m9 3 1-2h4l1 2 3 2 3 1v4l-2 2v3l1 3-4 2-3-1-3 1-4-2 1-3v-3L2 10V6l3-1 4-2zM8 11a4 4 0 1 0 8 0 4 4 0 1 0-8 0',
 'build':'m3 21 10-10-2-2 3-5 6-2-3 4 5 5-3 3-4-2L5 23z',
 'improve':'M12 22V9M12 15C3 16 2 9 3 5c7 0 10 4 9 10zM12 10C12 3 18 1 22 2c0 6-4 10-10 8z',
 'about':'M12 11v9M12 5h.01M2 12a10 10 0 1 0 20 0 10 10 0 1 0-20 0',
 'email':'M2 4h20v16H2zM2 4l10 9L22 4',
 'phone':'m4 2 5 4-2 4c2 4 3 5 7 7l4-2 4 5c-1 4-5 4-9 2C5 18 1 10 2 5z',
 'message':'M3 3h18v14H8l-5 4V3zM7 8h10M7 12h7',
}
def icon(name):
    return f'<svg class="v3-icon" viewBox="0 0 24 24" aria-hidden="true" focusable="false" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="{paths[name]}"/></svg>'
stages = [('Understand','Your needs, context and goals.','understand'),('Design','Practical, context-based solutions.','design'),('Prototype','Test, refine and validate.','prototype'),('Coordinate','People, materials and process.','community'),('Build','Implement with care and detail.','build'),('Improve','Learn, maintain and grow over time.','improve')]
process = '<ol class="v3-process" aria-label="How we work">' + ''.join(f'<li><span class="v3-node">{icon(k)}</span><h3>{label}</h3><p>{desc}</p></li>' for label,desc,k in stages) + '</ol>'
photos = [('end-grain-boards-768.webp','Hand-finished ALME end-grain cutting boards.'),('outdoor-shade-768.webp','ALME commercial fabric shade installation.'),('modern-black-kitchen-768.webp','Completed ALME kitchen installation.'),('hillside-garden-768.webp','Established ALME hillside growing system.')]
for route in ['index.html','solutions/index.html']:
    file = OUT / route
    soup = BeautifulSoup(file.read_text(encoding='utf-8'), 'html.parser')
    def fragment(html): return BeautifulSoup(html,'html.parser')
    soup.head.append(fragment('<meta name="robots" content="noindex,nofollow"><link rel="stylesheet" href="/assets/v3/prototype.css">'))
    nav = soup.select_one('.primary-nav')
    home = soup.new_tag('a', href='/'); home.string='Home'
    if route=='index.html': home['aria-current']='page'
    nav.insert(0,home)
    keys = {'Home':'home','Solutions':'solutions','Work':'work','Shop':'shop','Research':'research','Community':'community','Start a Project':'send','About':'about'}
    for a in nav.select('a'):
        a.insert(0,fragment(icon(keys[a.get_text(strip=True)])))
    if route=='index.html':
        offerings = soup.select('.section .grid')[0]
        offerings['class']=['grid','v3-offerings']
        cards=offerings.select(':scope > article')
    else:
        cards=soup.select('.container.grid > article')[:4]
    for i,card in enumerate(cards):
        card['class']=card.get('class',[])+['v3-offering']
        card.insert(0,fragment(f'<img class="v3-offering-art" src="/assets/v3/offering-{i}.png" alt="" width="150" height="120">'))
        a=card.select_one('a.text-link')
        if a: a['class']=['button','primary']
        photo,alt=photos[i]
        card.append(fragment(f'<figure class="v3-evidence"><img src="/assets/images/{photo}" alt="{alt}" loading="lazy" width="768" height="576"></figure>'))
    if route=='index.html':
        heading=soup.select_one('#how-we-work')
        heading.insert_after(fragment(process))
        for card in soup.select('[aria-labelledby="selected-work"] .card'):
            card['class'].append('v3-compact')
            heading=card.h3
            heading.insert_before(fragment('<p class="tag">Project</p>'))
    else:
        section=soup.new_tag('section',attrs={'class':'section','aria-labelledby':'v3-process-title'})
        section.append(fragment('<div class="container"><h2 id="v3-process-title">How we work</h2>'+process+'</div>'))
        soup.main.append(section)
    for cta in soup.select('.closing-cta'):
        cta['class'].append('v3-photo-cta')
    for a in soup.select('.footer-contact a'):
        href=a.get('href','')
        key='email' if href.startswith('mailto:') else 'phone' if href.startswith('tel:') else 'message'
        a.insert(0,fragment(icon(key)))
    file.write_text(str(soup),encoding='utf-8')
manifest={'baseline': '4bb49cc','board_sha256':hashlib.sha256(BOARD.read_bytes()).hexdigest(),'artwork':'Four exact offering illustration crops from approved board; no example photographs extracted.','logo':'Existing production brand assets copied byte-for-byte; no regeneration.','scope':['Home','Solutions'],'production_public_unchanged':True}
(ROOT/'prototypes/v3/provenance.json').write_text(json.dumps(manifest,indent=2))
print('Built prototypes/v3/public; production public/ untouched.')
