---
title: Data Ownership and Authority
summary: Identifies which system owns each category of data.
status: authoritative
---

# Data Ownership and Authority

## Ownership matrix

| Data                                                       | Authoritative owner                                              |                 Locally editable? |
| ---------------------------------------------------------- | ---------------------------------------------------------------- | --------------------------------: |
| Imported study identifier                                  | Institutional source                                             |                                No |
| Imported study description                                 | Institutional source                                             |                                No |
| Institutional study role                                   | Institutional source                                             |                                No |
| Current PI assignment                                      | Institutional source                                             |                                No |
| Imported PI `USER_NAME`, mapped to the SAML ePPN attribute | Institutional source                                             |                                No |
| Imported PI identity details                               | Institutional source                                             |                                No |
| Publishability                                             | Institutionally governed process                                 |            No through ordinary UI |
| Participant-facing study content                           | Application study team                                           |                               Yes |
| Study eligibility criteria                                 | Application study team                                           |                               Yes |
| Study activation and deactivation dates                    | Application study team; backend override is technically possible |                               Yes |
| `PRINCIPAL_INVESTIGATOR` association                       | Derived from imported PI data                                    |            No through ordinary UI |
| `STUDY_TEAM_MEMBER` association                            | Application study team                                           |                               Yes |
| Participant account                                        | Participant and supported administrative workflows               |                               Yes |
| Participant profile                                        | Participant                                                      |                               Yes |
| Participant visibility preference                          | Participant                                                      |                               Yes |
| Expression of interest                                     | Participant action                                               |               Cannot be withdrawn |
| Questionnaire structure                                    | Study team while study is inactive                               |                           Limited |
| Questionnaire answers                                      | Participant                                                      | Cannot be edited after submission |

## Imported identity and `APP_USER`

An imported PI may receive an `APP_USER` before first login.

When no corresponding `APP_USER` exists, the application creates one using imported values
including:

- Institutional `USER_NAME`
- First name
- Middle name, when available
- Last name
- Email

The imported `USER_NAME` must correspond to the value supplied by the institutional IdP in the SAML
ePPN attribute.

A PI record missing email or `USER_NAME` is an application error.

When an `APP_USER` already exists, later imported name or email changes are not copied under the
current implementation.

## SAML identity resolution

When a pre-created PI later authenticates, the SAML ePPN value must resolve to the existing
`APP_USER` created for `IMPORTED_TEAM_MEMBER.USER_NAME`.

The required identity mapping is:

```text
IMPORTED_TEAM_MEMBER.USER_NAME
=
APP_USER.USER_NAME
=
SAML ePPN attribute value
```

Email is used for communication and must not be used as the primary identity-matching key.

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

Authorized backend personnel can technically perform operations that are not exposed through
application UIs, including:

- Creating a study membership
- Altering study dates
- Altering publishability

These operations are outside the normal product workflow and must not be confused with ordinary
application permissions.

The approval and audit process for these interventions remains unresolved.

## Related pages

- [Imported Schema](../07-data-model/imported-schema.md)
- [Institutional Users](../04-users-and-access/institutional-users.md)
- [Study Membership](../04-users-and-access/study-membership.md)
- [Imported Institutional Data](../03-institutional-governance/imported-data.md)
- [Open Questions](../09-decisions/open-questions.md)
