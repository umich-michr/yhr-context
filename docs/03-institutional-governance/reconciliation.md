---
title: Governance Reconciliation
summary: Alignment of imported studies, publishability, application users, and PI memberships.
status: authoritative
relevant_when:
  - processing_imported_study_updates
  - troubleshooting_publishability
  - troubleshooting_pi_membership
  - comparing_um_and_csv_imports
canonical_for:
  - governance_reconciliation
  - pi_reconciliation
  - publishability_reconciliation
---

# Governance Reconciliation

Reconciliation aligns imported institutional data with operational application data.

The U-M and CSV-based ingestion paths use different implementations, but both enforce the same governance outcomes.

## Reconciliation responsibilities

Reconciliation is responsible for:

1. Applying imported study updates.
2. Validating publishability.
3. Updating operational study publishability.
4. Recalculating active status.
5. Identifying the current imported PI.
6. Finding or creating the PI's `APP_USER`.
7. Ensuring that the current PI has a `PRINCIPAL_INVESTIGATOR` membership.
8. Evaluating whether a delayed PI status-change notification is required.
9. Recording or reporting processing errors.

## University of Michigan reconciliation

At U-M:

1. eResearch provides the institutionally governed source data.
2. Data is placed in an eResearch staging area.
3. A scheduled database job moves data into the `IMPORTED_*` tables.
4. The scheduled job invokes an Oracle package.
5. The Oracle package reconciles imported data with operational application tables.

## CSV-based institutional reconciliation

For institutions using the CSV API:

1. A `STUDY_IMPORTER` or automated importing process submits an incremental CSV.
2. The request is authenticated using a JSON Web Token.
3. Java application code validates the token and CSV.
4. Valid data is applied to the `IMPORTED_*` tables.
5. Java application code reconciles imported and operational data.
6. The U-M Oracle reconciliation package is not used.

## Reconciliation flow

```mermaid
flowchart TD
    START[Receive final imported state for study]
    PUBVALID{PUBLISHABLE is 0 or 1?}
    PUBERROR[Record publishability error]
    FINDSTUDY[Find operational study]
    STUDYEXISTS{Operational study exists?}
    UPDATEPUB[Update operational publishability]
    CALCSTATUS[Recalculate active status]
    FINDPI[Find current imported PI]
    PICOMPLETE{PI has email and USER_NAME?}
    PIERROR[Record PI identity error]
    FINDUSER[Find APP_USER by USER_NAME]
    USEREXISTS{APP_USER exists?}
    CREATEUSER[Create APP_USER]
    REUSEUSER[Reuse APP_USER]
    ENSUREMEMBER[Ensure PI membership]
    NOTIFY[Evaluate delayed notification]
    AUDIT[Record result]
    END[Complete]

    START --> PUBVALID
    PUBVALID -- No --> PUBERROR
    PUBVALID -- Yes --> FINDSTUDY

    FINDSTUDY --> STUDYEXISTS
    STUDYEXISTS -- No --> AUDIT
    STUDYEXISTS -- Yes --> UPDATEPUB

    UPDATEPUB --> CALCSTATUS
    CALCSTATUS --> FINDPI
    FINDPI --> PICOMPLETE

    PICOMPLETE -- No --> PIERROR
    PICOMPLETE -- Yes --> FINDUSER

    FINDUSER --> USEREXISTS
    USEREXISTS -- No --> CREATEUSER
    USEREXISTS -- Yes --> REUSEUSER

    CREATEUSER --> ENSUREMEMBER
    REUSEUSER --> ENSUREMEMBER

    ENSUREMEMBER --> NOTIFY
    NOTIFY --> AUDIT

    PUBERROR --> AUDIT
    PIERROR --> AUDIT
    AUDIT --> END
```

## Incremental-update behavior

Institutional imports are incremental.

When an imported record is present:

- The corresponding imported row is inserted or updated.
- Applicable operational data is reconciled.

When an imported record is absent:

- The existing imported row remains unchanged.
- The operational study remains unchanged.
- Publishability remains unchanged.
- PI information remains unchanged.

Absence from a new file is not interpreted as deletion.

## Multiple updates for one study

A CSV may contain multiple updates for one `study_num`.

Only the latest applicable update is reconciled with operational application data.

Intermediate historical rows must not cause temporary transitions such as:

```text
ACTIVE
→ INACTIVE
→ ACTIVE
```

Only the final imported state affects:

- Operational publishability
- Operational active status
- Current PI processing
- Delayed status notifications

## Publishability reconciliation

`PUBLISHABLE` must be:

```text
0
```

or:

```text
1
```

A null, missing, or invalid value is an application error.

For an existing operational study:

```text
STUDY.PUBLISHABLE = final imported PUBLISHABLE value
```

Active status is then recalculated using:

- Publishability
- Activation date
- Deactivation date
- Current date

When publishability returns from `0` to `1`, the study automatically becomes active if the current date remains within the configured date range.

## PI reconciliation

Each valid imported study has one current institutional PI.

The imported PI record must include:

- Email
- `USER_NAME`

`IMPORTED_TEAM_MEMBER.USER_NAME` must correspond to the value supplied by the institutional IdP in the SAML ePPN attribute.

If either email or `USER_NAME` is missing, reconciliation reports an application error.

## New PI application user

If no corresponding `APP_USER` exists:

1. Create an `APP_USER`.
2. Copy the imported identity information.
3. Associate the user with the study as `PRINCIPAL_INVESTIGATOR`.

Imported values used for a new PI user include:

- Institutional `USER_NAME`
- First name
- Middle name, when present
- Last name
- Email

The identity mapping is:

```text
IMPORTED_TEAM_MEMBER.USER_NAME
=
APP_USER.USER_NAME
=
SAML ePPN attribute value
```

When the PI later authenticates, the SAML ePPN value resolves to the previously created `APP_USER`.

## Existing PI application user

If a corresponding `APP_USER` already exists:

- Reuse the existing application user.
- Ensure that the PI has a `PRINCIPAL_INVESTIGATOR` membership.
- Do not copy later imported name or email changes into the existing `APP_USER`.

## PI-change behavior

When the current imported PI changes:

1. Reconciliation finds or creates an `APP_USER` for the new PI.
2. Reconciliation associates the new PI with the study as `PRINCIPAL_INVESTIGATOR`.
3. The former PI's existing operational membership is not automatically removed.

The imported data can therefore identify one current PI while the operational study retains:

- The newly imported current PI
- A former PI with an existing `PRINCIPAL_INVESTIGATOR` membership

The former PI may continue to have study access unless another process removes the membership.

This is current behavior and a known access-governance concern.

## Status-change notification delay

Active-status notifications are delayed to avoid messages for temporary transitions.

Example:

```text
ACTIVE → INACTIVE → ACTIVE within one day
```

Result:

```text
No notification
```

If the changed state remains for more than one day:

```text
Notify the PI
```

The final stable state is evaluated rather than notifying for every intermediate transition.

## Idempotency

Repeated processing of the same final imported state should not:

- Create duplicate application users
- Create duplicate memberships
- Produce conflicting publishability values
- Produce conflicting active statuses
- Send duplicate notifications for the same stable transition

## Error handling

Reconciliation errors may include:

- Invalid publishability
- Missing PI
- PI missing email
- PI missing `USER_NAME`
- Imported `USER_NAME` that cannot be reconciled with the expected institutional identity
- Failure to create an `APP_USER`
- Failure to create a PI membership
- Failure to update the operational study
- Failure to schedule or send a notification

CSV-related errors are written to logs and reported by email to the responsible study importer.

## Rollback

The application does not provide an import-batch rollback function.

Corrections require a later incremental update containing the corrected final state.

## Related pages

- [Imported Institutional Data](imported-data.md)
- [Imported Schema](../07-data-model/imported-schema.md)
- [Import Pipeline](import-pipeline.md)
- [Publishability](publishability.md)
- [Institutional Users](../04-users-and-access/institutional-users.md)
- [Study Membership](../04-users-and-access/study-membership.md)
- [Open Questions](../09-decisions/open-questions.md)
