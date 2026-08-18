---
title: Eligibility-Criteria Authoring Complexity
summary: Feature engineering, SQL patterns, authoring-era controls, and validation for study eligibility-criteria authoring complexity.
status: mixed
relevant_when:
  - calculating_eligibility_complexity
  - defining_complexity_features
  - building_complexity_sql
  - validating_complexity_scores
canonical_for:
  - eligibility_complexity
  - criteria_complexity_features
---

# Eligibility-Criteria Authoring Complexity

Eligibility-authoring complexity is multidimensional.

A complexity profile should be retained even when a composite score is calculated.

## Complexity dimensions

### Structural complexity

- Number of groups
- Number of clauses
- Number of expressions
- Number of inclusion expressions
- Number of exclusion expressions

### Interaction complexity

- Number of numeric endpoints
- Number of lookup selections
- Number of medical-condition selections
- Number of operator choices
- Number of typeahead selections

### Semantic complexity

- Negated operators
- `ALL_OF` semantics
- OTHER free text
- Participant-facing text length

### Maintenance complexity

- Repeated variables
- Number of groups
- Criteria edits
- Questionnaire dependencies
- Legacy versus current authoring behavior

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

## Current versus legacy authoring data

The criteria database contains expressions created through legacy and current authoring interfaces.

Historically observed operator combinations must not automatically be interpreted as controls exposed by the current UI.

When possible, classify records as:

```text
LEGACY_UI
CURRENT_UI
TRANSITION_OR_UNKNOWN
```

Use the exact current-UI deployment date when available.

Potential analytical flags include:

```text
legacy_operator_combination
unexpected_operator_for_current_ui
missing_expected_lookup
invalid_numeric_format
invalid_range_format
unknown_authoring_era
```

Current UI mappings are documented in [Criterion Operator and Value Reference](../07-data-model/criterion-operator-reference.md).

## Counting guidance

- Count criteria groups using `STUDY_ELIGIBILITY_CRITERION`.
- Count clauses using distinct `CRITERION_CLAUSE.ID`.
- Count expressions using distinct `CRITERION_CLAUSE_EXPRESSION.ID`.
- Count lookups after aggregating at expression level.
- Parse ranges using the colon delimiter.
- Count one-sided numeric criteria as one endpoint.
- Count `BETWEEN` and `NOT_BETWEEN` as two endpoints.
- Classify exclusions using validated negated operators and the OTHER exclusion prefix.
- Treat OTHER text as participant-facing, non-structured matching content.

## Numeric endpoint rules

| Operator | Endpoint count |
|---|---:|
| `GREATER_THAN_OR_EQUAL` | 1 |
| `LESS_THAN_OR_EQUAL` | 1 |
| `NOT_GREATER_THAN_OR_EQUAL` | 1 |
| `NOT_LESS_THAN_OR_EQUAL` | 1 |
| `BETWEEN` | 2 |
| `NOT_BETWEEN` | 2 |

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

This is an analytical starting point rather than an application matching query.

It must be validated against:

- Multiple expression-value rows
- Null values
- Legacy records
- Lookup anomalies
- Current operator vocabulary
- Unicode length behavior

## Candidate composite score

If a single exploratory score is needed:

```text
score =
    w1 × group_count
  + w2 × expression_count
  + w3 × lookup_selection_count
  + w4 × numeric_endpoint_count
  + w5 × medical_condition_selection_count
  + w6 × negated_expression_count
  + w7 × all_of_expression_count
  + w8 × other_text_units
```

Weights must not be treated as objective without validation.

## Validation methods

Possible methods include:

- Expert review
- Regression against cleaned authoring time
- Regression against edit counts
- Factor analysis
- Cross-validation on held-out studies
- User studies

Report both:

- The composite score
- Its component features

## Related pages

- [Study Posting Authoring Telemetry](study-posting-authoring-telemetry.md)
- [AI-Assisted Study Posting Authoring Effectiveness](ai-assisted-study-posting-authoring-effectiveness.md)
- [Criteria Data Model](../07-data-model/criteria-data-model.md)
- [Criteria Query Cookbook](../07-data-model/criteria-query-cookbook.md)
- [Criterion Operator and Value Reference](../07-data-model/criterion-operator-reference.md)
