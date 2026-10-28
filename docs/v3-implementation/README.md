# V3 first production visual slice — October 28, 2026

Implemented locally on `implementation/v3-first-slice`. V2 remains protected at `main` / `4bb49ccf940b1d07f3aaea8ef8a702c1be213caa`; the approved isolated prototype remains at `18cba10e59025d3598998c7dac281444e03a6a8a`. No push, deployment, main merge, hosting change, or final QA/release progression.

## Exact changes

- Home and Solutions load `public/assets/v3/visual-system.css` with a content hash for cache refresh. The prototype-only robots exclusion is removed; existing canonical and social metadata remain.
- Four offering cards reuse the exact approved-board illustration crops. Existing titles, explanations, property-care limitations and CTA destinations remain. Duplicate visible offering actions gain offering-specific accessible names.
- Labelled, decorative SVG navigation icons, the approved six-stage ordered process (Understand → Design → Prototype → Coordinate → Build → Improve), Home compact project cards, photographic closing CTAs and footer contact icons reuse the prototype.
- Existing authentic project images retain their full frames. New supporting image descriptions avoid overstating project authorship. Existing header/footer logo files remain byte-identical to the approved prototype/V2 working tree. No logo generation or substitution.
- Buttons have minimum 44px height; interaction feedback uses stable borders/shadows and 160–180ms transitions. Existing high-contrast focus/current-page treatment remains. Scroll spacing keeps focus clear of the variable-height header; an open mobile menu uses a non-sticky header. Reduced motion disables nonessential transitions and animation. Optional dark preview remains usable, while the default remains light.
- All 40 other pre-existing public files are unchanged relative to V2 (text comparisons normalize Git CRLF line endings; binary comparisons are exact). The prototype, supporting routes, shared V2 CSS/JS, commercial architecture and intake behavior remain intact.

## Verification

- `source-checks.json`: static output/assets resolved, original main copy retained in order, existing links/canonical preserved, unique IDs, no nested interactive controls, whitespace and JavaScript syntax checks pass.
- `verification.json`: 20 Home/Solutions layouts at 320, 360, 540, 768, 800, 801, 1024, 1200, 1280 and 1440px; no overflow, four cards, ordered process, loaded images, labelled icons, focus, reduced motion and navigation without JavaScript pass. Brand assets match the V2 prototype byte for byte.
- `accessibility.json`: six axe-core audits at 320/768/1440px covering WCAG A/AA, 2.1 AA, 2.2 AA and best practices; zero detected violations.
- `interactions.json`: both pages in light/dark previews pass browser-driven keyboard focus visibility/obscuration checks, mobile Escape focus return, 44px offering actions, reduced motion, 320px reflow and four additional axe audits with zero violations.
- Existing commercial E2E suite: 27 route/layout combinations, 165 internal links, four commercial offerings, property-care contact context, mobile menu, JavaScript-disabled navigation and no page errors pass.
- Reviewed `home-1440.png`, `home-360.png`, `solutions-1440.png`, `solutions-360.png` against the approved board. Authentic V2 photographs and existing copy remain; card heights follow their full copy rather than shortening it to the board examples.

The initial E2E attempt lost its short-lived local server and was rerun successfully on a persistent server. Keyboard assertions wait for native smooth scrolling to settle. The baseline text check normalizes Git line endings; no source/logo fix was needed for that comparison.

## Reproduce

No framework compilation, package build, lint runner or unit-test runner exists in this static repository. The configured hosting build remains `exit 0` with `public` as output. Static integrity, syntax/whitespace checks and browser/E2E suites provide the applicable build/lint/test evidence; no invented package-script passes are claimed.

With Python (BeautifulSoup), Node, Playwright, Edge and axe-core available, serve `public` at `127.0.0.1:8874`, then run:

```text
python scripts/check-v3-source.py
node scripts/verify-v3-implementation.cjs
node scripts/audit-v3-implementation.cjs
node scripts/check-v3-interactions.cjs
BASE_URL=http://127.0.0.1:8874 node scripts/verify-commercial-alignment.cjs
```

On Windows set `BASE_URL` with PowerShell's `$env:BASE_URL` syntax. Set `NODE_PATH` to the installed Playwright package directory if needed. Audit scripts use the existing local axe-core installation path. `python scripts/integrate-v3.py` reproduces the integration from the preserved prototype and rules.

## Separate final QA boundary

This completes implementation verification only. Real devices, screen readers/assistive technology, actual browser zoom, cross-browser and broader performance/release checks remain for the separate final QA task. Narrow viewport reflow and browser automation do not claim those manual checks or full accessibility certification. Offering illustration masters remain the approved board crops; do not enlarge beyond their intended sizes without separate approved artwork.
