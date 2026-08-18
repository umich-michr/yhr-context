---
title: Criteria Query Cookbook
summary: SQL patterns and data-quality checks for eligibility-criteria analysis.
status: mixed
relevant_when:
  - writing_eligibility_sql
  - flattening_criteria
  - calculating_complexity_features
  - validating_criteria_data
---

# Criteria Query Cookbook

This page collects SQL and validation patterns for criteria analytics.

## Flattened eligibility query

```sql
SELECT
    s.study_num,
    sec.id AS criterion_id,
    sec.name AS criterion_group_name,
    sec.order_num AS criterion_order_num,
    cc.id AS clause_id,
    cc.expression_logical_connector,
    cc.clause_logical_connector,
    cc.order_num AS clause_order_num,
    cce.id AS expression_id,
    cce.order_num AS expression_order_num,
    cv.name AS criterion_variable,
    cce.relational_operator,
    ccev.id AS expression_value_id,
    ccev.saved_value,
    LISTAGG(lv.display_text, '; ')
        WITHIN GROUP (ORDER BY lv.display_text) AS lookup_values
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
LEFT JOIN lookup_value lv
    ON lv.id = evlv.lookup_value_id
WHERE (:study_num IS NULL OR s.study_num = :study_num)
GROUP BY
    s.study_num,
    sec.id,
    sec.name,
    sec.order_num,
    cc.id,
    cc.expression_logical_connector,
    cc.clause_logical_connector,
    cc.order_num,
    cce.id,
    cce.order_num,
    cv.name,
    cce.relational_operator,
    ccev.id,
    ccev.saved_value
ORDER BY
    sec.order_num,
    cc.order_num,
    cce.order_num,
    ccev.id;
```

## Safe expression-level aggregation

One expression may have multiple lookup rows.

Counting joined rows directly will overcount expressions.

Aggregate to the expression level first:

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
        COUNT(DISTINCT evlv.lookup_value_id) AS lookup_value_count
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
    SUM(lookup_value_count) AS lookup_selection_count
FROM expression_base
GROUP BY study_num;
```

## Preliminary exclusion detection

```sql
CASE
    WHEN cce.relational_operator LIKE 'NOT%'
        THEN 1
    WHEN ccev.saved_value LIKE '$#exclusion#$%'
        THEN 1
    ELSE 0
END
```

This logic must be validated against the complete production operator vocabulary.

## Data-quality checks

Useful checks include:

- Clause without a valid criterion root
- Expression without a clause
- Expression without a criterion variable
- Unsupported relational operator
- Missing required scalar value
- Missing required lookup selection
- Unexpected scalar and lookup combination
- Invalid range encoding
- Empty OTHER text
- Exclusion prefix without text
- Duplicate lookup selection
- Unexpected expression connector
- More than one clause in data authored by the current UI
