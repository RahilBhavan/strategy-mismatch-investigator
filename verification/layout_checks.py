"""Additional viewport, long-content and accessibility-state checks."""
import json
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 browser=p.firefox.launch(executable_path='/home/rahil/.cache/ms-playwright/firefox-1555/firefox/firefox',headless=True)
 page=browser.new_page(viewport={'width':1120,'height':950})
 page.goto('http://127.0.0.1:8807',wait_until='networkidle')
 page.get_by_role('button',name='Compare totals').click()
 page.get_by_role('button',name='Test the status selection').click()
 page.get_by_role('heading',name='The status selection explains the gap.').wait_for()
 values=[]
 for width in [320,390,768,1120,1440]:
  page.set_viewport_size({'width':width,'height':1000});page.evaluate('scrollTo(0,0)')
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  values.append({'width':width,'no_overflow':True})
 page.set_viewport_size({'width':390,'height':1000})
 for name,options in [('high-contrast',{'forced_colors':'active'}),('reduced-motion',{'reduced_motion':'reduce'})]:
  page.emulate_media(**options);page.screenshot(path=str(ROOT/'verification'/f'{name}-390.png'),full_page=True)
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  values.append({'mode':name,'no_overflow':True})
 page.emulate_media(forced_colors='none',reduced_motion='reduce')
 # Stress only the renderer using a separate synthetic source, not saved example edits.
 case=page.request.get('http://127.0.0.1:8807/api/cases/status').json()['case']
 case['name']='Long values and definitions'
 for report in case['reports']:report['name']='Very long synthetic report reference '+('Context '*12);report['unit']='illustrative units with a deliberately extended label'
 case['records'][0]['amount']='90071992547409.93'
 source=page.request.post('http://127.0.0.1:8807/api/cases',data=json.dumps(case),headers={'Content-Type':'application/json'}).json()
 page.goto('http://127.0.0.1:8807/?case='+source['id'],wait_until='networkidle')
 page.get_by_role('button',name='Compare totals').click();page.get_by_role('button',name='Test the status selection').wait_for()
 page.set_viewport_size({'width':320,'height':1000})
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 for detail in page.locator('.evidence>details').all():detail.evaluate('(e)=>e.open=true')
 assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
 page.screenshot(path=str(ROOT/'verification'/'stress-320.png'),full_page=True)
 values.append({'mode':'long reports, units, exact large amounts, open evidence at 320px','no_overflow':True})
 page.goto('http://127.0.0.1:8807',wait_until='networkidle')
 page.locator('#scenario').select_option('status');page.get_by_role('button',name='Compare totals').click();page.get_by_role('button',name='Test the status selection').click();page.get_by_role('heading',name='The status selection explains the gap.').wait_for()
 # Collect font sizes; contrast measurements are recorded separately in contrast-measurements.json.
 metrics=page.evaluate('''()=>{const e=document.querySelector('.finding h3');return {point_px:parseFloat(getComputedStyle(e).fontSize),label_sizes:[...document.querySelectorAll('.report-table th,.report-table .subline,.report-table .unit,.report-table caption,.experiment-values dt')].map(e=>parseFloat(getComputedStyle(e).fontSize))}}''')
 (ROOT/'verification'/'layout-checks.json').write_text(json.dumps({'checks':values,'quantitative_text':metrics,'limits':'Linux Firefox emulations; not physical Windows, Safari, device or screen-reader proof.'},indent=2)+'\n')
 browser.close()
print(json.dumps(values,indent=2));print(metrics)
