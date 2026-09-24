---
title: Participant Registration, Agreements, and Loved-One Accounts
summary: Signup, agreement-version enforcement, activation, visibility, communication email, and represented-participant account behavior.
status: authoritative
canonical_for:
  - participant_registration
  - participant_consent
  - participant_agreements
  - loved_one_accounts
  - participant_activation
relevant_when:
  - registering_a_participant
  - creating_a_loved_one_account
  - explaining_consent
  - explaining_agreement_updates
  - troubleshooting_activation
---

# Participant Registration, Agreements, and Loved-One Accounts

## Registration and loved-one creation paths

A participant account owner may:

- Register for themselves
- Register for a loved one
- Add a loved one after creating a self account

The signup-for-a-loved-one flow and Add Loved One both create a separate loved-one account managed
by the owning account.

The phrase “loved-one-first account” must not be treated as a separate account type. It describes
only the registration path through which the owning and loved-one accounts are established.

## Self signup

When registering for self, the person completes the required participant profile fields for the self
account.

The signup form asks:

```text
MY PROFILE IS VISIBLE TO
```

The available choices are:

```text
All study teams using the branded application instance
```

with explanatory text indicating that study teams may contact the participant about studies when the
profile appears to be a good fit, or:

```text
Only the study teams whose studies I show interest in
```

The selected value becomes the self profile's visibility setting.

## Signup for a loved one

Signup for a loved one creates two accounts:

1. A minimal owning account
1. A complete loved-one participant account

This does not mean that the owning account is a special kind of loved-one account. It is an ordinary
participant account created with only the information needed to authenticate and manage the
represented loved one.

### Minimal owning account

The owning account is created so the owner can authenticate and manage the loved-one account.

The signup flow collects the following owner information:

- Communication email
- First name
- Last name

The owner's communication email is also the owning account's username.

Country and ZIP code entered for the loved-one profile are copied to the owning account during this
signup flow.

Other required participant-profile fields are not collected for the owning account during this flow.
The owning profile is therefore incomplete for ordinary self participation.

The minimal owning profile defaults to hidden from study teams.

The copied country and ZIP values are confirmed signup behavior. They must not be described as
remaining automatically synchronized with later loved-one profile changes unless that behavior is
separately verified.

### Loved-one account

The loved-one account has:

- A separate user record
- A separate participant profile
- Required loved-one profile fields
- Its own visibility setting selected during signup
- An application-generated GUID-based email-like username
- The owning account's real email address for communication

The generated loved-one username is an internal authentication identity. It is not the loved one's
communication email address.

## Add Loved One

An existing self account may create a loved-one account through Add Loved One.

The new loved-one account receives:

- A separate user record
- A separate participant profile
- An application-generated GUID-based email-like username
- The owner's communication email
- The loved-one visibility selected in the Add Loved One workflow

The existing owning account is not recreated.

## Agreement definitions

Current agreement definitions are stored in:

```text
USER_AGREEMENT
```

Relevant fields are:

| Column    | Meaning                                 |
| --------- | --------------------------------------- |
| `ID`      | Unique agreement-definition identifier  |
| `TYPE`    | Agreement type                          |
| `VERSION` | Current agreement version for that type |

Known agreement types include values such as:

```text
VOL
STM
```

where:

- `VOL` identifies the participant or volunteer agreement
- `STM` identifies the study-team-member agreement

## Self and loved-one agreement presentation

Self and loved-one participant workflows use the same participant agreement type:

```
VOL
```

The agreement body is selected from one institution- and language-specific volunteer agreement file.
Frontend content selection receives the agreement type, institution/theme, and language. It does not
receive relationship, date of birth, age, or child/adult category.

The presentation differs by whether the workflow indicates that the account has loved ones:

- Without loved ones, the common participant agreement body is shown without the additional
  represented-loved-one acknowledgment.
- With loved ones, the same agreement body is shown and the owner must also:
  - Confirm that the agreement was read and accepted.
  - Confirm the common represented-loved-one discussion/decision acknowledgment.

The additional acknowledgment covers adults and children together. It says, in substance, that the
owner discussed participation in a way appropriate to the loved one's understanding and observed
willingness, or that the represented adult or child cannot discuss participation and the authorized
owner will decide.

There is no separate child agreement body, adult agreement body, agreement type, or frontend variant
selected from `LOVED_ONE.RELATIONSHIP` or date of birth. Child/adult-specific wording does appear in
the registration relationship choices, but those choices validate account creation and do not select
the agreement content.

## Agreement acceptance audit

Successful acceptance is recorded in:

```text
USER_AGREEMENT_AUDIT
```

The record contains:

| Column           | Meaning                                 |
| ---------------- | --------------------------------------- |
| `ID`             | Unique agreement-acceptance identifier  |
| `USER_NAME`      | Username associated with the acceptance |
| `TYPE`           | Agreement type accepted                 |
| `VERSION`        | Agreement version accepted              |
| `REMOTE_ADDRESS` | Client IP address                       |
| `USER_AGENT`     | Browser or client user agent            |
| `AGREED_TIME`    | Acceptance timestamp                    |

For self and loved-one participant agreement acceptance:

```text
TYPE = VOL
```

or the equivalent configured participant-agreement type.

The audit type alone does not distinguish:

- Self agreement presentation
- Loved-one agreement presentation
- Child loved-one context
- Adult loved-one context

If that distinction must be reconstructed, it must come from the registration or loved-one
relationship context rather than from a separate agreement type.

`USER_AGREEMENT_AUDIT.USER_NAME` is account-specific:

- Self signup writes the self account's username.
- Signup for a loved one writes two audit rows: one with the owning account's username and one with
  the generated loved-one username.
- Add Loved One writes one audit row with the newly generated loved-one username; it does not write a
  new owner row through that endpoint.
- Login-time re-agreement overwrites any client-supplied username with the authenticated security
  principal's username. Re-agreement in loved-one context therefore writes the represented
  loved-one account's generated username.

These rules identify the account to which acceptance is attributed. They do not record the rendered
agreement wording or child-versus-adult presentation variant.

## Agreement-version enforcement at login

At login, the application compares:

```text
Current USER_AGREEMENT.TYPE and VERSION
```

with:

```text
USER_AGREEMENT_AUDIT records associated with the user
```

If the user does not have an audit record for the current version of the applicable agreement type,
the user must review and accept the current agreement before continuing.

When the user accepts:

1. The application creates a `USER_AGREEMENT_AUDIT` record.
1. The record contains the current agreement type and version.
1. The record captures the remote address, user agent, and acceptance time.
1. The user may continue into the application.

When the workflow indicates that the account has loved ones, the application presents the common
represented-loved-one acknowledgment while retaining the participant agreement type for audit
storage. It does not select separate child or adult clauses.

## Declining an updated agreement

### Participant or volunteer

If a participant declines an updated agreement:

1. The frontend displays a confirmation popup.
1. The popup does not allow the user to choose a target account.
1. On confirmation, the frontend submits the current agreement-interruption `userId` and the
   backend-supplied `DECLINED_USER_AGREEMENT` deactivation reason to the participant-deactivation
   endpoint.
1. The affected account is therefore the account represented by the authenticated context that
   failed the agreement-version check.

The result depends on context:

- **Owning-account context:** the submitted target is the owner. Backend owner deactivation cascades
  to all enabled loved-one accounts.
- **Loved-one context:** the submitted target is the represented loved-one account. Only that
  loved-one account is deactivated; the owner and sibling loved-one accounts remain enabled.

After individual loved-one deactivation, the backend selects an appropriate related login context,
ordinarily the owning account.

The ordinary Account Settings deactivation page is a separate workflow. It may display related
accounts for selection, but the agreement-decline confirmation does not.

Agreement decline uses the ordinary account-deactivation notification:

- Owner-context decline sends the owner the standard deactivation email and identifies enabled
  dependent accounts affected by the cascade.
- Loved-one-context decline sends the owner the standard deactivation email for the individually
  deactivated loved-one account.
- There is no separate agreement-decline email method or template in the reviewed path.

The decline is persisted in `USER_DEACTIVATION` with reason `DECLINED_USER_AGREEMENT`. It does not
create a successful `USER_AGREEMENT_AUDIT` row or a distinct agreement-decline audit row. Previous
agreement-acceptance records remain historical.

### Study team member

If a study team member declines:

- The account is not deactivated through the participant endpoint.
- The user is logged out or removed from the application workflow.
- Institutional SAML authentication does not bypass the agreement requirement.

## Account activation

After successful registration and required agreement processing:

1. The application generates an expiring Java UUID token.
1. The application sends an activation email to the communication address.
1. The owner follows the activation link.
1. The application validates the token and expiration.
1. The applicable account becomes active.

## Where did you learn about us?

Registration requires one selection from institution-configured lookup values.

The value:

- Is used as registration and acquisition information
- Is not used in matching
- Is not displayed to study teams

## Loved-one account ownership

One owning account may manage multiple loved-one accounts.

Ownership is stored through:

```text
LOVED_ONE
```

The owner changes participant context rather than authenticating separately as the loved one.

Actions performed in loved-one context apply to the represented participant, including:

- Profile changes
- Study interests
- Matching
- Expressions of interest
- Questionnaire responses
- Messages
- Visibility

## Relationship validation

The relationship type is stored in:

```text
LOVED_ONE.RELATIONSHIP
```

Child-versus-adult relationship selection is validated against date of birth.

A child relationship cannot be created when the date of birth indicates an adult.

An adult relationship cannot be created when the date of birth indicates a child.

## Deactivation

An owner may deactivate their self account.

Self-account deactivation cascades to owned loved-one accounts.

A loved-one account may also be deactivated individually without deactivating the owner or other
loved-one accounts.

Deactivated participants:

- Have the database authentication record's enabled flag set to false
- Receive a `USER_DEACTIVATION` row containing user ID, deactivation time, and reason
- Are removed immediately from the process-local active-participant store handling the request
- Trigger asynchronous removal of system recommendation data from Redis
- Cannot continue ordinary participant actions
- Are hidden from study teams

For participant deactivation, Redis cleanup removes the participant from each active study's
study-facing recommendation sets and removes the participant's `SYSTEM` participant-facing
recommendation set. This cleanup is asynchronous and is not part of a single atomic transaction with
the database and in-memory changes.

## Age-out behavior

A scheduled job handles child loved-one age-out.

Before the represented person turns 18:

- The owning account receives an age-out or deactivation notice.

When the child reaches the age threshold:

- The loved-one account is deactivated.
- Proxy access through the owning account ends.
- The account is removed from active in-memory matching data.
- The represented person cannot assume control of the existing loved-one account.

The exact warning interval, execution time, and deactivation-reason value remain to be documented.

## Messages and communications

Messages belong to the represented participant account.

Message templates use the represented participant's name.

Email notifications are delivered to the owning account's communication address.

## EHR boundary

Registration and profile data are entered into the branded YourHealthResearch.org application
instance.

The application does not retrieve participant data from an electronic health record.

## Agreement acceptance records

Current agreement acceptance is determined by username, agreement type, and
current agreement version.

The backend supports exactly two agreement types:

```text
VOL
STM
```

Users with the application-wide `VOLUNTEER` role use `VOL`; other supported
authenticated users use `STM`.

An acceptance record stores username, type, version, agreement time, remote
address, and user agent. It does not identify represented loved-one context,
child-versus-adult relationship, rendered wording, or presentation variant.

`USER_AGREEMENT_AUDIT` alone therefore cannot prove whether the common represented-loved-one
acknowledgment was displayed.

Acceptance submitted through the authenticated agreement endpoint is
attributed to the authenticated security principal's username.

## Current-version enforcement

The application requires an acceptance for the current version of the
role-appropriate agreement type. Previous-version records remain historical
but do not satisfy the current-version check.

A user without current acceptance may access only the endpoints needed to
submit acceptance, submit participant deactivation, and retrieve a CSRF token.

## Agreement decline and reactivation

The backend does not persist a separate declined-agreement audit record.
Decline is represented through participant-account deactivation.

Deactivating an owning account deactivates its enabled loved-one accounts.
Deactivating one loved-one account does not deactivate the owner or siblings.

Reactivation does not itself record agreement acceptance. After reactivation,
the current-version agreement filter blocks ordinary use until acceptance.

Reactivating a loved-one account also reactivates an inactive owner.
Reactivating an owner does not automatically reactivate loved-one accounts.

A child loved-one account deactivated because the represented person reached
the configured maturity age cannot be reactivated.

## Child loved-one warning and age-out

`childAccountDeactivationJob` handles warnings and age-out. Mature age, warning
interval, and the persisted cron schedule are configurable.

For each active child loved-one account:

1. The application determines age from date of birth.
1. A warning may be sent during the configured pre-age-out interval.
1. The warning is recorded in `CHILD_DEACTIVATION_NOTICE`.
1. The same parent, child, and recorded birth-date value are not warned again.
1. On or after the maturity threshold, the account is deactivated with reason
   `CHILD_TURNED_ADULT`.
1. Deactivation writes `USER_DEACTIVATION`, disables the loved-one account, removes it from the local
   active-participant store, and initiates asynchronous Redis recommendation cleanup.
1. The owning account remains active and receives a deactivation notification when available.
1. No distinct age-out PHI-audit event is created by the reviewed age-out path; the durable lifecycle
   evidence is the deactivation row, while the earlier warning is recorded separately in
   `CHILD_DEACTIVATION_NOTICE`.

A changed date of birth may permit another warning because the recorded value
is part of duplicate detection.

The job is interruptible between child accounts. An interruption may leave
part of the collection unprocessed until a later run.

The former child loved-one account cannot be reactivated or transferred to the
represented adult. Future participation requires the supported self-account or
support workflow.

## Related pages

- [Participants](participants.md)
- [Participant Account and Consent Model](../07-data-model/participant-account-consent-model.md)
- [Messaging](../06-recruitment/messaging.md)
- [Open Questions](../09-decisions/open-questions.md)
