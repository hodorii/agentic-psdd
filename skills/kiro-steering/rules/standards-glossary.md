# Standards Glossary

Our terms mapped to standard terms so anyone reads them the same way. Read only the rows you need. This file carries everything an agent needs; sources and verification status live in the methodology repository's `docs/standards-research.md` (not installed into projects).

## 1. Levels

| Our level | Standard term | Primary standard | Holds |
|---|---|---|---|
| Value | the business (enterprise or business unit) | APQC PCF scope; Porter value chain (concept) | the root, one node |
| Mega | Category (PCF level 1), marked `kind: primary` or `support` | APQC PCF; Porter primary and support activities | a business area; `kind` follows Porter (directly delivers the business's value vs enables it), not PCF's operating vs management split |
| Main | Process Group (PCF level 2) | APQC PCF | a group of related processes |
| Unit | Process (PCF level 3) = biz-process L1 | APQC PCF; BPMN Process | one business process, performed by a role |
| biz-process L2 | Activity (PCF level 4) | APQC PCF; BPMN Activity | a set of steps within the process |
| biz-process L3 | Task (PCF level 5) | APQC PCF; BPMN Sub-Process | a group of business steps a role does together, named by business purpose |
| biz-process L4 | business step | BPMN Task | a step a role performs |
| biz-process L5 | business condition and branch | BPMN Gateway | conditions of a step |
| biz-process L6 | business rule or decision | DMN (decisions), SBVR (rules) | rules a business owner can approve |

## 1a. Choosing Megas
- Start from the PCF level 1 categories and keep only those where the business has evidenced processes (brief, product.md, existing biz-process). Industry PCFs (e.g., Education) come first, Cross-Industry second.
- PCF Cross-Industry 7.4 categories: 1.0 Develop Vision and Strategy; 2.0 Develop and Manage Products and Services; 3.0 Market and Sell Products and Services; 4.0 Manage Supply Chain for Physical Products; 5.0 Deliver Services; 6.0 Manage Customer Service; 7.0 Develop and Manage Human Capital; 8.0 Manage Information Technology; 9.0 Manage Financial Resources; 10.0 Acquire, Construct, and Manage Assets; 11.0 Manage Enterprise Risk, Compliance, Remediation, and Resiliency; 12.0 Manage External Relationships; 13.0 Develop and Manage Business Capabilities.
- Never invent a PCF id: take it from the PCF document, otherwise write `pcf: none` and mark `evidence: assumption`.

## 2. Other artifacts

| Our term | Standard term | Primary standard |
|---|---|---|
| system function map | Application Function, Application Service | ArchiMate 3.2 |
| common service consumed by roles | Business Service | ArchiMate 3.2 |
| capability | Capability | BIZBOK (capabilities exist before automation) |
| tasks.md item | work package in a Work Breakdown Structure | PMI Practice Standard for WBS |
| development, QA, deployment, operation, maintenance | technical processes | ISO/IEC/IEEE 12207 |
| standing IT service management | Manage Information Technology (PCF Cross-Industry 7.4, category 8.0) | APQC PCF |

## 3. Telling them apart
A value-chain node or a biz-process L1~L4 node belongs there only when all three answers are yes (L5 conditions and L6 rules use the business content test in biz-process rules instead; tasks.md items are expected to fail question 2):
1. Who: a business role performs it, or a business role directly uses it as a service (ArchiMate Business Role, Business Service). Work on the software itself is a 12207 technical process.
2. Does it end: no. It repeats with no completion date (a project is a temporary endeavor, PMBOK Guide definition; project work goes to WBS and tasks.md).
3. Does it survive without the system: yes. It would exist even if the system were rebuilt (BIZBOK: a capability exists regardless of automation). A system behavior a role uses directly goes to the system function map.
Hint: a name ending in develop, improve, migrate, verify, deploy, inspect, update or respond usually marks a work item, not a process.

## 4. Tags
- `pcf: <scope> <hierarchy id> (<element id>)`, `~` before the id when approximate, `none` when unmatched. The 5-digit element id is the stable reference; hierarchy ids change between PCF versions.
- Names stay noun phrases in the artifact's language; PCF verb-noun names are cited only through the tag.
