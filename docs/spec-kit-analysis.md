# github/spec-kit 분석 - agentic-psdd 대조

> 분석 기준: github/spec-kit 커밋 `adbd62a`(2026-09-24, v1.0.11 태그 `8147943` 이후) 클론을 파일 단위로 읽음. v1.0.13(`f1a548a`, 2026-09-29) 차이는 8절. 인용 경로는 spec-kit 저장소 기준. agentic-psdd 쪽은 `docs/design.md` 기준.

## 결론
spec-kit은 2025-08 출발한 4단계 선형 파이프라인에서 1년 만에 **다중 에이전트 대상 프로세스 배포 플랫폼**이 되었다. 방법론(헌법 1회, 기능마다 specify, clarify, plan, checklist, tasks, analyze, implement, converge)은 agentic-psdd와 같은 계열이나 투자 방향이 다르다.
- spec-kit: 배포, 확장, 자동화 기반 - 통합 42개(v1.0.13), 확장, 프리셋, 워크플로, 번들, 해시 추적 설치, 커뮤니티 카탈로그.
- agentic-psdd: 산출물 간 추적성과 구현 검증 엄격성 - 가치사슬, L1~L6, V-모델, 적대적 리뷰어, RED 증거, 실물 실행 증거.

## 1. 현황
| 항목 | 값 | 근거 |
|---|---|---|
| 파일 수 | 817 | 클론 `find` |
| 구현 | Python CLI `specify` (`src/specify_cli/`) | `README.md` |
| 릴리스 | 200회 이상, 최근 주 2~3회 (1.0.6 09-10 ... 1.0.11 09-24, 1.0.12 09-25, 1.0.13 09-29) | `CHANGELOG.md`, GitHub releases |
| 스타 | 약 132k (2026-09-01) | `newsletters/2026-August.md` |
| 내장 통합 | 42 (v1.0.13, mcode 추가) | `integrations/catalog.json` |
| 1차 확장 / 프리셋 / 번들 / 워크플로 | 5 (agent-context, git, bug, assess, github) / 2 (lean, constitution-sync) / 2 (bugfix, assess) / 3 | `extensions/`, `presets/`, `bundles/`, `workflows/` |
| 커뮤니티 카탈로그 (v1.0.13) | 확장 176, 프리셋 40, 번들 3, 워크플로 2 | `*/catalog.community.json` |
| 진입점 | SDD(코어), 버그 수정(bug 확장), 아이디어 평가(assess 확장) - "독립 진입점, 필수 3단계 아님" | `README.md` |
| 스튜어드 | Den Delimarsky -> Manfred Riem (2026-01-22) | `docs/history.md` |

## 2. 코어 SDD 프로세스
커맨드 템플릿 10개 `templates/commands/{constitution,specify,clarify,plan,checklist,tasks,analyze,implement,converge,taskstoissues}.md`. 공통 골격: `## User Input`($ARGUMENTS) -> 사전 훅 -> Outline -> 사후 훅 -> Completion Report -> `## Done When`.

| 단계 | 스크립트 | 산출물 | 게이트, 기계 검사 |
|---|---|---|---|
| constitution | `resolve-template.sh constitution-template` | `.specify/memory/constitution.md` | SemVer 증분 규칙(MAJOR/MINOR/PATCH), Sync Impact Report(HTML 주석), 거버넌스 외 요청은 Next Actions로 유보 |
| specify | (브랜치는 git 확장 훅) | `specs/NNN-name/spec.md`, `checklists/requirements.md`, `.specify/feature.json` | `[NEEDS CLARIFICATION]` **최대 3개**, 나머지 "informed guess"; 체크리스트 자기검증 최대 3회; 잔여 마커는 A/B/C 표로 질문 |
| clarify | `check-prerequisites.sh --paths-only` | spec.md `## Clarifications / ### Session <date>` | 10개 분류(기능 범위, 도메인/데이터, UX 흐름, NFR, 통합, 엣지, 제약, 용어, 완료 신호, 기타) Clear/Partial/Missing 스캔; 질문 <=5, **한 번에 정확히 하나**; 답변마다 즉시 반영 |
| plan | `setup-plan.sh` | plan.md, research.md(Phase 0), data-model.md, contracts/, quickstart.md(Phase 1) | Constitution Check를 Phase 0 전, Phase 1 후 2회; 위반은 Complexity Tracking 표에 정당화; tasks.md 생성 안 함 |
| checklist | `check-prerequisites.sh --template checklist-template` | `checklists/<domain>.md` | "Unit Tests for English": 요구사항 품질만, 구현 검증 동사(Verify/Test/Confirm) 금지, 항목 80% 이상 출처 태그 `[Spec §X.Y]`, `[Gap]`, `[Ambiguity]`, `[x]`는 리뷰어 소유 |
| tasks | `setup-tasks.sh` | tasks.md | 형식 `- [ ] T012 [P] [US1] ...`, 사용자 스토리 단위 Phase, **테스트 선택 사항**(명시 요청 시만), data-model 제약 원문 인용 |
| analyze | `check-prerequisites.sh --require-spec --require-tasks` | 보고서만(읽기 전용) | 6패스(중복, 모호, 미명세, 헌법 정합, 커버리지, 불일치), 헌법 충돌 자동 CRITICAL, 발견 <=50 |
| implement | 동상 | 코드, tasks.md `[X]` | 체크리스트 미완료 시 STOP 후 질문, `[P]` 동시 실행, 같은 파일 순차, 비병렬 실패 시 중단, "Follow TDD approach" |
| converge | 동상 | tasks.md 끝 `## Phase N: Convergence` 추가만 | "APPEND-ONLY, NEVER REWRITE"; 산출물이 "sole source of intent"; git diff 불사용; 체크박스 무관 전 태스크 재평가("completion claims are not evidence"); 발견 유형 missing/partial/contradicts/unrequested; 발견 0 -> Converged |
| taskstoissues | 동상 | GitHub 이슈 `T001: ...` | 제목 `T\d{3,}` 중복 제거 |

### 산출물 구조
- **spec.md**: User Scenarios & Testing(`### User Story N (Priority: P1~P3)` + Why this priority + Independent Test + Given/When/Then), Edge Cases, Requirements(`FR-001` "System MUST"), Key Entities, Success Criteria(`SC-001`, 기술 중립), Assumptions, Clarifications.
- **plan.md**: Summary, Technical Context(항목마다 "or NEEDS CLARIFICATION"), Constitution Check(GATE), Project Structure(문서 트리 + 소스 3옵션), Complexity Tracking.
- **tasks.md**: Phase 1 Setup, Phase 2 Foundational(Blocking), Phase 3+ 사용자 스토리별(MVP = US1, Tests OPTIONAL, Checkpoint), Phase N Polish, Dependencies & Execution Order, Parallel Example, Implementation Strategy.
- **constitution.md**: Core Principles(예시 I Library-First, II CLI Interface, III Test-First NON-NEGOTIABLE, IV Integration Testing, V Observability/Versioning/Simplicity), Governance, Version/Ratified/Last Amended.
- **추적성**: spec `FR-###`/`SC-###`/`US#` <-> tasks `[US#]` <-> converge `per FR-003 (missing)`. plan과 tasks 사이는 ID가 아니라 문서 읽기로 연결.

### 기능 디렉터리, 스크립트
- `specs/<NNN>-<name>/` - 순번(`%03d`) 또는 타임스탬프(`.specify/init-options.json feature_numbering`). `create-new-feature.sh`가 디렉터리, spec 템플릿, `.specify/feature.json` 생성. git 브랜치는 코어가 아니라 `git` 확장 `before_specify` 훅.
- 현재 기능 해석 순서: `SPECIFY_FEATURE_DIRECTORY` 환경변수, `.specify/feature.json`, 오류. 스크립트 bash, powershell, python 3종 동등 유지.

### 대규모 기능
- `docs/concepts/complex-features.md`: implement 범위 지정("T001~T010만"), `[P]` 태스크 서브에이전트 위임, 분해.
- `docs/concepts/spec-of-specs.md`: `roadmap.md` 표(`R1..` 불변 ID, Scope boundary, Depends on, Sub-spec) 후 슬라이스별 전체 체인; 워크트리로 병렬.
- `docs/concepts/spec-persistence.md`: 변경 모델 3종 - Flow-back(어느 산출물이든 수정 후 조정), Flow-forward(완료 디렉터리 불변, 변경마다 새 기능), Living spec(spec.md가 계약, plan/tasks 재생성). 기본값 없음, 헌법에 선택 기록.

### 초기 문서와의 불일치
`spec-driven.md`의 "Phase -1: Pre-Implementation Gates", "Don't guess", "specify가 브랜치 생성"은 현재 템플릿에 없다. 현행은 `## Constitution Check` + `## Complexity Tracking`, "Make informed guesses", 브랜치는 git 확장.

## 3. 플랫폼 다섯 원시
| 원시 | 정의 파일 | 핵심 |
|---|---|---|
| Integration | `src/specify_cli/integrations/<key>/__init__.py` | 베이스 4종(Markdown, Toml, Yaml, Skills) + Copilot 커스텀. 커맨드 템플릿 하나를 `$ARGUMENTS`/`{{args}}` 치환, `{SCRIPT}` 경로 치환, `__SPECKIT_COMMAND_X__` -> `/speckit.x`, `/speckit-x`, `$speckit-x`. 설치 파일마다 SHA-256을 `.specify/integrations/<key>.manifest.json`에 기록, 사용자가 수정한 파일은 제거하지 않음 |
| Extension | `extension.yml` | `provides{commands,templates,scripts,config}`, `hooks.before_/after_<cmd>`, 런타임 `events`. 커맨드명 `speckit.<ext>.<cmd>` 강제. 설정 4층(defaults -> config.yml -> local.yml -> env) |
| Preset | `preset.yml` | 코어, 확장의 커맨드 프롬프트, 템플릿, 스크립트를 `replace|prepend|append|wrap({CORE_TEMPLATE})`. 해석 순서: `.specify/templates/overrides/` -> 프리셋(priority) -> 확장 -> 코어. `specify artifact lookup`으로 승자 층 조회. `lean`은 코어 커맨드 5개를 짧은 프롬프트로 교체 |
| Workflow | `workflow.yml` | 스텝 타입 command, prompt, shell, init, slot, gate, if, switch, while, do-while, fan-out/in. 상태 `.specify/workflows/runs/<id>/{state.json,log.jsonl}`, gate에서 pause 후 `resume`. 오버레이로 스텝 삽입, 교체 |
| Bundle | `bundle.yml` | 역할별(developer, product-manager...) 확장, 프리셋, 워크플로 묶음. 런타임 없음, 핀 고정, 롤백 |

기타: 설치는 휠 내장 에셋만 사용(네트워크 불필요, 에어갭 지원). `AGENTS.md`/`CLAUDE.md`는 코어가 건드리지 않고 `agent-context` 확장이 담당. 텔레메트리 없음; "events"는 에이전트 훅(`session_start`, `pre_tool_use` 등) 배선. 인증은 사설 카탈로그, GHES 다운로드용.

## 4. 버그 수정, 아이디어 평가
- **bug** (`extensions/bug/commands/`): `speckit.bug.assess`(읽기 전용, 판정 valid / likely valid, needs reproduction / invalid) -> `fix`(유일한 코드 수정 단계, assessment.md가 계약, 이탈은 "Deviations from Assessment"에 기록 후 정지) -> `test`(소스 수정 금지, 판정 `verified|partial|failed`, 재현 미실행 시 partial 강등). 산출물 `.specify/bugs/<slug>/`.
- **assess** (`extensions/assess/commands/`): intake -> research(발견마다 `cited|ASSUMPTION` 태그, "Evidence Against the Idea" 필수) -> define -> shape(개념 수준만, 아키텍처 금지) -> decide(스코어카드 strong/adequate/weak/unknown, 판정 `go|needs-clarification|kill`). 산출물 `.specify/assessments/<slug>/`. "재실행 대신 산출물 수정으로 정제", 중단이 정상 결과.

## 5. 변천 요약
| 시점 | 변화 |
|---|---|
| 2025-08-22 0.0.1 | Specify CLI, specify, plan, tasks, implement, 헌법 |
| 2025-09~10 | constitution(0.0.40), clarify/analyze(0.0.52), checklist(0.0.57) 추가, `speckit.` 접두 |
| 2025-12~2026-02 | 릴리스 공백, 스튜어드 교체 |
| 2026-02-10 0.0.93 | 모듈형 확장 시스템(커뮤니티 기여) |
| 2026-02-19 0.0.99 | skills 설치 경로; 2026-08-05 0.16.0 Copilot 기본값 skills |
| 2026-03-13 0.3.0 | 프리셋 시스템 |
| 2026-03~04 0.4.x | 휠 내장 코어 팩(오프라인), 통합 베이스 클래스, 매니페스트, 레지스트리 |
| 2026-04-14 0.7.0 | 워크플로 엔진 |
| 2026-06 0.9.5~0.11.x | bug 확장, 레거시 플래그 제거, **converge**(0.11.2), bundle, PyPI |
| 2026-07 0.12~0.15 | Python 스크립트 포트, assess 확장, 런타임 이벤트 훅 |
| 2026-08-21 1.0.0 | "다섯 원시의 정합성" 선언, 안정성 약속 아님 |
| 2026-09 1.0.5~1.0.11 | 워크플로 슬롯, 1차 번들, `specify artifact` 조회 |
| 2026-09-25~29 1.0.12~1.0.13 | Bitbucket 인증, 프리셋 모듈 분리, `github` 확장(taskstoissues 이전 예고), mcode 통합, JSON 비ASCII 보존 |

철학 이동: 선형 파이프라인 -> 조합 가능한 원시; 3필수 단계 -> 독립 진입점; 헌법을 템플릿에 전파하던 방식 -> 런타임에 헌법을 읽는 방식(`docs/upgrade.md`); "8개 마크다운" 비판에 lean 프리셋으로 응답; "누가 스펙을 검증하나"에 상류(assess), 하류(converge)로 응답.

## 6. agentic-psdd 대조
네 방법론 비교와 agentic-psdd 공백: `sdd-comparison.md`.

## 7. agentic-psdd 반영 (2026-09-25)
1. **converge 상당 규정** -> `kiro-validate-impl/SKILL.md`: 산출물이 유일한 의도 원천, 체크박스 무관 전 태스크 재평가, 발견 분류 `missing | partial | contradicts | unrequested`, 기존 태스크 재작성, 재번호 금지, 발견 0이면 GO.
2. **clarify 커버리지 분류, 대화 규칙** -> `kiro-spec-requirements/rules/requirements-self-check.md`: 9개 영역 Clear/Partial/Missing 평가, 질문 <=5, 한 번에 하나, Recommended 표시, 답변 즉시 반영.
3. **checklist** -> 새 산출물 대신 같은 self-check의 기계 검사에 흡수: 모든 발견에 `[Gap] [Ambiguity] [Conflict] [Assumption]` 태그와 대상 ID, 구현 검증형 문장은 요구사항 발견이 아님. 산출물 수를 늘리지 않기 위한 선택.
4. **설치 파일 해시** -> `install.sh`: copy 모드가 `.kiro/settings/.methodology-files-manifest`에 파일별 SHA-256 기록, 이후 실행은 수정된 파일을 발견하면 exit 3, `--force`로 덮어씀, link 전환 시 매니페스트 삭제. 임시 프로젝트에서 시나리오 실행 확인.
5. **평가 판정** -> `kiro-discovery/SKILL.md` + `templates/brief.md`: Core Indicator `DECISION` = `GO | NEEDS_CLARIFICATION | STOP`, 찬반 근거를 `cited | assumption` 태그로 기록, 문서화된 STOP은 정상 결과, 미해결은 brief.md 수정으로 해소.
6. 따라가지 않은 것: 테스트 선택화, 모호함 추측 허용 - 증거 기반, 추측 금지 원칙과 충돌.

## 8. v1.0.11 -> v1.0.13 (2026-09-30 확인)
- 핵심 SDD 절차 변경 없음: `templates/` 트리 SHA `af00feb`, `templates/commands` `3c3e7fa`, `spec-driven.md` `28259ae` 두 태그 동일.
- 핵심 명령을 확장으로 분리: 1차 `github` 확장 `/speckit.github.taskstoissues`, 핵심 `taskstoissues`는 이전 예고(`docs/reference/agentic-sdd.md@v1.0.13`).
- `docs/guides/agentic-sdlc.md`: Spec Kit 자체 개발을 SDLC 7단계로 기술, "a map, not a required sequence"; 진행과 병합 결정은 메인테이너.
- 다중 에이전트 동시 실행: `SPECIFY_FEATURE_DIRECTORY`, `SPECIFY_FEATURE_NO_PERSIST` 권장(`docs/reference/core.md@v1.0.13`).
- 출처: GitHub release notes v1.0.12, v1.0.13; `compare/v1.0.11...v1.0.13`(커밋 41, 파일 115). CHANGELOG 본문 미확인.

## 검증 범위
- 세 조사 에이전트 보고를 종합. 다음은 원본 파일에서 직접 재확인: converge "APPEND-ONLY", "completion claims are not evidence"(`templates/commands/converge.md:73,148`), tasks 테스트 OPTIONAL(`templates/tasks-template.md:12`), 마커 3개 상한, informed guess(`templates/commands/specify.md:123,128,201`), 통합 41(`integrations/catalog.json`), 커맨드 10개 존재.
- 스타 수, 커뮤니티 카탈로그 수는 저장소 내 뉴스레터, JSON 값. GitHub 실시간 값 미확인.
- 초기 문서 불일치(2절)는 에이전트 보고 인용.

## 출처
- https://github.com/github/spec-kit
- https://github.github.com/spec-kit/
- https://github.com/github/spec-kit/releases
- https://github.blog/ai-and-ml/generative-ai/spec-driven-development-with-ai-get-started-with-a-new-open-source-toolkit/
- https://developer.microsoft.com/blog/spec-driven-development-spec-kit/
