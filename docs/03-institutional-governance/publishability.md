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

`PUBLISHABLE` indicates whether an institution currently permits a study to recruit through its
branded YourHealthResearch.org platform instance.

Publishability is study-specific. The existence of a study in an institutional IRB system does not
necessarily mean that the study may use the application as a recruitment method.

## Valid values

`PUBLISHABLE` is required and Boolean:

```text
0 = Not publishable
1 = Publishable
```

A null, missing, or otherwise invalid publishability value is an application error.

## Authority

Publishability is determined from institutionally governed information.

At the University of Michigan, the application team works with the eResearch team to identify which
source data points determine whether a study may recruit through UMHealthResearch.org.

Other institutions provide equivalent publishability information through their incremental CSV
imports.

Study team members cannot directly edit the imported publishability value.

## Relationship to active status

A study's matching-active status depends on publishability and local recruitment dates.

`V_ACTIVE_STUDY`, which supplies matching-active studies, requires:

- `PUBLISHABLE = 1`
- Current calendar date on or after `POSTING_ACTIVATION_DATE`
- Current calendar date before `POSTING_DEACTIVATION_DATE`

The view truncates time-of-day. Activation is inclusive and deactivation is exclusive.

`V_STUDY_STATUS` uses an inclusive `BETWEEN` comparison instead. On the saved deactivation date, the
status view and matching-active view can disagree. Matching follows `V_ACTIVE_STUDY`.

## Transition to non-publishable

When `PUBLISHABLE` changes from `1` to `0`:

- The study becomes inactive.
- Active matching and recruitment stop.
- The study is removed from the active in-memory study collection.
- Public active-study discovery stops.
- New Ask if interested actions are blocked.
- New expressions of interest are blocked.
- Study-team participant-data access is blocked.
- Existing conversations are hidden.
- New participant-data exports are blocked.
- Existing activation and deactivation boundaries remain unchanged.
- Historical expressions of interest remain stored.
- The current active interval is closed.
- The study's configured deactivation date is not changed.
- Delayed lifecycle-notification handling is initiated.

The current implementation uses the imported flag when calculating active status. It does not
persist a separate local governance-deactivation state.

## Transition to publishable

When an imported `PUBLISHABLE` value changes from `0` to `1`:

1. The application updates `STUDY.PUBLISHABLE`.
1. It sets `POSTING_ACTIVATION_DATE` to the current time.
1. It records or updates the applicable `STUDY_ACTIVE_INTERVAL`.
1. It updates local active-study state.
1. It initiates applicable matching when effective status changes.

The configured posting deactivation date is not replaced by this path. If that date has passed, the
resulting range cannot remain matching-active.

This behavior differs from merely reevaluating an unchanged activation range: imported transition to
publishable explicitly resets the activation boundary.

## Known governance concern

Automatic reactivation may not satisfy every institutional governance workflow.

Example:

1. The institution requires a study to stop recruitment unless it changes its participant-facing
   title.
1. The institution sets `PUBLISHABLE = 0`.
1. The study becomes inactive.
1. The study acknowledges the requirement in the institutional system.
1. The acknowledgment causes `PUBLISHABLE` to return to `1`.
1. The study team has not yet updated the title in the application.
1. The imported transition resets the posting activation date to the current time.
1. If the retained deactivation date is still in the future, the study becomes active automatically.

Possible future approaches include:

- Setting the local deactivation date when publishability becomes `0`
- Maintaining a separate governance-hold state
- Requiring study-team review before reactivation
- Requiring explicit manual reactivation after a governance deactivation

These are possible enhancements, not current behavior.

## Multiple updates in one CSV import

A CSV may contain multiple updates for the same study.

Rows are processed independently and in file order.

For example:

```text
Row 1: Study A PUBLISHABLE = 0
Row 2: Study A PUBLISHABLE = 1
Row 3: Study A PUBLISHABLE = 1 and PI changed
```

Each successfully processed row may update operational application data.

The later successful row overwrites an earlier value when both modify the same field. Therefore,
after all three rows succeed:

- Final publishability is `1`.
- The PI supplied by row 3 is current.
- Intermediate inactive and active transitions may have occurred.

The application does not first collapse these rows into one final row before processing them.

## Status-change notifications

Active-status changes participate in delayed notification handling.

A daily scheduled process evaluates lifecycle changes and configured Other Announcements recipients.

The current PI also receives lifecycle-related notifications when applicable.

Short-lived transitions may be suppressed by a one-day stabilization rule.

Conceptually:

```text
ACTIVE → INACTIVE → ACTIVE within the stabilization period
    No stable-state PI notification
```

If a changed state remains in effect beyond the stabilization period, the PI is notified.

Because CSV rows are processed sequentially, intermediate transitions may occur within one import.
Stabilization reduces misleading email about short-lived states but does not mean the intermediate
operational transitions were skipped.

## Incremental-import implications

If a study is absent from a later incremental import:

- Its imported record is not removed.
- Its imported publishability value remains unchanged.
- Its operational publishability remains unchanged.
- Its active status is not changed merely because it was absent from the import.

## Participant-facing inactive-study behavior

If a participant follows a direct or bookmarked URL for an inactive study posting, the application
displays a message that the study is no longer recruiting.

The study number remains part of the participant-facing URL even when the study is inactive.

## Access implications

When the study becomes non-publishable:

- It no longer participates in active matching.
- It is removed from active in-memory matching data.
- Study teams cannot access participant information for recruitment.
- Study teams cannot generate new participant-data exports.
- Historical interest relationships remain stored.
- Previously downloaded CSV files cannot be recalled or invalidated by the application.

## Related pages

- [Imported Institutional Data](imported-data.md)
- [Import Pipeline](import-pipeline.md)
- [Governance Reconciliation](reconciliation.md)
- [Study Lifecycle](../05-study-management/study-lifecycle.md)
- [Questionnaires and Exports](../06-recruitment/questionnaires-and-exports.md)
- [Open Questions](../09-decisions/open-questions.md)
