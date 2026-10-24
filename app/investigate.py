"""Deterministic reasoning over captured evidence, never hidden network requests."""
from copy import deepcopy
from .schema import LABEL, VERSION, display, fingerprint


def normalized(value):
    return None if value is None else sorted(set(value))


def investigate(case, adapter, phase="compare"):
    a, b = case["reports"]
    result = dict(label=LABEL, live_connection="not tested", software_version=VERSION,
                  case_fingerprint=fingerprint(case), phase=phase, originals=[], differences=[],
                  experiment=None, delta=None, percent_delta=None, residual=None, unknowns=[],
                  status="unresolved", summary="Not enough evidence to explain this difference.")
    for key in ("metric", "definition", "unit", "scale", "grain", "snapshot"):
        if a[key] != b[key] or a[key] == "":
            result["unknowns"].append(f"Different or missing {key}: a comparable context is not established.")
    for key in ("status", "region"):
        if normalized(a["filters"][key]) != normalized(b["filters"][key]):
            result["differences"].append(dict(field=key, a=a["filters"][key], b=b["filters"][key], status="candidate"))
    # Never manufacture results for an unsupported calculation.
    if a["definition"] != "SUM(amount)" or b["definition"] != "SUM(amount)":
        result["unknowns"].append("This calculation is outside the supported SUM(amount) scope.")
        return result
    result["originals"] = [adapter.execute(a), adapter.execute(b)]
    if any(not original["complete"] for original in result["originals"]):
        result["unknowns"].append("A captured result is incomplete. A page is not a report total.")
    first, second = result["originals"]
    if first["minor"] is None or second["minor"] is None:
        result["unknowns"].append("An aggregate is null; no numerical difference can be established.")
    if result["unknowns"]:
        result["summary"] = "Not enough evidence to compare these totals."
        return result
    delta = int(second["minor"]) - int(first["minor"])
    result["delta"] = display(delta, a["scale"])
    if int(first["minor"]) != 0:
        from decimal import Decimal
        result["percent_delta"] = str((Decimal(delta) * 100 / Decimal(first["minor"])).quantize(Decimal("0.01")))
    if delta == 0:
        result.update(status="equal", summary="No numerical difference in these captured results.")
        result["unknowns"].append("Equal totals do not establish equivalent business definitions.")
        return result
    if len(result["differences"]) != 1 or result["differences"][0]["field"] != "status":
        result["unknowns"].append("Status and region both differ. This status-only experiment cannot isolate their effects." if len(result["differences"]) > 1 else "This difference is outside the supported status-selection experiment.")
        return result
    result.update(status="candidate", summary="The status selections differ. Test whether that selection explains the gap.")
    if phase == "compare":
        return result
    # Re-run B with only A's runtime status selection. Saved definitions remain untouched.
    variant = adapter.execute(b, {"status": deepcopy(a["filters"]["status"])})
    if not variant["complete"] or variant["minor"] is None:
        result["unknowns"].append("The diagnostic result is incomplete or null.")
        result.update(status="unresolved", summary="Not enough evidence to explain this difference.")
        return result
    impact = int(variant["minor"]) - int(second["minor"])
    residual = int(variant["minor"]) - int(first["minor"])
    result["experiment"] = dict(changed_field="status", before=b["filters"]["status"],
                                after=a["filters"]["status"], result=variant,
                                impact=display(impact, a["scale"]), unchanged_fields=["region", "metric", "snapshot", "grain", "unit"])
    result["residual"] = display(residual, a["scale"])
    if residual == 0:
        result.update(status="demonstrated", summary=f"Rerunning B with A’s status selection changes {second['total']} to {variant['total']}. The remaining difference from A is {display(residual, a['scale'])}.")
        result["differences"][0]["status"] = "numerical cause demonstrated on synthetic data"
        result["unknowns"].append("This does not decide which status selection matches the intended business definition.")
    else:
        result.update(status="unresolved", summary="The selection does not explain the full measured difference.")
    return result
