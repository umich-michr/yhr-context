---
title: Eligibility-Criteria Authoring
summary: Authoritative current UI behavior for authoring criteria groups, inclusion criteria, exclusion criteria, and structured expressions.
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
  - planning_ai_assisted_criteria_authoring
---

# Eligibility-Criteria Authoring

Study eligibility criteria determine whether a participant is an exact match, a partial match, or not a match for a study.

Study team members author eligibility criteria during the final stage of study-posting creation.

The current AI-assisted posting feature does not author eligibility criteria.

## Authoring goals

The eligibility UI allows study teams to describe:

- Who may be eligible
- Who must be excluded
- Whether the study recruits healthy participants
- Whether the study recruits participants with specific conditions
- Alternative participant groups or study arms
- Participant-facing criteria that cannot be evaluated by the matching engine

## Current UI screenshots

### Inclusion criteria

![Current inclusion-criteria authoring form](../assets/images/eligibility/current-inclusion-form.png)

### Exclusion criteria

![Current exclusion-criteria authoring form](../assets/images/eligibility/current-exclusion-form.png)

### Groups and arms summary

![Current criteria groups and arms summary](../assets/images/eligibility/current-groups-summary.png)

## Participant types

The study team identifies whether the study is recruiting:

- Healthy participants
- Participants with specific conditions
- Both participant types, when supported by the posting

Participant type affects how criteria groups are presented and described.

## Criteria groups or arms

A study may define multiple criteria groups or arms.

Examples include:

- Participants with specific medical conditions
- Healthy participants
- Participants aged 24–36
- Participants aged 48–60

Each group has:

- A name
- Display order
- Inclusion criteria
- Exclusion criteria

Groups are alternatives.

Conceptually:

```text
Participant is eligible for the study
if the participant qualifies for Group 1
OR Group 2
OR Group 3
```

A participant does not need to satisfy every group.

The participant must qualify for at least one group.

## Inclusion criteria

The inclusion section describes conditions the participant must satisfy.

The current UI presents inclusion logic as:

> Participants may be eligible if they meet all of the following criteria.

Conceptually:

```text
Inclusion result for one group =
    Inclusion Expression 1
    AND Inclusion Expression 2
    AND ...
```

The author does not choose the expression connector.

The current UI uses:

```text
AND
```

for expressions within a group.

## Exclusion criteria

The exclusion section describes conditions that disqualify a participant.

The current UI presents exclusion logic as:

> Participants are not eligible if they meet any of the following criteria.

Conceptually:

```text
Excluded from one group =
    Exclusion Condition 1
    OR Exclusion Condition 2
    OR ...
```

In persisted normalized expressions, structured exclusions are represented using negated operators.

Examples include:

```text
NOT_EQUAL
NOT_ANY_OF
NOT_ALL_OF
NOT_GREATER_THAN_OR_EQUAL
NOT_LESS_THAN_OR_EQUAL
NOT_BETWEEN
```

This allows group qualification to be evaluated as conditions that must remain true.

Example:

```text
Eligible for group =
    Age is at least 18
    AND does not have a metal implant
    AND is not currently pregnant
```

## Group-level logic

The conceptual group logic is:

```text
Group qualifies =
    all inclusion requirements are satisfied
    AND no exclusion condition applies
```

Study-level eligibility is:

```text
Study eligibility =
    Group 1 qualifies
    OR Group 2 qualifies
    OR ...
```

Three-valued matching may produce `MAYBE` when a structured criterion references an optional participant profile property that has no value.

See [Matching and Visibility](matching-and-visibility.md).

## Current UI sections

The eligibility form organizes controls into sections including:

- Age and pregnancy
- Race and ethnicity
- Height, weight, and BMI
- Medical conditions
- Medications, treatments, and experimental drugs
- Metal implants
- Smoking status
- Parent or guardian status
- Fluency in English
- Other

The controls displayed differ between inclusion and exclusion modes.

## Numeric criteria

The current UI provides one or two numeric inputs for:

```text
AGE
HEIGHT
WEIGHT
BMI
```

The user may provide:

- A minimum value
- A maximum value
- Both a minimum and maximum value

Units are:

| Variable | UI and storage unit |
|---|---|
| `AGE` | Years |
| `HEIGHT` | Inches |
| `WEIGHT` | Pounds |
| `BMI` | Unitless BMI value |

Validation rules include:

- `AGE`, `HEIGHT`, and `WEIGHT` accept nonnegative whole numbers.
- `BMI` accepts a nonnegative decimal value.
- Negative values are not permitted.

The exact persisted operators and scalar/range encoding are documented in [Criterion Operator and Value Reference](../07-data-model/criterion-operator-reference.md).

## Gender and race

The inclusion UI presents checkbox selections for:

- Biological sex at birth
- Race

Selected values are stored as lookup-backed criterion expressions.

The current UI combines selected values according to the operator mappings documented in [Criterion Operator and Value Reference](../07-data-model/criterion-operator-reference.md).

## Medical conditions

Present and past medical conditions use typeahead multi-select controls.

The study team may specify whether the participant must have:

```text
ANY
```

or:

```text
ALL
```

of the selected conditions.

The current lookup values come from the visible `MEDICAL_CONDITION` vocabulary.

The vocabulary may change as reference data is maintained.

The current UI supports:

- Present medical conditions
- Past medical conditions
- Inclusion conditions
- Exclusion conditions

The current operator mappings are documented in [Criterion Operator and Value Reference](../07-data-model/criterion-operator-reference.md).

## Boolean criteria

The current UI uses checkbox or Boolean-style controls for criteria such as:

- Pregnancy at the time of enrollment
- Willingness to change medications or treatments
- Willingness to take experimental drugs
- Metal implants
- Parent or guardian of a child under 18
- Fluency in English

Not every Boolean criterion is displayed in both inclusion and exclusion modes.

Boolean selections are stored using lookup-backed expression values.

## Smoking status

Smoking status is presented as a set of selectable values.

The current inclusion UI can require one of the selected smoking-status values.

The current exclusion UI can exclude participants matching selected smoking-status values.

Smoking-status selections are stored as lookup-backed expressions.

## OTHER free text

`OTHER` allows study teams to enter participant-facing criteria that cannot be represented using the structured matching controls.

Examples include:

- A specialized occupational requirement
- A protocol-specific condition not represented in the controlled vocabulary
- A participant-facing exclusion that the matching engine cannot evaluate

OTHER criteria are displayed to participants.

The matching engine does not directly evaluate OTHER free text.

This distinction is important:

```text
Displayed criterion
does not necessarily mean
machine-evaluated criterion
```

The persisted inclusion/exclusion encoding for OTHER is documented in [Criterion Operator and Value Reference](../07-data-model/criterion-operator-reference.md).

## Current UI constraints

The current UI simplifies the more flexible underlying criteria model.

Current behavior includes:

- Each criteria group is persisted with one clause.
- Expressions within the clause use `AND`.
- The author does not select the expression connector.
- The clause is terminal.
- Criteria groups are alternatives.
- Operators are selected or inferred from the UI control.
- The current UI does not expose arbitrary clause construction.

The underlying relational model supports:

- Multiple clauses
- Expression connectors
- Clause connectors
- Ordered expressions

See [Criteria Data Model](../07-data-model/criteria-data-model.md).

## Current UI and legacy data

The database contains criteria authored through both legacy and current interfaces.

An operator-variable combination found in historical data does not necessarily mean that the current UI still exposes that combination.

The authoritative current-UI mappings are documented in [Criterion Operator and Value Reference](../07-data-model/criterion-operator-reference.md).

Historical-data analysis should account for the authoring era when possible.

## Form completion

Submitting the eligibility form finalizes the study-posting creation workflow.

The posting may then become active when its lifecycle conditions are satisfied.

Final submission does not override:

- Institutional publishability
- Study activation date
- Study deactivation date
- Other activation requirements

See [Study Lifecycle](../05-study-management/study-lifecycle.md).

## Analytics implications

The authored criteria structure can be used to derive study-level complexity features.

Complexity dimensions, candidate measures, weighting, timing analysis, and proposed composite scores are documented in [Eligibility-Criteria Authoring Complexity](../08-operations/ai-assisted-study-posting-authoring-effectiveness.md).

These proposed analytical measures are not application eligibility rules.

## Related pages

- [Criterion Operator and Value Reference](../07-data-model/criterion-operator-reference.md)
- [Criterion Variable Reference](../07-data-model/criterion-variable-reference.md)
- [Criteria Data Model](../07-data-model/criteria-data-model.md)
- [Matching and Visibility](matching-and-visibility.md)
- [Expressions of Interest](expressions-of-interest.md)
- [Study Lifecycle](../05-study-management/study-lifecycle.md)
- [AI-Assisted Study Posting Authoring](../05-study-management/ai-assisted-posting-authoring.md)
- [Eligibility-Criteria Authoring Complexity](../08-operations/ai-assisted-study-posting-authoring-effectiveness.md)
