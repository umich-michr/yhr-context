---
title: Troubleshooting
summary: Causes and checks for common import, study, PI, participant, questionnaire, and export problems.
status: authoritative
relevant_when:
  - answering_support_questions
  - investigating_import_failures
  - investigating_access_problems
  - investigating_matching_problems
---

# Troubleshooting

## Posting cannot be created

Check:

- Was the correct `study_num` entered?
- Does it exist in `IMPORTED_STUDY.ID`?
- Did import validation report an anomaly?
- Does an operational `STUDY` already exist for the `study_num`?
- Did another user create the posting concurrently?
- Is the institutional SAML session valid?
- Does the creator have access to the institutional study-team interface?
- Does the imported study have a current PI?
- Does the PI have both email and ePPN?

A study posting cannot be created for a study number absent from `IMPORTED_STUDY`.

A duplicate posting cannot be created.

## CSV import failed

Check:

- Is the JSON Web Token valid?
- Has the token expired?
- How does `STUDY_IMPORT_TOKEN_GRACE_PERIOD` affect token validity?
- Does the importing user have the `STUDY_IMPORTER` role?
- Does the CSV have the expected columns?
- Did application validation detect anomalous data?
- Were errors written to application logs?
- Was an error email sent to the responsible study importer?
- Does every imported study have `PUBLISHABLE` set to `0` or `1`?
- Does the current PI have email and ePPN?

## Import did not remove an old record

This is expected.

Imports are incremental.

A record absent from a later CSV is not treated as deleted.

The existing imported and operational data remains unchanged.

## Import cannot be rolled back

This is expected.

The application does not support import-batch rollback.

A correction requires a later incremental import with the corrected values.

## Study changed status during import

Check:

- Did the CSV contain multiple rows for the same `study_num`?
- Which row was selected as the latest update?
- Was only the final state applied to operational data?
- Was active status recalculated using the final publishability value?
- Did the transition come from a later separate import rather than an intermediate row?

Historical intermediate rows in one CSV should not cause operational deactivation and reactivation.

## Study became inactive

Check:

- Is `PUBLISHABLE = 0`?
- Has the deactivation date passed?
- Has the activation date not yet arrived?
- Did reconciliation update publishability?
- Did the study team alter the dates?
- Did the latest imported update change the final state?

## Study became active again unexpectedly

Check:

- Did `PUBLISHABLE` change from `0` to `1`?
- Does the current date remain inside the existing activation and deactivation dates?

If both are true, automatic reactivation is current behavior.

The application does not currently require a separate manual confirmation after publishability returns to `1`.

## PI did not receive a status-change email

Check:

- Did the status return to its original value within one day?
- Has the changed status persisted for more than one day?
- Which user is currently considered the PI for notification?
- Did email delivery fail?

A transition such as:

```text
ACTIVE → INACTIVE → ACTIVE
```

within one day does not generate a notification.

## Current PI is missing

Check:

- Does `IMPORTED_STUDY_TEAM_MEMBER` identify the current PI?
- Does the role value match the configured PI role code for that study?
- Does `IMPORTED_TEAM_MEMBER` contain the PI?
- Does the PI have email?
- Does the PI have ePPN?
- Does the identity match an existing `APP_USER`?
- Did Java or Oracle reconciliation complete?
- Did `APP_USER` creation fail?
- Did membership creation fail?

## Former PI still has access

This is consistent with current behavior.

When the imported PI changes:

- The new PI is associated with the study.
- The former PI's existing operational membership is not automatically removed.

Inspect all operational memberships with:

```text
STUDY_ROLE = PRINCIPAL_INVESTIGATOR
```

Do not assume that every operational PI membership represents the current imported PI.

## PI name or email is stale

Imported name and email values are copied when a PI `APP_USER` is initially created.

Later imported name or email changes are not copied into an existing `APP_USER` under current behavior.

## Team member cannot access a study

Check:

- Did SAML authentication succeed?
- Does the user have an `APP_USER`?
- Does the user have the `STAFF` application role?
- Does the user have a membership for the requested study?
- Was the ordinary membership removed?
- Was the invitation successfully accepted?
- Was the invitation token valid and unexpired?
- Is the user relying only on a non-PI institutional role that does not automatically grant application access?

## Invitation does not work

Check:

- Does the invitation record still exist?
- Has the invitation expired?
- Was the invitation revoked by record deletion?
- Was it already accepted?
- Did the recipient authenticate through SAML?
- Did membership creation succeed?
- Was the invitation record deleted only after membership creation completed?
- The link may be accepted by any SAML-authenticated institutional user who
  possesses it; it is not bound to the emailed recipient.

## Participant activation link does not work

Check:

- Does the activation token exist?
- Has the activation token expired?
- Was the account already activated?
- Was the activation link copied completely?
- Does the configured expiration match the participant's registration time?

## Participant is no longer visible

Check:

- Is the participant account active?
- Is the study active?
- Is `PUBLISHABLE = 1`?
- Does the user still have study access?
- Is the participant restricted or discoverable?
- Is the participant an exact or partial match?
- Did the participant express interest?
- Is the record historical with profile masking?

## Match appears as partial instead of exact

Check:

- Does an eligibility criterion reference an optional profile property?
- Is the participant missing a value for that property?
- Did the expression evaluate to `MAYBE`?
- Were all affected matches recalculated after the profile or criteria change?

A `MAYBE` eligibility result is displayed as a partial match.

## Match did not update after a profile change

Check:

- Was the changed property referenced by eligibility criteria?
- Was the participant's all-active-study recalculation triggered?
- Is the study active?
- Did the recalculation complete?
- Is a stored result stale?

## Matched studies changed but study-side participants did not

This may be expected after a participant changes study interests.

Participant interests affect the participant's matched-study list.

They do not affect the study's matched-participant list, which is based on eligibility and visibility.

## Participant cannot express interest

Check:

- Is the participant account active?
- Is the study active?
- Is `PUBLISHABLE = 1`?
- Did the participant update temporal profile values?
- What was the current eligibility result?
- Did the participant answer all required questionnaire questions?

If the eligibility recheck fails, the application displays a message that the participant cannot show interest because they are not eligible.

## Participant wants to withdraw interest

Participants cannot withdraw a finalized expression of interest through the application.

Any support or administrative correction process is not currently documented.

## Questionnaire cannot be edited

Check:

- Is the study active?
- Is the study team trying to edit an existing question?

The study must be inactive before its questionnaire structure can change.

While inactive:

- Questions may be added.
- Questions may be deleted.
- Question display order may be changed.
- Other existing-question content cannot be edited.

## Participant cannot edit questionnaire answers

This is expected.

Submitted questionnaire answers cannot be edited.

## Export is unavailable

Check:

- Does the user have a study membership?
- Is the user an `ADMIN`?
- Is the study publishable?
- Is `PUBLISHABLE = 1`? Inactive but publishable studies may export historical interested-participant data.
- Is participant profile information currently accessible?
- Is the participant relationship permitted for export?

When the study becomes non-publishable, study team members cannot access participant information or generate a new export.

## Participant requests reactivation or deletion

Participants request reactivation or hard deletion by emailing support.

For reactivation, an administrator uses the Help Participants interface. For
deletion, an administrator confirms the request, records a reason, and uses
the same interface to permanently remove participant data.

The application retains only the internal participant ID and deletion reason;
the original request is retained in ServiceNow rather than the application.

## Previously downloaded export remains available

This is expected.

After a CSV is downloaded, it exists outside the application.

The application cannot:

- Invalidate it
- Recall it
- Delete it from the study team's device

## Related pages

- [Support routing](support-routing.md)
- [Audit and monitoring](audit-and-monitoring.md)
- [Publishability](../03-institutional-governance/publishability.md)
- [Study membership](../04-users-and-access/study-membership.md)
- [Matching and visibility](../06-recruitment/matching-and-visibility.md)
- [Open questions](../09-decisions/open-questions.md)