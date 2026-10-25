# Independent critique — round 5

Reviewed 2026-10-25 against commit 5254c6a (software 0.4.0). Rahil explicitly authorised this round beyond Web Designer Pro's four-round budget, because the seven R4 defects were fixed after R4 but never rescored.

**Result: 12/15 lines at 4 or above, three at 3, none below 3. Not done by the stop rule.** The line count now reaches the threshold of 12, and Craft returns to 4. However, `critique.md` also requires line 8 (Depth and finish) to be at 4, and it stays at 3: the R4 ask to group the evidence stack was not attempted. Of the seven R4 defects, four are fixed and three are partly fixed. The fresh renders show one new verification defect: the reduced-motion capture is actually a forced-colours capture.

## Method and evidence

I read `references/critique.md` (15 lines and stop rule), REVIEW-R4.md, REVIEW-R4-rubric.md, DIRECTION.md, README.md, ACCEPTANCE-RECEIPT.md and `git show --stat HEAD`. I also read the relevant parts of `web/style.css`, `web/view.js`, `web/evidence.js`, `verification/engine.py`, `layout_checks.py` and `run_matrix.sh`. As in earlier rounds, I kept the approved identity: Inter, #FA660F and the neutral light worksheet.

**Rerun on this host:**
- `python -m unittest discover -s tests`: **33 tests passed** (4.4 s).
- Firefox 157 through Playwright 1.64.1, using the host Firefox binary and `isolated_server()` (temporary database, free port). Each script below passed:
  - `browser_check.py`: 11/11 checks pass.
  - `layout_checks.py`: no overflow at 320, 390, 768, 1120 and 1440, in forced colours, in reduced motion and in the 320 stress case.
  - `keyboard_check.py`: PASS. Focus lands on `finding-title` at top 96, below the 57 px banner, with zero pointer actions and no external requests.
  - `contrast_audit.py`: `failures: []`.
  - `motion_filmstrip.py`: opacity 0.5 → 0.744 → 0.922 → 1.0. The first run printed a JavaScript stack trace. Three further runs exited 0, so this looks like a one-off flake.
- These runs regenerated the Firefox `r4-*.png` captures and the JSON/HTML receipts. Only `r4-stress-320.png` and the export and report receipts changed bytes; the other PNGs re-rendered identically.

**Concurrent edits.** My renders finished at 09:58. Between 10:00 and 10:03, while I was writing this review, another process modified the working tree:
- `web/style.css`: 44 px min-height added to header links and file inputs.
- `engine.py` (a new `capture()` helper), the check scripts and `run_matrix.sh`.
- New untracked assistive receipts and `r5-*` captures.

This review scores commit 5254c6a as rendered at 09:58, and every file:line reference points at HEAD. The uncommitted changes are not scored. If they are committed, defects 1 and 6 below should be rechecked against them.

**Opened at original resolution:**
- demonstrated at 1440, 768, 390 and 320; candidate-1440 (cropped); ambiguous-1440, snapshots-1440 and missing-1440, which show the secondary controls expanded; unresolved-390; high-contrast-390; reduced-motion-390.
- stress-320, in three full-resolution crops: the totals, the candidate card and context table, and the source records.

**Not rerun:**
- The Chromium and WebKit receipts. `run_matrix.sh` needs podman, and I did not run it.
- I made no contact with port 8807 or 8791. I therefore could not check whether the six duplicate stress cases R4 found in the demo database are still there.
- I did not run the untracked `verification/assistive_check.py`, and I give it no credit.

## R4 defects

1. **Expanded secondary controls lost their styling: fixed.**
   - `style.css:3` now also selects `.secondary-tools label/select/input[type=text]`.
   - In ambiguous, snapshots and missing at 1440, "Amount on the refunded order" is a 13 px/500 block label. The 40.00 field and the "Normal execution" select are 44 px with a 6 px radius and match the setup rail.
   - Residual: the two native "Browse…" file buttons remain unstyled chips about 20 px tall (new defect 6).
2. **Wrong snapshot caption: partly fixed.**
   - `view.js:40` now prints "Snapshot for both: …" only when A and B match. Otherwise it prints a per-row "Snapshot:" line. snapshots-1440 correctly shows v1 under A and v2 under B, with no shared caption. `evidence.js:16` lists A and B separately.
   - Not fixed: the milder variant R4 named. In missing-1440 the caption still says "Illustrative values, computed from synthetic orders" while B's total says "Unit not provided" (new defect 3).
3. **Amount column clipped at 320: fixed, with a weak affordance.**
   - `evidence.js:9` wraps the record table in `.table-scroll` with `tabindex="0"`, `role="region"` and an aria-label. `style.css:63-64` give it `overflow-x:auto` and a focus ring.
   - According to the receipt, the layout check now also looks for clipped worksheet tables.
   - Residual: at rest at 320, the whole Amount column except a lone "A" is off-screen, and nothing shows that the table scrolls (new defect 4).
4. **Totals break mid-number at 320: partly fixed.**
   - Amounts now break only after group commas (`<wbr>` at `view.js:40`, 22 px at `style.css:66`). In stress-320 the total reads "90, / 071, / 992, / 547, / 529.93": readable as digit groups, but five lines for one number.
   - Not fixed: the unit still breaks mid-word as "deliberatel / y". `overflow-wrap:break-word` (`style.css:67`) breaks an overlong word in a narrow cell just as `anywhere` did.
5. **Verification scripts write into the 8807 demo: partly fixed.**
   - All five main checks now use `engine.isolated_server()`, and `run_matrix.sh` no longer targets 8807.
   - Not fixed:
     - `verification/review_shots.py:8,19` and `verification/figure_brief.py:12` still `goto('http://127.0.0.1:8807')` and click Compare and Test, which creates jobs in the demo database. Both are tracked in Git.
     - `README.md:44` still says `run_matrix.sh` "needs podman and the demo server on 8807", which is now false.
6. **Documents and receipts disagree: fixed, except one stale README line.**
   - ACCEPTANCE-RECEIPT.md now says 0.4.0, and the stale `chromium-check.json` and `webkit-check.json` are gone.
   - `docs/ACCEPTANCE.md:31` describes `live-demo-check.json` correctly as a public-demo receipt.
   - Remaining: README.md:44 (see defect 5). README also still links REVIEW-R4 as the latest critique.
7. **Live-status wording conflicts: fixed.**
   - Provenance (`evidence.js:9`) now reads "Simulated. This app never calls Strategy. A separate read-only check against Strategy's public demo is described on the integration boundary page."
   - This agrees with the banner ("This app: synthetic records · Live: one read-only public-demo check") and with the packet's `live_connection: "not tested"`, which describes this app.

The R3 sticky-banner capture anomaly is also **fixed**. `engine.CAPTURE_STYLE` makes the banner static during full-page captures, and no 1440 or 390 render shows it cutting mid-page.

## New defects, by severity

1. **Medium (verification integrity): the reduced-motion capture is a forced-colours capture.**
   - The Firefox `r4-reduced-motion-390.png` is byte-identical to `r4-high-contrast-390.png`. Both show grey system controls and black borders.
   - Cause: `layout_checks.py:22-23`. `emulate_media(forced_colors='active')` stays active when the loop next calls `emulate_media(reduced_motion='reduce')`.
   - The capture is also taken after the result has rendered, so it cannot show that the animation is suppressed. The receipt's "reduced motion" proof therefore shows nothing about normal colours or motion. (The WebKit pair does differ.)
   - Fix: use `{'forced_colors':'none','reduced_motion':'reduce'}` for the reduced-motion entry. Then rerun the test under reduced motion and assert `getAnimations().length===0` on `.result-enter`.
2. **Low-medium: narrow-cell number and unit wrapping at 320 (stress input).** See R4 defect 4. `style.css:66-67`.
   - Fix: at ≤360 px, stack the total under the report name (`.report-table td{display:block}` with the amount left-aligned at full width). This puts "90,071,992,547,529.93" on one line and the unit on its own line, with no mid-word break.
3. **Low: the missing-unit caption contradicts its row.** `view.js:40`: the caption always opens "Illustrative values".
   - Fix: say "Illustrative values" only when both units match. Otherwise write "Units: A illustrative units; B not provided."
4. **Low: the record-table scroll region has no affordance.** `style.css:63`.
   - Fix: add an edge-shadow cue (`background: linear-gradient(...) local, ... scroll` on `.table-scroll`).
   - Or, at ≤400 px, render each record as a two-line row (order · status · region, then the right-aligned amount).
5. **Low: the candidate helper text sits flush under its button.**
   - In candidate-1440, the "Test the status selection →" button has about 38 px above it and about 4 px below it before "Rerun B with only A's status selection…". The same happens at 320. Source: `view.js:54`; `.finding button{margin-top:20px}` in `style.css:3` and no margin on the hint.
   - Fix: `.finding .primary+.hint{margin-top:8px}`.
6. **Low (finish): unstyled native file buttons in the tools rail.** `style.css:3` (`.tools input[type=file]`).
   - Fix: style `::file-selector-button` like `.secondary`: 44 px high, 1 px #bcbcb6 border, 6 px radius, 13 px/600 text.
7. **Low (number honesty, stress only): a nonzero difference shows as "−0.00% relative to A".** `app/investigate.py:39` quantizes to 0.01.
   - Fix: when the ratio is nonzero and rounds to zero, show "< 0.01%" with its sign.
8. **Low: scripts and docs still point at the 8807 demo.** These are `review_shots.py:8,19`, `figure_brief.py:12` and `README.md:44` (see R4 defect 5).
   - Fix: move both scripts onto `isolated_server()` or delete them, and correct the README line.
9. **Trivial:**
   - The snapshot subline wraps at its hyphen at 390 ("synthetic-orders- / v1"). Fix: `white-space:nowrap` on the snapshot value.
   - `style.css` carries appended duplicate rules: line 10 sets `.report-table .amount` twice, and lines 15, 47 and 65 repeat `.record-table … :last-child`. Fold them into their original rules.

## All 15 rubric lines

A 3 is competent; a 4 would ship at a top studio within this analytical scope. No 5 is awarded.

| Line | R4 → R5 | Evidence (one line) |
|---|---:|---|
| 1. Concept on the page | 4 → 4 | Captured B → +40 "Adds order-2 (refunded, 40)" → rerun 220 → A 220 → double rule → 0 tells the product without docs at every width. |
| 2. Not category average | 4 → 4 | A double-ruled reconciliation ledger, not KPI cards or a chart shell; there are still two stacked numeric tables (totals and ledger). |
| 3. Not slop/rut | 4 → 4 | No decorative chart, gradient or KPI row. The "Fixed synthetic snapshot" pill and the single-bullet caveat are the last generic bits. |
| 4. First screen | 4 → 4 | 1440 shows setup, both totals, the difference and the action. At 390 the worksheet starts at about 630 px, and focus moves to the finding after the test (keyboard receipt: top 96). |
| 5. Typography | 4 → 4 | Inter hierarchy, tabular figures, real minus signs, a 30 px residual. Totals now break only at group commas; the unit still breaks mid-word at 320 (stress). |
| 6. Colour | 4 → 4 | Orange owns the primary actions and the result edge; dark-orange +40; the contrast audit reports `failures: []` at 1280 and 390. Non-text contrast is still unmeasured. |
| 7. Imagery / evidence material | 4 → 4 | The ledger sub-line names the added record, and the source table marks it. The connection is still text, not a visible record object. |
| 8. Depth and finish | 3 → 3 | The control styling is restored, but the R4 grouping ask was not attempted: four identical hairline disclosures plus two small outline buttons under a rich ledger, native "Browse…" chips in the rail, and flush helper text. Contain the evidence and exports in one tinted panel with its own heading. |
| 9. Below first screen | 4 → 4 | Context table with Differs marks, a marked added row and a now-scrollable record table at 320. The scroll has no cue. |
| 10. Craft | 3 → 4 | All primary states are clean at 1440, 768, 390 and 320: per-report snapshots, 44 px tools controls, no banner anomaly. The residuals are a stress-only unit wrap, the missing-unit caption, helper spacing and file chips (defects 2–6). |
| 11. Responsive | 4 → 4 | 390 and 320 keep setup → worksheet → tools with paired selects, and the ledger holds. 768 keeps a 240 px rail beside the worksheet. |
| 12. Everyone's computer | 3 → 3 | Firefox checks rerun green; Chromium and WebKit are receipt-only. Still no screen-reader pass, Windows scaling, Safari on Apple hardware or l10n check. The Firefox reduced-motion capture is actually forced colours (defect 1). |
| 13. Signature | 3 → 3 | A truthful 180 ms 0.5 → 1.0 fade plus focus moving to the finding. A generic fade; the ledger is the memorable part, not the motion. |
| 14. Copy and conversion | 4 → 4 | The live wording is reconciled ("This app never calls Strategy. A separate read-only check…"). The actions say what happens, and the abstentions are precise. |
| 15. Screenshot test | 4 → 4 | The ledger frame at 1440 is recognisable and saveable. The evidence below it is still plainer than the ledger. |

**Count: 12/15 at 4 or above (lines 1–7, 9–11, 14, 15). Lines 8, 12 and 13 are at 3; none is below 3.** The Firefox scan and matrix show no FAILs, though the reduced-motion receipt is weaker than claimed.

**Stop rule (`critique.md`): not met.** It requires no line below 3 (met), at least 12 lines at 4+ (met: 12), and lines 4, 7, 8, 9, 10 and 14 at 4+. **Line 8 (Depth and finish) is 3**, and that alone blocks "done".

The single move most likely to change the verdict is to group the evidence disclosures and exports into one contained, headed panel, and to style the file buttons. That would plausibly lift line 8 to 4 and meet the rule. This is a forecast, not a score. The trend across rounds is 9 → 11 → 12 lines at 4+.
