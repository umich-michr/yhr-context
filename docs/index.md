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
| Criterion operators and stored values | [Criterion operator reference](07-data-model/criterion-operator-reference.md) |
| Participant matching and visibility | [Matching and visibility](06-recruitment/matching-and-visibility.md) |
| Ask if interested | [Ask if interested](06-recruitment/ask-if-interested.md) |
| Participant interest and screening | [Expressions of interest](06-recruitment/expressions-of-interest.md) |
| Database entities | [Data model](07-data-model/index.md) |
| Study-property values | [Study property model](07-data-model/study-property-model.md) |
| Eligibility criteria storage | [Criteria data model](07-data-model/criteria-data-model.md) |
| Criteria SQL and validation checks | [Criteria query cookbook](07-data-model/criteria-query-cookbook.md) |
| AI-assisted study-posting authoring effectiveness  | [Authoring analytics](08-operations/study-posting-authoring-analytics.md) |
| Study-posting authoring telemetry and timing cleaning | [Study-posting authoring telemetry](08-operations/study-posting-authoring-telemetry.md) |
| Eligibility complexity scoring | [Eligibility complexity analysis](08-operations/ai-assisted-study-posting-authoring-effectiveness.md) |
| AI effectiveness methodology | [AI effectiveness analysis](08-operations/ai-assisted-study-posting-authoring-effectiveness.md) |
| Troubleshooting | [Support routing](08-operations/support-routing.md) |
| Behavior not yet decided | [Open questions](09-decisions/open-questions.md) |
| Study-posting authoring and analytics questions | [Study-posting authoring and analytics open questions](09-decisions/study-posting-authoring-analytics-open-questions.md) |

## LLM usage

An LLM should begin with [`llms.txt`](llms.txt), which is generated from [`context-map.yaml`](context-map.yaml) during the MkDocs build, and load only the pages relevant to the question.

Machine-readable routing is available in [`context-map.yaml`](context-map.yaml).

## Documentation authority

This documentation uses four status categories:

1. **Authoritative** — confirmed current behavior or business rules.
2. **Recommended** — proposed implementation, security, analytics, or operational guidance.
3. **Open** — unresolved behavior requiring confirmation.
4. **Mixed** — a page containing both confirmed context and proposed schema or analytical details.

An LLM must not present recommended, mixed-page proposals, or unresolved behavior as implemented functionality.

When using a page marked `mixed`, the LLM must distinguish statements labeled as current behavior from suggested or proposed content.
