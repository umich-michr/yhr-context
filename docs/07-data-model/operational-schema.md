---
title: Operational Schema
summary: Logical application-managed users, studies, memberships, participants, questionnaires, and related storage.
status: mixed
relevant_when:
  - mapping_features_to_tables
  - designing_schema_changes
  - explaining_application_roles
  - explaining_study_roles
---

# Operational Schema

This page combines confirmed application concepts with suggested logical fields.

Exact physical table and column names must be verified unless a specialized authoritative schema page states otherwise.

## Role domains

Application-wide roles:

```text
ADMIN
STUDY_IMPORTER
STAFF
VOLUNTEER
```

Study-association roles:

```text
PRINCIPAL_INVESTIGATOR
STUDY_TEAM_MEMBER
```

These roles represent different authorization scopes.

## `APP_USER`

Represents an application identity.

Suggested logical fields:

```text
ID
USER_NAME
FIRST_NAME
MIDDLE_NAME
LAST_NAME
EMAIL
APPLICATION_ROLE
STATUS
CREATED_AT
LAST_LOGIN_AT
```

For institutional users:

```text
APP_USER.USER_NAME
=
SAML ePPN attribute value
```

The application refers to this value as `USER_NAME`; it does not require a separate application field named `EPPN`.

## `STUDY`

Represents an operational study posting.

Suggested logical fields:

```text
ID
STUDY_NUM
PUBLISHABLE
POSTING_ACTIVATION_DATE
POSTING_DEACTIVATION_DATE
CREATED_BY_ID
CREATED_DATE
```

Participant-facing study information is stored through the generic property-value model rather than necessarily as direct `STUDY` columns.

See [Study Property Model](study-property-model.md).

`STUDY_NUM` corresponds to `IMPORTED_STUDY.ID` and is unique within the deployment.

Active status is derived from:

```text
PUBLISHABLE = 1
AND current date is within the activation and deactivation dates
```

## `STUDY_TEAM_MEMBER`

Associates an institutional `APP_USER` with an operational study.

Suggested logical fields:

```text
ID
STUDY_ID
APP_USER_ID
STUDY_ROLE
MEMBERSHIP_SOURCE
CREATED_AT
```

Allowed study roles:

```text
PRINCIPAL_INVESTIGATOR
STUDY_TEAM_MEMBER
```

Possible membership sources include:

```text
IMPORTED_PI
POSTING_CREATOR
INVITATION
BACKEND_ADMINISTRATION
```

The exact physical membership-source values must be verified.

When the imported PI changes:

- A membership is created for the new PI.
- The former PI's existing operational membership is not automatically removed.

The table may therefore contain more than one `PRINCIPAL_INVESTIGATOR` membership even though imported data identifies one current PI.

## Participant account and profile

Participant data conceptually includes:

```text
Participant account
Participant profile
Participant preferences
Participant status
Activation token and expiration
Visibility mode
Temporal profile properties
```

The participant account uses email as its username.

Participant deletion is a support-initiated hard-deletion workflow that retains only the documented deletion marker.

## Eligibility-criteria entities

Eligibility criteria are stored through the hierarchical model:

```text
STUDY_ELIGIBILITY_CRITERION
CRITERION_CLAUSE
CRITERION_CLAUSE_EXPRESSION
CRITERION_VARIABLE
CRIT_CLAUSE_EXPRESSION_VALUE
EXPRESSION_VALUE_LOOKUP_VALUE
LOOKUP_VALUE
```

See [Criteria Data Model](criteria-data-model.md).

## Redis recommendation and exclusion data

Current participant-study recommendations and directional exclusions are stored in Redis sorted sets rather than relational application tables.

The key families are:

```text
vol.rec:<APP_USER.ID>:<MATCH_SOURCE>
std.rec:<STUDY.ID>:<MATCH_RESULT>
std.exc:<STUDY.ID>
vol.exc:<APP_USER.ID>
```

See [Redis Match and Exclusion Model](redis-match-model.md).

## Study-team prompts

An Ask if interested action must logically identify:

```text
Participant
Study
Initiating study-team user
Participant-facing message
Action timestamp
```

The exact relational representation must be verified against the physical schema.

Ask if interested is not an expression of interest.

## Participant-study interest

A finalized expression of interest must logically identify:

```text
Participant
Study
Expression timestamp
Eligibility result at interest
Associated questionnaire submission, when applicable
```

Interest is created only after:

- Eligibility recheck succeeds with `TRUE` or `MAYBE`
- The study remains active and publishable
- The questionnaire is successfully completed, when one exists

Temporal-profile updates, any questionnaire submission, and interest creation occur in one transaction.

## Questionnaire entities

A study may have zero or one questionnaire.

Conceptual entities include:

```text
QUESTIONNAIRE
QUESTION
QUESTIONNAIRE_SUBMISSION
QUESTION_RESPONSE
```

Questionnaires are not versioned.

Questions may be added, deleted, or reordered while the study is inactive.

Deleting a question after confirmation also deletes its historical responses.

See [Questionnaires and Exports](../06-recruitment/questionnaires-and-exports.md).

## Study-team invitation

An unused invitation logically contains:

```text
Study
Token
Expiration
Inviter
Creation timestamp
```

The exact physical fields must be verified.

Confirmed invitation lifecycle behavior is documented in [Study-Team Invitations](../04-users-and-access/invitations.md).

## Study-import token

A study-import token authorizes institutional CSV upload.

Its physical representation may retain only token metadata rather than the JWT itself.

Token timing is governed by:

```text
STUDY_IMPORT_TOKEN_GRACE_PERIOD
```

## CSV exports

Exports are generated in memory and streamed to the browser.

The application does not retain:

- A relational export job
- A server-side export file
- A definitive export audit event

Participant-profile views and Splunk request logs may provide indirect investigative evidence.

## Suggested constraints

The following logical constraints should correspond to implemented database constraints where applicable:

```text
UNIQUE (STUDY.STUDY_NUM)

UNIQUE (APP_USER.USER_NAME)

UNIQUE (
    STUDY_TEAM_MEMBER.STUDY_ID,
    STUDY_TEAM_MEMBER.APP_USER_ID
)

UNIQUE (QUESTIONNAIRE.STUDY_ID)
```

## Related pages

- [Imported Schema](imported-schema.md)
- [Study Property Model](study-property-model.md)
- [Criteria Data Model](criteria-data-model.md)
- [Redis Match and Exclusion Model](redis-match-model.md)
- [Relationship Model](relationship-model.md)
- [Study Membership](../04-users-and-access/study-membership.md)
- [Questionnaires and Exports](../06-recruitment/questionnaires-and-exports.md)
