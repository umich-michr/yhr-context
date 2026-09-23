---
title: Open Questions and Known Concerns
summary: Guided completion backlog for unresolved behavior, implementation details, and documentation concerns.
status: open
canonical_for:
  - unresolved_behavior
  - documentation_completion_questions
relevant_when:
  - resolving_undocumented_behavior
  - completing_system_context
  - interviewing_subject_matter_experts
  - reconciling_conflicting_documentation
---

# Open Questions and Known Concerns

This page is the guided completion backlog for the YourHealthResearch.org context repository.

An LLM must not present unresolved items on this page as confirmed behavior.

## Instructions for an LLM facilitating documentation completion

When helping a subject-matter expert complete this repository:

1. Work through one numbered phase at a time.
1. Ask related questions in small groups rather than presenting the complete backlog at once.
1. Do not ask again for information already recorded under
   [Resolved clarifications](#resolved-clarifications).
1. Begin with questions that affect several modules or currently contradict authoritative pages.
1. For each answer, identify:
   - Confirmed current behavior
   - Deployment scope
   - Application version or time period
   - UI behavior
   - Backend behavior
   - Data storage
   - Scheduled-job behavior
   - Exceptions
   - Evidence source
1. Distinguish:
   - Current behavior
   - Historical behavior
   - Proposed behavior
   - Unknown behavior
1. Do not convert an answer into an authoritative rule if the answer is tentative.
1. If an answer applies only to one branded instance, do not generalize it to every deployment.
1. After resolving a question, identify every canonical, support, schema, and routing page affected.
1. Return complete replacement files when requested rather than patches or partial excerpts.

## Suggested answer-capture format

For each resolved question, capture:

```text
Question ID:
Short answer:
Status: confirmed | historical | proposed | still open
Applies to:
Effective version or date:
UI behavior:
Backend behavior:
Data or tables:
Scheduled jobs:
Exceptions:
Evidence:
Files to update:
```

Evidence may include:

- Application source code
- Database DDL
- Database records
- Configuration
- Scheduled-job definitions
- Automated tests
- Screenshots
- Verified production behavior
- Product-owner confirmation
- Institutional policy

## Resolution priority

Use this order unless the subject-matter expert requests a different topic:

1. Participant agreement attribution and account lifecycle
1. Memory synchronization and multi-server behavior
1. Scheduled-job administration
1. Notification generation and delivery
1. CSV import transactions and failure handling
1. PI reconciliation edge cases
1. Loved-one age-out
1. Redis reconstruction and freshness
1. Physical recruitment schema
1. Audit, export, and security controls
1. Product concerns and future enhancements
1. Study-posting authoring analytics

## Resolved clarifications

The following items are confirmed and are no longer open.

### Product and deployment identity

1. YourHealthResearch.org is the platform and product name.
1. `YourHealthResearch.org` is also the marketing website for prospective adopting organizations.
1. Adopting organizations operate separately branded instances.
1. Each branded instance has its own servers, database, supporting infrastructure, configuration,
   and institutional integrations.
1. Confirmed examples include:
   - `UMHealthResearch.org`
   - `UMiamiHealthResearch.org`
   - `BeTheNewNormalMatch.org`
   - `healthresearch.ccts.uic.edu`

### Participant and loved-one accounts

1. Participant visibility is selected during signup.
1. Signup for a loved one creates:
   - A minimal owning account
   - A complete loved-one account
1. The minimal owning account is not a special account type.
1. The minimal owning account defaults to hidden from study teams.
1. The owning account collects:
   - Communication email and username
   - First name
   - Last name
1. Country and ZIP entered for the loved one are copied to the owning account during signup.
1. The loved-one account receives a GUID-based email-like username.
1. The owner's real email is used for communication with both accounts.
1. A loved-one account can also be created later through Add Loved One.
1. Deactivating an owning self account cascades to its loved-one accounts.

### Participant and study-team agreements

1. Current agreement types and versions are stored in `USER_AGREEMENT`.
1. Agreement acceptance is stored in `USER_AGREEMENT_AUDIT`.
1. Known agreement types include:
   - `VOL` for participants or volunteers
   - `STM` for study team members
1. Self and loved-one participant workflows use the same participant agreement type and version for
   audit storage.
1. The participant agreement body is shared between self and loved-one use.
1. Loved-one presentation adds clauses appropriate to agreement on behalf of a represented loved
   one.
1. The additional loved-one clauses do not create a separate `USER_AGREEMENT.TYPE`.
1. The audit type does not distinguish self, child loved-one, and adult loved-one presentation.
1. A user without an audit record for the current agreement type and version must review the
   agreement at login.
1. A participant who confirms decline is deactivated.
1. A study team member who declines cannot continue into application features.

### PI reconciliation

1. The current PI is governed by imported institutional data.
1. When the imported PI changes:
   - The former PI membership is removed.
   - The new PI receives the operational `PRINCIPAL_INVESTIGATOR` membership.
1. Former PI membership is not normally retained merely because the person was previously PI.

### Criteria authoring

1. The criteria data model supports multiple clauses beneath one criterion root.
1. The current eligibility-authoring UI creates one clause per eligibility group.
1. Multi-clause examples describe data-model capability or historical data, not current UI authoring
   behavior.

### CSV row processing

1. CSV rows are processed independently.
1. Rows are processed in file order.
1. A later successful row overwrites an earlier value when both update the same study field.
1. The file is not first reduced to one final row per study.
1. Intermediate operational transitions may occur while a multi-row CSV is processed.

### Notifications

1. Study lifecycle notifications are processed asynchronously.
1. A daily job processes applicable lifecycle announcements.
1. Other Announcements configuration controls applicable recipients.
1. Stable PI status notifications use a one-day stabilization concept.
1. The PI receives a warning approximately one week before the scheduled deactivation date.
1. Ask if interested updates the promoted-match timestamp.
1. Ask if interested moves or emphasizes the match in the study-team-promoted participant grouping.
1. A scheduled job evaluates promoted matches newer than the participant's last login.

### Matching memory

1. Active studies and active participants are maintained in application memory.
1. Matching reads candidate entities from memory to reduce database-read latency.
1. The database remains the authoritative persistent source.
1. Relevant entity updates update the database and the in-memory representation.
1. Temporal participant-property changes must be reflected in memory.
1. Deactivated participants and inactive studies must be removed from active in-memory matching
   data.
1. Scheduled processing handles time-based transitions and synchronization.

______________________________________________________________________

# Phase 1: Participant Agreement Attribution and Lifecycle

These questions should be resolved before agreement analytics or detailed deactivation behavior is
described as complete.

## AGREEMENT-001: Loved-one signup audit username

During initial signup for a loved one, which username is written to:

```text
USER_AGREEMENT_AUDIT.USER_NAME
```

Possible implementations include:

- The owning account's username
- The generated loved-one username
- One record for each account
- A workflow-dependent result

Also determine whether the same rule applies to:

- Initial signup for a loved one
- Add Loved One
- Login-time re-agreement while using loved-one context

## AGREEMENT-002: Agreement presentation persistence

Is the fact that loved-one-specific clauses were presented stored anywhere?

If so, identify:

- Table or log
- Context value
- Agreement rendering version
- Loved-one relationship type
- Timestamp

If not, document that `USER_AGREEMENT_AUDIT` alone cannot prove whether the self or loved-one
presentation was displayed.

## AGREEMENT-003: Child versus adult loved-one clauses

Does the displayed loved-one wording differ between:

- Child loved one
- Adult loved one

If the wording differs, determine whether:

- The distinction is configuration-driven
- It is determined from `LOVED_ONE.RELATIONSHIP`
- It is determined from date of birth
- The rendered variant is audited

## AGREEMENT-004: Decline in loved-one context

If an owner declines an updated participant agreement while operating in a loved-one context, which
accounts are deactivated?

Possible outcomes to verify:

- Represented loved-one only
- Owning account and all loved ones
- Owning account only
- A confirmation screen allows choosing the affected account

## AGREEMENT-005: Decline evidence

Is agreement decline stored separately from account deactivation?

Check for:

- A declined-agreement audit record
- A deactivation reason
- Application logs
- Email notification
- Administrator-visible history

## AGREEMENT-006: Reactivation after agreement decline

When support or an administrator reactivates an account that was deactivated because of agreement
decline:

- Must the current agreement be accepted before reactivation?
- Is the account reactivated first and blocked at login?
- Are cascaded loved-one accounts reactivated automatically?
- Must each loved-one account be reviewed separately?

## AGREEMENT-007: Additional agreement types

Are `VOL` and `STM` the only agreement types in every branded instance?

Determine whether institutions can configure:

- Additional participant agreement types
- Institution-specific study-team agreements
- Language-specific agreement records
- Supplemental agreements

## AGREEMENT-008: Agreement retention

Determine:

- How long `USER_AGREEMENT` definitions are retained
- Whether old definitions remain after a version change
- How long `USER_AGREEMENT_AUDIT` records are retained
- Whether hard deletion removes participant agreement audit rows
- Whether institutional policy requires longer retention

______________________________________________________________________

# Phase 2: Minimal Owning Profiles

## PROFILE-001: Exact incomplete fields

Which required participant-profile fields remain missing on an owning account created through signup
for a loved one?

Identify:

- Database properties
- UI-required fields
- Matching-relevant fields
- Fields copied from the loved one
- Fields intentionally left null

## PROFILE-002: Completing the owner profile

What workflow allows an owner created through loved-one signup to become a participant for self?

Determine whether the owner must:

- Use Edit Profile
- Complete a dedicated registration continuation
- Accept additional clauses
- Choose self visibility
- Define study interests
- Activate another profile state

## PROFILE-003: Visibility after profile completion

When the owner later completes the self profile:

- Is visibility requested again?
- Does the profile remain hidden until explicitly changed?
- Can profile completion automatically make the owner visible?
- Is visibility independent from completeness?

## PROFILE-004: Country and ZIP copying

The initial copy is confirmed. Determine whether later changes are synchronized.

Check these cases:

- Loved-one country or ZIP changes
- Owner country or ZIP changes
- Add Loved One with a different country or ZIP
- Multiple loved ones with different addresses

Do not describe ongoing synchronization unless confirmed.

## PROFILE-005: Profile-completeness representation

How does the application determine that a participant profile is complete?

Determine whether completeness is:

- A persisted flag
- Computed from required fields
- Different by registration path
- Different by institution
- Used by matching or only by UI validation

______________________________________________________________________

# Phase 3: Memory Synchronization

## MEMORY-003: Cross-server propagation for existing active entities

Active stores are process-local. Scheduled synchronization adds and removes
active members but does not refresh entities present in both the database view
and local store.

Determine whether any deployment-specific mechanism propagates an ordinary
participant-profile or study-property update to other application servers
while the entity remains active. No message queue, shared active-entity cache,
or application event broadcast has been confirmed.

## MEMORY-004: Startup failure and readiness

Process-local active stores are populated from database-backed active views
during Spring bean initialization.

Determine:

- Whether a load failure aborts application startup
- Whether a partially populated store can remain available
- Whether readiness or health checks block traffic until all stores initialize
- How operators observe startup-load completion or failure

## MEMORY-005: Transaction boundary for incremental updates

A participant update hook reloads the entity into the local store and then
triggers asynchronous matching.

Determine the exact Spring advice and transaction ordering:

- Whether the database transaction commits before the local memory reload
- Whether matching can start before transaction commit
- What happens when the target transaction rolls back after memory changes
- What happens when local reload succeeds but Redis recomputation fails

Do not claim transactional atomicity across database, memory, and Redis.

## MEMORY-006: Effective synchronization schedule by deployment

Default persisted schedules are documented. Determine for each deployed
instance:

- Effective scheduler time zone
- Whether administrators changed the persisted cron expressions
- Whether multiple application servers run the same schedules
- Whether cluster coordination prevents duplicate execution

## MEMORY-007: Temporal transitions

List every time-based transition handled by synchronization or scheduled jobs, including:

- Study activation
- Study expiration
- Publishability changes
- Child loved-one age-out
- Participant deactivation
- Agreement-related deactivation

For each transition, document the source, job, and memory-removal behavior.

## MEMORY-008: Production freshness monitoring

Process-local task status, logs, application errors, and store counts exist.

Determine whether production operations expose or alert on:

- Last successful synchronization
- Database-to-memory count differences
- Database-to-memory-to-Redis consistency
- Cross-server divergence
- Synchronization duration
- Failed-entity thresholds

## MEMORY-009: Recovery procedures

Restart reloads local stores, scheduled synchronization repairs active
membership, and full rematching recalculates ordinary recommendations.

Document supported operator procedures for:

- Repairing stale data for an entity that remains active
- Recovering from startup database outage or partial store load
- Repairing cross-server divergence
- Recovering Redis exclusions after complete Redis data loss

______________________________________________________________________

# Phase 4: Administrative Scheduled-Job Controls

Detailed administrator job control is confirmed to exist but remains to be documented.

## ADMINJOB-001: Exposed jobs

Which scheduled jobs appear in the administrator UI?

Candidate categories include:

- Memory synchronization
- Participant rematching
- Study rematching
- Notification delivery
- Study lifecycle processing
- Upcoming-deactivation warnings
- Loved-one age-out
- Import or reconciliation
- Email retry

## ADMINJOB-002: Schedule format

Determine:

- Schedule representation
- Time zone
- Minimum frequency
- Maximum frequency
- Validation rules
- Institution-specific defaults

## ADMINJOB-003: Allowed actions

Can administrators:

- Edit schedules
- Run a job immediately
- Pause a job
- Disable a job
- Resume a job
- Cancel a running job
- Retry a failed job

## ADMINJOB-004: Concurrency control

How does the application prevent:

- Duplicate execution
- Overlapping runs
- Two administrators launching the same job
- A manual run overlapping a scheduled run

## ADMINJOB-005: Execution status

What information is visible to administrators?

Possible fields include:

- Last start
- Last completion
- Current status
- Duration
- Processed count
- Failure count
- Error message
- Next scheduled run

## ADMINJOB-006: Audit

Are these events audited?

- Schedule change
- Manual execution
- Pause or disable
- Cancellation
- Retry
- Failure acknowledgement

Identify physical audit tables or log events when available.

## ADMINJOB-007: Authorization

Which roles can:

- View jobs
- Modify schedules
- Run jobs
- Inspect failures

Determine whether every `ADMIN` has equal job-control permissions.

______________________________________________________________________

# Phase 5: Notification Generation and Delivery

## NOTIFY-001: Lifecycle recipient stabilization

Does the one-day stabilization rule apply to:

- Current PI only
- All Other Announcements recipients
- External recipients
- Every lifecycle event
- Only publishability-driven transitions

## NOTIFY-002: Stabilization calculation

Determine exactly when the stabilization period begins and ends.

Clarify whether “one day” means:

- 24 elapsed hours
- The next daily-job execution
- A calendar-day boundary
- An institution-configured interval

## NOTIFY-003: Upcoming-deactivation warning timing

Determine how “approximately one week” is calculated:

- Seven calendar days
- Seven 24-hour periods
- A date-window query
- The first scheduled job within a warning window

Also determine the applicable time zone.

## NOTIFY-004: Changed deactivation dates

If the deactivation date changes after a warning:

- Is another warning sent?
- Is the old warning state cleared?
- Can a study receive multiple warnings?
- Is warning history stored?

## NOTIFY-005: Ask if interested frequency

Which participant preference controls the promoted-study email?

Determine whether delivery can be:

- Immediate
- Daily
- Weekly
- Disabled
- Controlled by one general participant frequency setting

## NOTIFY-006: Last-login definition

Which timestamp is used when comparing a promotion with the participant's last login?

Possible sources include:

- `LOGIN_AUDIT`
- Participant profile field
- Session record
- Owning-account login
- Represented-participant context switch

For loved-one accounts, determine whether the owner's login or a context switch counts as the
represented participant's last login.

## NOTIFY-007: Repeated promotion

Can a study team use Ask if interested more than once for the same participant-study pair?

If yes:

- Is the message replaced or appended?
- Is the timestamp updated?
- Can another email be generated?
- Is prior promotion history retained?

## NOTIFY-008: Digest grouping

When multiple events exist, determine whether email is grouped by:

- Participant
- Study
- Event type
- Recipient
- Branded instance
- Digest period

## NOTIFY-009: Delivery evidence

Document the difference among:

```text
Event created
Notification selected
Email generated
Email handed to email service
Email delivered
Email bounced
Email retried
```

Identify which stages are available in `EMAIL_LOG` or external email-service records.

______________________________________________________________________

# Phase 6: CSV Import Transactions and Failure Handling

The row-order rule is resolved. Transaction and error boundaries remain open.

## IMPORT-001: One-row transaction boundary

Is each CSV row processed in one database transaction that includes:

- Imported-table update
- Operational-study update
- Publishability processing
- PI reconciliation
- Membership changes
- Active-interval changes

## IMPORT-002: Partial row failure

If imported-table persistence succeeds but operational reconciliation fails:

- Is the imported update rolled back?
- Does the imported row remain for later reconciliation?
- Is the row marked failed?
- Can a later row for the same study proceed?

## IMPORT-003: Continuation after invalid row

For each error category, determine whether processing continues:

- Invalid publishability
- Missing PI
- Missing PI email
- Missing PI username
- Unknown column value
- Database failure
- Runtime exception
- Notification failure

## IMPORT-004: Intermediate lifecycle effects

When sequential rows cause:

```text
ACTIVE → INACTIVE → ACTIVE
```

determine:

- How many `STUDY_ACTIVE_INTERVAL` changes occur
- Whether memory is updated after each row
- Whether Redis matching is recalculated after each row
- Whether recomputation is deferred
- How notification stabilization handles the sequence

## IMPORT-005: Import-run identity

Is there an import-run or batch identifier linking:

- File receipt
- Individual row results
- Errors
- Reconciliation actions
- Notifications
- Final completion status

## IMPORT-006: Recovery and correction

After an interrupted file:

- Can processing resume?
- Must the entire file be resubmitted?
- Can duplicate earlier rows be safely processed again?
- Which operations are idempotent?

## IMPORT-007: Token controls

Determine:

- Meaning of `STUDY_IMPORT_TOKEN_GRACE_PERIOD`
- Token lifetime
- Revocation
- Signing algorithm
- Key rotation
- Issuance audit
- Use audit

______________________________________________________________________

# Phase 7: PI Reconciliation Edge Cases

## PI-001: Separate ordinary membership

If a former PI also has a separately established `STUDY_TEAM_MEMBER` membership, does reconciliation
preserve that ordinary membership?

## PI-002: Atomic replacement

Are these operations atomic?

```text
Remove former PI membership
Find or create new PI APP_USER
Create new PI membership
Update notification recipients
```

## PI-003: Reconciliation failure

If removal succeeds but new PI creation fails:

- Is removal rolled back?
- Can the study temporarily have no PI membership?
- Is access restored automatically on retry?

## PI-004: Notification migration

When the PI changes:

- Is the former PI removed from Other Announcements?
- Is the new PI automatically subscribed?
- Are external addresses unchanged?
- Is the PI change itself announced?

## PI-005: Historical PI evidence

Where is PI history retained after the former operational membership is removed?

Possible sources include:

- Imported history
- Audit table
- Study audit
- Application logs
- No retained application history

## PI-006: Username changes

How are institutional username changes reconciled when:

```text
IMPORTED_TEAM_MEMBER.USER_NAME
```

changes for the same person?

Determine whether:

- A new `APP_USER` is created
- The existing username is updated
- Memberships are transferred
- Manual intervention is required

______________________________________________________________________

# Phase 8: Loved-One Age-Out

## AGEOUT-001: Warning interval

How long before the eighteenth birthday is the owning account notified?

## AGEOUT-002: Warning frequency

Is the warning:

- Sent once
- Repeated
- Retried after delivery failure
- Recorded in `CHILD_DEACTIVATION_NOTICE`

## AGEOUT-003: Deactivation time

At what time and in which time zone does age-based deactivation occur?

## AGEOUT-004: Deactivation persistence

Identify:

- Deactivation reason
- Deactivation table
- Notice table
- Audit event
- Memory-removal action
- Redis-removal action

## AGEOUT-005: Adult registration path

After age-out, what should the represented adult do to participate?

Determine whether they:

- Create a new self account
- May reuse the communication email
- Must use a different username
- Can request data transfer
- Can reference historical study interest

## AGEOUT-006: Failed job behavior

If the age-out job fails:

- Does proxy access continue?
- Is the failure retried?
- Is an administrator alerted?
- Is the account removed during the next full synchronization?

______________________________________________________________________

# Phase 9: Redis Reconstruction and Freshness

## REDIS-001: Exact key constants

Confirm:

- Ask if interested source token
- Exact eligibility suffix
- Partial eligibility suffix
- Every exclusion reason
- Any legacy key formats

## REDIS-002: Cold Redis rebuild procedure

Full rematching recalculates ordinary recommendations but does not
automatically detect empty Redis or reconstruct every Redis-only exclusion.

Determine the supported procedure after:

- Redis flush or data loss
- Redis server replacement
- Application deployment requiring rebuild
- Redis key-format change

## REDIS-004: Exclusion retention and recovery

Exclusions are retained during ordinary rematching and deactivation cleanup
unless a specific business action removes or replaces them.

Determine retention and cleanup rules for:

- Participant or study reactivation
- Hard deletion
- Study archive
- Expired promotion
- Complete Redis loss
- Obsolete exclusions with no remaining relational business context

## REDIS-006: Redis consistency monitoring

Recommendation timestamps and counts are available, but no cluster-wide
consistency comparison is confirmed.

Determine whether operators can compare:

- Database source state
- Per-server in-memory match inputs
- Redis recommendations and exclusions
- Last successful full recomputation
- Expected and actual key counts

______________________________________________________________________

# Phase 10: Physical Recruitment Schema

Detailed physical documentation may be completed later. Until then, do not infer columns or foreign
keys solely from table names.

## SCHEMA-001: Interested participants

Document:

```text
STUDY_VOLUNTEER
```

including:

- Primary key
- Study foreign key
- Participant foreign key
- Workflow-list storage
- Interest timestamp
- Eligibility state, if stored
- Unread-message count, if stored
- Uniqueness constraints

## SCHEMA-002: Questionnaires

Confirm the columns and relationships among:

```text
STUDY_SCREEN_QNAIRE
STUDY_SCREENING_QUESTION
STUDY_SCR_QUES_OPTION
VOL_SCR_QUESTION_ANSWER
VOL_QSTN_ANSWR_SLCTD_OPTNS
```

Determine:

- Questionnaire-to-study cardinality
- Question order
- Question type storage
- Required status
- Option order
- Free-text answer storage
- Selected-option storage
- Submission ownership

## SCHEMA-003: Messaging

Confirm the columns and relationships among:

```text
USER_MESSAGE
MESSAGE_TEMPLATE
MESSAGE_ATTACHMENT
MESSAGE_TEMPLATE_ATTACHMENT
```

Determine:

- Conversation scoping
- Sender and recipient references
- `STUDY_VOLUNTEER` relationship
- Attachment storage
- Template ownership
- Deletion behavior

## SCHEMA-004: Labels

Confirm:

```text
VOLUNTEER_LABEL
STUDY_VOLUNTEER_LABEL
```

including:

- Study ownership
- Label title
- Color
- Uniqueness
- Assignment cardinality
- Export fields

## SCHEMA-005: Notifications

Confirm:

```text
NOTIFICATION_SETTING_FREQ
STUDY_NOTIFICATION_SETTING
STUDY_NOTIFICATION_RECIPIENT
EMAIL_LOG
```

including:

- Event type
- Frequency
- Member recipient
- External recipient
- PI subscription
- Delivery status
- Digest ownership

## SCHEMA-006: Promotion and deactivation

Confirm:

```text
RECOMMENDED_STUDY_MESSAGE
USER_DEACTIVATION
CHILD_DEACTIVATION_NOTICE
```

including:

- Participant and study references
- Promotion text
- Promotion timestamps
- Deactivation reason
- Cascading deactivation
- Age-out notice state

______________________________________________________________________

# Phase 11: Audit, Export, and Security Controls

## AUDIT-001: Export auditing

Should CSV export generation receive a dedicated audit event?

Current documentation says it is not separately audited.

Determine whether request logs provide sufficient operational evidence.

## AUDIT-002: CSV formula injection

Determine whether participant-data exports protect spreadsheet users from formula injection in
values beginning with characters such as:

```text
=
+
-
@
```

If not, determine whether the risk is accepted or remediation is required.

## AUDIT-003: Job auditing

Determine whether administrative job changes and manual executions require dedicated audit events.

## AUDIT-004: Invitation auditing

Determine whether invitation creation, resend, revocation, and acceptance should be retained as
historical security events.

## AUDIT-005: Membership auditing

Determine how PI replacement, ordinary member removal, and backend membership overrides are audited.

## AUDIT-006: Attachment security

Determine:

- Malware scanning
- Content-type validation
- Storage encryption
- Retention
- Hard-deletion behavior
- User deletion permissions

## AUDIT-007: Backend overrides

Identify the approval and audit process for backend changes to:

- Membership
- Publishability
- Activation dates
- Participant state
- Job schedules

______________________________________________________________________

# Phase 12: Product Concerns and Future Enhancements

The following are observations or proposed directions, not implemented requirements.

## PRODUCT-001: Ask if interested comprehension

Determine:

- How often users mistake promotion for messaging
- Whether the current modal text is understood
- Whether naming or placement should change
- Whether analytics can measure participant response

## PRODUCT-002: Matched-participant actions

Investigate whether study teams need actions beyond:

- Ask if interested
- Dismiss

Any proposed action must preserve participant privacy and IRB constraints.

## PRODUCT-003: Recruitment effectiveness

Define reliable measures beyond self-reported enrollment totals.

Candidate measures include:

- Posting views
- Matches
- Promotions
- Expressions of interest
- Contact initiation
- Workflow progression
- Verified enrollment from an approved source

## PRODUCT-004: Interested-participant filtering

Determine requirements for:

- Advanced filters
- Screening-answer filters
- Rule-based filtering
- Stop logic
- Saved views
- Export reduction

## PRODUCT-005: Suspicious participation

Before documenting fraud controls, define:

- Duplicate account indicators
- Incentive-driven behavior
- Abnormal interest spikes
- False-positive safeguards
- Study-team review workflow
- Privacy and governance approval

______________________________________________________________________

# Phase 13: Study-Posting Authoring Analytics

See
[Study Posting Authoring and Analytics Open Questions](study-posting-authoring-analytics-open-questions.md)
for the detailed AI-assisted authoring and analytics backlog.

## Cross-reference requirements

When those questions are resolved, update as applicable:

- AI-assisted authoring behavior
- Posting-attempt audit model
- Telemetry sources
- Timing analysis
- Attempt-level analytical dataset
- Eligibility-complexity analysis
- Publication and privacy guidance

______________________________________________________________________

# Completion Criteria

The general context documentation may be considered functionally complete when:

1. Every cross-cutting behavior is represented on a canonical page.
1. Every known contradiction is resolved or explicitly marked open.
1. Deployment-specific rules identify their scope.
1. Database, in-memory, and Redis responsibilities are distinguished.
1. Scheduled jobs have documented triggers, schedules, effects, failures, and recovery behavior.
1. Participant and study-team agreement flows identify their audit behavior.
1. Loved-one ownership, visibility, deactivation, and age-out are documented.
1. PI replacement and access removal are documented.
1. Notification event creation and email delivery are distinguished.
1. CSV row ordering, transaction boundaries, and error continuation are documented.
1. Physical table names are not used with inferred columns or relationships.
1. Support and troubleshooting pages route to the canonical rules.
1. Open questions are not repeated as authoritative behavior.
1. `docs/context-map.yaml` routes every canonical topic.
1. `make check` succeeds.

## Documentation maintenance

When resolving an item:

1. Record the answer, scope, and evidence.
1. Update the canonical topic page.
1. Update [Business Rules](../01-overview/business-rules.md) when the answer is cross-cutting.
1. Update [Terminology](../01-overview/terminology.md) when a definition changes.
1. Update architecture and data-model pages when storage or processing changes.
1. Update support and troubleshooting pages when operational behavior changes.
1. Remove the item from the unresolved phase or mark it resolved.
1. Update `context-map.yaml` when routing changes.
1. Update diagrams when relationships or boundaries change.
1. Run `make check`.
