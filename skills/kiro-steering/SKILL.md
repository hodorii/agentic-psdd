---
name: kiro-steering
description: Lean contract for kiro-steering: manage steering, value chain, and specs knowledge.
---

# kiro-steering

Inputs
- brief.md
- value-chain.md (optional)

Outputs
- Core Indicators: STEERING_STATE, VALUE_CHAIN_LINKS, BOUNDARY_COMMITMENTS

Boundaries
- Only manage steering knowledge; no code changes.
- Never create or edit value-chain.md — it is owned by the product/business owner per its own header; read-only, same as kiro-biz-process.

Rules
- Read brief.md produced by kiro-orchestrate
- Read value-chain.md if present; if absent, do not create it — point the user to its bootstrap guide in `kiro-biz-process/rules/biz-process-rules.md`
- Read `rules/steering-principles.md` from this skill's directory for content granularity and lean-maintenance rules
- Read `{{TEMPLATES}}/steering/{product,tech,structure}.md` for baseline file structure
- Maintain boundary commitments in a separate artifact
- Do not modify specs directly
