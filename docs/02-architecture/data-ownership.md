---
title: Data Ownership and Authority
summary: Identifies which system owns each category of data.
status: authoritative
---

# Data Ownership and Authority

## Ownership matrix

| Data | Authoritative owner | Locally editable? |
|---|---|---:|
| Imported study identifier | Institutional source | No |
| Imported study description | Institutional source | No |
| Institutional study role | Institutional source | No |
| Current PI assignment | Institutional source | No |
| Imported PI username/ePPN | Institutional source | No |
| Imported PI identity details | Institutional source | No |
| Publishability | Institutionally governed process | No through ordinary UI |
| Participant-facing study content | Application study team | Yes |
| Study eligibility criteria | Application study team | Yes |
| Study activation and deactivation dates | Application study team; backend administrator override is possible | Yes |
| `PRINCIPAL_INVESTIGATOR` association | Derived from imported PI data | No through ordinary UI |
| `STUDY_TEAM_MEMBER` association | Application study team | Yes |
| Participant account | Participant and supported administrative workflows | Yes |
| Participant profile | Participant | Yes |
| Participant visibility preference | Participant | Yes |
| Expression of interest | Participant action | Cannot be withdrawn |
| Questionnaire structure | Study team while study is inactive | Limited |
| Questionnaire answers | Participant | Cannot be edited after submission |

## Imported identity and `APP_USER`

An imported PI may receive an `APP_USER` before first login.

When no `APP_USER` exists, the application creates one using imported values including:

- ePPN or institutional identifier
- First name
- Middle name, when available
- Last name
- Email

A PI record missing email or ePPN is treated as an application error.

When an `APP_USER` already exists, later imported name or email changes are not copied under the current implementation.

## SAML identity resolution

When a pre-created PI later authenticates, the SAML identity must resolve to the existing `APP_USER`.

The ePPN or another institutionally stable identifier should be used for this resolution. Email should not be the sole identity key because it can change.

## Application-wide roles versus study roles

Application-wide roles:

```text
ADMIN
STUDY_IMPORTER
STAFF
VOLUNTEER
```

Study-association roles:

```text
PRINCIPAL_INVESTIGATOR
STUDY_TEAM_MEMBER
```

These role domains must remain distinct in documentation, code, and data modeling.

## Backend overrides

Authorized backend personnel can technically perform operations that are not exposed through application UIs, including:

- Creating a study membership
- Altering study dates
- Altering publishability

These operations are outside the normal product workflow and must not be confused with ordinary application permissions.

The approval and audit process for these interventions remains documented under [Open Questions](../09-decisions/open-questions.md).

## Related pages

- [Institutional users](../04-users-and-access/institutional-users.md)
- [Study membership](../04-users-and-access/study-membership.md)
- [Imported institutional data](../03-institutional-governance/imported-data.md)
- [Open questions](../09-decisions/open-questions.md)