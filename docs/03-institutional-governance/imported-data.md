---
title: Imported Institutional Data
summary: Purpose, row-order update semantics, and authority of imported tables.
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
5. Create and maintain the current PI study association.
6. Remove the former PI association when the imported PI changes.
7. Determine whether a study may recruit.
8. Update publishability for existing study postings.
9. Make studies inactive when publishability becomes `0`.

## Incremental update semantics

Institutional imports are incremental.

This means:

- Imported records supplied in a new import are inserted or updated.
- Imported records absent from a new import remain unchanged.
- A missing imported row is not interpreted as a deletion.
- An operational study that does not appear in an import remains unchanged.
- Import batches cannot be rolled back through the application.

## CSV row-order semantics

For CSV-based instances:

- Rows are processed in file order.
- Each row is handled independently.
- A successfully processed row may immediately update imported data and
  reconcile operational data.
- A later row for the same study may overwrite an earlier value.
- The last successfully processed row affecting a particular field determines
  that field's final value after the file is processed.

Example:

```text
Row 1: Study A PUBLISHABLE = 0
Row 2: Study A PUBLISHABLE = 1
Row 3: Study A PUBLISHABLE = 1 and PI changed
```

The rows are not first reduced to one final study record.

Each row is processed in order. After all three rows succeed:

- Final publishability is `1`.
- The PI from row 3 is the current PI.
- Intermediate operational transitions caused by rows 1 and 2 may have
  occurred.

## Institutional roles

`IMPORTED_STUDY_TEAM_MEMBER` may contain:

- PI
- Study coordinator
- Other institution-defined roles

Each valid imported study has one current institutional PI.

Only the current PI relationship automatically creates application study
access. Other imported roles are retained for non-application or future use.

## Role mapping

| Imported condition | Application result |
|---|---|
| Current imported PI | Associate user as `PRINCIPAL_INVESTIGATOR` |
| Former imported PI after a PI change | Remove former operational PI membership |
| Imported non-PI role | No automatic application study association |
| Posting creator who is not PI | Associate as `STUDY_TEAM_MEMBER` |
| User accepts invitation | Associate as `STUDY_TEAM_MEMBER` |

## Imported PI requirements

The imported PI must have:

- An email address
- A `USER_NAME` value corresponding to the institutional SAML ePPN attribute

If either is missing, processing fails with an application error.

See [Imported Schema](../07-data-model/imported-schema.md).

## Related pages

- [Import Pipeline](import-pipeline.md)
- [Governance Reconciliation](reconciliation.md)
- [Institutional Users](../04-users-and-access/institutional-users.md)
