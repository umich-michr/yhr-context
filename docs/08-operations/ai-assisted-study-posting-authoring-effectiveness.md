---
title: AI-Assisted Study Posting Authoring Effectiveness
summary: Research questions, outcomes, usefulness measures, confounding, analytical designs, and publication considerations.
status: mixed
canonical_for:
  - ai_authoring_effectiveness
  - ai_suggestion_usefulness
  - ai_authoring_research_questions
relevant_when:
  - evaluating_ai_assistance
  - analyzing_suggestion_usefulness
  - comparing_ai_and_manual_workflows
  - designing_publication_analysis
---

# AI-Assisted Study Posting Authoring Effectiveness

The AI-assisted Study Information feature is intended to reduce study-team effort while improving
the usability and completeness of participant-facing study postings.

## Theory of benefit

The feature may improve recruitment setup when it:

- Reuses protocol or consent content already available to the study team
- Reduces manual drafting
- Provides lay-friendly alternatives
- Suggests controlled vocabulary values
- Preserves study-team control over final content
- Fits the team's existing recruitment workflow
- Reduces total effort without reducing posting quality

## Primary evaluation domains

### Adoption

Questions:

- What proportion of eligible attempts enable AI?
- Does adoption differ by:
  - User experience
  - Institutional study role
  - Application study role
  - Department
  - School
  - Participant type
  - Source type
  - Source length?

### Reliability

Questions:

- What proportion of generation attempts succeed?
- What errors occur?
- Are errors associated with:
  - Source type
  - Source size
  - Model
  - Time period
  - Infrastructure changes?
- How much user time is lost after an AI error?
- Do users retry with AI, continue manually, or abandon?

### Suggestion usefulness

Questions:

- Which fields have the highest selection rate?
- Which fields are most often edited after selection?
- Which suggestions are retained unchanged?
- Does usefulness differ by:
  - Text field
  - Lookup field
  - Compensation wording
  - Source type
  - Source length
  - User experience?
- Do users prefer generic or specific compensation wording?
- Does model suggestion rank predict selection?
- Does selection predict final-value similarity?

### Efficiency

Questions:

- Does AI reduce Study Information page time?
- Does AI reduce total posting-creation time?
- Does LLM latency offset drafting-time savings?
- Is any time reduction concentrated among:
  - New users
  - Experienced users
  - Non-PI staff
  - PIs
  - Particular departments
  - Particular source types?
- Does AI affect eligibility-authoring time even though eligibility is not AI assisted?

### Completion

Questions:

- Are AI-assisted attempts more likely to reach final submission?
- Are users more likely to abandon after:
  - Generation failure
  - Long latency
  - Low suggestion usefulness
  - Large source documents?
- How many attempts occur before one study is successfully created?

### Posting quality

Potential measures include:

- Required-field completion
- Public readability
- Text length
- Presence of jargon
- Use of participant-centered language
- Contact completeness
- Topic and location coverage
- Compensation clarity
- Consistency with source content
- Subsequent study-team edits

Quality measures require explicit definitions and validation.

### Recruitment outcomes

Exploratory downstream outcomes may include:

- Public posting views
- Number of exact participant matches
- Number of expressions of interest
- Time to first expression of interest
- Interest rate per posting view
- Study-team promotion activity
- Interested-participant workflow progression

These outcomes are strongly confounded by study population and design. They should not be attributed
to AI without careful adjustment.

## Suggestion funnel

For each field, model:

```text
Suggestion generated
→ Suggestion displayed
→ Suggestion selected
→ Selected value edited or retained
→ Final value submitted
```

Recommended metrics:

```text
generation_coverage
selection_rate
top_rank_selection_rate
retained_unchanged_rate
edited_after_selection_rate
final_matches_any_suggestion_rate
manual_override_rate
```

## Text-field comparison

Text comparison may include:

- Exact equality
- Whitespace-normalized equality
- Character edit distance
- Token overlap
- Semantic similarity
- Readability change
- Length change

Semantic similarity must not replace human review of factual correctness.

## Lookup-field comparison

For topics, locations, and department, compare sets:

```text
suggested
selected
final
```

Useful measures:

- Precision
- Recall
- Jaccard similarity
- Added final values
- Removed selected values
- Retained selected values

## Compensation analysis

Compensation provides a natural decision-analysis domain.

Questions include:

- Are generic suggestions selected more often?
- Are specific suggestions selected more often when the source names an amount?
- Do users remove amounts from specific suggestions?
- Do final postings with specific compensation receive more interest?
- Is that interest associated with lower subsequent eligibility rates or other indicators of
  poor-fit recruitment?

Any analysis of fake or inaccurate profiles requires a defensible operational definition.

## Historical timing comparison

Use Splunk-derived timing to compare pre-feature and post-feature periods.

Before combining timing sources:

- Validate audit versus Splunk agreement
- Document event definitions
- Apply consistent cleaning
- Preserve raw and cleaned values

See [Study Posting Authoring Timing Analysis](study-posting-authoring-timing-analysis.md).

## Confounding factors

Potential confounders include:

- Eligibility complexity
- Study participant type
- Source length
- Source type
- Study-team role
- Prior posting experience
- Login history
- Department and school
- Number of locations
- Number of topics
- Compensation
- PI versus non-PI author
- Study population rarity
- Application release
- Prompt version
- Model version
- Operational incidents

## Analytical designs

### Descriptive analysis

Start with:

- Attempt counts
- Completion rates
- Error rates
- Duration distributions
- Suggestion selection
- Field-level editing
- User feedback

### Adjusted observational analysis

Possible models include:

- Regression adjustment
- Mixed-effects models with repeated users
- Study-level clustered standard errors
- Propensity-score weighting or matching
- Time-period controls
- Department and role stratification

### Interrupted time series

A release-date analysis may examine changes in:

- Study Information completion time
- Total attempt time
- Completion rate

It must account for:

- Other releases
- Seasonal patterns
- Changes in user population
- Logging changes

### Within-user comparison

Users who have both manual and AI-assisted attempts can support a within-user comparison.

This may reduce confounding from stable user characteristics but not from study complexity or
learning over time.

### Sensitivity analysis

Recommended sensitivity analyses include:

- Completed attempts only
- All attempts including abandonment
- Excluding AI errors
- Treating AI errors as AI exposure
- Different timing-outlier rules
- Different complexity adjustments
- First attempt per study
- Successful attempt per study
- First attempt per user
- Current-UI period only

## Publication-oriented research questions

Potential publication questions include:

1. Does AI assistance reduce Study Information authoring time?
1. Which Study Information fields receive the most useful AI suggestions?
1. How does suggestion usefulness vary by user experience and role?
1. Does source type or source length predict generation quality?
1. Does AI assistance increase posting completion?
1. How much of the AI text is retained in final postings?
1. Do users systematically remove or add certain content?
1. Does generic versus specific compensation wording affect user selection or recruitment outcomes?
1. Does eligibility complexity moderate the effect of AI assistance on total creation time?
1. What workflow bottlenecks become visible only after introducing detailed telemetry?
1. Do AI errors lead to abandonment or successful retry?
1. Does source-type agreement between user and LLM predict suggestion usefulness?
1. Are there organizational differences in adoption or benefit?
1. Does the feature disproportionately benefit new or infrequent users?
1. Does AI assistance change participant-facing readability or completeness?

## Avoiding unsupported conclusions

Do not claim that AI caused:

- Faster recruitment
- Better participants
- More accurate eligibility
- Better scientific outcomes

unless the study design and measures support those conclusions.

The feature currently assists posting authoring, not eligibility decision-making.

## Future eligibility AI

Eligibility AI should be evaluated separately because it would affect structured matching logic.

Required future telemetry should include:

- Suggested criteria groups
- Suggested inclusion and exclusion expressions
- Suggested variables
- Suggested operators
- Suggested scalar and lookup values
- Source evidence
- User acceptance
- User edits
- Final criteria
- Match-population changes
- Review time
- Unsupported content mapped to OTHER

Human confirmation must remain required before AI-generated eligibility logic becomes active.

## Related pages

- [AI-Assisted Study Posting Authoring](../05-study-management/ai-assisted-posting-authoring.md)
- [Study-Posting Authoring Audit Model](../07-data-model/study-posting-authoring-audit-model.md)
- [Study Posting Authoring Telemetry](study-posting-authoring-telemetry.md)
- [Study Posting Authoring Timing Analysis](study-posting-authoring-timing-analysis.md)
- [Study Posting Authoring Analysis Dataset](study-posting-authoring-analysis-dataset.md)
- [Eligibility-Criteria Authoring Complexity](eligibility-criteria-authoring-complexity.md)
- [Study Posting Authoring and Analytics Open Questions](../09-decisions/study-posting-authoring-analytics-open-questions.md)
