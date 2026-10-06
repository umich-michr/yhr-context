---
title: Study Notifications
summary: Study-specific events, recipients, frequencies, scheduled dispatch, lifecycle announcements, and PI deactivation warnings.
status: authoritative
canonical_for:
  - study_notifications
  - notification_frequencies
  - notification_recipients
  - lifecycle_notifications
relevant_when:
  - configuring_study_notifications
  - troubleshooting_notification_email
  - explaining_notification_frequencies
  - explaining_deactivation_warnings
---

# Study Notifications

Study notification settings are configured per study and event.

Event creation and email delivery are separate operations. Some notifications are sent immediately,
while others are dispatched by scheduled jobs.

## Notification settings and recipients

### Current implementation

Each study has one `STUDY_NOTIFICATION_SETTING` row per notification event. A unique constraint on `(STUDY_ID, NOTIFICATION_SETTING_LV_ID)` enforces that rule. The setting points to an event lookup and, when the event supports selectable timing, a notification-frequency lookup.

`NOTIFICATION_SETTING_FREQ` is the compatibility table between event and frequency lookups. Its composite key contains both lookup IDs, and `ORDER_NUM` controls display order. Checked-in seed data permits:

- immediate, daily, or weekly delivery for new interested participants;
- immediate, daily, or weekly delivery for new messages;
- daily or weekly delivery for new matched participants; and
- no selectable frequency for Other Announcements.

This compatibility is current seed and application behavior, not a policy that every deployment must preserve unchanged.

Selected study members are normalized through `STUDY_NOTIFICATION_RECIPIENT`, whose composite key joins a setting to a `STUDY_TEAM_MEMBER`. Deleting a membership cascades its recipient joins. The setting-side foreign key is restrictive. `RECIPIENT_EMAILS` remains a string on the setting rather than a normalized external-recipient collection.

New studies receive a setting for every supported event. When only one team member exists, that member is the default recipient; otherwise the current service selects the first non-PI member it finds. PI subscription to Other Announcements is application behavior and must not be described as a physical-schema constraint.

A save validates that the event is a `NOTIFICATION_SETTING` lookup, any frequency is a `NOTIFICATION_FREQUENCY` lookup, and every selected member belongs to the study. The update is transactional and invokes `auditNotificationUpdate`. The dispatcher combines selected-member and external addresses into a set, so all recipients of one study/event share that event's frequency.

The current study-team interface presents New Interested Participants, New Messages, New Matched Participants, and Other Announcements. It treats the external-recipient field as one email address, although the transfer-object contract says that comma- or space-separated addresses may be stored. Application-level validation of that stored string was not established.

Participant recommendation notifications are different: their timing comes from each represented participant's preference and last-login state, not from `STUDY_NOTIFICATION_SETTING`.

### Delivery, batching, and retention evidence

Daily and weekly processing owns study-team digests. Current transaction batches contain up to 100 participant emails or 10 study-team emails. `EMAIL_LOG` records rewritten attempt data and local `SUCCESS` or `FAILURE`, but does not prove mailbox delivery. In particular, successful Java Message Service submissions are not recorded as `EMAIL_LOG.SUCCESS`; non-queue success, console success, queue submission, no-recipient success, and failure remain distinct outcomes.

The checked-in Oracle audit-backup job moves `EMAIL_LOG` records older than 180 days to backup storage without the message body, then removes backup rows after 1,461 days. These are job definitions, not proof that every deployment runs them effectively. Recommendation-notification filesystem audit files are separate and expire after 31 days when that audit is enabled.

### Known concerns and remaining decisions

- External recipient normalization and validation are not established.
- The active email profile, queue topology, provider evidence, scheduler times and time zone, monitoring, operational runbooks, and effective retention execution are deployment-specific.
- Delivery logs establish application or transport outcomes, not mailbox receipt.
- Recipient-selection and retention policies remain institutional decisions where they are not fixed by current behavior.

## Events and frequencies

| Event                       | Available frequency                    |
| --------------------------- | -------------------------------------- |
| New interested participants | Immediate, daily digest, weekly digest |
| New messages                | Immediate, daily digest, weekly digest |
| New matched participants    | Daily digest, weekly digest            |
| Other announcements         | No selectable frequency                |

Other Announcements includes lifecycle events such as study activation and deactivation.

## Recipient behavior

- The posting creator is subscribed by default.
- The current PI is automatically subscribed to Other Announcements.
- Only accepted study team members may be selected as study-member recipients.
- Pending invitees cannot be selected.
- External non-member email addresses may be added.
- External email addresses are not validated by the application.
- The same external address may receive multiple event types.
- All recipients for one study/event share the configured event frequency.

## PI replacement behavior

When import reconciliation replaces a PI, it retains the existing PI
membership row and changes the user referenced by that row. Existing study
notification recipient selections attached to that membership ID consequently
resolve to the new PI.

When the incoming PI also has a separate ordinary membership, reconciliation
deletes that duplicate membership. The database cascades deletion to
notification-recipient join rows attached to the deleted membership; those
recipient selections are not copied to the retained PI row.

External addresses in the study notification setting remain unchanged. The
reviewed reconciliation path does not generate a separate PI-change
announcement. A PI receives a later announcement only if the resulting
recipient settings and event-processing rules select that membership or
address for an independently generated event.

## Immediate events

When Immediate is selected for a supported event, the application attempts to send the applicable
notification without waiting for a daily or weekly digest.

Immediate is supported for:

- New interested participants
- New messages

Immediate is not offered for new matched participants.

## Scheduled digest processing

Scheduled jobs process:

- Daily digests
- Weekly digests
- New matched-participant notifications
- Other Announcements
- Lifecycle notifications
- Participant study-promotion notifications

A configured event may exist before its email is sent.

Troubleshooting must therefore distinguish:

```text
Event occurred
Recipient was configured
Digest job ran
Email was generated
External mail or recipient system confirms delivery
```

## Activation and deactivation announcements

Activation and deactivation emails are not sent synchronously as part of the
status-changing request.

The daily batch-notification job evaluates lifecycle changes recorded in
`STUDY_ACTIVE_INTERVAL`. It queries the previous calendar day, from the prior
day at midnight through one second before the current day at midnight. These
calendar boundaries use the application or Java virtual machine system-default
time zone.

The interval queries suppress transitions superseded by another applicable
interval. This produces the observed stabilization behavior. It is not a
separate recipient-level delay, a rolling 24-hour timer, or an
institution-configured stabilization interval.

For each selected study, the application resolves the complete current
recipient set configured for Other Announcements at dispatch time. That set can
include:

- The current PI, who is automatically subscribed
- Other selected accepted study team members
- Configured external email addresses

The stabilization behavior is therefore not limited to the PI. The lifecycle
query also does not classify a transition as manual, date-driven, or
publishability-driven; it operates on active intervals recorded by application
update and import paths.

## Upcoming-deactivation warning

Upcoming-deactivation warnings are generated by the daily batch-notification
job. Warning timing is controlled by the integer-list application setting
`STUDY_ANNOUNCEMENTS_DAYS_AHEAD`.

For each configured integer, the job queries the complete calendar day exactly
that many days after the beginning of the current day. The installation seed is
`2,14`, so the reviewed default configuration checks for studies deactivating
two and fourteen calendar days ahead. These are seed defaults and may be
changed in a deployment.

Calendar boundaries use the application or Java virtual machine system-default
time zone.

Warnings are sent to the current Other Announcements recipient set rather than
through a distinct PI-only recipient path. They are separate from:

- The later deactivation announcement
- New matched-participant notifications
- Other study-team digest events

The workflow stores no sent-warning record, deduplication marker, or
idempotency key. A study can therefore receive multiple warnings because
multiple offsets are configured, its deactivation date changes into a target
day again, or the same job window executes more than once.

## Ask if interested participant notification

Ask if interested promotes an existing match into the represented
participant's study-team-promoted studies area. The action creates a
participant-facing Redis recommendation with source `USER`; its sorted-set
score is the promotion time.

The same general participant preference used for ordinary recommended-study
email controls promotion email:

- `DAILY`
- `WEEKLY`
- `BI_WEEKLY`
- `MONTHLY`
- `NEVER`

There is no immediate option and no separate Ask if interested email
preference.

For each applicable frequency run, the batch-notification job iterates active
participant accounts. It compares recommendation scores with that represented
participant's `APP_USER.LAST_LOGIN_DATE`, filters out studies that are no longer
active, and sends at most one generic new-recommendations email to each
qualifying participant account.

The query includes both `SYSTEM` recommendations and study-team `USER`
promotions. Multiple qualifying studies or sources are therefore collapsed
into one email for the represented participant during that run. The email is
not grouped or sent separately by study or recommendation source.

For a loved-one account:

- Its own recommendation frequency and `APP_USER.LAST_LOGIN_DATE` govern its
  recommendation email.
- A normal authentication as that account updates its login timestamp.
- Logging in as the owner updates the owner's timestamp, not every loved one's.
- Switching account context changes the security principal but does not call
  the login-time update path, so the switch itself does not update the selected
  loved one's last-login timestamp.
- Loved-one accounts are evaluated separately even when they share the owner's
  email address.

The email is system-generated. It does not include the study team's
promotional note as a direct message, open a conversation, or create an
expression of interest.

A repeated Ask if interested attempt is rejected while the pair retains its
study-side `ASKED_IF_INTERESTED` exclusion. The repeated attempt does not append
or replace the promotion message, update the promotion score, or create another
email-triggering recommendation event.

## Membership removal

When a study membership is removed, that member's notification settings for the study are removed.

When the imported PI changes:

- The former PI membership is removed.
- The new current PI becomes the PI recipient for PI-specific notifications.
- The new current PI is subscribed to Other Announcements according to the current PI rule.

## In-application alerts

Email-notification configuration does not control:

- New-participant badges
- Message-inbox indicators
- Other in-application alerts

## Operational considerations

Administrative users can manage scheduled-job schedules through an administrative interface.

The detailed controls, validation rules, permissions, and audit behavior for that interface remain
to be documented.

## Related pages

- [Study Lifecycle](study-lifecycle.md)
- [Study Membership](../04-users-and-access/study-membership.md)
- [Ask If Interested](../06-recruitment/ask-if-interested.md)
- [Interested-Participant Management](../06-recruitment/interested-participant-management.md)
- [Messaging](../06-recruitment/messaging.md)
- [Notification Model](../07-data-model/recruitment-operations-model.md)

## Email generation and delivery evidence

Notification event selection, email generation, transport handoff, and
recipient delivery are distinct stages.

After an event is selected, the application:

1. Renders a body and subject from the configured theme and language templates.
1. Creates an `EmailMessage` with sender, reply-to, recipients, subject, and body.
1. Runs the email-rewriter chain.
1. Invokes the email client selected by the active Spring profile.

Available clients are:

- `consoleEmailClient` — logs that it would have sent the message
- `javaEmailClient` — connects to the configured SMTP or SMTPS server and calls
  Jakarta Mail transport
- `jmsEmailClient` — serializes the message as a Java Message Service object
  message and sends it to the configured queue

### Recipient rewriting

Before transport handoff, the recipient rewriter reads
`REWRITE_EMAIL_RECIPIENTS` and `REWRITE_EMAIL_RECIPIENTS_WHITELIST`.

When rewriting is enabled:

- Original To, Cc, and Bcc addresses are combined for allow-list matching.
- Matching allow-listed addresses become the To recipients.
- If none match, configured rewrite recipients are used.
- If neither an allow-listed recipient nor a replacement exists, all recipients
  become empty.
- Cc and Bcc are cleared.
- The rewritten message is the version handed to transport and stored in local
  email logs.
- A later rewriter can append a description of recipient changes to the body.

### Meaning of local success

For non-JMS profiles, `EmailSenderImpl` inserts `EMAIL_LOG.STATUS = SUCCESS`
after the configured client returns without throwing.

That status has client-specific meaning:

- With `javaEmailClient`, Jakarta Mail connected and returned from
  `sendMessage(...)` without an observed exception. This is application evidence
  of SMTP transport handoff, not proof of final mailbox delivery.
- With `consoleEmailClient`, the application only logged that it would have sent
  the email. No external delivery occurred.
- With `jmsEmailClient`, this application does not insert a success row. A
  successful call establishes only that the local Java Message Service send
  returned; downstream consumption and email transport belong to another
  application or service.

A non-JMS message with no recipients skips the client call but still reaches the
local success-log insertion. Such a row does not prove transport handoff.

### Meaning of local failure

A client or template error becomes `SendEmailException`. The web-controller
exception advice stores the attached message as `EMAIL_LOG.STATUS = FAILURE` and
creates an application-error record.

This failure recording is path-dependent. It is confirmed when the exception
reaches that controller advice. Scheduled or background workflows that catch,
transform, or handle exceptions elsewhere are not proven to create the same
failure row.

`EMAIL_LOG` contains the attempted message and one of two statuses, but no
provider message identifier, queue identifier, SMTP response, bounce reason,
delivery time, open/read event, retry count, or last-error field.

### External evidence boundary

Final delivery, bounce, rejection after initial SMTP acceptance, Java Message
Service consumption, downstream retries, and mailbox receipt require records
from the deployed queue, mail relay, provider, or recipient system. The
application's local success status alone cannot establish those outcomes.
