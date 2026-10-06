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

## Labels, notifications, promotion, and deactivation

### Recruitment labels

`VOLUNTEER_LABEL` has sequence primary key `ID`, restrictive `STUDY_ID`, `NAME`, and `STYLE`. No database uniqueness constraint was found for name or style within a study. `STUDY_VOLUNTEER_LABEL` is a composite-key join of `VOLUNTEER_LABEL_ID` and `STUDY_VOLUNTEER_ID`. Label deletion cascades assignment rows; the interested-participant foreign key is restrictive. One interested participant can hold multiple labels.

### Study notification configuration

`NOTIFICATION_SETTING_FREQ` has a composite primary key of `NOTIFICATION_FREQUENCY_LV_ID` and `NOTIFICATION_SETTING_LV_ID`. Both are restrictive lookup foreign keys, and `ORDER_NUM` controls presentation.

`STUDY_NOTIFICATION_SETTING` has sequence primary key `ID`, `STUDY_ID`, notification-event lookup, nullable frequency lookup, and `RECIPIENT_EMAILS`. A unique constraint on `(STUDY_ID, NOTIFICATION_SETTING_LV_ID)` enforces one setting per study and event. The nullable frequency accommodates events such as Other Announcements that have no selectable frequency.

`STUDY_NOTIFICATION_RECIPIENT` is the composite join of `STUDY_NOTIFICATION_SETTING_ID` and `STUDY_TEAM_MEMBER_ID`. Membership deletion cascades recipient joins; the setting-side foreign key is restrictive. External recipients remain a string on the setting instead of normalized recipient rows.

### Promotion

`RECOMMENDED_STUDY_MESSAGE` has sequence primary key `ID`, participant `USER_ID`, `STUDY_ID`, recommending `FROM_USER_ID`, `MESSAGE` with physical maximum length 512, and `REASON`. Known reasons include `ASKED_IF_INTERESTED` and `RECOMMENDED_ANOTHER_STUDY`. All three foreign keys are restrictive.

The table has no promotion-event timestamp, current-state marker, uniqueness constraint on participant-study-reason, Redis score, or durable email-attempt link. Multiple rows can physically exist for one participant-study pair.

### User deactivation

`USER_DEACTIVATION` has sequence primary key `ID`, nullable `USER_ID`, `DEACTIVATION_DATE`, and a deactivation-reason lookup. Unique `USER_ID` establishes at most one current deactivation row per retained user reference. Deleting `APP_USER` sets the reference to null and preserves the deactivation row. Reactivation deletes the row.

Reason availability and display vary by institution. Shared semantic reasons include `CHILD_TURNED_ADULT`, `DECLINED_USER_AGREEMENT`, `NOT_ENTERED`, and `PARENT_DEACTIVATED`. Deployment-specific numeric lookup IDs are not universal.

`CHILD_DEACTIVATION_NOTICE` has sequence primary key `ID`, parent and child account foreign keys, `CHILD_DOB_AT_TIME_OF_NOTICE`, and `SENT_DATE`. Both account foreign keys cascade on account deletion. The application deduplicates by parent, child, and recorded date of birth, so correcting the date of birth can permit another notice.

Warning email is handed off before the notice row is saved. A subsequent transaction failure can therefore produce delivery without committed deduplication evidence. Warning and age-out deactivation are separate records and actions.

### Study deactivation

Study deactivation updates posting dates and `STUDY_ACTIVE_INTERVAL`; it is not represented by `USER_DEACTIVATION`. Participant visibility, matched-participant behavior, asynchronous Redis cleanup, later daily notification, and archival each follow their own application paths.

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
