"""Real Firefox verification against an isolated HTTP server and disposable DB."""
import json
import sys
import tempfile
import threading
from pathlib import Path
from http.server import ThreadingHTTPServer
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from app.server import handler
from app.store import Store
from app.fixtures import example
from playwright.sync_api import sync_playwright
sys.path.insert(0,str(Path(__file__).resolve().parent))
from engine import HOST, capture, ENGINE, TAB, launch, named

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'verification'
receipts=[]


def server(store,port=0):
    http=ThreadingHTTPServer(('127.0.0.1',port),handler(store))
    thread=threading.Thread(target=http.serve_forever,daemon=True);thread.start()
    return http,thread


def stop(http,thread):
    http.shutdown();http.server_close();thread.join()


with tempfile.TemporaryDirectory() as tmp:
    db=Path(tmp)/'browser.sqlite3'
    store=Store(db);http,thread=server(store);port=http.server_port
    url=f'http://127.0.0.1:{port}'
    with sync_playwright() as p:
        browser=launch(p)
        page=browser.new_page(viewport={'width':1440,'height':1100},reduced_motion='reduce',accept_downloads=True)
        errors=[];page.on('pageerror',lambda error:errors.append(str(error)))
        page.goto(url,wait_until='networkidle')
        page.get_by_role('button',name='Compare totals').click()
        page.get_by_role('button',name='Test the status selection').wait_for()
        assert page.locator('.report-table .amount').all_text_contents()==['220','180']
        capture(page,str(OUT/named('r4-candidate-1440.png')))
        page.get_by_role('button',name='Test the status selection').click()
        page.get_by_role('heading',name='The status selection explains the gap.').wait_for()
        assert page.locator('.ledger .num').all_text_contents()==['180','+40','220','220','0']
        capture(page,str(OUT/named('r4-demonstrated-1440.png')))
        with page.expect_download() as info:page.get_by_role('button',name='Export evidence JSON').click()
        packet_path=OUT/named('browser-export.json');info.value.save_as(packet_path)
        with page.expect_download() as info:page.get_by_role('button',name='Save readable report').click()
        report_path=OUT/named('browser-report.html');info.value.save_as(report_path)
        remembered=page.url
        stop(http,thread);store=Store(db);http,thread=server(store,port)
        page.goto(remembered,wait_until='networkidle')
        page.get_by_role('heading',name='The status selection explains the gap.').wait_for()
        page.locator('.reopen').evaluate('(e)=>e.open=true')
        page.locator('#packet-file').set_input_files(str(packet_path))
        page.get_by_text('Packet arithmetic recomputed locally; original instance IDs are historical only.').wait_for()
        receipts.append({'check':'compute, experiment, JSON/HTML export, full HTTP-server restart, packet reopen','result':'pass'})
        page.locator('.tools summary').click()
        page.locator('#amount').fill('15.00')
        page.get_by_role('button',name='Update synthetic source').click()
        page.get_by_text('Report context changed. Capture a new comparison.').wait_for()
        assert page.locator('.report-table').count()==0
        page.get_by_role('button',name='Compare totals').click()
        page.get_by_role('button',name='Test the status selection').click()
        page.get_by_role('heading',name='The status selection explains the gap.').wait_for()
        assert page.locator('.report-table .amount').all_text_contents()==['195','180']
        assert page.locator('.ledger .num').all_text_contents()==['180','+15','195','195','0']
        assert page.locator('.record-table tr.added').count()==1
        receipts.append({'check':'changed source values recompute; stale result removed','result':'pass'})
        for name,title in [('equal','The captured totals agree.'),('snapshots','The evidence does not isolate a cause.'),('ambiguous','The evidence does not isolate a cause.'),('missing','The evidence does not isolate a cause.')]:
            page.locator('#scenario').select_option(name)
            page.get_by_role('button',name='Compare totals').click()
            page.get_by_role('heading',name=title).wait_for()
            assert page.locator('#diagnose').count()==0
            capture(page,str(OUT/named(f'r4-{name}-1440.png')))
        receipts.append({'check':'equal, snapshot, ambiguous and missing-context states','result':'pass'})
        page.locator('#scenario').select_option('status')
        page.locator('.tools').evaluate('(e)=>e.open=true')
        for mode,message in [('denied','Required report evidence is unavailable.'),('expired','The connection session expired.'),('timeout','Could not reproduce this report. Injected timeout.'),('error','Could not reproduce this report. Injected error.')]:
            page.locator('#condition').select_option(mode)
            page.get_by_role('button',name='Compare totals').click()
            page.get_by_text(message,exact=True).wait_for()
            assert page.locator('.report-table').count()==0
        for mode in ['transient','rate_limit']:
            page.locator('#condition').select_option(mode)
            page.get_by_role('button',name='Compare totals').click()
            page.get_by_role('button',name='Test the status selection').wait_for()
            body=page.request.get(url+'/api/jobs/'+page.url.split('job=')[1]).json()
            assert len([e for e in body['cleanup']['events'] if e['event']=='retry'])==1
        page.locator('#condition').select_option('slow')
        page.get_by_role('button',name='Compare totals').click()
        assert page.locator('#case-file').is_disabled() and page.locator('#condition').is_disabled()
        page.get_by_role('button',name='Cancel investigation').click()
        page.get_by_text('Investigation canceled. No conclusion was produced.',exact=True).wait_for()
        page.wait_for_timeout(1000)
        assert page.locator('.report-table').count()==0
        receipts.append({'check':'injected failures, one bounded retry, canceled attempt cannot publish','result':'pass'})
        page.locator('#condition').select_option('normal')
        page.get_by_role('button',name='Compare totals').click()
        page.get_by_role('button',name='Test the status selection').click()
        page.get_by_role('heading',name='The status selection explains the gap.').wait_for()
        external=[]
        page.on('request',lambda req:external.append(req.url) if not req.url.startswith(url) else None)
        page.route('**/*',lambda route:route.continue_() if route.request.url.startswith(url) else route.abort())
        page.reload(wait_until='networkidle')
        page.get_by_role('heading',name='The status selection explains the gap.').wait_for()
        assert not external,external
        receipts.append({'check':'no external network dependency','result':'pass'})
        for width in [320,390,768,1120,1440]:
            page.set_viewport_size({'width':width,'height':1100})
            metrics=page.evaluate('({width:innerWidth,scroll:document.documentElement.scrollWidth,font:document.fonts.check("15px Inter")})')
            assert metrics['scroll']<=width,metrics
            assert metrics['font']
            capture(page,str(OUT/named(f'r4-demonstrated-{width}.png')))
            page.locator('.tools').evaluate('(e)=>e.open=false')
            receipts.append({'check':'responsive demonstrated state','result':'pass',**metrics})
        page.set_viewport_size({'width':390,'height':1100})
        page.locator('#scenario').select_option('snapshots')
        page.get_by_role('button',name='Compare totals').click()
        page.get_by_role('heading',name='The evidence does not isolate a cause.').wait_for()
        capture(page,str(OUT/named('r4-unresolved-390.png')))
        # Keyboard focus is observable; traverse from the skip link into the real controls.
        page.goto(url,wait_until='networkidle')
        focus=[]
        for _ in range(16):
            page.keyboard.press(TAB)
            focus.append(page.evaluate('({tag:document.activeElement.tagName,id:document.activeElement.id,outline:getComputedStyle(document.activeElement).outlineStyle})'))
        assert any(item['id']=='compare' and item['outline']=='solid' for item in focus),focus
        receipts.append({'check':'keyboard traversal and visible focus','result':'pass','focus':focus})
        assert not errors,errors
        (OUT/named('browser-checks.json')).write_text(json.dumps({'browser':f'{ENGINE} {browser.version}, {HOST} headless','checks':receipts,'page_errors':errors},indent=2)+'\n')
        browser.close()
    stop(http,thread)
print(json.dumps(receipts,indent=2))
