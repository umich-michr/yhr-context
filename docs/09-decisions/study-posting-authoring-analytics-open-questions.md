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

1. Is a text-file upload stored as `RAW_TXT`, and can it be distinguished analytically from pasted
   text?
1. What is the maximum accepted source size?
1. Are uploaded source files retained outside the generation-audit table?
1. What document-extraction libraries are used?
1. What document-extraction failure categories are recorded?

## Prompt and model versioning

1. Is prompt history retained when `APPLICATION_SETTING.VALUE` changes?
1. Can every generation attempt be mapped to the exact prompt version?
1. Is model name always available in `LLM_METADATA`?
1. Are deployment, prompt, and model changes timestamped for analysis?
1. Are temperature and other generation parameters retained?

## Prompt-requested and observed suggestions

1. What exact suggestion cardinality does each current prompt version request for each field?
1. Are invalid lookup suggestions removed before storage, before display, or both?
1. Is suggestion rank retained exactly as returned?
1. Can a selected suggestion be deselected before Study Information submission?
1. Are selected suggestions captured only at form submission?
1. Are duplicate lookup identifiers removed before display?
1. Which validation rules are applied to the AI response before suggestions are stored?
1. How should analyses distinguish:
   - Prompt-requested count
   - Model-returned count
   - Parsed count
   - Stored count
   - Displayed count?

## Feedback

1. Is free-text feedback the only feedback mechanism?
1. Is feedback stored when the user skips the feedback interface?
1. Can feedback be edited after Study Information submission?
1. What is the maximum feedback length?
1. Can feedback submission fail independently of Study Information submission?
1. Does feedback failure block progression to eligibility authoring?

## Attempt completion

1. Does every successful final submission set `END_TIME`?
1. Can `FINAL_SUBMISSION` exist when `END_TIME` is null?
1. Can `END_TIME` exist without a created study?
1. Can one study have multiple completed posting attempts?
1. What exact timestamp tolerance should be used to attribute a created study to the posting attempt
   that created it?
1. Can final-submission audit capture succeed while operational study creation fails, or vice versa?
1. Are study creation, creator provisioning, memberships, final audit capture, and PI notification
   part of one transaction?

## AI error classification

1. Can a generation row indicate failure without a generation-error row?
1. Is `LATENCY_MS = 0` a reliable secondary error signal?
1. Can a successful AI response have zero or missing latency?
1. What standardized error categories should be derived from stack traces?
1. How long are stack traces retained?
1. Is there a non-stack-trace error code suitable for safer analysis?
1. How should an AI error followed by successful manual completion be represented in summary
   reports?

## Timing

1. Does frontend Study Information timing include AI-generation wait time?
1. Does it include browser idle time?
1. Does it continue while the browser tab is inactive?
1. Can a user revisit Study Information and overwrite or accumulate timing?
1. What tolerance defines agreement between audit and Splunk timing?
1. What exact date did audit-based timing begin?
1. What exact historical period has reliable Splunk coverage?
1. How should multiple browser tabs be handled?
1. How should repeated attempts for one study be handled?
1. Does feedback submission time occur inside the measured Study Information duration?

## First-time institutional users

1. Is an `APP_USER` creation timestamp available for historical analysis?
1. Are all logins without an `APP_USER` guaranteed to use `LOGIN_AUDIT.USER_ID = 0`?
1. Can any workflow other than successful posting creation, accepted invitation, or PI
   reconciliation create a staff `APP_USER`?
1. Are creator `APP_USER` creation, study creation, and creator membership creation atomic?
1. Is application-wide `STAFF` assignment created at the same time as the first `APP_USER`?
1. How should username changes be reconciled across historical login and posting-attempt records?

## HR enrichment

1. What HR fields are approved for this analysis?
1. Should appointments remain as child rows rather than concatenated text?
1. How should simultaneous appointments be represented?
1. How should missing HR records be classified?
1. How should former employees or external collaborators be represented?
1. Which organizational groupings are safe for publication?
1. How should small departments or rare roles be suppressed?

## Attempt classification

1. Should AI adoption include attempts where generation failed?
1. Should an AI-generation error followed by manual completion be reported as:
   - AI-exposed
   - Mixed workflow
   - Manual completion after AI failure?
1. Should a dropped attempt later followed by completion be counted independently?
1. What time interval should define a retry sequence?
1. How should attempts by different users for the same study be grouped?
1. Should a current-state `USER_TYPE` sanity-check field be included in publication-oriented
   datasets?
1. What historical source, if any, can determine whether `APP_USER` existed at attempt start?

## Suggestion usefulness

1. What text-similarity method is approved?
1. What threshold defines edited versus substantially rewritten?
1. Should lookup-field usefulness use Jaccard similarity, precision and recall, or exact equality?
1. How should suggestion order affect usefulness?
1. How should contact suggestions be scored?
1. How should generic and specific compensation suggestions be compared?
1. Should user feedback be analyzed qualitatively, quantitatively, or both?
1. How should duplicate lookup suggestions be handled?
1. How should empty selected-suggestion arrays be distinguished from unavailable feedback capture?

## Eligibility complexity

1. What are the final construct definitions for:
   - Representational complexity
   - Interface-specific authoring complexity
   - Participant eligibility-decision complexity
   - Machine-evaluation complexity?
1. Which component features belong in each complexity construct?
1. How should weights be estimated and validated?
1. Should the published method provide:
   - A feature vector
   - A composite score
   - Both?
1. How should legacy and current eligibility-authoring interfaces be distinguished?
1. How should free-text `OTHER` criteria be weighted?
1. How should ambiguous or unsupported ClinicalTrials.gov criteria be represented?
1. What human-annotation protocol should validate free-text conversion?
1. Which participant outcomes should validate eligibility-decision complexity?
1. Which staff outcomes should validate authoring complexity?
1. How should complexity be handled for incomplete attempts whose final eligibility criteria were
   never persisted?
1. Can later successful-study complexity be used only as an explicitly labeled sensitivity analysis?

## Outcome analysis

1. What is the primary effectiveness outcome?
1. Is Study Information time more appropriate than total creation time?
1. Should eligibility complexity be treated as:
   - Confounder
   - Moderator
   - Separate outcome?
1. Which downstream recruitment outcomes are approved?
1. How should study-population rarity be controlled?
1. How should repeated users and repeated studies be modeled?
1. What minimum sample size is needed for subgroup analysis?
1. How should AI-generation failures be included in adoption and effectiveness analyses?
1. How should successful manual completion after an AI failure be analyzed?
1. What pre-specified rules will be used for timing outliers and idle sessions?

## Publication

1. What data-governance review is required before publication analysis?
1. Which staff identifiers must be pseudonymized?
1. Can study text be used in publication examples?
1. How should small cells be suppressed?
1. Can HR title, department, school, or role be reported?
1. How should AI errors and infrastructure incidents be described?
1. What limitations must be reported for nonrandom AI adoption?
1. Can raw AI metadata be retained in an analytical dataset?
1. What review is required before publishing a reference implementation of the complexity score?

## Future eligibility AI

1. Which criterion variables may AI suggest?
1. Must suggestions include source evidence?
1. How should unsupported criteria be mapped to `OTHER`?
1. How should AI-generated criteria affect matched-population counts before acceptance?
1. What review UI is required?
1. What telemetry is needed for expression-level acceptance and editing?
1. How should eligibility-AI safety and governance differ from Study Information assistance?
1. How should generated eligibility criteria be compared with manually authored criteria using the
   complexity framework?

## Related pages

- [AI-Assisted Study Posting Authoring](../05-study-management/ai-assisted-posting-authoring.md)
- [Study Posting Creation](../05-study-management/posting-creation.md)
- [Study-Posting Authoring Audit Model](../07-data-model/study-posting-authoring-audit-model.md)
- [Study Posting Authoring Telemetry](../08-operations/study-posting-authoring-telemetry.md)
- [Study Posting Authoring Timing Analysis](../08-operations/study-posting-authoring-timing-analysis.md)
- [Study Posting Authoring Analysis Dataset](../08-operations/study-posting-authoring-analysis-dataset.md)
- [Eligibility-Criteria Authoring Complexity](../08-operations/eligibility-criteria-authoring-complexity.md)
- [AI-Assisted Study Posting Authoring Effectiveness](../08-operations/ai-assisted-study-posting-authoring-effectiveness.md)
