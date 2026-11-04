# Checkpoint 120: 122 of 240 trials complete

Snapshot: October 28, 19:40 Shanghai (11:40 UTC). Thirty of this fresh study’s 60 tasks are fully matched, with two attempts per condition. Go-critic has one completed attempt per condition and is reported separately. These are not the 30 tasks from the earlier study.

The existing Mac mini worker (PID 41064) holds the shared lock. At the health check, Go-critic custom repeat 2 was in official grading. No worker was dispatched or trial rerun this checkpoint. Blender, the original stop marker and the unrelated wuitu-ota VM remain intact. **118 primary slots remain.**

## Official results

| Population | Bundled | October 26 coding override |
| --- | ---: | ---: |
| All 122 completed slots | 42/61 (68.9%) | 49/61 (80.3%) |
| Same 30 fully matched tasks | 42/60 (70.0%) | 48/60 (80.0%) |
| Go-critic first pair, excluded from matched comparison | 0/1 | 1/1 |

All 122 primary attempts completed normally and passed frozen-prompt/model identity and isolation checks. All original valid zeros remain. Normal completion does not prove delivery: OPA custom repeat 2 ended without the required commit, so the official collector submitted an empty patch.

Six matched tasks favor custom on pass counts, one favors bundled, and 23 tie. The six-pass net difference is not six clear functional improvements:

- Four custom points come from official test-overlay collisions affecting bundled Updo, Actionlint and both KCP trials.
- Helm’s one-point difference depends on warning spelling, despite all four implementations passing its 47 feature checks.
- Kgateway’s difference involves an underspecified exact-output requirement; Awilix’s involves inherited-singleton startup behavior.
- OPA gives bundled one point because custom repeat 2 did not deliver the requested commit.

No interim significance test or capability-winner claim is made. The primary scores stay unadjusted even where grading artifacts are documented.

## Efficiency on the 30 matched tasks

Equal task weight, both repeats and all outcomes retained. Agent time excludes setup, grading and controller downtime. Go-critic’s partial pair and archived interrupted attempts are excluded.

| Mean per attempt | Bundled | Coding override | Change |
| --- | ---: | ---: | ---: |
| Agent time | 21.3 min | 18.2 min | −14.6% |
| Output tokens | 36,950 | 28,120 | −23.9% |
| Outer tool calls, including polls | 33.5 | 27.4 | −18.1% |
| Uncached input tokens | 94,921 | 90,162 | −5.0% |

Custom is faster on 25/30 task means and produces less output on 28/30. Median task-relative time change is −16.4%. Uncached input is less consistent: custom is lower on 15/30 tasks, with a median change of +0.2%. Thus the reduction is clearest in time and generated output, not uniformly in fresh input consumption.

These are whole-prompt differences. They do not isolate which instruction causes the savings, nor establish that every omitted check was unnecessary.

## Behavior and code

All 120 matched attempts inspect relevant implementation before editing. New repository test files appear in **60/60 bundled attempts versus 5/60 custom attempts**. Custom often writes temporary API/CLI consumers instead. Some assert expected results; others only print values or booleans and would still exit successfully on a mismatch. Fewer committed tests is not equivalent to no validation, but printed output is also not equivalent to an asserted pass.

Recent evidence shows both useful validation and blind spots:

- **fd:** custom repeat 2 runs a real CLI comparison across thread counts and reordered, overlapping roots. The output differs, exposing nondeterministic random ordering. It adds a depth tie-break before assigning random ranks and the comparisons then pass. This is a concrete application check that changes production code.
- **Koota:** each prompt scores 1/2. The passing implementations choose world-local entity IDs; the failing ones preserve packed IDs and reject restoration into another world. Bundled repeat 2 explicitly tests cross-world restore. Bundled repeat 1 instead writes a test requiring it to fail, matching its own interpretation. Both custom consumers only restore into the same world. This design choice varies within each condition.
- **Koota also catches a real issue:** bundled repeat 1’s new test crashes when a tracking query is used after rollback. It traces the reset path, restores tracking masks and passes subsequent source and built-package checks. Its same run still fails the official cross-world case. Useful bug detection and a self-confirming expectation can coexist.
- **Igel:** both bundled trials reject explicit `exclude=None` before reaching the official all-features-removed error path. Their own tests also endorse rejecting `None`; the task specifies string/list without defining explicit null. This is a contract interpretation problem that more checks with the same assumption do not resolve. Custom trials have a separate fixture-setup failure, so their raw zeros do not measure 24 failed feature assertions.

Code differences extend beyond comments. Koota production additions are 502/440 lines in bundled and 397/406 in custom, but the extra code does different work: tracking restoration, empty-store handling, allocation limits, relation notifications and target ordering vary between attempts. Bundled adds 964/879 new source-test lines, duplicated into generated package tests; those copies must not be counted as distinct new coverage. No aggregate code-quality or complexity advantage is inferred from line counts.

## Partial Go-critic pair

Bundled’s new walker test actually triggers an empty-bracket panic and leads to a parser/length-check repair. Custom’s real CLI exercise checks diagnostic formats, aliases, dot imports, promoted members and declaration positions, but omits empty brackets. Its corresponding code still indexes the parser’s text array without the bundled guard. This is an unexecuted source-derived risk, not a new controller reproduction or score adjustment.

The official bundled zero has a different immediate cause. Its own warning annotations also serve as doc-comment inputs. The official overlay strips those annotations and replaces two main fixtures, while retaining two extra model fixtures. Eleven expected diagnostics then have no corresponding input text and fail as unmatched. A **grading-only diagnostic is deferred**; production and all original scores will be retained. Custom adds no repository tests even though the project’s contribution instructions prescribe checker fixtures. Its official pass does not establish compliance with that project instruction.

Both agents encounter the same pre-existing ruleguard dependency lookup failures. Bundled resolves the module-cache environment and gets a full race-enabled pass; custom reproduces the same failures on unchanged main and accurately discloses them. These are not provider interruptions and do not authorize model reruns.

## Recovery, caveats and remaining work

The October 28 user amendment requires replacements for terminal network/provider interruptions, using the first uninterrupted result regardless of score. Both required replacements are complete. The two interrupted originals remain archived and excluded from primary completion and efficiency: 475.6 seconds of combined agent-stage elapsed time; the capacity-interrupted attempt records 179,269 input, 138,624 cached input and 10,255 output tokens. The 401 attempt reports no token usage, which is unknown rather than measured zero. Two separate pre-agent image-setup failures used no model runs. This post-start policy and changed execution order will remain a final-report limitation.

There are now **10 deferred grading-only diagnoses**, including Go-critic. None ran during the timed model queue, and no secondary pass has been assumed. Frozen prompts, Astra xhigh, memory-off and conveying-only isolation remain unchanged. Koota’s benchmark language label is Python although the inspected repository is TypeScript; the sampling label is preserved and the discrepancy disclosed.

The remaining 118 slots, final task-paired analysis, bounded grading diagnostics and full report are still pending. The monitor, copied credential and dedicated VM remain necessary while the queue runs. Cleanup and monitor deletion occur after final delivery, not at this midpoint.

## Evidence

- [Frozen checkpoint data](checkpoint-120-data.json) and [122-slot snapshot](checkpoint-120-results.json)
- [Current health](../infrastructure/monitor-20261028T1139.json)
- [Koota four-trial comparison](../review/koota-all4-comparison.json), [fd comparison](../review/fd-all4-comparison.json), [Igel comparison](../review/igel-all4-comparison.json)
- [Go-critic grading interaction](../infrastructure/go-critic-bundled-r1-grader-fixture-coupling.json)
- Per-trial visible evidence is retained under `behavior/` and `review/`; raw records and frozen settings are unchanged. Reviews are non-blind and do not inspect hidden reasoning.
