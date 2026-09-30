# Bugfix Analysis Rules

## When
- A delivered behavior is wrong and reproducible. In-flight blockers → `kiro-debug`; new behavior → feature spec.
- Especially when a previous fix introduced new problems, or the path is critical and regression risk is high.

## Format
- Criteria follow `../../kiro-spec-requirements/rules/acceptance-criteria-format.md` (`N.M: [조건] 결과`).
- Group numbers are fixed: `1` Current Behavior (Defect), `2` Expected Behavior (Correct), `3` Unchanged Behavior (Regression Prevention).
- `1.x` states observed facts only, provable by the reproduction steps — no suspected cause.
- `2.x` pairs 1:1 with `1.x` (same `M`).
- `3.x` lists behavior around the touched path that must keep working — at least one.
- Reproduction Steps: environment, input, observed result. Numbered steps.

## Self-check
- Every `1.M` has a `2.M`; `3.x` ≥ 1; no implementation terms; ~200 lines cap.
