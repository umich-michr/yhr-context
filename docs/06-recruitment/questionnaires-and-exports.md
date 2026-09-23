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

A study may have zero or one screening questionnaire.

## Purpose

The questionnaire captures study-specific information during the expression-of-interest transaction.

Questionnaire answers:

- Are not used by matching
- Are not used to resolve partial eligibility
- Are shown to authorized study team members
- Are included in CSV exports

## Question types

Supported question types are:

| Type             | Participant response         |
| ---------------- | ---------------------------- |
| Single-line text | Short free text              |
| Paragraph text   | Longer free text             |
| Checkboxes       | One or more selected options |
| Multiple choice  | One selected option          |
| Dropdown         | One selected option          |

Each question may include:

- Question text
- Optional help text
- Required or optional status
- Display order
- Response options when required by the question type

## Active-study editing restriction

The questionnaire cannot be edited while the study is active.

## Inactive-study editing

While the study is inactive, study team members may:

- Add questions
- Edit question text
- Edit help text
- Change required status
- Reorder questions
- Add response options
- Edit response-option text
- Delete response options
- Delete questions

Question type cannot be changed after creation.

## Response deletion effects

Deleting a response option:

- Deletes stored answers selecting that option
- Does not delete the complete questionnaire submission
- Does not delete unrelated answers

Deleting a question:

- Requires confirmation
- Deletes answers associated with that question

Questionnaires and answers are not versioned.

## Concurrent editing

When multiple study members edit the questionnaire concurrently:

1. The first valid submission succeeds.
1. A later stale submission is rejected.
1. The later editor must refresh.
1. Unsaved changes from the rejected edit are not preserved.

## Participant submission

The questionnaire is displayed in the same show-interest form as the temporal profile review.

When a questionnaire exists:

- Required questions must be answered
- Optional questions may be unanswered
- The complete form is submitted in one request
- Questionnaire capture and interest creation occur in one transaction

Participants cannot save and resume an incomplete show-interest questionnaire.

Participants cannot edit submitted answers.

## Export contents

Authorized study team members may export:

- All visible participant profile fields
- Contact information
- Questionnaire answers
- Interested-participant workflow-list information
- Applied labels

## Export availability

Historical interested-participant data may be exported while `PUBLISHABLE = 1`, including when the
study is inactive by date.

Participant deactivation hides that participant's information from new exports.

`PUBLISHABLE = 0` blocks participant-data access and new exports.

Exports are generated in memory and streamed to the browser.

The application does not retain a server-side export file or definitive export audit event.

Downloaded files cannot be recalled.

## Related pages

- [Expressions of Interest](expressions-of-interest.md)
- [Interested-Participant Management](interested-participant-management.md)
- [Study Lifecycle](../05-study-management/study-lifecycle.md)
- [PHI Audit](../08-operations/phi-audit.md)
