---
title: Institutional Users and Roles
summary: SAML authentication, agreement enforcement, application-wide roles, study roles, and PI governance.
status: authoritative
relevant_when:
  - explaining_roles
  - troubleshooting_staff_access
  - troubleshooting_pi_access
  - explaining_saml_accounts
  - analyzing_first_time_study_authors
canonical_for:
  - institutional_user_identity
  - first_time_institutional_user
---

# Institutional Users and Roles

Institutional users authenticate through an institution's SAML identity
provider.

Institutional identity authentication and application authorization are
separate:

```text
Authentication:
Who is the institutional user?

Authorization:
What may the user do, and which studies may the user access?
```

Acceptance of the current study-team agreement is an additional access
condition.

## Agreement-version enforcement

The current study-team agreement type and version are stored in:

```text
USER_AGREEMENT
```

A study team member's accepted versions are stored in:

```text
USER_AGREEMENT_AUDIT
```

At login, the application checks whether the authenticated user has accepted the
current study-team agreement version, such as the agreement type:

```text
STM
```

If the current version is missing from the user's agreement audit:

- The user must review the current agreement.
- Acceptance creates a new audit record for the current type and version.
- Declining prevents the user from entering or continuing through application
  features.
- The user is returned to the appropriate landing or exit page.

Successful SAML authentication does not bypass this agreement requirement.

## First institutional login without an `APP_USER`

An institutional user may authenticate successfully through SAML before the
application has created an `APP_USER` record for that person.

This occurs when the person has never:

- Successfully created a study posting
- Been associated with a study through `STUDY_TEAM_MEMBER`
- Been created as a PI through imported-governance reconciliation
- Otherwise received an application user through an authorized workflow

A successful login by such a person may create a `LOGIN_AUDIT` record with:

```text
LOGIN_AUDIT.USER_NAME = authenticated SAML username
LOGIN_AUDIT.USER_ID = 0
```

`LOGIN_AUDIT.USER_ID = 0` does not identify an `APP_USER` row.

It records that the institutional username authenticated successfully while no
corresponding application user existed.

SAML authentication alone therefore:

- Does not require that an `APP_USER` already exist
- Does not create access to every study
- Does not create an operational study membership

## Creation of an application user during posting creation

When an institutional user who does not yet have an `APP_USER` successfully
completes study-posting creation:

1. The application creates an `APP_USER` for the authenticated institutional
   username.
2. The application creates the operational study posting.
3. The application associates the creator with the new study.
4. A non-PI creator receives `STUDY_TEAM_MEMBER`.
5. A creator who is the current imported PI receives
   `PRINCIPAL_INVESTIGATOR`.

After the `APP_USER` is created, later login-audit records can reference the
application user identifier.

An abandoned or failed posting attempt does not by itself establish that an
`APP_USER` or study membership was created.

See [Study Posting Creation](../05-study-management/posting-creation.md).

## Analytical implication

Current existence in `APP_USER` is not a reliable historical indicator that the
user existed during an earlier posting attempt.

For example:

1. A new institutional user authenticates and makes two unsuccessful posting
   attempts.
2. No `APP_USER` exists at that time.
3. The same user later completes a posting successfully.
4. The application creates the `APP_USER`.
5. A later report that joins old attempts to the current `APP_USER` table finds
   the user for all earlier attempts.

A current `APP_USER` existence field is therefore suitable only as an
extract-time sanity check.

## Application-wide roles

The application has four application-wide roles:

```text
ADMIN
STUDY_IMPORTER
STAFF
VOLUNTEER
```

These roles control broad application capabilities.

They are different from study-association roles.

## `ADMIN`

`ADMIN` is an application-wide superuser role.

An administrator can:

- Access all studies
- Access all participant data
- Activate participant accounts
- Reactivate participant accounts
- Deactivate participant accounts
- Reset participant passwords
- Access administrative scheduled-job controls

The detailed capabilities and safeguards of scheduled-job administration remain
to be documented.

Administrators cannot directly create study memberships through ordinary
application UIs.

Administrators cannot impersonate another application user.

Authorized backend personnel can technically alter study dates, publishability,
or memberships outside normal application workflows. The approval and audit
process for those interventions remains unresolved.

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

The `STAFF` role alone does not grant access to an individual study.

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

Participants use local database-backed accounts rather than institutional SAML
authentication.

## Study-association roles

Study associations use:

```text
PRINCIPAL_INVESTIGATOR
STUDY_TEAM_MEMBER
```

These roles apply only within a specific study.

Under the current implementation, both roles have equivalent access to study
data.

Both may:

- Review permitted participant information
- Review interested participants
- Export permitted participant and questionnaire data
- Invite another institutional user to the study
- Remove an ordinary `STUDY_TEAM_MEMBER`

The distinction determines:

- How the user became associated with the study
- Whether the membership may be removed through ordinary workflows

## Institutional roles

The institutional source may contain study roles such as:

- PI
- Study coordinator
- Co-investigator
- Research staff
- Administrative staff
- Other institution-defined roles

Institutional roles are stored separately from application study roles.

Only the current imported PI role automatically creates application study
access.

An imported non-PI role does not automatically create a `STUDY_TEAM_MEMBER`
membership.

A non-PI institutional user receives operational membership by:

- Successfully creating the posting, or
- Accepting a study-team invitation

## Current PI

Each valid imported study has one current institutional PI.

The PI is controlled by the institutional source of truth.

The current imported PI:

- Is associated with the operational study as `PRINCIPAL_INVESTIGATOR`
- Cannot be removed through ordinary application UIs
- Cannot be appointed through an ordinary study-team invitation
- Must have imported email and `USER_NAME` information
- Must have a `USER_NAME` corresponding to the institutional SAML ePPN value

## PI application-user creation

A PI may receive an `APP_USER` before ever logging in.

If no PI `APP_USER` exists:

1. The application creates one from imported identity data.
2. The application associates the user as `PRINCIPAL_INVESTIGATOR`.
3. The PI can later authenticate through SAML.
4. The SAML ePPN value must resolve to the pre-created application user.

## Existing PI identity information

When the PI's `APP_USER` already exists:

- The existing record is reused.
- Later imported changes to the PI's name or email are not copied into the
  existing record under current behavior.

## PI changes

When the imported current PI changes:

1. The former PI's operational `PRINCIPAL_INVESTIGATOR` membership is removed.
2. The new PI's `APP_USER` is found or created.
3. The new PI is associated with the study as `PRINCIPAL_INVESTIGATOR`.
4. The new current PI cannot be removed through ordinary application UIs.

A former PI does not retain study access solely through the former PI
membership.

A distinct ordinary study-team membership, if one exists through another valid
workflow, is evaluated separately.

## Administrator auditing

Administrator access to participant profiles is audited.

Export actions, including administrator exports, are not separately audited.

## Institutional account lifecycle

Institutional identities are managed by institutional identity providers.

The application does not deactivate or delete the institutional identity.

Removing an ordinary study membership removes access to that study but does not
deactivate the institutional account.

The current imported PI's membership cannot be removed through the ordinary UI,
but it is replaced through institutional reconciliation when the source-of-truth
PI changes.

## Related pages

- [Study Posting Creation](../05-study-management/posting-creation.md)
- [Study Membership](study-membership.md)
- [Study-Team Invitations](invitations.md)
- [Governance Reconciliation](../03-institutional-governance/reconciliation.md)
- [Data Ownership](../02-architecture/data-ownership.md)
- [Open Questions](../09-decisions/open-questions.md)
