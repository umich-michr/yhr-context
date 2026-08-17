---
title: Users and Access
summary: Participant accounts, institutional authentication, application-wide roles, and study-scoped authorization.
status: authoritative
---

# Users and Access

The application supports two broad identity models.

## Participants

Participants use local database-backed accounts with email addresses as usernames.

Participants normally have the application-wide role:

```text
VOLUNTEER
```

## Institutional users

Study team members, PIs, study importers, and administrators authenticate using institutional SAML.

Institutional authentication does not grant universal study access.

## Application-wide roles

| Role | General purpose |
|---|---|
| `VOLUNTEER` | Participant access |
| `STAFF` | Institutional study-team access |
| `STUDY_IMPORTER` | Institutional CSV-import access |
| `ADMIN` | Application-wide administrative access |

A study team member or PI normally has the application-wide role `STAFF`.

Broader application roles, such as `ADMIN`, may grant additional application capabilities.

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
- [Institutional users](institutional-users.md)
- [Study membership](study-membership.md)
- [Invitations](invitations.md)