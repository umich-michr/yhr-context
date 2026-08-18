---
title: Relationship Model
summary: High-level relationships among imported governance, operational studies, users, participants, criteria, and audit data.
status: mixed
relevant_when:
  - mapping_entity_relationships
  - understanding_study_centric_data
  - tracing_participant_study_links
---

# Relationship Model

This page provides a high-level map.

Detailed physical fields belong in the specialized schema pages.

## Core relational relationships

```mermaid
erDiagram
    IMPORTED_STUDY ||--o| STUDY : governs

    IMPORTED_STUDY ||--o{ IMPORTED_STUDY_TEAM_MEMBER : has
    IMPORTED_TEAM_MEMBER ||--o{ IMPORTED_STUDY_TEAM_MEMBER : assigned_to
    IMPORTED_TEAM_MEMBER }o--o| APP_USER : resolves_to

    STUDY ||--o{ STUDY_TEAM_MEMBER : authorizes
    APP_USER ||--o{ STUDY_TEAM_MEMBER : receives

    STUDY ||--o{ STUDY_TEAM_INVITATION : has
    APP_USER ||--o{ STUDY_TEAM_INVITATION : creates

    STUDY ||--o{ STUDY_PROPERTY_VALUE : has
    ENTITY_PROPERTY ||--o{ STUDY_PROPERTY_VALUE : defines
    STUDY_PROPERTY_VALUE ||--o{ STUDY_PROP_VAL_LOOKUP_VAL : selects
    LOOKUP_VALUE ||--o{ STUDY_PROP_VAL_LOOKUP_VAL : referenced_by

    STUDY ||--o{ STUDY_ELIGIBILITY_CRITERION : defines
    STUDY_ELIGIBILITY_CRITERION -.-> CRITERION_CLAUSE : application_parent
    CRITERION_CLAUSE ||--o{ CRITERION_CLAUSE_EXPRESSION : contains
    CRITERION_VARIABLE ||--o{ CRITERION_CLAUSE_EXPRESSION : classifies

    PARTICIPANT_ACCOUNT ||--|| PARTICIPANT_PROFILE : has
    PARTICIPANT_ACCOUNT ||--o{ PARTICIPANT_PREFERENCE : defines
    PARTICIPANT_ACCOUNT ||--o{ PARTICIPANT_STUDY_INTEREST : expresses
    STUDY ||--o{ PARTICIPANT_STUDY_INTEREST : receives

    STUDY ||--o| QUESTIONNAIRE : may_have
    QUESTIONNAIRE ||--o{ QUESTION : contains
    PARTICIPANT_STUDY_INTEREST ||--o| QUESTIONNAIRE_SUBMISSION : finalized_with
    QUESTIONNAIRE_SUBMISSION ||--o{ QUESTION_RESPONSE : contains

    STUDY ||--o{ STUDY_POSTING_AUDIT : records
    STUDY_POSTING_AUDIT ||--o{ STUDY_POSTING_GENERATION_AUDIT : may_have
```

The dotted criterion relationship is application-managed because `CRITERION_CLAUSE.CRITERION_ID` may also reference `FIND_STUDIES_CRITERION`.

## Nonrelational recommendation and exclusion data

Current participant-study recommendations and directional match exclusions are stored in Redis sorted sets.

The four key families are:

```text
vol.rec:<APP_USER.ID>:<MATCH_SOURCE>
std.rec:<STUDY.ID>:<MATCH_RESULT>
std.exc:<STUDY.ID>
vol.exc:<APP_USER.ID>
```

Redis data is derived from relational application data but is not represented as a relational entity in the diagram above.

See [Redis Match and Exclusion Model](redis-match-model.md) for the authoritative key and member structures.

## Imported-to-operational flow

Imported governance data determines:

- Whether a study may have a posting
- Current publishability
- The current institutional PI

Operational data stores:

- Participant-facing posting content
- Study memberships
- Eligibility criteria
- Participant relationships
- Questionnaires
- Authoring audit records

## Historical relationships

A `PARTICIPANT_STUDY_INTEREST` may remain after:

- Participant deactivation
- Study date-based inactivity
- Study non-publishability
- Later eligibility changes

Retention of the relationship does not always imply current access to participant data.

## Canonical detail pages

- [Imported Schema](imported-schema.md)
- [Operational Schema](operational-schema.md)
- [Study Property Model](study-property-model.md)
- [Criteria Data Model](criteria-data-model.md)
- [AI-Assisted Study Posting Authoring](../05-study-management/ai-assisted-posting-authoring.md)
- [Matching and Visibility](../06-recruitment/matching-and-visibility.md)
- [Redis Match and Exclusion Model](redis-match-model.md)
