# POC acceptance receipt

Date: 2026-10-24. Artifact: this repository, software 0.3.0. Source spec: `docs/SPEC.md`, revision 3 (planning issue #41 is in a private repository). This receipt covers the functional synthetic POC, not a live Strategy integration or customer outcome.

## Evidence mapping

- AC-1: runtime simulation banner, local contract page and exported packet label/live status; `test_static_app`, browser/screenshots and export inspection.
- AC-2: `test_boundary`, `test_intake_and_origin`; project/type/format, 100,001 rows and >20 MB rejected. Public case intake validates actual source data before computation.
- AC-3: `docs/ADAPTER.md`, `test_faults_and_retry_limit` and browser denial/expired states. Actual enterprise authorization is not tested.
- AC-4: `test_record_backed_experiment_and_no_mutation`; browser starts with 220/180, edits refunded amount to 15 and obtains 195/180.
- AC-5: the original diagnostic yields impact 40/residual 0; changed amount yields impact 15/residual 0. Independent reverse, negative, fractional and novel-status tests also pass.
- AC-6: context evidence panels and `test_context_controls`; absent units, differing snapshots and different metric IDs block definitive explanation.
- AC-7: before/after case fingerprints in core/independent tests; transient selection execution uses deep-copied filters and never writes original definitions.
- AC-8: conflicting and missing contexts in core/HTTP/browser controls. A timestamp is not substituted for a source snapshot.
- AC-9: identical and coincidentally equal controls; no semantic-equivalence label. Reviewer supplement corrects an initially out-of-scope reference, preserved transparently in `REVIEW-R1.md`.
- AC-10: core ambiguous fixture produces status and region candidates with unresolved status; revised finding displays both. No overlapping additive impact or fabricated diagnostic is shown.
- AC-11: comparison-only candidate, completed synthetic diagnostic and unresolved/null/incomplete results tested. UI, packet and contract distinguish synthetic proof from live checks.
- AC-12: exact large decimals, negative values, zero baseline, null aggregates, overflow and incomplete-result marker tests. This is not actual Strategy pagination verification.
- AC-13: injected timeout/error/denial/expiry and transient/rate-limit retry tests plus browser failure states. Deadline checking is exercised independently. Injected Retry-After is 50 ms; at most one automatic retry, none for denial.
- AC-14: HTTP-server stop/start then URL reopen, JSON export/import recomputation, stale-source removal, idempotent resubmission and software-version invalidation. Tampered packet hash and fabricated rehashed conclusions are rejected.
- AC-15: actual Firefox flow at 320, 390, 768, 1120 and 1440 CSS pixels, no horizontal overflow; dedicated zero-pointer keyboard comparison, diagnostic, disclosure, both exports, source edit, cancel and denial/retry paths pass with visible focus; source/evidence panels and long values at 320px inspected. Controls freeze while a job runs; Cancel remains available.
- AC-16: dedicated keyboard run blocks all non-local requests from first navigation through comparison, diagnostic and both exports; app has no third-party runtime dependency. Fonts/scripts are local. Fixture data and exports are synthetic.
- AC-17: separate reviewer authored six unseen single-cause references, two equal controls and two ambiguous/incomplete controls, then exercised the public core interface. Ten in-scope outcomes match, with zero false explanations; an additional unsupported-calculation abstention passes. Reference scope correction and unexecuted counterfactual convention are disclosed in `REVIEW-R1.md`, not silently erased.
- AC-18: existing Test Center overlap and future reuse are recorded in `docs/ADAPTER.md`, the contract page and independent review. Customer usefulness and market uniqueness remain unverified.
- AC-19: canceled/failed/completed adapter instances all accounted for; per-adapter cleanup does not touch another attempt. Canceled jobs cannot later publish completed results. Live server cancellation/expiry remains not tested.

## Actual checks

`python -m unittest discover -s tests -v`: 30 tests passed, including 11 separately authored tests. Full output: `tests.txt`.

`verification/browser_check.py`: isolated HTTP server and disposable DB; JSON/readable export, restart/reopen, amount-edit recalculation, negative states, one retry, cancellation, five widths, offline external dependency check, keyboard focus and no page errors. Receipt: `browser-checks.json`.

`verification/layout_checks.py`: additional long-name/unit/large-exact-number stress at 320px with evidence opened, forced-colors and reduced-motion checks. Receipt: `layout-checks.json`. These are Linux browser/emulation checks, not physical Windows/device proof.

`verification/keyboard_check.py`: complete keyboard workflow at 390px, zero pointer actions and no external requests. Receipt: `keyboard-checks.json`. Measured quantitative text contrast is at least 7.14:1 (`contrast-measurements.json`); forced-color focus and reduced-motion properties are in `media-checks.json`. These are measured properties, not screen-reader or physical-device approval.

Independent reviews: `REVIEW-R1.md`, `REVIEW-R2.md`; `REVIEW-R3.md` is the final current-version review: reviewer independently reran 30 tests successfully and found no material functional blocker. The review read stale acceptance headers during concurrent edits; those headers and this criterion mapping now identify 0.3.0. Design remains 9/15 at 4+, none below 3; the design stop rule is not met. This is functional POC acceptance, not full design/platform approval. Original r1 filenames were regenerated during iterative smoke checks; round 2 uses stable r2-named renders and round 3 uses stable r3-named renders. R1 prose preserves the historical findings rather than claiming its original pixels remained frozen.

## Limits and outcome

Functional POC outcome: supported computations, controlled status experiments, abstentions and evidence workflow are exercised against synthetic records. No real analyst pilot or hiring/commercial benefit is observed. Live Strategy connectivity, permissions, API payload compatibility, native placement, server cleanup, production scale and real-data handling are not tested.

Firefox is exercised. Chromium stalls at the click stability check; it is unverified. WebKit fails to launch because `libicudata.so.74` is unavailable; Safari is unverified. T3 collaborative preview is blocked by its server tab limit and lists no reusable thread tabs. The final inline HTML preview separately timed out after 20 seconds in headless Chrome; the supplied app screenshots were inspected from the successful Firefox runs. No desktop OS configuration was changed to work around these limits.
