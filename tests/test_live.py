import json
import unittest
from app import live

WEB = f"h12;{live.REGION}"
EAST = f"h1;{live.REGION}"
BOOKS = f"h1;{live.CATEGORY}"
# (category, region, revenue): Web sells only electronics; B hides Web behind an unreadable filter.
FACTS = [(live.ELECTRONICS, EAST, 0.1), (live.ELECTRONICS, WEB, 0.2), (BOOKS, EAST, 5.0), (BOOKS, WEB, 7.0)]


def keep(fact, view_filter):
    if view_filter is None:
        return True
    if view_filter["operator"] == "And":
        return all(keep(fact, f) for f in view_filter["operands"])
    attribute, chosen = view_filter["operands"][0]["id"], {e["id"] for e in view_filter["operands"][1]["elements"]}
    value = fact[0] if attribute == live.CATEGORY else fact[1]
    return (value in chosen) == (view_filter["operator"] == "In")


class FakeLibrary:
    def __init__(self, expire_after=None):
        self.log, self.expire_after, self.executions = [], expire_after, 0

    def __call__(self, method, url, headers, body):
        path = url.split("/api", 1)[1]
        self.log.append((method, path, headers.get("X-MSTR-AuthToken")))
        payload = json.loads(body) if body else {}
        if path == "/auth/login":
            return 204, {"X-MSTR-AuthToken": "t0"}, b""
        if path == "/auth/logout":
            return 204, {}, b""
        if path.startswith("/model/reports/"):
            if live.REPORT_B in path:
                return 500, {}, b'{"errors":[{"message":"User does not have Read access"}]}'
            return 200, {}, b'{"dataSource":{}}'
        self.executions += 1
        if self.expire_after is not None and self.executions > self.expire_after:
            return 401, {}, b'{"message":"The user\'s session has expired"}'
        b_report = live.REPORT_B in path
        facts = [f for f in FACTS if keep(f, payload.get("viewFilter"))
                 and (not b_report or (f[0] == live.ELECTRONICS and f[1] != WEB))]
        regions = sorted({f[1] for f in facts})
        # B is a crosstab with two metrics, so the Revenue column must be picked out of each row.
        raw = [[sum(f[2] for f in facts if f[1] == r), 99] for r in regions]
        body = {"name": "B" if b_report else "A", "instanceId": f"i{self.executions}",
                "definition": {"grid": {"rows": [{"id": live.REGION, "elements": [{"id": r, "formValues": [r]} for r in regions]}],
                                        "columns": [{"type": "templateMetrics", "elements": [{"id": live.REVENUE}, {"id": "other"}]}]}},
                "data": {"paging": {"current": len(raw), "total": len(raw)}, "metricValues": {"raw": raw}}}
        return 200, {}, json.dumps(body).encode()


class LiveCheckTests(unittest.TestCase):
    def test_reproduces_b_by_rerunning_a_with_its_selections(self):
        fake = FakeLibrary()
        with live.Session(fake) as session:
            receipt = live.run_check(session)
        self.assertEqual([o["total"] for o in receipt["originals"]], ["12.30", "0.10"])
        self.assertEqual([(s["field"], s["result"]["total"], s["residual"]) for s in receipt["steps"]],
                         [("category", "0.30", "0.20"), ("region", "0.10", "0.00")])
        self.assertEqual(receipt["status"], "demonstrated")
        # Doubles 0.1 + 0.2 must not surface as 0.30000000000000004 in the evidence.
        self.assertEqual(receipt["steps"][0]["result"]["unrounded"], "0.3")
        self.assertFalse(receipt["context"]["B"]["readable"])
        self.assertTrue(any("not readable" in u for u in receipt["unknowns"]))
        self.assertEqual(fake.log[-1][:2], ("POST", "/auth/logout"))

    def test_session_failure_still_logs_out_and_reports_no_conclusion(self):
        fake = FakeLibrary(expire_after=2)
        with self.assertRaises(live.LiveFailure) as caught:
            with live.Session(fake) as session:
                live.run_check(session)
        self.assertEqual(caught.exception.status, 401)
        self.assertEqual(fake.log[-1][:2], ("POST", "/auth/logout"))

    def test_refused_login_raises(self):
        with self.assertRaises(live.LiveFailure):
            with live.Session(lambda *a: (401, {}, b'{"message":"no guest"}')):
                pass


if __name__ == "__main__":
    unittest.main()
