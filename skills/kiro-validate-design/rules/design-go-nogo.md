# Design Review

> Core question: is the design safe to hand to implementation? GO/NO-GO.

## Review Philosophy
- Quality assurance, not perfection. Critical issues ≤3. Interactive. Balanced strengths and weaknesses. Clear GO/NO-GO.

## Scope & Non-Goals
- Scope: design document quality → GO/NO-GO.
- Non-Goals: implementation-level design, technology research, final technology choice (left to design iterations).

## Core Review Criteria
1. **Fit with existing architecture**: boundaries, layers, dependency direction, coupling, module organization
2. **Consistency and standards**: naming, error handling, logging, configuration, data modeling
3. **Extensibility and maintainability**: separation of concerns, SRP, testability, appropriate complexity
4. **Types and interfaces**: type definitions, no `any`, API boundaries, input validation

## Review Process
1. **Analyze**: check the 4 criteria, focus on critical issues
2. **Critical Issues (≤3)**: each with Issue, Impact, Recommendation, Traceability (requirement ID), Evidence (design section)
3. **Strengths**: 1-2
4. **Decide**: GO (no critical mismatch, requirements met, clear implementation path) or NO-GO (fundamental conflict, critical gap, excessive complexity)

## Output Format
```
### Design Review Summary — 2-3 sentences (quality, readiness)
### Critical Issues (≤3) — Issue/Impact/Recommendation/Traceability/Evidence
### Design Strengths — 1-2
### Final Assessment — GO/NO-GO + rationale (1-2 sentences) + next step
```

## Length
- Summary 2-3 sentences. Each issue 5-7 lines. Total ~400 words.

## Checklist
- Critical issues ≤3, each with Impact and Recommendation
- Traceability: requirement ID per issue
- Evidence: design document location per issue
- Decision: GO/NO-GO with rationale and next step
