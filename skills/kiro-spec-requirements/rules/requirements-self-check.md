# Requirements Review Gate

Before writing `requirements.md`, review the draft requirements and repair local issues until the draft passes or a true scope ambiguity is discovered.

## Boundary Continuity

Use boundary terminology consistently across phases without turning requirements into design:

- **Discovery** identifies `Boundary Candidates`
- **Requirements** make inclusion, exclusion, and adjacent expectations explicit when scope could be misread
- **Design** turns those into `Boundary Commitments`
- **Tasks** use `_Boundary:_` to constrain executable work

Requirements should clarify the feature boundary in user- or operator-observable terms, not in architecture ownership or implementation detail.

## Scope and Coverage Review

- The draft must cover the feature's core user journeys, major scope boundaries, primary error cases, and meaningful edge conditions that are visible to the user or operator.
- Rate each coverage area `Clear` / `Partial` / `Missing`: functional scope and behavior, domain and data model, user flow and UX, non-functional (performance, scale, reliability, observability), integrations and external dependencies, edge cases and failure handling, constraints and trade-offs, terminology and consistency, completion signals (what "done" looks like to the user). `Partial`/`Missing` areas that affect user-visible behavior are gaps to repair or clarify.
- If the feature touches adjacent systems, specs, or workflows, the draft must make clear what this feature expects from them and what it does not own when that distinction affects user-visible behavior or operator expectations.
- Business/domain rules, compliance constraints, security/privacy expectations, and operational constraints that materially shape user-visible behavior must be reflected explicitly when they are in scope.
- If coverage is missing because the draft is incomplete, repair the draft and review again.
- If coverage cannot be completed cleanly because the project description or steering context is ambiguous, contradictory, or underspecified, stop and ask the user to clarify instead of guessing.

## Format and Testability Review

- Every acceptance criterion must follow the format defined in `acceptance-criteria-format.md`.
- Every requirement must be testable, observable, and specific enough that later design and validation can verify it.
- Remove implementation details that belong in `design.md` rather than `requirements.md`.
- Requirement headings must use numeric IDs only; do not mix numeric and alphabetic labels.

## Structure and Quality Review

- Group related behaviors into coherent requirement areas without duplicating the same obligation across multiple sections.
- Make inclusion/exclusion boundaries explicit when the feature scope could otherwise be misread.
- Keep boundary statements lightweight and observable: describe feature responsibility and adjacent expectations without prescribing components, layers, or internal ownership.
- Ensure non-functional expectations remain user-observable or operator-observable; move technology choices and internal architecture detail out of requirements.
- Normalize vague language such as "fast", "robust", or "secure" into concrete user-visible expectations whenever the source material supports it.

## Mechanical Checks

Before applying judgment, verify these mechanically:
- **Numeric IDs present**: Every requirement heading has a numeric ID (1, 1.1, 2, etc.). Scan the draft for headings without IDs.
- **Group names**: every group heading is subject + obligation per `acceptance-criteria-format.md`; flag bare topics, vague link words (integration, linkage), `·` in names, a role that is an organization, and a role or purpose prefix repeating the spec `Definition`.
- **Acceptance criteria exist**: Every requirement group has at least one `N.M: [condition] result` line; flag any arrow (`→`, `->`, `$\rightarrow$`) between condition and result.
- **Cross-requirement analysis**: flag logical inconsistencies (individually valid, jointly impossible), conflicting constraints, unstated assumptions (undefined terms or referenced behaviors), and missing failure/boundary cases.
- **No implementation language**: Scan for technology-specific terms (database names, framework names, API patterns) that belong in design, not requirements. Flag any found.
- **Tagged findings**: every issue the gate raises carries one tag — `[Gap]` (obligation absent), `[Ambiguity]` (two readings), `[Conflict]` (criteria jointly impossible), `[Assumption]` (undefined term or unstated dependency) — and names the criterion ID or section it applies to. A finding phrased as implementation verification ("verify that the service…") is a design or test concern, not a requirements finding.

## Review Loop

- Run mechanical checks first, then judgment-based review.
- If issues are local to the draft, repair the draft and re-run the review gate.
- Keep the loop bounded: no more than 2 review-and-repair passes before escalating a real ambiguity back to the user.
- Clarification dialogue: rank open questions by impact × uncertainty, ask at most 5, exactly one at a time; offer 2–5 options with a `Recommended:` mark when the answer space is known, otherwise ask for a short answer; integrate each answer into the affected criterion before asking the next; stop when the user says done.
- Write `requirements.md` only after the review gate passes.
