"""WCAG text contrast for visible text nodes and form-control values across six states at two widths.

Not measured: hover/focus colours, non-text contrast (borders, focus rings) and text over images.
"""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine import HOST, ENGINE, isolated_server, launch, named

ROOT = Path(__file__).resolve().parents[1]
# Resolve the effective background by walking ancestors; blend translucent layers over white.
MEASURE = """() => {
 const rgb = s => (s.match(/[\\d.]+/g) || []).map(Number);
 const lum = c => { const [r,g,b] = c.slice(0,3).map(v => { v /= 255; return v <= .03928 ? v/12.92 : ((v+.055)/1.055)**2.4; }); return .2126*r + .7152*g + .0722*b; };
 const bgOf = e => { let layers = []; for (let p = e; p; p = p.parentElement) { const c = rgb(getComputedStyle(p).backgroundColor); if (c.length && (c[3] ?? 1) > 0) { layers.push(c); if ((c[3] ?? 1) >= 1) break; } }
   let out = [255,255,255]; for (const c of layers.reverse()) { const a = c[3] ?? 1; out = out.map((v,i) => c[i]*a + v*(1-a)); } return out; };
 const rows = [];
 for (const e of document.querySelectorAll('body *')) {
  const control = ['INPUT','SELECT','BUTTON'].includes(e.tagName) && (e.value || e.textContent).trim();
  const own = control || [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim());
  const r = e.getBoundingClientRect(), st = getComputedStyle(e);
  if (!own || !r.width || !r.height || st.visibility === 'hidden' || e.closest('[hidden],details:not([open])>*:not(summary)')) continue;
  let fg = rgb(st.color); const bg = bgOf(e);
  let op = 1; for (let q = e; q; q = q.parentElement) op *= parseFloat(getComputedStyle(q).opacity);
  if ((fg[3] ?? 1) < 1) fg = fg.map((v,i) => i < 3 ? v*fg[3] + bg[i]*(1-fg[3]) : v);
  if (op < 1) fg = fg.map((v,i) => i < 3 ? v*op + bg[i]*(1-op) : v);
  const [l1, l2] = [lum(fg), lum(bg)].sort((a,b) => b-a);
  const size = parseFloat(st.fontSize), weight = parseInt(st.fontWeight);
  const large = size >= 24 || (size >= 18.66 && weight >= 700);
  rows.push({text: e.textContent.trim().slice(0,50), tag: e.tagName, size, ratio: +((l1+.05)/(l2+.05)).toFixed(2), needed: large ? 3 : 4.5, disabled: !!e.closest(':disabled'), width: innerWidth});
 }
 return rows;
}"""
states, failures = {}, []


def capture(page, url, width):
    def record(name):
        states[f"{name} @ {width}px"] = page.evaluate(MEASURE)
    page.goto(url + "/?case=status", wait_until="networkidle")
    record("empty")
    page.get_by_role("button", name="Compare totals").click()
    page.get_by_role("button", name="Test the status selection").wait_for()
    record("candidate")
    page.get_by_role("button", name="Test the status selection").click()
    page.get_by_role("heading", name="The status selection explains the gap.").wait_for()
    for d in page.locator("details").all():
        d.evaluate("e => e.open = true")
    record("demonstrated, all evidence and controls open")
    page.goto(url + "/?case=ambiguous", wait_until="networkidle")
    page.get_by_role("button", name="Compare totals").click()
    page.get_by_role("heading", name="The evidence does not isolate a cause.").wait_for()
    record("unresolved")
    page.get_by_text("Source & test controls", exact=True).click()
    page.locator("#condition").select_option("denied")
    page.get_by_role("button", name="Compare totals").click()
    page.get_by_text("Required report evidence is unavailable.", exact=True).wait_for()
    record("error")
    page.goto(url + "/contract.html", wait_until="networkidle")
    record("integration boundary page")


with isolated_server() as URL, sync_playwright() as p:
    browser = launch(p)
    for width in (1280, 390):
        page = browser.new_page(viewport={"width": width, "height": 1000}, reduced_motion="reduce")
        capture(page, URL, width)
        page.close()
    version = browser.version
    browser.close()
for state, rows in states.items():
    for row in rows:
        if row["ratio"] < row["needed"] and not row["disabled"]:
            failures.append(dict(state=state, **row))
summary = {"browser": f"{ENGINE} {version}, {HOST}", "states": {k: dict(elements=len(v), minimum=min(r["ratio"] for r in v if not r["disabled"])) for k, v in states.items()},
           "failures": failures, "excluded": "disabled controls (WCAG exempts inactive components)",
           "limits": "Text nodes and control values only, at 1280 and 390 CSS px; translucency is blended. Hover/focus colours, non-text contrast and physical displays are not measured."}
(ROOT / "verification" / named("contrast-audit.json")).write_text(json.dumps(summary, indent=2) + "\n")
print(json.dumps({k: v for k, v in summary.items() if k != "failures"}, indent=2), "\nfailures:", json.dumps(failures, indent=1))
