# Checkpoint 60: one quarter complete

Snapshot: October 27, 16:38 Shanghai (08:38:51 UTC). All 15 completed tasks have two attempts per condition. There are no partially matched tasks in this snapshot. The existing worker holds the shared lock and is running the first custom Pwntools trial, slot 61.

## Official completion

| Condition | Official passes | Rate |
| --- | ---: | ---: |
| Bundled Codex instructions | 21/30 | 70.0% |
| October 26 coding override | 25/30 | 83.3% |

All 60 attempts completed normally and passed identity, frozen-prompt and isolation attestation. Memory remains disabled and only conveying is enabled. These are original official scores, including every zero; no diagnostic grades replace them.

The four-pass difference comes from four tasks, each contributing one additional custom pass:

- **Updo and Actionlint:** one bundled attempt in each hits a collision between model-written tests and the official test overlay. These two differences cannot establish a functional advantage.
- **Kgateway:** both bundled attempts and one custom attempt emit an explicit `google_re2: {}` where the official golden output omits it. The task does not specify that representation detail. This is an exact-output mismatch, not an observed live hashing failure, and runtime equivalence has not been established.
- **Awilix:** bundled repeat 2 starts an unrelated inherited parent singleton when initializing a scope. The official scenario expects only the scoped dependency to initialize. Its own new tests encode the same mistaken startup policy, so they do not expose it.

The other 11 tasks tie. This mixed four-pass gap does not yet demonstrate a general capability improvement.

## Efficiency on the same 15 tasks

Means include both repeats and all outcomes. Every task has equal weight. Agent time excludes image setup, official grading and controller downtime.

| Mean per attempt | Bundled | Coding override | Change |
| --- | ---: | ---: | ---: |
| Agent time | 21.6 min | 18.5 min | −14.7% |
| Output tokens | 37,417 | 28,450 | −24.0% |
| Outer tool calls, including polls | 38.3 | 31.7 | −17.4% |
| Uncached input tokens | 103,697 | 101,996 | −1.6% |

Custom has lower task-mean time on 13/15 tasks and lower output on 14/15. Its median task-relative time change is −16.8%. Scriggo is a substantial exception: custom averages 45.6 minutes versus bundled 32.2 minutes, with all four attempts passing. Aiomonitor is also slightly slower under custom. These are descriptive interim results, not significance tests or billed-cost estimates.

## What changed in visible behavior

All 60 reviews find relevant implementation inspection before the first code edit. New repository test files appear in **30/30 bundled attempts and 3/30 custom attempts**. The custom exceptions are one Vitest attempt and both Kgateway attempts. Custom Scriggo repeat 2 re-enables three existing tests without adding test bodies.

Custom still generates temporary programs, drivers and fixtures. That moves validation outside the repository; it does not eliminate validation. Some programs compare against an independent oracle, while others only print results.

Scriggo makes the distinction concrete. Both conditions catch real interface-dispatch and pointer compound-assignment defects. Custom examples execute the same source under Scriggo and Go and compare outputs; they also expose addressable-field, array-write and interface-storage problems. Existing tests catch regressions introduced by those changes. Bundled repeat 2 separately catches nil-function receiver behavior through a new asserted program. These checks do find real problems, but they do not remove the need for an independent expected result. The Awilix failure shows how an implementation and its tests can agree on the wrong interpretation.

More local discoveries also mean more iteration. Scriggo’s custom runs are slower and generate more output despite adding no new test files. Fewer committed tests is therefore not a reliable proxy for fewer checks or less work.

## Implementation differences

The effects are not uniformly simpler or more complete. Custom Mobly uses the platform’s `threading.Barrier`; bundled builds separate synchronization machinery. On Kysely, bundled helpers infer the referenced column type plus null by default, while custom uses `unknown` unless the caller supplies an output type. Both pass the official checks.

Scriggo’s solutions all register per-type methods and use the existing VM call machinery. One custom repeat centralizes storage/address handling and adds a callable-identity map after a concrete failure. The other wraps native interface types to reuse existing composite storage. Bundled repeat 2 also centralizes storage conversion. These differences cannot be reduced to line count, comment count, or an isolated prompt-clause effect.

## Grading, infrastructure and remaining work

Five earlier bundled test-overlay collisions remain queued for grading-only diagnostics after the timed queue finishes: two Wazero, one Updo, one Actionlint and one Prometheus. Original scores will remain separate. Kgateway’s golden mismatch is not an infrastructure fault and will not trigger a retry. Prometheus’s fractional-millisecond encoding failures also remain valid recorded zeros, with the previously documented task-contract caveat.

No worker, model, grader or preflight was restarted at this checkpoint. The earlier Vitest image-pull recovery occurred before model execution and reused completed scores. The mini has 63 GiB free; Blender, the original stop barrier and unrelated wuitu-ota remain intact.

**180 slots remain across 45 tasks**, including the current trial. Hourly monitoring continues; the next detailed report is at 90 completed slots. Final inference will be task-paired, with both repeats retained, prior studies separate, and the non-blind review, small repeat count, model-time drift and Rosetta/harness limitations explicit.

## Evidence and validation

[Frozen plan](../experiment-plan.json), [checkpoint calculations](checkpoint-060-data.json), [fixed 60-row snapshot](checkpoint-060-results.json), [per-attempt reviews](../behavior/), [health receipt](../infrastructure/monitor-20261027T0838.json).

New native reward, attestation, isolation and source-reference checks were read-only. Report arithmetic was cross-checked against native rewards and retained rows. The inline comparison was inspected at desktop and narrow widths; no benchmark execution was used to validate the report.
