---
title: Users and Access
summary: Participant accounts, represented participants, institutional authentication, roles, and study authorization.
status: authoritative
---

# Users and Access

The application supports participant accounts and institutionally authenticated users.

## Participants

Participants use local, database-backed accounts.

Participant accounts may represent:

- The account owner
- A child loved one
- An adult loved one

One account owner may manage multiple loved-one participant accounts.

Participant accounts normally have the application-wide role:

```text
VOLUNTEER
```

## Institutional users

Study team members, PIs, study importers, and administrators authenticate using institutional SAML.

Institutional authentication does not grant access to every study.

## Application-wide roles

| Role             | General purpose                        |
| ---------------- | -------------------------------------- |
| `VOLUNTEER`      | Participant access                     |
| `STAFF`          | Institutional study-team access        |
| `STUDY_IMPORTER` | Institutional CSV-import access        |
| `ADMIN`          | Application-wide administrative access |

## Study-association roles

Study-specific authorization uses:

```text
PRINCIPAL_INVESTIGATOR
STUDY_TEAM_MEMBER
```

A `STAFF` role alone does not grant access to an individual study.

The user must also have a study association unless broader administrative access applies.

## Read next

- [Participants](participants.md)
- [Participant Registration, Consent, and Loved-One Accounts](participant-registration-consent-and-loved-ones.md)
- [Institutional Users](institutional-users.md)
- [Study Membership](study-membership.md)
- [Study-Team Invitations](invitations.md)
