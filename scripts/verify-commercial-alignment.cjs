const base = process.env.BASE_URL || 'http://127.0.0.1:8765';
const { chromium } = require('playwright');
(async()=>{
 const browser=await chromium.launch({headless:true,channel:process.env.BROWSER_CHANNEL || 'msedge'});
 const page=await browser.newPage(); const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 const routes=['/','/solutions/','/start-a-project/','/shop/','/work/','/about/','/community/','/research/','/404.html'];
 let links=0,layouts=0;
 for(const width of [360,768,1280]) for(const route of routes){
  await page.setViewportSize({width,height:900});await page.goto(base+route);
  const result=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,h1:document.querySelectorAll('h1').length}));
  if(result.overflow||result.h1!==1)throw Error(JSON.stringify({route,width,...result}));layouts++;
  if(width===360 && await page.locator('.menu-toggle').count()){await page.locator('.menu-toggle').click();if(await page.locator('.menu-toggle').getAttribute('aria-expanded')!=='true')throw Error('menu');await page.keyboard.press('Escape');}
  if(width===1280){const hrefs=await page.locator('a[href^="/"]').evaluateAll(els=>els.map(e=>e.getAttribute('href')));for(const href of hrefs){const u=new URL(href,base);const response=await page.request.get(u.href);if(response.status()!==200)throw Error('Broken link '+href);if(u.hash){const html=await response.text();if(!html.includes('id="'+u.hash.slice(1)+'"'))throw Error('Broken fragment '+href);}links++;}}
 }
 await page.goto(base+'/solutions/');
 const expected=['Product Design & Development','Infrastructure Design & Build','Project Coordination, Property Care & Systems Support','ALME Products & Equipment'];
 const headings=await page.locator('.container.grid > article > h2').allTextContents();if(JSON.stringify(headings)!==JSON.stringify(expected))throw Error('offerings');
 await page.locator('a[href="/start-a-project/#property-care"]').click();
 for(const selector of ['a[href^="mailto:"]','a[href^="https://wa.me/"]']){const href=await page.locator('#property-care').locator(selector).getAttribute('href');if(!decodeURIComponent(href).includes('Property Care & Operational Oversight'))throw Error('service context');}
 const off=await browser.newContext({javaScriptEnabled:false,viewport:{width:360,height:900}});const nojs=await off.newPage();await nojs.goto(base+'/start-a-project/#property-care');if(!await nojs.locator('#property-care a').first().isVisible())throw Error('nojs contact');if(!await nojs.locator('.primary-nav').isVisible())throw Error('nojs nav');
 if(errors.length)throw Error(errors.join('\n'));
 console.log(JSON.stringify({layouts,internalLinksChecked:links,offerings:'pass',propertyCareContactContext:'pass',mobileMenu:'pass',noJavaScript:'pass',pageErrors:errors}));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
