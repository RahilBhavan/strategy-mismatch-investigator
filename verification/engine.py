"""Browser choice for the checks: Firefox on this host, any engine inside the Playwright container.

Chromium on this Arch host never fires requestAnimationFrame, so its click checks stall; the
official Ubuntu image (run_matrix.sh) renders Chromium, WebKit and Firefox normally.
"""
import contextlib
import os
import platform
import sys
import tempfile
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

ENGINE = os.environ.get("ENGINE", "firefox")
ROOT = Path(__file__).resolve().parents[1]
# A Playwright Firefox already downloaded on this host, if any; otherwise the bundled default.
HOST_FIREFOX = next(iter(sorted(Path.home().glob(".cache/ms-playwright/firefox-*/firefox/firefox"), reverse=True)), None)
HOST = f"macOS {platform.mac_ver()[0]}" if sys.platform == "darwin" else "Linux"
# Safari on macOS tabs only to form fields unless the user enables "Press Tab to highlight each
# item"; Option+Tab reaches every control, as a default-settings Safari user would press it.
TAB = "Alt+Tab" if ENGINE == "webkit" and sys.platform == "darwin" else "Tab"


def launch(playwright):
    browser_type = getattr(playwright, ENGINE)
    if ENGINE == "firefox" and HOST_FIREFOX:
        return browser_type.launch(executable_path=HOST_FIREFOX, headless=True)
    return browser_type.launch(headless=True)


def named(filename):
    """Firefox keeps the historical receipt names; other engines (or RECEIPT_SUFFIX) get a suffix."""
    suffix = os.environ.get("RECEIPT_SUFFIX", "" if ENGINE == "firefox" else ENGINE)
    if not suffix:
        return filename
    stem, dot, ext = filename.rpartition(".")
    return f"{stem}-{suffix}{dot}{ext}"

def capture(page, path):
    """Full-page capture from the top. Otherwise the sticky banner is painted wherever the scroll
    position left it; an injected override style cannot help because the app's CSP blocks it."""
    page.mouse.move(0, 0)  # no hover colour left on the last button pressed
    page.evaluate("scrollTo(0, 0)")
    page.wait_for_timeout(50)
    page.screenshot(path=str(path), full_page=True)


@contextlib.contextmanager
def isolated_server():
    """A private app server on a free port with a throwaway database; never the 8807 demo."""
    sys.path.insert(0, str(ROOT))
    from app.server import handler
    from app.store import Store
    with tempfile.TemporaryDirectory() as tmp:
        http = ThreadingHTTPServer(("127.0.0.1", 0), handler(Store(Path(tmp) / "check.sqlite3")))
        thread = threading.Thread(target=http.serve_forever, daemon=True)
        thread.start()
        try:
            yield f"http://127.0.0.1:{http.server_port}"
        finally:
            http.shutdown()
            http.server_close()
            thread.join()
