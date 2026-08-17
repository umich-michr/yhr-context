---
title: Publishability
summary: Institutionally governed permission for a study to recruit through the application.
status: authoritative
relevant_when:
  - determining_whether_a_study_can_recruit
  - explaining_study_activation
  - troubleshooting_study_deactivation
  - processing_imported_study_updates
---

# Publishability

`PUBLISHABLE` indicates whether an institution currently permits a study to recruit through YourHealthResearch.org.

Publishability is study-specific. The existence of a study in an institutional IRB system does not necessarily mean that the study may use YourHealthResearch.org as a recruitment method.

## Valid values

`PUBLISHABLE` is required and Boolean:

```text
0 = Not publishable
1 = Publishable
```

A null, missing, or otherwise invalid publishability value is an application error.

## Source of publishability

Publishability is determined from institutionally governed information.

At the University of Michigan, the application team works with the eResearch team to identify which source data points must be processed to determine whether a study may recruit through YourHealthResearch.org.

Other institutions provide equivalent publishability information through their incremental CSV imports.

Study team members cannot directly edit the imported publishability value.

## Active-status calculation

A study's active status depends on both its local recruitment dates and its institutionally controlled publishability.

Conceptually:

```text
Study is active =
    PUBLISHABLE = 1
    AND today falls within the study's activation and deactivation dates
```

Activation-date and deactivation-date boundaries are inclusive.

## Transition from publishable to non-publishable

When `PUBLISHABLE` changes from `1` to `0`:

- The study becomes inactive.
- The study is removed from active matching.
- The study is no longer presented as actively recruiting.
- New participant recruitment interactions are blocked.
- Study-team access to participant profile information is restricted according to the study-deactivation rules.
- Historical expressions of interest may remain recorded.
- The study's configured deactivation date is not changed.

The current implementation uses the imported flag when calculating active status. It does not persist a separate local governance-deactivation state.

## Transition from non-publishable to publishable

When `PUBLISHABLE` changes from `0` to `1`:

1. The application recalculates the study's active status.
2. If the current date remains within the existing activation and deactivation dates, the study becomes active automatically.
3. No separate manual reactivation is required under the current implementation.

This means a publishability change alone can reactivate a study.

## Known governance concern

Automatic reactivation may not satisfy every institutional governance workflow.

Example:

1. The institution requires a study to stop recruitment unless it changes its participant-facing title.
2. The institution sets `PUBLISHABLE = 0`.
3. The study becomes inactive.
4. The study acknowledges the requirement in the institutional system.
5. The acknowledgment causes `PUBLISHABLE` to return to `1`.
6. The study team has not yet updated the title in YourHealthResearch.org.
7. The original activation and deactivation dates still include the current date.
8. The study becomes active automatically.

Possible future approaches include:

- Setting the local deactivation date when publishability becomes `0`
- Maintaining a separate governance-hold state
- Requiring study-team review before reactivation
- Requiring explicit manual reactivation after a governance deactivation

These are possible enhancements, not current behavior.

## Multiple updates in one import

An incremental CSV may contain multiple historical updates for the same study.

For example:

```text
Study A: PUBLISHABLE = 0
Study A: PUBLISHABLE = 1
Study A: PUBLISHABLE = 1 and PI changed
```

Only the latest applicable update for the study is applied to operational application data.

Intermediate rows must not cause temporary operational transitions such as:

```text
ACTIVE
→ INACTIVE
→ ACTIVE
```

This prevents historical rows within one import from unnecessarily disrupting recruitment or generating misleading notifications.

The exact field used to determine which row is the latest remains documented as an open technical question.

## Status-change notifications

PI notifications for active-status changes are delayed to avoid notifying the PI about short-lived transitions.

Conceptually:

```text
ACTIVE → INACTIVE → ACTIVE within one day
    No notification
```

If a status change remains in effect for more than one day, the PI is notified.

Example:

```text
ACTIVE → INACTIVE
and the study remains inactive for more than one day
    Notify PI
```

This notification delay prevents the PI from receiving messages about transient status changes.

## Incremental-import implications

Institutional imports are incremental.

If a study is absent from a later import:

- Its imported record is not removed.
- Its imported publishability value remains unchanged.
- Its operational publishability remains unchanged.
- Its active status is not changed merely because the study was absent from the import.

## Participant-facing inactive-study behavior

If a participant follows a direct or bookmarked URL for an inactive study posting, the application displays a message that the study is no longer recruiting.

The study number remains part of the participant-facing URL even when the study is inactive.

## Access implications

When the study becomes non-publishable:

- It no longer participates in active matching.
- Study teams cannot access participant information for recruitment.
- Study teams cannot generate new participant-data exports.
- Historical interest relationships may remain stored.
- Previously downloaded CSV files cannot be recalled or invalidated by the application.

## Related pages

- [Imported institutional data](imported-data.md)
- [Import pipeline](import-pipeline.md)
- [Governance reconciliation](reconciliation.md)
- [Study lifecycle](../05-study-management/study-lifecycle.md)
- [Questionnaires and exports](../06-recruitment/questionnaires-and-exports.md)
- [Open questions](../09-decisions/open-questions.md)