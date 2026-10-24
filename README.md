# Strategy number mismatch investigator

A working proof of concept for explaining a prompt/filter difference between two report totals. **Synthetic records and a simulated Strategy adapter only. Live Strategy integration is not tested.** This is an independent demonstration, not an official product or installed extension.

## Run

Python 3.11+; the application has no third-party dependencies.

```bash
cd /home/rahil/projects/strategy-mismatch-investigator
python -m app.server --port 8807
```

Open http://127.0.0.1:8807. The default local SQLite database is `.local/demo.sqlite3` and is ignored by Git. Override it with `--db /path/to/scratch.sqlite3` for an isolated instance. Do not use Orbit's port or database.

1. Choose the Status selection example and click **Compare totals**: A is 220, B is 180.
2. Click **Test the status selection**: only the transient B status changes; B becomes 220, measured impact is 40 and remaining difference is 0.
3. Inspect the context, computation and source records. The original definitions stay unchanged.
4. Change the refunded amount under Source & test controls, then rerun. The evidence changes with the data.
5. Try Different snapshots or Two selections differ: the feature abstains rather than inventing a cause.
6. Export JSON/readable HTML. Reopen JSON to validate its source and recompute its arithmetic. Reloading a saved `?case=...&job=...` URL also reopens persisted evidence.

Values are illustrative units, not money. A numerical explanation does not decide which business definition is correct. Default examples are editable; use a separate `--db` to restore pristine examples without deleting any existing evidence.

## Verify

```bash
python -m unittest discover -s tests -v
```

The app tests exercise its public computation/HTTP interfaces, cancellation, stale input, exact decimal arithmetic, boundaries, restart and tampered packets. Browser checks are in `verification/browser_check.py` and require a local Playwright/Firefox installation; this is a verification-only dependency, not a runtime dependency. They use an isolated server and disposable DB.

## Files and boundaries

- `app/schema.py`: input validation, exact quantities and content fingerprints.
- `app/adapter.py`: synthetic report computation, retry, cancellation and instance accounting.
- `app/investigate.py`: deterministic comparison and controlled-experiment reasoning.
- `app/store.py`: local case/job persistence and validated evidence reopen.
- `app/server.py`: local HTTP boundary and static asset serving.
- `web/`: offline Inter font, comparison UI, readable evidence export and contract page.
- `docs/ADAPTER.md`: documented inspiration versus locally designed contract fields.
- `docs/ACCEPTANCE.md`, `verification/`: criteria and observed checks, with untested live behavior kept separate.

Verification and limits: [acceptance receipt](verification/ACCEPTANCE-RECEIPT.md), [final independent critique](verification/REVIEW-R3.md). Firefox/Linux and responsive emulations were exercised; Chromium, WebKit, real devices and screen readers remain unverified. Functional synthetic checks do not establish live integration or portfolio-level design approval.

The source spec and issue are [RahilBhavan/main#41](https://github.com/RahilBhavan/main/issues/41). No account signup, production access, direct warehouse queries, publishing, automatic report edits or scheduled jobs are included.
