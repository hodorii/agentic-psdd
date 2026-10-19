# tree-view-rules

> Format rules for `kiro-biz-process-tree`. Principles: SSoT (the view is derived, never a second source), SRP (view only), Lean.

## 1. Principle
- biz-process.md wins on any mismatch; the view is regenerated, never hand-patched.
- Ids are copied as written: L1~L4 ids `BP-<x>`, `BP-<x>.A<n>`, `BP-<x>.A<n>.F<n>`, `BP-<x>.A<n>.F<n>.S<n>` and `BR-<x>-<nnn>`. L5 DetailSteps carry no id; show their name as written.
- Approval state is never copied into the view; refer to `spec.json` `approvals.bizProcess` when needed.
- Old N.M.P numbering (P/A/Step/DetailStep) is not supported: convert the spec to BP-/L1~L6 first (`biz-process-rules.md` section 7).
- Wording of steps, conditions and outcomes is copied verbatim; nothing is shortened or added. No source information for a branch result -> write `?`.

## 2. Symbols
Single definition of the symbols; the view, template and SKILL.md refer here and do not repeat it (section 5 for the fence):
```output
▣  L1 Process
■  L2 Activity
□  L3 FunctionGroup/UI
●  L4 Step
▶  L5 DetailStep without a branch: its name as written
◆  decision: a BR- rule (id follows) or an L5 DetailStep with a branch (no id, its name as written); every outcome is a child
✕  rejection or stop, state unchanged
✓  success
⚠  open item (section 4)
├─ └─ │   branch lines
→ <id>     continues at another node
```
## 3. Node mapping
- One node per line (about 45 characters of text); a longer text becomes child nodes.
- A node takes its id from the source heading. The process, activity, group and step symbols are followed by the id; the decision diamond by the `BR-` id when the decision is a rule. Nothing else is written directly after those symbols that looks like an id.
- A decision lists all outcomes: no `IF` without its `ELSE` result; "nothing happens" is written as such.
- Every branch ends in a check, a cross or an arrow reference to another id.
- Between activities link by id reference; never draw the same content twice.
- An L5 DetailStep is one node: a detail triangle, or an id-less decision diamond when it branches; the text is the L5 name verbatim, outcomes are children. Trailing markers after the name (`[1.1]`, a warning symbol with text, an arrow reference) are not part of the name.
- Requirement numbers from the heading go at line end in square brackets, e.g. `[1.1, 1.2]`.
- User viewpoint (`biz-process-rules.md` section 1): detail triangles and crosses show what the user sees, e.g. a notice; never status codes, API names or "the system does".
- `Logic` rules become a decision diamond with the `BR-<x>-<nnn>` id and the condition as the line; each outcome is a check or cross child.

## 4. Document structure
Per `{{TEMPLATES}}/reference/biz-process-tree.md` (header lines per `{{TEMPLATES}}/reference/reference-convention.md`): notice, overview (L1~L4 only), then one section per L1 Process with one tree block per L2 Activity, then open items when any.
- Omit a section the source has no content for.
- Open items: only `({{label.value_chain_mapping_needed}})` marks and decisions the source states as unresolved; the index repeats id, one-line summary, source location. No new ids.

## 5. Human-Typeable exception
- The view is a derived view under the `AGENTS.md` Human-Typeable exception: tree blocks sit in a fence whose info string is `output` and keep the symbols above.
- Prose, headings and tables of the view stay plain ASCII plus the language's letters; a symbol outside an `output` fence is a `human-typeable` error.

## 6. Verification
- `doc_lint.py` rules `tree-id-missing`, `tree-id-extra`, `tree-detail-step-missing`, `tree-detail-step-extra`, `tree-source-missing` (see `{{SKILLS}}/kiro-steering/rules/doc-lint.md`) compare the view with biz-process.md: ids of L1~L4 and `BR-`, and the names of L5 DetailSteps (each appears once as a detail node or an id-less decision node); view file name is `<feature>.md`.
- Then read the blocks once: branch lines connected, the last child of each parent closes its branch.
