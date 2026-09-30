# {{label.title_design}} — <feature>

## {{label.definition}}
{{label.definition_sentence}}

## {{label.boundary_commitments}}

### {{label.this_spec_owns}}
- **[책임 영역]**: [소유하는 동작·데이터 1줄]

### {{label.not_owned}}
- **[비소유 영역]**: [누가 소유하는지]

### {{label.allowed_dependencies}}
- 외부: [라이브러리 + 버전]
- 내부 의존 방향: `a` → `b` → `c` (역방향 import = 설계 위반)

### {{label.revalidation_triggers}}
- [이 설계의 전제가 깨져 재검토가 필요한 조건 — 계약·소유·의존 방향·런타임 전제·규모]

## {{label.architecture}}

### {{label.boundary_map}}
[Mermaid — 모듈/컴포넌트와 의존 방향. 복잡 기능 필수]

### {{label.technology_stack}}
| Layer | Choice | Role |
|-------|--------|------|
| | | |

### {{label.key_decisions}}
- **[결정]**: [내용] — 이유: [근거 1줄]. 대안 비교는 research.md.

## {{label.system_flows}}
[비자명 흐름만, Mermaid sequence/state. 없으면 절 생략]
- [흐름별 결정 사항 — 요구사항 ID 태그 (예: 7.2)]

## {{label.components_and_interfaces}}

### [module] — [Component]
- {{label.intent}}: [책임 1줄]
- {{label.requirements}}: [2.1~2.5, 3.1]
```[lang]
[공개 시그니처·타입 — 구현 언어 그대로. 오류 타입 포함]
```
- [계약 특이사항: 이벤트·상태·실패 모드]

## {{label.data_models}}
[도메인 타입·영속 구조·불변식 — 위 인터페이스로 충분하면 그렇게 명시]

## {{label.error_handling}}
- **{{label.user_input_error}}**: [처리 + 요구사항 ID]
- **{{label.external_resource_error}}** (파일·네트워크·권한): [격리 방식]
- **{{label.system_error}}** (패닉·예외): [복구·종료 경로]
- **{{label.graceful_degradation}}**: [의존 실패 시 폴백]

## {{label.testing_strategy}}
- **{{label.test_depth}}**: [Trivial | Standard | Complex — 근거 1줄]
- **{{label.unit_test}}**: [모듈별 핵심 케이스 + 요구사항 ID]
- **{{label.integration_test}}**: [경계 횡단 시나리오]
- **{{label.e2e_test}}**: [biz-process L2 흐름 대응]
- **{{label.acceptance_test}}**: [수용 기준 충족 + 실물 실행 확인]
- **{{label.performance_test}}**: [필요 시 수치]

## {{label.file_structure_plan}}
```
[디렉터리 트리 + 책임 주석 — 모든 컴포넌트가 파일 경로를 가져야 함]
```

## {{label.optional_sections}}
Security / Performance / Migration
