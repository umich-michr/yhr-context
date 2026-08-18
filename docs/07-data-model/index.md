---
title: Data-Model Overview
summary: Routing page for governance, operational, recruitment, criteria, messaging, audit, and nonrelational data models.
status: mixed
---

# Data-Model Overview

The application's data is divided into relational, nonrelational, generated, and external-data areas.

## Imported governance data

Authoritative institutional study and personnel data is stored in:

```text
IMPORTED_STUDY
IMPORTED_STUDY_TEAM_MEMBER
IMPORTED_TEAM_MEMBER
```

See:

- [Imported Schema](imported-schema.md)
- [Imported Institutional Data](../03-institutional-governance/imported-data.md)

## Operational identity and study data

Operational application concepts include:

- Application users
- Participant accounts
- Studies
- Study memberships
- Invitations
- Study active intervals
- Study properties
- Study archiving

See:

- [Operational Schema](operational-schema.md)
- [Relationship Model](relationship-model.md)
- [Study Lifecycle](../05-study-management/study-lifecycle.md)
- [Study Archiving](../05-study-management/study-archiving.md)

## Participant accounts and consent

Participant-account relationships include:

- Self accounts
- Loved-one accounts
- Owning and represented participants
- Consent definitions
- Consent acceptance records

See:

- [Participant Account and Consent Model](participant-account-consent-model.md)
- [Participant Registration, Consent, and Loved-One Accounts](../04-users-and-access/participant-registration-consent-and-loved-ones.md)

## Study-information properties

Study Information values use the generic study-property model:

```text
ENTITY_PROPERTY
STUDY_PROPERTY_VALUE
STUDY_PROP_VAL_LOOKUP_VAL
LOOKUP_VALUE
```

See:

- [Study Property Model](study-property-model.md)
- [Study Property Query Cookbook](study-property-query-cookbook.md)
- [Study Information Authoring](../05-study-management/study-information-authoring.md)

## Eligibility and study-interest criteria

The shared criteria model includes:

```text
STUDY_ELIGIBILITY_CRITERION
FIND_STUDIES_CRITERION
CRITERION_CLAUSE
CRITERION_CLAUSE_EXPRESSION
CRITERION_VARIABLE
CRIT_CLAUSE_EXPRESSION_VALUE
EXPRESSION_VALUE_LOOKUP_VALUE
LOOKUP_VALUE
```

See:

- [Criteria Data Model](criteria-data-model.md)
- [Criterion Variable Reference](criterion-variable-reference.md)
- [Criterion Operator and Value Reference](criterion-operator-reference.md)
- [Criteria Query Cookbook](criteria-query-cookbook.md)

## Redis recommendations and exclusions

Current participant-study recommendations and directional exclusions are stored in Redis sorted sets.

See:

- [Redis Match and Exclusion Model](redis-match-model.md)
- [Matching and Visibility](../06-recruitment/matching-and-visibility.md)

## Interested-participant operations

Recruitment operations include:

- `STUDY_VOLUNTEER` interested-participant relationships
- Workflow-list membership
- Study-specific labels
- Shared conversations
- Message templates and attachments
- Study notification configuration
- Study active intervals

See:

- [Recruitment Operations Model](recruitment-operations-model.md)
- [Interested-Participant Management](../06-recruitment/interested-participant-management.md)
- [Messaging](../06-recruitment/messaging.md)
- [Study Notifications](../05-study-management/study-notifications.md)

## Questionnaires

Questionnaire concepts include:

- Questionnaire
- Question
- Response option
- Questionnaire submission
- Question response

See:

- [Operational Schema](operational-schema.md)
- [Questionnaires and Exports](../06-recruitment/questionnaires-and-exports.md)

## Participant-data auditing

Participant list and profile views are audited through:

```text
PHI_AUDIT
```

See:

- [PHI Audit](../08-operations/phi-audit.md)
- [Audit and Monitoring](../08-operations/audit-and-monitoring.md)

## Study-posting authoring audit and telemetry

Study-posting authoring analysis uses:

```text
STUDY_POSTING_AUDIT
STUDY_POSTING_GENERATION_AUDIT
Application logs
Splunk-derived telemetry
```

See:

- [AI-Assisted Study Posting Authoring](../05-study-management/ai-assisted-posting-authoring.md)
- [Study Posting Authoring Telemetry](../08-operations/study-posting-authoring-telemetry.md)
- [Eligibility-Criteria Authoring Complexity](../08-operations/eligibility-criteria-authoring-complexity.md)
- [AI-Assisted Study Posting Authoring Effectiveness](../08-operations/ai-assisted-study-posting-authoring-effectiveness.md)

## Generated CSV output

CSV exports are generated in memory and streamed to the browser.

They are not retained as relational export jobs or server-side files.

See [Questionnaires and Exports](../06-recruitment/questionnaires-and-exports.md).

## Cross-domain relationships

See [Relationship Model](relationship-model.md).
