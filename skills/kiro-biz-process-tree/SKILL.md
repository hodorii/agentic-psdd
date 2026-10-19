---
name: kiro-biz-process-tree
description: Lean contract for kiro-biz-process-tree: read-only top-to-bottom tree view of a spec's biz-process.md, ids kept as written.
---

# kiro-biz-process-tree

Inputs
- {{SPECS}}/{feature}/biz-process.md (read-only SSoT)
- spec.json (`language`, `approvals.bizProcess.generated`)

Outputs
- Core Indicators: BIZ_PROCESS_TREE_MD, TREE_ID_PARITY

Boundaries
- View only: never edit biz-process.md, value-chain.md or steering; never assign, renumber or invent ids, rules, gaps or wording.
- User viewpoint only, as in kiro-biz-process; no API, status code, table or internal processing order.
- Not a spec artifact: no Definition, no spec.json entry; lives under {{REFERENCE}}.

Rules
- Read `rules/tree-view-rules.md` from this skill's directory for symbols, node mapping, branch writing and the Human-Typeable exception
- Read `{{TEMPLATES}}/reference/biz-process-tree.md` for document structure
- Stop if biz-process.md is missing or `approvals.bizProcess.generated` is false; point to `$kiro-biz-process` (approval is not required: a generated, unapproved draft may be viewed)
- Write `{{REFERENCE}}/biz-process-tree/{feature}.md`; regenerate it whole whenever biz-process.md changes
- Run `python3 {{SKILLS}}/kiro-steering/scripts/doc_lint.py` and fix every `tree-*` and `human-typeable` finding before reporting
- Next: continue the workflow at `$kiro-spec-design {feature}` (the view is optional)
