"""Promote the approved, committed prototype into the first production slice."""
from pathlib import Path
import shutil, hashlib
from bs4 import BeautifulSoup

root = Path(__file__).resolve().parents[1]
assets = root / 'public/assets/v3'
assets.mkdir(exist_ok=True)
for file in (root / 'prototypes/v3/public/assets/v3').glob('offering-*.png'):
    shutil.copyfile(file, assets / file.name)
css = (root / 'scripts/v3-prototype.css').read_text(encoding='utf-8')
css = css.replace('/* Scoped to the isolated V3 prototype. Existing ALME palette and V2 footer. */', '/* Approved first V3 slice. Loaded only by Home and Solutions. */')
css += '''
/* Interaction rules: stable layout, labelled actions, comfortable touch targets. */
.v3-offering>.button{display:inline-flex;align-items:center;min-height:44px}
.button,.primary-nav a,.v3-offering,.v3-compact{transition:background-color 160ms ease,border-color 160ms ease,box-shadow 180ms ease}
.button:active,.primary-nav a:active{box-shadow:inset 0 0 0 2px currentColor}
.v3-offering:focus-within,.v3-compact:focus-within{border-color:var(--green)}
@media(hover:hover){.v3-offering:hover,.v3-compact:hover{border-color:var(--green);box-shadow:0 3px 12px #073b2218}.button:hover{box-shadow:inset 0 0 0 2px currentColor}}
/* Keep keyboard focus and anchors clear of the variable-height header. */
html{scroll-padding-top:200px}
[id],a,button{scroll-margin-top:200px}
@media(max-width:800px){.site-header:has(.primary-nav.open){position:relative}html{scroll-padding-top:110px}[id],a,button{scroll-margin-top:110px}}
[data-theme="dark"] .v3-offering-art{mix-blend-mode:normal;background:#fbf5ea}
.v3-photo-cta .button.primary{border-color:#fffdf8}
[data-theme="dark"] .v3-photo-cta .button.primary{background:#fffdf8;color:#073b22;border-color:#fffdf8}
@media(prefers-reduced-motion:reduce){*,*:before,*:after{animation:none!important;transition:none!important;scroll-behavior:auto!important}}
'''
(assets / 'visual-system.css').write_text(css, encoding='utf-8')
version = hashlib.sha256(css.encode()).hexdigest()[:12]
for route in ['index.html', 'solutions/index.html']:
    soup = BeautifulSoup((root / 'prototypes/v3/public' / route).read_text(encoding='utf-8'), 'html.parser')
    soup.select_one('meta[name="robots"]').decompose()
    soup.select_one('link[href="/assets/v3/prototype.css"]')['href'] = f'/assets/v3/visual-system.css?v={version}'
    for svg in soup.select('svg[viewbox]'):
        svg['viewBox'] = svg.attrs.pop('viewbox')
    # Preserve visible approved copy; disambiguate repeated actions for AT users.
    for card in soup.select('.v3-offering'):
        heading = card.select_one('h2,h3')
        for link in card.select('a'):
            label = link.get_text(' ', strip=True)
            if label == 'Explore this offering →':
                link['aria-label'] = f'Explore this offering: {heading.get_text(" ", strip=True)}'
    # Existing photograph descriptions carry their source-specific context.
    alts = ['ALME end-grain cutting boards.', 'Tensioned fabric canopy at BizTown.', 'Modern black kitchen installation; see Work for contribution details.', 'Hillside food garden in Linstead.']
    for card, alt in zip(soup.select('.v3-offering'), alts):
        card.select_one('.v3-evidence img')['alt'] = alt
    (root / 'public' / route).write_text(str(soup), encoding='utf-8')
print('Integrated Home and Solutions; existing brand files and supporting routes untouched.')
