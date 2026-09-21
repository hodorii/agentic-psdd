# agentic-psdd

Agentic PSDD (Progressive Spec-Driven Development) — Kiro-style spec workflow for an agentic SDLC: `AGENTS.md` (router + principles), `skills/kiro-*` (lean skill contracts), `templates/` (artifact structure).
Project-specific knowledge never lives here — it belongs to the consuming project's `.kiro/steering/`, `.kiro/specs/`, `.kiro/reference/`.

## Layout in a consuming project
```
methodology/                        this repo (submodule, subtree, or copy)
AGENTS.md                           the project's own file — a pointer block is prepended, rest is untouched
.agents/skills/<skill>               -> ../../methodology/skills/<skill>   (one symlink per skill)
.claude/skills/<skill>                -> ../../methodology/skills/<skill>   (one symlink per skill)
.kiro/settings/templates            -> ../../methodology/templates
```
Skills are symlinked one by one, not as a whole `.agents/skills`/`.claude/skills` directory — a project already using its own skills there keeps them; only the `kiro-*` names come from `methodology/skills/`. Templates stay a single whole-directory symlink. `AGENTS.md` is deliberately never a symlink: many agent CLIs treat a project's root `AGENTS.md` as their own memory file and write to it in place, which through a symlink would corrupt the source `methodology/AGENTS.md`. Instead, `install.sh` prepends a managed block —
```
<!-- methodology:begin -->
Full methodology: `methodology/AGENTS.md` — read it before doing anything here.
<!-- methodology:end -->
```
— to the top of the project's own `AGENTS.md` and leaves everything else in the file as-is; re-running install refreshes only that block, wherever it currently sits. Paths used by skills are names (`{{SPECS}}`, `{{STEERING}}`, `{{REFERENCE}}`, `{{TEMPLATES}}`, `{{SKILLS}}`) resolved by the `## Paths` table in `methodology/AGENTS.md`.

## Install
- Submodule: `git submodule add <url> methodology && methodology/install.sh link`
- Subtree: `git subtree add --prefix=methodology <url> main --squash && methodology/install.sh link`
- Copy (no dependency): `git clone <url> /tmp/m && /tmp/m/install.sh copy /path/to/project`

`install.sh link` symlinks each methodology skill individually under `.agents/skills/` and `.claude/skills/`, replaces `.kiro/settings/templates` with a symlink, and prepends/refreshes the pointer block in the project's own `AGENTS.md`; `copy` does the same with real files (one directory per skill, full content in the pointer block's place) and can be re-run to update.

## Language
Spec artifacts are written in whatever `spec.json.language` says for that spec (`templates/specs/init.json` ships `"ko"` as the default value new specs are created with). This is a per-project, per-spec setting, not something the methodology hardcodes — change the template's default or edit an individual spec's `spec.json` to switch. Internal reasoning stays in English regardless (`AGENTS.md`'s `Reason in English` rule) so mixed-language teams get consistent tool behavior; only the artifacts written for humans follow `spec.json.language`.

## Skills
`skills/kiro-*` — one directory per skill, each a `SKILL.md` contract (Inputs / Outputs / Boundaries / Rules) plus its own `rules/` and `templates/`. See `AGENTS.md`'s `## Workflow` for how they chain together (discovery → requirements → biz-process → design → tasks → implementation → validation) and `## Skills` for invocation (`$kiro-<name>`).

## License
MIT — see `LICENSE`.
