# Independent critique — round 2

Reviewed 2026-10-24 for the approved synthetic Strategy integration POC, software version 0.2.0. **R1’s substantive explanation fixes landed. No new proven numerical defect or material numerical-honesty defect was found in this review. The rendered POC is suitable for a bounded synthetic demonstration; full acceptance and the Web Designer Pro stop rule are not independently signed off.**

## Scope and method

Read DIRECTION.md, revision 3 docs/SPEC.md and docs/ACCEPTANCE.md, historical verification/REVIEW-R1.md, Web Designer Pro’s critique/app/finish/slop references, and the shared design-system-workflow and Tufte guidance. Strategy’s observed Inter roles, orange controls and neutral worksheet authority prevail over decorative photography, poster typography or theatrical depth. Real computed evidence is the appropriate visual material.

Opened all six requested complete images: r2-demonstrated-1440.png, r2-demonstrated-390.png, r2-ambiguous-1440.png, r2-ambiguous-390.png, r2-evidence-390.png and r2-evidence-1440.png. The expanded evidence images were also opened at original resolution. No file was missing. These stable round-two renders govern this review; regenerated R1 filenames are not used to reconstruct earlier pixels.

Read tests.txt, browser-checks.json, layout-checks.json, chromium-check.json, webkit-check.json and the corresponding browser/layout scripts, plus independent-cases.json and tests/test_independent.py. **I did not execute tests, launch a browser, or independently reproduce these receipts in round 2.** Findings distinguish visible evidence, supplied execution receipts and unperformed checks. Only this review file was written; no code, tests, account, Git state or external artifact was changed.

## Did the R1 asks land?

- **Both ambiguous differences: landed.** The unresolved finding explicitly lists A/B status and A/B region on desktop and phone. It makes no experimental impact claim and does not add overlapping effects.
- **Computed transition and repetition: substantially landed.** The demonstrated summary now says B changes 180.00 to 220.00 and leaves 0.00 difference from A. One business-definition caveat remains inside the finding. The screenshots alone establish this example’s copy, not correctness of every dynamic text branch.
- **Intro promise: landed.** “Compare two totals. Test a possible cause. Inspect the evidence.” fits unresolved as well as demonstrated outcomes. The task title “Explain the difference” is reasonable as a task name with the explicit unresolved state beneath it.
- **Phone evidence: landed visually; interaction proof partial.** Both requested result types and open evidence are readable at 390px. Report rows retain names/selections next to totals, experiment values become label/value rows, fingerprints wrap, and export controls span the phone width. Receipts report no overflow at 320/390/768/1120/1440 and long-content stress at 320. Complete keyboard operation is still not established below.
- **Sign conventions: landed.** Measured change is labeled “variant − original B”; remaining difference is labeled “variant − A.” Original delta remains B − A. The example consistently displays −40, +40 impact and zero residual.

## Remaining concrete findings

1. **Medium verification gap — the keyboard pass overstates its coverage.** browser_check.py resets to the initial page before its 16-Tab walk and asserts only that Compare totals has a solid outline. The receipt reaches the report selectors, Compare, setup disclosure and packet input; it never records Test the status selection, result evidence disclosures or either export action. Repeated packet-input entries are insufficient evidence of a focus trap and are not reported as one. Supply an observed keyboard-only compare → test → open evidence → export path, with visible focus and Enter/Space activation, including expanded setup controls and retry/cancel where applicable. This is the remaining material AC-15 proof gap, not a demonstrated inability to use the app by keyboard.

2. **Low task friction — phone setup and recovery displace the current investigation.** In r2-evidence-390.png, the report panel begins around y=850, after the packet-import section. Thus an ordinary short phone viewport shows setup/recovery before showing even an original total, and the completed finding is much farther down. The narrower paired report selectors and result rows are deliberate adaptations, but recovery still interrupts the primary path. Collapse “Continue a review” by default on phone, or place it after the active worksheet. Keep packet recovery accessible. A comparison/result jump after completion would also help, with focus handled deliberately rather than unexpected scrolling.

3. **Low copy defect — the unresolved explanation still sounds less certain about known differences than its evidence warrants.** The ambiguous state repeats “The evidence does not isolate a cause” as “Not enough evidence to explain this difference,” then says “Status and region both differ, or the difference is outside the supported status experiment.” Here both changes are known and shown. For this branch, use “Status and region both differ. This status-only experiment cannot isolate their effects.” Keep a different message for unsupported differences. This is a clarity improvement; the present copy does not falsely demonstrate a cause.

4. **Low quantitative craft — source amounts are left-aligned.** In both expanded-evidence renders, Amount headers and values (100.00, 40.00, 60.00, 20.00) start at a shared left edge. Right-align this column, including its header, so decimal magnitudes are easier to compare. Main report totals and mobile experiment values already have stronger alignment. There is no misleading area/length encoding, truncated axis or chart to repair.

5. **Low verification/reporting defect — platform-state receipt names and assertions need narrower claims.** layout_checks.py finishes its width loop at 1440 and does not reset to 390 before writing high-contrast-390.png and reduced-motion-390.png. Those names do not establish phone coverage. Both media checks assert only no horizontal overflow; they do not assert forced-color legibility, distinguishable states, focus visibility or reduced-motion animation behavior. The comment about measuring contrast precedes font-size collection, not an actual contrast-ratio measurement. Relabel those screenshots or capture the intended width, and record the properties actually inspected. No contrast failure is established by this review.

These are the five highest-value next actions. None calls for enterprise access, a different brand, OS package installation, photography or a new visual identity.

## Numerical evidence and its limits

The supplied full-suite receipt reports **30 tests passed in 3.851 seconds**, including the 11 independent tests. This is receipt-backed success, not a new reviewer-run result. R1 records 10 supported reference outcomes: six demonstrated single-cause cases, two equal controls and two appropriate abstentions, plus one unsupported-calculation abstention. The stored test source checks exact totals, impacts, unchanged originals and cleanup. It also preserves the original reviewer correction: SUM(amount) + 0 is unsupported, so that case is not counted as a supported equal-definition test. The supplemental equal control reuses frozen arithmetic and is not freshly held out.

The independent reference file’s residual convention remains A − variant, whereas the implementation/UI use variant − A. This discrepancy is explicitly documented in the reference corrections. Executed single-cause residuals are zero; the nonzero ambiguous counterfactual is not executed or asserted as an observed residual. Therefore the cases do not independently prove a nonzero residual sign branch, and I do not infer a numerical bug from that unused reference.

The visible evidence supports the standard fixture: records 100 paid East, 40 refunded East, 60 paid West and 20 paid West produce A=220, paid-only B=180, variant=220, impact=40 and residual=0. In the ambiguous fixture B additionally selects West, producing B=80; the UI shows −140 and appropriately withholds a cause. Expanded evidence includes definitions, units/scale, grain, snapshot, original/variant instances, selected/known row counts, fingerprints, software version 0.2.0 and 3 released / 3 created instances. “Locally authored synthetic responses” is stated explicitly. These are appropriate provenance disclosures, not proof of actual Strategy API execution.

## Independent rubric scores

Scores assess this analytical app, not a marketing poster. A 3 is competent, a 4 is strong enough to ship within this scope, and no portfolio-level 5 is awarded from these materials. Every sub-5 row names a specific path toward 5; those refinements are not automatically POC blockers.

| Line | R1 → R2 | Visible evidence; single change toward 5 |
|---|---:|---|
| 1. Concept on the page | 4 → 4 | Originals, a status intervention and residual clearly express investigation; consolidate them into one compact, auditable original-to-variant sequence. |
| 2. Not category average | 3 → 3 | Useful but familiar form/worksheet shell; let the controlled numerical transition define the layout more distinctly. |
| 3. Not slop/rut | 4 → 4 | No fake KPI row, decorative chart or six-color status palette; remove the remaining redundant unresolved sentence. |
| 4. First screen | 3 → 3 | Desktop prioritizes originals and Compare; phone gives prime space to recovery before the current evidence; collapse/move recovery to expose the active work earlier. |
| 5. Typography | 4 → 4 | Inter hierarchy and the larger quantitative labels are clear; align source amounts by their decimal/right edge. |
| 6. Colour | 4 → 4 | Orange identifies action and the demonstrated result edge on neutral surfaces; add observed contrast/forced-color proof for all control states. |
| 7. Imagery / evidence material | 4 → 4 | Record-backed totals and open source records are honest, useful visual material; connect the changed record selection to B’s transition more directly. |
| 8. Depth and finish | 3 → 3 | Borders and the result inset organize the surface, but much has uniform visual weight; strengthen hierarchy between decision, summary and audit detail using spacing/weight rather than decorative effects. |
| 9. Below first screen | 3 → 4 | Open context, execution, source records and provenance remain legible at both widths; make common A/B context compactly comparable instead of repeating long vertical lists. |
| 10. Craft | 4 → 4 | No clipping/collision in the six supplied renders; finish numeric table alignment and the complete keyboard-state proof. |
| 11. Responsive | 2 → 4 | Paired selectors, compact report rows, stacked experiment rows and wrapped hashes hold at 390; shorten the recovery detour and prove active-state keyboard operation at narrow width. |
| 12. Everyone’s computer | 2 → 3 | Linux Firefox has meaningful receipts, while Chromium/WebKit remain unverified; supply successful engine checks and actual focus/contrast observations on an available supported host. |
| 13. Signature | 3 → 3 | The result occupies the investigation slot and exposes intervention/residual; show a timed transition/filmstrip with its reduced-motion counterpart before scoring the interaction higher. |
| 14. Copy and conversion | 3 → 4 | Actions, before/after summary and limits are specific and honest; replace the ambiguous branch’s generic “or” sentence with its known two-field explanation. |
| 15. Screenshot test | 3 → 3 | Credible restrained analyst tool, not yet a memorable explanatory composition; make the B-original → B-variant → residual relationship its defining visual grouping. |

**9/15 lines reach 4; none is below 3. Not done by the stop rule:** fewer than 12 lines reach 4, and first-screen/depth remain 3. An exhaustive clean scan/platform matrix is also absent. This judgment does not overturn the approved restrained app direction or imply the synthetic arithmetic failed. R2 improves over R1, so a two-round plateau is not established.

## Exact missing proof and disposition

- **Full acceptance:** this review does not re-exercise or map every AC-1–19 assertion to the exact runnable version. docs/ACCEPTANCE.md still labels all criteria unverified; the successful receipts need an explicit criterion-by-criterion reconciliation before declaring all 19 passed.
- **Keyboard:** demonstrated-state diagnostic/disclosure/export activation, expanded setup controls and relevant failure controls are not covered by the recorded walk. No independent screen-reader pass is supplied.
- **Restart:** browser_check.py shuts down/recreates the HTTP server and Store, reloads the existing page and reopens a packet. It does not close/relaunch the browser process before reopen. This is useful server-restart/export/reopen proof; a browser-process restart claim needs a separate receipt. The acceptance text’s application restart should be described precisely.
- **Offline:** the supplied script blocks nonlocal requests for a result reload; a fresh choose/compare/test/export cycle under that block is not shown. This limits the breadth of the “no external network dependency” receipt, not the observed reload pass.
- **Platforms:** Chromium is explicitly unverified after “Locator.click: Timeout 7000ms exceeded” while waiting for Compare totals to be visible/enabled/stable. WebKit could not launch because libicudata.so.74 is missing. Neither establishes an app defect or pass. Physical Windows scaling, Safari/iPhone and Android are unverified. No platform installation is requested.
- **Accessibility/media/motion:** no actual measured contrast receipt, comprehensive forced-color legibility pass or timed signature/reduced-motion proof is supplied. Width-only media assertions cannot replace these checks.
- **Version invalidation:** tests.txt names test_software_revision_invalidates_old_conclusions as passed, and visible provenance says 0.2.0. I did not independently rerun the old-version import/invalidation path.
- **External outcomes:** live authentication/privileges, real API response compatibility, real server lifecycle/cleanup, native installation/placement, customer demand, analyst usefulness and competitive uniqueness remain unverified. No enterprise account is required for the approved POC. The spec acknowledges existing Strategy Test Center comparisons; the proposed addition is the measured cause-specific experiment and its evidence, not comparison itself.

**Outcome: substantive R1 fixes accepted; no new proven numerical or responsive blocker in the inspected renders. Bounded synthetic demonstration is reviewable with the listed caveats. AC-15 keyboard proof and broad completion claims remain qualified. Not done by the Web Designer Pro stop rule.**
