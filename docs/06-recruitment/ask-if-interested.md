---
title: Ask If Interested
summary: Study-team promotion of an active study to a visible matching participant without direct messaging.
status: authoritative
canonical_for:
  - ask_if_interested
  - study_team_promotion
relevant_when:
  - promoting_a_study
  - explaining_ask_if_interested
  - troubleshooting_promoted_studies
---

# Ask If Interested

Ask if interested promotes a study to a visible matching participant.

It emphasizes an existing match by moving the participant-facing study from the ordinary
system-matched presentation into the study-team-promoted presentation.

It is distinct from:

- Direct messaging
- Expression of interest
- Ordinary system-generated participant recommendations

## Promotion storage and lifecycle

### Current implementation

Ask if interested is a study-team promotion action available from exact- and partial-match workflows. It moves the represented participant into the study team's Asked if interested list. The modal limits the optional note to 275 characters and supports first- and last-name merge tokens for bulk action. It also states that the study and note will appear in the participant's studies list and will not be sent as a direct message.

The participant interface separates Suggested by study teams from Matched by system. Ask if interested does not create an expression-of-interest `STUDY_VOLUNTEER`, a direct message, or enrollment. Participant history currently categorizes interest and dismissal events but has no promotion-history category.

`RECOMMENDED_STUDY_MESSAGE` stores the participant, study, recommending user, message, and reason. Its physical message limit is 512 characters. The reason includes `ASKED_IF_INTERESTED` and `RECOMMENDED_ANOTHER_STUDY`. The three foreign keys are restrictive, but the table has no promotion timestamp, active marker, participant-study-reason uniqueness constraint, Redis score, or durable email-attempt link. Multiple rows for the same participant and study can therefore exist physically.

The current repeat-prevention mechanism is Redis rather than relational uniqueness. The `ASKED_IF_INTERESTED` study-side exclusion prevents the same action from recurring, while the participant's `USER` recommendation score carries the promotion timestamp. A relational message row alone cannot deterministically reconstruct current Redis promotion state or its original timestamp.

When the participant selects Not Interested or Enrolled for a promoted study, the application removes promotion-message rows for that participant-study pair. Promotion retention, orphan cleanup, and exact reconstruction procedures remain unresolved policy or operational concerns.

### Known concerns

- Durable rows do not enforce promotion uniqueness or preserve the promotion event timestamp.
- Redis state and relational promotion messages can diverge and are not complete substitutes for each other.
- The participant-visible 275-character limit is stricter than the 512-character database limit.
- The promoted-study display is intentionally separate from direct messaging and expression of interest; documentation and code review must not conflate these workflows.

## Preconditions

Ask if interested requires:

- Active study
- Active participant
- Study membership or administrative access
- Participant visible to the study team
- Exact or partial study-facing eligibility match
- No existing exclusion that prevents the action

## Study-team action

When the study team selects Ask if interested:

1. The study team enters promotional text.
1. The application records the promotion.
1. The participant-study pair is removed from the ordinary study-side matched presentation.
1. The study is added to or emphasized in the participant's study-team-promoted studies area.
1. The Redis promotion timestamp is updated.
1. The study-side exclusion reason `ASKED_IF_INTERESTED` is created so the participant does not
   remain in the ordinary study-side match bucket.

The promotional text is displayed with the study card. It is not delivered as a private message.

## Participant-facing effect

The participant sees the study in the area labeled for studies suggested by study teams.

The study-team-authored promotion appears with or above the study card, depending on the current
interface presentation.

The action does not guarantee that the participant will:

- Open the study
- Express interest
- Qualify after the final eligibility recheck
- Reply to the study team

## Scheduled email notification

Ask if interested does not send an immediate email. It creates a
participant-facing `USER` recommendation whose Redis sorted-set score records
the promotion time.

The participant's general recommended-studies preference controls later email
processing:

- Daily
- Weekly
- Biweekly
- Monthly
- Never

There is no separate promotion frequency and no immediate option.

For each applicable frequency run, the batch-notification job evaluates active
participant accounts. It compares both `SYSTEM` and `USER` recommendation
scores with the represented participant's `APP_USER.LAST_LOGIN_DATE`. A
qualifying recommendation must also refer to a currently active study.

The application sends at most one generic new-recommendations email to a
qualifying represented participant during one frequency run. Multiple promoted
or system-recommended studies are collapsed into that email; they are not
grouped into separate messages by study or recommendation source.

The comparison uses the `LAST_LOGIN_DATE` field of the represented participant
account being evaluated, not `LOGIN_AUDIT` or a session timestamp. Ordinary
authentication updates the authenticated account's login fields. Logging in as
an owner does not update every loved-one account. The normal account-switch
path replaces the security principal without invoking the login-time update, so
switching to a loved-one context does not itself update that loved one's
`LAST_LOGIN_DATE`.

Loved-one accounts are processed as independent represented participants and
use their own recommendation preference and login timestamp. They may share an
email address with their owner, but that does not merge their batch evaluation.

This email:

- Is generated by the application
- Is not the study team's promotional text sent as a direct message
- Does not open a conversation
- Does not create an expression of interest

## What it does not do

Ask if interested:

- Does not create `STUDY_VOLUNTEER`
- Does not mean the participant expressed interest
- Does not open a direct-message conversation
- Does not allow the participant to message the study
- Does not bypass the final eligibility recheck
- Does not enroll the participant
- Does not guarantee email delivery

## Repeat behavior and participant response

While the study-side `ASKED_IF_INTERESTED` exclusion remains for the
participant-study pair, another Ask if interested attempt is rejected.

A rejected repeat does not:

- Replace or append the stored promotion message
- Update the participant-facing `USER` recommendation timestamp
- Create another promotion record
- Create a new email-triggering event

The application does not expose an ordinary reverse transition that clears the
`ASKED_IF_INTERESTED` state solely to permit another promotion.

After a successful first promotion, the participant may:

- Open the study posting
- Begin the show-interest workflow
- Dismiss the study as Not Interested
- Take no action

If the participant expresses interest, the ordinary interest transaction and
Redis exclusions are applied.

## Common misunderstanding

Ask if interested may be mistaken for direct outreach.

The accurate interpretation is:

```text
Promote and emphasize an existing match in the participant interface
```

not:

```text
Send a private message to the participant
```

Direct messaging remains unavailable until the participant has successfully expressed interest and a
study team member initiates the conversation.

## Related pages

- [Matching and Visibility](matching-and-visibility.md)
- [Expressions of Interest](expressions-of-interest.md)
- [Messaging](messaging.md)
- [Study Notifications](../05-study-management/study-notifications.md)
- [Redis Match and Exclusion Model](../07-data-model/redis-match-model.md)
