# Review Edition Rules

> Optional. For a spec whose design is read by reviewers outside the implementation team and needs a separate text. A spec without an edition follows `design-principles.md` alone.

## Relation
- design.md is the original; an edition is a derived view of it (the `AGENTS.md` derived-view term), never a second source.
- On any mismatch design.md wins; fix the original first, then bring the edition along.
- Allowed in an edition: leave a decision out, word a decision differently, restructure and shorten.
- Not allowed: a decision absent from design.md, a value that differs from design.md.

## Declaration
- An edition is a Markdown file in the same spec directory that carries one line, outside code fences: `<!-- derived-from: design.md; omitted: D15, D17 -->`
- `derived-from` names the original file in the same directory (a bare file name, no path); `omitted` lists the decision ids the edition leaves out (drop `; omitted: ...` when none).
- The declaration is the only way a file counts as an edition; file names carry no meaning. `omitted` entries are separated by commas or spaces; one declaration per file, the first counts.

## Decision ids
- A decision is identified by an id `D<n>` that opens a list item (bulleted or numbered) or the first cell of a table row (bold allowed), e.g. `- **D3 [decision]**: ...` or `| D3 | ... |`.
- The edition keeps the original's ids; it never renumbers or reuses a number for another decision.
- A reference to an id inside running text, including a trailing citation `(D3)`, is not a definition and is not checked.
- Ids are numbered within one design, never reused or renumbered.
- An edition drops the citations of the ids it omits.

## Verification
- `doc_lint.py` rules `edition-source-missing`, `edition-decision-extra`, `edition-omission-undeclared`, `edition-omission-invalid` (see `{{SKILLS}}/kiro-steering/rules/doc-lint.md`): the ids of the edition are a subset of the original's, and every id of the original absent from the edition is in `omitted`.
- Values and wording are not checked; compare them by reading before the edition goes out.
