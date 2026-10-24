"""Read-only check against Strategy's public demo Library through its guest login.

Nothing here is wired into the synthetic app. It proves one investigation against a real
Strategy server: authentication, report instances, transient view filters, totals, denial
and session cleanup. It does not prove any customer deployment, privilege model or scale.
"""
import http.cookiejar
import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from decimal import Decimal

BASE = "https://demo.microstrategy.com/MicroStrategyLibrary/api"
TUTORIAL = "B7CA92F04B9FAE8D941C3E9B7E0CD754"
REVENUE = "4C05177011D3E877C000B3B2D86C964F"
CATEGORY = "8D679D3711D3E4981000E787EC6DE8A4"
REGION = "8D679D4B11D3E4981000E787EC6DE8A4"
ELECTRONICS = f"h2;{CATEGORY}"
REPORT_A = "8A6A18DE4E9D410A7A6314BAFA372ADA"  # Region Category
REPORT_B = "2C3DFFB411D6044FC0008C916B98494F"  # Electronics Revenue by Region
CENT = Decimal("0.01")


class LiveFailure(Exception):
    def __init__(self, status, message):
        super().__init__(message)
        self.status = status


class CookieTransport:
    """The Library session is bound to both the auth token and its session cookie."""

    def __init__(self):
        self.opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))

    def __call__(self, method, url, headers, body):
        request = urllib.request.Request(url, method=method, data=body, headers=headers)
        try:
            with self.opener.open(request, timeout=30) as response:
                return response.status, dict(response.headers), response.read()
        except urllib.error.HTTPError as error:
            return error.code, dict(error.headers), error.read()


def elements(attribute, ids, operator="In"):
    return {"operator": operator, "operands": [{"type": "attribute", "id": attribute},
                                               {"type": "elements", "elements": [{"id": i} for i in ids]}]}


def all_of(*filters):
    return filters[0] if len(filters) == 1 else {"operator": "And", "operands": list(filters)}


def metric_total(body, metric_id):
    """Sum one metric over every returned cell; doubles are read through repr, then kept exact."""
    grid = body["definition"]["grid"]
    metrics = [m["id"] for c in grid["columns"] if c["type"] == "templateMetrics" for m in c["elements"]]
    index, width = metrics.index(metric_id), len(metrics)
    cells = [Decimal(repr(v)) for row in body["data"]["metricValues"]["raw"]
             for j, v in enumerate(row) if j % width == index and v is not None]
    paging = body["data"]["paging"]
    return sum(cells, Decimal(0)), len(cells), paging["current"] == paging["total"]


def row_elements(body, attribute):
    for row in body["definition"]["grid"]["rows"]:
        if row["id"] == attribute:
            return {e["id"]: e["formValues"][0] for e in row["elements"]}
    return None


class Session:
    def __init__(self, transport=None, base=BASE, project=TUTORIAL):
        self.transport = transport or CookieTransport()
        self.base, self.project = base, project
        self.token, self.instances, self.calls, self.requests = None, [], 0, []

    def call(self, method, path, body=None):
        headers = {"Content-Type": "application/json", "Accept": "application/json", "X-MSTR-ProjectID": self.project}
        if self.token:
            headers["X-MSTR-AuthToken"] = self.token
        self.calls += 1
        self.requests.append(f"{method} {path.split('?')[0]}")
        status, response_headers, raw = self.transport(method, self.base + path, headers,
                                                       None if body is None else json.dumps(body).encode())
        data = json.loads(raw) if raw and raw.lstrip().startswith(b"{") else None
        return status, {k.lower(): v for k, v in response_headers.items()}, data

    def __enter__(self):
        status, headers, data = self.call("POST", "/auth/login", {"loginMode": 8})
        self.token = headers.get("x-mstr-authtoken")
        if status != 204 or not self.token:
            raise LiveFailure(status, (data or {}).get("message", "Guest login was refused."))
        return self

    def __exit__(self, *exc):
        self.logout_status, _, _ = self.call("POST", "/auth/logout")
        self.token = None

    def execute(self, report_id, view_filter=None):
        status, _, data = self.call("POST", f"/v2/reports/{report_id}/instances?limit=5000",
                                    {} if view_filter is None else {"viewFilter": view_filter})
        if status != 200:
            raise LiveFailure(status, (data or {}).get("message", "Report execution failed."))
        self.instances.append(data["instanceId"])
        total, cells, complete = metric_total(data, REVENUE)
        return dict(report_id=report_id, name=data["name"], instance_id=data["instanceId"], view_filter=view_filter,
                    total=str(total.quantize(CENT)), unrounded=str(total), cells=cells, complete=complete,
                    regions=row_elements(data, REGION), paging=data["data"]["paging"])

    def filter_text(self, report_id):
        status, _, data = self.call("GET", f"/model/reports/{report_id}?showExpressionAs=tree")
        if status == 200:
            return dict(readable=True, text=(data.get("dataSource", {}).get("filter") or {}).get("text", "No report filter"))
        error = ((data or {}).get("errors") or [{}])[0].get("message") or (data or {}).get("message", "")
        return dict(readable=False, status=status, error=error)


def run_check(session):
    """Explain why B's total differs from A by rerunning A with B's observed selections."""
    a, b = session.execute(REPORT_A), session.execute(REPORT_B)
    context = {"A": session.filter_text(REPORT_A), "B": session.filter_text(REPORT_B)}
    delta = Decimal(b["total"]) - Decimal(a["total"])
    missing_regions = sorted(set(a["regions"]) - set(b["regions"]))
    steps, applied, previous = [], [], Decimal(a["total"])
    plan = [("category", "Category = Electronics (hypothesis from B's report name)", elements(CATEGORY, [ELECTRONICS]))]
    if missing_regions:
        names = ", ".join(a["regions"][i] for i in missing_regions)
        plan.append(("region", f"Region excludes {names} (observed: absent from B's returned rows)",
                     elements(REGION, missing_regions, "NotIn")))
    for field, description, view_filter in plan:
        applied.append(view_filter)
        variant = session.execute(REPORT_A, all_of(*applied))
        value = Decimal(variant["total"])
        steps.append(dict(field=field, change=description, result=variant, impact=str(value - previous),
                          residual=str(value - Decimal(b["total"]))))
        previous = value
        if value == Decimal(b["total"]):
            break
    explained = bool(steps) and Decimal(steps[-1]["residual"]) == 0 and all(r["complete"] for r in (a, b))
    unknowns = ["This shows which selections reproduce B numerically. It does not decide which definition is correct."]
    if not context["B"]["readable"]:
        unknowns.append("B's filter definition is not readable by the guest user, so the explanation is numerical, not a reading of B's definition.")
    return dict(kind="live-public-demo-check", checked_at=datetime.now(timezone.utc).isoformat(timespec="seconds"),
                server=session.base, project=session.project, login="guest (loginMode 8), read-only",
                originals=[a, b], context=context, delta=str(delta), steps=steps,
                status="demonstrated" if explained else "unresolved", unknowns=unknowns,
                cleanup=dict(instances_created=len(session.instances)))


if __name__ == "__main__":
    with Session() as live:
        receipt = run_check(live)
    receipt["cleanup"].update(logout_status=live.logout_status, calls=live.calls, requests=live.requests,
                              # Logout ends the session; instances are not deleted one by one.
                              instance_deletion="not attempted; instances end with the session",
                              writes_to_saved_objects=[r for r in live.requests if r.split()[0] in {"PUT", "PATCH", "DELETE"}
                                                       or (r.startswith("POST") and not r.endswith(("/instances", "/auth/login", "/auth/logout")))])
    print(json.dumps(receipt, indent=2))
