---
title: Expressions of Interest
summary: Temporal profile updates, eligibility recheck, questionnaire completion, and retained interest.
status: authoritative
relevant_when:
  - participant_expresses_interest
  - participant_fails_eligibility_recheck
  - explaining_temporal_profile_updates
  - explaining_historical_interest
---

# Expressions of Interest

An expression of interest is an explicit participant action indicating interest in a study.

Participants cannot withdraw a finalized expression of interest.

## Preconditions

Before interest can be finalized:

- The participant account must be active.
- The study must be active.
- The participant must provide current values for required temporal profile properties.
- The eligibility recheck must produce `TRUE` or `MAYBE`.
- The participant must complete the study's screening questionnaire when one is configured.

## Temporal profile refresh

When a participant selects the interest action, the application asks the participant to update profile information that may change over time.

The temporal properties include:

- Past medical conditions
- Present medical conditions
- Whether the participant is a parent or guardian of a child under 18

The parent-or-guardian property is collected as a Boolean radio-button response.

The eligibility recheck uses the refreshed profile information.

## Eligibility recheck

The application does not rely solely on an earlier stored match.

It reevaluates eligibility at the time the participant attempts to express interest.

If the eligibility recheck returns `FALSE`:

- The participant cannot complete the expression of interest.
- The application displays a message explaining that the participant cannot show interest because they are not eligible.

## Successful interest workflow

When the eligibility recheck returns `TRUE` or `MAYBE`:

1. The application presents the screening questionnaire, if configured.
2. The participant answers all required questions.
3. The participant may leave optional questions unanswered.
4. The participant submits the questionnaire.
5. The application creates and finalizes the expression of interest.
6. Permitted participant and questionnaire data becomes available to the authorized study team.

## Sequence diagram

```mermaid
sequenceDiagram
    participant P as Participant
    participant A as Application
    participant M as Matching Service
    participant Q as Screening Questionnaire
    participant ST as Study Team

    P->>A: Select interest action
    A-->>P: Request temporal profile updates
    P->>A: Submit current temporal values
    A->>M: Recheck eligibility

    alt TRUE or MAYBE
        M-->>A: Can proceed

        opt Study has a questionnaire
            A-->>P: Display questionnaire
            P->>Q: Answer required and optional questions
            Q-->>A: Submit completed questionnaire
        end

        A->>A: Recheck study status
        A->>A: Commit profile updates, optional questionnaire, and interest
        A-->>ST: Show permitted participant data
    else FALSE
        M-->>A: Ineligible
        A-->>P: Cannot express interest because not eligible
    end
```

## Questionnaire completion

Questionnaire completion is required to finalize the interest workflow when the study has a questionnaire.

Completion means:

- Every required question has an answer.
- Optional questions may be left unanswered.
- The participant submits the questionnaire.

An incomplete questionnaire cannot be saved or resumed.

## Interest-record timing

The application creates the interest record only after:

- The participant passes the eligibility recheck with `TRUE` or `MAYBE`.
- The study remains active.
- The participant successfully completes the screening questionnaire, when one is configured.

A study without a screening questionnaire does not require questionnaire submission.

The application does not create a pending interest record.

A failed or abandoned questionnaire produces no interest record.

The following applicable changes are committed in one transaction:

- Temporal-profile updates
- Questionnaire submission, when a questionnaire exists
- Finalized expression of interest

If the eligibility recheck, study-status recheck, questionnaire submission, or a later workflow step fails, none of those changes are saved.

## Participant withdrawal

Participants cannot withdraw a finalized expression of interest through the application.

There is no administrative application workflow for correcting an accidental expression of interest.

Such requests may be raised with support, but they are not handled by a defined application feature.

## Study status at submission

The application rechecks study status when the participant submits the interest workflow.

If the study is no longer active at submission, whether because of its date range or because `PUBLISHABLE` became `0`:

- Interest is not finalized.
- Temporal-profile and questionnaire changes in the transaction are not saved.
- The participant sees a message that the study is no longer recruiting.

## Eligibility changes after interest

After interest is finalized:

- Later participant-profile changes do not remove the interest.
- Later study eligibility-criteria changes do not remove the interest.
- The application does not reevaluate the completed interest relationship.
- The participant remains in the interested-participant history even if they would now be ineligible.

## Participant deactivation after interest

If the participant account becomes deactivated:

- The historical interest remains.
- The participant profile is hidden from the study team.
- New interactions are blocked.

## Study inactivity after interest

If the study becomes inactive because its date range no longer includes the current date, but `PUBLISHABLE = 1`:

- The historical interest remains.
- New expressions of interest are blocked.
- New matching stops.
- Authorized study team members may continue to access and export historical interested-participant data.

If `PUBLISHABLE = 0`:

- The historical interest remains.
- Participant information is not accessible to the study team.
- New participant-data exports are blocked.

Historical relationship retention, active recruitment, and participant-data access are separate concepts.

## Relationship to Ask if interested

Ask if interested does not create an expression of interest.

It only promotes the study in the participant interface.

The participant must still:

- Select the interest action
- Refresh temporal profile values
- Pass the eligibility recheck
- Complete the questionnaire workflow
- Submit while the study remains active

## Related pages

- [Matching and visibility](matching-and-visibility.md)
- [Ask if interested](ask-if-interested.md)
- [Questionnaires and exports](questionnaires-and-exports.md)
- [Study lifecycle](../05-study-management/study-lifecycle.md)
