---
title: Matching and Visibility
summary: Interest matching, eligibility matching, in-memory calculation, Redis recommendations, visibility, dismissal, and recomputation.
status: authoritative
canonical_for:
  - interest_matching
  - eligibility_matching
  - three_valued_logic
  - participant_visibility
  - match_recalculation
  - matching_memory
---

# Matching and Visibility

Matching has two independent dimensions:

1. Study-interest matching
2. Eligibility matching

## Matching runtime

To reduce calculation latency, the application maintains active studies and
active participants in memory.

When a match is triggered, the matching program evaluates the relevant
in-memory entities instead of repeatedly loading all candidate entities from
the database.

The relational database remains the authoritative persistent source.

When participant or study data changes:

1. The database record is updated.
2. The in-memory representation is updated.
3. Applicable matching is triggered.
4. Redis recommendation data is updated asynchronously.

Temporal participant-profile changes must update the in-memory participant
representation as well as the database record.

Inactive studies and deactivated participants are removed from active in-memory
matching collections.

Scheduled synchronization jobs reconcile time-based and other state changes.

## Interest matching

Interest matching compares participant study interests with study properties.

It determines whether an exact-matching study is recommended through My Studies.

Examples include:

- Topics and conditions
- Locations
- Compensation
- Healthy-participant preference

## Eligibility matching

Eligibility matching compares participant profile properties with study
eligibility criteria.

Results are:

```text
TRUE
MAYBE
FALSE
```

| Result | Meaning |
|---|---|
| `TRUE` | Exact match |
| `MAYBE` | Partial match |
| `FALSE` | Not a match |

## Three-valued logic

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

| Input | Result |
|---|---|
| `TRUE` | `FALSE` |
| `FALSE` | `TRUE` |
| `MAYBE` | `MAYBE` |

## Participant-facing recommendations

Ordinary system recommendations require:

- Active participant
- Active study
- Exact eligibility match
- Study-interest match
- No participant-side exclusion

Partial matches are not shown in participant-facing matched-study lists.

## Study-facing recommendations

Study-facing matching may contain:

- Exact matches
- Partial matches

Participant visibility is applied separately from underlying recommendation
storage.

## Visibility selection

Visibility is selected during participant or loved-one signup and may later be
changed.

### All study teams

The participant permits all study teams using the branded instance to view the
profile when the participant appears to be a suitable match.

This allows pre-interest study-team visibility.

### Only study teams whose studies receive interest

The participant is hidden from study teams until successfully expressing
interest in the applicable study.

Visibility does not change the underlying match result.

## Minimal owning accounts

An owning account created through signup for a loved one has an incomplete self
profile and defaults to hidden from study teams.

The loved-one account has its own profile and its own visibility selection.

## Reaching a study

A participant may reach a posting through:

- Public search
- My Studies
- Study-team promotion
- Direct or bookmarked URL
- Participant history

A participant may initiate interest from an accessible posting even when a
partial match was not displayed in My Studies.

Eligibility is reevaluated using the updated show-interest form values.

## Ask if interested

Ask if interested moves or emphasizes an existing participant-study match in the
study-team-promoted participant-facing bucket.

It:

- Updates the promotion timestamp
- Creates the applicable study-side exclusion
- Removes the participant from the ordinary study-side match presentation
- Does not create interest
- Does not create direct messaging

A scheduled job may email participants whose promoted matches are newer than
their last login.

## Not Interested

A participant may dismiss a study from My Studies.

This creates:

```text
NOT_INTERESTED
```

in the participant-side Redis exclusion structure.

Dismissed studies may appear in participant history.

## Recalculation triggers

### Participant profile change

If a changed profile property is referenced by eligibility criteria:

- Update the database profile
- Update the in-memory participant representation
- Recompute the participant against active studies
- Update applicable participant-facing and study-facing match results

### Temporal profile change during show interest

- Update the database profile in the transaction
- Update or prepare the corresponding in-memory participant representation
- Reevaluate eligibility before interest is finalized
- Commit the synchronized state only when the transaction succeeds

### Participant study-interest change

- Recompute that participant's matched-study recommendations
- Do not recompute study-side eligibility matches solely because interests
  changed

### Study-property change

If a property is referenced by participant study interests:

- Update the in-memory study representation
- Recompute affected participant-facing recommendations

### Study eligibility change

- Update the in-memory study representation
- Recompute the study's participant matches
- Recompute participant-facing results for that study

### Participant or study deactivation

- Remove the entity from active in-memory matching data
- Remove or suppress active recommendations
- Prevent new matching actions

## Redis storage

Recommendations, promotions, and exclusions are stored in Redis.

Redis contains derived matching state. It does not replace the authoritative
database or the active in-memory entity representations used for calculation.

See [Redis Match and Exclusion Model](../07-data-model/redis-match-model.md).

## After interest

Successful interest creates exclusions that remove the participant-study pair
from ordinary recommendation flows.

Later eligibility changes do not remove the historical interest relationship.

## Related pages

- [Participants](../04-users-and-access/participants.md)
- [Public Study Discovery](public-study-discovery.md)
- [Eligibility-Criteria Authoring](eligibility-criteria-authoring.md)
- [Ask If Interested](ask-if-interested.md)
- [Expressions of Interest](expressions-of-interest.md)
- [Redis Match and Exclusion Model](../07-data-model/redis-match-model.md)
