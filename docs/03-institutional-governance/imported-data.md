---
title: Imported Institutional Data
summary: Purpose, update semantics, and authority of the imported tables.
status: authoritative
---

# Imported Institutional Data

The application stores institutionally supplied information in:

- `IMPORTED_STUDY`
- `IMPORTED_STUDY_TEAM_MEMBER`
- `IMPORTED_TEAM_MEMBER`

These tables are not modifiable by ordinary study team members.

## Primary purposes

Imported data is used to:

1. Validate that a study exists before a posting is created.
2. Prevent posting creation for an unknown `study_num`.
3. Identify the study's current institutional PI.
4. Create an application user for a PI when needed.
5. Create or maintain PI study associations.
6. Determine whether a study may recruit.
7. Update publishability for existing study postings.
8. Make studies inactive when publishability becomes `0`.

## Incremental update semantics

Institutional imports are incremental.

This means:

- Imported records supplied in a new import are inserted or updated.
- Imported records absent from a new import remain unchanged.
- A missing imported row is not interpreted as a deletion.
- An operational study that does not appear in an import remains unchanged.
- Import batches cannot be rolled back through the application.

## Multiple updates for one study

A CSV file may contain multiple historical updates for the same study.

For example:

```text
Study A: PUBLISHABLE = 0
Study A: PUBLISHABLE = 1
Study A: PUBLISHABLE = 1 and PI changed
```

Only the latest update for that study is applied to operational application data.
Intermediate rows must not temporarily deactivate or reactivate the operational study. This prevents unnecessary disruption and avoids sending notifications for transient states represented only inside one import.

## Institutional roles

IMPORTED_STUDY_TEAM_MEMBER may contain:

* PI
* Study coordinator
* Other institution-defined roles

Each imported study has one current institutional PI.
Only the PI relationship currently affects application authorization. Other imported roles are retained for non-application or future use.

## Role mapping


| Imported condition | Application result |
| :--- | :--- |
| Current imported PI | Associate user as PRINCIPAL_INVESTIGATOR |
| Imported non-PI role | No automatic application study association |
| Posting creator who is not PI | Associate as STUDY_TEAM_MEMBER |
| User accepts invitation | Associate as STUDY_TEAM_MEMBER |


## Imported PI requirements

The imported PI must have:

- An email address
- A `USER_NAME` value corresponding to the institutional SAML ePPN attribute

If either is missing, processing fails with an application error.
See [Imported schema](../07-data-model/imported-schema.md).
