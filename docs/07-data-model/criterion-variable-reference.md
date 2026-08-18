---
title: Criterion Variable Reference
summary: Authoritative criterion-variable reference rows currently defined in the application database.
status: authoritative
canonical_for:
  - criterion_variable_vocabulary
  - criterion_variable_identifiers
relevant_when:
  - identifying_criterion_variables
  - interpreting_criterion_expressions
  - mapping_ui_fields_to_variables
  - calculating_criteria_complexity
---

# Criterion Variable Reference

`CRITERION_VARIABLE` defines the variables available to the application's generic criteria-expression model.

The table is not limited to study eligibility criteria.

Its vocabulary includes variables associated with:

- Study eligibility criteria
- Participant study-interest criteria
- Study-information properties
- Other criteria-based application functions

The presence of a variable in this table does not, by itself, establish that the variable is currently exposed by the eligibility-authoring UI.

UI availability and supported operators must be documented separately.

## Authoritative reference query

```sql
SELECT
    id,
    name
FROM criterion_variable
ORDER BY name;
```

## Current reference values

| ID | Name |
|---:|---|
| 435 | `ABOUT_STUDY` |
| 401 | `AGE` |
| 437 | `ARCHIVED_DATE` |
| 403 | `BMI` |
| 423 | `COMPENSATION` |
| 431 | `DATE_OF_BIRTH` |
| 436 | `DEPARTMENT` |
| 433 | `DUE_DATE` |
| 413 | `FLUENCY_IN_ENGLISH` |
| 400 | `GENDER` |
| 415 | `HAS_METAL_IMPLANTS` |
| 402 | `HEIGHT` |
| 426 | `LOCATIONS` |
| 424 | `OFFERS_COMPENSATION` |
| 410 | `OTHER` |
| 438 | `PARENT_OR_GUARDIAN_OF_A_CHILD` |
| 414 | `PAST_MEDICAL_CONDITION` |
| 405 | `PREGNANT_AT_THE_TIME_OF_ENROLLMENT` |
| 404 | `PRESENT_MEDICAL_CONDITION` |
| 428 | `PRINCIPAL_INVESTIGATOR` |
| 411 | `RACE` |
| 407 | `SMOKING_STATUS` |
| 421 | `STUDY_DESCRIPTION` |
| 422 | `STUDY_PURPOSE` |
| 420 | `STUDY_TITLE` |
| 425 | `TYPE_OF_RESEARCH_PATIENTS_THIS_STUDY_IS_SEEKING` |
| 412 | `WEIGHT` |
| 418 | `WILLING_TO_CHANGE_MEDICATIONS` |
| 417 | `WILLING_TO_TAKE_EXPERIMENTAL_DRUGS` |

## Eligibility-authoring variables

The current eligibility-authoring UI uses a subset of the complete vocabulary.

The documented eligibility-related subset includes:

```text
AGE
BMI
FLUENCY_IN_ENGLISH
GENDER
HAS_METAL_IMPLANTS
HEIGHT
OTHER
PARENT_OR_GUARDIAN_OF_A_CHILD
PAST_MEDICAL_CONDITION
PREGNANT_AT_THE_TIME_OF_ENROLLMENT
PRESENT_MEDICAL_CONDITION
RACE
SMOKING_STATUS
WEIGHT
WILLING_TO_CHANGE_MEDICATIONS
WILLING_TO_TAKE_EXPERIMENTAL_DRUGS
```

This subset should be kept synchronized with:

- The eligibility-authoring UI
- Application configuration
- Criterion-variable/operator mappings
- Automated tests

## Current UI exposure

The complete `CRITERION_VARIABLE` vocabulary is broader than the current eligibility-authoring UI.

Current eligibility-form exposure and operator mappings are documented in:

- [Eligibility-Criteria Authoring](../06-recruitment/eligibility-criteria-authoring.md)
- [Criterion Operator and Value Reference](criterion-operator-reference.md)

The operator reference, rather than historical operator combinations alone, is authoritative for the current UI.

## Study-information variables

The vocabulary also includes variables corresponding to study information:

```text
ABOUT_STUDY
ARCHIVED_DATE
COMPENSATION
DEPARTMENT
DUE_DATE
LOCATIONS
OFFERS_COMPENSATION
PRINCIPAL_INVESTIGATOR
STUDY_DESCRIPTION
STUDY_PURPOSE
STUDY_TITLE
TYPE_OF_RESEARCH_PATIENTS_THIS_STUDY_IS_SEEKING
```

Study Information form values are persisted through the generic study-property model documented in [Study Property Model](study-property-model.md).

A variable having a corresponding name in `CRITERION_VARIABLE` does not mean that the Study Information form stores its value directly in `CRITERION_VARIABLE`.

## Participant-profile variables

Some variables correspond to participant-profile properties used during matching:

```text
AGE
BMI
DATE_OF_BIRTH
FLUENCY_IN_ENGLISH
GENDER
HAS_METAL_IMPLANTS
HEIGHT
PARENT_OR_GUARDIAN_OF_A_CHILD
PAST_MEDICAL_CONDITION
PREGNANT_AT_THE_TIME_OF_ENROLLMENT
PRESENT_MEDICAL_CONDITION
RACE
SMOKING_STATUS
WEIGHT
WILLING_TO_CHANGE_MEDICATIONS
WILLING_TO_TAKE_EXPERIMENTAL_DRUGS
```

The matching engine uses a criterion variable to identify which participant or study property must be evaluated.

## IDs and names

Application logic should prefer stable semantic names where supported.

Database analyses should retain both:

- `CRITERION_VARIABLE.ID`
- `CRITERION_VARIABLE.NAME`

The numeric ID is required for database relationships, while the name makes analytical output interpretable.

Neither an analytical query nor an external integration should assume that the IDs are identical across unrelated institutional deployments unless that consistency is explicitly guaranteed.

## Related pages

- [Eligibility-Criteria Authoring](../06-recruitment/eligibility-criteria-authoring.md)
- [Criteria Data Model](criteria-data-model.md)
- [Study Property Model](study-property-model.md)
- [Eligibility-Criteria Authoring Complexity](../08-operations/eligibility-criteria-authoring-complexity.md)
- [Criterion Operator and Value Reference](criterion-operator-reference.md)
