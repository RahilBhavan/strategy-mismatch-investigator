"""A record-backed simulation; operation names are ours, not endpoint compatibility."""
import threading
import time
import uuid
from copy import deepcopy
from .schema import MAX_MINOR, CaseError, display, fingerprint, minor

MODES = {"normal", "denied", "expired", "transient", "rate_limit", "timeout", "incomplete", "error", "slow"}


class AdapterFailure(Exception):
    def __init__(self, code, message):
        super().__init__(message)
        self.code = code


class SimulatedAdapter:
    def __init__(self, case, cancel=None, mode="normal", timeout=5):
        if mode not in MODES:
            raise CaseError("Unknown injected condition.", "mode")
        self.case = case
        self.cancel = cancel or threading.Event()
        self.mode, self.timeout = mode, timeout
        self.instances = []
        self.events = []
        self.calls = 0

    def wait(self, duration, deadline):
        until = time.monotonic() + duration
        while time.monotonic() < until:
            self.check(deadline)
            self.cancel.wait(min(.02, max(0, until - time.monotonic())))
        self.check(deadline)

    def check(self, deadline):
        if self.cancel.is_set():
            raise AdapterFailure("canceled", "Investigation canceled. No conclusion was produced.")
        if time.monotonic() > deadline:
            raise AdapterFailure("timeout", "Could not reproduce this report. Execution exceeded 5 seconds.")

    def execute(self, report, overrides=None):
        deadline = time.monotonic() + self.timeout
        for attempt in range(2):
            try:
                return self._execute(report, overrides, deadline)
            except AdapterFailure as error:
                if error.code not in {"transient", "rate_limit"} or attempt:
                    raise
                retry_after = .05
                self.events.append(dict(event="retry", reason=error.code, retry_after=retry_after))
                self.wait(retry_after, deadline)
        raise AssertionError("unreachable")

    def _execute(self, report, overrides, deadline):
        self.calls += 1
        self.check(deadline)
        if self.mode == "denied":
            raise AdapterFailure("denied", "Required report evidence is unavailable.")
        if self.mode == "expired":
            raise AdapterFailure("expired", "The connection session expired.")
        if self.mode in {"transient", "rate_limit"} and self.calls == 1:
            raise AdapterFailure(self.mode, "Injected transient connection failure.")
        instance = dict(id=f"sim-{uuid.uuid4().hex[:12]}", report_id=report["id"], state="running",
                        diagnostic=overrides is not None)
        self.instances.append(instance)
        self.wait(.8 if self.mode == "slow" else .03, deadline)
        if self.mode in {"timeout", "error"}:
            raise AdapterFailure(self.mode, "Could not reproduce this report. Injected " + self.mode + ".")
        if report["definition"] != "SUM(amount)":
            raise AdapterFailure("unsupported", "This metric calculation is outside the first-release scope.")
        filters = deepcopy(report["filters"])
        if overrides:
            filters.update(overrides)
        total, selected, known = 0, 0, 0
        for index, row in enumerate(self.case["records"]):
            if index % 256 == 0:
                self.check(deadline)
            if any(values is not None and row[key] not in values for key, values in filters.items()):
                continue
            selected += 1
            value = minor(row["amount"], report["scale"])
            if value is not None:
                known += 1
                total += value
                if abs(total) > MAX_MINOR:
                    raise AdapterFailure("overflow", "Could not reproduce this report. Exact amount overflow.")
        instance["state"] = "completed"
        self.events.append(dict(event="execute", instance_id=instance["id"], report_id=report["id"], filters=filters))
        return dict(instance_id=instance["id"], report_id=report["id"], name=report["name"], filters=filters,
                    total=display(total if known else None, report["scale"]),
                    minor=str(total) if known else None, selected_rows=selected, non_null_rows=known,
                    complete=report["complete"] and self.mode != "incomplete", snapshot=report["snapshot"],
                    definition_hash=fingerprint(report))

    def cleanup(self):
        for instance in self.instances:
            instance["state"] = "released"
        return dict(created=len(self.instances), released=len(self.instances), instances=deepcopy(self.instances),
                    live_strategy="not tested", events=deepcopy(self.events))
