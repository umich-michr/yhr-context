---
title: Participants
summary: Participant registration, account activation, profiles, visibility, and account lifecycle.
status: authoritative
relevant_when:
  - answering_participant_account_questions
  - explaining_profile_data
  - explaining_account_activation
  - explaining_account_deactivation_or_deletion
---

# Participants

Participants use local, database-backed application accounts.

Participants normally have the application-wide role:

```text
VOLUNTEER
```

Participant accounts are distinct from institutional accounts authenticated through SAML.

## Registration

A participant registers using an email address as the account username.

The application does not attempt to determine whether two participant accounts represent the same real-world person.

The database prevents two active participant accounts from using the same email
username. This does not provide person-level duplicate detection because a
person may still use more than one email address.

## Account activation

After registration:

1. The application generates a random Java UUID token.
2. The application sends an account-activation email.
3. The email contains a link with the activation token.
4. The participant follows the link.
5. The application validates the token and expiration.
6. The participant account is activated.

The activation-link expiration duration is controlled by an application setting.

## Participant profile

A participant profile may contain:

- Date of birth
- Derived age
- Gender
- Race
- Other demographic information
- Location
- Contact information
- Past medical conditions
- Present medical conditions
- Whether the participant is a parent or guardian of a child under 18
- Other study-relevant information
- Study-interest preferences
- Profile-visibility preference

If date of birth is stored, age should be derived from it when needed rather than treated as an independently permanent value.

## Study-interest preferences

Participants may specify preferences such as:

- Research topics or conditions
- Study locations
- Compensation
- Visit format
- Other study characteristics

Study interests answer:

> Is this the type of study the participant wants to see?

Study interests are separate from eligibility criteria.

Eligibility criteria answer:

> Does the participant appear to qualify for this study?

## Temporal profile properties

Some participant properties can change over time.

When a participant attempts to express interest in a study, the application asks the participant to update:

- Past medical conditions
- Present medical conditions
- Whether the participant is a parent or guardian of a child under 18

The parent-or-guardian property is collected as a Boolean radio-button response.

The updated temporal values are used during the eligibility recheck.

## Visibility modes

Participants can select one of two visibility modes:

```text
Restricted
Discoverable
```

### Restricted

A restricted participant is not visible to a study team merely because the participant matches the study.

The participant becomes visible to a study only after successfully expressing interest, subject to the study and participant remaining accessible.

### Discoverable

A discoverable participant may be visible to an authorized study team when the participant matches the study's eligibility criteria.

The study does not need to match the participant's stated interests for study-team visibility.

See [Matching and visibility](../06-recruitment/matching-and-visibility.md).

## Participant deactivation

Participants may deactivate their own accounts.

When a participant account is deactivated:

- The participant no longer participates in active matching.
- The participant is removed from current matched-participant lists.
- Historical expressions of interest remain.
- Participant profile information is hidden from study teams.
- New recruitment interactions are blocked.

## Participant reactivation

Participants request reactivation by emailing support. An administrator then
reactivates the account through the Help Participants administrative interface.

Administrators may:

- Activate participant accounts
- Reactivate participant accounts
- Deactivate participant accounts
- Reset participant passwords

## Hard deletion

Participant deletion is a hard deletion.

The participant requests deletion by emailing support. An administrator uses the
Help Participants interface, confirms the deletion, and records a reason before
the application permanently removes the participant's information.

After hard deletion:

- The deleted email address may be reused.
- The application cannot recall participant data already downloaded by study teams.
- The deletion removes the participant account, profile, preferences, match
  records, expressions of interest, questionnaire submissions, questionnaire
  responses, and application audit records.

The application retains only the internally assigned participant ID and the
deletion reason as its in-application trace. The support request itself remains
in the external ServiceNow ticket.

## Institutional accounts

Institutional accounts are managed by institutional identity providers.

Institutional users include application users with roles such as:

```text
ADMIN
STUDY_IMPORTER
STAFF
```

Institutional accounts cannot be deactivated or deleted through participant-account workflows.

## Related pages

- [Users and access](index.md)
- [Institutional users](institutional-users.md)
- [Matching and visibility](../06-recruitment/matching-and-visibility.md)
- [Expressions of interest](../06-recruitment/expressions-of-interest.md)