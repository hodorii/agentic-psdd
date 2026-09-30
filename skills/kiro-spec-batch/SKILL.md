---
name: kiro-spec-batch
description: Lean contract for kiro-spec-batch: generate multiple specs from roadmap in parallel.
---

# kiro-spec-batch

Inputs
- `{{STEERING}}/roadmap.md`
- `{{SPECS}}/discovery/brief.md` (initiative brief from discovery path D or E)

Outputs
- Core Indicators: SPEC_LIST, BRIEFS, DEPENDENCY_ORDER, CROSS_SPEC_REVIEW

Boundaries
- Do not generate design or tasks; only spec.json, requirements.md and per-spec brief.md as output.

Rules
- Read `{{STEERING}}/roadmap.md` (inclusion: manual) produced by kiro-discovery or kiro-steering
- Read `{{SPECS}}/discovery/brief.md` (initiative) and each spec's roadmap line; write `{{SPECS}}/<feature>/brief.md` per new spec (BRIEFS)
- Group roadmap specs into dependency waves; within a wave generate specs in parallel sub-agents when the host supports them, otherwise sequentially
- Per spec emit spec.json (`{{TEMPLATES}}/specs/init.json`) and requirements.md following `{{SKILLS}}/kiro-spec-requirements/rules/acceptance-criteria-format.md` and `{{SKILLS}}/kiro-spec-requirements/rules/requirements-self-check.md`
- Then read `rules/cross-spec-review.md` from this skill's directory and run it across the batch; report CROSS_SPEC_REVIEW
- Do not modify existing specs without explicit approval
