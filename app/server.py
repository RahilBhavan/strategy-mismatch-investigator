"""Local HTTP boundary. No enterprise connections or third-party dependencies."""
import argparse
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse
from .schema import CaseError, MAX_BYTES, canonical
from .store import Store

WEB = Path(__file__).resolve().parents[1] / "web"


def no_duplicate_keys(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("Duplicate JSON key.")
        result[key] = value
    return result


def handler(store):
    class Handler(BaseHTTPRequestHandler):
        def log_message(self, *args):
            pass

        def send(self, code, value):
            body = canonical(value).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Cache-Control", "no-store")
            self.send_header("X-Content-Type-Options", "nosniff")
            self.end_headers()
            self.wfile.write(body)

        def body(self):
            origin = self.headers.get("Origin")
            if origin and urlparse(origin).netloc != self.headers.get("Host"):
                raise CaseError("Cross-origin writes are not accepted.", code="forbidden")
            if self.headers.get("Sec-Fetch-Site") == "cross-site":
                raise CaseError("Cross-site writes are not accepted.", code="forbidden")
            size = int(self.headers.get("Content-Length", "0"))
            if not 0 < size <= MAX_BYTES:
                raise CaseError("Request must contain JSON under 20 MB.")
            if "application/json" not in self.headers.get("Content-Type", ""):
                raise CaseError("Send application/json.")
            return json.loads(self.rfile.read(size), object_pairs_hook=no_duplicate_keys,
                              parse_constant=lambda _: (_ for _ in ()).throw(ValueError("Non-finite JSON.")))

        def respond(self, action):
            try:
                action()
            except CaseError as error:
                code = {"not_found": 404, "forbidden": 403, "busy": 409, "stale": 409}.get(error.code, 400)
                self.send(code, dict(error=dict(code=error.code, message=str(error), field=error.field)))
            except (ValueError, KeyError, TypeError, AttributeError, RecursionError):
                self.send(400, dict(error=dict(code="invalid", message="Cannot compare: check the highlighted inputs.", field="request")))
            except (BrokenPipeError, ConnectionResetError):
                pass

        def do_GET(self):
            self.respond(self.get)

        def get(self):
            path = urlparse(self.path).path
            parts = path.strip("/").split("/")
            if path == "/api/catalog":
                return self.send(200, dict(cases=store.cases(), live_connection="not tested"))
            if len(parts) == 3 and parts[:2] == ["api", "cases"]:
                return self.send(200, store.case(parts[2]))
            if len(parts) in {3, 4} and parts[:2] == ["api", "jobs"]:
                if len(parts) == 4 and parts[3] == "export":
                    return self.send(200, store.export(parts[2]))
                if len(parts) == 3:
                    return self.send(200, store.job(parts[2]))
            if path.startswith("/api/"):
                raise CaseError("API route not found.", code="not_found")
            file = (WEB / (path.lstrip("/") or "index.html")).resolve()
            if WEB not in file.parents or not file.is_file():
                raise CaseError("Page not found.", code="not_found")
            body = file.read_bytes()
            self.send_response(200)
            self.send_header("Content-Type", mimetypes.guess_type(file)[0] or "application/octet-stream")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("X-Content-Type-Options", "nosniff")
            self.send_header("Content-Security-Policy", "default-src 'self'; script-src 'self'; style-src 'self'; font-src 'self'; connect-src 'self'; img-src 'self' data:; object-src 'none'; base-uri 'none'; frame-ancestors 'self'")
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            self.respond(self.post)

        def post(self):
            path = urlparse(self.path).path
            body = self.body()
            if path == "/api/cases":
                return self.send(201, store.save_case(body))
            if path == "/api/jobs":
                if not isinstance(body, dict) or set(body) != {"case_id", "fingerprint", "phase", "mode"}:
                    raise CaseError("Choose a case, fingerprint, phase and injected condition.")
                if any(not isinstance(v, str) for v in body.values()):
                    raise CaseError("Investigation references must be text.")
                return self.send(202, store.submit(body["case_id"], body["fingerprint"], body["phase"], body["mode"]))
            if path == "/api/restore":
                return self.send(201, store.restore(body))
            parts = path.strip("/").split("/")
            if len(parts) == 4 and parts[:2] == ["api", "jobs"] and parts[3] == "cancel":
                return self.send(200, store.cancel(parts[2]))
            raise CaseError("API route not found.", code="not_found")

        def do_PUT(self):
            def put():
                parts = urlparse(self.path).path.strip("/").split("/")
                if len(parts) != 3 or parts[:2] != ["api", "cases"]:
                    raise CaseError("API route not found.", code="not_found")
                store.case(parts[2])
                self.send(200, store.save_case(self.body(), parts[2]))
            self.respond(put)
    return Handler


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8807)
    parser.add_argument("--host", default="127.0.0.1", help="Bind address; use a private (e.g. Tailscale) address only for device checks")
    parser.add_argument("--db", type=Path, default=Path(__file__).resolve().parents[1] / ".local" / "demo.sqlite3")
    args = parser.parse_args()
    args.db.parent.mkdir(parents=True, exist_ok=True)
    store = Store(args.db)
    server = ThreadingHTTPServer((args.host, args.port), handler(store))
    print(f"Synthetic Strategy POC: http://{args.host}:{args.port}", flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
