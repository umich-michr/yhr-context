---
title: Interested-Participant Management
summary: Workflow lists, labels, profile access, exports, and operational handling of interested participants.
status: authoritative
canonical_for:
  - interested_participant_lists
  - interested_participant_labels
  - interested_participant_profiles
relevant_when:
  - managing_interested_participants
  - moving_participants_between_lists
  - applying_participant_labels
  - viewing_interested_participant_profiles
---

# Interested-Participant Management

An interested participant is represented by one `STUDY_VOLUNTEER` row. The row is the durable
relationship used for workflow lists, labels, participant access, questionnaires, messaging, and
exports.

## Fixed workflow state

The persisted status enum is:

```text
NEW
ELIGIBLE
PENDING
INELIGIBLE
```

A successful expression of interest begins in `NEW`. `ALL` is a user-interface aggregate and query
without a status constraint; it is not a stored membership.

One row has one current status. Status movement updates both `STATUS` and
`STATUS_LAST_UPDATE_DATE`. The model does not retain prior status values, who moved the participant,
or a transition reason.

Labels are independent many-to-many tags and do not replace the status.

## Physical interested-participant schema

`STUDY_VOLUNTEER.ID` is the primary key. A unique constraint on `(USER_ID, STUDY_ID)` prevents
duplicate interest. Foreign keys connect to `APP_USER` and `STUDY` and cascade on deletion.

`STUDY_VOLUNTEER_LABEL` has the composite primary key:

```text
VOLUNTEER_LABEL_ID
STUDY_VOLUNTEER_ID
```

The label foreign key cascades when a label is deleted. The interested-participant foreign key is
restrictive at the database level; application deletion removes join rows through Hibernate before
deleting the relationship.

`VOLUNTEER_LABEL` stores `ID`, `STUDY_ID`, `NAME`, and `STYLE`. Its study foreign key is restrictive.
No database uniqueness constraint was found for label name or style within a study.

## Query and list behavior

Current list queries:

- constrain by study;
- optionally constrain by one status or one label;
- cannot combine status and label in the same application query;
- join the active quick-profile view;
- exclude inactive participant accounts;
- sort by interest date descending and relationship ID ascending;
- add applied labels; and
- calculate unread participant-to-study message counts.

Statistics likewise count only enabled participants. Participant-side interest history reads study
IDs from `STUDY_VOLUNTEER` ordered by interest date.

Current exports use the same active interested-participant query before reading full profile data from
process-local active-user memory.

## Authorization and visibility

List, profile, navigation, statistics, name-search, conversation-list, and export read paths require:

- an authenticated staff or administrator URL role;
- study membership or administrator access; and
- `PUBLISHABLE = 1` for interested-participant-specific access.

Expression of interest grants that study full profile access even when the participant's general
visibility is restricted. It does not change the participant's visibility preference or expose the
participant to unrelated studies.

Participant-data list and profile reads create PHI audit events.

## Known authorization concern: workflow and label PATCH

The interested-participant PATCH endpoint is under `/secure/staff`, so it requires a staff or
administrator role and CSRF protection. Unlike the corresponding read endpoints, it does not call
study-membership or publishability authorization. Its service accepts the study ID and relationship
ID and performs the requested status or label update.

This allows an authenticated staff account that knows IDs to attempt a status or label change outside
its study membership, and it permits mutation while the study is not publishable. Label assignment
does verify that the label and interested-participant relationship belong to the same study, but that
does not authorize the caller.

This is a current backend authorization gap and must not be documented as intended permission.

## Workflow-list operations

The current interface permits moving selected interested participants among the four fixed statuses,
including back to `NEW`. A test operation can make bulk updates conditional on the row still matching
the expected status or label.

Status movement does not alter:

- eligibility results;
- Redis recommendation exclusions;
- participant visibility;
- messaging eligibility;
- export authorization; or
- the participant's expression-of-interest timestamp.

No dedicated workflow-transition audit is created.

## Labels

Labels are study-specific shared definitions. Study members can create, rename, and delete them and
can assign multiple labels to one interested-participant row.

Deleting a label cascades its assignment rows. Deleting an interested-participant relationship through
the application removes its assignments first. Label changes are not audited.

The physical schema and current implementation establish ownership and deletion behavior. Naming
policy, maximum count, and retention remain product or institutional decisions unless enforced by
client validation.

## Deactivation, hard deletion, and retention

Participant deactivation retains the interested-participant row, answers, labels, and messages, but
active-profile list, statistics, and export queries hide the participant. Historical study-team
conversation views also depend on active-user views and become hidden.

Administrator hard deletion runs in a transaction, deletes messages before `STUDY_VOLUNTEER`, removes
label assignments, deletes the relationship, and then removes the user. Questionnaire answers also
cascade from the user foreign key.

No ordinary archive flag, withdrawal timestamp, enrollment outcome, or separate participation state
exists in `STUDY_VOLUNTEER`. The four workflow statuses are operational study-team organization, not
clinical enrollment or participation records.

Retention duration and whether deactivated relationships should remain recoverable are unresolved
institutional policy questions.

## Related pages

- [Expressions of Interest](expressions-of-interest.md)
- [Questionnaires and Exports](questionnaires-and-exports.md)
- [Messaging](messaging.md)
- [Recruitment Operations Model](../07-data-model/recruitment-operations-model.md)
- [PHI Audit](../08-operations/phi-audit.md)
