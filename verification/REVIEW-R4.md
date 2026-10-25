# Independent critique — round 4

Reviewed 2026-10-24 against revision 4 of the approved synthetic Strategy integration POC, software 0.4.0. **All five R3 follow-ups landed in some form. The reconciliation ledger is the strongest change in four rounds. The live public-demo check reproduces exactly and is honestly framed. Round 4 also introduced one visible styling regression and exposed three craft defects that the layout checks cannot detect. Score: 11/15 lines at 4 or above; four lines at 3; none below 3. Not done by the stop rule: Depth and finish stays at 3 and Craft drops to 3.** This is round 4 of the skill's four-round budget, so these are the honest final scores. A fifth rescoring round would go beyond that budget.

## Method and evidence authority

I read DIRECTION.md, docs/SPEC.md, docs/ACCEPTANCE.md, docs/ADAPTER.md, README.md, REVIEW-R3.md and ACCEPTANCE-RECEIPT.md. I also read Web Designer Pro's `references/critique.md`, which provides the 15 lines and stop rule. As in R3, I kept the approved Inter, #FA660F and neutral light worksheet identity and did not judge it against a different brand.

**Actually rerun:**
- `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v`: **33 tests passed in 3.865 s**. That is 30 earlier tests plus 3 in `tests/test_live.py`.
- `python -m app.live`, run once (guest login, read-only, network). Output went to `~/scratch/smi-r4/live-rerun.json`; the receipt was not overwritten. **The output matches `verification/live-demo-check.json` in every computed field:**
  - A = 35,023,708.15 (32 cells, complete) and B = 21,666,380.90 (21 cells, complete), so delta = −13,357,327.25.
  - Category = Electronics gives 24,391,302.85, leaving a residual of 2,724,921.95. Also excluding Web gives 21,666,380.90, leaving 0.00.
  - The same guest Read-access refusal on B's filter returns HTTP 500.
  - 4 instances, 8 calls, logout 204, status `demonstrated`.
  - Only `checked_at` differs (21:23:11Z vs 21:37:37Z).
- Read-only `sqlite3` queries and one `GET /api/catalog` against the 8807 demo, used to confirm the database pollution defect below. Nothing was written.

**Opened at original resolution:**
- r4-demonstrated at 1440, 1120, 768, 390 and 320; r4-candidate-1440; r4-ambiguous-1440; r4-unresolved-390; r4-equal-1440; r4-missing-1440; r4-snapshots-1440; r4-high-contrast-390; r4-motion-0ms.
- r4-stress-320, including full-resolution crops of its totals and its source-record table.
- r4-demonstrated-390-webkit and r4-demonstrated-1440-chromium.
- Not opened individually: r4-reduced-motion-390 and the remaining motion frames. For those I relied on the per-frame opacities recorded in motion-filmstrip.json (0.5 → 0.744 → 0.922 → 1.0).

**Read, not rerun:**
- Sources: `app/live.py`, `tests/test_live.py`, `verification/contrast_audit.py`, `motion_filmstrip.py`, `keyboard_check.py`, `layout_checks.py`, `engine.py` and `run_matrix.sh`.
- The relevant parts of `web/index.html`, `web/view.js`, `web/evidence.js`, `web/style.css` and `web/contract.html`.
- Every `*-chromium.json` and `*-webkit.json` receipt.

I launched no browser and ran no Playwright or container job. The Chromium and WebKit results are therefore receipt-backed, not independently reproduced. I did not verify the stated reason Chromium fails on the host (requestAnimationFrame never firing). Only this file was written.

## R3 follow-ups

1. **Move the secondary disclosures after the active worksheet: landed, with a regression.**
   - What landed: in the DOM, `aside.secondary-tools` now comes after `section#workspace`. At 390 and 320, "Source & test controls" and "Continue a review" sit below the worksheet and above the footer, in Firefox and in WebKit. At 390 the worksheet heading now starts about 630 CSS px down; in R3 it started at about 790. Report A/B are now a paired row.
   - Regression: the move took these controls out of `.setup`. The only form-control rules are `.setup label`, `.setup select` and `.setup input[type=text]` (`web/style.css` line 3), and they no longer apply. When expanded, `#amount` and `#condition` show browser-default styling, roughly 24 px high instead of the 44 px minimum. Their labels lose block display, the 13 px/500 weight and the spacing. This is visible in r4-ambiguous, r4-snapshots, r4-equal and r4-missing at 1440: a grey native select, a hairline input and labels pressed against fields, all directly under carefully styled 44 px setup controls.
2. **Compose B original → variant → residual as one unit: landed.** The ledger reads: B as captured 180 → "With A's status selection: All values +40 / Adds order-2 (refunded, 40)" → B rerun 220 → A as captured 220 → double rule → Remaining difference 0. It is consistent at 1440, 1120, 768, 390 and 320 and in the Chromium and WebKit renders. The sub-line names the record, which answers R3's imagery route.
3. **Compact A/B context comparison: landed.** "Inspect report context" is now a Field/A/B table with "Differs" marks (visible in r4-stress-320). Source records mark the row the test adds.
4. **Remove the redundant unresolved prose: landed.** The ambiguous finding goes from the heading to the two selection rows to the one precise bullet. Minus signs are real (−40, −18.18%, −140).
5. **Focus and position evidence, normal-motion filmstrip, capture anomaly: mostly landed.**
   - Landed: `keyboard_check.py` now asserts `finding-title` focus, top ≥ banner bottom, bottom ≤ viewport and ledger top < innerHeight. All three engines record pass, with the finding top at about 96 px. Caveat: the viewport is 390×1000, which is taller than a real phone browser viewport.
   - Landed: the filmstrip seeks the paused animation's own clock, which is more honest than guessing wall-clock offsets.
   - Not fixed: **the sticky-banner capture anomaly R3 asked to repair is still present.** It appears in r4-ambiguous-1440, r4-snapshots-1440, r4-equal-1440, r4-missing-1440, r4-unresolved-390 and r4-demonstrated-1440-chromium. In each, the banner cuts mid-page across the scenario select and the worksheet's "Captured report / Total" header. These captures cannot serve as layout proof for the covered region.

## New defects, with evidence

1. **Regression: the expanded secondary controls lost their styling.** See follow-up 1. Fix: change the selectors to `.setup label, .secondary-tools label`, `.secondary-tools select`, `.secondary-tools input[type=text]` (or a shared class). File: `web/style.css`, line 3. The regression is identical across engines. Nothing catches it: no check measures control size after `.tools` is opened.
2. **Wrong snapshot caption in the Different snapshots state.** `web/view.js` line 40 renders `Snapshot: ${reports[0].snapshot}` under both totals. In r4-snapshots-1440 the caption says "Snapshot: synthetic-orders-v1", but B's fixture is `synthetic-orders-v2` (`app/fixtures.py` line 26), and the finding below says "Different or missing snapshot". The main evidence surface therefore shows a shared context that does not exist. The readable export repeats the same pattern (`web/evidence.js` line 16, `p.case.reports[0].snapshot`). The missing-unit state has a milder version: the caption still says "Illustrative values" while B reads "Unit not provided".
3. **Amount column clipped at 320, hidden from the overflow check.** In r4-stress-320, the expanded source-record table runs past the card. The header reads "Amo" and the large amount `90071992547409.93` is cut off at the card edge. The cause is `.worksheet{overflow:hidden}` together with a `.record-table` that has no scroll wrapper. `layout_checks.py` asserts `documentElement.scrollWidth <= innerWidth` and passes because the overflow is clipped, not scrolled. The check cannot see this kind of failure.
4. **Totals break mid-number at 320.** `.report-table .amount{overflow-wrap:anywhere}` turns 90,071,992,547,529.93 into "90,07 / 1,992 / ,547, / 529.9 / 3" across five lines, and the unit into "deliberatel / y". This is synthetic stress input, but a total that breaks across digit groups cannot be read as a number. A smaller size or a break only after group separators would fix it.
5. **The verification scripts write into the 8807 demo database.** `layout_checks.py` POSTs a stress case to `http://127.0.0.1:8807/api/cases` on every run. `keyboard_check.py` edits and restores a source amount. `contrast_audit.py` and `motion_filmstrip.py` create jobs. `run_matrix.sh` targets 8807 too. Read-only evidence:
   - `GET /api/catalog` now returns six identical "Long values and definitions" entries after the six built-in examples. They appear in the demo's Example investigation picker, because `store.cases()` lists every row.
   - The demo database holds 21 denied/failed and 7 slow/canceled jobs.

   Only `browser_check.py` uses its own server and temporary database. The comment "a separate synthetic source, not saved example edits" is true of the case, not of the database. Fix: start an isolated server with a scratch `--db` (as `browser_check.py` does), or at least reuse one stress case id.
6. **Documentation and receipts disagree with each other (parent-owned reconciliation).**
   - README says Firefox, Chromium and WebKit pass and links this file.
   - `ACCEPTANCE-RECEIPT.md` still says software 0.3.0, Chromium unverified and WebKit failing to launch.
   - `chromium-check.json` and `webkit-check.json` (17:32) still record host "unverified" results next to passing container receipts.
   - `docs/ACCEPTANCE.md` line 31 says "No current live receipt … exists", but `live-demo-check.json` now exists. It should be described as a public-demo check, not as the optional live receipt: it used view filters rather than prompts and performed no explicit instance cleanup.
7. **Copy: the live-status wording conflicts.** The banner says "Live: one read-only public-demo check". On the same page, provenance says "Live Strategy: not tested" and `/api/catalog` returns `live_connection: "not tested"`. AC-1 specifies "not tested". Both statements are defensible, but side by side they read as a contradiction. Suggested wording: "This app: synthetic records · Live Strategy: not tested here (one public-demo check — see Integration boundary)".

## Live check (`app/live.py`): honesty assessment

The claims are honest overall, and the output reproduced exactly.
- **No saved-object change:** true by construction. The client only issues `POST /auth/login`, `POST /v2/reports/{id}/instances` with a transient `viewFilter`, `GET /model/reports/{id}` and `POST /auth/logout`. There are no PUT, PATCH or DELETE calls and no save. However, `saved_objects_changed=0` is a hard-coded constant, not a before/after measurement such as modification timestamps or version ids. The receipt field reads like a measurement; it would be clearer labelled "by construction".
- **Cleanup:** the code ends the session with logout (204 observed) and never deletes instances. The contract page correctly lists "instance cleanup" under "Still unverified live", and "the session was closed" is accurate. The module docstring's "session cleanup" means logout only.
- **Numerical, not definitional:** honestly framed. The first step is labelled "hypothesis from B's report name". The region step is "observed: absent from B's returned rows". When B's filter is unreadable, `unknowns` states that the result is a numerical reproduction. An exact cent-level match over 7 rows is strong evidence but not proof of B's filter; the docs say exactly that.
- **"A real permission denial":** fair in content, but the server returned HTTP 500 ("Model Server internal error … does not have Read access"), not 403. Worth one clause on the contract page.
- **Minor:** `explained` checks completeness only for the two originals, not for the variant runs (all were complete in both runs). `metric_total` assumes metrics are the innermost column dimension (`j % width`). It works for these reports, and the offline crosstab test covers the two-metric case, but other templates could break that assumption.

## Contrast audit: does it measure what it claims?

It largely does, though the claim is broader than the method. The script resolves the effective background by blending ancestor colours and computes WCAG 2.x ratios with correct large-text thresholds. It covers 6 states (empty, candidate, demonstrated with every disclosure open, unresolved, error, contract page) at 1280×1000 and reports 0 failures in all three engines with identical counts. The minimum among non-exempt text is 4.54:1 (3.72:1 in two states, which must be large text).

What it does not cover:
- **Text that is not a direct text node:** input values (the "40.00" amount), the displayed option of a closed select, `::before`/`::after` content and placeholders. "Every visible text element" should read "every element with a direct visible text node".
- **Opacity:** elements whose own opacity is below 1 are excluded under the label "disabled" rather than blended. Ancestor opacity is ignored. Harmless with reduced motion on, but mislabelled.
- **Interactive states and non-text contrast:** no hover, active or focus states, and no WCAG 1.4.11 checks (control borders, the focus ring, the orange result edge).
- **Narrow widths:** the 390/320 layouts and the equal, snapshots, missing, canceled, stale and imported states are not measured.

So "0 failures across six states for direct text at 1280px in three engines" is supported. "All UI contrast passes" would overclaim.

## All 15 rubric lines

The scored table and stop-rule verdict are in [REVIEW-R4-rubric.md](REVIEW-R4-rubric.md).

## Remaining limits

- **Platforms:** Chromium and WebKit pass inside Microsoft's Playwright Ubuntu image (receipts only; not rerun). Host Chromium still stalls and host WebKit still cannot launch; the cause attributed to Chromium is not independently verified. Physical Windows scaling/High Contrast, Safari on Apple hardware, iPhone, Android and real-device performance remain unverified.
- **Accessibility:** no screen-reader session. Contrast covers direct text only at 1280 px. Forced colours covers two states.
- **Live:** one guest, read-only reproduction on one public build with two transient view filters. Prompts, privileges, paging beyond one page, explicit instance cleanup, server-side cancellation and any customer deployment are not tested. The synthetic app does not call the live client.
- **Product:** customer need, analyst usefulness and differentiation from Test Center remain unvalidated; there was no user study.

**Disposition: 33/33 tests pass (reviewer-run). The live check reproduces exactly and is honestly scoped. No functional blocker in the arithmetic, abstention or recovery contracts. Functional synthetic acceptance stays supportable, subject to the receipt/version reconciliation in defect 6. The design is 11/15 at 4+ and not done by the stop rule; the four-round budget is spent.**
