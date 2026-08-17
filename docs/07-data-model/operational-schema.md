---
title: Operational Schema
summary: Logical application-managed users, studies, memberships, participants, matches, and questionnaires.
status: mixed
relevant_when:
  - mapping_features_to_tables
  - designing_schema_changes
  - explaining_application_roles
  - explaining_study_roles
---

# Operational Schema

This page combines confirmed application concepts with suggested logical fields.

Exact table and column names must be verified against the physical database schema.

## Role domains

The application uses two distinct role domains.

### Application-wide roles

```text
ADMIN
STUDY_IMPORTER
STAFF
VOLUNTEER
```

### Study-association roles

```text
PRINCIPAL_INVESTIGATOR
STUDY_TEAM_MEMBER
```

These roles must not be stored or interpreted as though they represent the same authorization scope.

## `APP_USER`

Represents an application identity.

Suggested fields:

```text
ID
USER_NAME
EPPN
FIRST_NAME
MIDDLE_NAME
LAST_NAME
EMAIL
APPLICATION_ROLE
STATUS
CREATED_AT
LAST_LOGIN_AT
```

Possible application-wide roles:

```text
ADMIN
STUDY_IMPORTER
STAFF
VOLUNTEER
```

Institutional users are managed through institutional identity providers.

## `STUDY`

Represents an operational study posting.

Suggested fields:

```text
ID
STUDY_NUM
TITLE
DESCRIPTION
PUBLISHABLE
ACTIVATION_DATE
DEACTIVATION_DATE
CREATED_BY
CREATED_AT
```

`STUDY_NUM` must:

- Correspond to `IMPORTED_STUDY.ID`
- Be unique within the institutional deployment

Conceptually:

```text
UNIQUE (STUDY.STUDY_NUM)
```

Study active status is derived from:

```text
PUBLISHABLE = 1
AND current date is within activation and deactivation dates
```

## `STUDY_TEAM_MEMBER`

Associates an institutional `APP_USER` with an operational study.

Suggested fields:

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

Possible membership sources:

```text
IMPORTED_PI
POSTING_CREATOR
INVITATION
BACKEND_ADMINISTRATION
```

A uniqueness rule should prevent duplicate user-study memberships unless the physical model intentionally permits separate rows for separate roles.

Conceptually:

```text
UNIQUE (
    STUDY_TEAM_MEMBER.STUDY_ID,
    STUDY_TEAM_MEMBER.APP_USER_ID
)
```

## PI-change implication

When the imported PI changes:

- A membership is created for the new PI.
- The former PI's existing operational membership is not automatically removed.

The operational table may therefore contain more than one `PRINCIPAL_INVESTIGATOR` membership even though imported data identifies one current PI.

## `PARTICIPANT_ACCOUNT`

Represents a local participant account.

Suggested fields:

```text
ID
EMAIL
PASSWORD_DATA
APPLICATION_ROLE
ACCOUNT_STATUS
ACTIVATION_TOKEN
ACTIVATION_TOKEN_EXPIRES_AT
CREATED_AT
DEACTIVATED_AT
```

Participant application role:

```text
VOLUNTEER
```

Participant deletion is a hard deletion initiated through the support-request process.

## `PARTICIPANT_PROFILE`

Suggested fields or profile areas:

```text
PARTICIPANT_ID
DATE_OF_BIRTH
GENDER
RACE
LOCATION
CONTACT_INFORMATION
VISIBILITY_MODE
PAST_MEDICAL_CONDITIONS
PRESENT_MEDICAL_CONDITIONS
PARENT_GUARDIAN_OF_CHILD_UNDER_18
UPDATED_AT
```

The actual model may normalize repeating profile properties into separate tables.

## `PARTICIPANT_PREFERENCE`

Represents participant study interests.

Suggested fields:

```text
ID
PARTICIPANT_ID
PREFERENCE_TYPE
PREFERENCE_VALUE
UPDATED_AT
```

Examples include:

- Topic
- Location
- Compensation preference
- Other study characteristics

## `ELIGIBILITY_CRITERION`

Represents a study inclusion or exclusion criterion.

Suggested fields:

```text
ID
STUDY_ID
PROFILE_PROPERTY
OPERATOR
EXPECTED_VALUE
CRITERION_TYPE
GROUP_ID
DISPLAY_ORDER
```

Eligibility criteria may require additional tables for grouped Boolean expressions.

## `MATCH_EVALUATION`

Represents a participant-study match result.

Suggested fields:

```text
ID
PARTICIPANT_ID
STUDY_ID
INTEREST_RESULT
ELIGIBILITY_RESULT
MATCH_CATEGORY
EVALUATED_AT
```

Eligibility results:

```text
TRUE
MAYBE
FALSE
```

Match categories:

```text
EXACT
PARTIAL
NO_MATCH
```

Match results are stored in Redis and recalculated asynchronously after a
relevant profile, preference, study-property, or eligibility-criteria change.
Failed recalculations are not retried automatically; operators can manually
trigger full study, participant, or combined recomputation jobs.

## `STUDY_TEAM_PROMPT`

Represents an Ask if interested action.

Suggested fields:

```text
ID
PARTICIPANT_ID
STUDY_ID
INITIATED_BY_APP_USER_ID
MESSAGE
CREATED_AT
DISPLAYED_AT
VIEWED_AT
RESPONDED_AT
STATUS
```

A prompt is not an expression of interest.

## `PARTICIPANT_STUDY_INTEREST`

Represents a finalized expression of interest.

Suggested fields:

```text
ID
PARTICIPANT_ID
STUDY_ID
EXPRESSED_AT
ELIGIBILITY_RESULT_AT_INTEREST
STATUS
```

Participants cannot currently withdraw a finalized interest.

The row is created only after successful questionnaire completion. The
temporal-profile update, questionnaire submission, and interest creation occur
in one transaction.

## `QUESTIONNAIRE`

Represents the single screening questionnaire for a study.

Suggested fields:

```text
ID
STUDY_ID
ACTIVE
CREATED_AT
UPDATED_AT
```

Conceptually:

```text
UNIQUE (QUESTIONNAIRE.STUDY_ID)
```

Questionnaires are not versioned.

## `QUESTION`

Represents a screening question.

Suggested fields:

```text
ID
QUESTIONNAIRE_ID
QUESTION_TEXT
REQUIRED
DISPLAY_ORDER
```

Questions may be added, deleted, or reordered while the study is inactive.
Other changes to existing question content are not supported. Deleting a
question also deletes its historical responses after confirmation.

## `QUESTIONNAIRE_SUBMISSION`

Represents a submitted screening questionnaire.

Suggested fields:

```text
ID
QUESTIONNAIRE_ID
PARTICIPANT_STUDY_INTEREST_ID
SUBMITTED_AT
```

Submitted questionnaires cannot be edited by participants.

## `QUESTION_RESPONSE`

Represents one answer.

Suggested fields:

```text
ID
QUESTIONNAIRE_SUBMISSION_ID
QUESTION_ID
RESPONSE_VALUE
```

Because questionnaires are not versioned and questions may be deleted, the handling of historical responses to deleted questions must be verified.

## `STUDY_TEAM_INVITATION`

Represents an unused invitation token.

Suggested fields:

```text
ID
STUDY_ID
TOKEN
EXPIRES_AT
CREATED_BY_APP_USER_ID
CREATED_AT
```

Confirmed behavior includes:

- Cryptographically secure UUID v4 token
- Expiration
- Revocation by invitation-record deletion
- Invitation-record deletion after successful membership creation
- Atomic membership creation and invitation-record deletion
- Transferable acceptance by any SAML-authenticated institutional user with the link

## `STUDY_IMPORT_TOKEN`

Represents authorization for institutional CSV upload.

Suggested fields:

```text
ID
STUDY_IMPORTER_APP_USER_ID
TOKEN_IDENTIFIER
EXPIRES_AT
CREATED_AT
```

Token timing is governed by:

```text
STUDY_IMPORT_TOKEN_GRACE_PERIOD
```

The physical implementation may store only token-related metadata rather than the JWT itself.

## CSV exports

Exports are generated in memory and streamed to the browser. No `EXPORT_JOB`
or server-side export file is retained, and the export action is not separately
audited. Participant-profile views are audited and can be correlated with
Splunk request logs for support investigation.

## Suggested constraints

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

- [Imported schema](imported-schema.md)
- [Study membership](../04-users-and-access/study-membership.md)
- [Matching and visibility](../06-recruitment/matching-and-visibility.md)
- [Open questions](../09-decisions/open-questions.md)