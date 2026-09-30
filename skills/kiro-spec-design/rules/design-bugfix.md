# Design for Bugfix Specs

Applies when `bugfix.md` exists instead of `requirements.md`. Skip discovery/synthesis unless the fix crosses a boundary. ~60 lines cap.

Sections
- `Definition`
- `## {{label.root_cause}}` (Root Cause): the defect path at file/function level, tied to `1.x`; evidence from reproduction.
- `## {{label.fix_approach}}` (Fix Approach): minimal change; rejected alternative in one line.
- `## {{label.verification_properties}}` (Verification Properties): three named tests — (a) defect reproduces before the fix (`1.x` fails), (b) expected behavior after the fix (`2.x` passes), (c) unchanged behavior holds before and after (`3.x` passes), stated as a property over inputs outside the defect condition when that input space is broad (`verification-mapping.md` §4).
- `## {{label.impact_scope}}` (Impact Scope): files touched; confirm no Boundary Commitment of the owning spec is violated.
