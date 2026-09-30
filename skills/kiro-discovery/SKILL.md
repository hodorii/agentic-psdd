---
name: kiro-discovery
description: Lean contract for kiro-discovery: determine path and decompose work into specs.
---

# kiro-discovery

Inputs
- brief_seed.md
- project_state.json (optional)

Outputs
- Core Indicators: PATH_DETECTED, BOUNDARIES_DEFINED, SPEC_ROUTES, DECISION

Boundaries
- Determine path without enacting changes outside the discovery phase.

Rules
- Read brief_seed.md produced by kiro-orchestrate (or provided by user)
- Read `rules/discovery-paths.md` from this skill's directory; PATH_DETECTED = `A | B | C | D | E` with its deciding fact
- Define SPEC_ROUTES and relevant boundaries
- Write brief.md and roadmap.md, at the locations the path names, from `templates/brief.md` / `templates/roadmap.md` in this skill's directory
- Record evidence for and against the idea; tag each finding `cited` (source named) or `assumption`
- Close with DECISION: `GO` (problem and evidence hold; route to specs), `NEEDS_CLARIFICATION` (named unknowns and who resolves them), or `STOP` (decisive reason recorded). A documented STOP is a valid outcome, not a failure; resolve unknowns by editing brief.md, not by rerunning discovery
- Stop after outputting path and next-step guidance
