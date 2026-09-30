---
inclusion: manual
status: draft
owner: <product or business owner>
updated_at: <YYYY-MM-DD>
---
# {{label.title_value_chain}} - SSoT

## Mega ({{label.value_chain_definition}})
| id | {{label.name}} | {{label.value}} | {{label.evidence}} |
|---|---|---|---|
| VC-<domain> | <domain value chain> | <top-level customer value> | <cited source, or assumption> |

## Main ({{label.main_value_flow}})
| id | {{label.name}} | {{label.parent}} | {{label.evidence}} |
|---|---|---|---|
| VC-<domain>-<main> | <main flow> | VC-<domain> | <cited source, or assumption> |

## Unit ({{label.unit_process}})
| id | {{label.name}} | {{label.parent}} | {{label.value}} | {{label.validation}} | {{label.evidence}} | bizProcessRef |
|---|---|---|---|---|---|---|
| VC-<domain>-<unit> | <unit process name> | VC-<domain>-<main> | <value this unit delivers> | <condition the value is met> | <cited source, or assumption> | <optional BP-<name>> |

<!-- One row per item. Long text belongs in the source cited, not in the cell. bizProcessRef is optional: the BizProcess -> Unit link (valueChainRef) alone is valid. -->
