# POC acceptance receipt

Date: 2026-10-24. Artifact: `/home/rahil/projects/strategy-mismatch-investigator`, software 0.4.0. Source spec: RahilBhavan/main#41, revision 3. This receipt covers the functional synthetic POC plus one read-only check against Strategy's public demo server. It is not a customer-deployment integration or a customer outcome.

## Evidence mapping

- AC-1: runtime simulation banner, local contract page and exported packet label/live status; `test_static_app`, browser/screenshots and export inspection.
- AC-2: `test_boundary`, `test_intake_and_origin`; project/type/format, 100,001 rows and >20 MB rejected. Public case intake validates actual source data before computation.
- AC-3: `docs/ADAPTER.md`, `test_faults_and_retry_limit` and browser denial/expired states. On Strategy's public demo, the guest user's read of B's filter was refused (HTTP 500 with a read-access message) and the live check reported a numerical, not definitional, explanation. Customer-deployment authorization is not tested.
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
- AC-15: the same flow in Firefox 157, Chromium 156 and WebKit 27.2 at 320, 390, 768, 1120 and 1440 CSS pixels, no horizontal overflow; dedicated zero-pointer keyboard comparison, diagnostic, disclosure, both exports, source edit, cancel and denial/retry paths pass with visible focus; source/evidence panels and long values at 320px inspected. Controls freeze while a job runs; Cancel remains available.
- AC-16: dedicated keyboard run blocks all non-local requests from first navigation through comparison, diagnostic and both exports; app has no third-party runtime dependency. Fonts/scripts are local. Fixture data and exports are synthetic.
- AC-17: separate reviewer authored six unseen single-cause references, two equal controls and two ambiguous/incomplete controls, then exercised the public core interface. Ten in-scope outcomes match, with zero false explanations; an additional unsupported-calculation abstention passes. Reference scope correction and unexecuted counterfactual convention are disclosed in `REVIEW-R1.md`, not silently erased.
- AC-18: existing Test Center overlap and future reuse are recorded in `docs/ADAPTER.md`, the contract page and independent review. Customer usefulness and market uniqueness remain unverified.
- AC-19: canceled/failed/completed adapter instances all accounted for; per-adapter cleanup does not touch another attempt. Canceled jobs cannot later publish completed results. Live server cancellation/expiry remains not tested.

## Actual checks (0.4.0)

`python -m unittest discover -s tests -v`: 33 tests passed, including 11 separately authored tests and 3 offline tests of the live client. Full output: `tests.txt`.

Browser checks run against a private server with a throwaway database; none touches the 8807 demo. Firefox runs on this host. Chromium and WebKit run through `verification/run_matrix.sh` in Microsoft's Playwright Ubuntu image, because host Chromium never fires `requestAnimationFrame`. Firefox receipts keep their historical names; the others carry an engine suffix.

- `browser_check.py`: export/reopen, HTTP-server restart, amount-edit recalculation including the marked added record, negative states, one retry, cancellation, five widths, blocked external requests, keyboard focus and no page errors. `browser-checks*.json`.
- `keyboard_check.py`: complete keyboard workflow at 390px with zero pointer actions and no external requests. Asserts focus lands on the comparison heading after Compare and on the finding heading after the test, below the sticky banner, with the ledger on screen. `keyboard-checks*.json`.
- `layout_checks.py`: five widths, forced colors, reduced motion and a 320px stress case. Checks that no worksheet table is clipped and that totals wrap only at digit-group commas. `layout-checks*.json`.
- `contrast_audit.py`: WCAG text contrast for visible text nodes and form-control values in six states at 1280 and 390px, with translucency blended. Zero failures in all three engines. `contrast-audit*.json`. Hover/focus colours and non-text contrast are not measured.
- `motion_filmstrip.py`: normal-motion frames of the 180 ms result fade (opacity 0.5 → 0.74 → 0.92 → 1.0), sampled on the animation's own clock. `motion-filmstrip.json`, `r4-motion-*.png`.

The earlier `platform_check.py` and its `chromium-check.json` and `webkit-check.json` failures are superseded by the matrix receipts and removed; git history keeps them.

`python -m app.live`: read-only guest check on `demo.microstrategy.com`. A *Region Category* 35,023,708.15; B *Electronics Revenue by Region* 21,666,380.90. Category = Electronics leaves 2,724,921.95; also excluding Web leaves 0.00. Eight requests, four transient instances, no writes to saved objects, logout 204. `live-demo-check.json`.

Independent reviews: `REVIEW-R1.md` to `REVIEW-R4.md`. R4 scored 11/15 lines at 4 or above, none below 3, and found seven defects. All seven were fixed after R4 (control styling in the moved panel, per-report snapshot captions, clipped records table, mid-number wraps, checks writing into the demo database, stale docs and receipts, and conflicting live wording). R4 was the last round of the design skill's budget, so those fixes are **not rescored**; the design stop rule remains formally unmet.

## Limits and outcome

Functional POC outcome: supported computations, controlled status experiments, abstentions and the evidence workflow are exercised against synthetic records in three browser engines. The live check shows the same method works against one public Strategy build with real REST payloads. No real analyst pilot, customer deployment or hiring/commercial benefit is observed. Privileged access, SQL views, prompts, caching, large paging, instance deletion, native placement and production scale are not tested.

All engine runs are Linux headless. Safari on Apple hardware, Windows scaling and High Contrast, Android, physical devices and screen readers remain unverified. No desktop OS configuration was changed; Chromium and WebKit run inside a rootless container.
