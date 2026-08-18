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

Event creation and email delivery are separate operations. Some notifications
are sent immediately, while others are dispatched by scheduled jobs.

## Events and frequencies

| Event | Available frequency |
|---|---|
| New interested participants | Immediate, daily digest, weekly digest |
| New messages | Immediate, daily digest, weekly digest |
| New matched participants | Daily digest, weekly digest |
| Other announcements | No selectable frequency |

Other Announcements includes lifecycle events such as study activation and
deactivation.

## Recipient behavior

- The posting creator is subscribed by default.
- The current PI is automatically subscribed to Other Announcements.
- Only accepted study team members may be selected as study-member recipients.
- Pending invitees cannot be selected.
- External non-member email addresses may be added.
- External email addresses are not validated by the application.
- The same external address may receive multiple event types.
- All recipients for one study/event share the configured event frequency.

## Immediate events

When Immediate is selected for a supported event, the application attempts to
send the applicable notification without waiting for a daily or weekly digest.

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
Email was delivered
```

## Activation and deactivation announcements

Activation and deactivation emails are not sent synchronously as part of the
status-changing request.

A daily scheduled process evaluates lifecycle changes and recipients configured
under Other Announcements.

The current PI receives applicable lifecycle notifications.

A one-day stabilization rule may suppress PI notifications for short-lived
state changes.

For example:

```text
ACTIVE → INACTIVE → ACTIVE within one day
```

does not generate a stable-state PI notification, even though the underlying
operational transitions may have occurred.

## Upcoming-deactivation warning

The current PI receives an email approximately one week before the study's
configured deactivation date.

This warning is separate from:

- The later deactivation announcement
- New matched-participant notifications
- Other study-team digest events

The warning allows the PI and study team to review the upcoming expiration.

## Ask if interested participant notification

Ask if interested promotes an existing match into the participant's
study-team-promoted studies area.

The promotion updates the applicable Redis recommendation timestamp.

A scheduled job compares promoted-match timestamps with the participant's last
login. When an eligible promotion is newer than the last login, the participant
may receive a system-generated email prompting them to sign in and review newly
suggested studies.

The email:

- Does not contain or create a direct-message conversation
- Does not mean the participant expressed interest
- Directs the participant to sign in and review the promoted study

## Membership removal

When a study membership is removed, that member's notification settings for the
study are removed.

When the imported PI changes:

- The former PI membership is removed.
- The new current PI becomes the PI recipient for PI-specific notifications.
- The new current PI is subscribed to Other Announcements according to the
  current PI rule.

## In-application alerts

Email-notification configuration does not control:

- New-participant badges
- Message-inbox indicators
- Other in-application alerts

## Operational considerations

Administrative users can manage scheduled-job schedules through an
administrative interface.

The detailed controls, validation rules, permissions, and audit behavior for
that interface remain to be documented.

## Related pages

- [Study Lifecycle](study-lifecycle.md)
- [Study Membership](../04-users-and-access/study-membership.md)
- [Ask If Interested](../06-recruitment/ask-if-interested.md)
- [Interested-Participant Management](../06-recruitment/interested-participant-management.md)
- [Messaging](../06-recruitment/messaging.md)
- [Notification Model](../07-data-model/recruitment-operations-model.md)
