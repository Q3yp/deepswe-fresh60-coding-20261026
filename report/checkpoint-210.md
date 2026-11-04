# Checkpoint 210: 212 of 240 primary trials complete

Snapshot: October 30, 12:05 Shanghai, including the same-patch grading recovery completed at 12:08. **53 tasks now have both repeats under both prompts. There are no partial task pairs in this score snapshot.** This is the fresh 60 October 26 coding-prompt study; previous studies remain separate.

**The coding override has a higher observed official pass rate and lower average resource use.** All valid failures and both repeats remain included. These are descriptive interim figures; the final report will calculate uncertainty with tasks as the paired unit.

## Official scores and matched efficiency

| Metric, same 53 tasks | Bundled | Coding override | Difference |
| --- | ---: | ---: | ---: |
| Official passes | 76/106 (71.7%) | 84/106 (79.2%) | +8 passes, +7.5 pp |
| Mean agent time | 20.5 min | 17.0 min | −17.0% |
| Mean output tokens | 35,212 | 26,275 | −25.4% |
| Mean outer tool calls, including polls | 32.3 | 25.4 | −21.3% |
| Mean uncached input tokens | 93,528 | 87,553 | −6.4% |

Coding has more passes on 9 tasks, bundled on 3, and 41 tie. Coding is faster on 47/53 task means and uses fewer output tokens on 50/53. Each task has equal weight; agent time excludes setup, grading and controller downtime. Archived external interruptions and pending grader recoveries are excluded from these primary figures. All 212 primary model attempts completed normally and passed frozen identity and enabled-skill configuration checks.

## Visible behavior and code

All 216 completed-model records have visible-evidence reviews, including the 4 Eicrud records awaiting grading recovery. All 212 primary attempts inspected relevant implementation before editing.

- **Bandit: both prompts 2/2.** All four use native AST analysis and the same five plugin entrypoints. Bundled saves 614/546 test lines; coding saves none but executes real CLI examples with 14 and 20 findings, checking printed IDs, locations, CWE and severity. Bundled repeat 1's assertions catch an imported-source alias miss, and a recursive-closure probe actually times out before a termination repair. Bundled repeat 2's observed failing test is fixture pollution, fixed in the fixture. Coding's annotation/alias corrections are source-led, then exercised. Core source additions excluding examples are 685/533 for bundled versus 590/485 for coding; repeated code differs in scoping, taint representation and memoization. Fewer lines alone do not establish lower complexity. Mean agent time is 19.1 versus 13.9 minutes.
- **ABS: both prompts 2/2.** Bundled saves 522/593 test lines; coding saves none but creates temporary ABS CLI scripts and public Go consumers. These visibly cover 24/30-level graphs, shared cached objects, quoted search paths, cycles, cache reset and captured runtime stderr. They print results for inspection rather than automatically asserting them. Bundled repeat 1's test exposes ENOTDIR incorrectly stopping module search; the implementation is repaired. Coding repeat 2 finds nested relative-path rebasing during source review, fixes it, then exercises a concrete nested graph. Source additions are 407/420 versus 351/358, including comments; all share the native cache/active-stack/evaluator architecture. Mean agent time is 19.0 versus 15.4 minutes.
- **Valibot, completed since the last milestone: both prompts 2/2.** Saved test additions are 1581/1341 versus 0/0, while production additions are 349/333 versus 326/317. Both coding attempts use asserted temporary runtime and TypeScript consumers; compiler failures on recursive unions drive real type fixes. Bundled repeat 1 also fixes a tuple-rest expansion failure, while weakening exact tuple equality to mutual assignability plus nested indexing. This illustrates why validation quality depends on the actual oracle, not just test-file count.

The implementation differences are often smaller than the total patch differences. This is a whole-prompt comparison; the evidence cannot assign gains to a particular instruction.

## Infrastructure and instruction exposure

ABS bundled repeat 2 finished its model turn, then ECR metadata lookup timed out before grading. The entire original job was archived. One official grader-only recovery used the identical patch and passed 20/20 feature plus 3/3 regression checks. No additional model execution occurred. The recovery took 81.0 seconds, separate from model efficiency. Both frozen prompts and trial settings remained unchanged.

Worker 91072 resumed after the free-lock/no-worker/no-container checks. At 12:13 Shanghai it held the shared lock with Adaptix bundled repeat 1 active, isolation passed and dedicated main/proxy containers healthy. Host free space 60.3 GiB; Blender, original stop barrier and unrelated wuitu-ota retained. One earlier resume guard used a nonexistent absolute Docker binary path and exited before dispatch; using the existing PATH resolved it. No duplicate worker, model preflight or reset card.

Only conveying was enabled in native skill configuration. **Valibot bundled repeat 2 nevertheless explicitly read two disabled repository SKILL.md files through shell.** The other three Valibot traces do not show those content reads. Retain its official pass and disclose the extra instruction exposure; enabled-skill isolation does not prove exclusive skill-content exposure.

Four Eicrud database-process grader crashes still require same-patch recovery after the timed queue releases the lock. Twelve separate test-overlay/fixture diagnostics remain deferred, with all original scores unchanged and no alternative passes assumed. Two externally interrupted model attempts and eight pre-inference/setup failures remain archived. Two model-complete registry grading interruptions, Go GenAI and ABS, are now recovered; neither caused a model rerun. The post-start interruption policy, two stochastic repeats, selected sample, non-blind review and possible endpoint drift remain study limitations.

## Remaining work

**28 primary slots remain:24 model trials, including the active one, and 4 grader recoveries.** Monitoring stays every two hours. The final 240-slot report will include task-paired statistics and the inline visualization, separate interruption usage and prior-study context. Copied-auth cleanup, shutdown of only codex-deepswe with disks retained, and deletion of this monitor remain due at completion.

## Evidence

- [Frozen checkpoint data](checkpoint-210-data.json) and [slot snapshot](checkpoint-210-results.json)
- [Bandit comparison](../review/bandit-all4-comparison.json), [ABS comparison](../review/abs-all4-comparison.json), [Valibot comparison](../review/valibot-all4-comparison.json)
- [Manual repository skill reads](../review/valibot-manual-repository-skills.json)
- [Recovery receipt](../jobs/abs-module-cache-flags--bundled--r2/abs-module-cache-flags__jM59Ykt/verifier-recovery.json), [confirmed worker health](../infrastructure/abs-resume-confirmed-health-20261030.json)
- [Evidence validation](../review/monitor-20261030T0402-validation.json)
