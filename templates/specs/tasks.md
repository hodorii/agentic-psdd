# {{label.title_tasks}} - <feature>

## {{label.definition}}
{{label.definition_sentence}}

- [ ] 1. [major task]
- [ ] 1.1 [sub-task]
  - _DoneWhen: [observable done state - rendered frame or output for tasks with screen or output]_
  - _Requirements: 1.1, 1.2_
  - _Difficulty: mid_

- [ ] 2. [major task]
- [ ] 2.1 (P) [sub-task]
  - _DoneWhen: [observable done state]_
  - _Requirements: 2.1_
  - _Difficulty: low_
  - _Boundary: [Component]_
  - _Depends: 1.1_
  - _BizProcess: BP-<ID>.L4_
- [ ]* 2.2 [optional test task]
  - _DoneWhen: [observable done state]_
  - _Requirements: 2.1_
