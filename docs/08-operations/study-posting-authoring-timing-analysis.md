---
title: Study Posting Authoring Timing Analysis
summary: Audit and Splunk timing definitions, historical reconstruction, comparability, cleaning, and validation.
status: mixed
canonical_for:
  - posting_authoring_timing
  - splunk_timing_reconstruction
  - audit_splunk_timing_comparison
relevant_when:
  - comparing_historical_authoring_time
  - validating_timing_sources
  - cleaning_duration_data
---

# Study Posting Authoring Timing Analysis

Study-posting authoring time is available from two sources:

1. Application audit tables
2. Historical access logs reconstructed through Splunk

## Why both sources are needed

Application audit timing was added with the AI-assisted authoring feature.

Splunk contains historical requests from before that feature existed.

Therefore:

- Application audit timing supports detailed recent analysis.
- Splunk timing supports historical comparison.
- The overlapping period can be used to assess comparability.

## Application timing definitions

### Study Information time

```text
STUDY_POSTING_AUDIT.TIME_SPENT_ON_STUDY_INFO_PAGE_MS
```

This is reported by the frontend.

It measures time from arriving on Study Information to submitting that form.

It may include:

- Active editing
- Reading suggestions
- Reviewing source information
- Browser idle time
- Interruptions

### Total attempt duration

Derived from:

```text
END_TIME - START_TIME
```

This covers the attempt from Add Study submission through successful eligibility final submission.

A null `END_TIME` indicates an incomplete attempt unless another status explains the record.

### AI latency

```text
STUDY_POSTING_GENERATION_AUDIT.LATENCY_MS
```

This measures LLM response time.

It is part of the user experience but should not be assumed to equal all waiting time visible in the browser.

## Splunk event markers

The historical Splunk report uses:

### Study start

```text
GET /backend/secure/staff/imported-studies/<study_num>
status = 200
```

### Eligibility page transition

```text
GET /backend/public/criterion-variable
```

### Final posting creation

```text
POST /backend/secure/staff/studies
status = 201
```

## Splunk-derived durations

```text
study_information_time_mins =
    criterion_time - start_time
```

```text
study_eligibility_criterion_time_mins =
    post_time - criterion_time
```

```text
study_creation_time_mins =
    post_time - start_time
```

## Session reconstruction

The report groups requests by:

```text
user
clientip
session_id
```

A new session ID begins at each study-start event.

Potential limitations include:

- Shared client IPs
- IP changes
- Parallel tabs
- Repeated attempts
- Cached reference-data requests
- Missing access-log events
- Background requests
- Multiple criterion-variable requests
- User inactivity

## Audit-versus-Splunk comparison

For overlapping completed attempts, compare:

```text
Audit Study Information time
vs
Splunk Study Information time
```

and:

```text
Audit total attempt duration
vs
Splunk total creation time
```

Recommended comparison fields:

```text
audit_ms
splunk_ms
absolute_difference_ms
signed_difference_ms
relative_difference
difference_within_tolerance
```

## Comparability analysis

Recommended methods include:

- Correlation
- Median absolute difference
- Median relative difference
- Bland-Altman-style difference plots
- Distribution comparison
- Agreement within a predefined tolerance
- Stratification by AI/manual attempt
- Stratification by duration
- Outlier review

Correlation alone is insufficient because two methods may correlate while disagreeing systematically.

## Choosing a tolerance

The tolerance should be selected before examining outcome differences.

Possible tolerance definitions include:

```text
Absolute:
    within 30 seconds
    within 60 seconds

Relative:
    within 5 percent
    within 10 percent

Combined:
    within max(60 seconds, 10 percent)
```

The selected rule should reflect expected differences between browser timing and access-log timing.

## Historical comparison strategy

If Splunk and audit timing agree sufficiently:

- Use Splunk timing for historical and current periods.
- Use audit timing for detailed current analyses.
- Report the validation results.

If they do not agree sufficiently:

- Do not combine them as identical measures.
- Use Splunk consistently for historical trend comparisons.
- Use audit timing for current within-feature analyses.
- Report both measures separately for the overlapping period.

## Cleaning rules

Retain raw timing values.

Flag:

```text
NEGATIVE_DURATION
MISSING_EVENT
EXTREME_DURATION
POSSIBLE_IDLE_SESSION
DUPLICATE_SESSION
PARALLEL_ATTEMPT
AI_ERROR
INCOMPLETE_ATTEMPT
```

Recommended derived fields:

```text
raw_duration
clean_duration
valid_duration_flag
outlier_flag
exclusion_reason
cleaning_rule_version
```

## Splunk query

The current report reconstructs completed attempts:

```spl
index="michr_apps"
host="michr-ap-ps15a.med.umich.edu"
source="/app/log/tomcat/localhost_access_log.txt"
(
    "/backend/secure/staff/imported-studies/"
    OR "/backend/public/criterion-variable"
    OR "/backend/secure/staff/studies"
)

| rex "^(?<clientip>\S+)\s+\S+\s+(?<user>\S+)\s+\["
| rex "\"(?<method>GET|POST|PUT|DELETE)\s+(?<request_uri>[^\s]+)\s+HTTP"
| rex "HTTP/\S+\"\s+(?<status>\d{3})"

| search NOT user IN ("<excluded-test-user>", "-", "- -")

| rex field=request_uri "/backend/secure/staff/imported-studies/(?<study_num>[^\/\?\s]+)"

| eval event_type=case(
    method="GET"
        AND status=200
        AND match(request_uri,"^/backend/secure/staff/imported-studies/"),
            "study_start",

    method="GET"
        AND match(request_uri,"^/backend/public/criterion-variable"),
            "criterion",

    method="POST"
        AND status=201
        AND request_uri="/backend/secure/staff/studies",
            "study_post"
)

| search event_type=*

| sort 0 user clientip _time

| streamstats
    count(eval(event_type="study_start")) as session_id
    by user clientip

| streamstats
    first(eval(if(event_type="study_start",_time,null()))) as start_time
    first(eval(if(event_type="study_start",study_num,null()))) as study_num
    by user clientip session_id

| eventstats
    first(eval(if(event_type="criterion",_time,null()))) as criterion_time
    first(eval(if(event_type="study_post",_time,null()))) as post_time
    by user clientip session_id

| where event_type="study_post"

| where isnotnull(start_time)
    AND isnotnull(criterion_time)
    AND isnotnull(post_time)

| eval study_creation_time_mins=round((post_time-start_time)/60,2)
| eval study_information_time_mins=round((criterion_time-start_time)/60,2)
| eval study_eligibility_criterion_time_mins=round((post_time-criterion_time)/60,2)

| table post_time user clientip study_num
        study_creation_time_mins
        study_information_time_mins
        study_eligibility_criterion_time_mins

| rename post_time as _time
| sort -_time
```

Infrastructure identifiers and real usernames should be parameterized or removed before publishing the query externally.

## Related pages

- [Study Posting Authoring Telemetry](study-posting-authoring-telemetry.md)
- [Study Posting Authoring Analysis Dataset](study-posting-authoring-analysis-dataset.md)
- [AI-Assisted Study Posting Authoring Effectiveness](ai-assisted-study-posting-authoring-effectiveness.md)
