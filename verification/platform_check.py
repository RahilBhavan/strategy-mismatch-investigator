"""Engine checks are Linux runs; emulations do not prove physical platforms."""
import argparse,json
from pathlib import Path
from playwright.sync_api import sync_playwright
parser=argparse.ArgumentParser();parser.add_argument('engine');args=parser.parse_args()
root=Path(__file__).resolve().parents[1];result={'engine':args.engine,'host':'Linux','live_strategy':'not tested'}
with sync_playwright() as p:
 browser=None
 try:
  if args.engine=='chromium':
   browser=p.chromium.launch(executable_path='/home/rahil/.cache/ms-playwright/chromium_headless_shell-1248/chrome-headless-shell-linux64/chrome-headless-shell',headless=True,timeout=15000,args=['--no-sandbox','--disable-gpu','--disable-dev-shm-usage'])
  else:browser=p.webkit.launch(executable_path='/home/rahil/.cache/ms-playwright/webkit-2370/pw_run.sh',headless=True,timeout=15000)
  page=browser.new_page(viewport={'width':390,'height':1000},reduced_motion='reduce')
  page.set_default_timeout(7000)
  page.goto('http://127.0.0.1:8807',wait_until='domcontentloaded',timeout=10000)
  page.get_by_role('button',name='Compare totals').click()
  page.get_by_role('button',name='Test the status selection').click()
  page.get_by_role('heading',name='The status selection explains the gap.').wait_for()
  assert page.locator('.experiment-values dd').all_text_contents()==['220','40','0']
  assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
  page.evaluate('scrollTo(0,0)');page.screenshot(path=str(root/'verification'/f'{args.engine}-390.png'),full_page=True,timeout=7000)
  result['result']='pass';result['scope']='compare, diagnostic, evidence values and 390px overflow'
 except Exception as error:
  result['result']='unverified';result['error']=str(error)
 finally:
  (root/'verification'/f'{args.engine}-check.json').write_text(json.dumps(result,indent=2)+'\n')
  if browser:browser.close()
print(json.dumps(result,indent=2))
