# {{label.title_biz_process}} - <feature>

## {{label.definition}}
{{label.definition_sentence}}

## {{label.value_chain_mapping}}
| L1 Process | Unit (valueChainRef) | {{label.related_requirements}} |
|------------|----------------------|---------------|
| BP-<x>     | VC-...-<unit>        | 1.1, 2.3 |

## L1 Process: <name>  (BP-<x>; valueChainRef: VC-...-<unit>)
### L2 Activity: <name>  (BP-<x>.A1; 1.1)
#### L3 FunctionGroup/UI: <name>  (BP-<x>.A1.F1; 1.1, 1.2)
##### L4 Step: <name>  (BP-<x>.A1.F1.S1)
###### L5 DetailStep: <name>
        Logic (business rules):
          - BR-<x>-001: IF <business condition> THEN <business outcome>
          - BR-<x>-002: <rule statement a business owner can approve>
###### L5 DetailStep: ...
##### L4 Step: ...  (BP-<x>.A1.F1.S2)
### L2 Activity: ...  (BP-<x>.A2)
### {{label.review_request}} (L1: <name>)
{{label.review_prompt}}

## L1 Process: <name2>  (valueChainRef: VC-...-<unit2>)
... (repeat the same structure)
### {{label.review_request}} (L1: <name2>)

