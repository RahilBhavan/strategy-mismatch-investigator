from playwright.sync_api import sync_playwright
from pathlib import Path
import json
root=Path(__file__).resolve().parents[1]
with sync_playwright() as p:
 b=p.firefox.launch(executable_path='/home/rahil/.cache/ms-playwright/firefox-1555/firefox/firefox',headless=True)
 page=b.new_page(viewport={'width':1440,'height':1000},reduced_motion='reduce')
 page.goto('http://127.0.0.1:8807',wait_until='networkidle');page.get_by_role('button',name='Compare totals').click();page.get_by_role('button',name='Test the status selection').click();page.get_by_role('heading',name='The status selection explains the gap.').wait_for()
 for w in (1440,390):
  page.set_viewport_size({'width':w,'height':1000});page.evaluate('scrollTo(0,0)');page.screenshot(path=str(root/'verification'/f'r3-demonstrated-{w}.png'),full_page=True)
  for d in page.locator('.evidence>details').all():d.evaluate('(e)=>e.open=true')
  page.screenshot(path=str(root/'verification'/f'r3-evidence-{w}.png'),full_page=True)
  for d in page.locator('.evidence>details').all():d.evaluate('(e)=>e.open=false')
 page.locator('#scenario').select_option('ambiguous');page.get_by_role('button',name='Compare totals').click();page.get_by_role('heading',name='The evidence does not isolate a cause.').wait_for()
 for w in (1440,390):
  page.set_viewport_size({'width':w,'height':1000});page.evaluate('scrollTo(0,0)');page.screenshot(path=str(root/'verification'/f'r3-ambiguous-{w}.png'),full_page=True)
 page.set_viewport_size({'width':390,'height':1000})
 page.emulate_media(forced_colors='active')
 page.goto('http://127.0.0.1:8807',wait_until='networkidle')
 page.keyboard.press('Tab')
 media=page.evaluate("({width:innerWidth,focus:getComputedStyle(document.activeElement).outlineStyle,buttonBackground:getComputedStyle(document.querySelector('#compare')).backgroundColor,buttonColor:getComputedStyle(document.querySelector('#compare')).color,buttonBorder:getComputedStyle(document.querySelector('#compare')).borderStyle})")
 assert media['width']==390 and media['focus']=='solid' and media['buttonBorder']=='solid',media
 page.screenshot(path=str(root/'verification'/'r3-forced-colors-390.png'),full_page=True)
 page.emulate_media(forced_colors='none',reduced_motion='reduce')
 page.get_by_role('button',name='Compare totals').click();page.get_by_role('button',name='Test the status selection').click();page.get_by_role('heading',name='The status selection explains the gap.').wait_for()
 reduced=page.locator('.finding').evaluate('(e)=>({animation:getComputedStyle(e).animationName,opacity:getComputedStyle(e).opacity})')
 assert reduced['animation']=='none' and reduced['opacity']=='1',reduced
 page.screenshot(path=str(root/'verification'/'r3-reduced-motion-390.png'),full_page=True)
 (root/'verification'/'media-checks.json').write_text(json.dumps({'forced_colors':media,'reduced_motion':reduced,'limits':'Linux Firefox media emulation, not a physical device check.'},indent=2)+'\n')
 b.close()
