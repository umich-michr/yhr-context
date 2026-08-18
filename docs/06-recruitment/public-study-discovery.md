---
title: Public Study Discovery
summary: Public search, study summaries, study details, contact information, counts, and direct URLs.
status: authoritative
canonical_for:
  - public_study_search
  - public_study_details
  - study_interest_count_display
relevant_when:
  - searching_for_studies
  - explaining_public_postings
  - troubleshooting_public_visibility
---

# Public Study Discovery

Public users may browse and search active studies without creating an account.

An account is required to express interest.

## Public eligibility

A study is publicly discoverable only when:

- It has an operational posting
- It is active
- It is not archived

## Search

Public search may include:

- Topics and conditions
- Locations
- Compensation
- Participant type
- Other supported study properties
- Highlighted or configured search categories

Searchable study fields are represented through the generic study-property and criteria model.

## Search results

A search-result study summary may display:

- Participant-facing study title
- Purpose
- Eligibility summary
- Locations
- Age range
- Healthy-versus-condition participant type

Selecting Learn More opens the detailed public posting.

## Study details

The detailed posting may include:

- Title
- Locations
- Purpose
- Inclusion and exclusion criteria
- What is involved
- Compensation
- Additional information
- PI
- Study identifier
- Posting dates
- Study contact information

Study contact email and other entered contact information are publicly displayed.

Optional sections are omitted when no value exists.

## Interested-participant count

The participant-facing count uses an application-configured threshold.

Conceptually:

```text
if interested_participant_count < configured_threshold:
    display volunteers-needed message
else:
    display numeric interested-participant count
```

Deactivated participants do not contribute to the displayed count.

## Direct URLs

Participant-facing postings support copied and bookmarked URLs.

A valid URL for an inactive study displays a not-currently-recruiting message.

Archived studies are not publicly accessible.

## Search-engine indexing

Public study pages may be indexed by external search engines.

Search-engine discovery, ranking, timing, and completeness are outside application control.

## Related pages

- [Study Information Authoring](../05-study-management/study-information-authoring.md)
- [Study Lifecycle](../05-study-management/study-lifecycle.md)
- [Study Archiving](../05-study-management/study-archiving.md)
- [Expressions of Interest](expressions-of-interest.md)
