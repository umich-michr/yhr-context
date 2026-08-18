---
title: Business Rules
summary: Canonical cross-cutting application invariants.
status: authoritative
---

# Business Rules

This page is the canonical source for confirmed cross-cutting rules.

## Role systems

1. The application has four application-wide roles:
   - `ADMIN`
   - `STUDY_IMPORTER`
   - `STAFF`
   - `VOLUNTEER`
1. Study associations use two separate roles:
   - `PRINCIPAL_INVESTIGATOR`
   - `STUDY_TEAM_MEMBER`
1. Application-wide roles and study-association roles must not be treated as the same type of role.
1. A `STAFF` user must have a study association to access a particular study.
1. For study-data access, `PRINCIPAL_INVESTIGATOR` and `STUDY_TEAM_MEMBER` have equivalent permissions.
1. `STUDY_IMPORTER` is limited to institutional CSV import functions.
1. `ADMIN` is a superuser with access to all studies and participant data.
1. `VOLUNTEER` represents a participant account.

## Participant identity

1. Participants use local, database-backed accounts.
1. A participant's email address functions as the username.
1. A participant must activate a new account using an expiring email link.
1. The activation link contains a randomly generated Java UUID token.
1. The activation-link expiration duration is an application setting.
1. Participants may deactivate their own accounts and request reactivation through support.
1. Administrators may activate, reactivate, and deactivate participant accounts and reset participant passwords.
1. Participant deletion is a hard deletion initiated only after the participant explicitly emails support.
1. A deleted participant email address may be reused.
1. The database prevents duplicate active email usernames, but the application does not attempt to detect that two accounts represent the same person.
1. Hard deletion removes the participant account, profile, preferences, matches, expressions of interest, questionnaire data, and participant-linked application audit records after administrator confirmation. The application retains the internally assigned participant ID and deletion reason as a deletion marker, while the original request remains in ServiceNow.

## Institutional identity and access

1. Institutional users authenticate through SAML.
1. Institutional accounts are managed through institutional identity providers.
1. Institutional accounts cannot be deactivated or deleted through the application.
1. SAML authentication alone does not grant access to a study.
1. Study access normally requires an active study association.
1. Administrators may access all studies without an ordinary study association.

## Institutional governance

1. Institutional data is loaded into read-only `IMPORTED_*` tables.
1. Ordinary study team members cannot modify imported data.
1. Each institutional import is incremental.
1. Imported rows absent from a subsequent import remain unchanged.
1. PI status is controlled by the institutional source.
1. A valid imported study has exactly one current institutional PI.
1. Only the imported PI role automatically produces application study access.
1. Other imported institutional roles do not automatically grant application access.
1. `PUBLISHABLE` must be either `0` or `1`.
1. A null, missing, or otherwise invalid publishable value is an application error.
1. An operational study missing from a later incremental import remains unchanged.

## Study posting creation

1. A posting can be created only for a `study_num` in `IMPORTED_STUDY`.
1. Only one operational study posting may exist for a `study_num`.
1. Study postings cannot be deleted through application UIs.
1. A posting may be edited but cannot be deleted and recreated through the UI.
1. The posting creator becomes associated with the study.
1. A non-PI creator receives the study role `STUDY_TEAM_MEMBER`.
1. The imported PI receives the study role `PRINCIPAL_INVESTIGATOR`.
1. An `APP_USER` is created for an imported PI when one does not already exist.
1. A PI record missing email or `USER_NAME` is an application error; `USER_NAME` must correspond to the value supplied by the institutional IdP in the SAML ePPN attribute.
1. When a PI `APP_USER` already exists, imported name and email changes are not copied into the existing record.
1. When a PI `APP_USER` is newly created, the imported identity information is copied into it.
1. The PI is notified of posting creation according to the posting-notification workflow.

## Study memberships

1. Any study team member associated with a study may invite another SAML-authenticated institutional user.
1. Any associated study team member may remove an ordinary `STUDY_TEAM_MEMBER`.
1. A posting creator may be removed unless the creator is also the institutionally identified PI.
1. An invited member may be removed.
1. A current PI cannot be removed through ordinary application UIs.
1. Administrators cannot directly create study memberships through application UIs.
1. Backend database intervention may create memberships but is outside the normal UI workflow.
1. Ordinary study team members may export permitted study data.

## Publishability and active status

1. A study's active status depends on:
   - The current date falling within the activation and deactivation dates
   - `PUBLISHABLE` being `1`
1. Activation and deactivation date boundaries are inclusive.
1. `PUBLISHABLE = 0` makes the study inactive.
1. If `PUBLISHABLE` returns to `1` while the date range remains active, the study becomes active again automatically.
1. The application currently does not change the study's deactivation date when publishability becomes `0`.
1. An expired study may be reactivated by changing its dates, provided `PUBLISHABLE = 1`; there is no separate manual-deactivation control.
1. An inactive study loses current matches; fresh matches are recomputed when it becomes active again.
1. Historical interested-participant data for active participants remains accessible while `PUBLISHABLE = 1`, even if the study is inactive by date. Participant-account deactivation still hides that participant's profile information.
1. When an inactive study is accessed through its valid `study_num` URL, the participant sees a message that the study is no longer recruiting.

## Import processing

1. CSV imports are authenticated using expiring JSON Web Tokens.
1. Token timing is governed by the `STUDY_IMPORT_TOKEN_GRACE_PERIOD` application setting.
1. CSV anomalies are detected by application validation.
1. Validation problems are written to logs and emailed to the responsible study importer.
1. CSV reconciliation occurs through Java application code when imported data is applied.
1. U-M reconciliation is performed through a scheduled database workflow and Oracle package.
1. A CSV may contain multiple chronological updates for the same study.
1. Only the latest update for a study is applied to operational application data.
1. Intermediate rows for the same study must not cause temporary study deactivation or notification.
1. Import batches cannot be rolled back through the application.

## Matching

1. Interest matching and eligibility matching are separate evaluations.
1. Eligibility uses three-valued logic:
   - `TRUE`
   - `MAYBE`
   - `FALSE`
1. A missing optional participant profile value referenced by a criterion produces `MAYBE`.
1. Three-valued `AND`, `OR`, and `NOT` follow the truth tables in [Matching and visibility](../06-recruitment/matching-and-visibility.md).
1. `TRUE` eligibility matches are exact matches.
1. `MAYBE` eligibility matches are partial matches.
1. Restricted participants are hidden from study teams until they express interest.
1. Discoverable participants may be visible to authorized study teams as exact (`TRUE`) or partial (`MAYBE`) matches. Partial matches are not shown in participant-facing matched-study lists.
1. Ask if interested does not create an expression of interest.
1. Participants cannot withdraw an expression of interest.

## Match recalculation

1. When a participant profile property referenced by eligibility criteria changes, matches between that participant and all active studies are recalculated.
1. When a participant's study interests change, that participant's matched-study list is recalculated.
1. A participant-interest change does not recalculate study-side matched-participant lists.
1. When a study property referenced by participant study interests changes, matched-study lists are recalculated for affected participants.
1. When study eligibility criteria change:
   - The study's matched-participant list is recalculated
   - Participants' matched-study lists are recalculated
1. Match results are stored in Redis and recomputed asynchronously; failed recalculations require a manually triggered recomputation job.

## Expressing interest

1. At the time of expressing interest, participants are asked to refresh specified temporal profile values.
1. Temporal values include:
   - Past medical conditions
   - Present medical conditions
   - Whether the participant is a parent or guardian of a child under 18
1. Eligibility is rechecked using current participant information; `TRUE` and `MAYBE` may proceed, while `FALSE` cannot.
1. Interest is created only after the eligibility recheck and, when a screening questionnaire exists, successful questionnaire completion. Temporal-profile updates, any questionnaire submission, and interest creation are committed atomically.
1. If the study is not active at submission, whether because of its date range or because `PUBLISHABLE = 0`, interest is not created and the participant sees a not-recruiting message.
1. After interest is successfully recorded, later eligibility changes do not alter the interest relationship.
1. Historical interest remains visible when an active participant later becomes ineligible.

## Questionnaires and exports

1. A study can have only one screening questionnaire.
1. When a study has a screening questionnaire, questionnaire completion is required to finalize the expression-of-interest workflow.
1. Individual questions may be required or optional.
1. Participants cannot edit submitted questionnaire answers.
1. A study must be deactivated before its questionnaire structure can be changed.
1. Study teams may add or delete questionnaire questions while the study is inactive.
1. Existing question content cannot be edited; question display order may be changed while the study is inactive.
1. Questionnaires are not versioned.
1. Only the current questionnaire structure is retained; deleting a question also deletes its prior answers after confirmation.
1. Authorized study team members may export all participant profile fields, including contact information, and all questionnaire answers.
1. Exports are allowed whenever `PUBLISHABLE = 1`, including for inactive studies; export actions are not separately audited.
1. A downloaded CSV cannot be invalidated or recalled by the application.

## Deactivation and historical visibility

1. A deactivated participant no longer participates in matching.
1. A non-publishable or otherwise inactive study no longer participates in active matching.
1. Historical expressions of interest may remain after participant or study deactivation.
1. Participant profile information is hidden when the participant is deactivated or the study has `PUBLISHABLE = 0`. Date-based study inactivity alone does not prevent authorized access to historical interested-participant data while `PUBLISHABLE = 1`.
1. Historical relationship retention and current profile visibility are separate concepts.

## Multi-institution deployment

1. Each adopting institution has a separately branded application instance.
1. Each institutional instance has a separate database schema.
1. Schemas are structurally identical, while data and configuration differ.
1. U-M imports eResearch-derived data.
1. Other institutions upload incremental CSV data through an authenticated application API.
