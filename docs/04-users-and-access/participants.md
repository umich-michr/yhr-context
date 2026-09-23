---
title: Participants
summary: Participant accounts, profiles, visibility, lifecycle, agreements, and loved-one management.
status: authoritative
relevant_when:
  - answering_participant_account_questions
  - explaining_profile_data
  - explaining_visibility
  - explaining_account_lifecycle
---

# Participants

Participants use local, database-backed accounts with the application-wide role:

```text
VOLUNTEER
```

## Participant identity

A participant account represents one participant profile.

An account may represent:

- The account owner
- A child loved one
- An adult loved one

One account owner may manage multiple loved-one participant accounts.

See
[Participant Registration, Agreements, and Loved-One Accounts](participant-registration-consent-and-loved-ones.md).

## Profile data

Participant profiles may contain:

- Date of birth
- Derived age
- Biological sex assigned at birth
- Gender identity
- Race and ethnicity
- Smoking status
- Current medical conditions
- Past medical conditions
- Metal objects or implants
- Willingness to change medications
- Willingness to take experimental drugs
- Fluency in English
- Weight
- Height
- Pregnancy
- Parent or guardian status
- Contact information
- Primary location
- Study interests
- Profile visibility

Not every profile property is used by matching.

## Visibility selection

During signup, the participant or account owner selects one of two visibility options. The selection
may later be changed.

Visibility affects study-facing matching and disclosure to study teams. It does not change the
underlying eligibility result or prevent participant-facing study recommendations.

### All study teams

The participant permits all study teams using the branded application instance to view the profile
when the participant appears to be a suitable match.

This setting allows the participant to participate in pre-interest study-facing matching. When the
applicable study-facing requirements are satisfied, the participant may appear in the study's
Matched Participants list, where authorized study-team members may access the available participant
information.

### Only study teams whose studies receive interest

The participant permits profile visibility only after successfully expressing interest in the
applicable study.

Before interest:

- The participant is ignored by pre-interest study-side matching.
- The participant does not appear in the study's Matched Participants list.
- Study-team members cannot access the participant through the matched-participant workflow.
- Participant-facing matching still runs.
- An otherwise qualifying study may appear in the participant's My Studies.

After the participant successfully expresses interest:

- The participant appears in the applicable study's Interested Participants workflow.
- Authorized members of that study team may access the participant information available through the
  interested-participant workflow.
- The participant remains hidden from unrelated study teams.

Access after interest results from the participant's interest relationship with the applicable
study. It does not change the participant's visibility selection.

For the canonical matching rules, see
[Matching and Visibility](../06-recruitment/matching-and-visibility.md).

## Minimal owning profile

When a person signs up for a loved one, the application creates a minimal owning account in addition
to the loved-one account.

The owning account contains:

- Username and communication email
- First name
- Last name
- Country copied from the loved-one signup data
- ZIP code copied from the loved-one signup data

Other participant-profile fields remain incomplete because the flow collects the required profile
data for the loved one rather than the owner.

The minimal owning profile defaults to hidden from study teams.

If the owner later wants to participate personally, the owner must complete the applicable self
profile and choose the desired visibility setting.

## Study interests

Participants may limit participant-facing recommendations by:

- Topics or conditions
- Locations
- Compensation
- Healthy-participant preference
- Other supported study properties

Only exact eligibility matches are shown as ordinary participant-facing matched studies.

## My Studies and history

Participants may use My Studies to view:

- System-matched studies
- Study-team-promoted studies
- Interested studies

Participants may mark a recommended study Not Interested. This creates a participant-side Redis
exclusion.

Participant history may show:

- Studies in which interest was expressed
- Studies dismissed as Not Interested

## Temporal profile properties

The show-interest form refreshes only:

- Past medical conditions
- Present medical conditions
- Parent or guardian of a child under 18

This limited review avoids requiring the participant to update the complete profile whenever they
express interest.

The persistent participant profile and its in-memory matching representation must remain
synchronized after these updates.

## Agreement updates

At login, the application checks whether the user has accepted the current version of the applicable
agreement.

If the current agreement version has not been accepted:

- The user must review the agreement.
- Acceptance creates a `USER_AGREEMENT_AUDIT` record for the current type and version.
- A participant who declines is warned that the account will be deactivated.
- Confirmed decline deactivates the account.
- Decline by an owning self account cascades deactivation to its loved-one accounts.

## Deactivation

Participants may deactivate their own accounts.

Deactivation:

- Removes the participant from active matching
- Removes the participant from active in-memory matching data
- Hides the profile from study teams
- Hides historical conversations from study teams
- Blocks new participant actions
- Retains historical expressions of interest

Deactivating an owning self account also deactivates its loved-one accounts.

A loved-one account may be deactivated individually without deactivating the owner or other
loved-one accounts.

## Age-based loved-one deactivation

A scheduled job deactivates a child loved-one account when the represented person turns 18.

The owner receives notice before the age-based deactivation.

The deactivation:

- Ends proxy access to that loved-one account
- Removes the participant from active in-memory matching data
- Removes the participant from active matching
- Does not transfer control of the existing account to the represented person

## Reactivation

Participants request reactivation through support.

Administrators reactivate accounts through participant-administration functions.

Reactivation of cascaded owner and loved-one accounts must follow the supported administrative
workflow rather than being inferred from account ownership alone.

## Hard deletion

Hard deletion requires an explicit support request and administrator confirmation.

It removes participant data, including:

- Account
- Profile
- Preferences
- Matches
- Expressions of interest
- Questionnaire data
- Messages and other participant-linked data
- Participant-linked application audit data

The application retains the internal participant ID and deletion reason.

Previously downloaded CSV files cannot be recalled.

## Related pages

- [Participant Registration, Agreements, and Loved-One Accounts](participant-registration-consent-and-loved-ones.md)
- [Matching and Visibility](../06-recruitment/matching-and-visibility.md)
- [Expressions of Interest](../06-recruitment/expressions-of-interest.md)
- [Messaging](../06-recruitment/messaging.md)
