# Synthetic adapter contract v1

This is a local, record-backed simulation, not a captured or certified Strategy REST schema. Every response/packet is labeled “Proof of concept — simulated Strategy connection”; live integration is not tested.

`SimulatedAdapter(case).execute(report, overrides=None)` captures a locally designed report instance: reference/name, original or transient prompt/filter selections, exact total/minor-unit string, selected/non-null row counts, declared snapshot, definition fingerprint and completeness. No arbitrary SQL is parsed or executed. `cleanup()` releases only this adapter's own in-memory instance records.

The case shape is `synthetic-case-v1`, two grid report references in one project, a fixed synthetic records array, and metric/unit/scale/grain/snapshot context. Every amount is a decimal string or null; `SUM(amount)` is the only calculation implemented. Only status and region selections are modeled. Numeric comparisons and rendering preserve exact decimal strings.

The operation boundary is informed by Strategy's official [report execution workflow](https://microstrategy.github.io/rest-api-docs/common-workflows/analytics/manage-reports/manage-report-objects/execute-report/) (checked October 24, 2026): instance creation, runtime prompts, result retrieval and optional SQL view. A real adapter would translate those deployment-specific payloads and prove authorization, data context, totals/pagination, asynchronous jobs and cleanup. These method/field names are ours; no direct endpoint or authentication compatibility is claimed.

Injected conditions are deterministic local failures. One automatic retry is permitted for a simulated transient/rate-limit failure; Retry-After is 50 ms within the 5-second execution deadline. Denial/session expiry are not retried. Cancellation never converts a partial attempt into a diagnosis. In-memory cleanup proves only local lifecycle accounting.

The evidence packet `synthetic-evidence-v1` contains the exact case, results, cleanup claims, software version and SHA-256 of canonical JSON. A hash detects alteration but is not a signature or trusted attestation. On reopen, the source case is validated and arithmetic/diagnosis recomputed; mismatching conclusions are rejected. Historical instance IDs are replaced by newly computed instances. No tokens, customer data, warehouse credentials or live identities are used.

The browser talks only to its local HTTP server, using the project's own case/job/export endpoints. Same-origin write checks prevent cross-origin mutation. These local routes are not Strategy routes. There is no LLM, paid API, external script, analytics or hosted font dependency.

Existing overlap: [Test Center](https://www2.strategy.com/producthelp/current/workstation/en-us/Content/test_center.htm) already compares report/baseline outputs. This POC tests a cause-specific prompt experiment and evidence review; it does not establish a missing market capability. Future work should reuse available comparison evidence.
