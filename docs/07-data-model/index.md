---
title: Data-Model Overview
summary: Imported, operational, recruitment, questionnaire, and audit entities.
status: authoritative
---

# Data-Model Overview

The logical model contains five areas.

## Imported governance

- `IMPORTED_STUDY`
- `IMPORTED_STUDY_TEAM_MEMBER`
- `IMPORTED_TEAM_MEMBER`

## Operational identity and studies

- `APP_USER`
- `STUDY`
- `STUDY_TEAM_MEMBER`
- `STUDY_TEAM_INVITATION`

## Participants and recruitment

- Participant account
- Participant profile
- Participant preferences
- Match evaluation
- Study-team prompt
- Participant-study interest

## Questionnaires and exports

- Questionnaire
- Question
- Submission
- Response
- In-memory CSV export

## Operations

- Audit event
- Status history
- Import batch
- Reconciliation run
- Notification

Read:

- [Imported schema](imported-schema.md)
- [Operational schema](operational-schema.md)