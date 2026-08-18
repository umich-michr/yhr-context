---
title: AI-Assisted Study Posting Authoring Effectiveness
summary: Adoption, reliability, usefulness, outcomes, confounders, and evaluation designs for AI-assisted study-posting authoring.
status: mixed
relevant_when:
  - evaluating_ai_assistance
  - analyzing_suggestion_usefulness
  - comparing_ai_vs_manual_workflows
  - designing_ai_evaluation_methodology
---

# AI-Assisted Study Posting Authoring Effectiveness

This page covers methods for evaluating AI-assisted study-information authoring.

## Core outcomes

- Adoption rate
- Generation success/error/timeout rates
- Suggestion selection and edit behavior
- User feedback
- Study-information time
- Eligibility time
- Total creation time
- Final-submission and abandonment rates

## Suggested metric groups

### Adoption

- AI usage among eligible attempts
- Adoption by institution and study type
- Repeat usage by user

### Generation reliability

- Success rate
- Error rate
- Timeout rate
- Document-extraction failure rate
- Empty-suggestion rate

### Suggestion usefulness

- Field-level selection rate
- Selected-without-edit rate
- Selected-then-edited rate
- Final-value overlap
- Feedback distributions

### Workflow outcomes

- Stage durations
- Completion/abandonment
- Session count and retries

## Confounders and causal limits

Unadjusted AI-vs-manual comparisons do not establish causation.

Potential confounders:

- Study complexity
- Source length/quality
- User experience
- Interruptions
- Study type
- Failed generation attempts

## Better evaluation designs

- Regression adjustment
- Matched comparisons
- Interrupted time series
- Staged rollout comparisons
- Controlled evaluations when feasible

## Interaction with eligibility complexity

Current AI support focuses on study-information authoring, but total creation time is still affected by eligibility complexity.

Modeling should separate:

- Study-information outcomes (most direct AI effect)
- Eligibility outcomes
- Total workflow outcomes

## Future telemetry for eligibility AI

If eligibility authoring is AI-assisted in the future, capture:

- Suggested groups/expressions/operators/values
- Acceptance and edit actions
- Deleted AI suggestions
- Added manual criteria
- Review time
- Final structured criteria
- OTHER mappings

## Related pages

- [AI-Assisted Study Posting Authoring](../05-study-management/ai-assisted-posting-authoring.md)
- [Study Posting Authoring Telemetry](study-posting-authoring-telemetry.md)
- [Eligibility-Criteria Authoring Complexity](eligibility-criteria-authoring-complexity.md)
