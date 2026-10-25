# Independent critique — round 6

Reviewed 2026-10-25 against the uncommitted working tree on top of commit 5254c6a (software 0.4.0). Rahil explicitly authorised rounds beyond Web Designer Pro's four-round budget. Same critic role, same bar and identity as R5: Inter, #FA660F, neutral light worksheet (DIRECTION.md). No other brand is used as a yardstick.

**Result: 14/15 lines at 4 or above, one at 3 (Signature), none below 3. Done by the stop rule.** The R5 blocker, line 8 (Depth and finish), moves to 4 because the evidence is now one headed, contained section with its exports in the heading and styled file buttons in the rail. Line 12 (Everyone's computer) moves to 4 on the new axe, touch, forced-colours and macOS WebKit receipts, which I reran in part. All nine R5 defects are fixed or substantially fixed. This round finds six new low-severity defects; under `critique.md` "After done" they should be fixed once, verified and listed as "fixed after the last round, not rescored".

Line 8 is the weakest 4. The evidence band's tint (#fafaf9 on #fff) is almost invisible, and two of the new defects (sub-headings larger than the panel heading, half-width export buttons on phones) are finish defects inside the very panel that earned the 4. If those two are left unfixed, I would not defend line 8 at 4 in another round.

## Method and evidence

I read `references/critique.md`, REVIEW-R5.md, DIRECTION.md, `git diff --stat`, the full `git diff` of `web/`, README and the changed verification scripts (`engine.py`, `layout_checks.py`, `figure_brief.py`, `run_matrix.sh`, new `assistive_check.py`). I also read the receipts `assistive-checks*.json`, `*-webkit-macos.json` and `a11y-tree.txt`.

**Rerun on this host, in a scratch copy (`~/scratch/smi-r6/`, deleted afterwards), so the user's receipts were not overwritten:**
- `python -m unittest discover -s tests`: 33 tests passed.
- Firefox 157 via Playwright with `isolated_server()`: `browser_check`, `layout_checks` (320/390/768/1120/1440, forced colours, reduced motion with the new `getAnimations()==0` assertion, 320 stress), `keyboard_check`, `contrast_audit` (`failures: []`), `assistive_check` (axe 4.14 WCAG 2.2 AA clean in 5 states) and `motion_filmstrip` (0.5 → 0.744 → 0.922 → 1.0). All exited 0, with no flake this time.
- Two scratch probes of my own: (a) the fully expanded state (all four evidence disclosures plus both secondary tool disclosures) at 1440, 390 and 320; (b) measurements of the evidence heading, the export-button widths, the evidence `h3` sizes and the finding eyebrow position after the test.

**Opened at original resolution (cropped where tall):**
- Firefox: demonstrated at 1440, 390 and 320; stress-320 (four crops); candidate, ambiguous, snapshots, missing and equal at 1440; high-contrast-390 and reduced-motion-390.
- Other engines: demonstrated-390-webkit-macos, r5-touch-finding-webkit and r5-forced-colors-390-chromium (five crops).
- My own expanded captures at 1440 (three crops), 390 and 320.

**Not rerun:** the Chromium, WebKit-Linux and WebKit-macOS receipts (podman and the Mac were not used). They are receipt-only credit. I made no contact with port 8807 or 8791.

## R5 defects

1. **Reduced-motion capture was a forced-colours capture: fixed.**
   - `layout_checks.py:23` now sets both media features per mode and asserts `matchMedia('(forced-colors: active)')` matches only for high contrast.
   - The reduced-motion entry replays `.result-enter` and asserts `document.getAnimations().length===0`; my rerun passed.
   - `r4-reduced-motion-390.png` is now byte-identical to `r4-demonstrated-390.png` in all three Linux engines. This is the correct outcome (same final state, normal colours), but it means the PNG proves nothing on its own. The assertion is the proof.
2. **Narrow-cell number and unit wrapping at 320: fixed.**
   - `style.css:65-71` stacks the cells at ≤360 px. In stress-320, "90,071,992,547,529.93" sits on one line under the report name, and "illustrative units with a deliberately / extended label" wraps between words.
   - The ARIA table roles keep the table semantics; `a11y-tree.txt` shows rowgroup/row/columnheader/cell.
3. **Missing-unit caption contradicted its row: partly fixed.**
   - "Illustrative values" no longer appears when the units do not match.
   - The replacement, "The units differ; each total shows its own." (`view.js:46`), is still not accurate in missing-1440: B's unit is not different, it is absent ("Unit not provided"). See new defect 4.
4. **No scroll affordance on the record table: fixed.** At stress-320 a soft shadow sits at the right edge of the clipped Amount column. The `local`/`scroll` gradients use the panel tint #fafaf9, so they match the new band. At 1440, where nothing overflows, no shadow shows.
5. **Helper text flush under the candidate button: fixed.** `.finding .primary+.hint{margin-top:8px}`. In candidate-1440 and stress-320 the helper text now sits clearly under the button.
6. **Unstyled native file buttons: fixed.** `::file-selector-button` is 44 px high with a 1 px #bcbcb6 border, a 6 px radius and 600 weight. In expanded-1440, "Browse…" now matches "Update synthetic source". My probe measured 44 px input height at every width.
7. **"−0.00%" for a nonzero delta: fixed.** `view.js:14` `percent()`; stress-320 shows "−<0.01% relative to A". The "−<" pairing reads awkwardly (trivial, new defect 6).
8. **Scripts and docs pointing at 8807: fixed.**
   - `review_shots.py` is deleted (staged).
   - `figure_brief.py` uses `isolated_server()` and `launch()`.
   - README:44 now reads "each check starts its own server and throwaway database".
9. **Trivial items: fixed.**
   - The snapshot value is wrapped in `.nowrap`, so "synthetic-orders-v1" stays on one line at 390.
   - The duplicate `.report-table .amount`, `.unit` and `.record-table :last-child` rules are folded into their originals (`style.css:10,14`).

## Other changes verified

- **Evidence panel** (`evidence.js:9`, `style.css:3`): `section.evidence` with `aria-labelledby`, the eyebrow "03 / Evidence", the h3 "What this result rests on", the exports in the heading, a #fafaf9 band under a top rule and the packet note under a rule. This completes the 01 / 02 / 03 sequence.
- **Custom select chevrons**: they render identically in Firefox and in WebKit on macOS. `@media(forced-colors:active)` restores native appearance; the forced-colours Chromium capture shows native selects.
- **Capture method**: `engine.capture()` scrolls to the top before full-page captures. No capture shows the banner mid-page.

## New defects, by severity

There are no high or medium defects.

1. **Low (finish/semantics): evidence sub-headings are larger than the panel heading.**
   - Where: `evidence.js:9` renders "Original A", "Original B" and "Diagnostic experiment" as `<h3>`, and they inherit `h3{font-size:20px}`. The panel heading is `.evidence-head h3{font-size:18px}`.
   - Measured at 390 and 768: 18 px panel heading, 20 px children. In expanded-1440 they read as louder than "What this result rests on". The heading outline also puts them at the same level as their parent.
   - Fix: render them as `<h4>` and add `.evidence h4{font-size:14px;font-weight:600;letter-spacing:0;margin:16px 0 8px}`.
2. **Low (responsive finish): export buttons are half-width on phones.**
   - Moving `.evidence-actions` into the flex `.evidence-head` (`style.css:3`) means the old ≤700 rule (`style.css:4`, `.evidence-actions{display:grid}.evidence-actions button{width:100%}`) only fills the shrink-wrapped actions box.
   - Measured at 390: the actions box is 164 px wide in a 324 px heading, so two stacked 164 px buttons leave an empty right half. Visible in demonstrated-390, the WebKit-macOS capture, forced colours and stress-320.
   - Fix, inside `@media(max-width:700px)`: `.evidence-actions{flex:1 1 100%;grid-template-columns:1fr 1fr}`. This puts the buttons side by side, each about 158 px, which fits "Export evidence JSON" at 12 px. Or use `1fr` for full-width stacking.
3. **Low (craft, phone): after the test, the finding's eyebrow lands under the sticky banner.**
   - Where: `style.css:20` `#finding-title{scroll-margin:96px 0 24px}` with `app.js:19` focusing and scrolling to the h3.
   - At 390 the banner is 57 px (two lines). My probe measured the eyebrow top at 39 px, so "NUMERICAL CAUSE DEMONSTRATED" is hidden behind the banner and only "ON SYNTHETIC DATA" shows. This is visible in `r5-touch-finding-webkit.png`. At 768 the margin is 2 px. The bug predates this round, but it is first visible in the new touch capture.
   - Fix: scroll the `.finding` container instead of the heading, with `.finding{scroll-margin-top:72px}` (`@media(max-width:700px){.finding{scroll-margin-top:72px}}`). Keep focus on the h3 with `preventScroll`. Alternatively raise the h3 margin to about 140 px at ≤700.
4. **Low (copy honesty): the missing-unit caption says "differ".**
   - Where: `view.js:46`.
   - Fix: when one unit is empty, write "Computed from synthetic orders. B's unit is not provided." Keep "The units differ; each total shows its own." only when both units are present and differ.
5. **Low (docs): receipts and README lag the new evidence.**
   - `layout_checks.py:56` writes `'limits':'Linux emulations…'` into `layout-checks-webkit-macos.json`, a macOS run.
   - README:59 still links REVIEW-R4 as the latest critique. It also does not mention the macOS WebKit and axe receipts.
   - Fix: derive the limits string from `HOST`, link REVIEW-R6, and add one sentence saying Playwright WebKit ran on macOS 27.2. That run is not Safari proper and not VoiceOver.
6. **Trivial:**
   - **Wide hyphens in identifiers.** `font-variant-numeric:tabular-nums` is set on the whole `.ledger` (`style.css:25`) and `.report-table`, and identifiers there render with spaced hyphens: "order‑2", "synthetic‑orders‑v1". The same strings in the context table look normal. Fix: scope `tabular-nums` to `.num`, `.amount` and `.difference strong`.
   - **"−<0.01%" reads awkwardly.** Fix: "less than 0.01% below A" / "above A".
   - **Select heights differ.** The "Example investigation" select is 46 px tall while the report selects are 44 px (different font sizes). Fix: `height:44px` on the selects.
   - **Hover state in captures.** Compare totals shows its hover colour in captures because the pointer rests on it. Fix: move the mouse away before capture.

## All 15 rubric lines

A 3 is competent; a 4 would ship at a top studio within this analytical scope. No 5 is awarded.

| Line | R5 → R6 | Evidence (one line) |
|---|---:|---|
| 1. Concept on the page | 4 → 4 | Captured B → +40 "Adds order-2 (refunded, 40)" → rerun 220 → A 220 → double rule → 0; now also 01 / 02 / 03 setup → investigate → evidence. |
| 2. Not category average | 4 → 4 | A double-ruled reconciliation ledger and evidence worksheet, not KPI cards or a chart shell. |
| 3. Not slop/rut | 4 → 4 | No decorative chart, gradient or KPI row. The "Fixed synthetic snapshot" pill and the single-bullet caveat remain the only generic bits. |
| 4. First screen | 4 → 4 | 1440 shows setup, both totals, difference and finding. At 390 the worksheet starts at about 640 px; the post-test eyebrow hides under the banner (defect 3). |
| 5. Typography | 4 → 4 | Inter hierarchy, tabular totals on one line at 320. The evidence sub-heading inversion (defect 1) and tnum-widened hyphens (defect 6) are the residuals. |
| 6. Colour | 4 → 4 | Orange owns the primary actions and the finding edge; dark-orange +40; contrast `failures: []` in all four engine receipts; forced colours keeps the boundaries. |
| 7. Imagery / evidence material | 4 → 4 | The ledger sub-line names order-2, the record table marks it "Added by the test", and the context table flags "Differs". |
| 8. Depth and finish | 3 → **4** | The evidence is one headed section (03 / Evidence, exports in the heading, packet note under a rule); styled 44 px file buttons, drawn chevrons, helper spacing fixed. The #fafaf9 band barely separates, and defects 1–2 sit inside it. |
| 9. Below first screen | 4 → 4 | Context table with Differs marks, the marked added row, a scroll-cued record table at 320 and a closing evidence section. |
| 10. Craft | 4 → 4 | Every R5 craft residual is closed (stress totals, file chips, helper spacing, nowrap snapshots). Defects 1–4 are new and low. |
| 11. Responsive | 4 → 4 | 320 stacks the totals full-width; 390 pairs the report selects; 768 keeps a 240 px rail. The phone export buttons are half-width (defect 2). |
| 12. Everyone's computer | 3 → **4** | axe WCAG 2.2 AA clean in 5 states (rerun in Firefox; receipts for Chromium, WebKit-Linux and WebKit-macOS), Pixel 7/iPhone 15 tap flow with no target under 44 px, forced-colour boundary assertions, reduced motion asserted, Option+Tab keyboard pass on macOS. Still no Windows scaling, l10n, real VoiceOver/NVDA or Safari proper. |
| 13. Signature | 3 → 3 | Unchanged: a truthful 180 ms 0.5 → 1.0 fade plus focus moving to the finding. The ledger is memorable; the moment is not. |
| 14. Copy and conversion | 4 → 4 | Actions say what happens; abstentions are precise; "What this result rests on" is plain. "The units differ" for a missing unit is the one inaccurate string (defect 4). |
| 15. Screenshot test | 4 → 4 | The 1440 ledger frame, now closed by the evidence section, holds up as a saveable analytical worksheet. |

**Count: 14/15 at 4 or above (all except line 13). Line 13 is at 3; none is below 3.** My Firefox reruns of the scan and matrix show no FAILs. The other engines pass by receipt.

**Stop rule (`critique.md`): met.**
- No line is below 3.
- 14 lines are at 4+, against the 12 required.
- Lines 4, 7, 8, 9, 10 and 14 are all at 4+.
- The scan and matrix have no FAILs.

Next step under "After done": fix new defects 1–5 once, then verify them with `layout_checks`, `assistive_check` and an expanded-state capture at 390 and 1440. List them as "fixed after the last round, not rescored", then stop. Line 13 is the only line below 4. Raising it would need a new moment born from the ledger (for example, the +40 step drawing from the marked source row), not a different fade, and it is outside the stop rule's requirements.

Trend of lines at 4+: R3 9 → R4 11 → R5 12 → R6 14.
