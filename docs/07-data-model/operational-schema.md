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

This page is the compact physical-storage map for operational identities, studies, recruitment,
questionnaires, messaging, and audit evidence.

## Identity and access

```text
APP_USER
DB_USER_AUTH_DETAIL
USER_ROLE
VOLUNTEER_PROFILE
CONTACT_INFO
LOVED_ONE
STUDY_TEAM_MEMBER
STUDY_TEAM_INVITATION
```

See [Participant Account and Consent Model](participant-account-consent-model.md) and
[Study Membership](../04-users-and-access/study-membership.md).

## Studies and lifecycle

```text
STUDY
STUDY_ACTIVE_INTERVAL
STUDY_PROPERTY_VALUE
ENTITY_PROPERTY
```

Active matching membership is derived through `V_ACTIVE_STUDY`. Archive and enrollment values use the
study-property model.

## Eligibility and recommendations

Eligibility and participant interests use the criterion tables. Current recommendations and
exclusions use Redis keys documented in the Redis model; Redis is not the authoritative
interested-participant store.

## Interested participants

```text
STUDY_VOLUNTEER
STUDY_VOLUNTEER_LABEL
VOLUNTEER_LABEL
```

`STUDY_VOLUNTEER` has:

- sequence primary key `ID`;
- foreign keys to `APP_USER` and `STUDY`;
- unique `(USER_ID, STUDY_ID)`;
- interest and status timestamps; and
- one current status: `NEW`, `ELIGIBLE`, `PENDING`, or `INELIGIBLE`.

`STUDY_VOLUNTEER_LABEL` is the composite-key assignment table.

See [Recruitment Operations Model](recruitment-operations-model.md).

## Questionnaires

```text
STUDY_SCREEN_QNAIRE
STUDY_SCREENING_QUESTION
STUDY_SCR_QUES_OPTION
VOL_SCR_QUESTION_ANSWER
VOL_QSTN_ANSWR_SLCTD_OPTNS
```

`STUDY_SCREEN_QNAIRE.VERSION` provides optimistic-concurrency state, not historical versions.
Question and option ordering are physical columns.

User-defined answers contain user, study, question, answer date, and either free text or selected
options. Fixed profile-backed questions persist through participant profile-property tables instead.

No database unique constraint on questionnaire `STUDY_ID` or historical definition snapshot was found.

## Messaging

```text
USER_MESSAGE
MESSAGE_ATTACHMENT
ATTACHMENT
MESSAGE_TEMPLATE
MESSAGE_TEMPLATE_ATTACHMENT
V_CONVERSATION_FOR_STUDY_TEAM
V_CONVERSATION_FOR_VOLUNTEER
```

A conversation is derived from messages sharing `STUDY_VOLUNTEER_ID`; no conversation table exists.
`USER_MESSAGE` stores sender, body, timestamp, shared `READ` or `UNREAD` status, and the
interested-participant relationship.

Attachment metadata is relational. File bytes are external filesystem state. Message and template
join rows cascade when an attachment is deleted.

## Generated exports

Interested-participant CSV is generated from:

- active interested-participant query results;
- the handling process's active-user store;
- current questionnaire definitions and answer rows; and
- current labels and workflow status.

The response is streamed to the browser. No relational export job, retained server-side CSV, or
definitive export audit event is created.

## PHI and application audit

```text
PHI_AUDIT
APPLICATION_ERROR
LOGIN_AUDIT
USER_AGREEMENT_AUDIT
EMAIL_LOG
```

Interested-participant list and profile reads create PHI audit evidence. Recruitment workflow changes,
labels, questionnaire definition history, message reads, and exports do not have complete dedicated
audit records established by the reviewed paths.

## Deletion and retention boundaries

Foreign-key cascades remove many dependent rows on account, study, question, option, label, message,
or attachment deletion. Restrictive message and relationship foreign keys require explicit
application deletion ordering.

Participant deactivation is not deletion. Active-profile queries hide the participant while durable
interest, answer, and message rows remain.

The schema does not encode institutional retention periods. Filesystem attachment retention and
orphan reconciliation are also operational concerns outside relational constraints.

## Email attempt log

`EMAIL_LOG` stores selected direct-client success or failure evidence after recipient rewriting. It
does not prove mailbox delivery, and successful JMS queue submissions are not logged there.

See [Audit and Monitoring](../08-operations/audit-and-monitoring.md).

## Related pages

- [Data-Model Overview](index.md)
- [Recruitment Operations Model](recruitment-operations-model.md)
- [Questionnaires and Exports](../06-recruitment/questionnaires-and-exports.md)
- [Messaging](../06-recruitment/messaging.md)
