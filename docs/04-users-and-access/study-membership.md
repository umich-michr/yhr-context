---
title: Study Membership
summary: Study-specific authorization, equivalent study roles, permissions, membership sources, PI replacement, and removal.
status: authoritative
canonical_for:
  - study_membership
  - study_team_permissions
  - membership_removal
relevant_when:
  - explaining_study_authorization
  - adding_or_removing_study_members
  - troubleshooting_study_access
  - distinguishing_pi_and_team_member_roles
---

# Study Membership

A study membership associates an institutional `APP_USER` with an operational
study.

A valid institutional SAML login does not grant access to every study.

The user must also have accepted the current study-team agreement.

## Study-association roles

Study memberships use:

```text
PRINCIPAL_INVESTIGATOR
STUDY_TEAM_MEMBER
```

These roles are separate from application-wide roles.

## Membership sources

| Source | Study role |
|---|---|
| Current imported PI assignment | `PRINCIPAL_INVESTIGATOR` |
| Posting creator who is not the imported PI | `STUDY_TEAM_MEMBER` |
| Accepted invitation | `STUDY_TEAM_MEMBER` |
| Authorized backend intervention | Depends on the intervention |

## Equivalent study permissions

Under the current implementation, `PRINCIPAL_INVESTIGATOR` and
`STUDY_TEAM_MEMBER` have equivalent study-data permissions.

An associated study member may:

- Edit study information
- Edit eligibility criteria while permitted by study status
- Edit screening questions while the study is inactive
- Activate or deactivate the study
- Archive or unarchive an eligible study
- Review matched participants
- Review interested participants
- Move interested participants between workflow lists
- Create and apply labels
- Initiate and participate in conversations with interested participants
- Review questionnaire answers
- Export permitted participant data
- Invite another institutional user
- Remove an ordinary `STUDY_TEAM_MEMBER`
- Configure applicable email-notification settings

## Messaging restriction

Study membership alone does not permit messaging every participant.

Study members may message only interested participants.

A matched participant cannot be directly messaged before interest.

See [Messaging](../06-recruitment/messaging.md).

## Current PI membership

The current PI membership:

- Originates from imported institutional data
- Is created and maintained through reconciliation
- Cannot be granted through an ordinary invitation
- Cannot be removed through ordinary application UIs
- Is replaced when the institutional source identifies a new current PI

## PI changes

When the imported PI changes:

1. The former PI's operational `PRINCIPAL_INVESTIGATOR` membership is removed.
2. The new PI receives a `PRINCIPAL_INVESTIGATOR` membership.
3. The new PI becomes the current non-removable PI in ordinary application
   workflows.

The former PI does not retain access solely because they were previously PI.

If the former PI has a distinct `STUDY_TEAM_MEMBER` relationship established
through another supported workflow, that separate membership is not the former
PI relationship and must be evaluated independently.

## Removability

| Membership | Removable through ordinary UI? |
|---|---:|
| Current imported PI | No |
| Non-PI posting creator | Yes |
| Invited study team member | Yes |
| Former PI membership after imported PI change | Removed by reconciliation |

## Removing ordinary members

Removing a study membership:

- Removes access to the study
- Removes that member's study-notification settings
- Does not deactivate or delete the institutional account
- Does not delete shared study conversations or messages previously sent

## General authorization

For a non-administrator:

```text
Can access study =
    institutional user is authenticated
    AND current study-team agreement is accepted
    AND APP_USER exists
    AND a study membership exists
    AND the membership references the requested study
```

Current matched-participant access additionally requires an active study.

Historical interested-participant access may remain available when the study is
inactive by date, provided:

- `PUBLISHABLE = 1`
- The participant account is active
- The requested operation remains permitted

When `PUBLISHABLE = 0`, study members cannot access participant information or
conversations.

## Administrators

Administrators have application-wide access without ordinary study membership.

Administrators cannot create study memberships through ordinary application
UIs.

## Related pages

- [Institutional Users](institutional-users.md)
- [Study-Team Invitations](invitations.md)
- [Governance Reconciliation](../03-institutional-governance/reconciliation.md)
- [Interested-Participant Management](../06-recruitment/interested-participant-management.md)
- [Messaging](../06-recruitment/messaging.md)
- [Study Notifications](../05-study-management/study-notifications.md)
