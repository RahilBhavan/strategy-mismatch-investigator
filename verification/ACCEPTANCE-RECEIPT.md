# POC acceptance receipt

Date: 2026-10-25. Artifact: this repository, software 0.4.0. Source spec: `docs/SPEC.md`, revision 3 (planning issue #41 is in a private repository). This receipt covers the functional synthetic POC plus one read-only check against Strategy's public demo server. It is not a customer-deployment integration or a customer outcome.

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
- AC-15: the same flow in Firefox 157, Chromium 156 and WebKit 27.2 on Linux, and WebKit 27.2 on macOS 27.2, at 320, 390, 768, 1120 and 1440 CSS pixels, no horizontal overflow; dedicated zero-pointer keyboard comparison, diagnostic, disclosure, both exports, source edit, cancel and denial/retry paths pass with visible focus; source/evidence panels and long values at 320px inspected. Controls freeze while a job runs; Cancel remains available.
- AC-16: dedicated keyboard run blocks all non-local requests from first navigation through comparison, diagnostic and both exports; app has no third-party runtime dependency. Fonts/scripts are local. Fixture data and exports are synthetic.
- AC-17: separate reviewer authored six unseen single-cause references, two equal controls and two ambiguous/incomplete controls, then exercised the public core interface. Ten in-scope outcomes match, with zero false explanations; an additional unsupported-calculation abstention passes. Reference scope correction and unexecuted counterfactual convention are disclosed in `REVIEW-R1.md`, not silently erased.
- AC-18: existing Test Center overlap and future reuse are recorded in `docs/ADAPTER.md`, the contract page and independent review. Customer usefulness and market uniqueness remain unverified.
- AC-19: canceled/failed/completed adapter instances all accounted for; per-adapter cleanup does not touch another attempt. Canceled jobs cannot later publish completed results. Live server cancellation/expiry remains not tested.

## Actual checks (0.4.0, 2026-10-25)

`python -m unittest discover -s tests -v`: 33 tests passed, including 11 separately authored tests and 3 offline tests of the live client. Full output: `tests.txt`.

Browser checks run against a private server with a throwaway database; none touches the 8807 demo. Firefox runs on the Linux host. Chromium and WebKit run through `verification/run_matrix.sh` in Microsoft's Playwright Ubuntu image, because host Chromium never fires `requestAnimationFrame`. The same five checks also ran with Playwright's WebKit on a Mac (macOS 27.2) over SSH. The committed `-webkit-macos` receipts come from the revision just before the R6 follow-ups, where all five checks passed. On the final revision, the Mac's browser and keyboard checks passed too. The Mac then went to sleep before the other three ran and before those receipts were copied back. Firefox receipts keep their historical names; the others carry an `-chromium`, `-webkit` or `-webkit-macos` suffix. Every check below passes in every one of those runs.

- `browser_check.py`: export/reopen, HTTP-server restart, amount-edit recalculation including the marked added record, negative states, one retry, cancellation, five widths, blocked external requests, keyboard focus and no page errors. `browser-checks*.json`.
- `keyboard_check.py`: complete keyboard workflow at 390px with zero pointer actions and no external requests. Asserts focus lands on the comparison heading after Compare and on the finding heading after the test, below the sticky banner, with the ledger on screen. `keyboard-checks*.json`.
- `layout_checks.py`: five widths, forced colors, reduced motion and a 320px stress case. Checks that no worksheet table is clipped and that totals wrap only at digit-group commas. `layout-checks*.json`.
- `contrast_audit.py`: WCAG text contrast for visible text nodes and form-control values in six states at 1280 and 390px, with translucency blended. Zero failures in every run. `contrast-audit*.json`. Hover/focus colours and non-text contrast are not measured.
- `assistive_check.py` (new): axe-core 4.14.0 WCAG 2.0–2.2 A/AA rules in five states (start, compared, finding, evidence open, denied): no violations in any engine. axe leaves colour contrast "incomplete" where backgrounds are layered; `contrast_audit.py` covers it. It saves the accessibility tree (`a11y-tree*.txt`). On emulated iPhone 15 (WebKit) and Pixel 7 (Chromium) it taps through the flow: the answer takes focus with the ledger on screen, there is no sideways scroll, and all 22 visible targets are at least 44 px tall. In Chromium's emulated forced colours, ledger rules, the double total rule, "Differs" marks, button borders and the focus outline remain. `assistive-checks*.json`, `r5-touch-finding-*.png`, `r5-forced-colors-390-chromium.png`.
- `motion_filmstrip.py`: normal-motion frames of the 180 ms result fade (opacity 0.5 → 0.74 → 0.92 → 1.0), sampled on the animation's own clock. `motion-filmstrip.json`, `r4-motion-*.png`.

The earlier `platform_check.py` and its `chromium-check.json` and `webkit-check.json` failures are superseded by the matrix receipts and removed; git history keeps them.

`python -m app.live`: read-only guest check on `demo.microstrategy.com`. A *Region Category* 35,023,708.15; B *Electronics Revenue by Region* 21,666,380.90. Category = Electronics leaves 2,724,921.95; also excluding Web leaves 0.00. Eight requests, four transient instances, no writes to saved objects, logout 204. `live-demo-check.json`.

Defects these checks found and fixed on 2026-10-25:
- Phone touch targets: the header link and both file pickers were 19–20 px tall. All three are now 44 px.
- Safari on macOS ignored the 44 px height on menus. They are now drawn by the app, with the native control restored under forced colours.
- Safari's default keyboard model reaches buttons only with Option+Tab, and closed menus ignore Home/End there. The checks now follow that model.
- Chromium screenshots showed the sticky banner across mid-page. The app's CSP blocked the injected capture style, so captures now scroll to the top instead.

Independent reviews: `REVIEW-R1.md` to `REVIEW-R6.md`. R4 scored 11/15 lines at 4 or above. R5, authorized beyond the design skill's four-round budget, rescored the R4 fixes at 12/15. It held the stop rule unmet because Depth and finish stayed at 3, and listed nine smaller defects. All nine, plus the evidence-panel grouping R5 asked for, were addressed before R6. R6 scored 14/15 lines at 4 or above, with Signature at 3 and none below 3, so **the design stop rule is met**. R6 then found five low defects plus trivial notes: evidence sub-headings larger than the panel heading, half-width export buttons on phones, the finding's label hidden under the banner after a test on phones, a "units differ" caption when a unit was missing, and stale limits text. All were fixed once and are **not rescored**, as the skill's after-done rule says.

## Limits and outcome

Functional POC outcome: supported computations, controlled status experiments, abstentions and the evidence workflow are exercised against synthetic records in three browser engines. The live check shows the same method works against one public Strategy build with real REST payloads. No real analyst pilot, customer deployment or hiring/commercial benefit is observed. Privileged access, SQL views, prompts, caching, large paging, instance deletion, native placement and production scale are not tested.

All engine runs are headless: Firefox, Chromium and WebKit on Linux, and Playwright's WebKit build on macOS. Real Safari was not driven, because its remote-automation setting is off and needs the owner's password. VoiceOver was not run either, because the Mac's screen-recording permission is not granted. Windows scaling and High Contrast, physical phones and screen readers remain unverified; touch and forced colours are emulations only. No OS setting was changed. [`docs/MANUAL-CHECKS.md`](../docs/MANUAL-CHECKS.md) gives the steps for each, plus a 20-minute session script for a Strategy user.
