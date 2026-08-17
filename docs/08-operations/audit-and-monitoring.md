---
title: Audit and Monitoring
summary: Recommended audit events and operational health metrics.
status: recommended
---

# Audit and Monitoring

This page distinguishes confirmed audit behavior from recommended improvements.

## Audit events

The application audits participant-profile access, including administrator
access. It does not separately audit CSV export actions or invitation lifecycle
events.

Recommended additional events include:

- Participant registration and login
- Participant profile or visibility change
- Participant deactivation or deletion
- Institutional SAML login
- Import received
- Import validation result
- Reconciliation run
- Publishability change
- Study creation, activation, or deactivation
- PI user creation
- PI membership change
- Invitation creation, revocation, and consumption
- Study membership change
- Ask if interested
- Expression or withdrawal of interest
- Questionnaire publication and submission
- Participant profile view
- Export request, generation, and download
- Administrator action

## Suggested audit fields

```text
EVENT_ID
EVENT_TYPE
ACTOR_TYPE
ACTOR_ID
TARGET_TYPE
TARGET_ID
STUDY_ID
PARTICIPANT_ID
TIMESTAMP
REQUEST_ID
RESULT
REASON
BEFORE_STATE
AFTER_STATE
```

Audit records should avoid unnecessarily duplicating sensitive participant data.

## Reconciliation metrics

Monitor:

- Last successful import
- Last successful reconciliation
- Imported record counts
- Rejected record counts
- Missing imported studies
- Publishability changes
- Studies deactivated
- PI users created
- PI memberships created or changed
- Unresolved personnel
- Job duration
- Failure reason

## Export investigation

Exports are generated in memory and streamed directly to the browser, so there
is no retained server-side export artifact to monitor.

To investigate a possible export, correlate:

- The audited visit to the interested-participants page
- The participant profile views associated with that visit
- Splunk request logs around the same time

This is an investigative approximation, not a definitive export audit trail.
