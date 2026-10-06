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
- Shop: four curated offerings with the end-grain cutting-board photograph explicitly presented as craftsmanship evidence only.

Home follows Hero → service families → Selected work → How we work → Build for Useful Life → final enquiry CTA. Solutions, Work and About have closing conversion blocks; Research offers an email contribution route. Commercial and Community intake paths remain separate.

The shared stylesheet uses contrasting green/cream keyboard focus rings and a content-version query to refresh cached styles. Every page footer exposes email, telephone and WhatsApp links. The custom 404 includes `noindex`; no catch-all redirect or SPA fallback is installed.

## Shop curation

The public catalogue follows **Website V2 Shop Curation Plan — V1** and is independent of internal Offering `Sales Readiness` values. It currently lists:

- Growing & Garden: Custom Compost Systems, Custom Trellis & Climbing Supports, and Raised Garden Beds.
- Resource & Resilience: Rainwater Collection Kit & Setup.

Compost and trellis are custom/made-to-order capabilities. Their developing modular standard families are modelled and have not been field-tested. Raised-bed dimensions/materials and rainwater scope/component supply are agreed for each site; no standardized sizes, prices or validated variants are advertised.

Raised Planters, Protective Plant Cages, Harvest Basket, Solar Dehydrator, Shade Covering, Garden Work Seating, Combined Growing System, and Land Management & Gardening Consultancy are held from the Shop until their customer-facing scopes and supporting evidence are sufficiently defined. Their internal records remain intact. The shade installation remains on Work as portfolio evidence.

The cutting-board photograph is making evidence, not a catalogue listing. The primary order enquiry continues to `/start-a-project/`. Future Shop additions need a clear commercial scope and appropriate maturity/evidence, rather than automatic publication from the Offering database.

## Production brand — v04

The approved ALME v04 package supplies the horizontal header logo, white footer mark and small-icon artwork. Browser/Apple/site icons are proportional derivatives of the supplied small icon. The default 1200 × 630 social image uses the approved horizontal logo and primary positioning on warm cream; it contains no generated project photography. Every HTML page includes favicon, manifest and Open Graph/Twitter image metadata.

The existing forest/leaf/cream/gold palette matches v04. Display headings use Bahnschrift when available, followed by Arial Narrow, Segoe UI and Arial; body text keeps Segoe UI/Arial. The site does not redistribute platform fonts or add external font requests. Accessible dark label colours and contrasting keyboard-focus rings take precedence over decorative leaf-green text.

Source hashes, Drive references and derivative sizes are recorded in [`docs/brand-v04-assets.json`](docs/brand-v04-assets.json). To reproduce the web derivatives, extract the approved v04 ZIP and run `python scripts/prepare-brand-v04.py PATH_TO_EXTRACTED_V04_PACKAGE` with Pillow and the Windows display font available. Original production masters remain in Drive. The logo artwork is not redrawn; only transparent outer canvas, output size and icon backing are adapted for web use.

## Remaining launch work

The separate Tally intake integration, real-device mail/telephone/WhatsApp handoffs, broader accessibility/performance review, public-link/QR audit and the V1 launch cutover remain separate work. This brand integration does not authorize retiring V1 or expanding the Shop from the offering database.


## Website theme variants

ALME Website V2 maintains two visual themes in the same codebase:

- **Light / ALME v04** — production default and current public presentation.
- **Dark / ALME Night Garden** — optional saved variant for future use.

The production default is controlled by `DEFAULT_THEME` in `public/assets/js/theme.js` and intentionally remains `light`.

Preview either maintained theme without changing the public default:

- `?theme=light`
- `?theme=dark`

When an explicit preview is active, the theme parameter follows internal website navigation. There is intentionally no public theme-toggle control at this stage.

The dark theme remains within ALME's v04 identity: deep forest-charcoal surfaces, warm cream text, leaf-green highlights and restrained Maker Gold accents. It is intentionally different from Miguel Francis's personal portfolio dark theme.
