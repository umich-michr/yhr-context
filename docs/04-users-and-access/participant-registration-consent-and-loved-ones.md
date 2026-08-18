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

The signup-for-a-loved-one flow and Add Loved One both create a separate
loved-one account managed by the owning account.

The phrase “loved-one-first account” must not be treated as a separate account
type. It describes only the registration path through which the owning and
loved-one accounts are established.

## Self signup

When registering for self, the person completes the required participant
profile fields for the self account.

The signup form asks:

```text
MY PROFILE IS VISIBLE TO
```

The available choices are:

```text
All study teams using the branded application instance
```

with explanatory text indicating that study teams may contact the participant
about studies when the profile appears to be a good fit, or:

```text
Only the study teams whose studies I show interest in
```

The selected value becomes the self profile's visibility setting.

## Signup for a loved one

Signup for a loved one creates two accounts:

1. A minimal owning account
2. A complete loved-one participant account

This does not mean that the owning account is a special kind of loved-one
account. It is an ordinary participant account created with only the information
needed to authenticate and manage the represented loved one.

### Minimal owning account

The owning account is created so the owner can authenticate and manage the
loved-one account.

The signup flow collects the following owner information:

- Communication email
- First name
- Last name

The owner's communication email is also the owning account's username.

Country and ZIP code entered for the loved-one profile are copied to the owning
account during this signup flow.

Other required participant-profile fields are not collected for the owning
account during this flow. The owning profile is therefore incomplete for
ordinary self participation.

The minimal owning profile defaults to hidden from study teams.

The copied country and ZIP values are confirmed signup behavior. They must not
be described as remaining automatically synchronized with later loved-one
profile changes unless that behavior is separately verified.

### Loved-one account

The loved-one account has:

- A separate user record
- A separate participant profile
- Required loved-one profile fields
- Its own visibility setting selected during signup
- An application-generated GUID-based email-like username
- The owning account's real email address for communication

The generated loved-one username is an internal authentication identity. It is
not the loved one's communication email address.

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

| Column | Meaning |
|---|---|
| `ID` | Unique agreement-definition identifier |
| `TYPE` | Agreement type |
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

Self participation and loved-one participation use the same participant
agreement type and version for agreement-audit purposes.

Conceptually:

```text
Self registration:
    Participant agreement type = VOL

Loved-one registration or management:
    Participant agreement type = VOL
    + Additional loved-one or proxy clauses in the presented agreement
```

The loved-one presentation includes additional clauses explaining the owner's
agreement and responsibilities when acting for the represented loved one.

Those additional clauses do not create a separate agreement type in
`USER_AGREEMENT` or `USER_AGREEMENT_AUDIT`.

Therefore, documentation must not describe the database as containing separate
participant agreement types such as:

```text
SELF
CHILD_LOVED_ONE
ADULT_LOVED_ONE
```

unless a future schema or configuration change introduces those values.

Child and adult loved-one relationships may affect the wording or applicability
of presented clauses, but agreement acceptance is captured under the same
participant agreement type.

## Agreement acceptance audit

Successful acceptance is recorded in:

```text
USER_AGREEMENT_AUDIT
```

The record contains:

| Column | Meaning |
|---|---|
| `ID` | Unique agreement-acceptance identifier |
| `USER_NAME` | Username associated with the acceptance |
| `TYPE` | Agreement type accepted |
| `VERSION` | Agreement version accepted |
| `REMOTE_ADDRESS` | Client IP address |
| `USER_AGENT` | Browser or client user agent |
| `AGREED_TIME` | Acceptance timestamp |

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

If that distinction must be reconstructed, it must come from the registration
or loved-one relationship context rather than from a separate agreement type.

The exact username written to `USER_AGREEMENT_AUDIT.USER_NAME` during each
loved-one creation and re-agreement scenario remains to be verified from the
implementation.

## Agreement-version enforcement at login

At login, the application compares:

```text
Current USER_AGREEMENT.TYPE and VERSION
```

with:

```text
USER_AGREEMENT_AUDIT records associated with the user
```

If the user does not have an audit record for the current version of the
applicable agreement type, the user must review and accept the current
agreement before continuing.

When the user accepts:

1. The application creates a `USER_AGREEMENT_AUDIT` record.
2. The record contains the current agreement type and version.
3. The record captures the remote address, user agent, and acceptance time.
4. The user may continue into the application.

For an owner who manages loved-one accounts, the application presents the
applicable loved-one or proxy clauses when the current workflow requires them,
while retaining the participant agreement type for audit storage.

## Declining an updated agreement

### Participant or volunteer

If a participant declines:

1. The application warns that the account will be deactivated.
2. The participant is asked to confirm the decision.
3. If the participant does not confirm, the deactivation is not completed.
4. If confirmed, the applicable participant account is deactivated.
5. If the deactivated account is an owning self account, its loved-one accounts
   are also deactivated.

The exact affected account when an owner declines while operating in a
loved-one context remains to be verified.

### Study team member

If a study team member declines:

- The study team member cannot continue using application features.
- The user is removed from the application workflow and returned to the
  appropriate landing or exit page.
- SAML authentication by itself does not bypass the agreement requirement.
- Declining does not deactivate the institutionally managed SAML identity.

## Account activation

After successful registration and required agreement processing:

1. The application generates an expiring Java UUID token.
2. The application sends an activation email to the communication address.
3. The owner follows the activation link.
4. The application validates the token and expiration.
5. The applicable account becomes active.

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

The owner changes participant context rather than authenticating separately as
the loved one.

Actions performed in loved-one context apply to the represented participant,
including:

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

A child relationship cannot be created when the date of birth indicates an
adult.

An adult relationship cannot be created when the date of birth indicates a
child.

## Deactivation

An owner may deactivate their self account.

Self-account deactivation cascades to owned loved-one accounts.

A loved-one account may also be deactivated individually without deactivating
the owner or other loved-one accounts.

Deactivated participants:

- Are removed from active matching
- Are removed from the active in-memory participant collection
- Cannot continue ordinary participant actions
- Are hidden from study teams

## Age-out behavior

A scheduled job handles child loved-one age-out.

Before the represented person turns 18:

- The owning account receives an age-out or deactivation notice.

When the child reaches the age threshold:

- The loved-one account is deactivated.
- Proxy access through the owning account ends.
- The account is removed from active in-memory matching data.
- The represented person cannot assume control of the existing loved-one
  account.

The exact warning interval, execution time, and deactivation-reason value remain
to be documented.

## Messages and communications

Messages belong to the represented participant account.

Message templates use the represented participant's name.

Email notifications are delivered to the owning account's communication
address.

## EHR boundary

Registration and profile data are entered into the branded
YourHealthResearch.org application instance.

The application does not retrieve participant data from an electronic health
record.

## Related pages

- [Participants](participants.md)
- [Participant Account and Consent Model](../07-data-model/participant-account-consent-model.md)
- [Messaging](../06-recruitment/messaging.md)
- [Open Questions](../09-decisions/open-questions.md)
