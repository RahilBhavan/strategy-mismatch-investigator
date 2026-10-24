# Independent critique — round 4: rubric

Part of [REVIEW-R4.md](REVIEW-R4.md), moved verbatim to keep each file under the repository size limit.

## All 15 rubric lines

A 3 is competent; a 4 is strong enough to ship in this analytical scope; no 5 is awarded. The last column gives one route toward 5.

| Line | R3 → R4 | Observed evidence and change toward 5 |
|---|---:|---|
| 1. Concept on the page | 4 → 4 | Captured B → controlled change → rerun → A → residual now explains the product without the docs. Show the added record inline in the ledger step (row chip or mini record), not only in the collapsed source table. |
| 2. Not category average | 3 → 4 | The double-ruled reconciliation ledger is a specific accounting form, not a generic form-and-table shell. Let the ledger replace the separate totals table once the test runs, so the page has one numerical spine instead of two stacked tables. |
| 3. Not slop/rut | 4 → 4 | No KPI cards, decorative chart or repeated summary. The small "Fixed synthetic snapshot" pill and bulleted single caveat are the last generic bits. Fold the caveat into the residual row's note. |
| 4. First screen | 3 → 4 | Desktop shows setup, both totals, the difference and the action. At 390×844, setup and Compare fit, the worksheet starts at about 630 px and A's total sits at about 805 px. After the test, the finding scrolls to the top. Compress the phone header and title enough to show both original totals above a 664 px Safari viewport. |
| 5. Typography | 4 → 4 | Clear Inter hierarchy, tabular figures, real minus signs, 30 px residual. Prevent digit-group breaks in large totals (defect 4) and restore label typography in the tools aside. |
| 6. Colour | 4 → 4 | Orange owns primary actions and the result edge; dark-orange +40 passes contrast; the audit is broader than R3's sample. Measure focus-ring, control-border and hover pairs (non-text contrast) before a full colour claim. |
| 7. Imagery / evidence material | 4 → 4 | "Adds order-2 (refunded, 40)" in the ledger plus the "Added by the test" source row now connect the record to the 180 → 220 step. Make that link visible without opening a disclosure. |
| 8. Depth and finish | 3 → 3 | The ledger panel (tint, orange rule, double rule, scale step on the residual) has real hierarchy and alone would justify 4. But the open tools rail shows browser-default controls in four of nine 1440 renders, and the four evidence disclosures are a uniform hairline stack. Restore the control styling and give the evidence stack one level of grouping (for example, a contained evidence panel with the exports). |
| 9. Below first screen | 4 → 4 | Compact A/B context table with Differs marks, marked source row, right-aligned amounts. The 320 record table clips (defect 3). Add a scroll wrapper or stacked rows for narrow record tables. |
| 10. Craft | 4 → 3 | Regressed: unstyled tools controls below 44 px (defect 1), wrong snapshot caption in a primary state (defect 2), clipped amounts at 320 (defect 3), mid-number wrap (defect 4) and the sticky-banner anomaly R3 asked to repair. Fix these five and add checks that would catch them (control box sizes after opening tools; element-level overflow, not only page scrollWidth). |
| 11. Responsive | 4 → 4 | The phone order is now setup → work → secondary tools, with paired report selects and the ledger holding at 320. Fix narrow record-table overflow, then show 768 with the rail beside an evidence-open state. |
| 12. Everyone's computer | 3 → 3 | Clear progress: browser, keyboard, layout and contrast checks recorded as passing in Firefox 157, Chromium 156 and WebKit 27.2 (receipts only; not rerun here). Forced colours now covers the demonstrated state. R3's second condition, an actual assistive-technology pass, is still absent, and there is no Windows scaling, Safari-on-Apple or l10n check. Run one VoiceOver or NVDA pass through compare → test → finding. |
| 13. Signature | 3 → 3 | The filmstrip proves a real 180 ms fade from 0.5 to 1.0 opacity plus focus and scroll to the finding. It is truthful and accessible but a generic fade. The memorable part is the ledger, not the motion. Make the transition show the change itself: the B row hands its 180 to the ledger, then +40 and the rerun land in sequence. |
| 14. Copy and conversion | 4 → 4 | Specific actions, precise abstention, honest live framing on the contract page. The banner's "Live: one read-only public-demo check" conflicts with "Live Strategy: not tested" in provenance. Reconcile to one statement. |
| 15. Screenshot test | 3 → 4 | A restrained analyst UI with a recognisable, saveable reconciliation ledger. To reach the bar, give the evidence below the ledger the same compositional care. |

**11/15 at 4+, none below 3.** First screen reaches 4; Depth and finish stays at 3. **Not done by the parent's stop rule** (it needs 12+ lines at 4 with First screen and Depth/finish at 4). It is also not done by the stricter `critique.md` rule, which further requires Imagery, Below first screen, Craft and Copy at 4 and no FAILs; Craft is 3. The trend over R1 → R4 is real: 9 → 11 lines at 4, with four lines raised and one lowered by a regression.

The two blocking lines are close. If defect 1 is fixed and the evidence stack gets a small grouping move, Depth and finish would plausibly reach 4. If defects 1–4 and the capture anomaly are fixed, Craft would plausibly return to 4. Together that would make 13/15. That is a forecast, not a score. This was the last round in the skill's budget, so any fixes should be recorded as "fixed after the last round, not rescored", not presented as a pass.
