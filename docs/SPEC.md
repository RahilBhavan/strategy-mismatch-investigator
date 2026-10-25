# Number mismatch investigator — Strategy integration proof of concept

**One sentence:** A Strategy analyst can explain a numerical disagreement between two reports using reproducible evidence.

**Decision owner:** Rahil. Implementation: local proof of concept, authorized by Rahil.
**Revised:** 2026-10-24, revision 3.
**Status:** IMPLEMENTED synthetic POC — build authorized with “Start” on 2026-10-24. Live Strategy integration is not tested.
**Path:** `docs/SPEC.md` (project mirror; authoritative planning issue is #41).
**Tracker:** spec #41 in a private repository, so the link is not public. This file is the public copy.

## 1. Confirmed scope

Rahil selected Strategy product integration, then clarified: “This is a proof of concept.” The deliverable is a working demonstration of the proposed integrated feature, not a production deployment or a request to obtain enterprise access before starting.

An existing Strategy environment is not a prerequisite for building the POC. Start with synthetic report data and a simulated Strategy adapter shaped around documented workflows. This is a functioning diagnostic demonstration with an integration boundary, not evidence that Strategy authentication, privileges or endpoints work in a real deployment. A live smoke test is optional subsequent evidence when authorized access becomes available.

No proprietary product source, official partnership, deployment/version, customer, real-data access or release channel is assumed.

## 2. Person, occasion and intended result

User: a BI analyst investigating two reports before a business review. The metric owner reviews the explanation and chooses the intended business definition. No named pilot analyst or recent customer incident has been obtained.

Working hypothesis: the analyst otherwise compares prompts, filters, definitions and totals manually. Frequency and effort are unmeasured. Different business definitions are not necessarily defects.

The POC must demonstrate: select two reports → reproduce their totals → identify one supported discrepancy → rerun a diagnostic experiment → inspect an evidence-backed explanation. It must also show an honest unresolved case.

## 3. Evidence and existing overlap

The originating planning issue (private repository, not linked) and its research records contain the original findings. [Test Center](https://www2.strategy.com/producthelp/current/workstation/en-us/Content/test_center.htm) already compares reports and baselines. The POC investigates cause-specific explanation, not a claim that comparison itself is absent or that the feature is unique.

Primary API references checked October 24, 2026:

- [Execute report workflow](https://microstrategy.github.io/rest-api-docs/common-workflows/analytics/manage-reports/manage-report-objects/execute-report/): report instances, prompt answers, results and SQL view. SQL view has a privilege requirement. The target deployment has not been exercised.
- [Embedding SDK samples](https://microstrategy.github.io/embedding-sdk-samples/): examples of web embedding and authentication. They do not establish a native toolbar plugin hook or make this POC an installed Strategy extension.

Use the documented concepts to define the adapter. Locally authored synthetic responses must be labeled as such, not described as captured API responses or certified schema conformance. Retain fields needed for the case without imitating every endpoint. Do not invent undocumented native extension points.

## 4. Must do

1. Present two synthetic report references with metric, prompt/filter, snapshot and unit context.
2. Compute the two original totals from the actual underlying synthetic records.
3. Detect one supported prompt/filter difference deterministically.
4. Rerun the selected diagnostic variant against those records without changing original report definitions.
5. Show evidence, residual delta, uncertainty and the limits of the conclusion.
6. Export/reopen a local synthetic investigation packet for review.
7. Show the future Strategy adapter boundary and what remains unverified live.

## 5. Non-goals

- No enterprise access, account provisioning, SSO setup or production deployment requirement for the POC.
- No real customer data, paid services, external messages, public posting or recurring automation.
- No editing saved reports, metric certification or deciding which business definition is correct.
- No direct warehouse connection, arbitrary generated-SQL replay, DAX/Tableau translation or cross-project comparisons.
- No full reproduction of Strategy Library, Test Center or its permission system. A simulated denied response tests our failure behavior only.
- No LLM dependency for determining the cause. No hardcoded explanation paired with a hardcoded total.

Join fan-out, null/distinct counting diagnosis, timezone transformation and refresh reconstruction remain NEXT. This keeps the first POC centered on one demonstrable mechanism. Existing synthetic examples are reference material, not a claim that a diagnostic feature has already passed.

## 6. Proposed decisions and open questions

- **ASSUMED 2026-10-24:** One analyst, one synthetic project, two grid-style reports, one selected aggregate total and a fixed synthetic data snapshot. No login is needed for the demonstration.
- **ASSUMED 2026-10-24:** First cause is different status prompt/filter selections on the same metric. The diagnostic experiment changes a transient selection, never the saved original definitions.
- **ASSUMED 2026-10-24:** Deterministic core, a contract-shaped simulated adapter and a browser comparison view. A real Strategy adapter is a separate implementation step sharing the evidence interface; interface reuse does not prove it will connect without changes.

No remaining access question blocks POC development after build authorization. Open: named analyst/reviewer, demonstration deadline, and a target deployment for an optional live smoke test. No customer-value or live-integration claim is possible without that evidence. No new environment question is required from Rahil now.

## 7. Outcome contract and estimate

Desired change: turn conflicting totals into a reviewable numerical explanation without inventing a cause.

Raw evidence: synthetic source records, report definitions, prompt/filter selections, fixed snapshot ID, original computations, controlled experiment and residual. Source versions and software version bind each result to its inputs.

Method: establish comparability → reproduce → isolate one supported change → recompute → inspect residual → report limits.

Independent check: a reviewer authors expected answers for unseen fixture variants before running the POC. Passing a prepared demo alone does not show general diagnosis.

POC stopping condition: all [19 revised acceptance criteria](ACCEPTANCE.md) pass, the exact runnable artifact is reviewed, and the evidence receipt labels functional proof separately from unverified live behavior. Analyst usefulness and commercial need remain unobserved until a separate pilot.

Proposed effort: **4–6 focused engineering days after scope agreement and project setup**, excluding optional live access/setup and interview scheduling. This replaces the 7–11-day integrated-pilot estimate. No calendar deadline or release commitment is set.

Must not touch Orbit's database/service/port 8791, live report definitions or external accounts. Planning does not scaffold or implement the feature.

## 8. POC workflow

**Choose:** select report A and B from the synthetic catalog. Show “Proof of concept — simulated Strategy connection” persistently. Use generic report UI with Strategy's verified design roles; do not depict this as an official product release.

**Compare:** show metric, prompts, filter definitions, unit/scale, grain and snapshot. Compute A/B from records, then signed delta `B - A`. Incomparable metadata blocks diagnosis; matching timestamps alone are not snapshot proof.

**Investigate:** identify the prompt/filter difference and propose one controlled transient selection. Rerun it through the adapter/core. Show changed selection, measured impact and remaining delta. Do not silently adopt a business definition or modify originals.

**Inspect:** present a short explanation with expandable evidence: originals, aggregate counts, experiment, residual, unknowns and source fingerprints. Distinguish “candidate,” “numerical cause demonstrated on synthetic data,” and “not enough evidence.” No confidence percentage.

**Review/export:** produce local JSON and a readable report for the synthetic investigation. Reopen the packet after restart with its original evidence versions. Changed inputs invalidate the result. No automatic sends, publishing or live-data retention are involved.

Required empty/failure states:

- Empty: “Choose two reports to investigate.”
- Invalid/unsupported input: “Cannot compare these reports.” Identify the invalid field or unsupported type.
- Incomparable context: “Not enough evidence to compare these totals.” Identify missing/conflicting units, grain or snapshot.
- Executing: “Reproducing the report totals…” with Cancel.
- Simulated denial: “Required report evidence is unavailable.” Do not treat denial as zero rows.
- Simulated session expiry: “The connection session expired.” No privileged fallback; label this an injected condition.
- Failure: “Could not reproduce this report.” Offer Retry; no partial diagnosis.
- Equal: “No numerical difference in these captured results.” No semantic-equivalence implication.
- Changed context: “Report context changed. Capture a new comparison.”
- Canceled: “Investigation canceled. No conclusion was produced.”

## 9. Data and architecture

Synthetic input: a small versioned orders dataset, stable report/project IDs, metric definition, report prompt/filter definitions, declared unit/scale/grain and common snapshot identity. Proposed POC limits: one investigation at a time, at most 100,000 synthetic records and 20 MB per case. Missing context is not guessed.

Adapter operations: discover/select supported report references; capture accessible context; execute original/diagnostic report instances; retrieve complete totals; track cancellation/expiry. The simulated implementation must perform computations, not return canned success totals. Its contract records version and known differences from the official API. A live implementation later handles actual authentication, pagination, async execution, privileges and server cleanup.

Domain output: comparability, original values/delta, candidates, controlled-variant output, residual, source/version pointers, unknowns and attributed review notes. Raw auth material never belongs in a case.

Separate adapter/capture, deterministic investigation and browser presentation. Keep network calls out of domain reasoning. Use exact scaled integer/decimal representation with declared units; preserve null versus zero. Reject incomplete totals, overflow and unsupported calculations. Formatting is not the numeric source of truth.

## 10. Sequence

### Slice 1 — Working comparison and adapter boundary (estimate: 1–2 days)

Create a synthetic catalog, record-backed original execution, validated evidence interface and browser selection/comparison flow. Show simulated-source labeling and incomplete-context behavior. Include adapter contract notes identifying documented versus locally designed fields. Check AC-1–4, AC-6 and AC-8.

### Slice 2 — Demonstrated prompt/filter explanation (estimate: 1–2 days)

Implement transient selection experiments, evidence excerpts and residuals. Verify that changing fixture values changes computed totals/explanations. Add equal-result and multi-difference controls. Check AC-5, AC-7 and AC-9–12.

### Slice 3 — Recovery, review and independent check (estimate: 2 days)

Complete retry/cancel/error states, local export/reopen, input invalidation, browser/keyboard review and held-out evaluation. Exercise AC-13–19 and any remaining criteria. Record actual observations against the exact artifact.

First cuts: percentage display and cosmetic report styling. Never cut recomputation, evidence, unknown states, honest simulated labeling or held-out checks.

### Optional subsequent milestone — Live Strategy smoke test

When a permitted environment becomes available, record build/project, auth/privileges, two allowed reports, supported routes, shared data context and approved evidence handling. Replace the simulated adapter for that exact path; exercise one original comparison, controlled runtime-prompt experiment, denial and transient-instance cleanup. Do not automatically turn simulated checks into live passes.

Live integration is separately “verified,” “failed,” or “not tested.” This milestone requires its own estimate after access; it is not a dependency for completing the synthetic POC and is not included in the 4–6-day estimate. Native Library placement remains a separate supported-hosting question.

## 11. Validation and business limits

A reviewer supplies unseen synthetic values and prompt/filter variants, equal-total controls, incomplete context and interacting differences. Measure correct numerical explanations, false explanations and abstentions separately. Include setup and review time if later comparing with an analyst's manual workflow; reusing an already-solved incident biases timing.

The POC can prove its computation, explanation, evidence handling and adapter design on synthetic cases. It cannot prove enterprise connectivity, real privilege behavior, production scale, workload safety, native extension installation, customer demand or revenue impact. A positive demo is not permission to publish or claim employment/contribution to Strategy.

## 12. Change log

- **r1, 2026-10-24:** standalone local SQL prototype; 17 criteria; 5–7-day estimate. Superseded.
- **r2, 2026-10-24:** Strategy integration selected; 19 integration criteria; 7–11-day estimate after access. Added identity, evidence policy and lifecycle checks; limited initial diagnosis to prompt/filter differences.
- **r3, 2026-10-24, IN by clarification “This is a proof of concept”:** retain Strategy integration as the intended product context; replace mandatory live environment with a transparently simulated, record-backed adapter for POC delivery. Rewrite AC-1–19 for functional POC evidence, net zero criteria; move live auth/permissions/hosting/retention proof to an optional subsequent milestone with no claimed pass. Estimate becomes 4–6 days for the POC, 3–5 fewer days than the previous range endpoints. No deadline, enterprise access or build authorization inferred.

Future scope changes require IN/NEXT/TRADE treatment with criterion and effort impacts. Full-spec sign-off is not inferred from selecting a deployment direction or clarifying POC scope.

## 13. Sign-off

Direction confirmed: proof of concept for a Strategy product integration. Rahil authorized the revised POC build with “Start” on 2026-10-24. The runnable implementation is this repository; its verification/ACCEPTANCE-RECEIPT.md maps all 19 criteria to observed synthetic checks. Live Strategy connection, customer usefulness and production readiness remain untested. No customer data is used.
