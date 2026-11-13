# Common Principles
Hold for all work: code, documents, guidance, agent roles, what goes into context. Single source - other files reference these names and do not restate them.

- **SSoT**: one fact (constant, setting, type, schema, rule, template, path, document) is defined in one place; everything else references it. A duplicate found -> merge it and replace the copy with a reference.
- **SRP**: a function, class, module, file, document or role has one responsibility. Two reasons to change, or a description that needs "and" -> split.
  - **Small Units**: size limits (function, class, file) are set by the project; over the limit = split signal, keeping it needs a stated reason.
- **Self-Documenting**: understandable without comments.
  - **Descriptable Name** (Descriptable Naming): a name states what the thing is; a name that needs a comment is the wrong name. No vague names (`data`, `tmp`, `handle`, `mgr`). Booleans start with `is`, `has` or `should`; functions with a verb.
  - **Why-Only Comment**: no comments by default (minimal comments); one line only for a WHY the code cannot show - explain why, never what or how. No requirement or task IDs, no history - tracing is git and the project's traceability records. Public API doc comments, license headers and generated code are exempt.
- **Lean**: write only what is needed; drop a line if the reader decides the same without it. No repetition, no prose retelling of a table or figure, no filler. Do not shorten where the meaning changes.
  - Guidance, specs and artifacts: core first, detail below; no "Conclusion:" label and no summary line that repeats the body; one example. Structure (numbering, sections, tables) only when it carries information.
  - Reports and requests: result and request first (두괄식), then evidence and detail. To the user: complete sentences, no arrow chains or abbreviations.
- **Keep the existing system**: where a system already exists (artifact, schema, procedure, tool), use it first. A proposal that adds or replaces one states why the existing cannot serve - in the deliverable itself, not only in the reply - and a replacement states its migration path.
- **Guidance vs history**: guidance and rule documents hold forward rules in the present tense and decision criteria only. Who decided what, when and why, discarded options and verification records live elsewhere: decision records, specs, git.
- **MoE**: split work into independent experts (module, document, agent, role, skill), each with its own rules and material, engaged only when its domain applies. Experts meet through artifacts, not each other's internals. An artifact carries no instructions; the criteria for judging it belong to the expert that judges.
  - Match the model to the grade of the work: default low, raise only for work that needs judgment. The delegating side sets the grade.
- **Lazy Loading**: keep the always-loaded surface (context, startup, imports) minimal - what every task needs, plus pointers. Load the rest when needed, at the narrowest grain (the row or section, not the file). Tiers: 0 always; 1 picked from a map by the task; 2 when its expert is engaged; 3 by explicit path only. Every item states its tier; an unplaced item is not tier 0. This file is tier 0.
