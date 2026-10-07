# Doc Lint

Deterministic check of `{{STEERING}}` and `{{SPECS}}`; no agent judgment. Needs `python3` (standard library only).

## Run
- `python3 {{SKILLS}}/kiro-steering/scripts/doc_lint.py [project-root] [--also PATH]... [--strict]`
- Output `path:line: error|warning [rule] message`, then `N errors, M warnings`. Exit 0 clean (or warnings only), 1 errors (or warnings with `--strict`), 2 no `.kiro` directory.
- `--also` adds files or directories to the human-typeable check (e.g. the project `AGENTS.md`).
- Human-Typeable exceptions: a code fence opened with ```` ```quote ```` (verbatim external syntax) or ```` ```output ```` (captured tool output) is skipped; any other fence is checked. A single line carries `lint-ignore: human-typeable`.

## Rules
| rule | level | meaning |
|---|---|---|
| human-typeable | error | `.md` or `.json` has a character that is not visible ASCII or a letter (symbols, emoji, circled numbers, middle dot, arrows, curly quotes, non-breaking space) |
| tree-root, tree-level, id-format, id-unique | error | value-chain tree shape: one Value root, 2-space levels, id `<parent id>-<segment>`, ids and aliases unique |
| required-tag, mega-kind, biz-process-ref-format | error | tags per level (Value: evidence; Mega: kind, pcf, evidence; Main: pcf, evidence; Unit: role, kpi, pcf, evidence, bizProcessRef); `kind` primary or support |
| kpi-number | error | `kpi:` holds `none` or KPI ids; no percent target in a node |
| value-chain-prose | warning | value-chain.md holds lines other than the tree, headings and comments |
| kpi-undefined, value-chain-ref, biz-process-ref, br-ref, br-prefix, bp-unique, br-unique | error | a reference with no definition: KPI id absent from the product.md KPI table; `valueChainRef` not a Unit id or alias; `bizProcessRef` or `_BizProcess:` BP id without an L1 Process heading; `BR-` id undefined or without its `BP-<x>`; duplicate definitions |
| kpi-unused, bp-unused, br-unused, back-link | warning | a definition nothing uses; a Unit naming a BP that no spec points back to |

## When to run
- `kiro-steering` Bootstrap after drafting value-chain.md, and Sync before reporting: fix errors in files the skill may edit, list the rest as proposals.
- `kiro-verify-completion` before DONE_EVIDENCE: errors block, warnings go into the report.
- Optional automation, project-owned: a pre-commit hook or CI step running the command with `--strict`, restricted to the same paths.
