---
name: kiro-steering
description: Lean contract for kiro-steering: manage steering, value chain, and specs knowledge.
---

# kiro-steering

Inputs
- brief.md
- value-chain.md (optional)
- Sync: the completed feature's spec artifacts and deliverable

Outputs
- Core Indicators: STEERING_STATE, STEERING_SYNC, VALUE_CHAIN_LINKS, BOUNDARY_COMMITMENTS

Boundaries
- Only manage steering knowledge; no code changes.
- value-chain.md: draft only. Never set `status: approved` and never edit an approved file; changes to it are proposals in the Sync report.

Rules
- Read brief.md produced by kiro-orchestrate
- Mode by state: **Bootstrap** when `product.md`, `tech.md` or `structure.md` is absent; **Sync** when a feature passes `kiro-verify-completion` or on request
- Bootstrap: write the missing baseline files; if value-chain.md is absent, draft it from `{{TEMPLATES}}/steering/value-chain.md` using brief.md and product.md, `status: draft`, `owner:` named, each Mega and Unit tagged `evidence: cited <source> | assumption`, then ask the owner to approve
- Sync: compare the feature's deliverable and design Key Decisions with steering; add what changed (additive, `updated_at`, reason) to product, tech, structure and boundary commitments; mark the feature `[x]` in `{{STEERING}}/roadmap.md`; list value-chain changes as proposals; report drift found. STEERING_SYNC = files updated, roadmap check, proposals
- Read `rules/steering-principles.md` from this skill's directory for content granularity and lean-maintenance rules
- Read `{{TEMPLATES}}/steering/{product,tech,structure}.md` for baseline file structure
- Maintain boundary commitments in a separate artifact
- Do not modify specs directly
