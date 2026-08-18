---
title: Study Information Authoring
summary: Participant-facing Study Information fields, public display, search, matching use, and property storage.
status: authoritative
canonical_for:
  - study_information_authoring
  - study_posting_fields
  - study_contact_information
relevant_when:
  - creating_a_study_posting
  - editing_study_information
  - explaining_public_posting_fields
  - mapping_study_fields_to_public_display
---

# Study Information Authoring

The Study Information form defines the main participant-facing content of a study posting.

The Study Information form is followed by the eligibility-authoring step.

## Fields authored on Study Information

### Study title

The participant-facing title appears in:

- Public search results
- Detailed study postings
- Participant matched-study views
- Participant history
- Other study references

### Topics and conditions

One or more topics or conditions are required.

They support:

- Public search
- Advanced search
- Participant study-interest matching
- Participant-facing study summaries

### Study purpose

The purpose is a participant-facing summary written in accessible language.

### What is involved

This field describes participation, such as:

- Procedures
- Visits
- Time commitments
- Remote or in-person participation
- Other expectations

### Locations

One or more configured locations are required.

Locations support:

- Public search
- Study-interest matching
- Study summaries
- Detailed posting display

A configured location may represent remote participation.

### Compensation

The study team indicates whether compensation is offered.

When compensation is offered, participant-facing details may be entered.

Compensation availability may be used by participant study-interest matching.

### Principal investigator

The PI field is read-only to ordinary study team members.

PI data originates from the institutional source of truth.

### Department

The study team selects a department from institution-configured lookup values.

### Study contact

Participant-facing contact information may include:

- Name or team
- Email
- Phone
- Website

Study contact information is publicly visible on active postings.

A public contact does not automatically receive application study access.

### Additional information

Additional information is optional.

When empty, the public section is omitted.

## Participant type is authored later

Participant type is not selected on the Study Information form.

The following required selection occurs on the eligibility-authoring page:

- Healthy participants
- Participants with specific conditions
- Both

The selected participant type is stored as a study property even though it is authored during the next workflow step.

See [Eligibility-Criteria Authoring](../06-recruitment/eligibility-criteria-authoring.md).

## Search and matching use

Study Information supports:

- Public study search
- Participant study-interest matching
- Public summaries
- Detailed posting display

Study Information and eligibility criteria have different purposes:

```text
Study Information:
    Is this the kind of study the participant wants to consider?

Eligibility criteria:
    Does the participant appear to satisfy recruitment criteria?
```

## Property-value storage

Study Information values use the flexible property-value model.

A property is stored as either:

- Scalar `saved_value`
- One or more lookup relationships

See [Study Property Model](../07-data-model/study-property-model.md).

## AI-assisted authoring

Optional AI assistance may suggest supported Study Information values.

The study team remains responsible for final values.

See [AI-Assisted Study Posting Authoring](ai-assisted-posting-authoring.md).

## Public display

Active, non-archived postings may display:

- Title
- Locations
- Purpose
- Eligibility summary
- What is involved
- Compensation
- Additional information
- PI
- Department
- Study identifier
- Posting dates
- Study contact

See [Public Study Discovery](../06-recruitment/public-study-discovery.md).

## Related pages

- [Posting Creation](posting-creation.md)
- [AI-Assisted Study Posting Authoring](ai-assisted-posting-authoring.md)
- [Eligibility-Criteria Authoring](../06-recruitment/eligibility-criteria-authoring.md)
- [Study Property Model](../07-data-model/study-property-model.md)
- [Public Study Discovery](../06-recruitment/public-study-discovery.md)
