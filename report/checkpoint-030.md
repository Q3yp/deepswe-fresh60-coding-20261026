# First checkpoint: 31 of 240 slots scored

Snapshot: October27, 03:40 Shanghai (2026-10-26T19:40:50Z). Seven tasks have all four attempts; Prometheus has three of four. The existing worker6930 holds the shared lock, its current Prometheus bundledr2 container is running, and its proxy is healthy. No worker, model or grader was restarted during this checkpoint.

## Completion and official scores

| Population | Bundled | October26 coding override |
| --- | ---: | ---: |
| All31 scored slots, unequal denominators | 10/15 (66.7%) | 12/16 (75.0%) |
| Seven fully matched tasks, two repeats each | 10/14 (71.4%) | 12/14 (85.7%) |
| Incomplete Prometheus task | 0/1 | 0/2 |

All31 attempts completed normally and passed identity, exact-prompt and isolation attestation. There were no provider interruptions. Memory remains disabled; only conveying is enabled. Scores are the original official binary outcomes, with every zero retained.

The matched score difference comes entirely from Updo and Actionlint, each with one bundled-side test-overlay collision. Wazero is zero for all four attempts, with bundled collisions and custom semantic failures. The raw lead therefore does not establish a completion advantage. No adjusted scores are available yet.

## Efficiency on identical tasks and repeats

These means include all28 attempts from the seven fully matched tasks, including failures. Each task contributes two attempts per condition. Prometheus is excluded from this table until its fourth attempt completes. Agent time excludes image setup, official grading and controller downtime.

| Per-attempt mean | Bundled | Coding override | Change |
| --- | ---: | ---: | ---: |
| Agent execution | 20.7min | 16.8min | −18.5% |
| Output tokens | 33,074 | 22,999 | −30.5% |
| Outer tool calls, including polls | 27.9 | 22.9 | −17.9% |
| Uncached input tokens | 85,114 | 85,362 | +0.3% |

The custom condition has lower task-mean time and output tokens on all seven tasks. Its median task-relative time change is −16.1%. This is an early descriptive pattern, not a significance claim or a billed-cost estimate. Total input tokens are mostly cached; lower output does not imply every resource measure fell.

## Visible behavior and implementation

Both conditions inspect implementation before editing and exercise normal entrypoints on these seven tasks. The clearest observed difference is where validation code goes: all14 bundled attempts add repository test files; one of14 custom attempts does, on Vitest. Custom attempts still generate temporary clients, drivers and fixtures, so this is not a comparison of testing against no testing. Some temporary programs assert results; others only print observations. Exit0 from the latter is not automatic semantic proof.

Tests sometimes catch actual integration bugs. Existing Actionlint SARIF checks reveal missing rule metadata in two bundled attempts and one custom attempt; production fixes follow the failures. Textual animation checks also drive repairs. Conversely, bundled Vitest r2 initially rejects an allowed Infinity value, and its own tests encode the same assumption. Source review corrects both code and tests without a failed test exposing the mistake. Tests and source review contribute different evidence; neither eliminates an incorrect oracle.

Coding differences are concrete but not uniformly better or worse. On Mobly, both custom attempts reuse native threading.Barrier; bundled attempts implement separate condition/generation machinery. On Vitest, custom attempts inline configuration validation and restrict history catches to reading/parsing, while bundled extracts configuration helpers and uses broader history catches. All four requested Vitest helper modules are in scope. Custom Vitest r2 also returns early for hash sharding before slow-file isolation, a code-derived coverage gap despite its official pass. These observations do not isolate the effect of any one prompt clause or equate fewer lines with correctness.

## Latest task: Prometheus

Both custom attempts run asserted Python clients against actual Prometheus processes, covering reload, rollback, persistence, restart and corrupt state. Those scenarios pass, as do their focused existing/OpenAPI checks. Compilation catches a YAMLv3/v4 schema-type mismatch, which each repairs. No failed local behavioral check drives a reload implementation repair.

Their official scores remain0: each passes10/15new tests and82/82existing tests. Five new tests reject fractional millisecond values because the official Go client decodes reloader_timings_ms into map[string]int64. The supplied task names the timing field but does not explicitly require integer encoding. This is a concrete client-contract gap, with an underspecified encoding caveat, not evidence that rollback itself failed. No regrading or production repair is being used to remove these zeros.

Bundledr1 adds repository unit and live-process integration tests. Its local selected suites and focused race check pass. The official tagged suite cannot build because both its new test file and an official test file declare getReloadStatus. Native counts are0/15new and80/82existing, with17 IDs missing, not17 executed semantic failures. Its implementation also emits fractional timings, so removing the collision would not establish a pass.

## Infrastructure and remaining work

There are now five documented, deferred grading-only collision diagnoses: two Wazero, one Updo, one Actionlint and one Prometheus. They will run only after the timed model queue finishes and releases the shared lock, in separate copies with production patches unchanged. Original scores remain primary records and diagnostic grades will be separate.

The earlier Vitest image-pull timeout happened before any model or grader ran. Its complete record was archived; recovery fetched the exact existing image and reused all24 then-scored slots. It was not a model retry. No additional infrastructure repair was needed now. The mini has72GiB free; Blender, the old operator-stop barrier and unrelated wuitu-ota remain intact.

There are209 unscored slots, including the current one. The next detailed report is due at60; hourly health checks continue. The final240-slot report will use task-paired statistics, preserve prior studies separately, and document the small-repeat, non-blind-review, harness and environment limitations. This checkpoint makes no winner, leaderboard or clause-causality claim.

## Evidence

- [Frozen analysis plan](../ANALYSIS-PLAN.md), [checkpoint calculations](checkpoint-030-data.json), [immutable scored-row snapshot](checkpoint-030-results.json).
- [Per-attempt visible-behavior reviews](../behavior/), [latest Prometheus bundled review](../behavior/prometheus-transactional-reload-status--bundled--r1.json), [customr1](../behavior/prometheus-transactional-reload-status--override-coding--r1.json), [customr2](../behavior/prometheus-transactional-reload-status--override-coding--r2.json).
- [Prometheus collision diagnosis](../infrastructure/prometheus-bundled-r1-grader-collision.json), [health receipt](../infrastructure/monitor-20261026T1940.json).

Validation: counts compared with native rewards and attestations; new review references checked against retained source files. No benchmark execution was used to validate this report. Inline comparison inspected at desktop and narrow widths before delivery.
