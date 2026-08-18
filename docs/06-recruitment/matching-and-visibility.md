---
title: Matching and Visibility
summary: Interest matching, three-valued eligibility, partial matches, and participant visibility.
status: authoritative
relevant_when:
  - explaining_study_matches
  - explaining_participant_matches
  - explaining_partial_matches
  - troubleshooting_participant_visibility
canonical_for:
  - interest_matching
  - eligibility_matching
  - three_valued_logic
  - participant_visibility
  - match_recalculation
---

# Matching and Visibility

Participant-study matching has two independent dimensions:

1. Interest matching
2. Eligibility matching

These dimensions answer different questions and should not be combined into one undifferentiated match value.

## Interest matching

Interest matching compares:

- Participant study interests
- Study posting properties

It answers:

> Is this the type of study the participant wants to see?

Examples of participant interests include:

- Research topics or conditions
- Locations
- Compensation
- Other study characteristics

## Eligibility matching

Eligibility matching compares:

- Participant profile properties
- Study inclusion criteria
- Study exclusion criteria

It answers:

> Does the participant appear eligible, ineligible, or only partially evaluable?

## Three-valued eligibility logic

Eligibility expressions use three values:

```text
TRUE
MAYBE
FALSE
```

### `TRUE`

The participant has sufficient profile data and satisfies the criterion.

### `FALSE`

The participant has sufficient profile data and does not satisfy the criterion.

### `MAYBE`

The criterion references an optional participant profile property for which the participant has no value.

Example:

```text
Criterion A = TRUE
Criterion B = MAYBE
```

When joined by `AND`:

```text
TRUE AND MAYBE = MAYBE
```

## Boolean truth tables

### `AND`

| `AND` | `TRUE` | `FALSE` | `MAYBE` |
|---|---:|---:|---:|
| `TRUE` | `TRUE` | `FALSE` | `MAYBE` |
| `FALSE` | `FALSE` | `FALSE` | `FALSE` |
| `MAYBE` | `MAYBE` | `FALSE` | `MAYBE` |

### `OR`

| `OR` | `TRUE` | `FALSE` | `MAYBE` |
|---|---:|---:|---:|
| `TRUE` | `TRUE` | `TRUE` | `TRUE` |
| `FALSE` | `TRUE` | `FALSE` | `MAYBE` |
| `MAYBE` | `TRUE` | `MAYBE` | `MAYBE` |

### `NOT`

| Input | `NOT` result |
|---|---|
| `TRUE` | `FALSE` |
| `FALSE` | `TRUE` |
| `MAYBE` | `MAYBE` |

## Match categories

| Eligibility result | Study-team category |
|---|---|
| `TRUE` | Exact match |
| `MAYBE` | Partial match |
| `FALSE` | Not matched |

Exact and partial categories apply to study-team matched-participant displays.

Participants are not shown partial matched studies.

## Restricted visibility

A restricted participant has chosen not to be visible to study teams unless the participant expresses interest.

For a restricted participant:

- The application evaluates study interests.
- The application evaluates eligibility.
- Exact matching studies may be shown to the participant.
- Partial matches are not shown to the participant.
- A system match does not make the participant visible to the study team.
- The participant becomes visible to the study after successfully expressing interest.

## Discoverable visibility

A discoverable participant permits studies to see them as an exact or partial match before an expression of interest.

For a discoverable participant:

- Eligibility can make the participant visible to the study team.
- The study does not need to match the participant's interests.
- The participant does not need to express interest first.
- `TRUE` results appear in the study team's exact-match category.
- `MAYBE` results appear in the study team's partial-match category.
- Partial matches are not presented to the participant as matched studies.

## Matching matrix

| Visibility | Eligibility | Interest match | Expressed interest | Study-team visibility | Participant-facing result |
|---|---|---:|---:|---|---|
| Restricted | `TRUE` | Yes | No | Hidden | Exact matched study |
| Restricted | `TRUE` | No | No | Hidden | Not recommended |
| Restricted | `MAYBE` | Any | No | Hidden | Not shown |
| Restricted | `TRUE` or `MAYBE` | Any | Successfully finalized | Visible as interested | Interested study after the participant reaches the posting and completes the interest workflow |
| Discoverable | `TRUE` | Yes | No | Exact-match category | Exact matched study |
| Discoverable | `TRUE` | No | No | Exact-match category | Usually not recommended |
| Discoverable | `MAYBE` | Any | No | Partial-match category | Not shown |
| Any | `FALSE` | Any | No | Not visible as a match | Not shown |

## Recalculation after participant-profile changes

When a participant profile property referenced by study eligibility criteria changes:

- Recalculate that participant's matches for all active studies.
- Update the participant's matched-study results.
- Update applicable study-side matched-participant results for that participant.

## Recalculation after participant-interest changes

When a participant changes study interests:

- Recalculate that participant's matched-study list.
- Do not recalculate study-side matched-participant lists.

Study-side matched participants are based on eligibility and visibility, not on whether the participant expressed a preference for the study.

## Recalculation after study-property changes

When a study property referenced by participant study interests changes:

- Recalculate affected participants' matched-study lists.

Example study properties may include:

- Topic
- Location
- Compensation
- Other participant-interest matching attributes

## Recalculation after eligibility-criteria changes

When a study changes its eligibility criteria:

- Recalculate the study's matched-participant list.
- Recalculate participant matched-study results for that study.

## Interest after matching

When a participant attempts to express interest:

1. The participant refreshes specified temporal profile data.
2. The application rechecks eligibility.
3. `TRUE` or `MAYBE` may proceed through the interest workflow.
4. `FALSE` prevents interest from being completed.
5. The participant completes the screening workflow when permitted.

Partial matches are not shown in the participant's matched-study list.

A participant may nevertheless reach a study through a direct or bookmarked study-posting URL. If the participant initiates interest from an accessible posting, the application performs the current eligibility recheck.

A `MAYBE` result may proceed through the interest workflow even though the underlying partial match was not displayed in the participant's matched-study list.

After an expression of interest is finalized, later eligibility changes do not remove or alter the interest relationship.

## Historical interest versus current matching

A participant may:

- Have a historical expression of interest
- No longer satisfy current eligibility
- Still remain in the interested-participant history

Historical interest is not recalculated away.

## Stored-match processing

Current recommendations and directional match exclusions are stored in Redis sorted sets.

Redis separately stores:

- Studies recommended to a participant
- Participants recommended to a study
- Participants excluded from study-side recommendation computation
- Studies excluded from participant-side recommendation computation

Participant visibility is applied separately from underlying recommendation storage.

Match recalculation runs asynchronously after relevant changes.

Failed recalculations are not automatically retried.

Operators can manually trigger jobs to recompute:

- All study matches
- All participant matches
- Both categories of matches

See [Redis Match and Exclusion Model](../07-data-model/redis-match-model.md) for the canonical key patterns, member values, timestamp scores, and exclusion reasons.

## Related pages

- [Participants](../04-users-and-access/participants.md)
- [Eligibility-criteria authoring](eligibility-criteria-authoring.md)
- [Criteria data model](../07-data-model/criteria-data-model.md)
- [Ask if interested](ask-if-interested.md)
- [Expressions of interest](expressions-of-interest.md)
- [Questionnaires and exports](questionnaires-and-exports.md)
