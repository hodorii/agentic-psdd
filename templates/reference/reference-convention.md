# Reference Convention

> General rule for everything under `{{REFERENCE}}`; project-specific examples stay in the project.

## What belongs
- Regenerable facts: what exists now, extracted from a system or derived from a source artifact (schema lists, repository lists, reverse-engineered maps, derived views).
- Test: one regeneration command rebuilds it -> reference. A human judgment or rule (why it must behave so) -> `{{STEERING}}`, always loaded.
- Large measurements stay out of steering: they cost context every session; reference is lazy-loaded.

## Header (required)
First lines of every reference file, rendered from `{{TEMPLATES}}/labels.md`:
```
> {{label.reference_generated}}: <one-line regeneration command>
> {{label.reference_basis}}: <timestamp>; {{label.reference_source}}: <source system or file>
```
- Paths are relative to the repository root, never absolute.
- Separator is `;`: the middle dot is not Human-Typeable.

## Upkeep
- Not a frozen snapshot: rerun the source to refresh; do not maintain it by hand.
- A derived view keeps its original symbols only inside an `output` fence (`AGENTS.md`, Human-Typeable exception).
- Judgment or rules that should load automatically do not go here.
