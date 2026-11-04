# Checkpoint 180: 182 of 240 primary trials complete

Snapshot: October 29, 18:02 Shanghai (10:02 UTC). **45 tasks have both repeats completed under both prompts.** Kombu has only its first-repeat pair complete. Four completed Eicrud model attempts await grader-only recovery and are excluded from the primary figures below. This is the fresh 60 October 26 coding-prompt study; previous studies remain separate.

**The custom prompt has a higher observed official pass rate, with lower average time and token use.** These are descriptive interim results; the final report will estimate uncertainty using tasks as the paired unit.

## Official scores

| Population | Bundled | Coding override |
| --- | ---: | ---: |
| All 182 settled primary slots | 61/91 (67.0%) | 69/91 (75.8%) |
| Same 45 fully matched tasks | 60/90 (66.7%) | 68/90 (75.6%) |
| Kombu first repeat, not yet a complete task | 1/1 | 1/1 |

The matched difference is **8 passes, or 8.9 percentage points**. Custom has more passes on 9 tasks, bundled on 3, and 33 tie. Both repeats and every valid scored failure remain included. All 182 primary attempts completed normally and passed the frozen identity/isolation checks. The four pending native Eicrud grades are preserved separately, not silently converted into primary zeros or passes.

## Efficiency on the same 45 tasks

Equal task weight, two repeats per condition. Agent time excludes setup, grading and controller downtime. Partial tasks, pending grader recoveries and archived external interruptions are excluded.

| Mean per attempt | Bundled | Coding override | Change |
| --- | ---: | ---: | ---: |
| Agent time | 20.5 min | 17.1 min | −16.6% |
| Output tokens | 35,141 | 26,449 | −24.7% |
| Outer tool calls, including polls | 31.9 | 25.3 | −20.6% |
| Uncached input tokens | 93,048 | 88,457 | −4.9% |

Custom is faster on 39/45 task means and uses fewer output tokens on 42/45. Median task-relative time change is−20.1%. Uncached input is less consistent, lower on 26/45 tasks with median change−1.3%. These compare the complete prompts, not individual clauses.

## What the visible evidence adds

All 180 matched attempts inspect relevant implementation before editing. The recurring difference is how much validation code is saved, with smaller differences in the core implementation on some tasks.

- **SQL formatter: all four pass.** Core additions are 84/88 lines for bundled versus 79/78 for custom; test additions 504/461 versus 0/0. All use structured AST/grammar and native indentation machinery. Bundled repeat 1's real formatting call exposes tabular indentation leaking into later pipe steps; custom repeat 2's generated application client exposes a comment splitting the pipe operator from its keyword. Both repair and recheck the affected behavior. Bundled repeat 2 also runs new tests before implementation, reproducing missing functionality. This is useful validation in both styles, not testing versus no testing.
- **SQLite: all four pass.** Every attempt finds and repairs a SQL-tracing regression. A custom client exposes broken stdin handling and automatic-rollback cleanup; a bundled CLI test exposes single-column CSV inference. Both custom repeat 1 and bundled repeat 2 reproduce whole-transaction rollback losing earlier pending writes, then add a guard. Bundled saves 728/733 test lines; custom saves none. Custom is slower on this particular task:22.7 versus 18.3 minutes on average, despite fewer output tokens.
- **Obsidian: all four fail the same exact-output assertion.** All turn `[[My Page]]` into `[My Page](<My Page>)`; the official expectation is `[My Page](My Page)`. Both bundled test files explicitly encode the same angle-wrapped choice, so their extra tests cannot catch that disagreement. Yet bundled repeat 2's tests do catch real trailing-escape and multiline-link bugs and drive repairs. Custom examples and printed application checks cover protected regions, but share the whitespace-output choice. All four zeros remain unchanged.
- **Kombu, first pair only: both pass.** Both fix shared delivery tags that could route rejection from one queue to another queue's dead-letter destination. Bundled first demonstrates a failing real memory-transport test; custom identifies the issue from source, fixes it, then prints the correct two-destination result. Its earlier multi-queue TTL client used `no_ack`, so it could not expose the QoS collision. This distinction matters when attributing a repair to a test. Second repeats are still unfinished.

The current evidence therefore supports reduced validation overhead in many custom runs while also showing real defects caught by both validation styles. It does not support treating all additional tests as waste, or all application checks as independent of the implementation's assumptions.

## Grading, infrastructure and remaining work

Worker 57379 remains active with the shared exclusive lock; Kombu bundled repeat 2 is running in the dedicated main/proxy containers. Host free space is 61 GiB. Blender, the original stop barrier and unrelated wuitu-ota remain intact. This monitoring turn launched no model, grader, preflight or replacement, and used no reset card. **Monitoring remains every two hours**, as requested.

Four Eicrud official grader database-process crashes require recovery on the unchanged model patches after the timed queue finishes and the lock is free. Twelve separate test-overlay/fixture diagnostics remain deferred; their original scores stay unchanged and no alternative passes are assumed. These are specific execution records, not a blanket reason to discount benchmark results. Two externally interrupted originals remain archived; both replacements completed earlier. Extra recorded interruption time is 475.6 seconds, with 10,255 output tokens from the capacity-interrupted attempt; the 401 attempt's token usage is unreported. Three pre-model setup failures are also archived.

**58 primary slots remain:54 model trials, including the active one, plus 4 grader recoveries.** Next detailed milestone 210. Final task-paired statistics, report/inline visualization, copied-auth removal, shutdown of only codex-deepswe, and deletion of this monitor remain due after completion. Whole-prompt design, non-blind reviews, two stochastic repeats, selected task population and post-start interruption policy remain study limitations.

## Evidence

- [Frozen checkpoint data](checkpoint-180-data.json), [complete slot snapshot](checkpoint-180-results.json)
- [Worker health](../infrastructure/monitor-20261029T1002.json)
- [SQL formatter](../review/sql-formatter-all4-comparison.json), [SQLite](../review/sqlite-utils-all4-comparison.json), [Obsidian](../review/obsidian-all4-comparison.json), [Kombu first pair](../review/kombu-firstpair-comparison.json)
- Per-trial visible source/call/output evidence remains under `behavior/` and `review/`. No hidden reasoning was reviewed and no benchmark product was rerun for the report.
