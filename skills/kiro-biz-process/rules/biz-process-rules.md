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
- L1 Process id is `BP-<meaningful-name>` (Descriptable); one L1 Process per value-chain Unit (Unit = PCF Process = biz-process L1).
- `valueChainRef` matches a `value-chain.md` Unit id exactly (case included); find it with `grep -n "^ *- <id> "`.
- Nothing from the value chain is copied (names aside): link only.
- Two-way check (recommended): Unit id as `valueChainRef` in biz-process, `bizProcessRef` tag in value-chain.
- `value-chain.md` is the product or business owner's SSoT: this skill never edits it. Without `bizProcessRef` the link is valid one-way (`valueChainRef` only); ask the owner to add it.

## 4. V-model left side (progressive unfold)
- BizProcess drill-down = V-model **left side**. Verification (right side) is not recorded in biz-process.md.
- Verification level mapping: `kiro-spec-design/rules/verification-mapping.md` (L1~L6 <-> test level <-> Depth). `design.md` Testing Strategy applies it; consuming skills (verify-completion, validate-impl, impl) follow that Testing Strategy.
- Levels: Process -> Activity -> FunctionGroup/UI -> Step -> DetailStep -> Logic (business rules). L4~L6 expose business procedure and business rules, never implementation.

## 4a. Business content test (L4~L6)
- Write each node so a business owner can read and approve it without knowing the code, and so it survives a rebuild of the system.
- L4 Step: a business step a role performs. L5 DetailStep: its business conditions and branches. L6 Logic: business rules and decisions as rule statements or decision tables (standards: DMN, SBVR; see `{{SKILLS}}/kiro-steering/rules/standards-glossary.md`).
- Not here: API calls, function, table or variable names, internal processing order. Those belong to design.md; work items belong to tasks.md.

## 4b. Numbering
- L1 `BP-<x>`, L2 `BP-<x>.A<n>`, L3 `BP-<x>.A<n>.F<n>`, L4 `BP-<x>.A<n>.F<n>.S<n>`; L5 is named under its L4; L6 rules carry `BR-<x>-<nn>`.
- Numbers run in order within the parent, new nodes are appended, existing numbers never change, retired numbers are not reused.

## 5. Drill-down notation
- Levels as heading depth per `{{TEMPLATES}}/specs/biz-process.md` (L1 `##` to L5 `######`), each L1~L4 heading carrying its id; L6 rules indented under their DetailStep, one `BR-` id per rule.
- Each **L1 Process** closes with an approval gate (`### Review Request (L1: <name>)`). Non-interactive (`-y`): full drill-down, then one gate for all.
- L2/L3 blocks carry related requirement IDs for traceability to `requirements.md` (also in the mapping table).

## 6. Approval gate (informed consent)
- Ask for user review right after each L1 Process: understanding-based consent, not a rubber stamp.
- `-y`: full drill-down, then a single gate for all levels (requirements and value chain approved beforehand).

## 7. Value chain status
- Missing: `$kiro-steering` Bootstrap drafts it from `{{TEMPLATES}}/steering/value-chain.md`.
- `status: draft`: present it to the owner for approval; never approve it or proceed on it.
- `status: approved`, or no `status` at all (a file from before drafts existed): read-only SSoT; suggest the owner add `status: approved`. `bizProcessRef` is optional; the BizProcess -> Unit link (`valueChainRef`) alone is valid. A table-format value chain from an earlier template stays readable; suggest converting it to the tree template.
