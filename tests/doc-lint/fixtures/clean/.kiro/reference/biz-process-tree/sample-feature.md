# BizProcess Tree View - sample-feature

Read-only view of biz-process.md; the source wins on any mismatch.

```output
▣ BP-molding Molding
├─ ■ BP-molding.A1 Mold  [1.1]
│  └─ ● BP-molding.A1.F1.S1 Set pressure
│     ├─ ▶ Read the pressure gauge  [1.1]
│     ├─ ◆ Check resin moisture  ⚠ open
│     │  ├─ ✓ dry
│     │  └─ ✕ wet
│     └─ ◆ BR-molding-001 IF the resin is wet
│        ├─ ✓ dry it first
│        └─ ✓ start molding
```
