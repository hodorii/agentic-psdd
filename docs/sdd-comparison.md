# SDD 방법론 비교 — Kiro, cc-sdd, spec-kit, agentic-psdd

> 기준(2026-09-30): Kiro 공식 문서, cc-sdd 커밋 `e2a0c67`, spec-kit v1.0.13(`f1a548a`), agentic-psdd `main`. 원형별 근거와 출처는 `kiro-cc-sdd-analysis.md`, `spec-kit-analysis.md`. 이 문서가 비교의 SSoT.

## 결론
- Kiro: IDE 제품. 사용자가 진입 유형 선택, UI 게이트, wave 동시 실행, Hooks와 PBT로 보강.
- cc-sdd: 에이전트 스킬 묶음. discovery 경로 분류, spec.json 승인, TDD와 서브에이전트 리뷰 루프, Boundary-first.
- spec-kit: 다중 에이전트 배포 플랫폼. 핵심 명령 10개 위에 확장, 프리셋, 워크플로, 번들; 핵심 기능도 확장으로 분리하는 중(v1.0.13 `github` 확장).
- agentic-psdd: cc-sdd 골격 + Kiro bugfix + spec-kit converge, clarify 규정 흡수, 여기에 가치사슬과 biz-process 계층, 산출물 유형별 검증, 라벨 표 현지화를 더함.

## 1. 구조
| 항목 | Kiro | cc-sdd | spec-kit | agentic-psdd |
|---|---|---|---|---|
| 형태 | IDE, CLI 제품 | 스킬 템플릿, `npx cc-sdd` 설치 | Python CLI `specify`, 휠 내장 에셋 | 라우터 + 스킬 계약 + 템플릿, `install.sh link/copy` |
| 대상 에이전트 | Kiro | 설치 시 선택한 에이전트 | 내장 통합 42 | `.agents/skills`, `.claude/skills` 규약 호스트 |
| 확장 | Powers, MCP | 스킬 추가 | 확장 5(1차) + 커뮤니티 176, 프리셋, 워크플로, 번들 | rules, templates 파일 추가, 경로 이름 표 |
| 자동화 | Hooks(태스크 전후 포함) | 스킬 체인 | 워크플로 엔진, 확장 훅, 런타임 이벤트 | 스킬 체인 수동, `-y`/`--auto` |

## 2. 흐름
| 단계 | Kiro | cc-sdd | spec-kit | agentic-psdd |
|---|---|---|---|---|
| 진입 | Feature, Bugfix, Quick 선택 | discovery 경로 A~E 자동 분류 | specify, bug, assess 독립 진입점 | discovery 경로 A~E(결정 근거 기록) + `GO / NEEDS_CLARIFICATION / STOP` |
| 프로젝트 원칙 | steering, inclusion 4종 | steering Bootstrap, Sync(drift 감지) | constitution.md, SemVer, 게이트 2회 | steering 3 + custom, inclusion, value-chain(초안과 승인 분리), 완료 시 Sync |
| 비즈니스 계층 | 없음 | 없음 | 없음(spec-of-specs roadmap) | value-chain Unit ↔ biz-process L1~L6(V-모델 좌측) |
| 요구사항 | EARS 대문자 `WHEN … SHALL` | EARS 문장형, 키워드 영어 고정 | 사용자 스토리 P1~P3 + FR, SC + Given/When/Then | `N.M: [조건] 결과`, 그룹명 대상과 의무 |
| 모호함 처리 | Analyze Requirements | validate-gap, 요구사항 review gate | 마커 3개 + informed guess, clarify | self-check 2회 초과 시 이전 단계, 질문 5개 이하 한 번에 하나, 추측 금지 |
| 설계 | Requirements-First 또는 Design-First | research.md, Boundary Commitments, File Structure Plan | plan.md + research, data-model, contracts, quickstart | cc-sdd 계승 + `Definition`, 검증 레벨 매핑 |
| 태스크 | 의존 그래프 | `(P)`, `_Boundary:`, `_Depends:` | `T001 [P] [US1]`, 테스트 선택 | + `_Difficulty:`, `_BizProcess:`, `DONE:` 필수 |
| 게이트 | UI Continue, CLI 체크포인트 | spec.json 플래그, `-y`도 review gate 유지 | 게이트 없음, "a map, not a required sequence" | spec.json 플래그, biz-process 포함 5단계 승인 |

## 3. 구현과 검증
| 항목 | Kiro | cc-sdd | spec-kit | agentic-psdd |
|---|---|---|---|---|
| 실행 | wave 내 동시, Autopilot/Supervised | 하위 태스크 1개씩 순차 | `[P]` 동시, 같은 파일 순차 | 의존 wave, wave 안 `(P)`만 동시(워크트리), 그 외 순차 |
| 구현 단위 | 코드 | 코드 | 코드 | 산출물 유형별(코드, 문서, 데이터, 설정, 분석) |
| 품질 게이트 | 사람 diff 리뷰, PBT | implementer, reviewer, debug, RED 필수 | implement 자기완료, TDD 권고 | 독립 리뷰어 13항목, RED 또는 미충족 목록, 크기와 주석 기준 |
| 재시도 | UNVERIFIED | 리뷰 2회 거부 → debug, 태스크당 2라운드 | 비병렬 실패 시 중단 | 2연속 실패 → 상위 모델 또는 debugger |
| 완료 검증 | PBT shrinking, PR | validate-impl GO/NO-GO, verify-completion | converge(append-only, 산출물 대 코드) | validate-impl(converge 규정 흡수), verify-completion + steering Sync |
| 버그 | bugfix.md + PBT | 스펙 없음(경로 B) | bug 확장 assess, fix, test | bugfix.md 3블록(Kiro 계승), 불변 동작은 속성으로 |
| 속성 기반 테스트 | 설계에서 도출(IDE) | 없음 | 없음 | 코드 산출물: `[always]`, 입력 범위, 불변 동작에서 도출, 필수 태스크 |
| 다중 스펙 | 없음 | roadmap + batch wave + cross-spec review | roadmap `R1..` + 슬라이스별 체인 | roadmap + batch wave(requirements까지) + 스펙 간 교차 검토 |

## 4. 언어와 원칙
| 항목 | Kiro | cc-sdd | spec-kit | agentic-psdd |
|---|---|---|---|---|
| 산출물 언어 | 규칙 없음 | `spec.json.language`, 헤딩 번역은 LLM 재량 | 헤딩 현지화 없음(JSON 비ASCII 보존만) | `spec.json.language` + 라벨 표(키, ko, en), 스펙 밖은 프로젝트 기본값 |
| 지침 언어 | 영어 | 영어, 언어별 한 문장 | 영어 | 에이전트용 파일 영어 |
| 코드 품질 원칙 | 없음 | Boundary-first | constitution 예시(Test-First 등) | Small Units, Why-Only Comment, Self-Documenting |

## 5. 강점
- Kiro: 제품 통합(Hooks, Supervised 모드), PBT로 요구사항과 테스트 연결, Design-First 진입.
- cc-sdd: 경로 분류와 다중 스펙 교차 검토, 태스크 그래프 sanity review, 재시도 상한과 debug 분류.
- spec-kit: 다중 에이전트 배포, 설치 파일 해시 추적, 프리셋 층위 해석, 워크플로 재개, 아이디어 평가(kill이 정상 결과).
- agentic-psdd: 가치사슬부터 태스크까지 ID 추적, 리뷰어의 경계와 의존 방향 기계 검사, 비코드 산출물 검증, 제목 현지화의 SSoT.

## 6. agentic-psdd 공백
| 공백 | 참조 원형 | 상태 |
|---|---|---|
| discovery 경로 정의 없음 | cc-sdd A~E | 해소: `kiro-discovery/rules/discovery-paths.md` |
| spec-batch 교차 검토 없음 | cc-sdd spec-batch | 해소: `kiro-spec-batch/rules/cross-spec-review.md` (requirements 단계, 승인 게이트 유지) |
| 태스크 실행 방식 미정 | Kiro wave, cc-sdd 순차 | 해소: `kiro-impl` 의존 wave 규칙 |
| 속성 기반 테스트 없음 | Kiro PBT | 해소: `verification-mapping.md` §4, 태스크, 리뷰어 |
| 이벤트 자동화 없음 | Kiro Hooks, spec-kit 워크플로 | 미해소: 호스트 hook 설정으로 대체 가능 |
