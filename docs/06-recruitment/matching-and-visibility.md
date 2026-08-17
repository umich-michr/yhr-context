---
title: Matching and Visibility
summary: Interest matching, three-valued eligibility, partial matches, and participant visibility.
status: authoritative
relevant_when:
  - explaining_study_matches
  - explaining_participant_matches
  - explaining_partial_matches
  - troubleshooting_participant_visibility
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

### Boolean truth tables

| `AND` | `TRUE` | `FALSE` | `MAYBE` |
|---|---:|---:|---:|
| `TRUE` | `TRUE` | `FALSE` | `MAYBE` |
| `FALSE` | `FALSE` | `FALSE` | `FALSE` |
| `MAYBE` | `MAYBE` | `FALSE` | `MAYBE` |

| `OR` | `TRUE` | `FALSE` | `MAYBE` |
|---|---:|---:|---:|
| `TRUE` | `TRUE` | `TRUE` | `TRUE` |
| `FALSE` | `TRUE` | `FALSE` | `MAYBE` |
| `MAYBE` | `TRUE` | `MAYBE` | `MAYBE` |

| Input | `NOT` result |
|---|---|
| `TRUE` | `FALSE` |
| `FALSE` | `TRUE` |
| `MAYBE` | `MAYBE` |

## Match categories

| Eligibility result | Display category |
|---|---|
| `TRUE` | Exact match |
| `MAYBE` | Partial match |
| `FALSE` | Not matched |

Exact and partial matches are displayed separately in the applicable matched-participant and matched-study interfaces.

## Restricted visibility

A restricted participant has chosen not to be visible to study teams unless the participant expresses interest.

For a restricted participant:

- The application evaluates study interests.
- The application evaluates eligibility.
- Exact matching studies may be shown to the participant.
- Partial (`MAYBE`) matches are not shown to participants.
- A system match does not make the participant visible to the study team.
- The participant becomes visible to the study after successfully expressing interest.

## Discoverable visibility

A discoverable participant permits eligible studies to see them as a match before an expression of interest.

For a discoverable participant:

- Eligibility can make the participant visible to the study team.
- The study does not need to match the participant's interests.
- The participant does not need to express interest first.
- Exact and partial matches appear in their corresponding categories.

## Matching matrix

| Visibility | Eligibility | Interest match | Expressed interest | Study-team visibility | Participant-facing result |
|---|---|---:|---:|---|---|
| Restricted | `TRUE` | Yes | No | Hidden | Exact matched study |
| Restricted | `MAYBE` | Yes | No | Hidden | Partial matched study |
| Restricted | `TRUE` | Any | Yes | Visible as interested | Interested study |
| Restricted | `MAYBE` | Any | Successful interest depends on recheck | Hidden until completed | Partial candidate |
| Discoverable | `TRUE` | Any | No | Exact-match category | Recommended when interests match |
| Discoverable | `MAYBE` | Any | No | Partial-match category | Partial recommendation when applicable |
| Any | `FALSE` | Any | No | Not visible as a match | Not recommended |

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
3. `TRUE` or `MAYBE` eligibility can proceed through the interest workflow.
4. `FALSE` eligibility prevents interest from being completed.
5. If eligible, the participant completes the screening workflow.

After an expression of interest is finalized, later eligibility changes do not remove or alter the interest relationship.

## Historical interest versus current matching

A participant may:

- Have a historical expression of interest
- No longer satisfy current eligibility
- Still remain in the interested-participant history

Historical interest is not recalculated away.

## Stored-match processing

Match results are stored in Redis rather than dynamically calculated on every
view. Match recalculation runs asynchronously after a trigger, including a
change to:

- A participant profile property used by study interests or eligibility
  criteria
- A participant's study interests
- A study property used by participant interests
- Study eligibility criteria

Failed recalculations are not automatically retried. Operators can manually
trigger jobs to recompute all matches for all studies, all matches for all
participants, or both.

## Related pages

- [Participants](../04-users-and-access/participants.md)
- [Ask if interested](ask-if-interested.md)
- [Expressions of interest](expressions-of-interest.md)
- [Questionnaires and exports](questionnaires-and-exports.md)