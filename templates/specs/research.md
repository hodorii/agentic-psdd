# {{label.title_research}}

## {{label.summary}}
- **{{label.feature}}**: `<feature-name>`
- **{{label.discovery_scope}}**: New Feature / Extension / Simple Addition / Complex Integration
- **{{label.key_findings}}**:
  - Finding 1
  - Finding 2
  - Finding 3

## {{label.research_log}}
Document notable investigation steps and their outcomes. Group entries by topic for readability.

### [Topic or Question]
- **{{label.context}}**: What triggered this investigation?
- **{{label.sources_consulted}}**: Links, documentation, API references, benchmarks
- **{{label.findings}}**: Concise bullet points summarizing the insights
- **{{label.implications}}**: How this affects architecture, contracts, or implementation

_Repeat the subsection for each major topic._

## {{label.architecture_pattern_evaluation}}
List candidate patterns or approaches that were considered. Use the table format where helpful.

| Option | Description | Strengths | Risks / Limitations | Notes |
|--------|-------------|-----------|---------------------|-------|
| Hexagonal | Ports & adapters abstraction around core domain | Clear boundaries, testable core | Requires adapter layer build-out | Aligns with existing steering principle X |

## {{label.design_decisions}}
Record major decisions that influence `design.md`. Focus on choices with significant trade-offs.

### {{label.decision}}: `<Title>`
- **{{label.context}}**: Problem or requirement driving the decision
- **{{label.alternatives_considered}}**:
  1. Option A — short description
  2. Option B — short description
- **{{label.selected_approach}}**: What was chosen and how it works
- **{{label.rationale}}**: Why this approach fits the current project context
- **{{label.trade_offs}}**: Benefits vs. compromises
- **{{label.follow_up}}**: Items to verify during implementation or testing

_Repeat the subsection for each decision._

## {{label.risks_and_mitigations}}
- Risk 1 — Proposed mitigation
- Risk 2 — Proposed mitigation
- Risk 3 — Proposed mitigation

## {{label.references}}
Provide canonical links and citations (official docs, standards, ADRs, internal guidelines).
- [Title](https://example.com) — brief note on relevance
- ...
