"""Automated accessibility audit, accessibility-tree capture, touch emulation and forced colors.

These are emulations and rule checks. They do not replace a person using VoiceOver, NVDA,
Windows High Contrast or a physical phone; ACCEPTANCE-RECEIPT.md keeps those as open limits.
axe-core is downloaded once from the npm registry, checked against its published integrity
hash and cached in the ignored .local/ folder.
"""
import base64
import hashlib
import io
import json
import sys
import tarfile
import urllib.request
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine import HOST, capture, ENGINE, TAB, ROOT, isolated_server, launch, named

AXE_VERSION = "4.14.0"
AXE_INTEGRITY = "sha512-9WTZxEjsZ7b13TH8JPmbV2z8CHbl80/2hm3XPEG4JgNdQLK81IBRXmSxHfMAOkSqQeRxT/0dwNDz2GOm3zzpcQ=="
AXE_TAGS = ["wcag2a", "wcag2aa", "wcag21a", "wcag21aa", "wcag22aa"]
DEVICES = {"webkit": "iPhone 15", "chromium": "Pixel 7"}
OUT = ROOT / "verification"


def axe_source():
    cached = ROOT / ".local" / f"axe-core-{AXE_VERSION}.min.js"
    if not cached.exists():
        url = f"https://registry.npmjs.org/axe-core/-/axe-core-{AXE_VERSION}.tgz"
        tarball = urllib.request.urlopen(url, timeout=60).read()
        digest = "sha512-" + base64.b64encode(hashlib.sha512(tarball).digest()).decode()
        assert digest == AXE_INTEGRITY, f"axe-core tarball integrity mismatch: {digest}"
        with tarfile.open(fileobj=io.BytesIO(tarball)) as archive:
            cached.parent.mkdir(exist_ok=True)
            cached.write_bytes(archive.extractfile("package/axe.min.js").read())
    return cached.read_text()


def run_flow(page, url, tap=False):
    """The primary path: compare, then test the selection, ending on the finding."""
    act = (lambda loc: loc.tap()) if tap else (lambda loc: loc.click())
    page.goto(url, wait_until="networkidle")
    act(page.locator("#compare"))
    page.get_by_role("button", name="Test the status selection").wait_for()
    act(page.locator("#diagnose"))
    page.get_by_role("heading", name="The status selection explains the gap.").wait_for()


def audit(page, axe):
    page.add_script_tag(content=axe)
    result = page.evaluate("tags => axe.run(document, {runOnly: {type: 'tag', values: tags}})", AXE_TAGS)
    return {"violations": [{"id": v["id"], "impact": v["impact"], "nodes": [n["target"] for n in v["nodes"]]}
                           for v in result["violations"]],
            "passes": len(result["passes"]), "incomplete": [v["id"] for v in result["incomplete"]]}


def axe_states(browser, url, axe):
    # The app forbids inline scripts; only this audit context bypasses that to load axe.
    page = browser.new_page(viewport={"width": 1280, "height": 900}, reduced_motion="reduce", bypass_csp=True)
    report = {}
    page.goto(url, wait_until="networkidle")
    report["start"] = audit(page, axe)
    page.locator("#compare").click()
    page.get_by_role("button", name="Test the status selection").wait_for()
    report["compared"] = audit(page, axe)
    page.locator("#diagnose").click()
    page.get_by_role("heading", name="The status selection explains the gap.").wait_for()
    report["finding"] = audit(page, axe)
    for details in page.locator(".evidence>details").all():
        details.locator("summary").click()
    report["evidence open"] = audit(page, axe)
    tree = page.locator("#workspace").aria_snapshot()
    page.locator(".secondary-tools summary").first.click()
    page.locator("#condition").select_option("denied")
    page.locator("#compare").click()
    page.get_by_text("Required report evidence is unavailable.", exact=True).wait_for()
    report["denied"] = audit(page, axe)
    live = page.locator("#message").evaluate("e => ({role: e.getAttribute('role'), live: e.getAttribute('aria-live'), text: e.textContent})")
    page.close()
    return report, tree, live


def touch(playwright, browser, url):
    device = dict(playwright.devices[DEVICES[ENGINE]])
    device.pop("default_browser_type", None)
    page = browser.new_context(**device, reduced_motion="reduce").new_page()
    run_flow(page, url, tap=True)
    landing = page.evaluate("""(() => {
      const e = document.activeElement, r = e.getBoundingClientRect(), ledger = document.querySelector('.ledger').getBoundingClientRect();
      return {focus: e.id, top: Math.round(r.top), ledger_top: Math.round(ledger.top), viewport: [innerWidth, innerHeight],
              horizontal_scroll: document.documentElement.scrollWidth > innerWidth};
    })()""")
    page.screenshot(path=OUT / named("r5-touch-finding.png"))
    page.locator(".secondary-tools summary").first.tap()
    for details in page.locator(".evidence>details").all():
        details.locator("summary").tap()
    # WCAG 2.5.8 asks for 24 px targets (or spacing); Apple and Google advise 44/48 px.
    targets = page.evaluate("""[...document.querySelectorAll('button, a[href], select, input, summary, [tabindex="0"]')]
      .filter(e => e.offsetParent !== null && !e.closest('.table-scroll') || e.matches('.table-scroll'))
      .map(e => { const r = e.getBoundingClientRect(); return {target: e.id || e.textContent.trim().slice(0, 40) || e.tagName,
                  width: Math.round(r.width), height: Math.round(r.height), inline: getComputedStyle(e).display === 'inline'}; })""")
    small = [t for t in targets if min(t["width"], t["height"]) < 24 and not t["inline"]]
    under_44 = [t for t in targets if t["height"] < 44 and not t["inline"]]
    page.context.close()
    assert landing["focus"] == "finding-title" and not landing["horizontal_scroll"], landing
    assert landing["ledger_top"] < landing["viewport"][1], landing
    assert not small, small
    return {"device": DEVICES[ENGINE], "landing": landing, "targets": len(targets),
            "below_24px": small, "below_44px_tall": under_44}


def forced_colors(browser, url):
    page = browser.new_page(viewport={"width": 390, "height": 900}, forced_colors="active", reduced_motion="reduce")
    run_flow(page, url)
    for details in page.locator(".evidence>details").all():
        details.locator("summary").click()
    active = page.evaluate("matchMedia('(forced-colors: active)').matches")
    capture(page,OUT / named("r5-forced-colors-390.png"))
    page.keyboard.press(TAB)
    boundaries = page.evaluate("""(() => {
      const css = (sel, prop) => { const e = document.querySelector(sel); return e ? getComputedStyle(e)[prop] : null; };
      const focused = getComputedStyle(document.activeElement);
      return {ledger_total_rule: css('.ledger .total td', 'borderTopStyle'),
              ledger_row_rule: css('.ledger td', 'borderTopStyle'),
              diff_mark_border: css('.diff-mark', 'borderTopStyle'),
              button_border: css('button', 'borderTopStyle'),
              focus_outline: [focused.outlineStyle, focused.outlineWidth]};
    })()""")
    page.close()
    assert active, "forced-colors emulation did not apply"
    missing = [k for k, v in boundaries.items() if v in ("none", "hidden") or (k == "focus_outline" and v[0] == "none")]
    assert not missing, (missing, boundaries)
    return boundaries


with isolated_server() as url, sync_playwright() as p:
    browser = launch(p)
    axe_report, tree, live = axe_states(browser, url, axe_source())
    receipt = {"browser": f"{ENGINE} {browser.version}, {HOST}", "axe_core": AXE_VERSION, "axe_tags": AXE_TAGS,
               "axe": axe_report, "status_region": live}
    violations = {state: r["violations"] for state, r in axe_report.items() if r["violations"]}
    if ENGINE in DEVICES:
        receipt["touch"] = touch(p, browser, url)
    if ENGINE == "chromium":
        receipt["forced_colors"] = forced_colors(browser, url)
    browser.close()
(OUT / named("a11y-tree.txt")).write_text(tree + "\n")
receipt["result"] = "fail" if violations else "pass"
(OUT / named("assistive-checks.json")).write_text(json.dumps(receipt, indent=2) + "\n")
assert not violations, json.dumps(violations, indent=2)
print(f"{ENGINE}: axe {AXE_VERSION} WCAG 2.2 AA clean in {len(axe_report)} states"
      + (", touch" if "touch" in receipt else "") + (", forced colors" if "forced_colors" in receipt else "") + ": PASS")
