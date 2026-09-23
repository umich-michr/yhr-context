---
title: Study Property Query Cookbook
summary: Tested Oracle SQL patterns for retrieving and validating flexible study-property values.
status: authoritative
canonical_for:
  - study_property_queries
  - study_information_extraction
  - property_value_aggregation
relevant_when:
  - querying_study_information
  - flattening_study_properties
  - comparing_ai_suggestions_to_final_values
  - validating_property_storage
---

# Study Property Query Cookbook

Study Information form values are stored using a flexible property-value model.

One logical property may be represented as:

- A scalar value in `STUDY_PROPERTY_VALUE.SAVED_VALUE`, or
- One or more lookup selections connected through `STUDY_PROP_VAL_LOOKUP_VAL`

A direct relational join can therefore produce multiple rows for one logical property value.

Queries used for analysis should aggregate at the `STUDY_PROPERTY_VALUE` level before counting
studies or properties.

See [Study Property Model](study-property-model.md) for the canonical model description.

## Flattened study-property query

The following query returns one row per `STUDY_PROPERTY_VALUE`.

Lookup values are aggregated into semicolon-separated lists.

```sql
WITH property_base AS (
    SELECT
        s.id AS study_id,
        s.study_num,
        s.created_by_id,
        s.created_date,
        s.publishable,
        s.posting_activation_date,
        s.posting_deactivation_date,

        spv.id AS property_value_id,
        spv.saved_value,

        ep.id AS property_id,
        ep.name AS property_name,
        ep.property_value_type,

        lv.id AS lookup_value_id,
        lv.display_text AS lookup_display_text,
        lv.name AS lookup_name,
        lv.type AS lookup_type,
        lv.visible AS lookup_visible

    FROM study s
    JOIN study_property_value spv
        ON spv.study_id = s.id
    JOIN entity_property ep
        ON ep.id = spv.entity_property_id
    LEFT JOIN study_prop_val_lookup_val spvlv
        ON spvlv.property_value_id = spv.id
    LEFT JOIN lookup_value lv
        ON lv.id = spvlv.lookup_value_id

    WHERE (:study_num IS NULL OR s.study_num = :study_num)
)
SELECT
    study_id,
    study_num,
    created_by_id,
    created_date,
    publishable,
    posting_activation_date,
    posting_deactivation_date,

    property_value_id,
    property_id,
    property_name,
    property_value_type,
    saved_value,

    COUNT(DISTINCT lookup_value_id) AS lookup_value_count,

    LISTAGG(lookup_display_text, '; ')
        WITHIN GROUP (ORDER BY lookup_value_id)
        AS lookup_display_values,

    LISTAGG(lookup_name, '; ')
        WITHIN GROUP (ORDER BY lookup_value_id)
        AS lookup_names,

    LISTAGG(lookup_type, '; ')
        WITHIN GROUP (ORDER BY lookup_value_id)
        AS lookup_types,

    LISTAGG(TO_CHAR(lookup_value_id), '; ')
        WITHIN GROUP (ORDER BY lookup_value_id)
        AS lookup_value_ids,

    LISTAGG(TO_CHAR(lookup_visible), '; ')
        WITHIN GROUP (ORDER BY lookup_value_id)
        AS lookup_visibility_values,

    CASE
        WHEN saved_value IS NOT NULL
             AND COUNT(DISTINCT lookup_value_id) > 0
            THEN 'INVALID_SCALAR_AND_LOOKUP'

        WHEN saved_value IS NOT NULL
            THEN 'SCALAR'

        WHEN COUNT(DISTINCT lookup_value_id) > 0
            THEN 'LOOKUP'

        ELSE 'EMPTY'
    END AS storage_shape

FROM property_base
GROUP BY
    study_id,
    study_num,
    created_by_id,
    created_date,
    publishable,
    posting_activation_date,
    posting_deactivation_date,

    property_value_id,
    property_id,
    property_name,
    property_value_type,
    saved_value

ORDER BY
    study_num,
    property_name,
    property_value_id;
```

## Why lookup values are aggregated

A study property such as locations may have several selected lookup values.

Without aggregation:

```text
One logical locations property
with three selected locations
=
three joined SQL rows
```

After aggregation:

```text
One logical locations property
=
one analytical row
with lookup_value_count = 3
```

This prevents:

- Overcounting properties
- Overcounting studies
- Incorrect AI-suggestion comparisons
- Incorrect study-complexity measures

## Ordering of aggregated lookup attributes

The lookup display text, name, type, identifier, and visibility lists are all ordered by:

```text
LOOKUP_VALUE.ID
```

Using the same order preserves positional alignment across the generated lists.

For example, the first value in:

```text
lookup_display_values
```

corresponds to the first value in:

```text
lookup_value_ids
```

## Storage-shape classification

The query derives:

| Value                       | Meaning                                                   |
| --------------------------- | --------------------------------------------------------- |
| `SCALAR`                    | `SAVED_VALUE` is populated and no lookup values exist     |
| `LOOKUP`                    | One or more lookup values exist and `SAVED_VALUE` is null |
| `EMPTY`                     | Neither scalar nor lookup storage is populated            |
| `INVALID_SCALAR_AND_LOOKUP` | Both scalar and lookup storage are populated              |

The property model expects scalar and lookup storage to be mutually exclusive for one property-value
record.

## Data-quality query

The following query identifies property-value rows that violate the scalar-versus-lookup invariant.

```sql
SELECT
    s.study_num,
    spv.id AS property_value_id,
    ep.id AS property_id,
    ep.name AS property_name,
    ep.property_value_type,
    spv.saved_value,
    COUNT(DISTINCT spvlv.lookup_value_id) AS lookup_value_count
FROM study s
JOIN study_property_value spv
    ON spv.study_id = s.id
JOIN entity_property ep
    ON ep.id = spv.entity_property_id
LEFT JOIN study_prop_val_lookup_val spvlv
    ON spvlv.property_value_id = spv.id
GROUP BY
    s.study_num,
    spv.id,
    ep.id,
    ep.name,
    ep.property_value_type,
    spv.saved_value
HAVING
    spv.saved_value IS NOT NULL
    AND COUNT(DISTINCT spvlv.lookup_value_id) > 0
ORDER BY
    s.study_num,
    ep.name,
    spv.id;
```

A returned row represents invalid mixed storage under the current property-value invariant.

## Querying one property

To retrieve one property across studies, filter by the semantic property name:

```sql
SELECT
    s.study_num,
    spv.id AS property_value_id,
    ep.name AS property_name,
    ep.property_value_type,
    spv.saved_value,
    lv.id AS lookup_value_id,
    lv.name AS lookup_name,
    lv.display_text AS lookup_display_text
FROM study s
JOIN study_property_value spv
    ON spv.study_id = s.id
JOIN entity_property ep
    ON ep.id = spv.entity_property_id
LEFT JOIN study_prop_val_lookup_val spvlv
    ON spvlv.property_value_id = spv.id
LEFT JOIN lookup_value lv
    ON lv.id = spvlv.lookup_value_id
WHERE ep.name = :property_name
ORDER BY
    s.study_num,
    spv.id,
    lv.id;
```

Examples of `:property_name` may include:

```text
title
studyDescription
purpose
locations
conditions
offersCompensation
participantType
department
```

The actual property names should be read from `ENTITY_PROPERTY`.

## Listing entity properties

```sql
SELECT
    id,
    name,
    property_value_type
FROM entity_property
ORDER BY name;
```

This query provides the authoritative property vocabulary for the Study Information property-value
model.

## AI-suggestion analysis

For comparison with AI-generated study-information suggestions:

1. Retrieve one logical property row per `STUDY_PROPERTY_VALUE`.
1. Preserve scalar values separately from lookup values.
1. Compare lookup values using stable lookup IDs where possible.
1. Compare scalar values only after applying the chosen normalization rules.
1. Retain the original final value for auditability.

Do not compare lookup-backed values solely by concatenated display text when stable lookup
identifiers are available.

## Oracle compatibility notes

The queries use:

```text
LISTAGG
```

The maximum returned string size and supported overflow behavior depend on the Oracle version and
database configuration.

For properties with very large lookup sets, the analysis may need:

- `LISTAGG ... ON OVERFLOW TRUNCATE`, when supported
- JSON aggregation
- Row-level output instead of concatenated output

Any modified query should preserve one-property-level counting semantics.

## Related pages

- [Study Property Model](study-property-model.md)
- [AI-Assisted Study Posting Authoring](../05-study-management/ai-assisted-posting-authoring.md)
- [AI-Assisted Study Posting Authoring Effectiveness](../08-operations/ai-assisted-study-posting-authoring-effectiveness.md)
- [Operational Schema](operational-schema.md)
