# ALME Website V2

Framework-free static website for A Likkle More Eco: practical solutions for spaces, production and land.

## Routes

`/` · `/solutions/` · `/shop/` · `/work/` · `/about/` · `/community/` · `/research/` · `/start-a-project/`

## Development and deployment

The site uses semantic HTML, one shared stylesheet, and minimal vanilla JavaScript. Cloudflare Pages is configured for the `main` branch with framework preset **None**, build command `exit 0`, and output directory `public`.

V1 remains live while V2 is built and tested. Do not retire the V1/TinyURL navigation until launch-critical QA passes on the public Pages address.

## Visual evidence and conversion

Approved project photographs are delivered as responsive WebP assets with three sizes per source, explicit intrinsic dimensions, descriptive alt text and below-fold lazy loading. The full photographs are retained without cropping or retouching. Source originals remain in Drive and outside `public`; provenance, original dimensions and exact output byte sizes are recorded in [`docs/visual-assets.json`](docs/visual-assets.json).

- Home: modular platform bed, outdoor shade and hillside garden, immediately after the four service families.
- Work: modern black kitchen, platform bed, outdoor shade, hillside garden and the existing design-capability composite. The composite is explicitly distinguished from a photograph of a completed project; portfolio contribution caveats remain intact.
- Shop: end-grain cutting-board craft photograph as context, with the existing twelve catalogue entries unchanged.

Home follows Hero → service families → Selected work → How we work → Build for Useful Life → final enquiry CTA. Solutions, Work and About have closing conversion blocks; Research offers an email contribution route. Commercial and Community intake paths remain separate.

The shared stylesheet uses contrasting green/cream keyboard focus rings and a content-version query to refresh cached styles. Every page footer exposes email, telephone and WhatsApp links. The custom 404 includes `noindex`; no catch-all redirect or SPA fallback is installed.

## Remaining launch work

Keep the text brand treatment for this stage. Approved logo/social imagery, the separate Tally intake integration, real-device mail/telephone/WhatsApp handoffs, public-link/QR review and the V1 launch cutover remain separate work. Passing this imagery/conversion update does not itself authorize retiring V1 or expanding the Shop from the offering database.
