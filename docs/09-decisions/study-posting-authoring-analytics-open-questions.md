---
title: Study Posting Authoring and Analytics Open Questions
summary: Unresolved implementation and research decisions for AI-assisted study-posting authoring and analysis.
status: open
---

# Study Posting Authoring and Analytics Open Questions

The following generation-workflow behavior is resolved and documented as current behavior:

```text
One posting attempt has zero or one generation row.
One generation row has zero or one generation-error row.
A failed AI generation displays a blank Study Information form with an error message.
The user may continue manual authoring within the same posting attempt.
Returning to Add Study and trying again creates a new posting-attempt row.
Selected suggestions and optional feedback are captured when Study Information is submitted.
```

See:

- [AI-Assisted Study Posting Authoring](../05-study-management/ai-assisted-posting-authoring.md)
- [Study-Posting Authoring Audit Model](../07-data-model/study-posting-authoring-audit-model.md)

## Source handling

1. Is a text-file upload stored as `RAW_TXT`, and can it be distinguished analytically from pasted text?
2. What is the maximum accepted source size?
3. Are uploaded source files retained outside the generation-audit table?
4. What document-extraction libraries are used?
5. What document-extraction failure categories are recorded?

## Prompt and model versioning

1. Is prompt history retained when `APPLICATION_SETTING.VALUE` changes?
2. Can every generation attempt be mapped to the exact prompt version?
3. Is model name always available in `LLM_METADATA`?
4. Are deployment, prompt, and model changes timestamped for analysis?
5. Are temperature and other generation parameters retained?

## Prompt-requested and observed suggestions

1. What exact suggestion cardinality does each current prompt version request for each field?
2. Are invalid lookup suggestions removed before storage, before display, or both?
3. Is suggestion rank retained exactly as returned?
4. Can a selected suggestion be deselected before Study Information submission?
5. Are selected suggestions captured only at form submission?
6. Are duplicate lookup identifiers removed before display?
7. Which validation rules are applied to the AI response before suggestions are stored?
8. How should analyses distinguish:
   - Prompt-requested count
   - Model-returned count
   - Parsed count
   - Stored count
   - Displayed count?

## Feedback

1. Is free-text feedback the only feedback mechanism?
2. Is feedback stored when the user skips the feedback interface?
3. Can feedback be edited after Study Information submission?
4. What is the maximum feedback length?
5. Can feedback submission fail independently of Study Information submission?
6. Does feedback failure block progression to eligibility authoring?

## Attempt completion

1. Does every successful final submission set `END_TIME`?
2. Can `FINAL_SUBMISSION` exist when `END_TIME` is null?
3. Can `END_TIME` exist without a created study?
4. Can one study have multiple completed posting attempts?
5. What exact timestamp tolerance should be used to attribute a created study to the posting attempt that created it?
6. Can final-submission audit capture succeed while operational study creation fails, or vice versa?
7. Are study creation, creator provisioning, memberships, final audit capture, and PI notification part of one transaction?

## AI error classification

1. Can a generation row indicate failure without a generation-error row?
2. Is `LATENCY_MS = 0` a reliable secondary error signal?
3. Can a successful AI response have zero or missing latency?
4. What standardized error categories should be derived from stack traces?
5. How long are stack traces retained?
6. Is there a non-stack-trace error code suitable for safer analysis?
7. How should an AI error followed by successful manual completion be represented in summary reports?

## Timing

1. Does frontend Study Information timing include AI-generation wait time?
2. Does it include browser idle time?
3. Does it continue while the browser tab is inactive?
4. Can a user revisit Study Information and overwrite or accumulate timing?
5. What tolerance defines agreement between audit and Splunk timing?
6. What exact date did audit-based timing begin?
7. What exact historical period has reliable Splunk coverage?
8. How should multiple browser tabs be handled?
9. How should repeated attempts for one study be handled?
10. Does feedback submission time occur inside the measured Study Information duration?

## First-time institutional users

1. Is an `APP_USER` creation timestamp available for historical analysis?
2. Are all logins without an `APP_USER` guaranteed to use `LOGIN_AUDIT.USER_ID = 0`?
3. Can any workflow other than successful posting creation, accepted invitation, or PI reconciliation create a staff `APP_USER`?
4. Are creator `APP_USER` creation, study creation, and creator membership creation atomic?
5. Is application-wide `STAFF` assignment created at the same time as the first `APP_USER`?
6. How should username changes be reconciled across historical login and posting-attempt records?

## HR enrichment

1. What HR fields are approved for this analysis?
2. Should appointments remain as child rows rather than concatenated text?
3. How should simultaneous appointments be represented?
4. How should missing HR records be classified?
5. How should former employees or external collaborators be represented?
6. Which organizational groupings are safe for publication?
7. How should small departments or rare roles be suppressed?

## Attempt classification

1. Should AI adoption include attempts where generation failed?
2. Should an AI-generation error followed by manual completion be reported as:
   - AI-exposed
   - Mixed workflow
   - Manual completion after AI failure?
3. Should a dropped attempt later followed by completion be counted independently?
4. What time interval should define a retry sequence?
5. How should attempts by different users for the same study be grouped?
6. Should a current-state `USER_TYPE` sanity-check field be included in publication-oriented datasets?
7. What historical source, if any, can determine whether `APP_USER` existed at attempt start?

## Suggestion usefulness

1. What text-similarity method is approved?
2. What threshold defines edited versus substantially rewritten?
3. Should lookup-field usefulness use Jaccard similarity, precision and recall, or exact equality?
4. How should suggestion order affect usefulness?
5. How should contact suggestions be scored?
6. How should generic and specific compensation suggestions be compared?
7. Should user feedback be analyzed qualitatively, quantitatively, or both?
8. How should duplicate lookup suggestions be handled?
9. How should empty selected-suggestion arrays be distinguished from unavailable feedback capture?

## Eligibility complexity

1. What are the final construct definitions for:
   - Representational complexity
   - Interface-specific authoring complexity
   - Participant eligibility-decision complexity
   - Machine-evaluation complexity?
2. Which component features belong in each complexity construct?
3. How should weights be estimated and validated?
4. Should the published method provide:
   - A feature vector
   - A composite score
   - Both?
5. How should legacy and current eligibility-authoring interfaces be distinguished?
6. How should free-text `OTHER` criteria be weighted?
7. How should ambiguous or unsupported ClinicalTrials.gov criteria be represented?
8. What human-annotation protocol should validate free-text conversion?
9. Which participant outcomes should validate eligibility-decision complexity?
10. Which staff outcomes should validate authoring complexity?
11. How should complexity be handled for incomplete attempts whose final eligibility criteria were never persisted?
12. Can later successful-study complexity be used only as an explicitly labeled sensitivity analysis?

## Outcome analysis

1. What is the primary effectiveness outcome?
2. Is Study Information time more appropriate than total creation time?
3. Should eligibility complexity be treated as:
   - Confounder
   - Moderator
   - Separate outcome?
4. Which downstream recruitment outcomes are approved?
5. How should study-population rarity be controlled?
6. How should repeated users and repeated studies be modeled?
7. What minimum sample size is needed for subgroup analysis?
8. How should AI-generation failures be included in adoption and effectiveness analyses?
9. How should successful manual completion after an AI failure be analyzed?
10. What pre-specified rules will be used for timing outliers and idle sessions?

## Publication

1. What data-governance review is required before publication analysis?
2. Which staff identifiers must be pseudonymized?
3. Can study text be used in publication examples?
4. How should small cells be suppressed?
5. Can HR title, department, school, or role be reported?
6. How should AI errors and infrastructure incidents be described?
7. What limitations must be reported for nonrandom AI adoption?
8. Can raw AI metadata be retained in an analytical dataset?
9. What review is required before publishing a reference implementation of the complexity score?

## Future eligibility AI

1. Which criterion variables may AI suggest?
2. Must suggestions include source evidence?
3. How should unsupported criteria be mapped to `OTHER`?
4. How should AI-generated criteria affect matched-population counts before acceptance?
5. What review UI is required?
6. What telemetry is needed for expression-level acceptance and editing?
7. How should eligibility-AI safety and governance differ from Study Information assistance?
8. How should generated eligibility criteria be compared with manually authored criteria using the complexity framework?

## Related pages

- [AI-Assisted Study Posting Authoring](../05-study-management/ai-assisted-posting-authoring.md)
- [Study Posting Creation](../05-study-management/posting-creation.md)
- [Study-Posting Authoring Audit Model](../07-data-model/study-posting-authoring-audit-model.md)
- [Study Posting Authoring Telemetry](../08-operations/study-posting-authoring-telemetry.md)
- [Study Posting Authoring Timing Analysis](../08-operations/study-posting-authoring-timing-analysis.md)
- [Study Posting Authoring Analysis Dataset](../08-operations/study-posting-authoring-analysis-dataset.md)
- [Eligibility-Criteria Authoring Complexity](../08-operations/eligibility-criteria-authoring-complexity.md)
- [AI-Assisted Study Posting Authoring Effectiveness](../08-operations/ai-assisted-study-posting-authoring-effectiveness.md)
