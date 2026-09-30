---
name: kiro-validate-impl
description: Lean contract for kiro-validate-impl: validate feature-level implementation integration.
---

# kiro-validate-impl

Inputs
- TASKS_MD
- VERIFICATION_RESULTS
- DESIGN_MD
- REQUIREMENTS_MD

Outputs
- Core Indicators: VALIDATION_RESULT, ISSUES, VERIFICATION_EVIDENCE

Boundaries
- Validation only; no new feature work.

Rules
- Read tasks.md produced by kiro-spec-tasks
- Read verification results; read design.md and requirements.md
- Runnable artifacts (binary, TUI, service): run the real thing against real data in its default configuration first, then one narrow/alternate size, and capture its output (terminal capture with escape codes, HTTP response, log) - a green test suite alone is not VERIFICATION_EVIDENCE
- Non-runnable deliverables (document, data, analysis): map every requirement ID to its location in the deliverable; the map with unmet IDs is VERIFICATION_EVIDENCE
- Code: list functions/classes/files over steering `tech.md` size limits without stated reason as ISSUES
- requirements.md, design.md and tasks.md are the sole source of intent; re-assess every task regardless of its checkbox state - a `[x]` or an implementer's report is a claim, not evidence
- Classify each finding as `missing` (intent with no implementation), `partial`, `contradicts` (implementation defies a requirement, Boundary Commitment or dependency direction) or `unrequested` (content no artifact asked for); cite the artifact ID and the deliverable location
- NO-GO findings are appended to tasks.md as rework tasks in bugfix order (code: failing reproduction test -> fix -> pass; non-code: gap statement -> fix -> recheck), each traced to requirement IDs; never rewrite or renumber existing tasks; re-validate after they close. Zero findings -> GO with tasks.md unchanged
- Output VALIDATION_RESULT and VERIFICATION_EVIDENCE
