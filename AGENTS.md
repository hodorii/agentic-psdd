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
이해 > 문서. 산출물은 "이해했음을 증명하는 최소 증거"다.
- **SSoT**: 규칙·값·템플릿·경로는 한 곳에만, 나머지는 참조. `value-chain.md`는 product owner 소유 — 스킬은 읽기만.
- **SRP**: 파일 하나 = 책임 하나.
  - **Small Units**: 함수·클래스·파일 크기는 steering `tech.md` 코드 품질 기준 이하. 초과 = 분리 신호, 유지 시 사유 명시.
- **Self-Documenting**: 주석 없이 이해되는 산출물.
  - **Descriptable Name**: 이름이 내용(WHAT)을 말한다.
  - **Why-Only Comment**: 코드 주석 기본 없음. 코드로 드러나지 않는 이유(WHY)만 한 줄. WHAT·요구사항/태스크 ID·경위 금지 — 추적은 `_Requirements:`와 git. 공개 API 문서 주석·라이선스 헤더·생성 코드 제외.
- **Goal Delivery**: 구현은 프로그램 작성이 아니라 스펙 `Definition`의 목표를 달성하는 산출물 전달 — 코드·문서·데이터·설정·분석. 검증은 산출물 유형별 증거(코드: 실패 테스트 → 통과; 비코드: 적용 전 미충족 목록 → 요구사항 ID별 산출물 위치).
- **지침 / 히스토리 분리**: `{{SKILLS}}`·`{{STEERING}}`에는 앞으로의 규칙만. 경위·결정·검증 기록은 `{{SPECS}}`와 git.
- **MoE**: 각 스킬은 독립 전문가 — 자기 rules·자기 산출물만, 필요한 단계에서만 로드. 산출물에 지시를 싣지 않는다; 평가 기준은 SKILL.md `Core Indicators`.
- **Lean**: 지침·산출물에 적용 — 개조식·명사형 동사, 부연 금지, 예시 1개. 인용구(`>`)는 보조 설명. 구조 장치(번호·섹션·표)는 정보를 담을 때만. 사용자 대면 보고는 반대로 결과 먼저·완전한 문장, 화살표 체인·약어 금지.

## Artifacts
- Labels: template headings and fixed labels are `{{label.<key>}}`; render from `{{TEMPLATES}}/labels.md`, column = `spec.json.language`; artifacts outside a spec (steering, discovery brief/roadmap) use the `language` of `{{TEMPLATES}}/specs/init.json`; absent column → `en`. Machine tags (`_Requirements:`, `_Boundary:`, `DONE:` …) and identifiers (`L1 Process`, `valueChainRef`) stay fixed. Rules name sections by the `en` label; checks locate them through the same row.
- `Definition` opens every spec artifact, one `definition_sentence`.
- Acceptance criteria `N.M: [condition] result` (no arrow; the bracket closes the condition); IDs unprefixed as numbered in requirements.md; contiguous ranges `2.1~2.5` allowed.
- Traceability: value-chain Unit ↔ biz-process L1 (`valueChainRef` / `bizProcessRef`, 값 복제 금지) → requirement IDs on L2/L3 → design Boundary Commitments → tasks `_Requirements:` / `_Boundary:` / `_BizProcess:` → validate-impl coverage.
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
- 승격(elevation): a standard-worthy artifact moves to `{{STEERING}}` or `{{REFERENCE}}`.
