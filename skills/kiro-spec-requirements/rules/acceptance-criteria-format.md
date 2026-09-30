# Acceptance Criteria Format

One criterion per line under a numbered requirement group, inside the `Requirements` section:

```
### N. [subject + obligation]
- N.M: [condition] result
```

- Group name: subject + obligation — what the deliverable must provide (`Process variable definition`, `Prediction accuracy calculation method`). A bare topic (`Command draft`, `Evidence`) or a vague link word (`integration`, `linkage`) is not a name.
- Prefix `[role] … so that [purpose]` only when the group's beneficiary or purpose differs from the spec `Definition`, or when the name is otherwise indistinguishable from another group. A role is a user of the deliverable (steering `product.md` roles), never a participating organization; organizations belong in `Adjacent expectations`.
- `[condition]`: the triggering event, state, failure, or option; `[{{label.always}}]` for invariants; combine with `+`.
- `[result]`: what is observable — rendered output, exit code, file state, message. No implementation terms (framework, module, table).
- No arrow: the closing `]` separates condition from result. One behavior per line. Measurable words (`within 2 s`), never "fast" / "robust".

Examples
- `1.3: [root lookup fails] error with the searched paths on stderr, non-zero exit`
- `7.6: [watching unavailable] status bar shows 'watch unavailable', r refreshes manually`
- `8.1: [always] creates, modifies or deletes no file under the watched directory`
