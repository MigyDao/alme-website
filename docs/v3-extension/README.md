# V3 process artwork and remaining public pages

October 28, 2026. Baseline: deployed `5f6e69ae37b45866673752ace88ca3b4b942b4a8`. Work remains on `implementation/v3-first-slice`; no push, deployment, hosting change or form submission.

## Changes

- Home and Solutions replace all six simplified process SVGs with exact artwork crops from the supplied `Eco Brand Website V3 Design Board(2).png`. Original beige circles and detailed lightbulb, pencil, gear, people, hammer and leaf artwork are retained. Nothing redrawn or generated. Source board, original reported screenshot and pixel coordinates are included beside this document.
- Shop, Work, About, Community, Research and Start a Project load the same shared V3 stylesheet and labelled navigation as Home/Solutions, with the correct current-page state and mobile first-paint behavior. Existing cards use the shared warm surface, rounded border and restrained interaction treatment, with existing navigation symbols as content cues. Existing closing CTAs use the same authentic garden photograph treatment. Shop and Start a Project reuse the relevant approved offering illustrations.
- About includes the same ordered six-stage process used on Home/Solutions. No process is added to contexts where it would distract from the page's purpose.
- Existing text and information architecture, all original image attributes, footer text, links, metadata, branded logos, community/commercial separation, property-care boundaries and contact behavior are preserved. The 404 remains unchanged.

`scripts/extend-v3.py` performs the extension using the supplied board. `artwork-provenance.json` records source hash, original dimensions and exact crop boxes. `scripts/check-v3-source.py` now checks all eight pages, exact process pixels, original photographic metadata and footer text. The old two-page-only exclusion in the interaction preservation check now allows the eight explicitly approved pages; the other 34 V2 baseline files still must match.

## Verification

See `verification.json` for the page-wide light/dark audit results and the adjacent desktop/mobile screenshots. Existing suites and source evidence remain in `docs/v3-implementation`.

- Full extension: 48 layouts and axe audits (eight pages × three widths × two themes), zero violations; loaded/decoded images, correct labelled/current navigation, process assets and mobile Escape focus return pass. All eight routes work without JavaScript. Zero page errors.
- Work screenshot review prompted moving the content cue below its photograph to preserve the original edge-to-edge image spacing. The final Work page separately passes all six layout/theme audits and no-JavaScript navigation; see `work-refinement.json`.
- Existing V3 implementation: all 20 Home/Solutions layouts pass. Existing responsive axe suite: six audits, zero violations. Existing interaction suite: four light/dark scenarios, zero violations; keyboard focus/header clearance, Escape return, 44px offering actions, reduced motion and reflow pass.
- Commercial regression: 27 layouts, 171 internal links/fragments, offering headings, property-care contact context, mobile menu and no-JavaScript behavior pass; zero page errors.
- Source checks: all eight pages preserve copy, links, canonicals, original image attributes and footer text; exact source pixels, resolved assets, unique IDs and no nested controls pass. All 34 other pre-existing V2 public files and all authentic branding remain unchanged. JavaScript syntax and whitespace checks pass.

Desktop/mobile screenshots were visually reviewed for Home, Shop, About, Work, Community, Research and Start a Project, with Solutions additionally covered by the existing first-slice screenshot review and automated suites.

Commands (PowerShell, with Playwright on NODE_PATH and installed Edge):

```powershell
python -m http.server 8874 --bind 127.0.0.1 --directory public
python scripts/check-v3-source.py
node scripts/verify-v3-implementation.cjs
node scripts/audit-v3-implementation.cjs
node scripts/check-v3-interactions.cjs
$env:BASE_URL='http://127.0.0.1:8874'
node scripts/verify-commercial-alignment.cjs
node scripts/verify-v3-extension.cjs
git diff --check
```

Local verification used an isolated server at port 8891 after the existing port 8874 became unreliable. For the existing hardcoded scripts, temporary copies changed only the target port; the extension/commercial scripts accept BASE_URL. Initial interrupted image checks were rerun after waiting for responsive-image requests to settle before decoding. Prototype files are historical first-slice evidence and were not regenerated.

## Limitations and release boundary

The supplied board is raster artwork, so the exact process assets retain its native 66px dimensions; no unavailable vector masters are implied. Mobile and desktop browser screenshots are evidence of browser rendering, not physical-device testing. Physical-device touch, screen readers/assistive technology, cross-browser/native contact-app handoffs and broader performance/field checks remain manual limitations. Tally activation and V1/public-link cutover remain separate. This commit is for review; production remains at the verified first-slice baseline until a controlled release.
