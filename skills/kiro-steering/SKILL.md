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
- Bootstrap: write the missing baseline files; if value-chain.md is absent, draft it from `{{TEMPLATES}}/steering/value-chain.md` using brief.md and product.md: Value as root, Megas as PCF categories marked primary or support, Mains as process groups, Units as processes performed by roles (level meanings in `rules/standards-glossary.md`), every node a noun-phrase name with `evidence: cited <source>` or `assumption`, KPI numbers only in the product.md KPI table; `status: draft`, `owner:` named; then run doc lint (`rules/doc-lint.md`), fix draft errors, ask the owner to approve
- Sync: compare the feature's deliverable and design Key Decisions with steering; add what changed (additive, `updated_at`, reason) to product, tech, structure and boundary commitments; mark the feature `[x]` in `{{STEERING}}/roadmap.md`; list value-chain changes as proposals; report drift found; run doc lint (`rules/doc-lint.md`) and report its findings. STEERING_SYNC = files updated, roadmap check, proposals, doc lint result
- Read rows of `rules/standards-glossary.md` from this skill's directory when placing value-chain nodes or telling a process from a work item
- Read `rules/doc-lint.md` from this skill's directory when running the lint
- Read `rules/steering-principles.md` from this skill's directory for content granularity and lean-maintenance rules
- Read `{{TEMPLATES}}/steering/{product,tech,structure}.md` for baseline file structure
- Maintain boundary commitments in a separate artifact
- Do not modify specs directly
