"""Keyboard-only activation of the primary and failure paths in Firefox."""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0,str(Path(__file__).resolve().parent))
from engine import HOST, ENGINE, TAB, isolated_server, launch, named
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
trace=[]
with isolated_server() as URL, sync_playwright() as p:
 b=launch(p)
 page=b.new_page(viewport={'width':390,'height':1000},accept_downloads=True,reduced_motion='reduce')
 # Block external dependencies before the first navigation, not just on a saved-result reload.
 external=[]
 page.on('request',lambda r:external.append(r.url) if not r.url.startswith(URL) else None)
 page.route('**/*',lambda r:r.continue_() if r.request.url.startswith(URL) else r.abort())
 def focus():return page.evaluate('({tag:document.activeElement.tagName,id:document.activeElement.id,text:document.activeElement.textContent.trim().slice(0,80),outline:getComputedStyle(document.activeElement).outlineStyle})')
 def tab_to(test,reverse=False):
  for _ in range(65):
   page.keyboard.press('Shift+'+TAB if reverse else TAB);page.wait_for_timeout(65)
   value=focus();trace.append(value)
   if test(value):
    assert value['outline']=='solid',value
    return value
  raise AssertionError('Could not reach target by keyboard: '+str(trace[-10:]))
 def by_id(name):return lambda f:f['id']==name
 def summary(text):return lambda f:f['tag']=='SUMMARY' and text in f['text']
 page.goto(URL,wait_until='networkidle')
 tab_to(by_id('compare'));page.keyboard.press('Enter')
 page.get_by_role('button',name='Test the status selection').wait_for()
 assert focus()['id']=='worksheet-title',focus()
 tab_to(by_id('diagnose'));page.keyboard.press('Enter')
 page.get_by_role('heading',name='The status selection explains the gap.').wait_for()
 # The answer must receive focus and sit inside the viewport, below the sticky banner.
 landing=page.evaluate("(()=>{const e=document.activeElement,r=e.getBoundingClientRect(),banner=document.querySelector('.simulation').getBoundingClientRect().bottom;return {id:e.id,top:r.top,bottom:r.bottom,banner,height:innerHeight}})()")
 assert landing['id']=='finding-title' and landing['top']>=landing['banner'] and landing['bottom']<=landing['height'],landing
 # On a phone the reconciliation must start on screen, not below the fold.
 assert page.evaluate("document.querySelector('.ledger').getBoundingClientRect().top<innerHeight"),'ledger below the fold'
 tab_to(summary('Inspect report context'));page.keyboard.press('Space')
 assert page.locator('.evidence>details').first.evaluate('(e)=>e.open')
 tab_to(summary('Inspect execution evidence'));page.keyboard.press('Enter')
 assert page.locator('.evidence>details').nth(1).evaluate('(e)=>e.open')
 # The export buttons sit in the evidence heading, before the sections just opened.
 tab_to(by_id('export-json'),reverse=True)
 with page.expect_download() as info:page.keyboard.press('Enter')
 path=ROOT/'verification'/named('keyboard-export.json');info.value.save_as(path)
 packet=json.loads(path.read_text());assert packet['payload']['result']['residual']=='0.00'
 tab_to(by_id('export-report'))
 with page.expect_download() as info:page.keyboard.press('Enter')
 info.value.save_as(ROOT/'verification'/named('keyboard-report.html'))
 assert not external,external
 # Expanded setup controls and transient cancellation remain keyboard-operable.
 page.goto(URL,wait_until='networkidle')
 tab_to(summary('Source & test controls'));page.keyboard.press('Space')
 tab_to(by_id('amount'));page.keyboard.press('ControlOrMeta+A');page.keyboard.type('25.00')
 tab_to(by_id('save-amount'));page.keyboard.press('Enter')
 page.get_by_text('Report context changed. Capture a new comparison.',exact=True).wait_for()
 # Type-ahead picks an option in every engine; Safari on macOS ignores Home/End on a closed menu.
 tab_to(by_id('condition'));page.keyboard.type('Slow')
 assert page.locator('#condition').input_value()=='slow'
 tab_to(by_id('compare'),reverse=True);page.keyboard.press('Enter')
 tab_to(by_id('cancel'));page.keyboard.press('Enter')
 page.get_by_text('Investigation canceled. No conclusion was produced.',exact=True).wait_for()
 # Denial and Retry are invoked without pointer actions too.
 # WebKit keeps a type-ahead buffer for about a second; start a fresh search.
 tab_to(by_id('condition'));page.wait_for_timeout(1200);page.keyboard.type('Evidence')
 assert page.locator('#condition').input_value()=='denied',page.locator('#condition').input_value()
 tab_to(by_id('compare'),reverse=True);page.keyboard.press('Enter')
 page.get_by_text('Required report evidence is unavailable.',exact=True).wait_for()
 tab_to(by_id('retry'));page.keyboard.press('Enter')
 page.get_by_text('Required report evidence is unavailable.',exact=True).wait_for()
 assert page.locator('.report-table').count()==0
 b.close()
(ROOT/'verification'/named('keyboard-checks.json')).write_text(json.dumps({'browser':f'{ENGINE} {b.version}, {HOST}','post_result_focus':landing,'viewport':390,'result':'pass','pointer_actions':0,'external_requests':external,'paths':['compare → diagnostic → open context/execution → JSON and readable export','expanded amount edit → slow run → cancel','denied evidence → retry without partial result'],'focus_trace':trace},indent=2)+'\n')
print('Keyboard-only complete workflow, setup edit, cancellation, denial/retry and fresh external-blocked execution: PASS')
