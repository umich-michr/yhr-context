---
title: Questionnaires and Exports
summary: Screening-questionnaire authoring, show-interest capture, response retention, and interested-participant CSV exports.
status: authoritative
canonical_for:
  - questionnaire_behavior
  - questionnaire_editing
  - export_contents
  - export_availability
---

# Questionnaires and Exports

A study has a physical `STUDY_SCREEN_QNAIRE` row associated with the study. Current participant and
study-team services retrieve it by `STUDY_ID`.

## Physical questionnaire model

| Table                        | Purpose and key relationships                                                                                  |
| ---------------------------- | -------------------------------------------------------------------------------------------------------------- |
| `STUDY_SCREEN_QNAIRE`        | Questionnaire header; sequence primary key, `STUDY_ID` foreign key to `STUDY`, integer `VERSION`               |
| `STUDY_SCREENING_QUESTION`   | Ordered questions; sequence primary key and `QUESTIONNAIRE_ID` foreign key with cascade delete                 |
| `STUDY_SCR_QUES_OPTION`      | Ordered response choices; sequence primary key and question foreign key with cascade delete                    |
| `VOL_SCR_QUESTION_ANSWER`    | Participant answer; sequence primary key plus `USER_ID`, `STUDY_ID`, question ID, answer text, and answer date |
| `VOL_QSTN_ANSWR_SLCTD_OPTNS` | Composite-key join table connecting one answer to selected options                                             |

Questionnaire deletion cascades to questions. Question deletion cascades to options and answers.
Deleting an answer or option cascades the applicable selected-option joins. Account deletion cascades
participant answers. Study deletion cascades questionnaire definitions but the answer table's direct
`STUDY_ID` foreign key is restrictive; dependent answers must be removed through question cascades or
application deletion ordering.

The current schema does not declare a database unique constraint on `STUDY_SCREEN_QNAIRE.STUDY_ID`.
The application queries as though one questionnaire per study exists and would fail on multiple
results. Treat zero-or-one questionnaire per study as an application invariant rather than a
database-enforced uniqueness fact.

## Questions, choices, and ordering

A question stores:

- `ORDER_NUM`
- `EDITABLE`
- `REQUIRED`
- `TEXT`
- `HELP_TEXT`
- `INPUT_TYPE`

Questions are returned in ascending `ORDER_NUM`. Response choices similarly store `ORDER_NUM` and
`TEXT` and are returned in display order.

Current participant rendering supports free text and option selections. Profile-backed questions are
represented in the participant payload as `VOLUNTEER_PROFILE`; their values are persisted through the
ordinary profile-property tables rather than `VOL_SCR_QUESTION_ANSWER`. User-defined study questions
persist in the answer tables.

## Current authoring behavior

A study member may author questions while the study is inactive. The service rejects add, update,
delete, and reorder operations while `Study.isActive()` is true.

The application allows:

- adding questions;
- changing question text, help text, and required status;
- adding response choices;
- changing or removing choices in the submitted model;
- deleting questions; and
- reordering questions.

The service does not replace `INPUT_TYPE` while updating an existing question, so question type is
effectively fixed after creation.

The study-team interface disables editing or deleting an existing choice when answer count for the
question is greater than zero, while still allowing new choices. This client guard is important
because the service's update merge can remove choices omitted from a request.

## Authorization concerns

The staff URL namespace requires an authenticated `ADMIN` or `STAFF` role. GET, DELETE, reorder PATCH,
and answer-count paths also call study-level authorization.

The question-creation POST and question-update PUT handlers do not call `checkStudyAccess`, and their
service methods do not verify study membership. Therefore any authenticated staff account can
currently attempt those operations for an inactive study ID. This is a known backend authorization
gap, not an intended business rule.

## Version and concurrency control

`STUDY_SCREEN_QNAIRE.VERSION` is a JPA `@Version` field. Study-team GET responses expose it as an
`ETag`; authoring calls supply `If-Match`.

Questionnaire updates use a pessimistic force-increment lock together with the version field.
Application code also compares expected and actual versions on selected paths. A stale operation is
returned as precondition failure where the controller handles the locking exception.

The participant submission also sends `If-Match`. A stale or missing questionnaire causes
precondition failure, forcing a refresh before interest can be finalized.

This version is a concurrency counter, not a historical questionnaire version. No definition
snapshot or version history is retained.

## Participant submission and answers

The participant submits one form containing profile-backed and study-specific questions.

For a user-defined answer:

- free text is stored in `ANSWER_VALUE`; or
- one answer row links to one or more selected choices through
  `VOL_QSTN_ANSWR_SLCTD_OPTNS`;
- `ANSWER_DATE`, `USER_ID`, `STUDY_ID`, and question ID are stored.

Blank optional responses create no answer row. Participants cannot save a partial submission or edit
submitted answers through the current interface.

## Definition changes and historical reconstruction

Deleting a question explicitly deletes its existing answer rows before deleting the question.
Selected-option joins are then removed by cascade.

When a response choice is deleted, database cascade removes selected-option joins referencing that
choice. The parent answer row can remain, potentially with no selected choices. Existing free-text
answers are unaffected.

Question text and option text are mutable in place, and answers do not retain snapshots of the text
shown at submission. Exports and profile display join answers to the current question and option
definitions. Consequently:

- later text edits change the label or option text used to interpret old answers;
- deleted definitions and deleted answer links cannot be reconstructed from these tables;
- the questionnaire concurrency version cannot recreate a historical questionnaire; and
- complete historical reconstruction requires an external archive or audit source not established in
  the reviewed application.

## Interested-participant export

The export endpoint requires study membership or administrator access and `PUBLISHABLE = 1`. It
streams CSV directly to the response and creates no retained server-side export file.

Rows are selected through the interested-participant query, which requires an active quick profile.
The exporter then reads full participant data from the handling process's active-user store.

The CSV contains profile and contact fields, interest date, workflow status, labels, and
questionnaire answers. Questionnaire columns use current question text; selected-choice values use
current option text.

Known implementation concerns:

- The exporter assumes a questionnaire exists and calls `getQuestions()` without a null guard.
- An answer whose question was removed from the current definition cannot be mapped by the current
  export code.
- Free-text and selected-option values receive a trailing tab intended to reduce spreadsheet
  auto-conversion, but there is no general formula-injection neutralization.
- The active-user store is process-local, so stale local profile data can affect a generated export.
- No definitive export audit event is created by this endpoint.

Downloaded files cannot be recalled. Export-file handling after download is outside application
control.

## Export security and audit interpretation

**Current implementation:** The export controller verifies interested-participant study access, sets
CSV response headers, and streams the generated content directly to the browser. Neither the
controller nor the exporter creates a dedicated export audit event, export-job row, or retained
server-side copy.

Participant-list and profile-view PHI events and application request logs may support investigation
by actor and time. They are indirect evidence and do not prove that an export completed, identify the
exact fields or participant rows returned, distinguish failure after response headers were committed,
or establish what happened to the downloaded file.

**Known implementation concern:** Super CSV provides structural CSV quoting, but quoting is not
spreadsheet-formula neutralization. Questionnaire free-text and selected-option values are
HTML-unescaped and receive a trailing tab intended to discourage spreadsheet type or date conversion.
A trailing tab does not neutralize a leading equals sign, plus sign, minus sign, or at sign. Fixed
profile and contact values, labels, questionnaire headers, current option text, and free-text answers
do not pass through one general formula-control policy. Current tests establish ordinary CSV output
but do not exercise formula-leading malicious values.

**Open decisions:** Whether export generation requires a dedicated event and whether exported headers
and cells require formula-injection remediation are institutional privacy, security, and product
decisions. A future event would need defined actor, study, source address, participant scope or count,
request and completion times, result, and failure semantics. A future CSV contract should cover every
exported header and cell and test every supported formula-leading character.

## Audit and retention

Participant list and profile views create PHI audit events. No questionnaire-definition change audit,
answer-change history, export event, or historical definition snapshot was found.

Retention periods for questionnaire definitions, answers, and downloaded exports remain policy and
deployment questions.

## Related pages

- [Expressions of Interest](expressions-of-interest.md)
- [Interested-Participant Management](interested-participant-management.md)
- [Operational Schema](../07-data-model/operational-schema.md)
- [PHI Audit](../08-operations/phi-audit.md)
