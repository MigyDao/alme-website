const { chromium } = require('playwright');
const fs = require('fs');
const base=process.env.BASE_URL || 'http://127.0.0.1:8765';
(async()=>{
 const browser=await chromium.launch({headless:true,channel:'msedge'});
 const results=[];
 for(const width of [320,360,768,1280]){
  const page=await browser.newPage({viewport:{width,height:900}});
  await page.goto(base+'/solutions/');
  const cards=page.locator('#consultations article');
  if(await cards.count()!==3)throw Error('Missing consultation');
  for(let i=0;i<3;i++){
   const card=cards.nth(i);const title=await card.locator('h3').innerText();
   await card.locator('a').click();
   const target=page.locator(new URL(page.url()).hash);
   if(!await target.isVisible())throw Error('Missing enquiry context');
   for(const prefix of ['mailto:','https://wa.me/']){
    const href=await target.locator('a[href^="'+prefix+'"]').getAttribute('href');
    if(!decodeURIComponent(href).includes(title))throw Error('Contact context lost');
   }
   if(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth))throw Error('Overflow '+width);
   await target.getByRole('link',{name:'Use the enquiry form',exact:true}).click();
   await page.waitForFunction(()=>document.querySelector('iframe').src.includes('service='));
   const service=new URL(page.url()).searchParams.get('service');
   if(new URL(await page.locator('iframe').getAttribute('src')).searchParams.get('service')!==service)throw Error('Prefill forwarding');
   await page.goto(base+'/solutions/');
  }
  if(width===360||width===1280){await page.locator('#consultations').scrollIntoViewIfNeeded();await page.screenshot({path:'docs/service-pricing-v1/solutions-'+width+'.png'});}
  results.push({width,consultationFlows:3,contacts:'service context retained',overflow:false});
  await page.close();
 }
 const page=await browser.newPage();
 const actualPrefills=[];let retired=false;
 for(const service of ['Maker Project Consultation','Organization / Spatial Systems','Growing / Land']){
  await page.goto('https://tally.so/r/ODWE0p?service='+encodeURIComponent(service),{waitUntil:'domcontentloaded'});
  const combo=page.getByRole('combobox').first();await combo.waitFor();
  const value=await combo.inputValue();if(value!==service)throw Error('Actual form prefill '+service);
  actualPrefills.push(value);
  await combo.click();
  retired=retired||(await page.getByRole('option').allTextContents()).some(t=>t.includes('Remote Design & Production Support'));
 }
 if(retired)throw Error('Discontinued service remains public');
 const nojs=await browser.newPage({javaScriptEnabled:false,viewport:{width:360,height:900}});await nojs.goto(base+'/start-a-project/#garden-planning');
 if(!await nojs.locator('#garden-planning a[href^="mailto:"]').isVisible())throw Error('NoJS contact');
 const report={verifiedAt:new Date().toISOString(),base,responsive:results,actualFormPrefills:actualPrefills,noJavaScript:'consultation email links available',discontinuedOfferingVisibleInForm:retired,submissionsSent:0};
 fs.writeFileSync('docs/service-pricing-v1/verification.json',JSON.stringify(report,null,2)+'\n');console.log(JSON.stringify(report));await browser.close();
})().catch(e=>{console.error(e);process.exit(1)});
