---
name: kiro-impl
description: Lean contract for kiro-impl: deliver approved tasks toward the spec goal — code, document, data, config or analysis.
---

# kiro-impl

Inputs
- brief.md
- requirements.md
- design.md
- tasks.md

Outputs
- Core Indicators: STATUS, VERIFICATION_RESULTS, DELIVERABLE_CHANGES, TASKS_UPDATE, ERROR_FLAGS

Boundaries
- Deliver only tasks approved in specs; do not modify scope beyond current tasks.

Rules
- Read brief.md produced by kiro-spec-init
- Read requirements.md produced by kiro-spec-requirements
- Read design.md produced by kiro-spec-design
- Read tasks.md produced by kiro-spec-tasks
- Deliverable type per task (`code` | `document` | `data` | `config` | `analysis`) comes from design.md File Structure Plan; pass it to implementer and reviewer, which apply the matching verification
- Dispatch each task to a sub-agent built from `templates/implementer-prompt.md`, gate it with `templates/reviewer-prompt.md`, and on blockers use `templates/debugger-prompt.md` (all from this skill's directory) — pass only the task-relevant sections of requirements.md/design.md
- Parallel implementers on one crate work in separate git worktrees (one per session); the orchestrator verifies each result in isolation at HEAD and merges. A shared working tree makes regenerated artifacts (goldens, snapshots) and tests thrash across sessions
- Sessions rotate: one session per major task group at most, and a new session before context compaction would trigger (rotate at ~50% of the window); small-context implementers get one fresh session per task. Compaction loses working context — handoff through tasks.md and git is cheaper
- Effort by `_Difficulty:` for implementers that expose it — low: medium, mid: high, high: xhigh
- The brief opens with the spec's `Definition` section. A `low` brief includes the Procedure appendix of `templates/implementer-prompt.md`; capable implementers get the Contract sections only. Never show sub-agents remaining-context counts
- Match implementer to `_Difficulty:` — `low` may go to a small-context model with a self-contained brief; `mid`/`high` go to the strongest available. Two consecutive failures on a task → reassign upward or dispatch the debugger
- The reviewer gate runs the verification itself and, for user-visible output, inspects the rendered frame/output; the implementer's claim is not evidence
- Real runs start from the default launch (no flags, every panel visible) and add one narrow width; a run in the configuration easiest to capture verifies the renderer, not the product
- Update STATUS and DELIVERABLE_CHANGES upon completion
- Do not proceed beyond approved tasks without reviewer approval
