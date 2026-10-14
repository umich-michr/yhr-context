---
title: Study Archiving
summary: Archive and unarchive behavior for inactive studies.
status: authoritative
canonical_for:
  - study_archiving
  - archived_studies
relevant_when:
  - archiving_a_study
  - unarchiving_a_study
  - explaining_archived_studies
---

# Study Archiving

Archiving is an institutional-user organization feature separate from recruitment activity.

## Preconditions

Only an inactive study may be archived.

An active study must first be deactivated.

## Archive behavior

Archiving:

- Sets the archived-date study property.
- Removes the study from Current Studies.
- Places the study in Archived Studies.
- Prevents public access and discovery because the study is already inactive
- Does not delete the study.
- Does not change participant-data access.
- Does not remove exports.
- Does not hide existing conversations.

`ARCHIVED_DATE` is stored through `STUDY_PROPERTY_VALUE` as string in the long time format.

Archive and unarchive use the study-property update path. `STUDY_AUDIT` records the user, study,
operation time, and `studyProperties[archivedDate]` field path, but it does not retain the old and new
archived values. Archive is not a lifecycle cause stored on `STUDY_ACTIVE_INTERVAL`.

## Unarchive behavior

An archived study may be unarchived.

Unarchiving:

- Removes or clears the archived state
- Returns the study to the inactive Current Studies view
- Does not activate the study

An archived study cannot be activated directly.

The study must first be unarchived and then explicitly activated.

## Archive and active status

Archive status and recruitment activity are separate dimensions:

```text
Active/inactive:
    Derived from publishability and dates

Archived/not archived:
    Organizational state controlled by study team
```

## Related pages

- [Study Lifecycle](study-lifecycle.md)
- [Study Property Model](../07-data-model/study-property-model.md)
- [Messaging](../06-recruitment/messaging.md)
