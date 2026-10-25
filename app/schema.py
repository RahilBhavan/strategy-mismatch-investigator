"""The only intake boundary; immutable case values use exact decimal strings."""
import hashlib
import json
from decimal import Decimal, InvalidOperation

LABEL = "Proof of concept — simulated Strategy connection"
VERSION = "0.4.0"
MAX_BYTES = 20 * 1024 * 1024
MAX_ROWS = 100_000
MAX_MINOR = 2**63 - 1


class CaseError(ValueError):
    def __init__(self, message, field="case", code="invalid"):
        super().__init__(message)
        self.field, self.code = field, code


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False)


def fingerprint(value):
    return hashlib.sha256(canonical(value).encode()).hexdigest()


def text(value, field, empty=False):
    if not isinstance(value, str) or len(value) > 500 or (not empty and not value.strip()):
        raise CaseError("Provide a text value of 1–500 characters.", field)
    return value


def minor(value, scale):
    if value is None:
        return None
    if not isinstance(value, str) or len(value) > 50:
        raise CaseError("Amounts must be decimal strings or null.", "records.amount")
    try:
        amount = Decimal(value)
        scaled = amount * 10**scale
        if not amount.is_finite() or scaled != scaled.to_integral_value():
            raise CaseError("Amount exceeds the declared decimal scale.", "records.amount")
        result = int(scaled)
    except (InvalidOperation, ValueError, OverflowError) as error:
        raise CaseError("Provide a finite exact decimal amount.", "records.amount") from error
    if abs(result) > MAX_MINOR:
        raise CaseError("Amount exceeds the supported integer range.", "records.amount", "overflow")
    return result


def display(value, scale):
    if value is None:
        return None
    sign = "-" if value < 0 else ""
    value = abs(value)
    if not scale:
        return f"{sign}{value}"
    unit = 10**scale
    return f"{sign}{value // unit}.{value % unit:0{scale}d}"


def validate_case(value):
    if not isinstance(value, dict):
        raise CaseError("Provide a case object.")
    try:
        size = len(canonical(value).encode())
    except (ValueError, TypeError) as error:
        raise CaseError("Provide a finite JSON case.") from error
    if size > MAX_BYTES:
        raise CaseError("Case exceeds 20 MB.")
    if set(value) != {"schema_version", "synthetic", "name", "records", "reports"}:
        raise CaseError("Case fields do not match synthetic-case-v1.")
    if value["schema_version"] != "synthetic-case-v1" or value["synthetic"] is not True:
        raise CaseError("Only declared synthetic-case-v1 examples are accepted.")
    text(value["name"], "name")
    rows, reports = value["records"], value["reports"]
    if not isinstance(rows, list) or len(rows) > MAX_ROWS:
        raise CaseError("A case may contain at most 100,000 records.", "records")
    if not isinstance(reports, list) or len(reports) != 2:
        raise CaseError("Choose exactly two reports.", "reports")
    for index, report in enumerate(reports):
        path = f"reports.{index}"
        fields = {"id", "name", "project", "type", "metric", "definition", "unit", "scale", "grain", "snapshot", "filters", "complete"}
        if not isinstance(report, dict) or set(report) != fields:
            raise CaseError("Report fields do not match the evidence contract.", path)
        for key in ("id", "name", "project", "metric", "definition"):
            text(report[key], f"{path}.{key}")
        for key in ("unit", "grain", "snapshot"):
            text(report[key], f"{path}.{key}", empty=True)
        if report["type"] != "grid":
            raise CaseError("This report type is outside the first-release scope.", path, "unsupported")
        if type(report["scale"]) is not int or not 0 <= report["scale"] <= 6:
            raise CaseError("Scale must be an integer from 0 to 6.", path)
        if type(report["complete"]) is not bool:
            raise CaseError("Declare result completeness.", path)
        filters = report["filters"]
        if not isinstance(filters, dict) or set(filters) != {"status", "region"}:
            raise CaseError("Provide status and region selections.", f"{path}.filters")
        for key, choices in filters.items():
            if choices is not None and (not isinstance(choices, list) or len(choices) > 50):
                raise CaseError("A selection is null or a list of at most 50 values.", path)
            if choices is not None:
                for choice in choices:
                    text(choice, f"{path}.filters.{key}")
    if reports[0]["project"] != reports[1]["project"]:
        raise CaseError("Choose reports in the same project.", "reports", "different_project")
    if reports[0]["id"] == reports[1]["id"]:
        raise CaseError("Report references must have distinct IDs.", "reports")
    ids = set()
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"id", "amount", "status", "region"}:
            raise CaseError("Each record needs id, amount, status and region.", "records")
        for key in ("id", "status", "region"):
            text(row[key], f"records.{key}")
        if row["id"] in ids:
            raise CaseError("Record IDs must be unique.", "records.id")
        ids.add(row["id"])
        for report in reports:
            minor(row["amount"], report["scale"])
    return json.loads(canonical(value))
