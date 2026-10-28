const {chromium}=require('playwright');
const fs=require('fs');
const assert=require('assert/strict');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const page=await browser.newPage(); const errors=[];page.on('pageerror',e=>errors.push(String(e)));
 const results=[];
 for(const width of [360,540,768,1024,1440]) for(const route of ['/','/solutions/']){
  await page.setViewportSize({width,height:1000});await page.goto('http://127.0.0.1:8873'+route);await page.evaluate(()=>document.fonts.ready);
  const state=await page.evaluate(()=>({overflow:document.documentElement.scrollWidth>innerWidth,cards:document.querySelectorAll('.v3-offering').length,stages:[...document.querySelectorAll('.v3-process h3')].map(e=>e.textContent),images:[...document.images].filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src),nav:[...document.querySelectorAll('.primary-nav a')].every(a=>a.textContent.trim()&&a.querySelector('svg[aria-hidden="true"]'))}));
  assert(!state.overflow,JSON.stringify({width,route,...state}));assert.equal(state.cards,4);assert.deepEqual(state.stages,['Understand','Design','Prototype','Coordinate','Build','Improve']);assert(state.nav);
  await page.locator('img[loading="lazy"]').evaluateAll(imgs=>imgs.forEach(i=>i.loading='eager'));
  await page.waitForFunction(()=>[...document.images].every(i=>i.complete&&i.naturalWidth));
  await page.evaluate(()=>Promise.all([...document.images].map(i=>i.decode())));
  assert.equal(await page.locator('img').evaluateAll(imgs=>imgs.filter(i=>!i.complete||!i.naturalWidth).length),0);
  results.push({width,route,pass:true});
  if(width===1440||width===360){await page.evaluate(()=>scrollTo(0,0));await page.screenshot({path:`prototypes/v3/${route==='/'?'home':'solutions'}-${width}.png`,fullPage:true});}
 }
 await page.goto('http://127.0.0.1:8873');await page.keyboard.press('Tab');assert.equal(await page.locator(':focus').textContent(),'Skip to content');
 const focus=await page.locator(':focus').evaluate(e=>({style:getComputedStyle(e).outlineStyle,width:getComputedStyle(e).outlineWidth}));assert.equal(focus.style,'solid');
 await page.emulateMedia({reducedMotion:'reduce'});assert.equal(await page.evaluate(()=>getComputedStyle(document.documentElement).scrollBehavior),'auto');
 const nojs=await browser.newContext({javaScriptEnabled:false,viewport:{width:360,height:900}});const p=await nojs.newPage();await p.goto('http://127.0.0.1:8873');assert(await p.locator('.primary-nav').isVisible());
 for(const name of fs.readdirSync('public/assets/brand'))assert(fs.readFileSync('public/assets/brand/'+name).equals(fs.readFileSync('prototypes/v3/public/assets/brand/'+name)),name);
 assert.equal(errors.length,0);fs.writeFileSync('prototypes/v3/verification.json',JSON.stringify({results,keyboardFocus:focus,reducedMotion:'pass',noJavaScriptNavigation:'pass',brandAssets:'byte-identical',pageErrors:errors},null,2));
 console.log('V3: 10 responsive layouts, loaded images, labelled icons, six ordered stages, keyboard focus, reduced motion, no-JS navigation, unchanged brand assets PASS');await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
