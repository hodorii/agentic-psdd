# BizProcess - sample

## Value chain mapping
| L1 Process | Unit (valueChainRef) | Requirements |
|---|---|---|
| BP-molding | VC-plant-production-making-molding | 1.1 |

## L1 Process: Molding  (BP-molding; valueChainRef: VC-plant-production-making-molding)
### L2 Activity: Mold  (BP-molding.A1; 1.1)
##### L4 Step: Set pressure  (BP-molding.A1.F1.S1)
###### L5 DetailStep: Read the pressure gauge
###### L5 DetailStep: Check resin moisture
        Logic (business rules):
          - BR-molding-001: IF the resin is wet THEN dry it first
