# Agentic SDLC - Kiro-style Spec-Driven Development

## Paths
Skills refer to these names; relocate by editing this table.

| Name | Default | Holds |
|---|---|---|
| `{{SPECS}}` | `.kiro/specs` | one directory per feature or fix: spec.json, requirements.md or bugfix.md, biz-process.md, design.md, tasks.md, research.md |
| `{{STEERING}}` | `.kiro/steering` | project memory - rules and judgment |
| `{{REFERENCE}}` | `.kiro/reference` | regenerable measurements - one command rebuilds it; lazy-loaded; header rule `{{REFERENCE}}/reference-convention.md` |
| `{{TEMPLATES}}` | `.kiro/settings/templates` | artifact structure only: `labels.md`, `specs/`, `steering/`, `steering-custom/` |
| `{{SKILLS}}` | `.agents/skills` | `kiro-*/`: `SKILL.md` contract (Inputs / Outputs / Boundaries / Rules), `rules/` method, `templates/` sub-agent prompts; each skill symlinked individually (existing non-kiro skills untouched); `.claude/skills` mirrors the same per-skill links |

- `.kiro/specs` and `.kiro/steering` are Kiro IDE conventions.
- The methodology lives in `methodology/`; `{{SKILLS}}` (per-skill) and `{{TEMPLATES}}` (whole directory) are symlinked from there - `methodology/README.md`.
- The project root `AGENTS.md` is the project's own file, not a symlink - a managed pointer block (`<!-- methodology:begin/end -->`) is prepended to it, the rest of its content stays untouched. Not a symlink because a tool that overwrites `AGENTS.md` in place would otherwise write through it and corrupt this file.
- A local `AGENTS.md` in a subdirectory carries folder-specific context.

## Principles
Understanding over documents. An artifact is the minimum evidence that understanding exists.
- **SSoT**: rules, values, templates and paths live in one place; everything else references them. `value-chain.md` is owned by the product owner: skills may draft it (`status: draft`), only the owner approves (`status: approved`); once approved, skills read it and propose changes as drafts.
- **SRP**: one file, one responsibility.
  - **Small Units**: function, class and file sizes stay within the steering `tech.md` code-quality limits. Over the limit = split signal; keeping it needs a stated reason.
- **Self-Documenting**: artifacts understandable without comments.
  - **Descriptable Name**: a name states its content (WHAT).
  - **Why-Only Comment**: no code comments by default; one line only for a WHY the code cannot show. No WHAT, requirement or task IDs, or history - tracing is `_Requirements:` and git. Public API doc comments, license headers and generated code are exempt.
- **Goal Delivery**: implementation delivers what achieves the spec `Definition`, not just a program - code, document, data, config or analysis. Evidence per deliverable type (code: failing test then pass; non-code: pre-state gap list, then a location per requirement ID).
- **Human-Typeable**: guidance and artifacts use only characters a person types on a standard keyboard: visible ASCII plus the letters of the artifact's language. No other symbols or emoji; write the word or the ASCII form (`->`, `<->`, `-`, `...`, `<=`, `>=`, `!=`, `+/-`). Numbering levels `1.`, then `1)`, then `(1)`; circled numbers only where a word processor or slide tool generates them. Exception: verbatim quotes of external syntax. Reason: people edit artifacts directly, and artifacts should not read as machine-written.
- **Guidance vs history**: `{{SKILLS}}` and `{{STEERING}}` hold forward rules only; background, decisions and verification records live in `{{SPECS}}` and git.
- **MoE**: each skill is an independent expert - its own rules and artifacts, loaded only at its phase. Artifacts carry no instructions; evaluation criteria are SKILL.md `Core Indicators`.
  - **Lazy Loading**: keep the always-loaded surface minimal. Tier 0 always (router pointer, skill descriptions); tier 1 picked from a map (steering, reference); tier 2 on invocation (skill contract, then per-phase rules); tier 3 by path only (optional skills, archives). Read only the rows or sections needed. Tier follows location: skill descriptions 0; `{{STEERING}}` and `{{REFERENCE}}` 1 by `inclusion`; `rules/`, `templates/` 2; `docs/`, optional skills, archives 3. A project file outside these states its tier.
- **Lean**: for guidance and artifacts - terse bullets, noun or verb phrases, no elaboration, one example. Blockquotes (`>`) for side notes. Structure (numbering, sections, tables) only when it carries information. User-facing reports are the opposite: result first, complete sentences, no arrow chains or abbreviations. In names and inline lists, join two items with a conjunction, three or more with commas.

## Artifacts
- Labels: template headings and fixed labels are `{{label.<key>}}`; render from `{{TEMPLATES}}/labels.md` reading only the rows of keys the template uses (e.g., grep `^| <key> |`), never the whole table; column = `spec.json.language`; artifacts outside a spec (steering, discovery brief/roadmap) use the `language` of `{{TEMPLATES}}/specs/init.json`; absent column -> `en`. Machine tags (`_Requirements:`, `_Boundary:`, `_DoneWhen:` ...) and identifiers (`L1 Process`, `valueChainRef`) stay fixed. Templates hold no other fixed text: headings, bold labels and table headers are keys; author guidance is an HTML comment, never rendered; placeholder and example text sits in `[...]` or `<...>` and is replaced by the author (steering-custom example bodies included). Rules name sections by the `en` label; checks locate them through the same row.
- `Definition` opens every spec artifact except research.md (an investigation log), one `definition_sentence`.
- Acceptance criteria `N.M: [condition] result` (no arrow; the bracket closes the condition); IDs unprefixed as numbered in requirements.md; contiguous ranges `2.1~2.5` allowed.
- Traceability: value-chain Unit <-> biz-process L1 (`valueChainRef` / `bizProcessRef`, no value duplication) -> requirement IDs on L2/L3 -> design Boundary Commitments -> tasks `_Requirements:` / `_Boundary:` / `_BizProcess:` -> validate-impl coverage.
- Boundary term: discovery `Boundary Candidates` -> requirements `Scope` -> design `Boundary Commitments` -> tasks `_Boundary:`.
- Written in `spec.json.language`; ~200 lines cap, over = split signal.

## Workflow
Command order: `{{SKILLS}}/kiro-spec-status/rules/workflow.md` - read only when choosing the next command.

## Skills
- Invoke with `$kiro-<name>`; `/skills` lists them with their contracts' descriptions.
- If there is even a 1% chance a skill applies, invoke it.

## Rules
- Approval gates: Requirements or Bugfix -> BizProcess -> Design -> Tasks -> Implementation. Human review at each gate; `-y` only for an intentional fast-track.
- Reason in English. Follow the user's instructions precisely; within that scope act autonomously end-to-end, asking only when essential information is missing.
- When the user describes a problem or thinks aloud, the deliverable is an assessment: report and stop; change things only when asked.
- Report only what a tool result in this session evidences; say plainly what is unverified. Pause for the user only for destructive or irreversible actions, real scope changes, or input only they can give.

## Steering
Inclusion, Steering Sync and Elevation rules: `{{SKILLS}}/kiro-steering/rules/steering-principles.md` - read only for steering work.
