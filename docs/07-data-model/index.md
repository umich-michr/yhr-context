---
title: Data-Model Overview
summary: Routing page for imported, operational, criteria, questionnaire, audit, and nonrelational data models.
status: mixed
---

# Data-Model Overview

The application's data is divided into relational, nonrelational, generated, and external-data areas.

## Imported governance tables

- `IMPORTED_STUDY`
- `IMPORTED_STUDY_TEAM_MEMBER`
- `IMPORTED_TEAM_MEMBER`

See [Imported Schema](imported-schema.md).

## Operational identities and studies

- `APP_USER`
- `STUDY`
- `STUDY_TEAM_MEMBER`
- `STUDY_TEAM_INVITATION`

See [Operational Schema](operational-schema.md).

## Participant and recruitment data

Conceptual areas include:

- Participant account
- Participant profile
- Participant preferences
- Study-team prompts
- Participant-study interests

See:

- [Operational Schema](operational-schema.md)
- [Relationship Model](relationship-model.md)

## Study-information properties

- `ENTITY_PROPERTY`
- `STUDY_PROPERTY_VALUE`
- `STUDY_PROP_VAL_LOOKUP_VAL`
- `LOOKUP_VALUE`

See [Study Property Model](study-property-model.md).

## Criteria data

- `STUDY_ELIGIBILITY_CRITERION`
- `FIND_STUDIES_CRITERION`
- `CRITERION_CLAUSE`
- `CRITERION_CLAUSE_EXPRESSION`
- `CRITERION_VARIABLE`
- `CRIT_CLAUSE_EXPRESSION_VALUE`
- `EXPRESSION_VALUE_LOOKUP_VALUE`

See:

- [Criteria Data Model](criteria-data-model.md)
- [Criteria Query Cookbook](criteria-query-cookbook.md)

## Criterion reference data and encoding

- `CRITERION_VARIABLE` defines the available generic criterion-variable vocabulary.
- The current UI maps supported controls to relational operators and scalar or lookup values.
- Historical data may contain combinations produced by the legacy UI.

See:

- [Criterion Variable Reference](criterion-variable-reference.md)
- [Criterion Operator and Value Reference](criterion-operator-reference.md)

## Questionnaires

Conceptual entities include:

- Questionnaire
- Question
- Questionnaire submission
- Question response

See:

- [Operational Schema](operational-schema.md)
- [Questionnaires and Exports](../06-recruitment/questionnaires-and-exports.md)

## Authoring audit and telemetry data

- `STUDY_POSTING_AUDIT`
- `STUDY_POSTING_GENERATION_AUDIT`
- Application log events
- Splunk-derived telemetry

See:

- [AI-Assisted Study Posting Authoring](../05-study-management/ai-assisted-posting-authoring.md)
- [Study Posting Authoring Telemetry](../08-operations/study-posting-authoring-telemetry.md)
- [Eligibility-Criteria Authoring Complexity](../08-operations/ai-assisted-study-posting-authoring-effectiveness.md)
- [AI-Assisted Study Posting Authoring Effectiveness](../08-operations/ai-assisted-study-posting-authoring-effectiveness.md)

## Nonrelational match data

Current match results are stored in Redis.

Redis match data is derived from relational application data and asynchronously recalculated.

The exact Redis key and value schema is not documented on this page.

See [Matching and Visibility](../06-recruitment/matching-and-visibility.md).

## Generated CSV output

CSV exports are generated in memory and streamed to the browser.

They are not persisted as relational export entities or retained server-side files.

See [Questionnaires and Exports](../06-recruitment/questionnaires-and-exports.md).

## Cross-domain relationship map

See [Relationship Model](relationship-model.md).

## Redis recommendations and exclusions

Current participant-study recommendations and directional exclusions are stored in Redis sorted sets.

See [Redis Match and Exclusion Model](redis-match-model.md).
