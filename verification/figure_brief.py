import json
from pathlib import Path
from playwright.sync_api import sync_playwright
root=Path(__file__).resolve().parents[1]
def luminance(rgb):
 vals=[x/255 for x in rgb]
 vals=[x/12.92 if x<=.04045 else ((x+.055)/1.055)**2.4 for x in vals]
 return .2126*vals[0]+.7152*vals[1]+.0722*vals[2]
with sync_playwright() as p:
 b=p.firefox.launch(executable_path='/home/rahil/.cache/ms-playwright/firefox-1555/firefox/firefox',headless=True)
 page=b.new_page(viewport={'width':390,'height':1000})
 page.goto('http://127.0.0.1:8807',wait_until='networkidle');page.get_by_role('button',name='Compare totals').click();page.get_by_role('button',name='Test the status selection').click();page.get_by_role('heading',name='The status selection explains the gap.').wait_for()
 data=page.evaluate('''()=>[...document.querySelectorAll('.report-table th,.report-table .unit,.report-table .subline,.report-table caption,.ledger th,.ledger .subline,.finding h3')].map(e=>{let p=e,bg;while(p){bg=getComputedStyle(p).backgroundColor;if(!bg.endsWith(', 0)')&&bg!=='transparent')break;p=p.parentElement}return {size:parseFloat(getComputedStyle(e).fontSize),fg:getComputedStyle(e).color,bg:bg||'rgb(255,255,255)'}})''')
 b.close()
import re
ratios=[]
for row in data:
 fg=list(map(float,re.findall(r'[\d.]+',row['fg'])))[:3];bg=list(map(float,re.findall(r'[\d.]+',row['bg'])))[:3]
 a,b=sorted([luminance(fg),luminance(bg)])
 ratios.append((b+.05)/(a+.05))
brief=dict(id='status-reconciliation',reader='Analyst reviewing whether one status selection explains a numerical gap',decision='Inspect the evidence before choosing the intended business definition',point='Changing only the status selection changes B from 180 to 220, leaving 0 residual.',comparison='Original report B versus B rerun with report A status selection',title='The status selection explains the gap.',caption='Illustrative values, computed from synthetic orders.',form='table',values_count=6,encodings=[],accents=1,accent_meaning='title-value',estimates={'present':False},illustration=True,illustration_labeled=True,sources=[{'title':'Locally authored synthetic record fixture','url':'../app/fixtures.py','as_of':'2026-10-24'}],alt='Synthetic A is 220 and B is 180. Rerunning B with all statuses returns 220; measured impact 40 and residual 0. This does not decide business correctness.',sizes_checked=['390x1000','1440x1000'],feed_width_viewed=True,min_label_px=min(r['size'] for r in data),point_px=19,contrast_min=round(min(ratios),2),measured_by='Firefox computed styles and WCAG luminance calculation; quantitative labels only',warn_reasons={'title shares no number':'The adjacent comparison carries the actual values; the interactive heading states the demonstrated mechanism.','smallest label renders':'14px app labels viewed at actual 390px width; this is a working UI rather than a social raster.','the point renders':'19px finding heading in a dense analyst interface; visible at actual browser width.','no five-second test recorded':'Independent agent critique completed; no human timed comprehension test was run.'})
(root/'verification/figure-brief.json').write_text(json.dumps(brief,indent=2)+'\n')
(root/'verification/contrast-measurements.json').write_text(json.dumps({'elements':data,'ratios':ratios},indent=2)+'\n')
print('quantitative label contrast minimum:',brief['contrast_min'])
