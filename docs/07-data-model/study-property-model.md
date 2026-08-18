---
title: Study Property Model
summary: Generic property-value storage used by the Study Information form.
status: mixed
relevant_when:
  - mapping_study_information_ui_to_database
  - comparing_ai_suggestions_to_saved_values
  - analyzing_study_property_changes
---

# Study Property Model

The Study Information form uses a generic property-value model.

This model provides the final saved values that can be compared with:

- LLM suggestions
- User-selected suggestions
- Audit records

## Core entities

| Entity | Purpose |
|---|---|
| `STUDY` | Root operational study posting |
| `ENTITY_PROPERTY` | Defines a supported study property |
| `STUDY_PROPERTY_VALUE` | Stores one study's value for one property |
| `STUDY_PROP_VAL_LOOKUP_VAL` | Connects a property value to selected lookup values |
| `LOOKUP_VALUE` | Defines selectable vocabulary values |

## UI-to-database mapping

```mermaid
flowchart TB
    subgraph UI["Study Information Form"]
        TITLE[Title]
        DESCRIPTION[Study Description]
        PURPOSE[Purpose]
        ABOUT[About Study]
        LOCATION[Locations]
        COMP[Compensation]
        OFFER[Offers Compensation]
        CONDITION[Conditions or Topics]
        TYPE[Participant Type]
        PI[PI User Reference]
        DEPT[Department]
        ARCHIVE[Archived Date]
        ENROLL[Enrollment Number]
    end

    subgraph API["API Representation"]
        PAYLOAD[propertyValues array]
        SCALAR[savedValue]
        LOOKUPS[lookupValues array]
    end

    subgraph DB["Relational Storage"]
        STUDY[STUDY]
        EP[ENTITY_PROPERTY]
        SPV[STUDY_PROPERTY_VALUE]
        JOIN[STUDY_PROP_VAL_LOOKUP_VAL]
        LV[LOOKUP_VALUE]
    end

    TITLE --> PAYLOAD
    DESCRIPTION --> PAYLOAD
    PURPOSE --> PAYLOAD
    ABOUT --> PAYLOAD
    LOCATION --> PAYLOAD
    COMP --> PAYLOAD
    OFFER --> PAYLOAD
    CONDITION --> PAYLOAD
    TYPE --> PAYLOAD
    PI --> PAYLOAD
    DEPT --> PAYLOAD
    ARCHIVE --> PAYLOAD
    ENROLL --> PAYLOAD

    PAYLOAD --> SCALAR
    PAYLOAD --> LOOKUPS

    SCALAR --> SPV
    LOOKUPS --> JOIN

    STUDY --> SPV
    EP --> SPV
    SPV --> JOIN
    LV --> JOIN
```

## `ENTITY_PROPERTY`

`ENTITY_PROPERTY` identifies a supported property.

Relevant fields include:

```text
ID
NAME
VALUE_TYPE
```

Possible value types include:

```text
STRING
DATE
LOOKUP
```

Examples of property names include:

```text
title
studyDescription
purpose
aboutStudy
locations
conditions
offersCompensation
participantType
department
```

The actual property names should be obtained from application reference data.

## Scalar property values

Scalar fields are stored in:

```text
STUDY_PROPERTY_VALUE.SAVED_VALUE
```

Examples include:

- Title
- Study description
- Purpose
- About the study
- Compensation text
- Enrollment number
- Dates
- PI user identifier, when represented as a scalar property

## Lookup property values

Lookup selections are stored through:

```text
STUDY_PROP_VAL_LOOKUP_VAL
```

This table associates a `STUDY_PROPERTY_VALUE` with one or more `LOOKUP_VALUE` rows.

Examples include:

- Locations
- Conditions or topics
- Participant type
- Offers compensation
- Department

## Scalar-versus-lookup invariant

For one logical study property value, the current model expects either:

- A scalar `saved_value`, or
- One or more associated lookup values

It is an application-data error for the same property-value record to contain both:

- A non-null `saved_value`
- Associated lookup selections

Analytics should validate this invariant before comparing final values with AI suggestions.

## Common storage patterns

| Property kind | Storage pattern |
|---|---|
| Text | `saved_value` |
| Long text | `saved_value` |
| Date | `saved_value` |
| Single lookup | One lookup join |
| Multiple lookup | Multiple lookup joins |
| Boolean | Lookup value such as `TRUE` or `FALSE` |

## Example lookup types

Possible lookup types include:

```text
STUDY_LOCATION
MEDICAL_CONDITION
BOOLEAN
STUDY_DEPARTMENT
PARTICIPANT_TYPE
```

The values should be verified against deployment reference data.

## Conceptual relationships

```mermaid
erDiagram
    STUDY {
        NUMBER ID PK
        VARCHAR2 STUDY_NUM
    }

    ENTITY_PROPERTY {
        NUMBER ID PK
        VARCHAR2 NAME
        VARCHAR2 VALUE_TYPE
    }

    STUDY_PROPERTY_VALUE {
        NUMBER ID PK
        NUMBER STUDY_ID FK
        NUMBER ENTITY_PROPERTY_ID FK
        VARCHAR2 LANGUAGE
        CLOB SAVED_VALUE
    }

    STUDY_PROP_VAL_LOOKUP_VAL {
        NUMBER PROPERTY_VALUE_ID FK
        NUMBER LOOKUP_VALUE_ID FK
    }

    LOOKUP_VALUE {
        NUMBER ID PK
        VARCHAR2 DISPLAY_TEXT
        VARCHAR2 NAME
        VARCHAR2 TYPE
        VARCHAR2 LANGUAGE
        NUMBER VISIBLE
    }

    STUDY ||--o{ STUDY_PROPERTY_VALUE : has
    ENTITY_PROPERTY ||--o{ STUDY_PROPERTY_VALUE : defines
    STUDY_PROPERTY_VALUE ||--o{ STUDY_PROP_VAL_LOOKUP_VAL : selects
    LOOKUP_VALUE ||--o{ STUDY_PROP_VAL_LOOKUP_VAL : referenced_by
```

## AI-assisted comparison

For AI-effectiveness analysis, compare values at the normalized property level.

### Scalar normalization

Possible normalization includes:

- Trimming whitespace
- Normalizing line endings
- Normalizing dates
- Preserving original text for audit
- Measuring exact and semantic similarity separately

### Lookup normalization

Lookup comparisons should use stable lookup identifiers instead of display text when possible.

Possible measures include:

- Exact set equality
- Suggestion-to-final overlap
- Added values
- Removed values
- Selected suggestion retained unchanged
- Selected suggestion edited before save

## Proposed comparison categories

The following are proposed analytical categories, not current database statuses:

```text
SUGGESTION_NOT_GENERATED
SUGGESTION_GENERATED_NOT_SELECTED
SUGGESTION_SELECTED_UNCHANGED
SUGGESTION_SELECTED_THEN_EDITED
FINAL_VALUE_MATCHES_UNSELECTED_SUGGESTION
FINAL_VALUE_DIFFERS_FROM_ALL_SUGGESTIONS
```

## Query examples

Tested Oracle SQL for reconstructing one logical row per study property is documented in [Study Property Query Cookbook](study-property-query-cookbook.md).

The cookbook includes:

- Scalar and lookup property extraction
- Lookup aggregation
- Storage-shape classification
- Scalar-versus-lookup validation
- Property-specific queries
- AI-suggestion comparison guidance

## Related pages

- [AI-Assisted Study Posting Authoring](../05-study-management/ai-assisted-posting-authoring.md)
- [Operational Schema](operational-schema.md)
- [AI-Assisted Study Posting Authoring Effectiveness](../08-operations/ai-assisted-study-posting-authoring-effectiveness.md)
- [Study Property Query Cookbook](study-property-query-cookbook.md)
- [Criterion Variable Reference](criterion-variable-reference.md)
