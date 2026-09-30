# Agentic SDLC — Kiro-style Spec-Driven Development

## Paths
Skills refer to these names; relocate by editing this table.

| Name | Default | Holds |
|---|---|---|
| `{{SPECS}}` | `.kiro/specs` | one directory per feature or fix: spec.json, requirements.md or bugfix.md, biz-process.md, design.md, tasks.md, research.md |
| `{{STEERING}}` | `.kiro/steering` | project memory — rules and judgment |
| `{{REFERENCE}}` | `.kiro/reference` | regenerable measurements — one command rebuilds it; lazy-loaded; header rule `{{REFERENCE}}/reference-convention.md` |
| `{{TEMPLATES}}` | `.kiro/settings/templates` | artifact structure only: `specs/`, `steering/`, `steering-custom/` |
| `{{SKILLS}}` | `.agents/skills` | `kiro-*/`: `SKILL.md` contract (Inputs / Outputs / Boundaries / Rules), `rules/` method, `templates/` sub-agent prompts; each skill symlinked individually (existing non-kiro skills untouched); `.claude/skills` mirrors the same per-skill links |

- `.kiro/specs` and `.kiro/steering` are Kiro IDE conventions.
- The methodology lives in `methodology/`; `{{SKILLS}}` (per-skill) and `{{TEMPLATES}}` (whole directory) are symlinked from there — `methodology/README.md`.
- The project root `AGENTS.md` is the project's own file, not a symlink — a managed pointer block (`<!-- methodology:begin/end -->`) is prepended to it, the rest of its content stays untouched. Not a symlink because a tool that overwrites `AGENTS.md` in place would otherwise write through it and corrupt this file.
- A local `AGENTS.md` in a subdirectory carries folder-specific context.

## Principles
Understanding over documents. An artifact is the minimum evidence that understanding exists.
- **SSoT**: rules, values, templates and paths live in one place; everything else references them. `value-chain.md` is owned by the product owner; skills only read it.
- **SRP**: one file, one responsibility.
  - **Small Units**: function, class and file sizes stay within the steering `tech.md` code-quality limits. Over the limit = split signal; keeping it needs a stated reason.
- **Self-Documenting**: artifacts understandable without comments.
  - **Descriptable Name**: a name states its content (WHAT).
  - **Why-Only Comment**: no code comments by default; one line only for a WHY the code cannot show. No WHAT, requirement or task IDs, or history — tracing is `_Requirements:` and git. Public API doc comments, license headers and generated code are exempt.
- **Goal Delivery**: implementation delivers what achieves the spec `Definition`, not just a program — code, document, data, config or analysis. Evidence per deliverable type (code: failing test then pass; non-code: pre-state gap list, then a location per requirement ID).
- **Guidance vs history**: `{{SKILLS}}` and `{{STEERING}}` hold forward rules only; background, decisions and verification records live in `{{SPECS}}` and git.
- **MoE**: each skill is an independent expert — its own rules and artifacts, loaded only at its phase. Artifacts carry no instructions; evaluation criteria are SKILL.md `Core Indicators`.
- **Lean**: for guidance and artifacts — terse bullets, noun or verb phrases, no elaboration, one example. Blockquotes (`>`) for side notes. Structure (numbering, sections, tables) only when it carries information. User-facing reports are the opposite: result first, complete sentences, no arrow chains or abbreviations. No middle dot `·` anywhere: commas; in names, a conjunction for two items.

## Artifacts
- Labels: template headings and fixed labels are `{{label.<key>}}`; render from `{{TEMPLATES}}/labels.md`, column = `spec.json.language`; artifacts outside a spec (steering, discovery brief/roadmap) use the `language` of `{{TEMPLATES}}/specs/init.json`; absent column → `en`. Machine tags (`_Requirements:`, `_Boundary:`, `DONE:` …) and identifiers (`L1 Process`, `valueChainRef`) stay fixed. Rules name sections by the `en` label; checks locate them through the same row.
- `Definition` opens every spec artifact, one `definition_sentence`.
- Acceptance criteria `N.M: [condition] result` (no arrow; the bracket closes the condition); IDs unprefixed as numbered in requirements.md; contiguous ranges `2.1~2.5` allowed.
- Traceability: value-chain Unit ↔ biz-process L1 (`valueChainRef` / `bizProcessRef`, no value duplication) → requirement IDs on L2/L3 → design Boundary Commitments → tasks `_Requirements:` / `_Boundary:` / `_BizProcess:` → validate-impl coverage.
- Boundary term: discovery `Boundary Candidates` → requirements `Scope` → design `Boundary Commitments` → tasks `_Boundary:`.
- Written in `spec.json.language`; ~200 lines cap, over = split signal.

## Workflow
- Phase 0 (optional): `$kiro-steering`, `$kiro-steering-custom`
- Discovery: `$kiro-discovery "idea"`
- Phase 1 (Specification): `$kiro-spec-quick {feature} [--auto]` or step by step:
  - `$kiro-spec-init {feature}`
  - `$kiro-spec-requirements {feature}`
  - `$kiro-validate-gap {feature}` (optional)
  - `$kiro-biz-process {feature}`
  - `$kiro-spec-design {feature} [-y]`
  - `$kiro-validate-design {feature}` (optional)
  - `$kiro-spec-tasks {feature} [-y]`
  - Multi-spec: `$kiro-spec-batch`
  - Bugfix: `$kiro-bugfix {fix}` → `$kiro-spec-design` → `$kiro-spec-tasks`
- Phase 2 (Implementation): `$kiro-impl {feature} [tasks]` → `$kiro-validate-impl {feature}` → `$kiro-verify-completion`
- Ticket-driven: `$kiro-orchestrate`
- Progress: `$kiro-spec-status {feature}`

## Skills
- Invoke with `$kiro-<name>`; `/skills` lists them with their contracts' descriptions.
- If there is even a 1% chance a skill applies, invoke it.

## Rules
- Approval gates: Requirements or Bugfix → BizProcess → Design → Tasks → Implementation. Human review at each gate; `-y` only for an intentional fast-track.
- Reason in English. Follow the user's instructions precisely; within that scope act autonomously end-to-end, asking only when essential information is missing.
- When the user describes a problem or thinks aloud, the deliverable is an assessment: report and stop; change things only when asked.
- Report only what a tool result in this session evidences; say plainly what is unverified. Pause for the user only for destructive or irreversible actions, real scope changes, or input only they can give.

## Steering
- `inclusion` front matter (Kiro): `always` (default when absent) every session; `manual` only when a skill reads it by path; `fileMatch` / `auto` per Kiro docs.
- `always` baseline: `product.md`, `tech.md`, `structure.md`. Custom files via `$kiro-steering-custom`; every new file states its `inclusion`.
- Steering Sync: on code diff, additive, per repository, at ticket or feature completion.
- Elevation: a standard-worthy artifact moves to `{{STEERING}}` or `{{REFERENCE}}`.
