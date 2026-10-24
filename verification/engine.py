"""Browser choice for the checks: Firefox on this host, any engine inside the Playwright container.

Chromium on this Arch host never fires requestAnimationFrame, so its click checks stall; the
official Ubuntu image (run_matrix.sh) renders Chromium, WebKit and Firefox normally.
"""
import contextlib
import os
import sys
import tempfile
import threading
from http.server import ThreadingHTTPServer
from pathlib import Path

ENGINE = os.environ.get("ENGINE", "firefox")
ROOT = Path(__file__).resolve().parents[1]
HOST_FIREFOX = "/home/rahil/.cache/ms-playwright/firefox-1555/firefox/firefox"


def launch(playwright):
    browser_type = getattr(playwright, ENGINE)
    if ENGINE == "firefox" and os.path.exists(HOST_FIREFOX):
        return browser_type.launch(executable_path=HOST_FIREFOX, headless=True)
    return browser_type.launch(headless=True)


def named(filename):
    """Firefox keeps the historical receipt names; other engines get a suffix."""
    if ENGINE == "firefox":
        return filename
    stem, dot, ext = filename.rpartition(".")
    return f"{stem}-{ENGINE}{dot}{ext}"

# Full-page captures otherwise paint the sticky banner wherever the scroll position left it.
CAPTURE_STYLE = ".simulation{position:static!important}"


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
