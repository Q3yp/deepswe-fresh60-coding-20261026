# Fresh60 DeepSWE1.1: frozen October 26 coding prompt versus bundled Codex

Completed October31,2026 (Shanghai). **240 primary slots,60 tasks,2 repeats per condition.** GPT-6 Astra, xhigh; no imported scores. Previous studies are separate.

__LEAD__

## Official result and uncertainty

__SCORE_TABLE__

Each task contributes the mean of its two attempts under each prompt. The score comparison uses an exact two-sided paired sign-flip test; intervals resample whole task pairs100,000 times. The120 attempts per prompt are not treated as120 independent tasks. Neither repeat is selected or discarded based on reward. Secondary metrics and subgroup intervals are exploratory, without multiplicity adjustment; these are not equivalence or noninferiority tests.

__SUBGROUPS__

The sample was chosen before outcomes from83 tasks not used in the previous30-task study, using seed20261026, one task per repository and benchmark-metadata language quotas. It covers60/113 tasks (53.1%) of the full benchmark, not a full-benchmark leaderboard run. Metadata language labels are retained for sampling, even where the implementation language differs.

## Efficiency and code changes

__EFFICIENCY_TABLE__

Agent time includes the model's tool and validation work, but excludes setup, official grading and controller downtime. Output tokens include the reported reasoning-output component. Uncached input is reported input minus cached input; these figures are usage measures, not a price estimate.

__CODE_TABLE__

__CODE_INTERPRETATION__

Code counts come from submitted patches, not temporary validation scripts or uncommitted files. Test/fixture paths, documentation and examples are separated; reviewed embedded Rust tests are split out. The non-comment proxy removes blank and comment-looking added lines with hunk-local lexical rules. It is approximate: inline comments remain on code lines and string/docstring classification can be ambiguous. Fewer lines do not automatically mean simpler implementation or better maintainability.

## What changed in visible work

All240 retained model records have visible-call, output and patch reviews. Both conditions inspected relevant implementation before editing. The reviews are non-blind and concern visible behavior, not hidden reasoning.

- **The override often replaces saved test files with temporary consumers, rather than eliminating execution.** Query and Valibot custom attempts run asserted public runtime/type consumers; go-git, ABS and Happy DOM examples often print results for inspection. These are materially different validation methods, so neither test-line count nor a statement that checks passed establishes coverage by itself.
- **Comparable feature cores can have very different total patch sizes.** Query passes all four attempts. Bundled adds1,189/1,250 test lines versus5/10 existing-test lines for coding; source-file additions are138/128 versus126/141 (the first bundled count includes18 lines of test support). All four reuse native query fetch/cache paths. Valibot likewise passes all four, with source additions349/333 versus326/317 and saved test additions1,581/1,341 versus0/0. These are whole-prompt outcomes, not an ablation of the test-writing rule.
- **Both validation styles find real defects.** Valibot temporary TypeScript consumers expose recursive-union compiler failures and drive fixes. Go-git C1's public client exposes a root-directory-removal failure; C2 and bundled fixtures expose the same native Remove boundary during fixture setup. Bundled go-git B2's existing linked-worktree test finds a new `.git/MERGE_HEAD` regression, which is repaired. All four go-git official grades pass. Coding adds578/544 source lines and no saved tests, versus658/699 source and613/661 test lines for bundled.
- **More checks do not guarantee independent expectations.** All four Happy DOM attempts fail the same4 feature cases (10/14F2P,9/9P2P). They assume connected targets and notifications for rectangle changes; official fixtures exercise detached supplied geometry and silent changes. Bundled saves758/630 test lines, coding none, but both sets of selected scenarios miss the same requirement boundary. Those are ordinary retained failures.
- **Factoring changes are real but not uniform.** The go-git coding variants keep more orchestration in Merge; bundled uses more planning/application helpers. Wasmi coding repeat2 stores encoded section ranges and rewrites them on reentry, whereas other variants keep typed snapshots. A smaller representation can trade explicit types for bookkeeping, so line-count reductions are not a universal complexity result.

Inspect [go-git](../review/go-git-all4-comparison.json), [Query](../review/query-all4-comparison.json), [Valibot](../review/valibot-all4-comparison.json), [Happy DOM](../review/happy-dom-all4-comparison.json) and the individual records under `behavior/` for source references and check limitations.

## Grading, interruptions and retained failures

**Six same-patch official grader recoveries** were performed, without rerunning their models. Two repaired registry/network failures before the grader ran (Go GenAI and ABS). Four Eicrud originals suffered a MongoDB process crash; one recorded error24, “Too many open files.” The pinned image's measured soft limit was1,024, with hard limit524,288. Recovery raised only the verifier soft limit to65,536, kept CPU/RAM, production patches and official tests unchanged, and captured MongoDB logs and process/resource evidence. Original native records and grades remain archived and untouched.

__EICRUD__

**Twelve additional test-overlay observations retain their original zeros:**10 bundled and2 coding. These include overwritten model test helpers still referenced by retained files, duplicate Go test/helper declarations, and fixture assumptions about an implementation-global name. For example, Updo's model and official patches both declare `TestHandleWebhookDecisionWithHeaders` in the same package; the notifications package fails to build. Igel's official fixture tries to patch a global removed when the implementation replaces the temporary CSV round-trip with a DataFrame path. The evidence and per-case limits are in the [final disposition](../infrastructure/fixture-diagnostics-final-disposition.json).

No test renaming, deletion or official-fixture edits were used to invent corrected passes. Their counterfactual grades remain unmeasured. This is a concrete sensitivity of these submitted patches to this evaluator, not evidence that every benchmark or every failure is invalid. It matters when interpreting the score difference, while the published official score above remains unchanged. Testem B2's removed required test ID and Happy DOM's semantic failures also remain zeros and were not rerun.

__INTERRUPTIONS__

Optique bundled repeat2 exceeded the enforced8GiB model-container memory limit. Its exit137 and kernel/container evidence preceded the later host power loss. The model had uncommitted work but submitted an empty patch; its official zero is retained, not replaced. The power outage did not interrupt a different active model. The approved orphaned Optique setup build was terminated only after setup had already failed before inference; its records were archived before resuming.

Only conveying was enabled and memory use/generation disabled in trial configuration. One Valibot bundled attempt nevertheless explicitly read two disabled repository skill files through shell. Its score remains included; enabled-skill isolation is not proof of exclusive instruction-content exposure. See [exposure record](../review/valibot-manual-repository-skills.json).

## Scope and reproducibility

This compares two complete prompts under Codex0.163.0/Pier0.3.1, with a3-hour agent timeout,30-minute verifier timeout,2CPUs and8GiB memory, linux/amd64 through M4 Rosetta. Storage quota was not enforced. The60 tasks and30ABBA/30BAAB sequences were frozen before outcomes. No proposed requirement-first rule was added. There is no model seed, and provider drift or time effects can remain despite counterbalancing. The October28 replacement policy was a disclosed post-start amendment. Prior30-task results informed prompt development and test a different prompt version; none are pooled here.

Reproduce the calculations with `python3 report/analyze-final.py` against the retained primary records (requires NumPy). [Frozen plan](../experiment-plan.json), [bundled prompt](../prompts/bundled.md), [coding prompt](../prompts/override-coding.md), [analysis and intervals](final-analysis.json), [all240 slots](checkpoint-240-results.json), [file-level line counts](final-code-file-metrics.json) and [final evidence check](final-validation.json) are preserved. Raw transcripts remain private.

__CLEANUP__

## All60 paired task scores

Values are official passes out of2 attempts per condition, with no best-of-two selection.

__TASK_TABLE__
