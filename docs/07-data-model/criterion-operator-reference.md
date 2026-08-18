---
title: Criterion Operator and Value Reference
summary: Authoritative current-UI mappings from criterion controls to stored relational operators and expression values.
status: authoritative
canonical_for:
  - criterion_operator_mapping
  - criterion_value_encoding
  - numeric_range_encoding
  - eligibility_exclusion_encoding
relevant_when:
  - mapping_eligibility_ui_to_storage
  - interpreting_criterion_expressions
  - querying_criterion_values
  - calculating_eligibility_complexity
  - distinguishing_current_and_legacy_criteria
---

# Criterion Operator and Value Reference

This page documents how the current eligibility-authoring UI maps user input to:

- `CRITERION_CLAUSE_EXPRESSION.RELATIONAL_OPERATOR`
- `CRIT_CLAUSE_EXPRESSION_VALUE.SAVED_VALUE`
- `EXPRESSION_VALUE_LOOKUP_VALUE`

The mappings are based on:

- Current inclusion and exclusion authoring forms
- Confirmed frontend behavior
- Confirmed value-serialization rules
- Persisted database examples

## Current UI versus historical data

The application database contains criteria created through:

- A legacy eligibility-authoring UI used approximately from 2013 through 2018
- The current eligibility-authoring UI used from approximately 2018 onward

A variable/operator combination found in historical data does not necessarily mean that the current UI still exposes that combination.

This page distinguishes:

1. Current UI mappings
2. General persisted-value formats
3. Historically observed combinations

Analyses spanning both authoring eras should identify or control for the authoring era when possible.

## Expression storage

A criterion expression combines:

```text
Criterion variable
+ relational operator
+ scalar or lookup value
```

The principal tables are:

```text
CRITERION_CLAUSE_EXPRESSION
CRIT_CLAUSE_EXPRESSION_VALUE
EXPRESSION_VALUE_LOOKUP_VALUE
LOOKUP_VALUE
```

See [Criteria Data Model](criteria-data-model.md) for the complete relational hierarchy.

## Numeric criterion variables

The current eligibility UI supports numeric values for:

```text
AGE
HEIGHT
WEIGHT
BMI
```

## Numeric units and validation

| Variable | Unit | Allowed numeric form |
|---|---|---|
| `AGE` | Years | Nonnegative whole number |
| `HEIGHT` | Inches | Nonnegative whole number |
| `WEIGHT` | Pounds | Nonnegative whole number |
| `BMI` | Unitless BMI value | Nonnegative decimal number |

Additional rules:

- Negative values are rejected by frontend validation.
- Stored numeric values contain no whitespace.
- Numeric values are stored as strings in `SAVED_VALUE`.
- Only `BMI` permits a decimal point.
- Range endpoints use the same unit and numeric rules as single values.

## Numeric scalar and range encoding

For `AGE`, `HEIGHT`, `WEIGHT`, and `BMI`:

| UI input | Inclusion operator | Exclusion operator | `SAVED_VALUE` |
|---|---|---|---|
| Minimum or lower bound only | `GREATER_THAN_OR_EQUAL` | `NOT_GREATER_THAN_OR_EQUAL` | `<lower>` |
| Maximum or upper bound only | `LESS_THAN_OR_EQUAL` | `NOT_LESS_THAN_OR_EQUAL` | `<upper>` |
| Both lower and upper bounds | `BETWEEN` | `NOT_BETWEEN` | `<lower>:<upper>` |

The range delimiter is a colon:

```text
:
```

The lower bound is stored first and the upper bound second.

### Inclusion examples

```text
AGE at least 18

criterion_variable = AGE
relational_operator = GREATER_THAN_OR_EQUAL
saved_value = 18
```

```text
AGE at most 65

criterion_variable = AGE
relational_operator = LESS_THAN_OR_EQUAL
saved_value = 65
```

```text
AGE between 18 and 65

criterion_variable = AGE
relational_operator = BETWEEN
saved_value = 18:65
```

```text
HEIGHT between 60 and 72 inches

criterion_variable = HEIGHT
relational_operator = BETWEEN
saved_value = 60:72
```

```text
WEIGHT at least 100 pounds

criterion_variable = WEIGHT
relational_operator = GREATER_THAN_OR_EQUAL
saved_value = 100
```

```text
BMI at most 24.9

criterion_variable = BMI
relational_operator = LESS_THAN_OR_EQUAL
saved_value = 24.9
```

### Exclusion examples

```text
Exclude participants whose AGE is between 80 and 99

criterion_variable = AGE
relational_operator = NOT_BETWEEN
saved_value = 80:99
```

```text
Exclude participants whose AGE is at least 75

criterion_variable = AGE
relational_operator = NOT_GREATER_THAN_OR_EQUAL
saved_value = 75
```

```text
Exclude participants whose WEIGHT is at most 100 pounds

criterion_variable = WEIGHT
relational_operator = NOT_LESS_THAN_OR_EQUAL
saved_value = 100
```

## Date-value encoding

The generic criterion model also contains date-related variables:

```text
DATE_OF_BIRTH
DUE_DATE
```

Date values are submitted by the frontend and stored in a `VARCHAR2`-based `SAVED_VALUE` using:

```text
yyyy-mm-dd
```

Example:

```text
2026-03-24
```

These variables are part of the generic criterion-variable vocabulary. Their presence in `CRITERION_VARIABLE` does not mean that they are exposed by the current eligibility-authoring form.

## Lookup-backed expressions

Lookup-backed criteria store selected values through:

```text
CRIT_CLAUSE_EXPRESSION_VALUE
→ EXPRESSION_VALUE_LOOKUP_VALUE
→ LOOKUP_VALUE
```

For these expressions:

- The relational operator is stored on `CRITERION_CLAUSE_EXPRESSION`.
- Selected values are stored as lookup relationships.
- `SAVED_VALUE` is not used for the selected lookup values.

## Current inclusion-control mappings

| Current inclusion UI control | Criterion variable | Stored operator | Value storage |
|---|---|---|---|
| Biological sex at birth | `GENDER` | `ANY_OF` | `GENDER` lookups |
| Race | `RACE` | `ANY_OF` | `RACE` lookups |
| Currently has any selected condition | `PRESENT_MEDICAL_CONDITION` | `ANY_OF` | `MEDICAL_CONDITION` lookups |
| Currently has all selected conditions | `PRESENT_MEDICAL_CONDITION` | `ALL_OF` | `MEDICAL_CONDITION` lookups |
| Previously had any selected condition | `PAST_MEDICAL_CONDITION` | `ANY_OF` | `MEDICAL_CONDITION` lookups |
| Previously had all selected conditions | `PAST_MEDICAL_CONDITION` | `ALL_OF` | `MEDICAL_CONDITION` lookups |
| Willing to change medications or treatments | `WILLING_TO_CHANGE_MEDICATIONS` | `EQUAL` | `BOOLEAN` lookup |
| Willing to take experimental drugs | `WILLING_TO_TAKE_EXPERIMENTAL_DRUGS` | `EQUAL` | `BOOLEAN` lookup |
| Has metal implants | `HAS_METAL_IMPLANTS` | `EQUAL` | `BOOLEAN` lookup |
| Smoking status | `SMOKING_STATUS` | `ANY_OF` | `SMOKING_STATUS` lookups |
| Parent or guardian of a child under 18 | `PARENT_OR_GUARDIAN_OF_A_CHILD` | `EQUAL` | `BOOLEAN` lookup |
| Fluent in English | `FLUENCY_IN_ENGLISH` | `EQUAL` | `FLUENT_ENGLISH` lookup |

Numeric inclusion controls use the mappings defined in [Numeric scalar and range encoding](#numeric-scalar-and-range-encoding).

## Current exclusion-control mappings

| Current exclusion UI control | Criterion variable | Stored operator | Value storage |
|---|---|---|---|
| Pregnant at the time of enrollment | `PREGNANT_AT_THE_TIME_OF_ENROLLMENT` | `NOT_EQUAL` | `BOOLEAN` lookup |
| Currently has any selected condition | `PRESENT_MEDICAL_CONDITION` | `NOT_ANY_OF` | `MEDICAL_CONDITION` lookups |
| Currently has all selected conditions | `PRESENT_MEDICAL_CONDITION` | `NOT_ALL_OF` | `MEDICAL_CONDITION` lookups |
| Previously had any selected condition | `PAST_MEDICAL_CONDITION` | `NOT_ANY_OF` | `MEDICAL_CONDITION` lookups |
| Previously had all selected conditions | `PAST_MEDICAL_CONDITION` | `NOT_ALL_OF` | `MEDICAL_CONDITION` lookups |
| Has metal implants | `HAS_METAL_IMPLANTS` | `NOT_EQUAL` | `BOOLEAN` lookup |
| Excluded smoking status | `SMOKING_STATUS` | `NOT_ANY_OF` | `SMOKING_STATUS` lookups |
| Not fluent in English | `FLUENCY_IN_ENGLISH` | `NOT_EQUAL` | `FLUENT_ENGLISH` lookup |

Numeric exclusion controls use the negated mappings defined in [Numeric scalar and range encoding](#numeric-scalar-and-range-encoding).

The current exclusion form does not expose every criterion variable available in the generic criteria model.

## Medical-condition operators

The medical-condition UI allows the study team to select:

```text
ANY
ALL
```

For inclusion criteria:

| UI choice | Stored operator |
|---|---|
| Any selected condition | `ANY_OF` |
| All selected conditions | `ALL_OF` |

For exclusion criteria:

| UI choice | Stored operator |
|---|---|
| Any selected condition | `NOT_ANY_OF` |
| All selected conditions | `NOT_ALL_OF` |

Selected conditions are stored as `MEDICAL_CONDITION` lookup relationships.

Medical-condition selections are drawn from the current visible `MEDICAL_CONDITION` lookup vocabulary.

The available values and vocabulary size may change as lookup reference data is maintained.

## Boolean expressions

Boolean controls use a lookup value rather than storing the words `true` or `false` directly in `SAVED_VALUE`.

The meaning of a Boolean expression depends on:

- The selected Boolean lookup value
- The relational operator
- Inclusion or exclusion mode

Examples:

```text
HAS_METAL_IMPLANTS EQUAL TRUE
```

means that having metal implants is an inclusion requirement.

```text
HAS_METAL_IMPLANTS NOT_EQUAL TRUE
```

means that participants who have metal implants are excluded.

## `OTHER` expressions

`OTHER` stores participant-facing free text.

The relational operator is null:

```text
criterion_variable = OTHER
relational_operator = NULL
```

### Inclusion OTHER

For inclusion text, `SAVED_VALUE` contains the participant-facing text without a special prefix.

Example:

```text
"Trainers" must currently be working with clients in a local gym.
```

### Exclusion OTHER

For exclusion text, `SAVED_VALUE` begins with:

```text
$#exclusion#$
```

Example:

```text
$#exclusion#$Completed allogeneic stem cell transplantation
```

The prefix allows the application to distinguish OTHER inclusion text from OTHER exclusion text even though both have a null relational operator.

The prefix is an internal application encoding and is not participant-facing text.

The matching engine does not directly evaluate OTHER free text.

## Historically observed operator combinations

The database contains criteria created by both legacy and current interfaces.

Historically observed operators include:

```text
ANY_OF
ALL_OF
EQUAL
BETWEEN
GREATER_THAN_OR_EQUAL
LESS_THAN_OR_EQUAL
NOT_ANY_OF
NOT_ALL_OF
NOT_EQUAL
NOT_BETWEEN
NOT_GREATER_THAN_OR_EQUAL
NOT_LESS_THAN_OR_EQUAL
NULL for OTHER
```

Some historically observed combinations may not be creatable through the current UI.

Examples include:

- `RACE` with `ALL_OF`
- Boolean expressions without an associated lookup value
- Operator combinations produced by the legacy authoring interface

Historical observations must not be used by themselves to define current UI behavior.

## Legacy-data analysis

Criteria analyses spanning legacy and current authoring periods should derive an authoring-era category when possible:

```text
LEGACY_UI
CURRENT_UI
TRANSITION_OR_UNKNOWN
```

The exact current-UI deployment date should be used when available.

If only the year is known, records from the transition period should not be assigned to one UI generation without additional evidence.

## Data-quality considerations

Potential data-quality conditions include:

```text
missing_expected_lookup
unexpected_operator_for_current_ui
invalid_numeric_format
invalid_range_format
negative_numeric_value
unexpected_decimal_value
legacy_operator_combination
unknown_authoring_era
OTHER_exclusion_missing_prefix
OTHER_inclusion_with_exclusion_prefix
```

These are analytical data-quality classifications, not necessarily application status values.

## Related pages

- [Criterion Variable Reference](criterion-variable-reference.md)
- [Criteria Data Model](criteria-data-model.md)
- [Eligibility-Criteria Authoring](../06-recruitment/eligibility-criteria-authoring.md)
- [Criteria Query Cookbook](criteria-query-cookbook.md)
- [Matching and Visibility](../06-recruitment/matching-and-visibility.md)
- [Eligibility-Criteria Authoring Complexity](../08-operations/ai-assisted-study-posting-authoring-effectiveness.md)
- [Eligibility-Criteria Authoring Complexity](../08-operations/ai-assisted-study-posting-authoring-effectiveness.md)
