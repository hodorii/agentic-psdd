# Acceptance Criteria Format

One criterion per line under a numbered requirement group, inside the `Requirements` section:

```
### N. [subject + obligation]
- N.M: [condition] result
```

- Group name: subject + obligation — what the deliverable must provide (`공정변수 정의`, `PINN 예측 정확도 산출 방법`). A bare topic (`명령안`, `증빙`) or a vague link word (`연계`) is not a name.
- `[condition]`: the triggering event, state, failure, or option; `[항상]` for invariants; combine with `+`.
- `[result]`: what is observable — rendered output, exit code, file state, message. No implementation terms (framework, module, table).
- No arrow: the closing `]` separates condition from result. One behavior per line. Measurable words (`2초 이내`), never "fast" / "robust".

Examples
- `1.3: [루트 탐색 실패] 탐색 경로 포함 오류를 stderr 출력, 비제로 종료`
- `7.6: [감시 불가 환경] 상태 표시줄에 '감시 불가' 표시, r 키로 수동 갱신`
- `8.1: [항상] 감시 대상 디렉터리 아래 어떤 파일도 생성/수정/삭제하지 않음`
