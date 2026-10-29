const {chromium}=require('playwright');
const fs=require('fs');const assert=require('assert/strict');
const base=process.env.BASE_URL || 'http://127.0.0.1:8874';
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const routes=process.env.V3_ROUTES?.split(',') || ['/','/solutions/','/shop/','/work/','/about/','/community/','/research/','/start-a-project/'];
 const results=[],errors=[];
 for(const theme of ['light','dark']) for(const width of [320,768,1440]) for(const route of routes){
  const page=await browser.newPage({viewport:{width,height:1000}});page.on('pageerror',e=>errors.push(String(e)));
  console.log(theme,width,route);
  await page.goto(base+route+'?theme='+theme);
  await page.locator('img').evaluateAll(imgs=>imgs.forEach(i=>i.loading='eager'));
  await page.waitForLoadState('networkidle');
  await page.locator('img').evaluateAll(imgs=>Promise.all(imgs.map(i=>i.decode())));
  assert(await page.locator('img').evaluateAll(imgs=>imgs.every(i=>i.complete&&i.naturalWidth)),route);
  assert(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),`${route} ${width}`);
  assert.equal(await page.locator('.primary-nav a').count(),8);
  assert.equal(await page.locator('.primary-nav a[aria-current="page"]').count(),1);
  assert.equal(await page.locator('.primary-nav a[aria-current="page"]').getAttribute('href'),base+route+'?theme='+theme);
  if(['/','/solutions/','/about/'].includes(route)){
   assert.equal(await page.locator('.v3-process .v3-node img').count(),6);
   assert.equal(await page.locator('.v3-process svg').count(),0);
  }
  if(width===320){
   await page.locator('.menu-toggle').click();assert(await page.locator('.primary-nav').isVisible());
   await page.keyboard.press('Escape');assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'),'false');
   assert(await page.locator('.menu-toggle').evaluate(e=>e===document.activeElement));
  }
  await page.addScriptTag({path:'C:/Users/migue/.codex/tmp/alme-v3-qa/node_modules/axe-core/axe.min.js'});
  const audit=await page.evaluate(()=>axe.run({runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa','best-practice']}}));
  const violations=audit.violations.map(v=>({id:v.id,nodes:v.nodes.map(n=>n.target)}));
  results.push({route,theme,width,violations});
  if(violations.length)console.log(JSON.stringify(results.at(-1)));
  if(theme==='light'&&[320,1440].includes(width))await page.screenshot({path:`docs/v3-extension/${route==='/'?'home':route.split('/')[1]}-${width}.png`,fullPage:true});
  await page.close();
 }
 const context=await browser.newContext({javaScriptEnabled:false,viewport:{width:320,height:900}});
 for(const route of routes){const p=await context.newPage();await p.goto(base+route);assert(await p.locator('.primary-nav').isVisible());await p.close();}
 fs.writeFileSync(process.env.V3_REPORT || 'docs/v3-extension/verification.json',JSON.stringify({results,pageErrors:errors,noJavaScriptRoutes:routes},null,2));
 await browser.close();assert.equal(errors.length,0);assert(results.every(r=>!r.violations.length));
 console.log(`PASS: ${results.length} layouts/axe audits, ${routes.length} no-JS routes, current navigation, exact process assets, loaded images, mobile Escape focus, zero page errors`);
})().catch(e=>{console.error(e);process.exit(1)});
