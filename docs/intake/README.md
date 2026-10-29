# Commercial intake acceptance — 29 October 2026

Existing Tally form: ODWE0p, published at https://tally.so/r/ODWE0p.
The earlier handoff URL `stA2Wx` returned a not-found page. No duplicate form was created.
The existing native Notion connection was already active; its mapping editor showed 23 approved target properties. No credentials or permissions were changed by this release.

Destination: ALME Inbound Inquiries, data source `f9c5fc00-596f-4a76-b85f-ae179265e8a0`.

| Case | Observed outcome | Notion record |
| --- | --- | --- |
| A commercial + attachment | Custom Build / Furniture, Business / Commercial, Kingston; synthetic text file present; Source Website / Form; Review Status New; consent true; coursework false | `408adf602d0d811db2bed33277248082` |
| B editable prefill | `?service=Maker%20Project%20Consultation` preselected consultation; changed to General / Other and that changed value arrived in Notion | `408adf602d0d81c9b480f86e6d3f2715` |
| C coursework | Student / School; Yes revealed academic-integrity notice and teacher-contact field; synthetic teacher contact arrived; coursework true | `408adf602d0d815b8f64f73370671358` |
| D international remote | Toronto, Canada; Remote Design & Production Support; Remote; no Jamaica-only requirement | `408adf602d0d8152b9b0f1e14879b90f` |
| E minimal | Required fields and consent only; accepted; optional values blank; coursework false | `408adf602d0d8108b608f98c2f6153a2` |
| F no consent | Submission blocked; required checkbox highlighted with Please select an option | No record created |

All five submitted cases reached the approved confirmation copy. All five records had Source Website / Form, Review Status New, Consent to Contact true and no Converted Prospect or Next Action. The coursework checkbox was false except in C.

The five new synthetic records and the older disposable E-minimal record were moved to the established To Be Deleted — Review Queue (`3e2adf602d0d81e4b071c447334ca69c`), rather than deleted. The earlier Brainy Quick Capture test was also staged there. The historical TEST COMPLETE routing record was left intact; it was already Declined and documented as retained system evidence.

The attachment upload initially required the user to enable the Chrome extension's file-URL permission. Upload succeeded after the user enabled it. Notion SQL/rows query allowance was exhausted; saved-view queries and direct page fetches supplied the destination evidence.

The page uses Tally's standard embed widget for dynamic height, a direct-form link for unavailable JavaScript, and visible email/WhatsApp alternatives. Service query prefill is forwarded to the form and direct-form alternative. Community intake and bounded property-care contact actions remain separate.

Validation: `scripts/verify-intake.cjs` checks the live Tally embed at 360, 768 and 1280 px, dynamic resizing, editable service prefill, fallbacks, no-JavaScript access and browser errors. `scripts/verify-commercial-alignment.cjs` checks the surrounding site. No acceptance test includes customer data.

## Production verification

- Implementation commit: `3e11437edfb4984311d599b7173008f1377ea466`, pushed to `main`.
- Cloudflare Pages check completed successfully; deployment `341b637c-31da-437f-84c4-1e0199699124`.
- Live URL: https://alme-website.pages.dev/start-a-project/.
- Production embed checks passed at 360, 768 and 1280 px, with dynamic heights 3416.5, 3020.5 and 3054 px; no horizontal overflow or page errors; service prefill and email/WhatsApp fallbacks present. JavaScript-disabled direct-form/email access passed.
- Production surrounding-site checks: 27 layouts, 172 internal links, offering headings, property-care contact context, mobile menu and JavaScript-disabled navigation passed; zero page errors.
- The deployed intake HTML and `assets/js/intake.js` returned HTTP 200 and matched local source after newline normalization.
- Live embedded submission `TEST — ALME Tally production embed — 2026-10-29` arrived at 2026-10-29T16:12:38.282Z (11:12:38 AM Jamaica) in record `408adf602d0d816abe69ff3125b88e07`: Maker Project Consultation, Website / Form, New, consent true, coursework false, no automatic prospect or next action. The live embed showed the approved confirmation.
- The production test was then moved to the existing review queue. A destination readback showed no new synthetic tests left in the inbound database; only the pre-existing Declined historical routing evidence remains.
