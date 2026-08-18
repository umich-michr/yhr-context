---
title: Institutional Users and Roles
summary: SAML-authenticated users, application-wide roles, study roles, and PI governance.
status: authoritative
relevant_when:
  - explaining_roles
  - troubleshooting_staff_access
  - troubleshooting_pi_access
  - explaining_saml_accounts
---

# Institutional Users and Roles

Institutional users authenticate through an institution's SAML identity provider.

Institutional identity authentication and study authorization are separate.

```text
Authentication:
Who is the institutional user?

Authorization:
What may the user do, and which studies may the user access?
```

## Application-wide roles

The application has four application-wide roles:

```text
ADMIN
STUDY_IMPORTER
STAFF
VOLUNTEER
```

These roles control broad application capabilities.

They are different from the study-association roles that connect a staff user to a particular study.

## `ADMIN`

`ADMIN` is an application-wide superuser role.

An administrator can:

- Access all studies
- Access all participant data
- Activate participant accounts
- Reactivate participant accounts
- Deactivate participant accounts
- Reset participant passwords

Administrators cannot directly create study memberships through application UIs.

Administrators cannot impersonate another application user. They can alter
study dates or publishability through backend operations.

A membership can be created through backend intervention, but that is outside
normal application UI behavior. Authorized staff handle these requests after
receiving confirmation from an authorized institutional contact. This backend
procedure is not currently documented in an operational runbook.

## `STUDY_IMPORTER`

`STUDY_IMPORTER` is an application-wide role used for institutional CSV imports.

A study importer can:

- Authenticate to the institutional CSV-import function
- Upload incremental data into the `IMPORTED_*` data layer
- Receive import-error reports when associated with the import token

`STUDY_IMPORTER` does not itself grant:

- Access to study data
- Access to participant data
- Membership in any study

## `STAFF`

`STAFF` is the application-wide role for institutional study personnel.

A `STAFF` user may log in through SAML.

The `STAFF` role alone does not grant access to any individual study.

To access a study, the staff user must ordinarily be associated with it as:

```text
PRINCIPAL_INVESTIGATOR
```

or:

```text
STUDY_TEAM_MEMBER
```

## `VOLUNTEER`

`VOLUNTEER` is the application-wide role used for participant accounts.

Participants use local email-based accounts rather than institutional SAML authentication.

## Study-association roles

Study associations use:

```text
PRINCIPAL_INVESTIGATOR
STUDY_TEAM_MEMBER
```

These roles apply only within a specific study.

Under the current implementation, both roles have equivalent access to study data.

Both may:

- Review permitted participant information
- Review interested participants
- Export permitted participant and questionnaire data
- Invite another institutional user to the study
- Remove an ordinary `STUDY_TEAM_MEMBER`

The distinction determines:

- How the user became associated with the study
- Whether the membership may be removed through ordinary application workflows

## Institutional roles

The institutional source may contain study roles such as:

- PI
- Study coordinator
- Co-investigator
- Other institution-defined roles

These institutional roles are stored separately from application study roles.

Only the current imported PI role automatically creates application study access.

An imported study coordinator does not automatically receive a `STUDY_TEAM_MEMBER` membership.

The coordinator must instead:

- Create the posting, or
- Accept an invitation

## Current PI

Each valid imported study has one current institutional PI.

The PI is controlled by the institutional source of truth.

The current imported PI:

- Is associated with the operational study as `PRINCIPAL_INVESTIGATOR`
- Cannot be removed through ordinary application UIs
- Cannot be appointed through an ordinary study-team invitation
- Must have imported email and `USER_NAME` information
- Must have a `USER_NAME` that corresponds to the value returned in the institutional SAML ePPN attribute

## PI application-user creation

A PI may receive an `APP_USER` before ever logging in.

If no PI `APP_USER` exists:

1. The application creates one from imported identity data.
2. The application associates the user as `PRINCIPAL_INVESTIGATOR`.
3. The PI can later authenticate through SAML.
4. The SAML identity must resolve to the pre-created application user.

## Existing PI identity information

When the PI's `APP_USER` already exists:

- The existing record is reused.
- Later imported changes to the PI's name or email are not copied into the existing record under current behavior.

## PI changes

When the imported current PI changes:

1. The new PI's `APP_USER` is found or created.
2. The new PI is associated with the study as `PRINCIPAL_INVESTIGATOR`.
3. The former PI's existing operational membership is not automatically removed.

As a result, the operational study may retain multiple `PRINCIPAL_INVESTIGATOR` memberships even though imported data identifies only one current PI.

The former PI may continue to have study access.

This is current behavior and a known access-governance concern.

## Administrator auditing

Administrator access to participant profiles is audited. Export actions,
including administrator exports, are not separately audited.

## Institutional account lifecycle

Institutional accounts are managed by institutional identity providers.

The application does not deactivate or delete institutional accounts.

However, ordinary access to an individual study may be removed by deleting the user's `STUDY_TEAM_MEMBER` membership.

The current imported PI's membership cannot be removed through the ordinary UI.

## Related pages

- [Study membership](study-membership.md)
- [Invitations](invitations.md)
- [Governance reconciliation](../03-institutional-governance/reconciliation.md)
- [Data ownership](../02-architecture/data-ownership.md)
- [Open questions](../09-decisions/open-questions.md)
