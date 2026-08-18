---
title: Open Questions and Known Concerns
summary: Unresolved behavior and implementation concerns that must not be presented as confirmed.
status: open
relevant_when:
  - behavior_is_not_explicitly_documented
  - planning_feature_changes
  - reviewing_security_or_governance
  - resolving_data_model_ambiguity
---

# Open Questions and Known Concerns

This page contains only behavior that remains unresolved or requires technical confirmation.

An LLM must not present these items as confirmed functionality.

## Import transaction behavior

1. If one CSV row is invalid, is the complete batch, only that row, or the related study rejected?
2. How is the final row selected when an import contains multiple updates for one `study_num`?
3. Is final-row selection based on file order, source timestamp, sequence number, or another supplied field?
4. Can a partially applied CSV leave imported and operational data inconsistent?
5. Is applying a study's final imported state transactional?
6. Can reconciliation succeed for some studies while failing for others?
7. How is an interrupted import recovered when rollback is unavailable?

## CSV import tokens

1. Does `STUDY_IMPORT_TOKEN_GRACE_PERIOD` represent the primary token lifetime, additional time after expiration, or both?
2. Is a JWT bound to one institutional deployment?
3. Is a JWT bound to one `STUDY_IMPORTER`?
4. Can a JWT be revoked before expiration?
5. Are JWT issuance and use audited?
6. Can one token upload multiple CSV files?
7. What signing algorithm and key-rotation process are used?

## Publishability and notification policy

1. Must `PUBLISHABLE = 1` to create a draft, or only to activate the posting?
2. Should a transition to `PUBLISHABLE = 0` create a persistent local hold rather than allowing automatic reactivation?
3. Should the application retain a reason code for non-publishability?
4. Exactly when does the one-day PI notification delay begin and end?
5. Are both activation and deactivation transitions subject to that delay?
6. Which PI receives a delayed notification when a former PI membership is retained?

## Former PI access and identity

Current behavior adds a new PI membership but does not automatically remove a former PI membership.

1. Should the former PI remain a `PRINCIPAL_INVESTIGATOR`, become a `STUDY_TEAM_MEMBER`, be removed, or be marked inactive?
2. Is continued former-PI access institutionally acceptable?
3. Should reconciliation remove PI memberships that no longer correspond to the current imported PI?
4. Should former and new PIs receive notifications about a PI change?
5. Should PI changes be recorded in a dedicated audit event?
6. What happens when `IMPORTED_TEAM_MEMBER.USER_NAME` does not match the institutional username associated with an existing `APP_USER`?
7. Can an institution change the SAML ePPN value, and if so, how should the imported `USER_NAME` and existing `APP_USER` be reconciled?
8. Is a PI notified when personally creating the posting?

## AI-assisted study-posting authoring and telemetry

Detailed questions are tracked in [Study Posting Authoring and Analytics Open Questions](study-posting-authoring-analytics-open-questions.md).

Use that page for:

- Suggestion generation
- Suggestion selection
- Feedback capture
- Authoring timing
- Complexity scoring
- AI-effectiveness analysis

## Study lifecycle

1. Should the application separately report whether a study is inactive because `PUBLISHABLE = 0` or because its date range does not include today?
2. What participant information, if any, remains available for an inactive but publishable study beyond historical interested-participant data?
3. Can a backend override bypass institutional governance, and what approval and audit trail are required?

## Invitations

1. Should transferable invitations be bound to a recipient identity in a future security model?
2. Should invitation creation, resend, revocation, and acceptance be audited?
3. Should a resend extend expiration or retain the original expiration?

## Participant support and deletion

1. What evidence does support require before acting on a reactivation or hard-deletion email request?
2. How long does ServiceNow retain the deletion request, and what privacy controls apply?

## Matching and interest workflow

1. How do inclusion and exclusion expressions individually interpret `MAYBE` before the overall Boolean result is calculated?
2. What operational alert identifies a failed asynchronous match recalculation?
3. Should there be an administrator-supported correction process for an accidental expression of interest?

## Questionnaires

1. Should a future retention rule replace the current behavior in which deleting a question also deletes submitted answers?
2. Is stale-edit rejection implemented through optimistic locking, and what version field or equivalent mechanism is used?

## Redis match storage

1. What exact `vol.rec` match-source token represents Ask if interested?
2. What exact `std.rec` suffix represents an exact (`TRUE`) match?
3. Is the observed `std.rec:<STUDY.ID>:0` suffix guaranteed to represent `MAYBE` in all deployments and versions?
4. What process removes obsolete exclusion reasons when business state changes?
5. Are Redis recomputation failures monitored or alerted?

## Exports and administrative operations

1. Is the absence of CSV formula-injection protection an accepted risk?
2. Should export actions be explicitly audited?
3. What approval and documentation should govern backend membership creation, administrator provisioning, date overrides, and publishability overrides?

## Documentation maintenance

When an open question is resolved:

1. Update the canonical topic page.
2. Update [Business Rules](../01-overview/business-rules.md) if the decision is cross-cutting.
3. Remove the item from this page or move it to a resolved-decision register.
4. Update `context-map.yaml` if routing changes.
5. Update diagrams and data-model pages when affected.
