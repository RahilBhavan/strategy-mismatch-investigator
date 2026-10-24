"""Dedicated local persistence; nothing connects to Orbit or enterprise services."""
import json
import sqlite3
import threading
import time
import uuid
from contextlib import contextmanager
from copy import deepcopy
from .adapter import AdapterFailure, MODES, SimulatedAdapter
from .fixtures import examples
from .investigate import investigate
from .schema import CaseError, LABEL, VERSION, canonical, fingerprint, validate_case


def stable_result(value):
    if isinstance(value, dict):
        return {key: stable_result(item) for key, item in value.items() if key != "instance_id"}
    if isinstance(value, list):
        return [stable_result(item) for item in value]
    return value


class Store:
    def __init__(self, path):
        self.path = str(path)
        self.lock = threading.RLock()
        self.events = {}
        with self.db() as db:
            db.executescript("""CREATE TABLE IF NOT EXISTS cases(id TEXT PRIMARY KEY,body TEXT NOT NULL,fp TEXT NOT NULL);
            CREATE TABLE IF NOT EXISTS jobs(id TEXT PRIMARY KEY,case_id TEXT NOT NULL,case_fp TEXT NOT NULL,
            snapshot TEXT NOT NULL,phase TEXT NOT NULL,mode TEXT NOT NULL,state TEXT NOT NULL,
            result TEXT,error TEXT,cleanup TEXT,created REAL NOT NULL);""")
            db.execute("UPDATE jobs SET state='interrupted',error=? WHERE state IN ('queued','running')",
                       (canonical(dict(code="interrupted", message="Application restarted. Retry this investigation.")),))
            for key, value in examples().items():
                db.execute("INSERT OR IGNORE INTO cases VALUES(?,?,?)", (key, canonical(value), fingerprint(value)))

    @contextmanager
    def db(self):
        connection = sqlite3.connect(self.path, timeout=10)
        connection.row_factory = sqlite3.Row
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def cases(self):
        with self.db() as db:
            return [dict(id=row["id"], name=json.loads(row["body"])["name"], fingerprint=row["fp"])
                    for row in db.execute("SELECT * FROM cases ORDER BY rowid")]

    def case(self, key):
        with self.db() as db:
            row = db.execute("SELECT * FROM cases WHERE id=?", (key,)).fetchone()
        if not row:
            raise CaseError("Case not found.", "case_id", "not_found")
        return dict(id=row["id"], case=json.loads(row["body"]), fingerprint=row["fp"])

    def save_case(self, value, key=None):
        value = validate_case(value)
        key = key or "custom-" + uuid.uuid4().hex[:12]
        with self.lock, self.db() as db:
            db.execute("INSERT INTO cases VALUES(?,?,?) ON CONFLICT(id) DO UPDATE SET body=excluded.body,fp=excluded.fp",
                       (key, canonical(value), fingerprint(value)))
        return self.case(key)

    def submit(self, key, expected_fp, phase, mode):
        if phase not in {"compare", "diagnose"} or mode not in MODES:
            raise CaseError("Choose a supported phase and injected condition.")
        with self.lock:
            source = self.case(key)
            if source["fingerprint"] != expected_fp:
                raise CaseError("Report context changed. Capture a new comparison.", "fingerprint", "stale")
            with self.db() as db:
                previous = db.execute("SELECT id,result,state FROM jobs WHERE case_id=? AND case_fp=? AND phase=? AND mode=? "
                                      "AND state IN ('queued','running','complete') ORDER BY created DESC LIMIT 1",
                                      (key, expected_fp, phase, mode)).fetchone()
                if previous and (previous["state"] != "complete" or json.loads(previous["result"])["software_version"] == VERSION):
                    return self.job(previous["id"])
                if db.execute("SELECT 1 FROM jobs WHERE state IN ('queued','running') LIMIT 1").fetchone():
                    raise CaseError("One investigation is already running. Cancel it or wait.", "job", "busy")
                job_id = uuid.uuid4().hex
                db.execute("INSERT INTO jobs(id,case_id,case_fp,snapshot,phase,mode,state,created) VALUES(?,?,?,?,?,?,?,?)",
                           (job_id, key, expected_fp, canonical(source["case"]), phase, mode, "queued", time.time()))
            event = self.events[job_id] = threading.Event()
            threading.Thread(target=self._run, args=(job_id, source["case"], phase, mode, event), daemon=True).start()
            return self.job(job_id)

    def _run(self, job_id, case, phase, mode, event):
        adapter = SimulatedAdapter(case, cancel=event, mode=mode)
        result, error, state = None, None, "failed"
        try:
            with self.db() as db:
                db.execute("UPDATE jobs SET state='running' WHERE id=? AND state='queued'", (job_id,))
            result = investigate(case, adapter, phase)
            state = "complete"
        except (AdapterFailure, CaseError) as failure:
            error = dict(code=getattr(failure, "code", "invalid"), message=str(failure))
            state = "canceled" if error["code"] == "canceled" else "failed"
        except Exception:
            error = dict(code="internal", message="Could not reproduce this report. Unexpected local error.")
        finally:
            cleanup = adapter.cleanup()
            # Serialize final publication with cancellation; canceled attempts never become completed.
            with self.lock:
                if event.is_set():
                    result, state = None, "canceled"
                    error = dict(code="canceled", message="Investigation canceled. No conclusion was produced.")
                with self.db() as db:
                    db.execute("UPDATE jobs SET state=?,result=?,error=?,cleanup=? WHERE id=?",
                               (state, canonical(result) if result else None, canonical(error) if error else None,
                                canonical(cleanup), job_id))
                self.events.pop(job_id, None)

    def job(self, job_id):
        with self.db() as db:
            row = db.execute("SELECT * FROM jobs WHERE id=?", (job_id,)).fetchone()
            if not row:
                raise CaseError("Investigation not found.", "job", "not_found")
            current = db.execute("SELECT fp FROM cases WHERE id=?", (row["case_id"],)).fetchone()
        return dict(id=row["id"], case_id=row["case_id"], fingerprint=row["case_fp"], phase=row["phase"],
                    mode=row["mode"], state=row["state"], stale=not current or current["fp"] != row["case_fp"] or (row["result"] is not None and json.loads(row["result"]).get("software_version") != VERSION),
                    result=json.loads(row["result"]) if row["result"] else None,
                    error=json.loads(row["error"]) if row["error"] else None,
                    cleanup=json.loads(row["cleanup"]) if row["cleanup"] else None,
                    label=LABEL, live_connection="not tested")

    def cancel(self, job_id):
        with self.lock:
            self.job(job_id)
            event = self.events.get(job_id)
            if event:
                event.set()
        return self.job(job_id)

    def export(self, job_id):
        job = self.job(job_id)
        if job["state"] != "complete":
            raise CaseError("Only a completed synthetic investigation can be exported.")
        with self.db() as db:
            row = db.execute("SELECT snapshot FROM jobs WHERE id=?", (job_id,)).fetchone()
        payload = dict(packet_version="synthetic-evidence-v1", label=LABEL, live_connection="not tested",
                       software_version=VERSION, case=json.loads(row["snapshot"]), result=job["result"],
                       source_stale=job["stale"], mode=job["mode"], cleanup=job["cleanup"])
        return dict(payload=payload, sha256=fingerprint(payload))

    def restore(self, packet):
        if not isinstance(packet, dict) or set(packet) != {"payload", "sha256"}:
            raise CaseError("Choose an exported synthetic evidence packet.", "packet")
        body = packet["payload"]
        expected = {"packet_version", "label", "live_connection", "software_version", "case", "result", "source_stale", "mode", "cleanup"}
        if not isinstance(body, dict) or set(body) != expected or fingerprint(body) != packet["sha256"]:
            raise CaseError("Evidence packet integrity check failed.", "packet")
        if body["packet_version"] != "synthetic-evidence-v1" or body["label"] != LABEL or body["live_connection"] != "not tested":
            raise CaseError("Only labeled synthetic evidence is accepted.", "packet")
        if body["software_version"] != VERSION:
            raise CaseError("This packet uses a different computation version. Keep the original packet and rerun its source.", "packet")
        case = validate_case(body["case"])
        phase = body["result"].get("phase") if isinstance(body["result"], dict) else None
        if phase not in {"compare", "diagnose"}:
            raise CaseError("Packet has an unsupported experiment phase.", "packet")
        if body["mode"] not in MODES:
            raise CaseError("Unsupported packet condition.", "packet")
        adapter = SimulatedAdapter(case, mode="incomplete" if body["mode"] == "incomplete" else "normal")
        try:
            reference = investigate(case, adapter, phase)
        finally:
            adapter.cleanup()
        if stable_result(body["result"]) != stable_result(reference):
            raise CaseError("Evidence does not match recomputation from its synthetic source.", "packet")
        source = self.save_case(case)
        # Imported instance IDs/cleanup are untrusted historical claims. Use recomputed evidence.
        job_id = uuid.uuid4().hex
        with self.db() as db:
            db.execute("INSERT INTO jobs VALUES(?,?,?,?,?,?,?,?,?,?,?)",
                       (job_id, source["id"], source["fingerprint"], canonical(case), phase, "normal", "complete",
                        canonical(reference), None, canonical(adapter.cleanup()), time.time()))
        job = self.job(job_id)
        job["import_note"] = "Packet arithmetic recomputed locally; original instance IDs are historical only."
        return job
