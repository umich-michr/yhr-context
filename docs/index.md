---
title: YourHealthResearch.org Application Context
summary: Main routing page for the application context.
status: authoritative
---

# YourHealthResearch.org Application Context

YourHealthResearch.org facilitates recruitment of participants for human-subject research studies.

This documentation describes:

- Participant accounts, profiles, preferences, and visibility
- Institutional authentication and study authorization
- Study posting creation and lifecycle
- AI-assisted study-posting authoring
- Eligibility-criteria authoring
- Institutionally governed PI assignments
- Institutionally derived publishability
- Participant-study matching
- Expressions of interest and screening questionnaires
- Data exports
- Imported and operational data models
- Study-property and criteria data models
- Authoring telemetry and complexity analysis
- Multi-institution deployment
- Support and troubleshooting

## Quick routing

| If you need to understand... | Read |
|---|---|
| The application at a high level | [Application overview](01-overview/index.md) |
| Canonical definitions | [Terminology](01-overview/terminology.md) |
| Confirmed cross-cutting rules | [Business rules](01-overview/business-rules.md) |
| System integrations | [System context](02-architecture/system-context.md) |
| Separate institutional deployments | [Multi-institution deployment](02-architecture/multi-institution-deployment.md) |
| eResearch, CSV imports, or governance data | [Institutional governance](03-institutional-governance/index.md) |
| Whether a study may recruit | [Publishability](03-institutional-governance/publishability.md) |
| PI and study-team authorization | [Study membership](04-users-and-access/study-membership.md) |
| Creating a study posting | [Posting creation](05-study-management/posting-creation.md) |
| AI-assisted study-posting authoring | [AI-assisted authoring](05-study-management/ai-assisted-posting-authoring.md) |
| Eligibility-criteria authoring | [Eligibility-criteria authoring](06-recruitment/eligibility-criteria-authoring.md) |
| Participant matching and visibility | [Matching and visibility](06-recruitment/matching-and-visibility.md) |
| Ask if interested | [Ask if interested](06-recruitment/ask-if-interested.md) |
| Participant interest and screening | [Expressions of interest](06-recruitment/expressions-of-interest.md) |
| Database entities | [Data model](07-data-model/index.md) |
| Study-property values | [Study property model](07-data-model/study-property-model.md) |
| Eligibility criteria storage | [Criteria data model](07-data-model/criteria-data-model.md) |
| Authoring telemetry and complexity | [Authoring telemetry](08-operations/authoring-telemetry-and-complexity.md) |
| Troubleshooting | [Support routing](08-operations/support-routing.md) |
| Behavior not yet decided | [Open questions](09-decisions/open-questions.md) |
| AI-assisted authoring questions | [Authoring analytics open questions](09-decisions/authoring-analytics-open-questions.md) |

## LLM usage

An LLM should begin with [`llms.txt`](llms.txt), which is generated from [`context-map.yaml`](context-map.yaml) during the MkDocs build, and load only the pages relevant to the question.

Machine-readable routing is available in [`context-map.yaml`](context-map.yaml).

## Documentation authority

This documentation separates three categories:

1. **Confirmed behavior** — current business rules.
2. **Recommended design** — proposed implementation or security guidance.
3. **Open questions** — behavior requiring confirmation.

An LLM must not present recommended or unresolved behavior as an existing feature.
