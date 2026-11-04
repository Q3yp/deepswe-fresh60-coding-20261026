# Fresh 60 DeepSWE 1.1: frozen October 26 coding prompt versus bundled Codex

Completed October 31, 2026 (Shanghai). **240 primary slots, 60 tasks, 2 repeats per condition.** GPT-6 Astra, xhigh; no imported scores. Previous studies are separate.

**The coding override scored 78.3% versus 70.0% for bundled, while using 16.7% less agent time and 25.0% fewer output tokens.** The official-score gain is statistically detectable at the nominal 5% level in this full paired sample (exact p = 0.040). Resource and source-line reductions are more consistent across tasks. The score gain is sensitive to the documented test-overlay cases; the post-hoc analysis below makes that dependence explicit.

## Official result and uncertainty

| Measure | Bundled | Coding override |
| --- | ---: | ---: |
| Official passes | 84/120 | 94/120 |
| Official pass rate | 70.0% | 78.3% |
| Tasks with more passes | 3 | 11 |

There are 46 task-level ties. The difference is **+10 passes, +8.3 percentage points**, with a paired-task bootstrap 95% interval of **+1.7 to +15.8 points** and exact paired **p = 0.03967**.

Each task contributes the mean of its two attempts under each prompt. The score comparison uses an exact two-sided paired sign-flip test; intervals resample whole task pairs 100,000 times. The 120 attempts per prompt are not treated as 120 independent tasks. Neither repeat is selected or discarded based on reward. Secondary metrics and subgroup intervals are exploratory, without multiplicity adjustment; these are not equivalence or noninferiority tests.

| Repository stratum | Tasks | Bundled | Coding | Difference |
| --- | ---: | ---: | ---: | ---: |
| Repositories not in the prior study | 52 | 75/104 (72.1%) | 84/104 (80.8%) | +8.7 pp |
| Previously seen repositories, new tasks | 8 | 9/16 (56.3%) | 10/16 (62.5%) | +6.3 pp |

The 52-new-repository interval is +1.0 to +16.3 pp (exact p = 0.063); the eight-repository stratum is too small for a precise estimate. Every task itself was new. These strata are descriptive secondary analyses.

The sample was chosen before outcomes from 83 tasks not used in the previous 30-task study, using seed 20261026, one task per repository and benchmark-metadata language quotas. It covers 60/113 tasks (53.1%) of the full benchmark, not a full-benchmark leaderboard run. Metadata language labels are retained for sampling, even where the implementation language differs.

## Efficiency and code changes

| Per-trial mean | Bundled | Coding override | Change (paired-task 95% interval) |
| --- | ---: | ---: | ---: |
| Agent time | 20.3 min | 16.9 min | -16.7% (-21.8 to -11.1%) |
| Output tokens | 35,064 | 26,303 | -25.0% (-29.2 to -20.5%) |
| Outer tool calls, including polls | 32.5 | 25.8 | -20.8% (-25.5 to -15.7%) |
| Uncached input tokens | 95,229 | 88,302 | -7.3% (-12.1 to -2.3%) |

Agent time includes the model's tool and validation work, but excludes setup, official grading and controller downtime. Output tokens include the reported reasoning-output component. Uncached input is reported input minus cached input; these figures are usage measures, not a price estimate.

| Per-trial mean | Bundled | Coding override | Change (paired-task 95% interval) |
| --- | ---: | ---: | ---: |
| All added lines | 1,254.5 | 557.1 | -55.6% (-61.0 to -49.8%) |
| Test/fixture additions | 696.2 | 61.6 | -91.1% (-98.1 to -82.4%) |
| Source-file additions | 491.5 | 436.0 | -11.3% (-14.7 to -7.5%) |
| Source nonblank, non-comment proxy | 404.9 | 368.1 | -9.1% (-12.4 to -5.5%) |
| Source comment-only additions | 48.6 | 34.6 | -28.8% (-43.5 to -16.9%) |

**The smaller patch is mostly fewer saved tests, but it is not just comments.** Test/fixture additions account for 91.0% of the total added-line gap. After separating tests, docs and examples, source-file additions remain 11.3% lower. After also excluding blank and comment-only-looking lines, the source proxy remains **9.1% lower (95% interval: 5.5% to 12.4% lower)**. The interval excludes zero. Coding has fewer source additions on 55/60 task means and fewer proxy code additions on 52/60. Test/fixture additions appear in 119/120 bundled submissions and 23/120 coding submissions; the empty OOM submission is retained.

Coding is faster on 53/60 task means, uses fewer output tokens on 56/60, and fewer outer tool calls on 54/60.

Code counts come from submitted patches, not temporary validation scripts or uncommitted files. Test/fixture paths, documentation and examples are separated; reviewed embedded Rust tests are split out. The non-comment proxy removes blank and comment-looking added lines with hunk-local lexical rules. It is approximate: inline comments remain on code lines and string/docstring classification can be ambiguous. Fewer lines do not automatically mean simpler implementation or better maintainability.

## What changed in visible work

All 240 retained model records have visible-call, output and patch reviews. Both conditions inspected relevant implementation before editing. The reviews are non-blind and concern visible behavior, not hidden reasoning.

- **The override often replaces saved test files with temporary consumers, rather than eliminating execution.** Query and Valibot custom attempts run asserted public runtime/type consumers; go-git, ABS and Happy DOM examples often print results for inspection. These are materially different validation methods, so neither test-line count nor a statement that checks passed establishes coverage by itself.
- **Comparable feature cores can have very different total patch sizes.** Query passes all four attempts. Bundled adds 1,189/1,250 test lines versus 5/10 existing-test lines for coding; source-file additions are 138/128 versus 126/141 (the first bundled count includes 18 lines of test support). All four reuse native query fetch/cache paths. Valibot likewise passes all four, with source additions 349/333 versus 326/317 and saved test additions 1,581/1,341 versus 0/0. These are whole-prompt outcomes, not an ablation of the test-writing rule.
- **Both validation styles find real defects.** Valibot temporary TypeScript consumers expose recursive-union compiler failures and drive fixes. Go-git C1's public client exposes a root-directory-removal failure; C2 and bundled fixtures expose the same native Remove boundary during fixture setup. Bundled go-git B2's existing linked-worktree test finds a new `.git/MERGE_HEAD` regression, which is repaired. All four go-git official grades pass. Coding adds 578/544 source lines and no saved tests, versus 658/699 source and 613/661 test lines for bundled.
- **More checks do not guarantee independent expectations.** All four Happy DOM attempts fail the same 4 feature cases (10/14 F2P, 9/9 P2P). They assume connected targets and notifications for rectangle changes; official fixtures exercise detached supplied geometry and silent changes. Bundled saves 758/630 test lines, coding none, but both sets of selected scenarios miss the same requirement boundary. Those are ordinary retained failures.
- **Factoring changes are real but not uniform.** The go-git coding variants keep more orchestration in Merge; bundled uses more planning/application helpers. Wasmi coding repeat 2 stores encoded section ranges and rewrites them on reentry, whereas other variants keep typed snapshots. A smaller representation can trade explicit types for bookkeeping, so line-count reductions are not a universal complexity result.

Inspect [go-git](../review/go-git-all4-comparison.json), [Query](../review/query-all4-comparison.json), [Valibot](../review/valibot-all4-comparison.json), [Happy DOM](../review/happy-dom-all4-comparison.json) and the individual records under `behavior/` for source references and check limitations.

## Grading, interruptions and retained failures

**Six same-patch official grader recoveries** were performed, without rerunning their models. Two repaired registry/network failures before the grader ran (Go GenAI and ABS). Four Eicrud originals suffered a MongoDB process crash; one recorded error 24, “Too many open files.” The pinned image's measured soft limit was 1,024, with hard limit 524,288. Recovery raised only the verifier soft limit to 65,536, kept CPU/RAM, production patches and official tests unchanged, and captured MongoDB logs and process/resource evidence. Original native records and grades remain archived and untouched.

All four recovered Eicrud runs pass **14/14 feature checks**. Bundled B1/B2 and coding C1 pass 167/168 regression checks; coding C2 passes 166/168. The remaining failures return HTTP 425 where login/2FA assertions expect 201 or 401. **All four official binary zeros are retained, with no further retry.** Grading recovery restores executed evidence; it does not guarantee a passing score.

**Twelve additional test-overlay observations retain their original zeros:** 10 bundled and 2 coding. These include overwritten model test helpers still referenced by retained files, duplicate Go test/helper declarations, and fixture assumptions about an implementation-global name. For example, Updo's model and official patches both declare `TestHandleWebhookDecisionWithHeaders` in the same package; the notifications package fails to build. Igel's official fixture tries to patch a global removed when the implementation replaces the temporary CSV round-trip with a DataFrame path. The evidence and per-case limits are in the [final disposition](../infrastructure/fixture-diagnostics-final-disposition.json).

**Post-hoc task-level sensitivity:** removing all eight affected tasks from both conditions, including both repeats, leaves 81/104 bundled versus 84/104 coding (+2.9 pp; 95% interval −2.9 to +8.7; exact p = 0.508). Agent time is still 15.2% lower and output tokens 23.5% lower. This is a different, outcome-informed 52-task population, not a corrected score or the 52-new-repository stratum. Seven of the ten net additional official passes arise on those eight tasks; their hypothetical repaired grades remain unknown.

Removing the entire Optique task separately leaves 83/118 versus 92/118 (+7.6 pp; exact p = 0.063), with 17.4% lower time. This second sensitivity is also post hoc.

No test renaming, deletion or official-fixture edits were used to invent corrected passes. Their counterfactual grades remain unmeasured. This is a concrete sensitivity of these submitted patches to this evaluator, not evidence that every benchmark or every failure is invalid. It matters when interpreting the score difference, while the published official score above remains unchanged. Testem B2's removed required test ID and Happy DOM's semantic failures also remain zeros and were not rerun.

Two network/provider-interrupted model attempts were archived and replaced under the October 28 amendment: coding Termenv (provider capacity) and bundled ytt (routing 401). Termenv consumed 424.164 seconds, 179,269 input tokens (138,624 cached), 10,255 output tokens and 6 outer calls; ytt consumed 51.408 seconds, with token usage unreported and 0 outer calls. Their 475.571 seconds of extra agent execution and known usage are separate from primary efficiency; unreported tokens are not counted as measured zero. The first uninterrupted replacement was retained regardless of score. Nine pre-inference setup/isolation failures were also archived. No additional model preflight or reset card was used for this final recovery.

Optique bundled repeat 2 exceeded the enforced 8 GiB model-container memory limit. Its exit 137 and kernel/container evidence preceded the later host power loss. The model had uncommitted work but submitted an empty patch; its official zero is retained, not replaced. The power outage did not interrupt a different active model. The approved orphaned Optique setup build was terminated only after setup had already failed before inference; its records were archived before resuming.

Only conveying was enabled and memory use/generation disabled in trial configuration. One Valibot bundled attempt nevertheless explicitly read two disabled repository skill files through shell. Its score remains included; enabled-skill isolation is not proof of exclusive instruction-content exposure. See [exposure record](../review/valibot-manual-repository-skills.json).

## Scope and reproducibility

This compares two complete prompts under Codex 0.163.0/Pier 0.3.1, with a 3-hour agent timeout, 30-minute verifier timeout, 2 CPUs and 8 GiB memory, linux/amd64 through M4 Rosetta. Storage quota was not enforced. The 60 tasks and 30 ABBA/30 BAAB sequences were frozen before outcomes. No proposed requirement-first rule was added. There is no model seed, and provider drift or time effects can remain despite counterbalancing. The October 28 replacement policy was a disclosed post-start amendment. Prior 30-task results informed prompt development and test a different prompt version; none are pooled here.

Reproduce the calculations with `python3 report/analyze-final.py` against the retained primary records (requires NumPy). [Frozen plan](../experiment-plan.json), [bundled prompt](../prompts/bundled.md), [coding prompt](../prompts/override-coding.md), [analysis and intervals](final-analysis.json), [all 240 slots](checkpoint-240-results.json), [file-level line counts](final-code-file-metrics.json) and [final evidence check](final-validation.json) are preserved. Raw transcripts remain private.

**Cleanup verified at 02:25 Shanghai:** copied auth removed (no `auth.json` remains in this queue), no worker or dedicated containers, shared lock available, only `codex-deepswe` stopped with disks retained. `wuitu-ota` remains running; Blender and the original operator-stop barrier remain present. [Cleanup receipt](../infrastructure/final-cleanup-20261030.json). The exact two-hour monitor was deleted after this report and the inline visual were delivered. [Deletion receipt](../infrastructure/monitor-deletion-20261030.json).

## All 60 paired task scores

Values are official passes out of 2 attempts per condition, with no best-of-two selection.

| Task | Bundled /2 | Coding /2 |
| --- | ---: | ---: |
| wazero-multi-module-snapshots | 0 | 0 |
| dasel-html-document-format | 2 | 2 |
| textual-richlog-follow-state | 2 | 2 |
| updo-policy-alerting | 1 | 2 |
| actionlint-action-pinning-lint | 1 | 2 |
| mobly-grouped-test-barriers | 2 | 2 |
| vitest-duration-sharding | 2 | 2 |
| prometheus-transactional-reload-status | 0 | 0 |
| aiomonitor-task-snapshots-diff | 2 | 2 |
| fastapi-deprecation-response-headers | 2 | 2 |
| dynamodb-toolbox-lazy-recursive-schemas | 2 | 2 |
| awilix-async-container-initialization | 1 | 2 |
| kgateway-consistent-hash-policy | 0 | 1 |
| kysely-window-grouping-helpers | 2 | 2 |
| scriggo-method-declarations | 2 | 2 |
| pwntools-tube-multiplexing | 2 | 2 |
| langchain-request-coalescing | 2 | 2 |
| ofetch-per-origin-circuit-breaker | 2 | 2 |
| claude-code-by-agents-recursive-delegation | 2 | 2 |
| wasmi-trap-coredumps | 2 | 2 |
| kcp-go-multiplexed-kcp-streams | 0 | 2 |
| helm-array-merge-strategies | 0 | 1 |
| opa-template-string-reconstruction | 2 | 1 |
| tengo-destructuring-bindings | 2 | 2 |
| termenv-preserve-ansi-resets | 0 | 0 |
| ytt-jsonpath-query-api | 2 | 2 |
| csstree-shorthand-expansion-compression | 2 | 2 |
| fd-deterministic-multi-key-sorting | 2 | 2 |
| igel-persist-feature-schema | 0 | 0 |
| koota-entity-snapshot-rollback | 1 | 1 |
| go-critic-doc-link-checker | 0 | 2 |
| anko-default-function-arguments | 2 | 2 |
| superjson-error-stack-serialization | 1 | 2 |
| arktype-json-schema-refs-dependencies | 2 | 1 |
| geo-shapeindex-serialization | 1 | 2 |
| tomlkit-toml-table-converters | 2 | 2 |
| python-statemachine-state-data-scoping | 0 | 0 |
| mnamer-daemon-watch-lifecycle | 2 | 2 |
| cliffy-config-file-parsing | 2 | 2 |
| eicrud-keyset-pagination-cursor | 0 | 0 |
| mashumaro-flattened-dataclass-fields | 2 | 1 |
| sqlfmt-create-table-ddl-formatting | 0 | 0 |
| meriyah-explicit-resource-declarations | 0 | 0 |
| sqlite-utils-safe-import-checkpoints | 2 | 2 |
| obsidian-linter-link-format-conversion | 0 | 0 |
| sql-formatter-bigquery-pipe-formatting | 2 | 2 |
| kombu-virtual-queue-dead-lettering | 2 | 2 |
| quill-shared-toolbar-focus | 2 | 2 |
| psd-tools-blend-range-api | 2 | 2 |
| go-genai-streamed-function-args | 2 | 2 |
| effect-sse-httpapi-streaming | 2 | 2 |
| valibot-recursive-schema-composition | 2 | 2 |
| bandit-interprocedural-taint-checks | 2 | 2 |
| abs-module-cache-flags | 2 | 2 |
| adaptix-name-mapping-aliases | 2 | 2 |
| optique-conditional-option-dependencies | 1 | 2 |
| query-persist-restored-query-state | 2 | 2 |
| testem-per-launcher-reports | 1 | 2 |
| happy-dom-deterministic-intersectionobserver | 0 | 0 |
| go-git-worktree-merge-conflicts | 2 | 2 |
