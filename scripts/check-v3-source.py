"""Static build integrity and preservation checks for the framework-free slice."""
from pathlib import Path
import subprocess, json, re
from bs4 import BeautifulSoup
from PIL import Image
root = Path(__file__).resolve().parents[1]
provenance=json.loads((root/'docs/v3-extension/artwork-provenance.json').read_text())
board=Image.open(root/'docs/v3-extension'/provenance['source'])
for name,box in provenance['processCrops'].items():
    assert Image.open(root/f'public/assets/v3/process-{name}.png').tobytes()==board.crop(box).tobytes(), name
results = []
for route in ['index.html'] + [f'{r}/index.html' for r in ['solutions','shop','work','about','community','research','start-a-project']]:
    before = BeautifulSoup(subprocess.check_output(['git','show',f'4bb49cc:public/{route}'],cwd=root).decode(), 'html.parser')
    after = BeautifulSoup((root/'public'/route).read_text(encoding='utf-8'), 'html.parser')
    # Every existing text node and link survives, including commercial caveats.
    old = list(before.main.stripped_strings)
    new = iter(after.main.stripped_strings)
    assert all(any(value == candidate for candidate in new) for value in old), route
    for link in before.select('a[href]'):
        assert after.find('a',href=link['href']), (route,link['href'])
    ids = [e['id'] for e in after.select('[id]')]
    assert len(ids)==len(set(ids)), route
    assert not after.select('meta[name="robots"]'), route
    assert after.select_one('link[rel="canonical"]')['href']==before.select_one('link[rel="canonical"]')['href']
    for element in after.select('[src],link[rel="stylesheet"]'):
        url = element.get('src',element.get('href','')).split('?')[0]
        if url.startswith('/'):
            assert (root/'public'/url.lstrip('/')).is_file(), url
    assert all(not a.select('a,button') for a in after.select('a'))
    assert all(e.get('aria-hidden')=='true' for e in after.select('svg.v3-icon'))
    deployed = BeautifulSoup(subprocess.check_output(['git','show',f'5f6e69a:public/{route}'],cwd=root).decode(), 'html.parser')
    # Keep the complete existing photographic/brand image metadata and footer copy.
    for image in deployed.select('img'):
        assert any(candidate.attrs == image.attrs for candidate in after.find_all('img',src=image['src'])), (route,image['src'])
    assert deployed.select_one('.footer-contact').get_text()==after.select_one('.footer-contact').get_text(), route
    results.append({'route':route,'existingMainCopy':'preserved in order','existingLinks':'preserved','uniqueIds':'pass','assets':'resolved','canonical':'preserved','nestedControls':'none'})
subprocess.run(['git','diff','--check'],cwd=root,check=True)
for path in (root/'public/assets/js').glob('*.js'):
    subprocess.run(['node','--check',str(path)],check=True)
report={'build':'Static public directory; no compilation or package build configured. Asset integrity passes.','lint':'Git whitespace and Node syntax checks pass; no repository lint runner configured.','pages':results}
(root/'docs/v3-implementation/source-checks.json').write_text(json.dumps(report,indent=2))
print(json.dumps(report))
