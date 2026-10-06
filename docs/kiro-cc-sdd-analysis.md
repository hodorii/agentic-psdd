# Kiro, cc-sdd 방법론, 템플릿 분석 - agentic-psdd 대조

> 분석 기준: gotalab/cc-sdd 커밋 `e2a0c67`(2026-09-23) 원본 파일, kiro.dev 공식 문서 `.md` 원문(2026-09-30 열람). 경로 약어 `G = https://github.com/gotalab/cc-sdd/blob/e2a0c67/`, `SK/x = G/tools/cc-sdd/templates/agents/claude-code-skills/skills/x/SKILL.md`, `T = G/tools/cc-sdd/templates/shared/settings/templates/specs/`. 확인 못 한 항목은 `UNVERIFIED`.

## 결론
- Kiro: IDE 제품 - 사용자가 Feature / Bugfix / Quick 선택, UI 게이트, wave 동시 실행, Hooks, PBT로 자동화, 정합성 보강.
- cc-sdd: 에이전트 스킬 묶음 - discovery 자동 경로 분류(A~E), spec.json 승인 플래그, TDD, 서브에이전트 리뷰 루프, Boundary-first 추적.
- agentic-psdd: cc-sdd 골격 계승 + Kiro bugfix 흡수 + 가치사슬, biz-process, `Definition` 절 추가. 라벨 표로 헤딩 현지화(두 원형 모두 없음).
- agentic-psdd 공백과 네 방법론 비교: `sdd-comparison.md`.

## 1. 흐름
| 단계 | Kiro | cc-sdd |
|---|---|---|
| 진입 | Feature(Requirements-First / Design-First), Bugfix, Quick Spec, Plan mode - kiro.dev/docs/specs/feature-specs, /quick-spec, /plan | discovery가 경로 A~E 분류 - SK/kiro-discovery |
| 요구사항 | EARS `WHEN ... THE SYSTEM SHALL`; 선택 Analyze Requirements(모순, 모호, 누락 엣지) - /specs/analyze-requirements | EARS 문장형, 서브에이전트 병렬 조사, "기술 선택 없이 쓸 수 있으면 요구사항" - SK/kiro-spec-requirements |
| 갭 | - | validate-gap(선택지 제공, brownfield 권장) - SK/kiro-validate-gap |
| 설계 | Design-First 가능; PBT 속성 도출(IDE) - /specs/correctness | 조사 full/light/minimal, research.md, Boundary Commitments, File Structure Plan 필수, 요구사항 갭이면 되돌림 - SK/kiro-spec-design |
| 설계 검증 | - | validate-design(핵심 이슈 <=3, GO/NO-GO) - SK/kiro-validate-design |
| 태스크 | 의존 그래프 | `(P)` `_Boundary:_` `_Depends:_`, 전 요구사항 ID 포함 게이트, sanity review PASS/RETURN_TO_DESIGN - SK/kiro-spec-tasks |
| 구현 | Run all Tasks: wave 내 동시, wave 간 순차; Autopilot / Supervised - /specs, /ide/chat/autopilot | 하위 태스크 1개씩 순차; implementer -> reviewer -> verify-completion -> 파일 지정 커밋 - SK/kiro-impl |
| 완료 | PBT 실패 시 shrinking 반례, Web은 PR | validate-impl GO/NO-GO/MANUAL_VERIFY_REQUIRED, verify-completion 신규 증거 필수 - SK/kiro-validate-impl, SK/kiro-verify-completion |
| 변경 추종 | Sync Files(태스크 재생성, 완료분 유지) - /specs/best-practices | Revalidation Triggers, upstream spec 수정 후 의존 spec 재검증 - G/docs/guides/spec-driven.md |

## 2. 게이트, 자동화
- Kiro 승인: IDE "Proceed to Design", Continue, CLI 체크포인트 + `Ctrl+X` 줄 단위 코멘트 - /specs, /specs/analyze-requirements. Quick Spec은 게이트 없음.
- cc-sdd 승인: `spec.json.approvals.{requirements,design,tasks}.{generated,approved}`; `-y`는 앞 단계 자동 승인, "review gate는 절대 우회 안 함"; spec-quick 기본 interactive, `--auto` 무정지 - SK/kiro-spec-tasks, SK/kiro-spec-quick
- 재시도 상한(cc-sdd): 리뷰 2회 거부 -> debug(CATEGORY 8종, NEXT_ACTION 3종), 태스크당 debug 2라운드 -> `_Blocked:_`, validate-impl 수정 3라운드 - SK/kiro-impl, SK/kiro-debug
- TDD(cc-sdd): reviewer는 `RED_PHASE_OUTPUT` 없으면 거부; Feature Flag TDD(OFF 실패, ON 통과, 제거 후 통과) - SK/kiro-review, SK/kiro-impl
- Hooks(Kiro): `.kiro/hooks/<id>.json`, `command`/`agent`, 트리거 PromptSubmit, Pre/PostToolUse, File Create/Save/Delete, Pre/Post Task Execution 등, 차단 가능 PromptSubmit, PreToolUse, PreTaskExecution - /hooks. cc-sdd hook 연동 UNVERIFIED.

## 3. 다중 스펙, Steering
- cc-sdd discovery 경로: A 기존 spec 확장 / B spec 불필요(버그, 설정, 사소) / C 새 단일 spec / D 다중(여러 도메인 또는 태스크 20개 이상) / E 혼합 - SK/kiro-discovery. 접근안 2~3개, 서브에이전트 타당성 검증, 파일 기록 후 정지.
- cc-sdd spec-batch: roadmap 의존 wave, wave 내 서브에이전트 병렬로 init->tasks(design, tasks `-y`), cross-spec review(데이터 모델, 인터페이스, 공유 인프라, `_Boundary:_` 파일 중복) 최대 3라운드, 분해 결함이면 discovery 복귀 - SK/kiro-spec-batch
- Kiro 다중 spec 기능 없음(Web은 다중 저장소 단일 spec) - /specs
- Steering(Kiro): product/tech/structure, `inclusion: always | fileMatch | manual | auto`, `#[[file:...]]`, AGENTS.md 상시 포함, CLI는 inclusion 무시 - /steering
- Steering(cc-sdd): Bootstrap / Sync(drift 감지, 추가 보존), Golden Rule "기존 패턴을 따르는 새 코드는 steering 수정 불필요", 주제당 1파일, 100~200줄; inclusion front matter 없음 - SK/kiro-steering
- product.md 역할(Kiro, cc-sdd, agentic-psdd 동일): 제품의 why(목적, 대상 사용자, 핵심 기능, 비즈니스 목표). Kiro는 공식 문서, cc-sdd는 템플릿(Overview, Core Capabilities, Target Use Cases, Value Proposition)으로 확인. agentic-psdd는 같은 섹션에 KPI 표를 더해 KPI 수치의 유일한 정본으로 삼고, value-chain Unit의 `kpi:`가 id로 참조하며 doc lint가 참조를 검증 - kiro.dev/docs/steering, cc-sdd 템플릿 steering/product.md

## 4. 템플릿
| 파일 | cc-sdd 헤딩(순서) - T |
|---|---|
| requirements.md | Requirements Document > Introduction > Boundary Context (Optional: In scope / Out of scope / Adjacent expectations) > Requirements > Requirement N (`**Objective:** As a ...`) > Acceptance Criteria |
| design.md | Overview(Goals / Non-Goals) > Boundary Commitments(This Spec Owns / Out of Boundary / Allowed Dependencies / Revalidation Triggers) > Architecture > File Structure Plan > System Flows > Requirements Traceability > Components and Interfaces > Data Models > Error Handling > Testing Strategy > Optional Sections > Supporting References |
| tasks.md | Implementation Plan - `- [ ] N.M (P)`, `_Requirements:_` `_Boundary:_` `_Depends:_`, `- [ ]*` 선택 테스트 |
| research.md | Summary > Research Log > Architecture Pattern Evaluation > Design Decisions > Risks & Mitigations > References |
| bugfix | 없음 |

- Kiro bugfix.md: Current Behavior (Defect) `WHEN ... THEN` / Expected Behavior (Correct) `SHALL` / Unchanged Behavior (Regression Prevention) `SHALL CONTINUE TO`; design에 근본 원인 + 속성 3종, tasks는 PBT - /specs/bugfix-specs
- Kiro 템플릿 헤딩 원문, ID 체계: 공식 문서 없음(UNVERIFIED). 비공식 재구성본 github.com/jasonkneen/kiro
- ID(cc-sdd): 숫자 전용 `N` / `N.M` - T/requirements.md L15

## 4a. 같은 이름 문서의 역할 비교
같은 이름의 문서는 같은 역할을 기대한다. 아래 문서는 모두 역할이 일치하고 표기만 다르다.

| 문서 | Kiro | cc-sdd | agentic-psdd |
|---|---|---|---|
| product.md | 제품 목적, 대상 사용자, 핵심 기능, 비즈니스 목표 | 템플릿 Overview, Core Capabilities, Target Use Cases, Value Proposition | 같은 섹션 + KPI 표(KPI 수치의 유일한 정본, value-chain `kpi:`가 id로 참조, doc lint 검증) |
| tech.md | 프레임워크, 라이브러리, 개발 도구, 기술 제약 | 템플릿 Architecture, Core Technologies, 개발 표준, Key Technical Decisions; "표준과 패턴, 의존성 전부 아님" | cc-sdd 구조 + 코드 품질 크기 한도 |
| structure.md | 파일 구성, 이름 규칙, import 패턴, 아키텍처 결정 | 템플릿 Organization Philosophy, Directory Patterns, Naming, Import, Code Organization; "트리가 아니라 패턴" | cc-sdd 구조 |
| steering-custom | 사용자 정의 steering(예시 `api-standards.md`, `testing-standards.md`, `security-policies.md`); 위치 `.kiro/steering/`, 전역 `~/.kiro/steering/` | 7종 api-standards, authentication, database, deployment, error-handling, security, testing | cc-sdd와 같은 7종 |
| requirements.md | EARS 인수 기준 `WHEN ... THE SYSTEM SHALL` | 사용자 스토리 `As a / I want / so that` + When, If, While, Where 인수 기준; 제목은 숫자 ID만 | `Definition`, `Scope`, `N.M: [조건] 결과`; 사용자 스토리와 EARS 문장형은 쓰지 않음 |
| design.md, tasks.md | 아키텍처, 컴포넌트, 흐름, 테스트 전략 / 개별 실행 태스크 | 4절 표 | cc-sdd 계승 + `Definition`; tasks는 `_DoneWhen:_`, `_Difficulty:_`, `_BizProcess:_` 추가 |
| bugfix.md, research.md | 현재, 기대, 불변 동작 / 없음 | 없음 / 4절 표 | bugfix는 Kiro, research는 cc-sdd 계승 |
| init.json | 확인 못 함 | `feature_name`, 시각, `language`, `phase`, `approvals`, `ready_for_implementation` | `{{TIMESTAMP}}` 기반 init.json(`language` 기본 `ko`) |

- requirements.md 표기 차이의 이유: `N.M`은 값이 아니라 참조 키라 biz-process, design, tasks, 리뷰가 같은 번호를 쓴다(`design.md` 요구사항 ID 규칙). 수용 기준 형식은 화살표 없이 `[조건] 결과`(`design.md` 수용 기준 항목). 사용자 스토리와 EARS를 쓰지 않는 선택의 비교는 `sdd-comparison.md` 요구사항 행.
- cc-sdd에만 있는 `requirements-init.md`(프로젝트 설명 입력 + 생성 예정 표시 자리)는 agentic-psdd에 대응 파일이 없다. spec-init은 `spec.json`만 만들고 `requirements.md`는 kiro-spec-requirements가 처음 쓴다.
- Kiro 사용자 정의 steering 예시 파일명은 cc-sdd, agentic-psdd 이름과 다르다(`testing-standards.md` 대 `testing.md`). 역할은 같다.

## 5. 언어
- cc-sdd: 설치 `--lang`(14개), spec-init이 입력 언어 감지해 `spec.json.language` 기록, 기본 `en`; 언어별 차이는 `DEV_GUIDELINES` 한 문장 - README "Language", SK/kiro-spec-init L26, `tools/cc-sdd/src/template/context.ts` L21-35
- 헤딩 사전 없음, 번역 여부 LLM 재량(UNVERIFIED); EARS 키워드만 영어 고정 - `rules/ears-format.md`
- Kiro: 출력 언어 규칙 문서화 없음(UNVERIFIED)

## 6. agentic-psdd 대조
네 방법론 비교와 agentic-psdd 공백: `sdd-comparison.md`.

## 7. 라벨 표 결정
- `en` 열: bugfix는 Kiro 원명, 나머지는 기존 agentic-psdd 이름 유지(cc-sdd 개명 `This Spec Owns`, `Out of Boundary`는 규칙 참조 안정성 위해 미채택)
- 표에 없는 언어 -> `en`(cc-sdd 기본값과 동일)
- 대상: 스펙, steering, steering-custom, discovery 템플릿의 고정 헤딩, 굵은 라벨, 표 열 머리. 스펙은 `spec.json.language`, 스펙 밖 산출물은 `specs/init.json`의 `language`
- 제외: 기계 태그(`_Requirements:` 등), 식별자(`L1 Process`, `valueChainRef`)
- 키 분리: 설계 `not_owned`(Out-of-Scope, 비소유) != brief `out_of_boundary`(Out of Boundary, 비목표)

## 검증 범위
- cc-sdd: 고정 커밋 원본 직접 확인. `ready_for_implementation` 전환 시점, hook 연동 UNVERIFIED
- Kiro: 공식 문서만. 템플릿 헤딩 원문, Design-First 승인 UI 세부, 태스크 실패 재시도 정책, Powers의 spec 연동 UNVERIFIED
- product.md: Kiro의 갱신 규칙과 수치 규칙은 문서에 없음. cc-sdd의 inclusion 모드 사용 여부와 `/kiro:steering`의 product.md 생성 방식은 cc-sdd 자체 문서로 UNVERIFIED(검색 결과 보조 설명만)
- 4a절: Kiro는 steering, specs 공식 문서와 feature-specs 문서, cc-sdd는 고정 커밋이 아니라 main 브랜치의 템플릿 원본(steering, steering-custom, specs 디렉터리 목록과 requirements.md, requirements-init.md, init.json, tech.md, structure.md, product.md)을 열람. Kiro의 tech.md, structure.md는 공식 steering 문서와 외부 가이드 2건(dev.to Sienna, kirodotdev Roblox 글)을 확인했으나 설명만 있고 생성 파일 본문 예시가 없어 템플릿 헤딩 원문은 UNVERIFIED(Kiro IDE의 Generate Steering Docs 실행 결과로 확인 가능). Kiro 스펙 파일 저장 경로와 설정 파일(`.config.kiro` 여부)은 열람한 문서에 없어 UNVERIFIED
