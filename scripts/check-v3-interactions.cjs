const {chromium}=require('playwright');
const assert=require('assert/strict');
const fs=require('fs');
const cp=require('child_process');
(async()=>{
 const browser=await chromium.launch({channel:'msedge',headless:true});
 const results=[];
 for(const theme of ['light','dark']) for(const route of ['/','/solutions/']){
  const page=await browser.newPage({viewport:{width:1280,height:900}});
  await page.goto('http://127.0.0.1:8874'+route+'?theme='+theme);
  assert.equal(await page.locator('meta[name="robots"]').count(),0);
  for(let i=0;i<60;i++){
   await page.keyboard.press('Tab'); await page.waitForTimeout(350);
   const state=await page.locator(':focus').evaluate(e=>{
    const r=e.getBoundingClientRect(),h=document.querySelector('.site-header').getBoundingClientRect();
    return {tag:e.tagName,style:getComputedStyle(e).outlineStyle,width:parseFloat(getComputedStyle(e).outlineWidth),visible:r.bottom>0&&r.top<innerHeight,obscured:!e.closest('.site-header')&&!e.matches('.skip-link')&&r.top<h.bottom-1};
   });
   assert(state.visible&&!state.obscured,JSON.stringify({route,theme,i,state}));
   assert(state.style!=='none'&&state.width>=2,JSON.stringify(state));
   if(await page.locator(':focus').evaluate(e=>e.closest('.site-footer')!==null))break;
  }
  await page.setViewportSize({width:320,height:700});
  await page.locator('.menu-toggle').click();
  assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'),'true');
  await page.locator('.primary-nav a').last().focus();
  await page.keyboard.press('Escape');assert(await page.locator('.menu-toggle').evaluate(e=>e===document.activeElement));
  assert.equal(await page.locator('.menu-toggle').getAttribute('aria-expanded'),'false');
  for(const e of await page.locator('.v3-offering>.button').all()){
   const r=await e.boundingBox();assert(r.width>=44&&r.height>=44);
  }
  await page.emulateMedia({reducedMotion:'reduce'});
  assert.equal(await page.locator('.v3-offering').first().evaluate(e=>getComputedStyle(e).transitionDuration),'0s');
  assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth),true);
  await page.addScriptTag({path:'C:/Users/migue/.codex/tmp/alme-v3-qa/node_modules/axe-core/axe.min.js'});
  const axe=await page.evaluate(()=>axe.run({runOnly:{type:'tag',values:['wcag2a','wcag2aa','wcag21aa','wcag22aa','best-practice']}}));
  assert.equal(axe.violations.length,0,JSON.stringify(axe.violations));
  results.push({route,theme,keyboardFocus:'pass',escapeFocusReturn:'pass',touchTargets:'pass',reducedMotion:'pass',reflow320:'pass',axeViolations:0});
  await page.close();
 }
 // Every pre-existing public file other than the two approved pages stays identical.
 const files=cp.execFileSync('git',['ls-tree','-r','--name-only','4bb49cc','public'],{encoding:'utf8'}).trim().split('\n');
 for(const file of files.filter(f=>!['public/index.html','public/solutions/index.html'].includes(f))){
  const actual=fs.readFileSync(file),expected=cp.execFileSync('git',['show','4bb49cc:'+file]); assert(/\.(html|css|js|svg|txt|xml|webmanifest)$/.test(file)?actual.toString().replace(/\r\n/g,'\n')===expected.toString().replace(/\r\n/g,'\n'):actual.equals(expected),file);
 }
 fs.writeFileSync('docs/v3-implementation/interactions.json',JSON.stringify({results,unchangedBaselineFiles:files.length-2},null,2));
 console.log(JSON.stringify({results,unchangedBaselineFiles:files.length-2}));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});

