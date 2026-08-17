---
title: Users and Access
summary: Participant accounts, institutional authentication, and study-scoped authorization.
status: authoritative
---

# Users and Access

The application supports two broad identity models.

## Participants

Participants use local database-backed accounts with email addresses as usernames.

## Institutional users

Study team members and PIs authenticate using institutional SAML.

Authentication does not grant universal study access. Authorization is study-scoped and membership-based.

## Application User Roles

Participants => VOLUNTEER
Institutional Users => STAFF, ADMIN, STUDY_IMPORTER
Any user who is either PI or study team member for a study by default is STAFF if not more privileges are required.

## Application study roles

```text
PRINCIPAL_INVESTIGATOR
STUDY_TEAM_MEMBER
```

Read:

- [Participants](participants.md)
- [Institutional users](institutional-users.md)
- [Study membership](study-membership.md)
- [Invitations](invitations.md)
