---
name: kiro-bugfix
description: Lean contract for kiro-bugfix: capture a reproducible defect as current / expected / unchanged behavior for a regression-safe fix.
---

# kiro-bugfix

Inputs
- Bug report: reproduction steps, current behavior, expected behavior, constraints
- Existing spec artifacts of the affected feature (if any)

Outputs
- Core Indicators: BUGFIX_MD, UNCHANGED_BEHAVIORS

Boundaries
- Analysis only: observed behavior, no root cause, no code. Root cause belongs to design.
- Not for in-flight blockers (`kiro-debug`) or new behavior (`kiro-spec-requirements`).

Rules
- Read `rules/bugfix-analysis.md` from this skill's directory
- Reproduce first; if the defect cannot be reproduced, stop and route to `$kiro-debug`
- Read `{{TEMPLATES}}/specs/bugfix.md` for document structure; write `{{SPECS}}/{fix}/bugfix.md`
- Write spec.json from `{{TEMPLATES}}/specs/init.json` with `approvals.bugfix` in place of `requirements`, and drop the `approvals.bizProcess` key entirely unless the fix changes a user flow (a left-in `bizProcess: {generated: false, approved: false}` reads downstream as a real gate stuck pending forever, not as "not applicable"); `phase: bugfix-generated`
- Next: `$kiro-spec-design {fix}` - reads bugfix.md; biz-process is skipped unless the fix changes a user flow
