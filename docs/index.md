---
title: YourHealthResearch.org Application Context
summary: Main routing page for functional, technical, support, data-model, and analytics documentation.
status: authoritative
---

# YourHealthResearch.org Application Context

YourHealthResearch.org facilitates recruitment for human-subject research studies.

## Quick routing

| Topic | Canonical page |
|---|---|
| Application overview | [Application Overview](01-overview/index.md) |
| Terms and definitions | [Terminology](01-overview/terminology.md) |
| Cross-cutting rules | [Business Rules](01-overview/business-rules.md) |
| System integrations and boundaries | [System Context](02-architecture/system-context.md) |
| Institutional governance | [Institutional Governance](03-institutional-governance/index.md) |
| Participant accounts and profiles | [Participants](04-users-and-access/participants.md) |
| Signup, consent, and loved-one accounts | [Participant Registration](04-users-and-access/participant-registration-consent-and-loved-ones.md) |
| Institutional roles and study access | [Study Membership](04-users-and-access/study-membership.md) |
| Creating a study posting | [Posting Creation](05-study-management/posting-creation.md) |
| Study Information fields | [Study Information Authoring](05-study-management/study-information-authoring.md) |
| AI-assisted posting authoring | [AI-Assisted Study Posting Authoring](05-study-management/ai-assisted-posting-authoring.md) |
| Study activation and deactivation | [Study Lifecycle](05-study-management/study-lifecycle.md) |
| Study archiving | [Study Archiving](05-study-management/study-archiving.md) |
| Study email notifications | [Study Notifications](05-study-management/study-notifications.md) |
| Public study search and details | [Public Study Discovery](06-recruitment/public-study-discovery.md) |
| Eligibility authoring | [Eligibility-Criteria Authoring](06-recruitment/eligibility-criteria-authoring.md) |
| Matching and visibility | [Matching and Visibility](06-recruitment/matching-and-visibility.md) |
| Ask if interested | [Ask if Interested](06-recruitment/ask-if-interested.md) |
| Show-interest transaction | [Expressions of Interest](06-recruitment/expressions-of-interest.md) |
| Questionnaires and exports | [Questionnaires and Exports](06-recruitment/questionnaires-and-exports.md) |
| Interested-participant lists and labels | [Interested-Participant Management](06-recruitment/interested-participant-management.md) |
| Participant messaging | [Messaging](06-recruitment/messaging.md) |
| Data models | [Data-Model Overview](07-data-model/index.md) |
| Redis recommendations | [Redis Match and Exclusion Model](07-data-model/redis-match-model.md) |
| Recruitment operations data | [Recruitment Operations Model](07-data-model/recruitment-operations-model.md) |
| Participant-data audit | [PHI Audit](08-operations/phi-audit.md) |
| Support questions | [Support Routing](08-operations/support-routing.md) |
| Troubleshooting | [Troubleshooting](08-operations/troubleshooting.md) |
| Study-posting authoring analytics | [Study Posting Authoring Analytics](08-operations/study-posting-authoring-analytics.md) |
| Unresolved behavior | [Open Questions](09-decisions/open-questions.md) |

## LLM routing

Repository-aware assistants should begin with:

```text
docs/context-map.yaml
```

The generated website also exposes:

```text
/llms.txt
```

The routing map identifies canonical and related pages so narrow questions do not require loading the complete documentation set.

## Documentation authority

| Status | Meaning |
|---|---|
| `authoritative` | Confirmed current behavior |
| `recommended` | Proposed control or improvement |
| `mixed` | Confirmed context plus clearly identified proposals |
| `open` | Unresolved behavior |

Recommended, proposed, and unresolved content must not be presented as implemented behavior.
