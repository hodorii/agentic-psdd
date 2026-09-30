# verification-mapping

V-model right side: test level and pass criteria per biz-process level (L1~L6). `kiro-spec-design` applies it when writing Testing Strategy.

## 1. Level <-> test level <-> pass criteria

| L-level | biz-process level | Test level | Pass criteria |
|---|---|---|---|
| L1 | Process | Acceptance | every requirements.md criterion met + runnable artifacts run for real |
| L2 | Activity | E2E | user scenario flow succeeds |
| L3 | FunctionGroup/UI | Integration (UI-API) | screen-to-API wiring succeeds, failure paths included |
| L4 | Step | Integration (API) | single API or service boundary contract met |
| L5 | DetailStep | Integration (Service) | internal service collaboration behaves |
| L6 | Logic (AST) | Unit | function or method logic correct |

Tools and frameworks: steering `tech.md`. Volume: Unit most, Acceptance least.

## 2. Depth: never force every level

| Depth | When | Required levels |
|---|---|---|
| Trivial | simple CRUD, configuration | Unit + Acceptance smoke |
| Standard | new logic, multiple screens | Unit ~ E2E |
| Complex | domain rules, integration, state machines | all levels (Unit ~ Acceptance) |

Judge Depth from requirements.md; state it on the first line of Testing Strategy.

## 3. Regression
- A lower-level change rechecks its level and the levels above (e.g., L6 Logic change -> Unit, plus the L5/L4 Integration that calls it).

## 4. Properties (code deliverables)
- Derive a property from each `[{{label.always}}]` criterion, each criterion over an input range or class, and each bugfix `3.x` unchanged behavior with a broad input space.
- Record in Testing Strategy: `P<n>: <statement> - <requirement IDs> - <input domain>`.
- Each property gets a property-based test (generator over the domain, shrinking on failure); library from steering `tech.md`.
- A failing property reports its shrunk counterexample; decide with the user whether the implementation, the test or the requirement is wrong. Never weaken a property silently.
- Non-code deliverables: N/A.
