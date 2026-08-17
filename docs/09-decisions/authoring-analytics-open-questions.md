---
title: Authoring and Analytics Open Questions
summary: Unresolved questions about AI-assisted study-posting authoring, eligibility authoring, and telemetry analysis.
status: open
relevant_when:
  - reviewing_ai_assisted_authoring
  - defining_authoring_telemetry
  - planning_complexity_metrics
  - evaluating_audit_schema
---

# Authoring and Analytics Open Questions

This register contains only unresolved questions about AI-assisted study-posting authoring, eligibility-criteria authoring, and related telemetry analysis.

It should not be used to confirm behavior that the implementation does not yet verify.

## AI suggestion generation

1. Can a study posting have multiple AI generation attempts before final submission?
2. Is the latest suggestion set the only one shown to the user, or are prior attempts retained in the UI?
3. Is the model selection fixed, configurable, or versioned per institution?
4. Does the generation request include the full source text or only a filtered subset?
5. Are prompt templates stored, versioned, and auditable?
6. What happens when text extraction fails for an uploaded document?

## Study-information suggestion selection

1. Can the user select multiple suggestions for one field?
2. Can a selected suggestion be edited after selection and before save?
3. Is suggestion selection captured per field or only at the posting level?
4. Are ignored suggestions still retained for analysis?
5. Is feedback optional or required before final submission?

## Timing capture

1. Does study-information timing exclude idle time if the user leaves the page open?
2. Does the study-information timer pause during modal dialogs or document preview?
3. Does eligibility timing begin immediately after study-information save or after the eligibility page fully renders?
4. Does total posting time include AI generation wait time?
5. How are aborted sessions represented in timing metrics?

## Eligibility-criteria authoring analytics

1. Should eligibility-complexity metrics be calculated from groups, clauses, expressions, or all three?
2. Should `OTHER` free text count more heavily than structured expressions?
3. Should negated operators be weighted differently from positive operators?
4. Should medical-condition selections be normalized before counting complexity?
5. Should the analytics distinguish inclusion-heavy studies from exclusion-heavy studies?
6. Should group count be treated as a linear or nonlinear complexity factor?

## Schema and audit questions

1. Does the physical schema store one generation audit row per attempt or per posting?
2. Can multiple suggestion payloads exist for one posting attempt?
3. Are generated suggestions stored as normalized rows or as serialized JSON?
4. Is the user feedback stored as free text, a fixed rating, or both?
5. Are the timing fields duration-only or timestamp-pair derived?
6. Are AI-related audit records retained independently of the base posting record?

## Observational-analysis questions

1. Which confounders should be controlled for in AI-assisted vs manual comparisons?
2. Should analysis split by source type or by document format?
3. Should generation-success metrics be computed per request, per field, or per posting?
4. Should suggestion usefulness be measured by acceptance rate, edit distance, or downstream time savings?
5. Should eligibility-authoring time be modeled separately from study-information time?
6. Should the analysis compare complete postings only, or include abandoned attempts?

## Related pages

- [AI-Assisted Study Posting Authoring](../05-study-management/ai-assisted-posting-authoring.md)
- [Eligibility-Criteria Authoring](../06-recruitment/eligibility-criteria-authoring.md)
- [Authoring Telemetry and Complexity Analysis](../08-operations/authoring-telemetry-and-complexity.md)
- [Open Questions and Known Concerns](open-questions.md)
