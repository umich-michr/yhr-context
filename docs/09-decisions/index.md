---
title: Decision Register
summary: Separates confirmed behavior from unresolved product, telemetry, and technical decisions.
status: authoritative
---

# Decision Register

The documentation uses these status categories:

| Status | Meaning |
|---|---|
| Authoritative | Confirmed current behavior or business rule |
| Recommended | Proposed implementation, security, or operational guidance |
| Open | Requires product, institutional, legal, security, or technical confirmation |
| Mixed | Contains both confirmed concepts and proposed schema details |

Before answering a question about behavior not explicitly documented as authoritative, consult [Open questions](open-questions.md).

For AI-assisted authoring and analytics questions, consult [Authoring analytics open questions](authoring-analytics-open-questions.md).

When an open question is resolved:

1. Record the decision.
2. Update the canonical topic page.
3. Update the business rules if the decision is cross-cutting.
4. Remove or mark the question resolved.
5. Regenerate `llms.txt` from `context-map.yaml` if routing changes.
