const { chromium } = require('playwright');
const fs = require('node:fs');
const base = process.env.BASE_URL || 'http://127.0.0.1:8765';
(async () => {
  const browser = await chromium.launch({headless: true, channel: process.env.BROWSER_CHANNEL || 'msedge'});
  const results = [];
  for (const width of [360, 768, 1280]) {
    const page = await browser.newPage({viewport: {width, height: 900}});
    const errors = [];
    page.on('pageerror', e => errors.push(String(e)));
    await page.goto(base + '/start-a-project/?service=Maker%20Project%20Consultation');
    const frame = page.frameLocator('iframe[data-tally-src]');
    await frame.locator('[id="12776d11-1721-4906-b818-7284af3f442f"]').waitFor();
    await page.waitForFunction(() => document.querySelector('iframe').getBoundingClientRect().height > 1000);
    const layout = await page.evaluate(() => ({
      overflow: document.documentElement.scrollWidth > innerWidth,
      height: document.querySelector('iframe').getBoundingClientRect().height,
      frameWidth: document.querySelector('iframe').getBoundingClientRect().width
    }));
    if (layout.overflow || layout.frameWidth > width) throw Error('Embed overflow at ' + width);
    if (!await frame.getByRole('combobox').first().evaluate(el => (el.value || el.textContent).includes('Maker Project Consultation'))) throw Error('Service prefill failed');
    if (!await frame.getByRole('button', {name: 'Submit', exact: true}).isVisible()) throw Error('Missing submit');
    for (const href of ['mailto:', 'https://wa.me/']) {
      if (!await page.locator('#project-intake a[href^="' + href + '"]').isVisible()) throw Error('Missing fallback');
    }
    if (errors.length) throw Error(errors.join('\n'));
    if (width === 360 || width === 1280) {
      fs.mkdirSync('docs/intake', {recursive: true});
      await page.evaluate(() => window.scrollTo({top: document.querySelector('#intake-heading').getBoundingClientRect().top + scrollY - 120, behavior: 'instant'}));
      await frame.getByRole('heading', {name: 'Your name', exact: true}).waitFor({state: 'visible'});
      // Give the browser a painted frame after scrolling the embedded document.
      await page.evaluate(() => new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve))));
      await page.screenshot({path: 'docs/intake/start-a-project-' + width + '.png'});
    }
    results.push({width, ...layout, prefill: 'pass', fallbacks: 'pass', pageErrors: errors});
    await page.close();
  }
  const nojs = await browser.newPage({javaScriptEnabled: false, viewport: {width: 360, height: 900}});
  await nojs.goto(base + '/start-a-project/');
  if (!await nojs.locator('#intake-direct-link').isVisible()) throw Error('No-JS direct form link missing');
  if (!await nojs.locator('#project-intake a[href^="mailto:"]').isVisible()) throw Error('No-JS email missing');
  const report = {base, responsive: results, noJavaScript: 'direct form and email available'};
  fs.writeFileSync('docs/intake/verification.json', JSON.stringify(report, null, 2) + '\n');
  console.log(JSON.stringify(report));
  await browser.close();
})().catch(e => {console.error(e); process.exit(1);});
