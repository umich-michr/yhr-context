---
title: Questionnaires and Exports
summary: Screening-questionnaire rules, submission behavior, and participant-data CSV exports.
status: authoritative
relevant_when:
  - creating_or_editing_questionnaires
  - completing_interest
  - exporting_participant_data
  - troubleshooting_export_access
---

# Questionnaires and Exports

A study may use one screening questionnaire to collect additional information from participants who express interest.

## One questionnaire per study

A study can have only one screening questionnaire.

Conceptually:

```text
One STUDY
has zero or one QUESTIONNAIRE
```

The application does not maintain multiple active questionnaires for one study.

## Questionnaire questions

When creating a screening questionnaire, study team members may mark each question as:

- Required
- Optional

To complete the questionnaire:

- Every required question must have an answer.
- Optional questions may be left unanswered.

Questionnaire completion is required to finalize the expression-of-interest workflow when a questionnaire exists.

## Editing restrictions

A study team cannot change the questionnaire structure while the study is active.

To change the questionnaire:

1. Deactivate the study.
2. Add or delete questions.
3. Reactivate the study when activation conditions are satisfied.

While the study is inactive, the study team may:

- Add questions
- Delete questions
- Change question display order

Changing display order is considered an edit, but it is allowed while the study
is inactive. Other changes to existing question content are not supported.

## No questionnaire versioning

Questionnaires are not versioned.

Only the current questionnaire structure is retained.

There is no separately displayable historical questionnaire version.

Deleting a question also hard-deletes its previously submitted answers. The
historical answers are not retained or independently interpretable.

## Submitted answers

Participants cannot edit submitted questionnaire answers.

Participants cannot save or resume an incomplete questionnaire.

Deleting a question is allowed even when it has existing answers, but the
application requires a confirmation before deleting those answers.

When multiple study-team members edit an inactive questionnaire concurrently,
the first successful submission wins. A later submission based on stale data is
rejected and the user must refresh; the rejected user's unsaved changes are
not preserved.

## Relationship to expressions of interest

When a participant attempts to express interest:

1. The participant refreshes temporal profile values.
2. The application rechecks eligibility.
3. If eligible, the participant completes the questionnaire.
4. The interest workflow is finalized after required questionnaire answers are provided.

See [Expressions of interest](expressions-of-interest.md).

## Export permissions

Both study-association roles have equivalent export access:

```text
PRINCIPAL_INVESTIGATOR
STUDY_TEAM_MEMBER
```

Authorized study team members may export:

- All participant profile fields available to the study
- All screening-questionnaire answers submitted by interested participants

## Export availability

Participant data can be exported whenever `PUBLISHABLE = 1`; study active
status does not restrict exports of historical interested-participant data.

If the study becomes non-publishable:

- Study team members cannot access participant information.
- Study team members cannot generate a new participant-data export.

## Downloaded CSV files

The application generates a CSV file that the study team downloads.

After download:

- The file exists outside the application.
- The application cannot invalidate the file.
- The application cannot recall the file.
- A later participant deactivation does not delete the downloaded copy.
- A later study deactivation does not delete the downloaded copy.
- A later publishability change does not delete the downloaded copy.

Study teams are responsible for handling downloaded data according to applicable institutional and study requirements.

## Export processing and auditability

Exports are generated in memory and streamed to the browser; the application
does not retain a temporary server-side export file.

The export action itself is not audited. Participant-profile views are audited,
however, and an export is preceded by a visit to the interested-participants
page. Support investigations may correlate that audit event with Splunk request
logs by time, but this does not create a definitive export audit record.

## Export content and security behavior

Each export includes all participant profile fields available to the study,
including contact information, whether or not each field was relevant to the
study criteria. Export generation does not require recent reauthentication.

The application does not currently escape CSV values to mitigate spreadsheet
formula injection. After the stream is downloaded, protection, encryption at
rest, and retention of the resulting file are the study team's responsibility.

## Related pages

- [Expressions of interest](expressions-of-interest.md)
- [Study membership](../04-users-and-access/study-membership.md)
- [Study lifecycle](../05-study-management/study-lifecycle.md)
- [Publishability](../03-institutional-governance/publishability.md)