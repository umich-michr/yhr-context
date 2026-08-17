---
title: Authoring Telemetry and Complexity Analysis
summary: Telemetry sources, data cleaning, eligibility-complexity features, and AI-feature evaluation.
status: mixed
relevant_when:
  - evaluating_ai_assisted_authoring
  - measuring_eligibility_complexity
  - analyzing_form_time
  - investigating_authoring_bottlenecks
---

# Authoring Telemetry and Complexity Analysis

Application data, audit records, and application logs can be combined to study:

- Authoring effort
- Workflow bottlenecks
- Feature adoption
- AI-assistance effectiveness
- Study-posting abandonment
- Eligibility-criteria complexity
- Performance problems
- Opportunities for future automation

This page distinguishes implemented telemetry from proposed analytical measures.

## Analysis goals

Potential questions include:

- Which authoring stage takes the most time?
- Does eligibility complexity predict authoring time?
- Does AI assistance reduce Study Information form time?
- Does AI assistance reduce total creation time?
- Does AI assistance change abandonment rates?
- Which criterion variables are hardest to author?
- Do studies with many medical-condition selections take longer?
- Does OTHER free text indicate missing structured variables?
- Which studies produce slow matching recalculations?
- Which enhancements have measurable effects?

## Data sources

### Operational database

Relevant operational data includes:

- Study properties
- Criteria groups
- Clauses
- Expressions
- Scalar expression values
- Lookup selections
- Final saved study values
- Posting status
- Creator
- Creation and submission timestamps

### Posting audit tables

Relevant audit entities include:

```text
STUDY_POSTING_AUDIT
STUDY_POSTING_GENERATION_AUDIT
```

These records may contain:

- Posting-attempt identifiers
- Study number
- AI-use indicator
- Generated suggestions
- Selected suggestions
- Final values
- User feedback
- Form timing
- Final-submission status

Exact physical fields must be verified.

### Application and Splunk logs

Application logs may contain:

- Request timestamps
- Endpoint
- User
- Study number
- Client IP
- Response status
- Error information
- Request duration
- Workflow events

A derived Splunk export may contain:

```text
_time
user
clientip
study_num
study_creation_time_mins
study_information_time_mins
study_eligibility_criterion_time_mins
```

The exact export schema depends on the Splunk query and should be versioned with the analysis.

## Correlation keys

Potential correlation keys include:

- `study_num`
- `study_posting_audit.id`
- Application user ID
- Request ID
- Session ID
- Event timestamp

`study_num` alone may be insufficient when:

- One user makes several attempts
- A workflow is resumed
- Several users edit one posting
- Events occur before final creation

A posting-attempt ID or request correlation ID is preferable when available.

## Privacy considerations

Telemetry may contain:

- User identifiers
- Email addresses
- Client IP addresses
- Study identifiers
- Uploaded-document metadata
- Generated text
- Source text
- Error information

Analysis datasets should contain only the fields needed for the approved analytical purpose.

Client IP should normally be removed or transformed unless specifically required.

## Timing-data quality

Timing values may contain:

- Negative durations
- Extremely large durations
- Idle browser time
- Multiple tabs
- Interrupted sessions
- Repeated submissions
- Client-clock errors
- Missing events
- Retries
- Automated traffic

A negative duration is invalid.

An extremely large duration may represent an abandoned browser session rather than active authoring.

## Recommended timing-cleaning process

A reproducible process should:

1. Preserve the raw duration.
2. Mark negative durations invalid.
3. Mark missing durations.
4. Define a plausible active-session limit.
5. Investigate extreme values before excluding them.
6. Report results with and without outliers.
7. Distinguish trimming from winsorization.
8. Avoid selecting a percentile threshold solely because it produces favorable results.
9. Record a cleaning-rule version.

Suggested derived fields:

```text
raw_duration_minutes
duration_valid
duration_invalid_reason
duration_clean_minutes
duration_outlier_flag
cleaning_rule_version
```

## Complexity is multidimensional

### Structural complexity

Examples:

- Number of groups
- Number of clauses
- Number of expressions
- Number of inclusion expressions
- Number of exclusion expressions

### Interaction complexity

Examples:

- Number of range endpoints
- Number of checkbox selections
- Number of lookup selections
- Number of operator choices
- Number of typeahead selections

### Semantic complexity

Examples:

- Medical-condition vocabulary use
- Negation
- `ALL_OF` semantics
- Unsupported OTHER text
- Long participant-facing text

### Matching complexity

Examples:

- Number of expressions
- Number of lookup comparisons
- Number of active participants
- Number of groups
- Number of recalculations

### Maintenance complexity

Examples:

- Number of groups
- Number of repeated variables
- Number of OTHER criteria
- Frequency of edits
- Questionnaire dependencies

A single total score can hide these dimensions.

A complexity profile should generally be retained even when a composite score is calculated.

## Recommended study-level features

```text
group_count
clause_count
expression_count
inclusion_expression_count
exclusion_expression_count
distinct_variable_count
lookup_selection_count
medical_condition_selection_count
numeric_endpoint_count
range_expression_count
negated_expression_count
other_expression_count
other_character_count
all_of_expression_count
partial_match_capable_expression_count
```

## Inclusion-versus-exclusion classification

Exclusions may be identified by:

- A relational operator beginning with `NOT`
- Another known negating operator
- An OTHER value beginning with `$#exclusion#$`

The classification must be validated against production operator values.

## Numeric endpoint count

Examples:

```text
AGE >= 18
endpoint count = 1
```

```text
AGE BETWEEN 18 AND 65
endpoint count = 2
```

The application-specific range encoding must be used when parsing endpoints.

## Lookup-selection count

Lookup values must be counted at the expression level.

Example:

```text
One PRESENT_MEDICAL_CONDITION expression
with five selected conditions
```

should produce:

```text
expression_count = 1
lookup_selection_count = 5
```

## Medical-condition interaction units

A proposed measure is:

```text
medical_condition_interaction_units =
    selected_condition_count
    + operator_selection_count
```

This is a proposed analytical feature, not a current application metric.

## OTHER text complexity

A simple proposed measure is:

```text
other_text_units = ceiling(character_count / 100)
```

This is easy to calculate but is not a validated measure of cognitive difficulty.

Alternatives include:

- Word count
- Sentence count
- Readability
- Number of concepts
- Presence of negation
- Manual categorization of unsupported structured concepts

## Proposed complexity profile

```text
Structural:
    groups
    clauses
    expressions
    distinct variables

Interaction:
    numeric endpoints
    lookup selections
    medical-condition selections
    operator choices
    OTHER text units

Logical:
    negations
    ALL_OF expressions
    alternative groups
    partial-match-capable expressions

Display:
    participant-facing criterion count
    OTHER text length
```

## Candidate composite score

If a single score is required, begin with a transparent exploratory formula:

```text
Candidate Eligibility Authoring Complexity Score =
    w1 × group_count
  + w2 × expression_count
  + w3 × lookup_selection_count
  + w4 × numeric_endpoint_count
  + w5 × medical_condition_selection_count
  + w6 × negated_expression_count
  + w7 × all_of_expression_count
  + w8 × other_text_units
```

The weights must not be treated as objective without validation.

Possible validation methods include:

- Expert review
- Regression against cleaned authoring time
- Regression against edit count
- User studies
- Factor analysis
- Cross-validation against held-out studies

Report both the composite score and its component features.

## Expression-level SQL base

```sql
WITH expression_base AS (
    SELECT
        s.study_num,
        sec.id AS criterion_id,
        cc.id AS clause_id,
        cce.id AS expression_id,
        cv.name AS variable_name,
        cce.relational_operator,
        MAX(ccev.saved_value) AS saved_value,
        COUNT(DISTINCT evlv.lookup_value_id) AS lookup_value_count,
        CASE
            WHEN cce.relational_operator LIKE 'NOT%'
                THEN 1
            WHEN MAX(ccev.saved_value) LIKE '$#exclusion#$%'
                THEN 1
            ELSE 0
        END AS exclusion_flag
    FROM study s
    JOIN study_eligibility_criterion sec
        ON sec.study_id = s.id
    JOIN criterion_clause cc
        ON cc.criterion_id = sec.id
    JOIN criterion_clause_expression cce
        ON cce.clause_id = cc.id
    LEFT JOIN criterion_variable cv
        ON cv.id = cce.criterion_variable_id
    LEFT JOIN crit_clause_expression_value ccev
        ON ccev.criterion_clause_expression_id = cce.id
    LEFT JOIN expression_value_lookup_value evlv
        ON evlv.crit_clause_expr_value_id = ccev.id
    GROUP BY
        s.study_num,
        sec.id,
        cc.id,
        cce.id,
        cv.name,
        cce.relational_operator
)
SELECT
    study_num,
    COUNT(DISTINCT criterion_id) AS group_count,
    COUNT(DISTINCT clause_id) AS clause_count,
    COUNT(DISTINCT expression_id) AS expression_count,
    COUNT(DISTINCT variable_name) AS distinct_variable_count,
    SUM(lookup_value_count) AS lookup_selection_count,
    SUM(exclusion_flag) AS exclusion_expression_count,
    SUM(
        CASE
            WHEN variable_name = 'OTHER' THEN 1
            ELSE 0
        END
    ) AS other_expression_count,
    SUM(
        CASE
            WHEN variable_name = 'OTHER'
                THEN CEIL(
                    LENGTH(
                        REPLACE(saved_value, '$#exclusion#$', '')
                    ) / 100
                )
            ELSE 0
        END
    ) AS other_text_units
FROM expression_base
GROUP BY study_num;
```

This query is an analytical starting point and must be validated for:

- Multiple expression-value rows
- Null values
- Prefix removal
- Unicode character counting
- Operator vocabulary
- Range encoding
- Production-data anomalies

## AI-effectiveness measures

### Adoption

- Percentage of eligible attempts using AI
- Adoption by institution
- Adoption by study type
- Repeat use by the same user

### Generation reliability

- Successful generation rate
- Error rate
- Timeout rate
- Document-extraction failure rate
- Empty suggestion rate

### Suggestion usefulness

- Suggestion selection rate
- Field-level selection rate
- Selected-without-edit rate
- Selected-then-edited rate
- Final-value overlap with suggestions
- User feedback

### Workflow outcomes

- Study Information form time
- Eligibility form time
- Total creation time
- Final-submission rate
- Abandonment rate
- Number of sessions
- Number of corrections

## Controlling for eligibility complexity

The current AI feature affects study information rather than eligibility authoring.

Total posting time can still be heavily affected by eligibility complexity.

A model may include:

```text
Outcomes:
    study_information_time
    eligibility_time
    total_creation_time

Predictors:
    AI use
    source type
    source length
    user experience
    eligibility complexity profile
    study type
    institution
```

Study Information time is the most direct timing outcome for the current AI feature.

## Causal limitations

An unadjusted comparison between AI-assisted and manual attempts does not establish causation.

Potential confounders include:

- Study complexity
- Source-document length
- Source-document quality
- User experience
- Number of sessions
- Interruptions
- Study type
- Failed generation attempts

Possible stronger approaches include:

- Matched comparisons
- Regression adjustment
- Interrupted time-series analysis
- Staged rollout analysis
- Controlled evaluation when feasible

## Future eligibility-AI telemetry

If AI-assisted eligibility authoring is implemented, capture:

- Suggested groups
- Suggested inclusion expressions
- Suggested exclusion expressions
- Suggested variables
- Suggested operators
- Suggested scalar values
- Suggested lookup values
- User acceptance
- User edits
- Deleted suggestions
- Added manual criteria
- Final structured criteria
- Unsupported statements mapped to OTHER
- Time spent reviewing suggestions

## Related pages

- [AI-Assisted Study Posting Authoring](../05-study-management/ai-assisted-posting-authoring.md)
- [Eligibility-Criteria Authoring](../06-recruitment/eligibility-criteria-authoring.md)
- [Criteria Data Model](../07-data-model/criteria-data-model.md)
- [Study Property Model](../07-data-model/study-property-model.md)
- [Audit and Monitoring](audit-and-monitoring.md)
- [Authoring and Analytics Open Questions](../09-decisions/authoring-analytics-open-questions.md)