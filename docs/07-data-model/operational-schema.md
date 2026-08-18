---
title: Operational Schema
summary: Routing page for operational identities, studies, participants, recruitment relationships, questionnaires, and audit storage.
status: mixed
relevant_when:
  - mapping_features_to_tables
  - designing_schema_changes
  - locating_operational_entities
---

# Operational Schema

This page provides a compact map of operational storage.

Use the specialized schema pages for field-level detail.

## Identity and access

Operational identity and authorization include:

```text
APP_USER
UMCS_USER
STUDY_TEAM_MEMBER
STUDY_TEAM_INVITATION
LOVED_ONE
```

For institutional identities:

```text
APP_USER.USER_NAME
=
SAML ePPN attribute value
```

See:

- [Institutional Users](../04-users-and-access/institutional-users.md)
- [Study Membership](../04-users-and-access/study-membership.md)
- [Participant Account and Consent Model](participant-account-consent-model.md)

## Studies and lifecycle

Study data includes:

```text
STUDY
STUDY_ACTIVE_INTERVAL
STUDY_PROPERTY_VALUE
ENTITY_PROPERTY
```

Active status is derived from publishability and activation boundaries.

Archive state and total enrollment are stored through study properties.

See:

- [Study Lifecycle](../05-study-management/study-lifecycle.md)
- [Study Archiving](../05-study-management/study-archiving.md)
- [Study Property Model](study-property-model.md)

## Criteria

Eligibility and participant study interests use:

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

See [Criteria Data Model](criteria-data-model.md).

## Recommendations

Current recommendations and exclusions are stored in Redis:

```text
vol.rec
std.rec
vol.exc
std.exc
```

See [Redis Match and Exclusion Model](redis-match-model.md).

## Expressions of interest

Successful show-interest processing creates:

```text
STUDY_VOLUNTEER
```

The relationship supports:

- Workflow-list membership
- Questionnaire submission
- Labels
- Messaging
- Export

See [Recruitment Operations Model](recruitment-operations-model.md).

## Questionnaires

A study may have zero or one questionnaire.

Questionnaire storage includes concepts such as:

```text
Questionnaire
Question
Response option
Questionnaire submission
Question response
```

Exact physical names remain to be documented.

See [Questionnaires and Exports](../06-recruitment/questionnaires-and-exports.md).

## Messaging and notifications

Messaging storage includes:

- Messages
- Study-specific templates
- Stored attachments
- Message attachments

Notification storage includes:

- Study
- Event
- Shared frequency
- Study-member recipients
- External recipients

Exact physical table names remain to be documented.

See:

- [Messaging](../06-recruitment/messaging.md)
- [Study Notifications](../05-study-management/study-notifications.md)
- [Recruitment Operations Model](recruitment-operations-model.md)

## Consent

Consent uses:

```text
USER_AGREEMENT
USER_AGREEMENT_AUDIT
```

See [Participant Account and Consent Model](participant-account-consent-model.md).

## PHI audit

Participant-data access uses:

```text
PHI_AUDIT
```

See [PHI Audit](../08-operations/phi-audit.md).

## Study-posting authoring telemetry

Study-posting attempts and optional AI generation use:

```text
APPLICATION_SETTING
STUDY_POSTING_AUDIT
STUDY_POSTING_GENERATION_AUDIT
STUDY_POSTING_GENERATION_AUDIT_ERROR
```

See [Study-Posting Authoring Audit Model](study-posting-authoring-audit-model.md).

## Generated exports

CSV exports are streamed to the browser.

The application does not retain:

- Relational export jobs
- Server-side export files
- Definitive export audit events

## Related pages

- [Relationship Model](relationship-model.md)
- [Data-Model Overview](index.md)
