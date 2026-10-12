# Doc Lint

Deterministic check of `{{STEERING}}` and `{{SPECS}}`; no agent judgment. Needs `python3` 3.9 or newer (standard library only).

## Run
- `python3 {{SKILLS}}/kiro-steering/scripts/doc_lint.py [project-root] [--also PATH]... [--strict] [--asof YYYY-MM-DD] [--max-age-days N]`
- Output `path:line: error|warning [rule] message`, then `N errors, M warnings`. Exit 0 clean (or warnings only), 1 errors (or warnings with `--strict`), 2 no `.kiro` directory.
- `--asof` is the reference date for staleness (default today); `--max-age-days` the age limit (default 180).
- `--also` adds files or directories to the human-typeable check (e.g. the project `AGENTS.md`).
- Human-Typeable exceptions: a code fence opened with ```` ```quote ```` (verbatim external syntax) or ```` ```output ```` (captured tool output) is skipped; any other fence is checked. A single line carries `lint-ignore: human-typeable`.

## Rules
| rule | level | meaning |
|---|---|---|
| human-typeable | error | `.md` or `.json` has a character that is not visible ASCII or a letter (symbols, emoji, circled numbers, middle dot, arrows, curly quotes, non-breaking space) |
| tree-root, tree-level, id-format, id-unique | error | value-chain tree shape: one Value root, 2-space levels, id `<parent id>-<segment>`, ids and aliases unique |
| required-tag, mega-kind, biz-process-ref-format | error | tags per level (Value: evidence; Mega: kind, pcf, evidence; Main: pcf, evidence; Unit: role, kpi, pcf, evidence, bizProcessRef); `kind` primary or support |
| kpi-number | error | `kpi:` holds `none` or KPI ids; no percent target in a node |
| requirement-not-in-design | error | a requirement ID `N.M` in requirements.md (criterion line or decision table row) appears nowhere in design.md of the same spec; ranges `2.1~2.5` count |
| value-chain-prose | warning | value-chain.md holds lines other than the tree, headings and comments |
| kpi-undefined, value-chain-ref, biz-process-ref, br-ref, br-prefix, bp-unique, br-unique | error | a reference with no definition: KPI id absent from the product.md KPI table; `valueChainRef` not a Unit id or alias; `bizProcessRef` or `_BizProcess:` BP id without an L1 Process heading; `BR-` id undefined or without its `BP-<x>`; duplicate definitions |
| stale-file, stale-node | warning | steering front matter `updated_at` or a value-chain node tag `asof` is older than `--max-age-days` before `--asof` |
| date-format | error | `updated_at` or `asof` is not `YYYY-MM-DD` (`updated_at` may continue with a time, e.g. `2026-10-01T09:00`); a `<...>` placeholder `updated_at` is skipped |
| kpi-unused, bp-unused, br-unused, back-link | warning | a definition nothing uses; a Unit naming a BP that no spec points back to |

## When to run
- `kiro-steering` Bootstrap after drafting value-chain.md, and Sync before reporting: fix errors in files the skill may edit, list the rest as proposals.
- `kiro-verify-completion` before DONE_EVIDENCE: errors block, warnings go into the report.
- Optional automation, project-owned: a pre-commit hook or CI step running the command with `--strict`, restricted to the same paths.
