# Checkpoint 150: 153 of 240 trials complete

Snapshot: October 29, 06:40 Shanghai (October 28, 22:40 UTC). **38 tasks are fully matched**, with two attempts per condition. Cliffy has only bundled repeat 1 complete and is excluded from matched comparisons. This is the fresh60 October26 prompt study; previous studies remain separate.

The Mac mini worker (PID57379) holds the shared lock and is running Cliffy custom repeat1. Its dedicated containers are healthy. **87 primary slots remain.** No worker, model, grader or preflight was launched by this monitoring turn. The original stop barrier, Blender and unrelated wuitu-ota VM remain intact.

## Official scores

| Population | Bundled | Coding override |
| --- | ---: | ---: |
| All 153 completed slots | 53/77 (68.8%) | 61/76 (80.3%) |
| Same 38 fully matched tasks | 52/76 (68.4%) | 61/76 (80.3%) |
| Cliffy bundled repeat1, not yet matched | 1/1 | Not completed |

All153 primary attempts completed normally and passed frozen identity/isolation checks. Nine matched tasks favor custom on two-repeat pass counts, two favor bundled, and27 tie. The net difference is nine passes, or11.8 percentage points, but it is not nine demonstrated functional improvements.

Seven of the eleven favorable custom pass-count differences involve documented official test-overlay/fixture interactions: Updo1, Actionlint1, KCP2, Go-critic2 and Geo1. These raw scores remain unchanged; no diagnostic pass has been assumed. Other differences include Helm warning wording, Kgateway exact-output interpretation, Awilix initialization behavior and SuperJSON filtering order. Bundled gains one each from OPA's missing custom commit and ArkType's nested-recursion failure. These are descriptive interim results, not a capability-winner claim or a significance test.

## Efficiency on matched tasks

Equal task weight; both repeats and every primary outcome retained. Agent time excludes setup, grading and controller downtime. Cliffy's partial result and archived interruptions are excluded.

| Mean per attempt | Bundled | Coding override | Change |
| --- | ---: | ---: | ---: |
| Agent time | 21.0 min | 17.4 min | −16.7% |
| Output tokens | 35,897 | 27,242 | −24.1% |
| Outer tool calls, including polls | 32.3 | 26.1 | −19.1% |
| Uncached input tokens | 94,130 | 88,724 | −5.7% |

Custom is faster on33/38 task means and produces less output on35/38. Median task-relative time change is−17.7%. Uncached input is less consistent: lower on22/38 tasks, with median change−0.9%. These whole-prompt differences do not identify a particular clause as the cause, or prove all omitted work was unnecessary.

## Visible behavior and code

All152 matched attempts inspect relevant implementation before editing. New repository test files appear in76/76 bundled attempts versus7/76 custom attempts. The custom count includes both state-data runs, whose project explicitly mandates test-first development and branch coverage. Temporary application clients are still generated code; fewer committed tests does not mean no validation.

- **Mnamer daemon: both conditions pass2/2.** Bundled adds769/655 repository-test lines; custom adds none, but both custom runs exercise real CLI subprocesses, files, timed file growth, asynchronous moves and lifecycle commands. The second custom run verifies a real cross-filesystem move's bytes, permissions and modification time. Bundled also uses real CLI lifecycle tests, with injected EXDEV for cross-device paths. No failed functional assertion drives a production repair in these four; several fixes are source-led. Bundled/custom mean agent time is15.2/12.6minutes. Production additions are567/596 versus522/538, so the size difference is not only tests, but this is no general complexity rating. Both prompts vary internally: first repeats skip webhooks under “no network”; second repeats implement optional HTTP and mock it during checks. Official passes do not settle that wording ambiguity.
- **State data: all four fail the same API boundary.** The implementation returns`{}` for an active state without declared data, while official tests expect`None`. Each passes69/72 feature tests and1286/1286 existing tests. Their own extensive tests/docs preserve the empty-dictionary interpretation. Test-first development, high coverage and opposite-direction review did not independently resolve this expectation. The brief does not explicitly distinguish omitted data from an empty dictionary. All four zeros remain valid recorded outcomes.
- **Tomlkit: both conditions pass2/2, with real check-driven repairs.** Bundled tests and generated fixture sweeps find conversion/comment/nesting problems; custom's application checks also expose inline-table and array-conversion issues. This is evidence for useful testing in both styles, not a test-versus-no-test comparison.
- **Cliffy, still unpaired:** bundled's added public-API test exposes an environment value overriding config being rejected as a missing required option. It repairs the existing flags validator, then509 scoped tests pass. That is an in-scope defect found by a new test; no prompt comparison is yet available.

## Caveats and remaining work

Twelve bounded grader-only diagnoses remain deferred until the timed queue completes and the shared lock is free. Two provider-interrupted originals remain archived separately; their fresh replacements completed. Known extra usage is475.6agent seconds, with179,269input and10,255output tokens reported for the capacity-interrupted attempt. The401 attempt's tokens are unreported, not measured zero. Three pre-agent image/setup failures are also archived. No new interruption or recovery occurred at this checkpoint.

The post-start interruption amendment, execution-order changes, non-blind visible reviews, two stochastic repeats and whole-prompt comparison remain limitations. No additional reset card was used. Frozen prompts, model settings, memory-off/conveying-only isolation and the queue are unchanged. Continue the remaining87slots; next detailed milestone180. Final task-paired analysis, diagnostics, report, copied-auth removal, dedicated-VM shutdown and monitor deletion remain due at completion.

## Evidence

- [Frozen checkpoint data](checkpoint-150-data.json), [153-slot snapshot](checkpoint-150-results.json)
- [Health record](../infrastructure/monitor-20261028T2240.json)
- [Mnamer four-run comparison](../review/mnamer-all4-comparison.json), [state-data comparison](../review/statemachine-all4-comparison.json)
- Per-trial evidence under`behavior/` and`review/` retains visible call/output references and original patches/grades. No hidden reasoning was reviewed and no benchmark product was rerun for this report.
