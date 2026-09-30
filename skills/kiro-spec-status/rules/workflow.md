# Workflow

Command order across phases. Read when choosing or reporting the next command.

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
  - Bugfix: `$kiro-bugfix {fix}` -> `$kiro-spec-design` -> `$kiro-spec-tasks`
- Phase 2 (Implementation): `$kiro-impl {feature} [tasks]` -> `$kiro-validate-impl {feature}` -> `$kiro-verify-completion`
- Ticket-driven: `$kiro-orchestrate`
- Progress: `$kiro-spec-status {feature}`
