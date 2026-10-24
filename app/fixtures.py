"""Locally authored fixtures. No responses were captured from a live service."""
from copy import deepcopy


def example():
    report = dict(id="sales-overview", name="Sales overview", project="synthetic-retail", type="grid",
                  metric="order-amount", definition="SUM(amount)", unit="illustrative units", scale=2,
                  grain="order", snapshot="synthetic-orders-v1", filters={"status": None, "region": None}, complete=True)
    second = deepcopy(report)
    second.update(id="finance-review", name="Finance review", filters={"status": ["paid"], "region": None})
    return dict(schema_version="synthetic-case-v1", synthetic=True, name="Status selection",
                records=[dict(id="order-1", amount="100.00", status="paid", region="East"),
                         dict(id="order-2", amount="40.00", status="refunded", region="East"),
                         dict(id="order-3", amount="60.00", status="paid", region="West"),
                         dict(id="order-4", amount="20.00", status="paid", region="West")],
                reports=[report, second])


def examples():
    base = example()
    equal = deepcopy(base)
    equal["name"] = "Equal results"
    equal["reports"][1]["filters"]["status"] = None
    snapshot = deepcopy(base)
    snapshot["name"] = "Different snapshots"
    snapshot["reports"][1]["snapshot"] = "synthetic-orders-v2"
    ambiguous = deepcopy(base)
    ambiguous["name"] = "Two selections differ"
    ambiguous["reports"][1]["filters"]["region"] = ["West"]
    missing = deepcopy(base)
    missing["name"] = "Missing metric context"
    missing["reports"][1]["unit"] = ""
    null = deepcopy(base)
    null["name"] = "No known amounts"
    for row in null["records"]:
        row["amount"] = None
    return {"status": base, "equal": equal, "snapshots": snapshot, "ambiguous": ambiguous, "missing": missing, "null": null}
