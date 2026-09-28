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
1. Country and ZIP entered for the loved one are stored on the loved-one profile and are not copied
   to the minimal owner.
1. The minimal owner's missing required fields are country, ZIP, biological sex assigned at birth,
   date of birth, race/ethnicity, and parent/guardian-of-a-child response.
1. The owner completes the self profile through ordinary Profile cards.
1. Profile completion does not change the owner's restricted visibility.
1. Related account contact/profile fields are not synchronized; preferred-language propagation from
   owner to loved ones is the confirmed exception.
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
1. Loved-one workflows add one common represented-loved-one acknowledgment covering adults and
   children.
1. The common acknowledgment does not create a separate `USER_AGREEMENT.TYPE`.
1. The audit type does not distinguish self and represented-loved-one presentation.
1. The frontend does not select separate child and adult agreement variants.
1. Loved-one workflows use a common acknowledgment covering both adults and children.
1. The common acknowledgment is not persisted in the agreement audit.
1. A user without an audit record for the current agreement type and version must review the
   agreement at login.
1. A participant who confirms decline is deactivated.
1. Agreement decline targets the current authenticated account context:
   - Owner context deactivates the owner and enabled loved-one accounts.
   - Loved-one context deactivates only the represented loved-one account.
1. The agreement-decline confirmation does not offer account selection.
1. A study team member who declines cannot continue into application features.
1. Agreement-audit username attribution is account-specific:
   - Self signup writes the self username.
   - Initial loved-one signup writes one owner row and one loved-one row.
   - Add Loved One writes the new loved-one username.
   - Login-time re-agreement writes the authenticated context's username.

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

### Loved-one age-out

1. Mature age and warning interval are configurable application settings.
1. The warning is stored in `CHILD_DEACTIVATION_NOTICE`.
1. Age-out writes `USER_DEACTIVATION` with reason `CHILD_TURNED_ADULT`.
1. The child is removed immediately from the local active-user store handling the transition.
1. Redis system-recommendation cleanup is asynchronous.
1. The owner remains active and receives a deactivation notice when available.
1. No separate age-out PHI-audit event is confirmed.

### Matching memory

1. Active studies and active participants are maintained in application memory.
1. Matching reads candidate entities from memory to reduce database-read latency.
1. The database remains the authoritative persistent source.
1. Relevant entity updates update the database and the in-memory representation.
1. Temporal participant-property changes must be reflected in memory.
1. Deactivated participants and inactive studies must be removed from active in-memory matching
   data.
1. Scheduled processing handles time-based transitions and synchronization.
1. Child age-out uses date of birth and configured age thresholds.
1. Age-out deactivation immediately removes the child from the handling process's active-user store
   and initiates asynchronous Redis system-recommendation cleanup.
1. Active-study synchronization uses `V_ACTIVE_STUDY` as its membership source; additions trigger
   matching and removals trigger asynchronous study-recommendation cleanup.

______________________________________________________________________

# Phase 1: Participant Agreement Attribution and Lifecycle

These questions should be resolved before agreement analytics or detailed deactivation behavior is
described as complete.

## AGREEMENT-001: Loved-one-context principal username — resolved

The backend behavior is confirmed:

- Initial self signup writes the self account username.
- Initial signup for a loved one writes two acceptance rows: the owning account username and the
  generated loved-one username.
- Add Loved One writes one acceptance row for the newly generated loved-one username.
- Login-time re-agreement writes the authenticated security principal's username. In loved-one
  context, this is the loved-one account's generated username.

The audit record does not identify the rendered child/adult wording variant.

## AGREEMENT-003: Child-versus-adult displayed clauses — resolved

The frontend does not select separate child and adult agreement variants.

All participant workflows use agreement type `VOL` and load one institution- and language-specific
volunteer agreement body. Relationship, date of birth, age, and child/adult category are not inputs to
agreement-body selection.

Loved-one workflows add one common represented-loved-one acknowledgment. Its wording explicitly
covers both an “adult or child” represented by the owner.

Relationship-specific child/adult wording exists in the signup form and is validated against date of
birth, but it does not select the agreement body. Neither the rendered body nor the common
acknowledgment variant is stored in `USER_AGREEMENT_AUDIT`.

## AGREEMENT-004: Decline target in loved-one context — resolved

The agreement-version interruption supplies the current authenticated context's `userId` to the
frontend. After a yes/no confirmation, the decline callback posts that ID to the participant
deactivation endpoint.

There is no target-account chooser in the agreement-decline confirmation.

Consequences:

- Decline in owner context targets the owner and cascades to enabled loved-one accounts.
- Decline in loved-one context targets only the represented loved-one account.
- The owner and sibling loved-one accounts remain enabled after individual loved-one decline.

The ordinary Account Settings deactivation screen is a separate workflow and may display related
accounts for selection.

## AGREEMENT-005: Decline reason and operational history — resolved

The unsigned-agreement response supplies the `DECLINED_USER_AGREEMENT` lookup value as its
`deactivationReason`. The frontend submits that value unchanged to the participant-deactivation
endpoint.

The common deactivation service persists `USER_DEACTIVATION` with:

- Target user ID
- Deactivation timestamp
- Reason lookup reference for `DECLINED_USER_AGREEMENT`

No successful `USER_AGREEMENT_AUDIT` row or distinct agreement-decline record is created. Previous
agreement-acceptance rows remain historical evidence but do not satisfy a newer current-version
check.

Agreement decline uses the standard account-deactivation notification:

- Owner decline emails the owner and includes enabled dependent accounts affected by the cascade.
- Individual loved-one decline emails the owner about that loved-one account.
- No separate agreement-decline email method or template is used.

There is no agreement-decline-specific PHI-audit function. `ADMIN_DEACTIVATE_USER` applies only when
an administrator performs the deactivation.

The persistence behavior is confirmed. Whether a particular administration UI exposes this reason
and timestamp remains a separate user-interface question.

## AGREEMENT-006: Support reactivation workflow — application behavior resolved

The current administrator workflow is in the React `yhr-study-team` application, not the obsolete
standalone admin project.

Only administrators may use Customer Support → Help Participants. They find a participant by email or
name, select the specific profile, review the inactive status and reason, and confirm reactivation.

Confirmed scope:

- Owner reactivation restores only the owner.
- Loved-one accounts must be reactivated from their own profiles.
- Loved-one reactivation also restores an inactive owner.
- `CHILD_TURNED_ADULT` loved-one accounts cannot be reactivated.
- The modal previews the affected accounts before submitting the selected user ID.

Backend reactivation restores the account to active memory, initiates rematching, and deletes the
deactivation row. It does not accept the current agreement.

No dedicated participant email or in-application reactivation notification is confirmed. Support
communication about the next login and required agreement acceptance remains an operational
procedure rather than implemented application behavior.

Implementation caution: the current UI disables child-age-out reactivation using seeded numeric
reason ID `261001`. The backend independently checks the semantic `CHILD_TURNED_ADULT` lookup and is
authoritative if deployment IDs differ.

## AGREEMENT-008: Agreement-definition and policy retention

Hard deletion removes participant agreement-audit rows. Acceptance rows retain
version strings, but this model does not store historical agreement text.

Determine audit retention, external definition archives, and institutional
records-retention requirements.

______________________________________________________________________

# Phase 2: Minimal Owning Profiles

## PROFILE-001: Exact incomplete fields — resolved

The current signup-for-a-loved-one path gives the minimal owner:

- First name
- Last name
- Communication email/username
- Preferred language
- Restricted visibility
- Explicit no-current-condition and no-past-condition responses
- Learned-from data when supplied

Country and ZIP are stored only on the loved-one profile; no current frontend, Java service, test, or
migration path copies them to the owner.

The owner's exact missing required fields are:

- Country
- ZIP
- Biological sex assigned at birth
- Date of birth
- Race and/or ethnicity
- Parent/guardian-of-a-child response

Optional completeness fields also remain unanswered but do not belong to the required-field gate.

## PROFILE-002: Completing the owner profile — resolved

There is no dedicated registration continuation or persisted self-participation state.

While operating in owner context, the owner uses ordinary Profile cards:

- Contact Information for country and ZIP
- Demographics for biological sex, date of birth, race/ethnicity, and parent/guardian status
- Other cards for optional percentage completeness
- Study Interests for optional recommendation filters
- Visibility for the independent study-team visibility choice

The owner account is already activated with the loved-one account. Profile completion does not require
another activation or a separate agreement type.

## PROFILE-003: Visibility after profile completion — resolved

The minimal owner starts with `visibleToStudyTeams = false`.

Required-field completion and percentage completeness do not include or modify visibility. The owner
remains restricted until explicitly changing the Visibility profile section.

Owner and loved-one visibility values belong to separate profiles and do not propagate.

## PROFILE-004: Country and ZIP copying — resolved

The current implementation does not copy country or ZIP from the loved one to the minimal owner.

It also does not maintain ongoing address synchronization:

- Add Loved One saves only the new loved-one profile.
- Later owner contact edits update only the owner.
- Later loved-one contact edits update only that loved one.
- No country/ZIP propagation hook or database trigger is present in reviewed source or migrations.

Preferred language is the confirmed exception: changing the owner's language updates loved-one
preferred language.

## PROFILE-005: Profile-completeness representation — resolved

There is no persisted profile-complete flag or percentage.

The participant frontend computes:

1. A missing-required-fields list for essential unanswered data.
1. A broader profile-completeness percentage that includes optional questions.

Study Interests and Visibility are excluded from both calculations.

A participant can satisfy required fields without reaching 100%, and can reach 100% while retaining
restricted visibility. These are calculated presentation/workflow measures rather than account
lifecycle states.

Implementation concern: the required-field module mutates a module-level field array when adding the
owner-only parent/guardian requirement. This is current code behavior to review, not a business rule.

# Phase 3: Memory Synchronization

## MEMORY-003: Cross-server propagation for existing active entities — application behavior resolved

Active participant and study stores are `ConcurrentHashMap` collections owned
by one application process. Ordinary update hooks invoke the local Spring store
bean directly:

- Participant matching-trigger advice reloads the handling process's
  active-user entry.
- Study update and import paths add, update, or remove the handling process's
  active-study entry.
- Matching reads the initiating process's local active entities.

The reviewed application does not propagate participant or study source-entity
changes to other application servers through:

- An entity-change message queue
- A Spring application-event broadcast
- Redis pub/sub
- A distributed active-entity cache
- A database notification listener
- Another confirmed cross-process refresh channel

The configured Java Message Service queue is for email delivery. Redis contains
shared derived recommendations and exclusions; it is not the active source-
entity store and does not update another process's participant or study object.

Scheduled active-user and active-study synchronization is membership-only. It
compares database-view IDs with local-store IDs, adds active IDs absent locally,
and removes local IDs no longer active. An ID present in both sets is left
unchanged, so the job does not repair stale fields for an entity that remains
active.

Application-level consequence: an ordinary update refreshes only the handling
process. Another process that already holds the active entity can remain stale
until an explicit entity reload, full store refresh, or application restart.

Remaining deployment-specific questions:

- How many application servers each branded instance runs
- Whether session affinity reduces how often users encounter different local
  copies
- Whether external infrastructure not present in the reviewed repositories
  provides propagation or mitigation
- Which operator procedure repairs cross-server divergence

## MEMORY-004: Startup failure and readiness — application behavior resolved

Process-local stores inherit a synchronous `@PostConstruct` initializer. During
Spring bean creation, each store:

1. Clears its concurrent map.
1. Loads replacement values from its database-backed source.
1. Inserts the returned values.
1. Rebuilds any store-specific derived indexes.
1. Logs object counts and load durations.

Store initialization contains no local catch-and-continue behavior. An exception
from database loading, insertion, or derived-index rebuilding escapes the
initializer and fails that Spring bean's creation. The application therefore
does not intentionally publish a failed startup store as successfully ready.

The refresh algorithm is not an atomic map swap:

- A database-fetch failure after the clear leaves the map empty.
- A failure during value insertion can leave a partially populated map.
- A failure while rebuilding a derived index can leave the primary map loaded
  while the derived index is stale or incomplete.
- During initial context creation, the bean still fails initialization.
- During a later manual or scheduled refresh, an already published store can
  remain empty, partial, or internally inconsistent after failure.

Most prerequisite stores depend on `inMemoryStoreInitLock`, which depends on the
production data source. Active-study construction also depends on its builder
and supporting stores, although the direct lock annotation on
`ActiveStudiesStoreImpl` is commented out.

Application logs provide per-store load start, object count, database-load
duration, total duration, and startup exceptions. No dedicated
store-completeness health indicator, readiness endpoint, or application-level
traffic gate was found in the reviewed backend or routing source.

Remaining deployment-specific question: determine whether each deployed
servlet container, load balancer, monitoring system, or orchestration layer
withholds traffic or alerts based on successful application-context startup and
store completion.

## MEMORY-005: Transaction boundary for incremental updates — code behavior resolved

The participant matching-trigger path uses AspectJ `@After` advice on annotated
controller methods. The advice:

1. Reloads the participant from the database into the handling server's
   process-local active-user store.
1. Reads the reloaded local participant.
1. Submits asynchronous matching through `CompletableFuture.runAsync(...)`.

The advice is not an after-commit listener. No transaction synchronization or
transactional event listener defers these operations until relational commit.
The hook can therefore reload memory and submit matching while the request
transaction is still open.

Confirmed consequences:

- Matching may start before the relational transaction commits.
- A later relational rollback does not automatically restore a prior
  process-local entity.
- Redis work already performed by the asynchronous task is not transactionally
  compensated by relational rollback.
- Matching failures are recorded as application errors and may trigger error
  notification, but they do not roll back the initiating database operation
  and are not automatically retried.
- A later entity update or full recommendation recomputation may repair derived
  recommendation state.

This resolution covers annotated participant update endpoints. Workflows that
explicitly use separate transaction helpers or direct memory operations must be
documented according to their own path.

Database, process-local memory, and Redis do not form one atomic transaction.

## MEMORY-006: Effective synchronization schedule by deployment — application behavior resolved

Confirmed application behavior and installation defaults:

- Cron expressions are persisted in
  `APPLICATION_JOB_SCHEDULE.CRON_EXPRESSION`.
- Seed defaults schedule active-user synchronization daily at 5:05 a.m.,
  active-study synchronization daily at 5:10 a.m., lookup synchronization for
  January 1, 2099 at midnight, and full recommendation recomputation Saturdays
  at 2:00 a.m.
- Administrators can replace persisted cron expressions through the
  administrator job API.
- Every application process initializes its own in-memory Quartz scheduler and
  recreates dynamic jobs from the persisted rows at startup.
- Trigger construction does not assign an explicit time zone, so Quartz uses
  the scheduler/JVM effective default time zone.
- The reviewed configuration does not enable a clustered JDBC Quartz job store,
  general no-overlap annotation, or another application-level cross-server
  execution lock.

The seed values are defaults, not evidence of current deployment values.
Determine for each deployed instance:

- Current persisted cron expressions and whether administrators changed them
- Effective JVM, host, or Quartz time zone
- Number of application servers and schedulers executing the rows
- Any deployment-level clustering, leader election, or external
  duplicate-execution control

## MEMORY-007: Remaining temporal-transition behavior — code behavior resolved

Confirmed runtime behavior:

- `V_ACTIVE_STUDY` determines effective active matching membership using calendar dates, an inclusive
  activation date, an exclusive deactivation date, and `PUBLISHABLE = 1`.
- `activeStudiesSynchronizationJob` reconciles that view with process-local active-study stores.
- Newly active studies trigger matching.
- Removed studies trigger asynchronous Redis system-recommendation cleanup.
- Direct date changes invoke `StudyActiveIntervalService.updateInterval(...)`.
- Imported publishability changes update `STUDY.PUBLISHABLE`, write synchronization history, and may
  open or close the most recent interval.
- Pure date-boundary passage does not invoke the interval service.
- `BatchNotificationJob` queries intervals but does not mutate them.
- Participant deactivation and child age-out remove users from local memory and initiate asynchronous
  recommendation cleanup.
- The seeded `updateActiveIntervalsJob` schedule has no corresponding dynamic-job bean in the
  reviewed source and is not executable by itself.

The remaining item is a design decision rather than an unanswered code path:
`V_ACTIVE_STUDY` excludes the deactivation date while `V_STUDY_STATUS` includes it. Matching follows
`V_ACTIVE_STUDY`; the desired canonical date rule and migration require product and technical
agreement.

Deployment-specific effective cron schedules and time zones remain covered by `MEMORY-006`.

## MEMORY-008: Production freshness monitoring — application behavior resolved

Confirmed application-level observability:

- Full store population and refresh log the database object count,
  database-load duration, and total load duration.
- Scheduled active-store synchronization logs debug start and return messages
  and individual activity, but does not record duration or processed counts.
- Synchronization wrappers log informational success after the synchronizer
  returns. Cooperative interruption can still reach that message, so it is not
  proof of complete reconciliation.
- Matching status is a transient process-local Boolean for one participant or
  study. Task, thread, and outstanding-work identifiers are held only in local
  concurrent maps.
- Matching chunks log debug durations, and matching or scheduler failures create
  durable `APPLICATION_ERROR` rows and may generate error notifications.
- The administrator jobs API reports local previous trigger time, next
  executions, trigger state, and running-instance count. Previous trigger time
  is not a durable business-success timestamp.
- Redis recommendation timestamps and selected entity-level counts are
  queryable, but no global expected-versus-actual key comparison exists.

The reviewed application does not persist or expose:

- Last successful store synchronization or full recomputation
- Synchronization duration, added/removed/skipped/failed counts, or a
  complete-versus-interrupted result
- Database-active-view versus local-store comparison
- Database-to-memory-to-Redis consistency
- Cross-server in-memory divergence
- Expected versus actual Redis recommendation or exclusion key counts
- Failed-entity thresholds
- A dedicated freshness health, readiness, liveness, metrics, or Prometheus
  endpoint
- Server or process attribution for freshness status

The checked-in production logging configuration sets application logging to
`WARN`, while freshness and successful-completion messages are emitted at
`INFO` or `DEBUG`.

Still determine for each deployed instance whether centralized logging,
configuration overrides, dashboards, alerts, health probes, traffic gates,
retention policies, server attribution, or operational thresholds provide
additional production observability.

## MEMORY-009: Recovery procedures — application behavior resolved

Confirmed application recovery behavior:

- A successful application restart clears and reloads the restarted process's
  local stores from database-backed sources and rebuilds store-specific derived
  indexes.
- Restart does not refresh another application process or rebuild Redis.
- Administrators can manually execute active-user synchronization,
  active-study synchronization, and full recommendation recomputation.
- Active-store synchronization repairs membership only. It adds missing active
  IDs and removes inactive IDs, but does not reload an entity present in both
  the database active view and local store.
- `ApplicationStoreService` exposes only `getById` through the reviewed
  administrator controller. No generic operator command for per-entity reload
  or whole-store refresh was found.
- After a startup database outage or startup-load failure, restore database
  availability and restart the affected process. A failed later refresh can
  leave a published store empty, partial, or inconsistent because refresh is
  clear-first and not atomic.
- Matching failures are recorded as application errors and may generate error
  notifications, but are not automatically retried. Operators must rerun the
  applicable synchronization or recomputation after correcting the cause.
- No application-supported cross-server broadcast, divergence detector, or
  cluster-wide repair operation was found. Each affected process must be
  repaired independently.
- Full recomputation can reconstruct ordinary participant-facing `SYSTEM`
  recommendations and exact or partial study-facing recommendations from the
  executing process's current active stores.
- Full recomputation does not reconstruct study-team `USER` promotions or
  Redis-only directional exclusions.
- Relational business records may support selected event reconstruction, but no
  general application routine rebuilds every promotion, exclusion direction,
  reason, member, and timestamp.
- No complete application implementation for Redis backup, restore, cold
  rebuild, or exclusion reconstruction was found.

Operational rule: do not flush or replace Redis expecting full recommendation
recomputation to restore all user actions. Preserve or restore Redis when
exclusions and study-team promotions must survive, verify each affected
process's local stores, and then recompute ordinary recommendations.

Remaining deployment-specific questions:

- Which Redis persistence, backup, restore, and disaster-recovery procedures
  apply to each environment
- Which application processes must be restarted or removed from service during
  repair
- Whether external orchestration provides traffic gating, rolling restart, or
  cross-server coordination
- Which operational runbook verifies restored exclusions, promotions, and
  recommendation completeness

______________________________________________________________________

# Phase 4: Administrative Scheduled-Job Controls

Detailed administrator job control is confirmed to exist but remains to be documented.

## ADMINJOB-004: Cluster-wide and general job concurrency

The reviewed backend does not provide general cluster-wide no-overlap enforcement.

Confirmed protections are limited to full recommendation recomputation:

- Manual execution checks the local Quartz scheduler's currently executing jobs.
- A visible existing run causes a second manual request to be rejected.
- The underlying update-all method is synchronized within one application process.

Confirmed limitations:

- Check and trigger are not atomic.
- The guard is special-cased to `updateAllRecommendationsJob`.
- The Quartz wrapper lacks `@DisallowConcurrentExecution`.
- The reviewed configuration does not enable a clustered JDBC Quartz job store.
- Process-local synchronization does not coordinate multiple application servers.
- Other jobs may overlap, including manual/scheduled overlap.

Still determine the production deployment topology and whether duplicate execution is operationally
acceptable or externally prevented for each job.

## ADMINJOB-006: Durable job-control audit

Application job-control actions produce logs, and scheduler errors create
application errors and notifications. No dedicated durable action-audit table
is confirmed.

Determine production retention and actor attribution for schedule changes,
manual execution, interruption, and failure acknowledgement.

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

## AGEOUT-001: Deployed warning interval

Mature age and warning interval are application settings. Unit tests use age
18 and a 14-day warning interval.

Confirm effective setting values for each branded deployment.

## AGEOUT-004: Immediate age-out cleanup and audit — resolved

Age-out uses the common participant-deactivation service with reason `CHILD_TURNED_ADULT`.

The service:

1. Sets the child's database account enabled flag to false.
1. Removes the child immediately from the handling process's `ActiveUsersStore`.
1. Starts asynchronous Redis recommendation cleanup.
1. Writes `USER_DEACTIVATION` with user ID, timestamp, and reason.
1. Sends the owning account a deactivation notification when the parent is available.

Redis cleanup removes the child from each active study's study-facing recommendations and removes the
child's `SYSTEM` participant-facing recommendation set.

The warning path is separate. It sends a pre-age-out email and writes
`CHILD_DEACTIVATION_NOTICE`, deduplicated by parent ID, child ID, and the birth-date value recorded at
notice time.

No distinct age-out PHI-audit event is invoked by the reviewed path. `USER_DEACTIVATION` and
`CHILD_DEACTIVATION_NOTICE` are the confirmed durable records.

## AGEOUT-005: Adult self-registration and historical data

A loved-one account deactivated for `CHILD_TURNED_ADULT` cannot be reactivated
or transferred.

Determine the supported path for self-registration, username/email reuse,
historical-data linkage, and support requests.

## AGEOUT-006: Age-out failure operations

An interrupted run may leave unvisited accounts active until a later run.

Determine business-exception alerting, manual rerun procedures, partial-run
identification, and proxy-access review.

______________________________________________________________________

# Phase 9: Redis Reconstruction and Freshness

## REDIS-001: Exact key constants

**Status: application behavior resolved; deployed legacy-key inventory
remains deployment-specific.**

Current prefixes:

```text
vol.rec:
std.rec:
vol.exc:
std.exc:
```

Participant-facing source tokens:

- `SYSTEM` — ordinary generated recommendation
- `USER` — study-team promotion, including Ask if interested

Study-facing suffixes:

- `1` — exact
- `0` — partial

Participant-side reasons in `vol.exc:<APP_USER.ID>`:

- `ALREADY_SHOWN_INTEREST`
- `ENROLLED_IN_STUDY`
- `NOT_INTERESTED`

Study-side reasons in `std.exc:<STUDY.ID>`:

- `ALREADY_SHOWN_INTEREST`
- `ASKED_IF_INTERESTED`
- `DISMISSED`

Current code and tests support only these serialized values.

Repository history records removal of an `UNDO_DISMISS` cache prefix
in 2018. No current compatibility reader or migration was found.
Whether a deployed Redis instance still contains old or unknown keys,
and any required migration or rollback procedure, remain
deployment-specific.

## REDIS-002: Cold Redis rebuild procedure

**Status: application behavior resolved; deployment recovery remains open.**

The reviewed application has no automatic cold-Redis detection, complete
rebuild command, or application-managed backup and restore workflow.

`updateAllRecommendationsJob` is the supported application operation for
recomputing ordinary recommendations after the Redis service and process-local
matching inputs are ready. It does not clear Redis first and does not recreate
all user-action state.

Application recovery boundary:

1. Infrastructure must restore Redis when retained promotions, exclusions, and
   timestamps must survive.
1. Operators must verify that the executing application's active participant
   and study stores are current and complete.
1. Full recomputation can then reconstruct ordinary `SYSTEM`
   participant-facing recommendations and exact/partial study-facing
   recommendations.
1. Operators must separately validate `USER` promotions and both exclusion
   directions.

A flush, unrecoverable data loss, or replacement without a valid backup can
therefore cause irrecoverable loss of Redis-only facts. Relational promotion
messages and interest records preserve selected evidence, but no application
routine deterministically rebuilds every current promotion, exclusion reason,
direction, and timestamp from them.

Still deployment-specific:

- Redis snapshot or append-only persistence
- Replication, failover, backup, and restore procedures
- Eviction and memory policy
- Maintenance-mode or write-quiescence procedure
- Key-format migration and rollback plan
- Post-restore validation thresholds and operational ownership

## REDIS-003: Source of full recomputation

**Status: application behavior resolved.**

Full recommendation recomputation uses both persistent and process-local state,
but not by directly joining or rereading all relational business tables during
the job.

Direct job inputs:

- The executing process's `ActiveStudiesStore`
- The executing process's `ActiveUsersStore`
- Existing Redis state consulted by pair-level matching, including directional
  exclusions and current recommendations

The active stores are populated from database-backed sources through separate
startup, refresh, and synchronization paths. Full recomputation itself iterates
the local objects already present in those stores.

The job does not use `STUDY_ACTIVE_INTERVAL` as its matching collection and does
not reconstruct historical exclusions. Active intervals support lifecycle and
notification processing; active-store membership controls the set processed by
the full job.

The job writes new pair-computation timestamps. It does not restore original
recommendation, promotion, or exclusion timestamps.

Relational records preserve only selected facts:

- `RECOMMENDED_STUDY_MESSAGE` preserves participant, study, recommending user,
  message, and promotion-message reason, but has no event timestamp or
  current-state marker.
- `STUDY_VOLUNTEER` preserves expressions of interest and associated
  relational workflow state.

No reviewed application routine converts those relational rows into a complete,
unambiguous reconstruction of all `USER` promotions and directional
exclusions.

## REDIS-004: Exclusion retention and recovery

**Status: application behavior resolved; retention policy and operational
cleanup remain open.**

Exclusions and `USER` promotions have no application-assigned expiration.
Ordinary rematching, full recomputation, participant or study deactivation,
reactivation, eligibility changes, and study archive do not generally remove
them.

Confirmed lifecycle behavior:

- Participant deactivation removes study-facing recommendations for that
  participant and participant-facing `SYSTEM` recommendations. It preserves
  exclusions and `USER` promotions.
- Study deactivation removes exact/partial keys for that study and
  participant-facing `SYSTEM` recommendations. It preserves exclusions and
  `USER` promotions.
- Reactivation restores active-store membership and runs ordinary matching; it
  does not clear retained exclusions or promotions.
- Archive adds no Redis cleanup beyond the study's preceding deactivation.
- Changed eligibility affects ordinary recommendations but does not remove
  exclusion members.

Specific business actions remove or replace specific reasons. Interest replaces
selected dismissal and not-interested state with `ALREADY_SHOWN_INTEREST` in
both directions. Ask if interested can replace study-side `DISMISSED` with
`ASKED_IF_INTERESTED`. Questionnaire submission removes participant-side
`NOT_INTERESTED`. Generic undismissal removes only the requested
participant-side reason.

Hard participant deletion removes relational interest and promotion-message
evidence after initiating asynchronous deactivation cleanup. It does not wait
for Redis cleanup, and the deactivation task does not remove exclusions or
`USER` promotions. Orphaned Redis members can therefore remain.

No general application garbage collector or referential-integrity sweep for
obsolete Redis members was found.

Still open as product, privacy, and operations policy:

- Required retention for each exclusion and promotion reason
- Whether temporary inactivity should preserve all user-action state
- Authorized cleanup of orphaned state
- Production detection and repair procedures
- Whether automated Redis referential-integrity cleanup should be added

Complete Redis-loss recovery remains covered by `REDIS-002` and `REDIS-003`.

## REDIS-006: Redis consistency monitoring

**Status: application behavior resolved; deployment observability remains
open.**

This question overlaps with the resolved application-level portion of
`MEMORY-008`. The reviewed application exposes entity-specific Redis reads,
selected per-study recommendation counts, process-local matching status,
application errors, optional error notifications, local Quartz trigger
information, and application logs.

Those signals do not provide a global or cluster-wide freshness determination.

No application implementation was found for:

- Global Redis recommendation, promotion, or exclusion inventory
- Expected versus actual Redis key or member counts
- Database-active-view versus process-local store comparison
- Database-to-memory-to-Redis consistency checking
- Cross-server in-memory divergence detection
- Last successful full-recomputation tracking
- Durable full-recomputation completion, duration, processed-count, or
  failed-count records
- Freshness thresholds
- Dedicated matching/store health, readiness, liveness, metrics, or Prometheus
  endpoints

Redis scores record member event or computation times, but do not prove current
source-data consistency. The local scheduler's previous trigger fire time does
not prove successful completion or successful Redis writes.

Canonical application behavior is documented under
[Audit and Monitoring](../08-operations/audit-and-monitoring.md#matching-and-memory-observability)
and [Redis Match and Exclusion Model](../07-data-model/redis-match-model.md#match-freshness).

Still deployment-specific:

- Centralized logs and server attribution
- Dashboards and alerts
- Health probes and traffic gates
- Log and metric retention
- Freshness thresholds and escalation policy
- Production Redis inventory and consistency tooling
- Operational ownership and runbooks

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
