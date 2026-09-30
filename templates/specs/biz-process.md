# {{label.title_biz_process}} — <feature>

## {{label.definition}}
{{label.definition_sentence}}

## {{label.value_chain_mapping}}
| L1 Process | Unit Process (valueChainRef) | {{label.value}} | {{label.related_requirements}} |
|------------|------------------------------|------|---------------|
| BP-<x>     | VC-...-<unit>                | <value> | 1.1, 2.3 |

## L1 Process: <name>  (valueChainRef: VC-...-<unit>)
### L2 Activity: <name>  (1.1)
  ### L3 FunctionGroup/UI: <name>  (1.1, 1.2)
    ### L4 Step: <name>
      ### L5 DetailStep: <name>
        Logic(AST):
          - IF <cond> THEN <action>
          - ELSE THROW <error>
      ### L5 DetailStep: ...
    ### L4 Step: ...
### L2 Activity: ...
### ✅ {{label.review_request}} (L1: <name>)
승인(✓) 또는 수정 사항을 입력하세요.

## L1 Process: <name2>  (valueChainRef: VC-...-<unit2>)
... (동일 구조 반복)
### ✅ {{label.review_request}} (L1: <name2>)

