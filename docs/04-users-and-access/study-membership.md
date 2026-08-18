---
title: Study Membership
summary: Study-specific associations, role permissions, membership sources, and removal rules.
status: authoritative
relevant_when:
  - explaining_study_authorization
  - adding_or_removing_study_members
  - troubleshooting_study_access
  - distinguishing_pi_and_team_member_roles
---

# Study Membership

A study membership associates an institutional `APP_USER` with an operational study.

A valid institutional SAML login does not, by itself, grant access to every study.

## Study-association roles

Study memberships use two roles:

```text
PRINCIPAL_INVESTIGATOR
STUDY_TEAM_MEMBER
```

These are study-association roles.

They are separate from application-wide roles such as:

```text
ADMIN
STUDY_IMPORTER
STAFF
VOLUNTEER
```

## Membership sources

A user may become associated with a study through:

| Source | Study role |
|---|---|
| Current imported PI assignment | `PRINCIPAL_INVESTIGATOR` |
| Posting creator who is not the imported PI | `STUDY_TEAM_MEMBER` |
| Accepted study invitation | `STUDY_TEAM_MEMBER` |
| Backend intervention | Depends on the intervention |

Logical membership-source values may include:

```text
IMPORTED_PI
POSTING_CREATOR
INVITATION
BACKEND_ADMINISTRATION
```

The exact physical database values should be verified.

## Study-data permissions

Under the current implementation, the two study roles have equivalent access to study data.

A `PRINCIPAL_INVESTIGATOR` or `STUDY_TEAM_MEMBER` may:

- Review permitted matching participants
- Review interested participants
- Review permitted participant profile information
- Review screening-questionnaire answers
- Export permitted participant and questionnaire data
- Invite another SAML-authenticated institutional user
- Remove an ordinary `STUDY_TEAM_MEMBER`

## Removability

| Membership | Removable through application UI? |
|---|---:|
| Current imported PI | No |
| Posting creator who is not the current PI | Yes |
| Invited study team member | Yes |
| Former PI retained as `PRINCIPAL_INVESTIGATOR` after a PI change | Not automatically removed; whether the retained former-PI membership can be removed through the ordinary UI is unresolved |

A posting creator is protected from removal only when the creator is also the current institutionally identified PI.

## Current PI membership

The current PI membership:

- Is derived from imported institutional data
- Is created or maintained through reconciliation
- Cannot be granted by ordinary study team members
- Cannot be removed through ordinary application UIs

A PI correction must originate in the institution's governed source data.

## PI-change behavior

When the imported PI changes:

- The new PI is associated as `PRINCIPAL_INVESTIGATOR`.
- The former PI's existing operational membership is not automatically removed.

This can leave both the former and current PI with operational study access.

## Inviting members

Any user currently associated with the study may invite another person who has a valid institutional SAML account.

After successful invitation acceptance, the new user receives:

```text
STUDY_TEAM_MEMBER
```

See [Invitations](invitations.md).

## Removing ordinary members

Any associated study team member may remove an ordinary `STUDY_TEAM_MEMBER`.

This includes:

- A membership received through invitation
- A posting-creator membership when the creator is not the current PI

Removing a study membership does not deactivate or delete the institutional account.

It only removes access to that study.

## Administrators

`ADMIN` is an application-wide superuser role.

Administrators can access all studies and participant data without ordinary study membership.

Administrators cannot create study memberships through application UIs.

Backend database intervention may create a membership, but that is outside
normal UI behavior. Authorized staff handle these requests after an authorized
institutional contact confirms the request; no operational runbook currently
documents this procedure.

## General authorization rule

For a non-administrator:

```text
Can access study =
    institutional user is authenticated
    AND APP_USER is valid
    AND an applicable study membership exists
    AND the membership references the requested study
```

Participant-data access additionally depends on:

- Study publishability
- Whether the requested data concerns a current match or a historical expression of interest
- Participant account status
- Participant visibility mode
- Requested operation
- Data-field permissions

Current matched-participant access requires the study to be active.

Historical interested-participant access may remain available when the study is inactive by date, provided `PUBLISHABLE = 1`.

When `PUBLISHABLE = 0`, study team members cannot access participant information.

## Related pages

- [Institutional users](institutional-users.md)
- [Invitations](invitations.md)
- [Posting creation](../05-study-management/posting-creation.md)
- [Governance reconciliation](../03-institutional-governance/reconciliation.md)
- [Open questions](../09-decisions/open-questions.md)
