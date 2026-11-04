# Fresh 60 DeepSWE 1.1: Codex System Prompt Override vs. Bundled

**240 primary slots, 60 tasks, 2 repeats per condition (ABBA/BAAB counterbalanced).** GPT-6 Astra (`xhigh`), 619.2M total tokens (7.36M output tokens) across 74.4 agent hours.

## Repository Contents

- [`prompts/override-coding.md`](prompts/override-coding.md): The coding system prompt override (`model_instructions_file`).
- [`prompts/bundled.md`](prompts/bundled.md): The default bundled Codex system prompt used as baseline.
- [`traces.zip`](traces.zip): Raw agent rollouts, `model.patch` submissions, verifier logs, and review records for all 240 sessions (also attached on [Releases](../../releases)).

## Summary of Results

| Measure | Bundled (`prompts/bundled.md`) | Coding Override (`prompts/override-coding.md`) | Difference / Change (95% Paired CI) |
| :--- | ---: | ---: | ---: |
| **Official passes (all 60 tasks)** | 84 / 120 (70.0%) | **94 / 120 (78.3%)** | **+10 passes, +8.3 pp** (+1.7 to +15.8 pp, $p = 0.0397$) |
| **Standard engineering tasks (52 tasks, excluding 8 parser/formatter tasks)** | 78 / 104 (75.0%) | **88 / 104 (84.6%)** | **+10 passes, +9.6 pp** (10 task wins vs. 1 loss) |
| **Diagnostic regraded passes (all 60 tasks, 12 overlay collisions repaired)** | 91 / 120 (75.8%) | **94 / 120 (78.3%)** | **+3 passes, +2.5 pp** (-2.5 to +7.5 pp, $p = 0.5078$) |
| **Agent time (per-trial mean)** | 20.3 min | **16.9 min** | **-16.7%** (-21.8% to -11.1%) |
| **Output tokens (per-trial mean)** | 35,064 | **26,303** | **-25.0%** (-29.2% to -20.5%) |
| **Total input tokens (per-trial mean)** | 2,905,443 | **2,193,440** | **-24.5%** (-32.1% to -15.9%) |
| **Uncached input tokens (per-trial mean)** | 95,229 | **88,302** | **-7.3%** (-12.1% to -2.3%) |
| **Outer tool calls (per-trial mean)** | 32.5 | **25.8** | **-20.8%** (-25.5% to -15.7%) |
| **All added lines (per-trial mean)** | 1,254.5 | **557.1** | **-55.6%** (-61.0% to -49.8%) |
| **Test / fixture additions (per-trial mean)** | 696.2 | **61.6** | **-91.1%** (-98.1% to -82.4%) |
| **Source-file additions (per-trial mean)** | 491.5 | **436.0** | **-11.3%** (-14.7% to -7.5%) |
| **Source non-blank, non-comment additions (per-trial mean)** | 404.9 | **368.1** | **-9.1%** (-12.4% to -5.5%) |
| **Source comment-only additions (per-trial mean)** | 48.6 | **34.6** | **-28.8%** (-43.5% to -16.9%) |

Across the 60 tasks, [`prompts/override-coding.md`](prompts/override-coding.md) uses fewer output tokens on 56/60 task means, finishes faster on 53/60, makes fewer outer tool calls on 54/60, adds fewer total source lines on 55/60, and adds fewer non-blank non-comment source lines on 52/60.

## Key Findings from the 240 Sessions

1. **Saved unit tests vs. backward source review and minimal entry-point checks:**
   - Under `bundled`, models added or expanded saved test files in 119/120 runs (averaging 696.2 lines per run). Only **58/120 (48.3%)** caught a real production defect (red-to-green repair). The remaining **62/120 (51.7%)** either passed on the first run without catching any defect (42 runs) or suffered from shared-assumption false greens and grader test-overlay collisions (20 runs).
   - Under `override-coding`, models trace behavior backward from the implementation to the requirements and validate unresolved questions through the normal entry point or minimal targeted checks. On tasks like `query` and `valibot`, all four runs pass 100% of official checks with zero saved test files (vs. 1,189–1,581 saved test lines in `bundled`) and ~10% fewer production source lines.

2. **Remaining semantic failures concentrate in single-character / lexer / formatter conventions:**
   - Outside the 8 lexer, parser, formatter, and AST/schema serialization tasks (`meriyah`, `sqlfmt`, `obsidian-linter`, `termenv`, `helm`, `opa`, `mashumaro`, `arktype`), `override-coding` passes **88/104 (84.6%)** versus **78/104 (75.0%)** for `bundled`.
   - On those text/parsing/formatting tasks, submissions pass 92%–100% of feature assertions and miss 1–3 repository-specific formatting or grammar edge cases:
     - `obsidian-linter-link-format-conversion`: 59/60 F2P, 1131/1131 P2P (emits CommonMark `[My Page](<My Page>)` for spaced targets instead of unbracketed `[My Page](My Page)`).
     - `meriyah-explicit-resource-declarations`: 48/49 F2P, 51469/51469 P2P (misses `for (using of of [1, 2])` where contextual keyword `of` is also the bound identifier).
     - `termenv-preserve-ansi-resets`: 34/35 F2P, 87/87 P2P (early `width <= 0` guard returns `""` instead of preserving zero-width OSC8 hyperlink control sequences).
     - `sqlfmt-create-table-ddl-formatting`: 30/32 F2P, 1271/1273 P2P (emits `CREATE TABLE foo(` instead of `CREATE TABLE foo (` with a space before `(`).
     - `helm-array-merge-strategies`: 47/47 F2P, 10/12 P2P (all merge strategy logic passes; 2 `helm lint` warning strings differ in wording).

## All 60 Paired Task Scores

Values are official passes out of 2 attempts per condition, with no best-of-two selection.

| Task | Bundled (/2) | Coding Override (/2) | Diagnostic Regraded Bundled (/2) | Diagnostic Regraded Override (/2) |
| :--- | ---: | ---: | ---: | ---: |
| `wazero-multi-module-snapshots` | 0 | 0 | 0 | 0 |
| `dasel-html-document-format` | 2 | 2 | 2 | 2 |
| `textual-richlog-follow-state` | 2 | 2 | 2 | 2 |
| `updo-policy-alerting` | 1 | 2 | 2 | 2 |
| `actionlint-action-pinning-lint` | 1 | 2 | 2 | 2 |
| `mobly-grouped-test-barriers` | 2 | 2 | 2 | 2 |
| `vitest-duration-sharding` | 2 | 2 | 2 | 2 |
| `prometheus-transactional-reload-status` | 0 | 0 | 0 | 0 |
| `aiomonitor-task-snapshots-diff` | 2 | 2 | 2 | 2 |
| `fastapi-deprecation-response-headers` | 2 | 2 | 2 | 2 |
| `dynamodb-toolbox-lazy-recursive-schemas` | 2 | 2 | 2 | 2 |
| `awilix-async-container-initialization` | 1 | 2 | 1 | 2 |
| `kgateway-consistent-hash-policy` | 0 | 1 | 0 | 1 |
| `kysely-window-grouping-helpers` | 2 | 2 | 2 | 2 |
| `scriggo-method-declarations` | 2 | 2 | 2 | 2 |
| `pwntools-tube-multiplexing` | 2 | 2 | 2 | 2 |
| `langchain-request-coalescing` | 2 | 2 | 2 | 2 |
| `ofetch-per-origin-circuit-breaker` | 2 | 2 | 2 | 2 |
| `claude-code-by-agents-recursive-delegation` | 2 | 2 | 2 | 2 |
| `wasmi-trap-coredumps` | 2 | 2 | 2 | 2 |
| `kcp-go-multiplexed-kcp-streams` | 0 | 2 | 2 | 2 |
| `helm-array-merge-strategies` | 0 | 1 | 0 | 1 |
| `opa-template-string-reconstruction` | 2 | 1 | 2 | 1 |
| `tengo-destructuring-bindings` | 2 | 2 | 2 | 2 |
| `termenv-preserve-ansi-resets` | 0 | 0 | 0 | 0 |
| `ytt-jsonpath-query-api` | 2 | 2 | 2 | 2 |
| `csstree-shorthand-expansion-compression` | 2 | 2 | 2 | 2 |
| `fd-deterministic-multi-key-sorting` | 2 | 2 | 2 | 2 |
| `igel-persist-feature-schema` | 0 | 0 | 0 | 0 |
| `koota-entity-snapshot-rollback` | 1 | 1 | 1 | 1 |
| `go-critic-doc-link-checker` | 0 | 2 | 2 | 2 |
| `anko-default-function-arguments` | 2 | 2 | 2 | 2 |
| `superjson-error-stack-serialization` | 1 | 2 | 1 | 2 |
| `arktype-json-schema-refs-dependencies` | 2 | 1 | 2 | 1 |
| `geo-shapeindex-serialization` | 1 | 2 | 2 | 2 |
| `tomlkit-toml-table-converters` | 2 | 2 | 2 | 2 |
| `python-statemachine-state-data-scoping` | 0 | 0 | 0 | 0 |
| `mnamer-daemon-watch-lifecycle` | 2 | 2 | 2 | 2 |
| `cliffy-config-file-parsing` | 2 | 2 | 2 | 2 |
| `eicrud-keyset-pagination-cursor` | 0 | 0 | 0 | 0 |
| `mashumaro-flattened-dataclass-fields` | 2 | 1 | 2 | 1 |
| `sqlfmt-create-table-ddl-formatting` | 0 | 0 | 0 | 0 |
| `meriyah-explicit-resource-declarations` | 0 | 0 | 0 | 0 |
| `sqlite-utils-safe-import-checkpoints` | 2 | 2 | 2 | 2 |
| `obsidian-linter-link-format-conversion` | 0 | 0 | 0 | 0 |
| `sql-formatter-bigquery-pipe-formatting` | 2 | 2 | 2 | 2 |
| `kombu-virtual-queue-dead-lettering` | 2 | 2 | 2 | 2 |
| `quill-shared-toolbar-focus` | 2 | 2 | 2 | 2 |
| `psd-tools-blend-range-api` | 2 | 2 | 2 | 2 |
| `go-genai-streamed-function-args` | 2 | 2 | 2 | 2 |
| `effect-sse-httpapi-streaming` | 2 | 2 | 2 | 2 |
| `valibot-recursive-schema-composition` | 2 | 2 | 2 | 2 |
| `bandit-interprocedural-taint-checks` | 2 | 2 | 2 | 2 |
| `abs-module-cache-flags` | 2 | 2 | 2 | 2 |
| `adaptix-name-mapping-aliases` | 2 | 2 | 2 | 2 |
| `optique-conditional-option-dependencies` | 1 | 2 | 1 | 2 |
| `query-persist-restored-query-state` | 2 | 2 | 2 | 2 |
| `testem-per-launcher-reports` | 1 | 2 | 1 | 2 |
| `happy-dom-deterministic-intersectionobserver` | 0 | 0 | 0 | 0 |
| `go-git-worktree-merge-conflicts` | 2 | 2 | 2 | 2 |
| **Total** | **84 / 120** | **94 / 120** | **91 / 120** | **94 / 120** |

## Usage

Give [`prompts/override-coding.md`](prompts/override-coding.md) to Codex and ask it to configure the file as its native system prompt override (`model_instructions_file` in `~/.codex/config.toml`).
