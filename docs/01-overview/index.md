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

### Participants (VOLUNTEER)

Participants create local accounts using an email address as their username. They maintain profiles, define study interests, review studies, express interest, and complete study-specific screening questionnaires.

### Institutional users (STAFF)

Study team members and principal investigators authenticate using institutional SAML single sign-on.

A valid institutional login permits access to the study-team side of the application, but does not grant access to every study.

### Principal investigators (STAFF)

PIs are identified by an institutionally governed source of truth. PI membership is synchronized into the application and cannot be changed through ordinary local workflows.

### Administrators (ADMIN)

Administrators support accounts and application operations. The complete scope of administrator authority requires additional documentation.

### Study Importers (STUDY_IMPORTER)

Creates api key to upload csv files for institutional source of truth study PI and publishable flag to be imported int the application.

## Major application capabilities

1. Import institutionally governed study and PI data.
2. Validate whether an authoritative study exists.
3. Derive or receive a study's publishability.
4. Create one recruiting posting for an imported study.
5. Associate the creator and PI with the posting.
6. Match studies and participants.
7. Allow participants to express interest.
8. Collect study-specific questionnaire responses.
9. Allow authorized study teams to export permitted data.
10. Deactivate recruitment when institutional or application conditions require it.

## Important distinctions

- An imported institutional study is not the same as a study posting.
- Institutional roles are not the same as application roles.
- Authentication is not the same as study authorization.
- Study-interest matching is not the same as eligibility matching.
- A system match is not the same as an expression of interest.
- Historical interest is not the same as current profile visibility.

## Related pages

- [Terminology](terminology.md)
- [Business rules](business-rules.md)
- [System context](../02-architecture/system-context.md)
- [Recruitment overview](../06-recruitment/index.md)
