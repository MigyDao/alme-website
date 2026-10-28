# ALME V3 visual prototype

Local-only review build on `prototype/v3-visual-system`, based on V2 commit `4bb49cc`. Production `public/`, main, and hosting configuration are unchanged. Nothing has been pushed or deployed.

Preview: serve this folder's `public/` over HTTP; Home and Solutions show the prototype and other routes preserve V2. No compilation step exists for this static site. The production build command remains `exit 0`.

## Implementation

- `scripts/build-v3-prototype.py`: reproducible copy of V2 into this isolated output, with targeted Home/Solutions visual changes.
- `scripts/v3-prototype.css`: responsive offering cards, process, navigation, compact project cards and photo CTA.
- `public/`: runnable snapshot including unchanged assets and supporting routes.
- `reference/Eco Brand Website V3 Design Board(1).png`: exact recovered user attachment.
- `provenance.json`: board hash, asset treatment and baseline.
- `scripts/verify-v3-prototype.cjs`, `scripts/audit-v3.cjs`: browser and accessibility verification.
- `verification.json`, `accessibility.json`, and desktop/mobile screenshots: recorded results.

The generator needs Pillow and BeautifulSoup. Browser checks need Playwright, Microsoft Edge and axe-core. The audit uses this machine's separately installed axe-core path; adapt it on another machine.

## Verification

Ten Home/Solutions layouts at 360, 540, 768, 1024 and 1440 px pass overflow, loaded image, four offering and ordered process checks. Keyboard focus, reduced motion, navigation without JavaScript and byte-identical existing brand assets pass. Six axe-core audits (360/768/1440 px, both pages) report zero WCAG A/AA or best-practice violations. The existing commercial suite passes 27 route/layout combinations and 165 internal links, including service-specific contact context and mobile menu behavior. Automated checks do not replace assistive technology or real-device user testing.

## Visual comparison and decisions

Reviewed desktop and mobile screenshots against the approved board. Offering illustrations are exact raster crops from that board, not newly generated illustrations. Navigation/process icons follow its labelled outline family. High-resolution separate offering masters would improve sharpness if these icons are enlarged later; current sizes stay near source resolution.

Authentic V2 project photographs replace the board's illustrative photo examples. Photographs retain their full frames. All existing approved commercial copy remains, so cards are taller than the board's short-copy examples. Existing About navigation remains and Home is added as specified. Existing footer information, contact destinations and brand assets remain, with supporting contact icons. The high-contrast CTA button uses cream on dark green for accessibility.

Only Home and Solutions receive this prototype layer. Rollout across the remaining V3 routes, production integration, deployment and broader performance QA remain separate tasks. No blocking design decision remains for this prototype; visual review is the next step.
