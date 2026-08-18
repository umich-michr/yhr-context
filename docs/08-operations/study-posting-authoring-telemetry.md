---
title: Study Posting Authoring Telemetry
summary: Telemetry sources, correlation keys, privacy controls, and timing-data cleaning for study-posting authoring analysis.
status: mixed
relevant_when:
  - identifying_authoring_data_sources
  - correlating_authoring_events
  - cleaning_authoring_time_data
  - reviewing_privacy_controls_for_analytics
---

# Study Posting Authoring Telemetry

This page documents operational telemetry inputs for study-authoring analysis.

## Data sources

### Operational database

Relevant data includes:

- Study properties and saved values
- Criteria groups, clauses, expressions, and values
- Posting status and lifecycle timestamps
- Creator and membership references

### Posting audit entities

```text
STUDY_POSTING_AUDIT
STUDY_POSTING_GENERATION_AUDIT
```

Potential fields include:

- Posting-attempt IDs
- `study_num`
- AI-use indicator
- Generated and selected suggestions
- Feedback
- Study-information and eligibility timing
- Final-submission status

Exact physical fields must be verified against the implementation.

### Application and Splunk logs

Logs may include:

- Request time
- Endpoint
- User
- `study_num`
- Client IP
- Response status
- Error details
- Request duration

Example derived Splunk fields:

```text
_time
user
clientip
study_num
study_creation_time_mins
study_information_time_mins
study_eligibility_criterion_time_mins
```

## Correlation keys

Use the most specific key available:

- `study_posting_audit.id`
- Request ID
- Session ID
- User ID
- Timestamp
- `study_num` (fallback)

`study_num` alone may be ambiguous across retries or resumed sessions.

## Privacy considerations

Telemetry may contain sensitive values such as:

- User identifiers
- Email addresses
- Client IP addresses
- Uploaded-document metadata
- Generated text

Analytics datasets should include only required fields and transform/remove IP when not explicitly needed.

## Timing-data cleaning

Timing data can include:

- Negative durations
- Outliers
- Idle browser time
- Interrupted sessions
- Duplicate/retry events

Recommended process:

1. Preserve raw values.
2. Mark invalid records.
3. Define explicit outlier rules.
4. Report with and without outliers.
5. Version the cleaning policy.

Suggested derived fields:

```text
raw_duration_minutes
duration_valid
duration_invalid_reason
duration_clean_minutes
duration_outlier_flag
cleaning_rule_version
```

## Related pages

- [Eligibility-Criteria Authoring Complexity](eligibility-criteria-authoring-complexity.md)
- [AI-Assisted Study Posting Authoring Effectiveness](ai-assisted-study-posting-authoring-effectiveness.md)
- [AI-Assisted Study Posting Authoring](../05-study-management/ai-assisted-posting-authoring.md)
