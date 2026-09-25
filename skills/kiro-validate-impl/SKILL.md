---
name: kiro-validate-impl
description: Lean contract for kiro-validate-impl: validate feature-level implementation integration.
---

# kiro-validate-impl

Inputs
- TASKS_MD
- TEST_RESULTS
- DESIGN_MD
- REQUIREMENTS_MD

Outputs
- Core Indicators: VALIDATION_RESULT, ISSUES, VERIFICATION_EVIDENCE

Boundaries
- Validation only; no new feature work.

Rules
- Read tasks.md produced by kiro-spec-tasks
- Read test results; read design.md and requirements.md
- Runnable artifacts (binary, TUI, service): run the real thing against real data in its default configuration first, then one narrow/alternate size, and capture its output (terminal capture with escape codes, HTTP response, log) — a green test suite alone is not VERIFICATION_EVIDENCE
- requirements.md, design.md and tasks.md are the sole source of intent; re-assess every task regardless of its checkbox state — a `[x]` or an implementer's report is a claim, not evidence
- Classify each finding as `missing` (intent with no implementation), `partial`, `contradicts` (implementation defies a requirement, Boundary Commitment or dependency direction) or `unrequested` (code no artifact asked for); cite the artifact ID and the code location
- NO-GO findings are appended to tasks.md as rework tasks in bugfix order (failing reproduction test → fix → pass), each traced to requirement IDs; never rewrite or renumber existing tasks; re-validate after they close. Zero findings → GO with tasks.md unchanged
- Output VALIDATION_RESULT and VERIFICATION_EVIDENCE
