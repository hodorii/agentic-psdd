# Kiro · cc-sdd 방법론·템플릿 분석 — agentic-psdd 대조

> 분석 기준: gotalab/cc-sdd 커밋 `e2a0c67`(2026-09-23) 원본 파일, kiro.dev 공식 문서 `.md` 원문(2026-09-30 열람). 경로 약어 `G = https://github.com/gotalab/cc-sdd/blob/e2a0c67/`, `SK/x = G/tools/cc-sdd/templates/agents/claude-code-skills/skills/x/SKILL.md`, `T = G/tools/cc-sdd/templates/shared/settings/templates/specs/`. 확인 못 한 항목은 `UNVERIFIED`.

## 결론
- Kiro: IDE 제품 — 사용자가 Feature / Bugfix / Quick 선택, UI 게이트, wave 동시 실행, Hooks·PBT로 자동화·정합성 보강.
- cc-sdd: 에이전트 스킬 묶음 — discovery 자동 경로 분류(A~E), spec.json 승인 플래그, TDD·서브에이전트 리뷰 루프, Boundary-first 추적.
- agentic-psdd: cc-sdd 골격 계승 + Kiro bugfix 흡수 + 가치사슬·biz-process·`## 정의` 추가. 라벨 표로 헤딩 현지화(두 원형 모두 없음).
- 이 저장소의 공백 3건(§6): discovery 경로 정의 누락, spec-batch 범위 축소(cross-spec review 없음), 태스크 실행 방식 미정.

## 1. 흐름
| 단계 | Kiro | cc-sdd |
|---|---|---|
| 진입 | Feature(Requirements-First / Design-First) · Bugfix · Quick Spec · Plan mode — kiro.dev/docs/specs/feature-specs, /quick-spec, /plan | discovery가 경로 A~E 분류 — SK/kiro-discovery |
| 요구사항 | EARS `WHEN … THE SYSTEM SHALL`; 선택 Analyze Requirements(모순·모호·누락 엣지) — /specs/analyze-requirements | EARS 문장형, 서브에이전트 병렬 조사, "기술 선택 없이 쓸 수 있으면 요구사항" — SK/kiro-spec-requirements |
| 갭 | — | validate-gap(선택지 제공, brownfield 권장) — SK/kiro-validate-gap |
| 설계 | Design-First 가능; PBT 속성 도출(IDE) — /specs/correctness | 조사 full/light/minimal, research.md, Boundary Commitments·File Structure Plan 필수, 요구사항 갭이면 되돌림 — SK/kiro-spec-design |
| 설계 검증 | — | validate-design(핵심 이슈 ≤3, GO/NO-GO) — SK/kiro-validate-design |
| 태스크 | 의존 그래프 | `(P)` `_Boundary:_` `_Depends:_`, 전 요구사항 ID 포함 게이트, sanity review PASS/RETURN_TO_DESIGN — SK/kiro-spec-tasks |
| 구현 | Run all Tasks: wave 내 동시·wave 간 순차; Autopilot / Supervised — /specs, /ide/chat/autopilot | 하위 태스크 1개씩 순차; implementer → reviewer → verify-completion → 파일 지정 커밋 — SK/kiro-impl |
| 완료 | PBT 실패 시 shrinking 반례, Web은 PR | validate-impl GO/NO-GO/MANUAL_VERIFY_REQUIRED, verify-completion 신규 증거 필수 — SK/kiro-validate-impl, SK/kiro-verify-completion |
| 변경 추종 | Sync Files(태스크 재생성, 완료분 유지) — /specs/best-practices | Revalidation Triggers, upstream spec 수정 후 의존 spec 재검증 — G/docs/guides/spec-driven.md |

## 2. 게이트·자동화
- Kiro 승인: IDE "Proceed to Design"·Continue, CLI 체크포인트 + `Ctrl+X` 줄 단위 코멘트 — /specs, /specs/analyze-requirements. Quick Spec은 게이트 없음.
- cc-sdd 승인: `spec.json.approvals.{requirements,design,tasks}.{generated,approved}`; `-y`는 앞 단계 자동 승인, "review gate는 절대 우회 안 함"; spec-quick 기본 interactive, `--auto` 무정지 — SK/kiro-spec-tasks, SK/kiro-spec-quick
- 재시도 상한(cc-sdd): 리뷰 2회 거부 → debug(CATEGORY 8종, NEXT_ACTION 3종), 태스크당 debug 2라운드 → `_Blocked:_`, validate-impl 수정 3라운드 — SK/kiro-impl, SK/kiro-debug
- TDD(cc-sdd): reviewer는 `RED_PHASE_OUTPUT` 없으면 거부; Feature Flag TDD(OFF 실패·ON 통과·제거 후 통과) — SK/kiro-review, SK/kiro-impl
- Hooks(Kiro): `.kiro/hooks/<id>.json`, `command`/`agent`, 트리거 PromptSubmit·Pre/PostToolUse·File Create/Save/Delete·Pre/Post Task Execution 등, 차단 가능 PromptSubmit·PreToolUse·PreTaskExecution — /hooks. cc-sdd hook 연동 UNVERIFIED.

## 3. 다중 스펙·Steering
- cc-sdd discovery 경로: A 기존 spec 확장 / B spec 불필요(버그·설정·사소) / C 새 단일 spec / D 다중(여러 도메인 또는 태스크 20개 이상) / E 혼합 — SK/kiro-discovery. 접근안 2~3개, 서브에이전트 타당성 검증, 파일 기록 후 정지.
- cc-sdd spec-batch: roadmap 의존 wave, wave 내 서브에이전트 병렬로 init→tasks(design·tasks `-y`), cross-spec review(데이터 모델·인터페이스·공유 인프라·`_Boundary:_` 파일 중복) 최대 3라운드, 분해 결함이면 discovery 복귀 — SK/kiro-spec-batch
- Kiro 다중 spec 기능 없음(Web은 다중 저장소 단일 spec) — /specs
- Steering(Kiro): product/tech/structure, `inclusion: always | fileMatch | manual | auto`, `#[[file:…]]`, AGENTS.md 상시 포함, CLI는 inclusion 무시 — /steering
- Steering(cc-sdd): Bootstrap / Sync(drift 감지, 추가 보존), Golden Rule "기존 패턴을 따르는 새 코드는 steering 수정 불필요", 주제당 1파일·100~200줄; inclusion front matter 없음 — SK/kiro-steering

## 4. 템플릿
| 파일 | cc-sdd 헤딩(순서) — T |
|---|---|
| requirements.md | Requirements Document › Introduction › Boundary Context (Optional: In scope / Out of scope / Adjacent expectations) › Requirements › Requirement N (`**Objective:** As a …`) › Acceptance Criteria |
| design.md | Overview(Goals / Non-Goals) › Boundary Commitments(This Spec Owns / Out of Boundary / Allowed Dependencies / Revalidation Triggers) › Architecture › File Structure Plan › System Flows › Requirements Traceability › Components and Interfaces › Data Models › Error Handling › Testing Strategy › Optional Sections › Supporting References |
| tasks.md | Implementation Plan — `- [ ] N.M (P)`, `_Requirements:_` `_Boundary:_` `_Depends:_`, `- [ ]*` 선택 테스트 |
| research.md | Summary › Research Log › Architecture Pattern Evaluation › Design Decisions › Risks & Mitigations › References |
| bugfix | 없음 |

- Kiro bugfix.md: Current Behavior (Defect) `WHEN … THEN` / Expected Behavior (Correct) `SHALL` / Unchanged Behavior (Regression Prevention) `SHALL CONTINUE TO`; design에 근본 원인 + 속성 3종, tasks는 PBT — /specs/bugfix-specs
- Kiro 템플릿 헤딩 원문·ID 체계: 공식 문서 없음(UNVERIFIED). 비공식 재구성본 github.com/jasonkneen/kiro
- ID(cc-sdd): 숫자 전용 `N` / `N.M` — T/requirements.md L15

## 5. 언어
- cc-sdd: 설치 `--lang`(14개), spec-init이 입력 언어 감지해 `spec.json.language` 기록, 기본 `en`; 언어별 차이는 `DEV_GUIDELINES` 한 문장 — README "Language", SK/kiro-spec-init L26, `tools/cc-sdd/src/template/context.ts` L21-35
- 헤딩 사전 없음, 번역 여부 LLM 재량(UNVERIFIED); EARS 키워드만 영어 고정 — `rules/ears-format.md`
- Kiro: 출력 언어 규칙 문서화 없음(UNVERIFIED)

## 6. agentic-psdd 대조
| 항목 | Kiro | cc-sdd | agentic-psdd |
|---|---|---|---|
| 요구사항 표기 | `WHEN … SHALL` | EARS 문장형 | `N.M: [조건] 결과` |
| 추가 산출물 | — | research.md, spec.json | + biz-process.md(L1~L6), `Definition` 절, value-chain |
| bugfix | 있음(PBT) | 없음(경로 B) | 있음(Kiro 3블록 계승, PBT 없음) |
| 경계 | — | Candidates → Commitments → `_Boundary:_` | 동일 + requirements `Scope` |
| steering 로딩 | inclusion 4종 | 없음 | Kiro inclusion 채택 |
| 헤딩 현지화 | 없음 | 없음 | 라벨 표 `templates/labels.md` |
| discovery 경로 | 사용자 선택 | A~E 정의 | **PATH_DETECTED만 요구, 경로 정의 없음** — `skills/kiro-discovery/SKILL.md` |
| spec-batch | — | init→tasks + cross-spec review | **spec.json·requirements.md만, cross-spec review 없음** — `skills/kiro-spec-batch/SKILL.md` |
| 태스크 실행 | wave 동시 | 순차, `(P)` 정보용 | 미확인(이번 분석 범위 밖) |

## 7. 라벨 표 결정
- `en` 열: bugfix는 Kiro 원명, 나머지는 기존 agentic-psdd 이름 유지(cc-sdd 개명 `This Spec Owns`·`Out of Boundary`는 규칙 참조 안정성 위해 미채택)
- 표에 없는 언어 → `en`(cc-sdd 기본값과 동일)
- 대상: 스펙·steering·steering-custom·discovery 템플릿의 고정 헤딩·굵은 라벨·표 열 머리. 스펙은 `spec.json.language`, 스펙 밖 산출물은 `specs/init.json`의 `language`
- 제외: 기계 태그(`_Requirements:` 등), 식별자(`L1 Process`, `valueChainRef`)
- 키 분리: 설계 `not_owned`(Out-of-Scope, 비소유) ≠ brief `out_of_boundary`(Out of Boundary, 비목표)

## 검증 범위
- cc-sdd: 고정 커밋 원본 직접 확인. `ready_for_implementation` 전환 시점, hook 연동 UNVERIFIED
- Kiro: 공식 문서만. 템플릿 헤딩 원문, Design-First 승인 UI 세부, 태스크 실패 재시도 정책, Powers의 spec 연동 UNVERIFIED
