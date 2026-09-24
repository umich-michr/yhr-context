---
title: Troubleshooting
summary: Causes and checks for common participant, study, matching, interest, messaging, questionnaire, notification, and export problems.
status: authoritative
---

# Troubleshooting

## Participant activation failed

Check:

- Was the applicable consent accepted?
- Was an activation email sent?
- Does the activation token exist?
- Has it expired?
- Was the account already activated?
- Was registration for self or a loved one?
- Was the selected loved-one relationship consistent with date of birth?

## Loved-one account is inaccessible

Check:

- Is the parent account active?
- Is the loved-one account active?
- Does a `LOVED_ONE` relationship connect the accounts?
- Is the owner using the correct participant context?
- Did a child account automatically deactivate after turning 18?

## Posting cannot be created

Check:

- Does the entered `study_num` exist in `IMPORTED_STUDY`?
- Does an operational posting already exist?
- Does the imported study have one current PI?
- Does the PI have email and `USER_NAME`?
- Does imported `USER_NAME` match the SAML ePPN value?
- Did import or reconciliation fail?

## Study cannot be activated

Check:

- Is `PUBLISHABLE = 1`?
- Is required posting content complete?
- Is a valid future deactivation date supplied?
- Is the study archived?
- Is the user associated with the study?

A study cannot be activated while archived or non-publishable.

## Study became inactive

Possible causes:

- Manual deactivation set the deactivation date to today
- The deactivation date passed
- `PUBLISHABLE` changed to `0`

Inspect:

- Posting activation date
- Posting deactivation date
- Publishability
- `STUDY_ACTIVE_INTERVAL`
- Reconciliation and notification records

## Study became active automatically

Imported automatic reactivation occurs when:

- Imported `PUBLISHABLE` changes from `0` to `1`
- Reconciliation resets the posting activation date to the current time
- The retained posting deactivation date still permits active membership

If the retained deactivation date has passed, the resulting range cannot remain matching-active.
Inspect reconciliation logs, the updated activation date, the retained deactivation date, and
`V_ACTIVE_STUDY` membership.

## Study cannot be archived

Check:

- Is the study inactive?
- Is it already archived?
- Does the archived-date property already have a value?

An active study must be deactivated before it can be archived.

## Public study cannot be found

Check:

- Does the posting exist?
- Is the study active?
- Is `PUBLISHABLE = 1`?
- Does the date range include today?
- Is the study archived?
- Does the search filter exclude the study?
- Are the relevant study properties populated?

## Participant is missing from study recommendations

Check:

- Is the participant active?
- Is the study active?
- Is eligibility exact or partial?
- Is the participant hidden by restricted visibility?
- Does `std.exc:<STUDY.ID>` contain the participant?
- Does the expected `std.rec` key contain the participant?
- Did asynchronous recomputation complete?

A participant may exist in Redis and still be hidden by visibility rules.

## Study is missing from My Studies

Check:

- Is the participant active?
- Is the study active?
- Is eligibility exact?
- Does the study match participant interests?
- Did the participant select Not Interested?
- Does `vol.exc:<APP_USER.ID>` contain the study?
- Does `vol.rec:<APP_USER.ID>:SYSTEM` contain the study?
- Did recomputation complete?

Partial matches are not shown in ordinary participant-facing recommendations.

## Show interest failed

Check:

- Is the participant active?
- Is the study still active?
- Has the participant already expressed interest?
- Were all required screening questions answered?
- What eligibility result was produced after temporal profile updates?
- Did any part of the transaction fail?

A `FALSE` result prevents interest.

Any transaction failure rolls back:

- Profile updates
- Questionnaire answers
- `STUDY_VOLUNTEER` creation

## Participant cannot message the study

Check:

- Has the participant successfully expressed interest?
- Has a study team member initiated the conversation?
- Is the participant account active?
- Is `PUBLISHABLE = 1`?

Participants cannot initiate the first message.

## Study team cannot message a participant

Check:

- Is the participant interested rather than merely matched?
- Is the participant account active?
- Is `PUBLISHABLE = 1`?
- Does the user have study membership?
- Is the message attachment 5 MB or less?

Study teams cannot message matched participants before interest.

## Existing conversation is hidden

Check:

- Did `PUBLISHABLE` become `0`?
- Was the participant account deactivated?
- Does the user still have study membership?

Date-based inactivity alone does not hide an existing conversation.

## Attachment cannot be sent

Check:

- Is the file larger than 5 MB?
- Is the participant interested?
- Does a conversation exist or is the study team initiating it?
- Is participant and study access currently permitted?

File type is not restricted by the application.

## Interested participant is on the wrong list

Check:

- Which fixed workflow list is assigned?
- Did a study member move the participant?
- Is the user viewing a label list rather than a workflow list?
- Is the user viewing `ALL`?

One interested participant belongs to one fixed workflow list at a time.

## Label disappeared

Check:

- Was the label deleted?
- Was it renamed?
- Was the participant assignment removed?
- Is the user viewing the correct study?

Deleting a label removes all assignments for that label.

## Questionnaire cannot be edited

Check:

- Is the study active?
- Is the editor using stale questionnaire data?
- Did another study member save first?

The study must be inactive.

A stale submission is rejected and requires refresh.

## Questionnaire answers disappeared

Possible causes:

- A question was deleted
- A response option was deleted

Deleting one response option removes only answers selecting that option.

Deleting a question removes all answers for that question.

## Notification email was not sent

Check:

- Is the event configured?
- Is the recipient selected?
- Is the invitee an accepted study member?
- Was the membership removed?
- Is the configured frequency immediate, daily, or weekly?
- Is the address an external recipient?
- Did email delivery fail?

External addresses are not validated by the application.

## Export is unavailable

Check:

- Is `PUBLISHABLE = 1`?
- Is the participant account active?
- Does the user have study access?
- Is the participant an interested participant?
- Is participant information currently visible?

A date-inactive but publishable study may export historical interested-participant data.

A non-publishable study cannot.

## Participant-data access investigation

Use `PHI_AUDIT` to investigate:

- Administrator search results
- Matched-participant list views
- Interested-participant list views
- Matched profile views
- Interested profile views

Workflow-list movement, label changes, and exports are not separately audited.

## Suspected stale in-memory state

Active stores are process-local. Scheduled synchronization adds newly active
entities and removes inactive entities, but it does not refresh complete data
for entities that remain active.

When one server appears stale:

- Confirm which application server processed the update.
- Confirm that the local entity update hook completed.
- Compare the database record with that server's in-memory entity.
- Check matching application errors.
- Trigger the supported entity rematch or store-repair operation when
  appropriate.
- Do not assume another server received an ordinary profile or study-property
  update immediately.

## Suspected Redis data loss

A full recommendation recomputation can regenerate ordinary recommendations
from active in-memory entities. It may not reconstruct all directional
exclusions because exclusions are also stored in Redis.

Before relying on a rematch after Redis loss:

- Determine whether exclusions were lost.
- Identify which exclusions can be reconstructed from relational business
  records.
- Preserve participant-facing study-team promotions separately from ordinary
  system recommendations.

## Related pages

- [Support Routing](support-routing.md)
- [PHI Audit](phi-audit.md)
- [Messaging](../06-recruitment/messaging.md)
- [Interested-Participant Management](../06-recruitment/interested-participant-management.md)
- [Study Lifecycle](../05-study-management/study-lifecycle.md)
- [Open Questions](../09-decisions/open-questions.md)
