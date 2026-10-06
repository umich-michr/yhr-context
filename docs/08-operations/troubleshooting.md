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

## Child age-out warning or deactivation failed

Establish the effective deployment configuration first:

- Current `DAYS_BEFORE_MATURE_TO_NOTIFY`
- Current `YEARS_TO_BE_CONSIDERED_MATURE`
- Current persisted `childAccountDeactivationJob` cron expression
- Scheduler or Java virtual machine default time zone
- Number of application processes running equivalent schedules

For a missed warning, verify that a successful run occurred while the date of birth was strictly inside
the configured open interval. With the installation value 14, eligibility is 1 through 13 calendar days
before maturity. Also inspect `CHILD_DEACTIVATION_NOTICE` using parent ID, child ID, and the recorded
date-of-birth string.

For a failed or partial run:

1. Inspect Quartz and application logs for the first uncaught child-processing, parsing, template, data,
   or email exception.
1. Do not rely on the wrapper success log as proof that every child completed.
1. Compare authentication enablement and `USER_DEACTIVATION` with the handling process's active-user
   store.
1. Inspect `APPLICATION_ERROR` and Redis for incomplete asynchronous cleanup.
1. Check warning and age-out email evidence separately; transport handoff does not prove delivery.
1. Account for warning email without a committed notice row and for local-memory or Redis effects that
   escaped a rolled-back relational transaction.
1. After correcting the cause, rerun the child job. It reevaluates current state but has no resume
   cursor or automatic retry ledger.
1. If relational state is active while local memory is missing, run active-user synchronization or
   restart the affected process as appropriate.
1. If ordinary recommendations remain stale, rerun cleanup through a verified deactivation path or
   perform full recommendation recomputation after local stores are correct. Full recomputation does
   not restore or remove every exclusion or `USER` promotion.

Repair each affected application process independently; the application has no cluster-wide memory
repair or age-out reconciliation command.

## Adult self-registration does not show prior loved-one history

Check whether support is comparing two distinct user IDs:

- The aged-out loved-one account retains its generated username, `LOVED_ONE` relationship, profile, and
  history but is disabled with `CHILD_TURNED_ADULT`.
- Public self-registration uses the adult's entered email as a new username and creates a new account.
- No automatic match, claim, merge, transfer, or history migration occurs.
- A username collision is rejected rather than attached to the old account.

Do not manually re-enable the age-out account or infer identity solely from matching demographics or
email. Any consolidation, data movement, or disclosure requires an authorized identity, privacy, and
records-handling procedure with a backup and audit plan.

## Posting cannot be created

Check:

- Does the entered `study_num` exist in `IMPORTED_STUDY`?
- Does an operational posting already exist?
- Does the imported study have one current PI?
- Does the PI have email and `USER_NAME`?
- Does imported `USER_NAME` match the SAML ePPN value?
- Did import or reconciliation fail?

## CSV import reported row or batch failures

Check:

- Was the header valid and complete?
- Was the row tokenized successfully?
- Did bean validation reject publishability, study number, PI username, PI name, or PI email?
- Did row processing record a persistence exception?
- Did batch flush or commit fail?
- Did an uncaught runtime exception stop the file?
- Which earlier batches had already committed?
- Did process-local active-study or matching work start before the failed database commit?

The default importer commits in batches of up to 500 processed rows. A commit failure rolls back the
current batch when possible but does not undo earlier committed batches. It also cannot roll back
process-local memory changes, asynchronous matching tasks, Redis effects, or later notification
selection caused by work already initiated.

A row-level persistence error does not prove row-level rollback. The importer continues in the same
transaction without explicitly clearing or restarting it. Compare all three imported tables,
operational study and PI state, synchronization logs, active intervals, process-local memory, matching
status, Redis state, and application errors before preparing a corrective incremental row.

## Interrupted CSV import recovery

The application cannot resume an archived CSV from a stored row checkpoint.

1. Preserve the timestamped processed CSV and same-basename text log.
1. Determine which transaction batches committed and which current batch rolled back.
1. Check whether `CSV_FILE_UPLOAD_LOG` exists; absence may mean processing failed before the
   controller wrote the audit.
1. Inspect linked detail rows, time-adjacent reconciliation logs, imported tables, operational study
   and PI state, active intervals, application errors, process-local memory, matching status, and
   Redis.
1. Account for memory or matching work that may have started before a database rollback.
1. Build a new corrective incremental file containing the intended authoritative state.
1. Submit the corrective subset or full file according to the verified state; do not assume replay is
   globally idempotent.
1. Verify database, memory, Redis, and notification outcomes after correction.

Resubmitted rows generally update existing imported entities by key, and unchanged stable values
usually avoid repeat operational changes. Nevertheless, every submission creates new file artifacts
and may create a new upload audit, errors, reconciliation history, lifecycle effects, matching work,
and notification consequences.

## PI reconciliation failed

Check:

- Did the incoming PI already have an ordinary membership for the study?
- Did reconciliation delete that row before reassigning the former PI row?
- Did either explicit flush fail?
- Does the study have exactly one `PRINCIPAL_INVESTIGATOR` membership?
- Does the `piUserId` property identify the same user?
- Do synchronization logs show the ordinary-membership deletion, PI-row update, property update, and
  any identity update?
- Did the import report a caught persistence error or a batch commit failure?
- Did the handling process refresh its active-study entry before a later rollback?

The database membership changes and synchronization logs normally share the current import batch
transaction. A successful rollback should undo that relational batch, but it cannot restore an
earlier process-local active-study object. The caught-persistence-exception path does not prove
row-level rollback. Verify current relational and process-local state before submitting a corrective
row.

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

## PI changed but notifications or account history look unexpected

Check:

- Which `STUDY_TEAM_MEMBER` row was retained as the PI row
- Whether notification-recipient joins remain attached to that retained
  membership ID
- Whether the incoming PI had a duplicate ordinary membership whose recipient
  joins were cascade-deleted
- Whether external recipient strings remained in the notification setting
- Whether the imported username matched an existing prefixed `APP_USER`
- Whether reconciliation created a new account instead of renaming the former
  account
- Whether `IMPORTED_STUDY_SYNC_LOG` records the PI membership, property,
  duplicate-membership deletion, account creation, or contact update
- Whether operators are incorrectly expecting memberships, agreements, login
  history, or other account history to move automatically between usernames

The importer does not generate a separate PI-change announcement and does not
automatically consolidate accounts that institutional evidence says belong to
the same person. Perform any account correction only through an authorized
procedure after verifying institutional identity, current memberships,
notification settings, and retained audit evidence.

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

Check each stage separately:

1. Did the business event occur?
1. Did notification-selection logic include the event?
1. Was the intended recipient configured at selection time?
1. Did template rendering create an `EmailMessage`?
1. Did recipient rewriting preserve the address, replace it, or remove all
   recipients?
1. Which email-client profile was active: console, Java Mail, or Java Message
   Service?
1. Does `EMAIL_LOG` contain a relevant success or failure row?
1. Did `resendFailedEmailsJob` process a failure row?
1. Do downstream queue, relay, provider, bounce, or mailbox records show what
   happened after application handoff?

Interpret `EMAIL_LOG` carefully:

- Non-JMS `SUCCESS` means the configured client returned without throwing.
- Java Mail success does not prove final mailbox delivery.
- Console success means no external send occurred.
- JMS queue submission success is not recorded locally in `EMAIL_LOG`.
- A no-recipient non-JMS message can still receive a local success row.
- A `FAILURE` row is confirmed when `SendEmailException` reaches controller
  advice; other background failure paths may differ.
- A row changed to success by the resend job records a successful retry call,
  not mailbox delivery.

Also check whether:

- The invitee is an accepted study member.
- The membership or notification setting was removed.
- The participant or study frequency was applicable.
- An external recipient address was entered incorrectly.
- Replacement and allow-list settings differ from production expectations.
- Overlapping or repeated resend execution may have produced duplicates.

External addresses are not validated by the application. Final delivery,
bounce, rejection, and recipient-mailbox acceptance require external
mail-service evidence.

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

1. Identify the application process serving the stale result and the process
   that handled the originating update.
1. Compare the authoritative database record with the affected process's
   in-memory entity.
1. Check application errors and matching failures associated with the update.
1. If the entity is missing from memory or is no longer active, an
   administrator may manually run `activeUsersSynchronizationJob` or
   `activeStudiesSynchronizationJob` as applicable.
1. If the entity remains active and exists in both database and memory,
   membership synchronization will leave it unchanged. Exercise a verified
   business update path that reloads that entity, or restart the affected
   application process to force a complete local store reload.
1. Repair every divergent process independently. The reviewed application has
   no cluster-wide entity broadcast, divergence detector, or repair command.
1. After source stores are current, run `updateAllRecommendationsJob` when
   ordinary Redis recommendations may also be stale.

`ApplicationStoreService` exposes only `getById` through the reviewed
administrator controller. It does not expose a supported generic command for
single-entity `addOrUpdate` or whole-store `refreshStoreFromDB`.

### Startup database outage or failed store load

Store population is clear-first and not an atomic map swap. A failed later
refresh can leave an already-published store empty, partial, or inconsistent.

Recovery is:

1. Restore database availability and correct the underlying load failure.
1. Restart the affected application process.
1. Confirm successful Spring context creation and store-load logs.
1. Verify the process's active-user and active-study data before returning it
   to normal service.
1. Recompute ordinary recommendations if matching ran from incomplete source
   stores.

A restart repairs only that process's local stores. It does not refresh another
server or rebuild Redis automatically.

### Failed or interrupted synchronization

Synchronization and matching failures create application errors and may send
configured error notifications, but failed matching is not automatically
retried. Cooperative interruption can also leave already completed work in
place while skipping unvisited entities.

After correcting the cause:

1. Rerun the applicable active-user or active-study synchronization job.
1. Confirm that the run was not interrupted.
1. Inspect application errors rather than relying only on the wrapper's
   informational success message.
1. Run full recommendation recomputation if additions, removals, or prior
   matching failures may have left ordinary recommendations stale.

## Suspected Redis data loss

`updateAllRecommendationsJob` reads the executing process's active-user and
active-study stores. It can regenerate ordinary participant-facing `SYSTEM`
recommendations and exact or partial study-facing recommendations.

It does not:

- Clear Redis before recomputing
- Detect an empty Redis instance automatically
- Reconstruct study-team `USER` promotions
- Reconstruct every directional exclusion
- Provide a complete Redis backup or restore workflow

Before relying on recomputation after Redis loss:

1. Stop further destructive Redis changes and determine whether a complete
   infrastructure restore is available.
1. Verify that every application process used for recomputation has current,
   complete local stores.
1. Inventory lost `vol.exc`, `std.exc`, and participant-facing `USER`
   recommendation state.
1. Identify which facts can be corroborated from relational expressions of
   interest, enrollment, or `RecommendedStudyMessage` records.
1. Do not assume those relational records provide every original Redis member,
   direction, reason, or timestamp; no general application reconstruction
   routine was found.
1. Restore Redis from infrastructure backup when exclusions, study-team
   promotions, or their timestamps must survive.
1. Verify the executing process's active-participant and active-study stores;
   full recomputation reads those process-local stores rather than directly
   rereading all relational source tables.
1. After source stores and retained Redis business state are correct, manually
   run `updateAllRecommendationsJob` to reconstruct ordinary `SYSTEM`,
   exact, and partial recommendations.
1. Validate representative participant-facing and study-facing results,
   exclusions, and `USER` promotions.

Do not flush or replace Redis expecting full recommendation recomputation to
restore all user actions.

### Orphaned Redis state after participant deletion

Hard participant deletion initiates asynchronous recommendation cleanup and
then deletes relational participant data. It does not synchronously remove all
Redis state.

After deletion, inspect for the deleted participant ID in:

- `vol.rec:<participant>:SYSTEM`
- `vol.rec:<participant>:USER`
- `vol.exc:<participant>`
- Study-facing `std.rec:<study>:<result>` members
- Study-facing `std.exc:<study>` members

Ordinary deactivation cleanup targets ordinary recommendations. Exclusions and
`USER` promotions can remain even when that cleanup succeeds. If cleanup failed
or was interrupted, ordinary recommendations may remain as well.

The reviewed application has no whole-Redis referential-integrity sweep.
Removal of orphaned state therefore requires a deployment-approved procedure
that validates the participant ID, affected studies, business retention
requirements, and backup or rollback plan before modification.

## Participant cannot use a reactivated account

Check:

- Was the intended owner or loved-one profile reactivated?
- If an owner was reactivated, do individual loved-one accounts still remain inactive?
- If a loved one was reactivated, was the owner also restored when needed?
- Is the deactivation reason `CHILD_TURNED_ADULT`, which prevents reactivation?
- Has the account accepted the current participant agreement version?
- Did local active-user restoration and asynchronous rematching complete?

Reactivation does not itself record agreement acceptance. A reactivated participant without current
acceptance will receive the agreement interruption before ordinary application use.

The reviewed reactivation path does not send a dedicated participant notification, so support may
need to communicate the next login and agreement steps outside the application.

## Related pages

- [Support Routing](support-routing.md)
- [PHI Audit](phi-audit.md)
- [Messaging](../06-recruitment/messaging.md)
- [Interested-Participant Management](../06-recruitment/interested-participant-management.md)
- [Study Lifecycle](../05-study-management/study-lifecycle.md)
- [Open Questions](../09-decisions/open-questions.md)
