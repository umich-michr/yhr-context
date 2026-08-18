---
title: Application Overview
summary: High-level description of users, studies, recruitment, and governance.
status: authoritative
relevant_when:
  - explaining_application_purpose
  - onboarding
  - general_support
---

# Application Overview

YourHealthResearch.org connects participants with human-subject research studies.

## Principal actors

### Participants (`VOLUNTEER`)

Participants create local accounts using email addresses as usernames.

They may:

- Maintain participant profiles
- Define study interests
- Review matched studies
- Express interest
- Complete study-specific screening questionnaires
- Deactivate their accounts

### Institutional study users (`STAFF`)

Study team members and principal investigators authenticate using institutional SAML single sign-on.

A valid institutional login permits access to the institutional-user portion of the application, but it does not grant access to every study.

A `STAFF` user ordinarily needs a study-specific association to access an individual study.

### Principal investigators (`STAFF`)

The current PI is identified by the institutionally governed source of truth.

The imported current PI is associated with the study as:

```text
PRINCIPAL_INVESTIGATOR
```

The current PI membership cannot be removed through ordinary application UIs.

When the imported PI changes, the former PI's existing operational membership is not automatically removed.

### Administrators (`ADMIN`)

Administrators are application-wide superusers.

They may:

- Access all studies
- Access participant data
- Activate, reactivate, and deactivate participant accounts
- Reset participant passwords
- Perform other supported administrative operations

Administrators do not create study memberships through ordinary application UIs.

### Study importers (`STUDY_IMPORTER`)

Study importers support the authenticated institutional CSV-import workflow.

A study importer or automated importing process uses an expiring JSON Web Token to upload incremental institutional study data.

Imported data may update:

- Study existence information
- Publishability
- Institutional study-team information
- Current PI information

The `STUDY_IMPORTER` role does not itself grant access to study or participant data.

## Major application capabilities

1. Import institutionally governed study and PI data.
2. Validate whether an authoritative study exists.
3. Derive or receive a study's publishability.
4. Create one recruiting posting for an imported study.
5. Associate the creator and PI with the posting.
6. Author study information and eligibility criteria.
7. Match studies and participants.
8. Allow participants to express interest.
9. Collect study-specific questionnaire responses.
10. Allow authorized study teams to export permitted data.
11. Deactivate recruitment when institutional or application conditions require it.

## Important distinctions

- An imported institutional study is not the same as a study posting.
- Institutional roles are not the same as application roles.
- Application-wide roles are not the same as study-association roles.
- Authentication is not the same as study authorization.
- Study-interest matching is not the same as eligibility matching.
- A partial match is not shown in a participant-facing matched-study list.
- A system match is not the same as an expression of interest.
- Historical interest is not the same as current profile visibility.
- Date-based inactivity is not the same as non-publishability.

## Related pages

- [Terminology](terminology.md)
- [Business rules](business-rules.md)
- [System context](../02-architecture/system-context.md)
- [Users and access](../04-users-and-access/index.md)
- [Study management](../05-study-management/index.md)
- [Recruitment overview](../06-recruitment/index.md)
