# biz-process-rules

> Writing and format rules for `kiro-biz-process`. Principles: SSoT, SRP, Descriptable Name; output language per `AGENTS.md` Labels.

## 1. User perspective
- Subject is always a **user or role** (customer, administrator, new member); the system is never the subject.
- Verbs are user actions: enters, checks, selects.
- System responses are written as what the user sees or receives, not "the system does".
- Screen and UX terms use units the user perceives (screen, button, notification).

## 2. BPMN flow
- **Sequence**: step-by-step progress
- **Gateway**: branch on a condition (IF/ELSE, ERROR)
- **Parallel**: independent units in parallel
- **Event**: timeout, external callback, exception

## 3. Value chain links (SSoT)
- L1 Process id is `BP-<meaningful-name>` (Descriptable).
- `valueChainRef` matches a `value-chain.md` Unit id exactly (case included).
- A Unit's `value` and `validation` are never copied; link only.
- Two-way check (recommended): Unit id as `valueChainRef` in biz-process, `bizProcessRef` in value-chain.
- `value-chain.md` is the product or business owner's SSoT: this skill never edits it. Without `bizProcessRef` the link is valid one-way (`valueChainRef` only); ask the owner to add it.

## 4. V-model left side (progressive unfold)
- BizProcess drill-down = V-model **left side**. Verification (right side) is not recorded in biz-process.md.
- Verification level mapping: `kiro-spec-design/rules/verification-mapping.md` (L1~L6 ↔ test level ↔ Depth). `design.md` Testing Strategy applies it; consuming skills (verify-completion, validate-impl, impl) follow that Testing Strategy.
- Levels: Process → Activity → FunctionGroup/UI → Step → DetailStep → Logic(AST)

## 5. Drill-down notation
- Levels as heading depth per `{{TEMPLATES}}/specs/biz-process.md` (L1 `##` to L5 `######`); L6 Logic as indented pseudo-code under its DetailStep.
- Each **L1 Process** closes with an approval gate (`### ✅ Review Request`). Non-interactive (`-y`): full drill-down, then one gate for all.
- L2/L3 blocks carry related requirement IDs for traceability to `requirements.md` (also in the mapping table).

## 6. Approval gate (informed consent)
- Ask for user review right after each L1 Process: understanding-based consent, not a rubber stamp.
- `-y`: auto-approve every level (requirements and value chain approved beforehand).

## 7. Bootstrap (value-chain.md)
Without `value-chain.md`, propose this minimum skeleton to the product or business owner and ask them to create it; this skill never creates it.

```markdown
# {{label.title_value_chain}} — SSoT

## Mega ({{label.value_chain_definition}})
- id: VC-<domain>
- name: <domain value chain>
- value: <top-level customer value>

## Main ({{label.main_value_flow}})
- id: VC-<domain>-<main>
- name: <main flow>
- parent: VC-<domain>

## Unit ({{label.unit_process}})
- id: VC-<domain>-<unit>
- name: <unit process name>
- parent: VC-<domain>-<main>
- value: <value this unit delivers>
- validation: <condition the value is met>
- bizProcessRef: BP-<meaningful-name>   # optional: two-way link to the BizProcess
```

`bizProcessRef` is optional; the BizProcess → Unit link (`valueChainRef`) alone is valid.
