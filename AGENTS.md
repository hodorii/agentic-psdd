# Agentic SDLC - Kiro-style Spec-Driven Development

## Paths
Skills refer to these names; relocate by editing this table.

| Name | Default | Holds |
|---|---|---|
| `{{SPECS}}` | `.kiro/specs` | one directory per feature or fix: spec.json, requirements.md or bugfix.md, biz-process.md, design.md, tasks.md, research.md |
| `{{STEERING}}` | `.kiro/steering` | project memory - rules and judgment |
| `{{REFERENCE}}` | `.kiro/reference` | regenerable measurements - one command rebuilds it; lazy-loaded; header rule `{{TEMPLATES}}/reference/reference-convention.md` |
| `{{ROLES}}` | unset | role files - per-role rules and judgment precedents shared across projects; a project sets its path here; tier 1 when set, not read when unset |
| `{{TEMPLATES}}` | `.kiro/settings/templates` | artifact structure only: `labels.md`, `specs/`, `steering/`, `steering-custom/`, `reference/` |
| `{{SKILLS}}` | `.agents/skills` | `kiro-*/`: `SKILL.md` contract (Inputs / Outputs / Boundaries / Rules), `rules/` method, `templates/` sub-agent prompts; each skill symlinked individually (existing non-kiro skills untouched); `.claude/skills` mirrors the same per-skill links |

- `.kiro/specs` and `.kiro/steering` are Kiro IDE conventions.
- The methodology lives in `methodology/`; `{{SKILLS}}` (per-skill) and `{{TEMPLATES}}` (whole directory) are symlinked from there - `methodology/README.md`.
- The project root `AGENTS.md` is the project's own file, not a symlink - a managed pointer block (`<!-- methodology:begin/end -->`) is prepended to it, the rest of its content stays untouched. Not a symlink because a tool that overwrites `AGENTS.md` in place would otherwise write through it and corrupt this file.
- A local `AGENTS.md` in a subdirectory carries folder-specific context.

## Principles
Understanding over documents. An artifact is the minimum evidence that understanding exists.

Common principles (SSoT, SRP, Small Units, Self-Documenting, Descriptable Name, Why-Only Comment, Lean, Keep the existing system, Guidance vs history, MoE, Lazy Loading): `PRINCIPLES.md` next to this file - one source; read it first. Their binding here:
- **SSoT**: `value-chain.md` is owned by the product owner: skills may draft it (`status: draft`), only the owner approves (`status: approved`); once approved, skills read it and propose changes as drafts.
- **Small Units**: sizes stay within the steering `tech.md` code-quality limits.
- **Why-Only Comment**: tracing is `_Requirements:` and git.
- **Guidance vs history**: `{{SKILLS}}` and `{{STEERING}}` are guidance; background, decisions and verification records live in `{{SPECS}}` and git.
- **MoE**: each skill is an expert - its own rules and artifacts, loaded only at its phase; evaluation criteria are SKILL.md `Core Indicators`; the work grade is the task `_Difficulty:`, mapped to a model in `kiro-impl` SKILL.md.
- **Lazy Loading**: tier follows location - tier 0 = router pointer, skill descriptions; tier 1 = `{{STEERING}}` and `{{REFERENCE}}` by `inclusion`; tier 2 = skill contract, then `rules/` and `templates/` per phase; tier 3 = `docs/`, optional skills, archives. A project file outside these states its tier; an unplaced file is not tier 0.
- **Lean**: blockquotes (`>`) for side notes. In names and inline lists, join two items with a conjunction, three or more with commas.

Spec-work principles:
- **Goal Delivery**: implementation delivers what achieves the spec `Definition`, not just a program - code, document, data, config or analysis. Evidence per deliverable type (code: failing test then pass; non-code: pre-state gap list, then a location per requirement ID).
- **Human-Typeable**: guidance and artifacts use only what a person can write by hand in a rich text editor (email level: bold, italic, strikethrough, lists, tables, links) or in Markdown (plus code spans, code blocks, HTML comments). Characters are visible ASCII plus the letters of the artifact's language; other symbols and emoji become words or ASCII (`->`, `<->`, `-`, `...`, `<=`, `>=`, `!=`, `+/-`). Numbering levels `1.`, then `1)`, then `(1)`; circled numbers never, since editors do not produce them. Exception: verbatim quotes of external syntax, captured tool output, and derived views (a regenerable rendering of a source artifact, e.g. the biz-process tree view, which keeps its original symbols), kept in a code fence whose info string is `quote` or `output` (a single line carries `lint-ignore: human-typeable`). Reason: people edit artifacts directly, and artifacts should not read as machine-written.
- **Knowledge layers**: three layers, each with one source of truth. Organization = this methodology and its common principles; role = rules and judgment precedents per role, shared across projects (`{{ROLES}}`); project = `{{SPECS}}`, `{{STEERING}}`, `{{REFERENCE}}`. A rule lives in the widest layer it holds for; a role precedent is advice for one role across projects, a steering rule binds this project.

## Artifacts
- Labels: template headings and fixed labels are `{{label.<key>}}`; render from `{{TEMPLATES}}/labels.md` reading only the rows of keys the template uses (e.g., grep `^| <key> |`), never the whole table; column = `spec.json.language`; artifacts outside a spec (steering, discovery brief/roadmap) use the `language` of `{{TEMPLATES}}/specs/init.json`; absent column -> `en`. Machine tags (`_Requirements:`, `_Boundary:`, `_DoneWhen:` ...) and identifiers (`L1 Process`, `valueChainRef`) stay fixed. Templates hold no other fixed text: headings, bold labels and table headers are keys; author guidance is an HTML comment, never rendered; placeholder and example text sits in `[...]` or `<...>` and is replaced by the author (steering-custom example bodies included). Rules name sections by the `en` label; checks locate them through the same row.
- `Definition` opens every spec artifact except research.md (an investigation log), one `definition_sentence`.
- Acceptance criteria `N.M: [condition] result` (no arrow; the bracket closes the condition); IDs unprefixed as numbered in requirements.md; contiguous ranges `2.1~2.5` allowed.
- Traceability: value-chain Unit (Value > Mega > Main > Unit = PCF Category > Process Group > Process) <-> biz-process L1 (`valueChainRef` / `bizProcessRef`, no duplication) -> requirement IDs on L2/L3 -> L4 ids and `BR-` rules -> design Boundary Commitments and Key Decisions `D<n>` -> tasks `_Requirements:` / `_Boundary:` / `_BizProcess:` -> validate-impl coverage.
- Review edition (optional): a text of design.md for reviewers outside the implementation team; design.md stays the original, the edition is a derived view with a `derived-from` declaration and decision-id parity checked by doc lint - `{{SKILLS}}/kiro-spec-design/rules/review-edition.md`.
- Standard terms and the process vs work item test: `{{SKILLS}}/kiro-steering/rules/standards-glossary.md`.
- Boundary term: discovery `Boundary Candidates` -> requirements `Scope` -> design `Boundary Commitments` -> tasks `_Boundary:`.
- Written in `spec.json.language`; ~200 lines cap, over = split signal.

## Workflow
Command order: `{{SKILLS}}/kiro-spec-status/rules/workflow.md` - read only when choosing the next command.

## Skills
- Invoke with `$kiro-<name>`; `/skills` lists them with their contracts' descriptions.
- If there is even a 1% chance a skill applies, invoke it.
- Every phase, even with steering/spec context already loaded: use explicitly requested skills and task-relevant local skills/playbooks (design, accessibility, UX included). Select by description, read only the guidance needed, keep required checks and host/project rules.

## Rules
- Approval gates: Requirements or Bugfix -> BizProcess -> Design -> Tasks -> Implementation. Human review at each gate; `-y` only for an intentional fast-track. An approved requirements.md or bugfix.md changes only on the user's decision: work that needs a requirement the spec lacks reports it and does not write it.
- Reason in English. Follow the user's instructions precisely; within that scope act autonomously end-to-end, asking only when essential information is missing.
- When the user describes a problem or thinks aloud, the deliverable is an assessment: report and stop; change things only when asked.
- Report only what a tool result in this session evidences; say plainly what is unverified. Pause for the user only for destructive or irreversible actions, real scope changes, or input only they can give.

## Steering
Inclusion, Steering Sync and Elevation rules: `{{SKILLS}}/kiro-steering/rules/steering-principles.md` - read only for steering work.
