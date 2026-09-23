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

An interested participant is represented by a participant-study relationship in `STUDY_VOLUNTEER`.

## Initial state

A successful expression of interest creates the relationship in:

```text
NEW
```

## Fixed workflow lists

The fixed workflow lists are:

```text
NEW
ELIGIBLE
INELIGIBLE
PENDING
```

`ALL` is an aggregate view and is not a workflow-list membership.

## List membership

- One interested-participant relationship belongs to one workflow list at a time.
- Any associated study team member may move the participant.
- A participant may be returned to `NEW`.
- A participant cannot be moved to the list they already occupy.

List movement does not change:

- Eligibility matching
- Redis exclusions
- Messaging permission
- Export permission
- Participant profile visibility

Moving to `INELIGIBLE` does not create a Redis exclusion.

## Restricted-visibility participants

Successful expression of interest makes the participant available to the applicable study team
through the Interested Participants workflow even when the participant selected restricted
visibility.

In this case:

- The participant appears in the applicable study's Interested Participants list.
- Authorized members of that study team may access the participant profile information available
  through the interested-participant workflow.
- The participant's restricted visibility preference remains in effect for pre-interest matching by
  other studies.
- The expression of interest does not make the participant visible to unrelated study teams.

This access results from the participant's interest relationship with the applicable study, not from
changing the participant's visibility preference.

## Profile access

Selecting an interested participant displays:

- Participant profile information
- Demographic and health information
- Screening questions and answers
- Workflow list
- Applied labels
- Messaging controls

Profile visibility still depends on:

- Participant account status
- Study publishability
- Study membership or administrative access

## Labels

Study team members may create study-specific labels.

Rules:

- Labels are shared by the study team.
- A participant may have multiple labels.
- Labels may be renamed.
- Labels may be deleted.
- Deleting a label removes its participant assignments.
- Labels are independent of workflow-list membership.
- Labels are included in CSV exports.
- Label changes are not audited.

## Messaging

A study team member may initiate messaging from the interested-participant profile.

See [Messaging](messaging.md).

## Audit behavior

Workflow-list movement is not audited.

Participant-data viewing is audited through `PHI_AUDIT`.

See [PHI Audit](../08-operations/phi-audit.md).

## Related pages

- [Expressions of Interest](expressions-of-interest.md)
- [Messaging](messaging.md)
- [Questionnaires and Exports](questionnaires-and-exports.md)
- [Recruitment Operations Model](../07-data-model/recruitment-operations-model.md)
