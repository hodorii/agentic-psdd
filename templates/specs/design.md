# {{label.title_design}} — <feature>

## {{label.definition}}
{{label.definition_sentence}}

## {{label.boundary_commitments}}

### {{label.this_spec_owns}}
- **[responsibility area]**: [owned behavior and data, one line]

### {{label.not_owned}}
- **[non-owned area]**: [who owns it]

### {{label.allowed_dependencies}}
- External: [library + version]
- Internal direction: `a` → `b` → `c` (reverse import = design violation)

### {{label.revalidation_triggers}}
- [conditions that break this design's premises and force review — contract, ownership, dependency direction, runtime premise, scale]

## {{label.architecture}}

### {{label.boundary_map}}
[Mermaid — modules or components and dependency direction; required for complex features]

### {{label.technology_stack}}
| {{label.layer}} | {{label.tech_choice}} | {{label.role}} |
|-------|--------|------|
| | | |

### {{label.key_decisions}}
- **[decision]**: [content] — reason: [one line]. Alternatives in research.md.

## {{label.system_flows}}
[non-obvious flows only, Mermaid sequence or state; omit the section if none]
- [decision per flow — requirement ID tag (e.g., 7.2)]

## {{label.components_and_interfaces}}

### [module] — [Component]
- {{label.intent}}: [responsibility, one line]
- {{label.requirements}}: [2.1~2.5, 3.1]
```[lang]
[public signatures and types in the implementation language, error types included]
```
- [contract notes: events, state, failure modes]

## {{label.data_models}}
[domain types, persistence, invariants — say so if the interfaces above suffice]

## {{label.error_handling}}
- **{{label.user_input_error}}**: [handling + requirement ID]
- **{{label.external_resource_error}}** (file, network, permission): [isolation]
- **{{label.system_error}}** (panic, exception): [recovery or exit path]
- **{{label.graceful_degradation}}**: [fallback when a dependency fails]

## {{label.testing_strategy}}
- **{{label.test_depth}}**: [Trivial | Standard | Complex — one-line reason]
- **{{label.unit_test}}**: [key cases per module + requirement ID]
- **{{label.integration_test}}**: [boundary-crossing scenarios]
- **{{label.e2e_test}}**: [biz-process L2 flows]
- **{{label.acceptance_test}}**: [criteria met + real run]
- **{{label.performance_test}}**: [numbers when needed]

## {{label.file_structure_plan}}
```
[directory tree + responsibility notes — every component has a file path]
```

## {{label.optional_sections}}
Security / Performance / Migration
