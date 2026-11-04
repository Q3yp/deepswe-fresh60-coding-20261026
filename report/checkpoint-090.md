# Checkpoint 90: 91 of 240 trials complete

Snapshot: October 28, 07:39 Shanghai (October 27, 23:39 UTC). There are 22 fully matched tasks, each with two attempts per condition, plus three OPA attempts. The existing worker holds the exclusive lock and is running OPA bundled repeat 2, slot 92. No worker was dispatched or trial rerun.

## Official results

| Population | Bundled | October 26 coding override |
| --- | ---: | ---: |
| All 91 scored attempts | 32/45 (71.1%) | 39/46 (84.8%) |
| Same 22 fully matched tasks | 31/44 (70.5%) | 38/44 (86.4%) |

All 91 model turns completed normally and passed identity, frozen-prompt and isolation attestation. Normal turn completion does not necessarily mean the requested work was delivered. Every official zero remains in the results.

The seven-pass matched difference is not seven clear functional improvements. Four points come from official test-overlay collisions in bundled Updo, Actionlint and both KCP attempts. One Helm point depends on warning spelling: the official assertion rejects `merge strategy`, while the passing custom run says `merge-strategy`; all four implementations warn for the missing path and pass all 47 feature checks. The other two points remain Kgateway’s underspecified exact-output mismatch and Awilix’s inherited-singleton startup behavior. Six tasks favor custom on raw pass counts; 16 tie. No task favors bundled in this fully matched subset yet.

OPA is separate: both first attempts pass all nine official checks. Custom repeat 2 returns normally but **does not make the explicitly requested commit**, citing absent Git identity and human DCO sign-off. Its two changed files remain staged. The official collector takes the committed diff against the base, so it submits an empty patch and the grader tests unchanged code: 0/5 feature checks, 4/4 regression checks. This is an incomplete-delivery result, not evidence that the staged implementation fails those checks. It is not an infrastructure recovery candidate. The remaining bundled repeat is still running.

## Efficiency on 22 fully matched tasks

Means retain both repeats and all outcomes, with equal task weight. OPA is excluded until all four slots finish. Agent time excludes setup, grading and controller downtime.

| Mean per attempt | Bundled | Coding override | Change |
| --- | ---: | ---: | ---: |
| Agent time | 22.1 min | 19.7 min | −10.9% |
| Output tokens | 38,643 | 30,492 | −21.1% |
| Outer tool calls, including polls | 36.1 | 30.0 | −16.9% |
| Uncached input tokens | 101,228 | 95,635 | −5.5% |

Custom has lower task-mean time on 17/22 tasks and lower output on 20/22. The median task-relative time change is −15.1%. This remains descriptive, without repeated interim significance tests. Wasmi is a counterexample: custom averages 29.8 minutes versus bundled 21.1 minutes, with all four attempts passing.

## Behavior and implementation

All 88 fully matched attempts inspect relevant implementation before editing. New repository test files appear in 44/44 bundled attempts and 5/44 custom attempts. Custom’s exceptions are one Vitest, both Kgateway and both Langchain attempts. Temporary drivers and fixtures remain common, so fewer committed tests does not mean no validation.

The new evidence shows both forms can expose actual mistakes:

- **Wasmi:** a custom driver triggers a real arena-relocation panic; bundled tests expose host-tail and callee-instance problems. More local discoveries and iteration can make custom slower.
- **Helm:** custom application runs expose lost reused subchart values and a mismatch between reset-rendered and stored/recomputed values. Bundled adds extensive tests, but its schema-helper checks do not exercise the full template-lint path. Test quantity alone does not establish coverage.
- **OPA:** bundled’s new tests and custom’s temporary drivers compare original-policy evaluation with reconstructed AST/source. They expose required-input semantics and nested reconstruction leaks. Custom repeat 2 locally repairs a real missing-input mismatch, yet fails delivery by leaving the change uncommitted.

Code choices differ beyond comments and tests. KCP custom drafts use 568/598-line multiplexers versus bundled’s 601/699 lines, but checks cover different shutdown and ordering scenarios. OPA’s first custom implementation uses a 280-line restorer and public-boundary wrappers; bundled uses a 384-line restorer at the shared partial boundary plus 431 test lines. Both reuse existing AST/copy-propagation machinery. These are observed design differences, not proof that fewer lines mean less complexity or better correctness. The uncommitted second custom draft must not be counted as a successful zero-line implementation.

## Caveats and remaining work

Seven grader-only build-collision diagnostics remain deferred until the timed queue finishes and releases its lock. Helm’s wording-sensitive oracle is a separate caveat, with no adjusted score. Required OPA lint is unavailable in the task environment; the agents disclose this. Both custom OPA attempts omit accompanying repository tests despite the project’s testing guidance, so test avoidance is not unqualified compliance.

There are 149 slots left in this snapshot, including the running trial. Prompts, model settings and isolation remain frozen; prior studies are separate. The sample and whole-prompt design do not support leaderboard-equivalence or individual-clause causal claims. Visible review is non-blind. The dedicated VM and copied auth remain in place for the active queue and will receive the authorized scoped cleanup when it completes. The monitor will be removed after final delivery.

Evidence: [snapshot calculations](checkpoint-090-data.json), [raw scored rows](checkpoint-090-results.json), [OPA submission finding](../review/opa-coding-r2-submission.json), [Helm oracle finding](../infrastructure/helm-all4-lint-oracle-wording.json), and per-trial records in `behavior/`.
