# Discovery Paths

| Path | When | Writes | Next |
|---|---|---|---|
| A. Existing spec | the whole request fits one existing spec's Scope | nothing new; note the target spec | `$kiro-spec-requirements <spec>` (requirement change) or `$kiro-bugfix <fix>` (defect) |
| B. No spec | config change, rename, trivial addition, defect with no regression risk | nothing | direct implementation; `$kiro-bugfix` when a regression is possible |
| C. New single spec | no overlap with existing specs, one domain, about 20 tasks or fewer expected | `{{SPECS}}/<feature>/brief.md` | `$kiro-spec-init <feature>` or `$kiro-spec-quick <feature>` |
| D. Multi-spec | several domains, or more than about 20 tasks expected | `{{SPECS}}/discovery/brief.md` (initiative) + `{{STEERING}}/roadmap.md` (`inclusion: manual`) | `$kiro-spec-batch` |
| E. Mixed | extends existing specs + at least one new spec (+ direct items) | as D, roadmap adds `Existing Spec Updates` and `Direct Implementation Candidates` | `$kiro-spec-batch` for new specs, `$kiro-spec-requirements` per updated spec |

## Classification
- Scan metadata first: existing `{{SPECS}}/*/spec.json`, their Scope sections, steering. Overlap with an existing Scope -> A or E.
- Count domains and expected tasks; state the deciding fact with PATH_DETECTED (e.g., `D: 5 deliverables across 3 work packages`).
- Between two paths, take the one with fewer new specs and say why.
- Ask one boundary question at a time; offer 2-3 approaches with a recommendation.
- Write the files, report the path and next command, then stop; never run the next skill.
