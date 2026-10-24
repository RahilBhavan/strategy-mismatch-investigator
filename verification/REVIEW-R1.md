# Independent verification and design critique — round 1

Reviewed 2026-10-24 against copied revision 3 SPEC/ACCEPTANCE, DIRECTION.md, Web Designer Pro critique/app references, and shared design-system/Tufte guidance. This is a synthetic POC review, not live Strategy verification. No enterprise account is needed. No product code, Git state, external account, issue or PR was changed.

## Independent test method and results

Expected fixture descriptions and arithmetic were written to `verification/independent-cases.json` before reading schema, adapter, investigation logic or existing tests. Only `app.fixtures.example` was read first to learn the case shape. Test cases copy that fixture, replace records with unique IDs and exact decimal strings, and retain two report references. The tests call `validate_case`, `SimulatedAdapter`, `investigate(case, adapter, 'diagnose')` and `cleanup` in a finally block. Each also checks original input fingerprint preservation and release of every created instance.

One initial reference had a reviewer scope error: `equal-different-definitions` used `SUM(amount) + 0`, outside the supported SUM(amount) calculation. Its initial expected arithmetic/status is preserved, rather than silently rewritten. The supplementary `equal-different-status-selections` uses the same independently calculated amounts and selections with supported SUM(amount), supplying the second valid equal-total control. A separate test asserts the unsupported calculation safely abstains. This correction was made after code inspection and is not an independently held-out definition test. The six single-cause cases, the original identical control and the two ambiguous/incomplete cases were frozen before algorithm inspection; the supplemental equal control reuses frozen math.

The frozen ambiguous reference includes a hypothetical variant and residual. The implementation correctly declines that experiment when both status and region differ; the test requires unresolved status and two separate candidates, not those unexecuted numbers. Its frozen residual convention was A minus variant, while the implementation uses variant minus A; executed single-cause residuals are all zero, so no sign mismatch was hidden or scored as a defect.

| Case | A | B | B − A | Variant B with A status | Impact variant − B | Observed |
|---|---:|---:|---:|---:|---:|---|
| fractional-negative | 15.00 | 17.10 | 2.10 | 15.00 | -2.10 | Demonstrated; residual 0.00 |
| reverse-selection | 7.00 | 10.50 | 3.50 | 7.00 | -3.50 | Demonstrated; residual 0.00 |
| renamed-statuses | 15.00 | 0.01 | -14.99 | 15.00 | 14.99 | Demonstrated; residual 0.00 |
| two-specific-selections | -10.50 | 2.25 | 12.75 | -10.50 | -12.75 | Demonstrated; residual 0.00 |
| zero-baseline | 0.00 | 1.05 | 1.05 | 0.00 | -1.05 | Demonstrated; percentage unavailable |
| negative-both | -10.25 | -10.00 | 0.25 | -10.25 | -0.25 | Demonstrated; residual 0.00 |
| equal-identical | 0.00 | 0.00 | 0.00 | Not run | Not run | Equal; no equivalence claim |
| equal-different-status-selections | 7.20 | 7.20 | 0.00 | Not run | Not run | Equal; no equivalence claim |
| overlapping-selections | 20.00 | 3.30 | -16.70 | Not run | Not run | Unresolved; status and region candidates |
| missing-unit | 3.25 | 2.50 | Not comparable | Not run | Not run | Unresolved; missing unit identified |

In-scope reference outcomes: **10/10 correct: 6 demonstrated, 2 equal, 2 appropriate abstentions; 0 false explanations, 0 failures.** Supplementary unsupported-calculation abstention: 1/1. Exact output totals are strings. Negative and fractional impacts, reversed selections, unseen labels and zero-baseline percentage behavior match the references. Successful demonstrations create/release 3 instances; equal and missing/ambiguous controls create/release 2; unsupported calculation creates 0.

Command actually run:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s tests -p test_independent.py -v
```

Result: **11 tests passed**, 0.786 seconds. Existing test source was inspected after expectations were frozen; the existing full suite was not rerun. These tests establish this held-out core behavior, not all 19 acceptance criteria, browser behavior, cancellation races, export/restart recovery or live connectivity. Product code inspection found no additional proven numerical defect in the reviewed path.

## Screens inspected

Opened at full supplied resolution:

- `r1-candidate-1440.png`
- `r1-demonstrated-1440.png`
- `r1-ambiguous-1440.png`

Missing at review time, explicitly checked twice without waiting:

- `r1-demonstrated-390.png`
- `r1-unresolved-390.png`

No live browser was exercised in this round. `browser_check.py` was read as an implementation artifact, not accepted as proof that its checks ran. No phone/tablet, focus, contrast, platform matrix or animation pass is claimed. Additional supplied desktop screenshots exist but were outside the requested three desktop states and were not visually scored.

## Findings and concrete improvements

**No proven core computation defect in the ten in-scope cases.** The dominant uncertainty is missing interaction and responsive evidence. The following visible issues are design/copy findings, not numerical failures or claims of user-study results.

1. **Medium — unresolved explanation does not name both competing changes in its finding.** In `r1-ambiguous-1440.png`, the finding's comparison strip shows only “A status” and “B status”, followed by “The supported single status-selection experiment cannot isolate these differences.” Region West versus all values is visible higher in the report rows, but absent from the explanation itself. Show both status and region differences in the finding, then say “Status and region both differ. This experiment cannot isolate one cause.” Keep the unresolved state and avoid fabricated impacts. This improves inspectability of AC-10's separate candidates; the core result already contains both.
2. **Low — conclusion copy repeats instead of explaining the observed transition.** In the demonstrated PNG, “The status selection explains the gap” is followed by substantially the same sentence, then two business-definition cautions. Replace the summary with “Rerunning B with all statuses changes 180 to 220, closing the 40-unit gap.” Retain one clear business-definition caveat. Use sign-aware wording for negative/reversed cases; do not hardcode these sample values.
3. **Low — the first comparison screen overpromises an explanation in unresolved/equal flows.** The persistent introduction says “Two totals. One measured explanation.” even when the ambiguous finding says a cause cannot be isolated. Use “Compare two totals. Test a possible cause. Inspect the evidence.” This preserves scope without promising every case has an answer.
4. **Verification gap — required phone evidence is absent.** Supply the two named 390px screenshots, including the whole result and open evidence content, then exercise the compare → test → inspect flow with keyboard and narrow viewport. This is a missing review prerequisite, not evidence of an actual overflow. Do not mark AC-15 passed from desktop stills.
5. **Low — experiment sign conventions could be easier to audit.** The demonstrated result labels “Measured change to B” and “Remaining difference from A” are reasonable, but only the original difference explicitly states its subtraction order. Add short definitions “variant − original B” and “variant − A” beside those values or in accessible help, particularly for negative and reversed selections. The tested arithmetic is correct; this is explanation clarity.

The desktop comparison itself is legible and task centered: report names, selections and directly labeled units sit beside the totals; the original delta explicitly says B − A. Candidate does not masquerade as proof. The demonstrated state exposes impact/residual without developer tools. Persistent simulated labeling and “Live integration: not tested” prevent an enterprise-connectivity claim. The evidence accordions promise useful provenance without flooding the main view; their expanded layout was not inspected.

## Rubric scores

Scores apply only to the inspected desktop stills; missing evidence is scored conservatively, not as a proven rendering fault. Brand authority and app.md override poster typography, decorative photos, gradients and theatrical depth. No decorative photo is requested. A calm analytical worksheet can earn a strong score through useful evidence and interaction.

| Rubric | Score / 5 | Visible evidence and single change needed for 5 |
|---|---:|---|
| Concept on the page | 4 | Paired reports and a controlled status experiment communicate reconciliation; show both conflicting fields inside the ambiguous explanation. |
| Not category average | 3 | Familiar worksheet shell fits the job but has little distinctive explanatory composition; make original → controlled rerun → residual a coherent compact sequence. |
| Not slop/rut | 4 | No decorative KPI row, gratuitous illustration or hero split; consolidate repeated finding prose to make every line earn its place. |
| First screen | 3 | Desktop comparison action and originals are prominent, but experiment result extends down-page and phone is unreviewed; prove a compact actionable phone result. |
| Typography | 4 | Clear Inter hierarchy and aligned totals; refine secondary-copy measure and reduce redundant text rather than adding display fonts. |
| Colour | 4 | Orange controls and a restrained demonstrated-state edge on neutral surfaces; verify real contrast/focus across states before a 5. |
| Imagery / evidence material | 4 | Actual synthetic totals/selections are the appropriate visual material; include the measured transition in one immediately auditable grouping. |
| Depth and finish | 3 | Clean bordered worksheet, restrained but largely uniform hierarchy; strengthen result grouping and state transition without decorative shadows. |
| Below first screen | 3 | Finding, evidence disclosures and exports are orderly but repetitive and mostly collapsed; show an expanded, well-composed evidence state. |
| Craft | 4 | No visible clipping or collisions in these desktop screenshots; stress long labels/large exact values and inspect expanded evidence before a 5. |
| Responsive | 2 | Requested 390px evidence absent; supply and inspect it, then verify the complete phone workflow. |
| Everyone's computer | 2 | Stills cannot establish keyboard/platform behavior; provide observed focus, reflow and relevant platform matrix results. |
| Signature | 3 | Candidate and demonstrated occupy the same finding position; inspect the actual transition and reduced-motion behavior before awarding interaction craft. |
| Copy and conversion | 3 | Concrete primary actions and honest limits, with duplicated summaries and an overpromising intro; apply the three copy changes above. |
| Screenshot test | 3 | Credible analyst tool, little unique visual explanation; make the controlled numerical transition the memorable focal point. |

Five highest-value next changes: name both ambiguous filters; replace the demonstrated summary with computed before/after evidence; soften the persistent explanatory promise; supply the phone and keyboard evidence; clarify the experiment sign labels. The per-row final column gives the specific path toward a 5 without demanding decorative analyst-UI content.

**Not done by the stop rule.** Only 6/15 lines reach 4, responsive/platform evidence is incomplete, and this is round 1. This does not mean the synthetic computation failed.

## Product overlap and limits

The supplied revision 3 specification records that Strategy Test Center already compares reports and baselines. A future integration should reuse existing report selection/context, prompt execution, result capture and comparison capabilities where supported, rather than reconstructing the whole product. This POC adds a measured, cause-specific status-selection rerun and its evidence/residual, not the invention of report comparison. This review relies on the supplied spec for that overlap; it performed no new external product research.

Customer usefulness, competitive uniqueness, production scale, real permissions/authentication, actual Strategy instance cleanup/cancellation and native placement remain **unverified / not tested**. No account acquisition is a prerequisite to the approved synthetic POC. The observed simulated arithmetic and cleanup are not proof of any live equivalent.
