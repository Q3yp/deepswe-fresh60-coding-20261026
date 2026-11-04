# Test-overlay diagnostic regrading (2026-11-01)

> **Scope note:** These are post-hoc diagnostic scores, not replacements for the original published primary scores ([`report/final-report.md`](file:///C:/Users/padyu/Documents/gpt-trial/deepswe-fresh60-coding-20261026/report/final-report.md)). All 60 tasks and both repeats (120 attempts per condition) remain in the denominator. Only the 12 documented test-overlay/fixture cases from [`infrastructure/fixture-diagnostics-final-disposition.json`](file:///C:/Users/padyu/Documents/gpt-trial/deepswe-fresh60-coding-20261026/infrastructure/fixture-diagnostics-final-disposition.json) were regraded, with byte-identical production implementations (`model.patch`).

## 1. Score comparison (Original vs. Diagnostic adjusted)

| Condition | Original primary | Diagnostic adjusted | Additional passes |
|---|---:|---:|---:|
| Bundled (`prompts/bundled.md`) | 84/120 (70.0%) | **91/120 (75.8%)** | **+7** |
| October 26 coding (`prompts/override-coding.md`) | 94/120 (78.3%) | **94/120 (78.3%)** | **0** |
| **Coding minus Bundled** | **+10 passes (+8.33 pp)** | **+3 passes (+2.50 pp)** | **-7 net gap** |

- **Task-paired bootstrap 95% confidence interval (100,000 draws, RNG seed `20261101`):** `-2.50` to `+7.50` percentage points (vs. `+1.7` to `+15.8` pp on original primary scores).
- **Exact task-paired two-sided sign-flip test:** `p = 0.5078` (vs. `p = 0.03967` on original primary scores).
- **Task-level win/loss/tie breakdown (out of 60 tasks):**
  - Before diagnostic repair: Coding won **11** tasks, Bundled won **3** tasks, **46** ties.
  - After diagnostic repair (`+7` passes across 5 Bundled tasks):
    - `updo-policy-alerting`: `1/2 vs 2/2` -> **`2/2 vs 2/2`** (tie)
    - `actionlint-action-pinning-lint`: `1/2 vs 2/2` -> **`2/2 vs 2/2`** (tie)
    - `kcp-go-multiplexed-kcp-streams`: `0/2 vs 2/2` -> **`2/2 vs 2/2`** (tie)
    - `go-critic-doc-link-checker`: `0/2 vs 2/2` -> **`2/2 vs 2/2`** (tie)
    - `geo-shapeindex-serialization`: `1/2 vs 2/2` -> **`2/2 vs 2/2`** (tie)
  - Diagnostic-adjusted task wins: Coding wins **6** tasks (`awilix`, `kgateway`, `helm`, `superjson`, `optique`, `testem`), Bundled wins **3** tasks (`opa`, `arktype`, `mashumaro`), **51** ties.

---

## 2. Replayed 12 test-overlay / fixture cases

| # | Submitted attempt | Condition | Original | Feature tests (F2P) | Regression tests (P2P) | Diagnostic binary result | Outcome category |
|---:|---|---|---:|---:|---:|---:|---|
| 1 | `wazero-multi-module-snapshots--bundled--r1` | Bundled | 0 | 77/78 | 2/2 | **0** | Semantic edge failure (incremental from incremental baseline) |
| 2 | `wazero-multi-module-snapshots--bundled--r2` | Bundled | 0 | 77/78 | 2/2 | **0** | Semantic edge failure (incremental from incremental baseline) |
| 3 | `updo-policy-alerting--bundled--r2` | Bundled | 0 | 17/17 | 123/123 | **1** | **Recovered pass (+1)** |
| 4 | `actionlint-action-pinning-lint--bundled--r1` | Bundled | 0 | 55/55 | 145/145 | **1** | **Recovered pass (+1)** |
| 5 | `prometheus-transactional-reload-status--bundled--r1` | Bundled | 0 | 10/15 | 82/82 | **0** | Semantic contract failure (float vs. int64 ms timings) |
| 6 | `kcp-go-multiplexed-kcp-streams--bundled--r1` | Bundled | 0 | 30/30 | 12/12 | **1** | **Recovered pass (+1)** |
| 7 | `kcp-go-multiplexed-kcp-streams--bundled--r2` | Bundled | 0 | 30/30 | 12/12 | **1** | **Recovered pass (+1)** |
| 8 | `igel-persist-feature-schema--override-coding--r1` | Coding | 0 | 23/24 | 2/2 | **0** | Semantic contract failure (`exclude=None` on all-removed) |
| 9 | `igel-persist-feature-schema--override-coding--r2` | Coding | 0 | 23/24 | 2/2 | **0** | Semantic contract failure (`exclude=None` on all-removed) |
| 10 | `go-critic-doc-link-checker--bundled--r1` | Bundled | 0 | 3/3 | 16/16 | **1** | **Recovered pass (+1)** |
| 11 | `go-critic-doc-link-checker--bundled--r2` | Bundled | 0 | 3/3 | 16/16 | **1** | **Recovered pass (+1)** |
| 12 | `geo-shapeindex-serialization--bundled--r2` | Bundled | 0 | 24/24 | 599/599 | **1** | **Recovered pass (+1)** |

---

## 3. Remaining failures among the 5 non-passing replayed slots

### 3.1 `wazero-multi-module-snapshots--bundled--r1` & `r2` (`77/78 F2P`, `2/2 P2P`)
- **Failing test:** `[f2p] github.com/tetratelabs/wazero/experimental/snapshot.TestCoordinator_CaptureIncremental_FromIncrementalBaseline`
- **Root cause:** Both implementations reject or fail when capturing an incremental snapshot on top of an incremental baseline ( matching the same `77/78` F2P semantic failure seen in the `override-coding` attempts).

### 3.2 `prometheus-transactional-reload-status--bundled--r1` (`10/15 F2P`, `82/82 P2P`)
- **Failing tests (5):**
  - `[f2p] github.com/prometheus/prometheus/cmd/prometheus.TestReloadStatusEndpointAndStateFile_BlackBox`
  - `[f2p] github.com/prometheus/prometheus/cmd/prometheus.TestTransactionalConfigReload_ConcurrentReloadRequestsConverge`
  - `[f2p] github.com/prometheus/prometheus/cmd/prometheus.TestTransactionalConfigReload_RollsBackOnPartialApplyFailure`
  - `[f2p] github.com/prometheus/prometheus/cmd/prometheus.TestTransactionalConfigReload_Sequence_45ReloadAttemptsMaintainInvariants`
  - `[f2p] github.com/prometheus/prometheus/cmd/prometheus.TestTransactionalConfigReload_SuccessfulReloadUpdatesStatusAndSuccessMetric`
- **Root cause:** Returns fractional millisecond timings that the official Go test decoder (`map[string]int64`) expects as integers (matching the same `10/15` F2P failure in `bundled--r2` and `override-coding--r1/r2`).

### 3.3 `igel-persist-feature-schema--override-coding--r1` & `r2` (`23/24 F2P`, `2/2 P2P`)
- **Failing test:** `[f2p] tests.test_igel.test_feature_schema_persistence.test_fit_rejects_when_all_features_are_removed`
- **Root cause:** Both implementations fail the all-features-removed case because the official test passes `exclude=None` and the implementation's strict null-option validation rejects `None` before reaching the empty-feature check (matching the exact `23/24` F2P result already observed in `igel-persist-feature-schema--bundled--r1` & `r2`).

---

## 4. Repair methodology & audit constraints

1. **Zero model or production edits:** No new model executions, no production code edits, no altered expected outcomes, and no retries of completed diagnostic failures. Every submitted `model.patch` was verified byte-for-byte identical after replay.
2. **Scoped test/fixture repairs only:**
   - Restored exact overwritten model test helpers where the official `test.patch` overwrote shared test files.
   - Renamed colliding model test symbols (`TestHandleWebhookDecisionWithHeaders`, duplicate Go helper declarations).
   - Preserved retained `go-critic` fixture doc-link inputs and `Record` declaration.
   - Permitted `igel` fixture monkeypatching of an absent unused temporary-path attribute via `raising=False`.
3. **Impact on test-effectiveness accounting (`240` slots):**
   - In `bundled`, the **7 recovered slots** (`updo` B2, `actionlint` B1, `kcp-go` B1/B2, `go-critic` B1/B2, `geo` B2) were pure grader-overlay false negatives: the model's production code was 100% compliant with all official F2P and P2P assertions, and only failed because the saved model tests collided with the evaluator's `git apply` test overlay.
   - The other **5 replayed slots** (`wazero` B1/B2, `prometheus` B1, `igel` C1/C2) were masked by overlay/fixture crashes in the primary run, and after repair reveal the **exact same underlying semantic contract disagreements** (`77/78`, `10/15`, `23/24` F2P) as their sibling runs.
