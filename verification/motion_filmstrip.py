"""Normal-motion capture of the result transition: the finding fades from 50% to full opacity in 180 ms."""
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright
sys.path.insert(0, str(Path(__file__).resolve().parent))
from engine import ENGINE, isolated_server, launch, named

OUT = Path(__file__).resolve().parent
frames = []
with isolated_server() as URL, sync_playwright() as p:
    browser = launch(p)
    page = browser.new_page(viewport={"width": 1120, "height": 900}, reduced_motion="no-preference")
    page.goto(URL+"/?case=status", wait_until="networkidle")
    page.get_by_role("button", name="Compare totals").click()
    page.get_by_role("button", name="Test the status selection").click()
    page.locator("#finding-title").wait_for()
    # Sample the running animation's own clock instead of guessing wall-clock offsets.
    animation = "document.querySelector('.finding').getAnimations()[0]"
    page.evaluate(f"{animation}.pause()")
    for ms in (0, 60, 120, 180):
        page.evaluate(f"{animation}.currentTime={ms}")
        opacity = page.evaluate("getComputedStyle(document.querySelector('.finding')).opacity")
        path = OUT / named(f"r4-motion-{ms}ms.png")
        page.locator(".finding").screenshot(path=str(path))
        frames.append(dict(ms=ms, opacity=float(opacity), frame=path.name))
    focused = page.evaluate("document.activeElement.id")
    browser.close()
assert frames[0]["opacity"] < frames[-1]["opacity"] == 1, frames
(OUT / named("motion-filmstrip.json")).write_text(json.dumps(dict(engine=ENGINE, duration_ms=180, frames=frames, focus_after_result=focused), indent=2) + "\n")
print(json.dumps(frames))
