# agentic-psdd

Agentic PSDD (Progressive Spec-Driven Development) - Kiro-style spec workflow for an agentic SDLC: `AGENTS.md` (router + principles), `skills/kiro-*` (lean skill contracts), `templates/` (artifact structure).
Project-specific knowledge never lives here - it belongs to the consuming project's `.kiro/steering/`, `.kiro/specs/`, `.kiro/reference/`.

## Layout in a consuming project
```
methodology/                        this repo (submodule, subtree, or copy)
AGENTS.md                           the project's own file - a pointer block is prepended, rest is untouched
.agents/skills/<skill>               -> ../../methodology/skills/<skill>   (one symlink per skill)
.claude/skills/<skill>                -> ../../methodology/skills/<skill>   (one symlink per skill)
.kiro/settings/templates            -> ../../methodology/templates
.kiro/settings/.methodology-skills-manifest   list of skill names install.sh placed, so a later
                                     run can prune ones since removed/renamed upstream
.kiro/settings/.methodology-files-manifest    copy mode only: SHA-256 per placed file, so a later
                                     run refuses to overwrite files the project edited by hand
```
Skills are symlinked one by one, not as a whole `.agents/skills`/`.claude/skills` directory - a project already using its own skills there keeps them; only the `kiro-*` names come from `methodology/skills/`. Templates stay a single whole-directory symlink. `AGENTS.md` is deliberately never a symlink: many agent CLIs treat a project's root `AGENTS.md` as their own memory file and write to it in place, which through a symlink would corrupt the source `methodology/AGENTS.md`. Instead, `install.sh` prepends a managed block:
```
<!-- methodology:begin -->
Spec-driven work (`$kiro-*` skills, `.kiro/specs`, `.kiro/steering`): read `methodology/AGENTS.md` first. Other work does not need it.
<!-- methodology:end -->
```
The block goes to the top of the project's own `AGENTS.md` and leaves everything else in the file as-is. The block is conditional so sessions that do no spec work never load the methodology router (lazy loading, MoE); re-running install refreshes only that block, wherever it currently sits. Paths used by skills are names (`{{SPECS}}`, `{{STEERING}}`, `{{REFERENCE}}`, `{{TEMPLATES}}`, `{{SKILLS}}`) resolved by the `## Paths` table in `methodology/AGENTS.md`.

## Install
- Submodule: `git submodule add <url> methodology && methodology/install.sh link`
- Subtree: `git subtree add --prefix=methodology <url> main --squash && methodology/install.sh link`
- Copy (no dependency): `git clone <url> /tmp/m && /tmp/m/install.sh copy /path/to/project`

`install.sh link` symlinks each methodology skill individually under `.agents/skills/` and `.claude/skills/`, replaces `.kiro/settings/templates` with a symlink, and prepends/refreshes the pointer block in the project's own `AGENTS.md`; `copy` does the same with real files (one directory per skill) and copies the router to `.kiro/settings/methodology/AGENTS.md`, which the pointer block then names and can be re-run to update. A copy install records the SHA-256 of every file it placed; a later run (either mode) stops with exit 3 and lists any of those files the project has since edited, so hand edits are never silently discarded - move them into `.kiro/steering/` or a project-owned skill, or pass `--force` to overwrite.

## Language
Spec artifacts are written in whatever `spec.json.language` says for that spec (`templates/specs/init.json` ships `"ko"` as the default value new specs are created with). This is a per-project, per-spec setting, not something the methodology hardcodes - change the template's default or edit an individual spec's `spec.json` to switch. Internal reasoning and every agent-facing file (router, skill contracts, rules, template placeholders) stay in English regardless (`AGENTS.md`'s `Reason in English` rule) so mixed-language teams get consistent tool behavior; only the artifacts written for humans follow `spec.json.language` - body text, plus headings and fixed labels rendered from `templates/labels.md` (steering and discovery follow the project default in `templates/specs/init.json`).

## Skills
`skills/kiro-*` - one directory per skill, each a `SKILL.md` contract (Inputs / Outputs / Boundaries / Rules) plus its own `rules/` and `templates/`. See `skills/kiro-spec-status/rules/workflow.md` for how they chain together (discovery -> requirements -> biz-process -> design -> tasks -> implementation -> validation) and `## Skills` for invocation (`$kiro-<name>`).

## License
MIT - see `LICENSE`.
