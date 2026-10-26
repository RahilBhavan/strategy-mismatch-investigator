"""Additional viewport, long-content and accessibility-state checks."""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0,str(Path(__file__).resolve().parent))
from engine import HOST, capture, ENGINE, isolated_server, launch, named
ROOT=Path(__file__).resolve().parents[1]
with isolated_server() as URL, sync_playwright() as p:
 browser=launch(p)
 page=browser.new_page(viewport={'width':1120,'height':950})
 page.goto(URL,wait_until='networkidle')
 page.get_by_role('button',name='Compare totals').click()
 page.get_by_role('button',name='Test the status selection').click()
 page.get_by_role('heading',name='The status selection explains the gap.').wait_for()
 values=[]
 for width in [320,390,768,1120,1440]:
  page.set_viewport_size({'width':width,'height':1000});page.evaluate('scrollTo(0,0)')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  values.append({'width':width,'no_overflow':True})
 page.set_viewport_size({'width':390,'height':1000})
 # Each mode is set completely so one capture cannot inherit the previous mode's settings.
 for name,options in [('high-contrast',{'forced_colors':'active','reduced_motion':'no-preference'}),('reduced-motion',{'forced_colors':'none','reduced_motion':'reduce'})]:
  page.emulate_media(**options);capture(page,str(ROOT/'verification'/named(f'r4-{name}-390.png')))
  assert page.evaluate("matchMedia('(forced-colors: active)').matches")==(name=='high-contrast'),name
  if name=='reduced-motion':
   page.locator('.finding').evaluate("e=>{e.classList.remove('result-enter');void e.offsetWidth;e.classList.add('result-enter')}")
   assert page.evaluate('document.getAnimations().length')==0,'animation ran under reduced motion'
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  values.append({'mode':name,'no_overflow':True})
 page.emulate_media(forced_colors='none',reduced_motion='reduce')
 # Stress only the renderer using a separate synthetic source, not saved example edits.
 case=page.request.get(URL+'/api/cases/status').json()['case']
 case['name']='Long values and definitions'
 for report in case['reports']:report['name']='Very long synthetic report reference '+('Context '*12);report['unit']='illustrative units with a deliberately extended label'
 case['records'][0]['amount']='90071992547409.93'
 source=page.request.post(URL+'/api/cases',data=json.dumps(case),headers={'Content-Type':'application/json'}).json()
 page.goto(URL+'/?case='+source['id'],wait_until='networkidle')
 page.get_by_role('button',name='Compare totals').click();page.get_by_role('button',name='Test the status selection').wait_for()
 page.set_viewport_size({'width':320,'height':1000})
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 for detail in page.locator('.evidence>details').all():detail.evaluate('(e)=>e.open=true')
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 # Page width alone misses tables clipped by the worksheet's overflow:hidden.
 clipped=page.evaluate('''()=>{const edge=document.querySelector('.worksheet').getBoundingClientRect().right+.5;return [...document.querySelectorAll('.worksheet table')].filter(t=>!t.closest('.table-scroll')&&t.getBoundingClientRect().right>edge).map(t=>t.className)}''')
 assert not clipped,clipped
 # Totals may wrap only at digit-group commas.
 broken=page.evaluate('''()=>[...document.querySelectorAll('.report-table .amount')].filter(e=>{const r=document.createRange();for(const n of e.childNodes){if(n.nodeType!==3)continue;r.selectNodeContents(n);if(r.getClientRects().length>1)return true}return false}).map(e=>e.textContent)''')
 assert not broken,broken
 capture(page,str(ROOT/'verification'/named('r4-stress-320.png')))
 values.append({'mode':'long reports, units, exact large amounts, open evidence at 320px','no_overflow':True})
 page.goto(URL,wait_until='networkidle')
 page.locator('#scenario').select_option('status');page.get_by_role('button',name='Compare totals').click();page.get_by_role('button',name='Test the status selection').click();page.get_by_role('heading',name='The status selection explains the gap.').wait_for()
 # Collect font sizes; contrast measurements are recorded separately in contrast-measurements.json.
 metrics=page.evaluate('''()=>{const e=document.querySelector('.finding h3');return {point_px:parseFloat(getComputedStyle(e).fontSize),label_sizes:[...document.querySelectorAll('.report-table th,.report-table .subline,.report-table .unit,.report-table caption,.ledger th,.ledger .subline')].map(e=>parseFloat(getComputedStyle(e).fontSize))}}''')
 (ROOT/'verification'/named('layout-checks.json')).write_text(json.dumps({'checks':values,'quantitative_text':metrics,'browser':f'{ENGINE} {browser.version}, {HOST}','limits':f'Headless {ENGINE} on {HOST} with emulated widths and media; not physical Windows, Safari, device or screen-reader proof.'},indent=2)+'\n')
 browser.close()
print(json.dumps(values,indent=2));print(metrics)
