---
inclusion: manual
status: draft
owner: <product or business owner>
updated_at: <YYYY-MM-DD>
---
# {{label.title_value_chain}} — SSoT

## Mega ({{label.value_chain_definition}})
- id: VC-<domain>
- name: <domain value chain>
- value: <top-level customer value>
- evidence: <cited source | assumption>

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
- evidence: <cited source | assumption>
- bizProcessRef: BP-<meaningful-name>   # optional: two-way link to the BizProcess
