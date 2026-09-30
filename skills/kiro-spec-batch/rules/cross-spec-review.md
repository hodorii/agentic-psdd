# Cross-Spec Review

Runs after every spec of the batch has spec.json and requirements.md. Reads all of them plus `{{STEERING}}/roadmap.md`.

## Checks
- **[Duplicate]**: the same obligation in two specs. Keep it in the spec the roadmap assigns; the other references it in `Adjacent expectations`.
- **[Overlap]**: two specs' `In scope` claim the same responsibility.
- **[Unmet]**: spec A's `Adjacent expectations` needs X from spec B, and no criterion in B produces X.
- **[Order]**: a spec depends on output of a spec later in the roadmap dependency order.
- **[Term]**: one concept under different names, or a cross-spec ID reference that does not exist.
- **[Definition]**: a shared data item or indicator defined in more than one spec instead of one owner.

## Loop
- Each finding names the tag, both specs and the criterion IDs.
- Repair inside the specs (move, reference, rename); keep IDs contiguous per the requirements rules; re-run the checks. At most 3 rounds.
- A finding that needs a different decomposition (split, merge, reorder specs) -> stop and route to `$kiro-discovery`; do not patch it in requirements.
- CROSS_SPEC_REVIEW = findings per round and their resolution, or `CLEAN`.
