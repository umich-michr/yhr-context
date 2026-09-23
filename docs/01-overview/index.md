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

The application supports:

- Public discovery of active studies
- Participant registration and consent
- Self and loved-one participant accounts
- Participant profiles and study interests
- Eligibility and interest matching
- Study-team promotion through Ask if interested
- Expressions of interest
- Screening questionnaires
- Interested-participant workflow management
- Study-team messaging with interested participants
- Study-specific labels
- Study notifications
- Participant-data exports
- Institutionally governed study posting and publishability

## Principal actors

### Participants

Participants use local accounts to manage profiles, discover studies, express interest, complete
screening questionnaires, and respond to study-team messages.

One participant login may manage multiple loved-one participant accounts.

### Study team members

Institutional users authenticate through SAML.

A study member may manage posting content, criteria, questionnaires, interested participants,
messages, labels, notifications, and study lifecycle actions for authorized studies.

### Principal investigators

The current PI is identified by imported institutional data and receives an irremovable current-PI
membership through reconciliation.

### Administrators

Administrators have application-wide access and participant-account administration capabilities.

### Study importers

Study importers use authenticated institutional data imports to maintain study governance
information.

## Important boundaries

- SAML authentication does not grant access to every study.
- Institutional study roles are not application study memberships.
- Matching does not create interest.
- Ask if interested does not create interest or direct messaging.
- Direct messaging begins only after interest and must be initiated by the study team.
- Screening answers are not used by matching.
- Active status is derived from publishability and dates.
- Archive status is separate from active status.
- Historical interest does not always imply current profile or message visibility.
- The application does not integrate with an EHR.

## Related pages

- [Terminology](terminology.md)
- [Business Rules](business-rules.md)
- [System Context](../02-architecture/system-context.md)
- [Participants](../04-users-and-access/participants.md)
- [Study Management](../05-study-management/index.md)
- [Recruitment Overview](../06-recruitment/index.md)
