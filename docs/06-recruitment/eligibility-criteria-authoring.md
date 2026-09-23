---
title: Eligibility-Criteria Authoring
summary: Current UI behavior and the distinction between UI constraints and the more flexible criteria data model.
status: authoritative
canonical_for:
  - eligibility_authoring_ui
  - inclusion_criteria_authoring
  - exclusion_criteria_authoring
  - criteria_group_authoring
relevant_when:
  - authoring_inclusion_criteria
  - authoring_exclusion_criteria
  - explaining_criteria_groups
  - understanding_eligibility_ui
---

# Eligibility-Criteria Authoring

Study eligibility criteria determine whether a participant is an exact match, a partial match, or
not a match.

The underlying data model supports more complex criteria and clause structures than the current
authoring interface exposes.

## Who to recruit

The study team must select at least one:

- Healthy participants
- Participants with specific conditions

Both may be selected.

Leaving both choices blank is invalid and does not imply both participant types.

## Criteria groups or arms

A study may define zero or more criteria groups.

A group is saved only when it contains at least one criterion expression.

The application does not create an empty default group.

Groups are alternatives:

```text
Study eligibility =
    Group 1 qualifies
    OR Group 2 qualifies
    OR ...
```

If no groups are saved, the study has no group-specific structured eligibility expressions.

## Inclusion and exclusion in one group

The Inclusion and Exclusion tabs belong to the same group editor.

Unsaved values are preserved when switching tabs.

Inclusion and exclusion values are submitted together to save one group.

## Inclusion logic

Within a group, current-UI inclusion expressions use:

```text
AND
```

Conceptually:

```text
Inclusion result =
    Expression 1
    AND Expression 2
    AND ...
```

Blank controls do not add an expression and therefore do not restrict the participant for that
property.

## Exclusion logic

Exclusion controls represent conditions that disqualify a participant.

Structured exclusions are persisted using negated operators such as:

```text
NOT_EQUAL
NOT_ANY_OF
NOT_ALL_OF
NOT_GREATER_THAN_OR_EQUAL
NOT_LESS_THAN_OR_EQUAL
NOT_BETWEEN
```

Conceptually:

```text
Group qualifies =
    all inclusion requirements are satisfied
    AND no exclusion condition applies
```

## Current UI sections

Current controls include:

- Age and pregnancy
- Race and ethnicity
- Height, weight, and BMI
- Present medical conditions
- Past medical conditions
- Willingness to change medications
- Willingness to take experimental drugs
- Metal implants
- Smoking status
- Parent or guardian status
- Fluency in English
- Other free text

## Legacy medication and treatment criteria

The current UI does not support selecting actual medications or treatments as matching criteria.

The current UI supports only:

- Willingness to change medications
- Willingness to take experimental drugs

Historical data may contain actual medication or treatment criteria produced by a legacy interface.

Those historical combinations must not be treated as current authoring behavior.

## Numeric criteria

The current UI supports:

```text
AGE
HEIGHT
WEIGHT
BMI
```

The study team may enter:

- Minimum only
- Maximum only
- Both bounds

| Variable | Unit     | Input                    |
| -------- | -------- | ------------------------ |
| `AGE`    | Years    | Nonnegative whole number |
| `HEIGHT` | Inches   | Nonnegative whole number |
| `WEIGHT` | Pounds   | Nonnegative whole number |
| `BMI`    | Unitless | Nonnegative decimal      |

See [Criterion Operator and Value Reference](../07-data-model/criterion-operator-reference.md).

## Medical conditions

Present and past medical conditions use typeahead multi-select controls.

The study team chooses:

```text
ANY
ALL
```

The current values come from the visible `MEDICAL_CONDITION` lookup vocabulary.

## OTHER free text

OTHER allows participant-facing criteria that cannot be evaluated by structured matching.

OTHER text:

- Is displayed in the posting
- Is not evaluated by the matching engine
- May represent inclusion or exclusion content

## Current UI constraints

The current eligibility UI creates a simplified structure:

```text
One criterion root per eligibility group
One clause per group
Expression connector = AND
Clause connector = TERMINAL
```

The current UI does not allow study teams to author arbitrary clause trees or choose general-purpose
clause connectors.

## Data-model capability

The underlying criteria model supports:

- Multiple clauses under one criterion root
- Expression-level connectors
- Clause-level connectors
- More general AND/OR structures

A multi-clause example describes the capability of the data model or historical data. It does not
describe what the current eligibility-authoring UI creates.

Documentation must not infer current UI functionality solely from the more flexible database model.

## Matching results

Three-valued matching may produce:

```text
TRUE
MAYBE
FALSE
```

See [Matching and Visibility](matching-and-visibility.md).

## Analytics

Historical and current criteria data may differ because:

- Legacy interfaces exposed different combinations
- The data model supports structures not exposed by the current UI
- Current UI data normally contains one clause per group

See
[Eligibility-Criteria Authoring Complexity](../08-operations/eligibility-criteria-authoring-complexity.md).

## Related pages

- [Criterion Operator and Value Reference](../07-data-model/criterion-operator-reference.md)
- [Criterion Variable Reference](../07-data-model/criterion-variable-reference.md)
- [Criteria Data Model](../07-data-model/criteria-data-model.md)
- [Matching and Visibility](matching-and-visibility.md)
- [Study Information Authoring](../05-study-management/study-information-authoring.md)
