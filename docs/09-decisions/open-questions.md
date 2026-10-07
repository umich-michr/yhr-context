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
1. Lifecycle announcements use previous-calendar-day active-interval queries and the current Other Announcements recipient set.
1. Upcoming-deactivation warnings use configurable calendar-day offsets; the installation seed is two and fourteen days ahead.
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

## ADMINJOB-004: Cluster-wide and general job concurrency — application behavior resolved

The reviewed backend does not provide general cluster-wide no-overlap
enforcement.

Confirmed protections are limited to full recommendation recomputation:

- Manual execution checks the local Quartz scheduler's currently executing jobs.
- A visible existing run causes a second manual request to be rejected.
- The underlying update-all method is synchronized within one application
  process.

Confirmed limitations:

- Check and trigger are not atomic.
- The guard is special-cased to `updateAllRecommendationsJob`.
- The Quartz wrapper lacks `@DisallowConcurrentExecution`.
- The reviewed configuration uses an in-memory job store and does not enable
  Quartz clustering.
- Process-local synchronization does not coordinate multiple application
  servers.
- Other jobs may overlap, including manual/scheduled and
  manual/manual overlap.

Application behavior is resolved. Still determine per deployment:

- Application-server and scheduler count
- Any external clustering, leader election, or duplicate-execution control
- Whether duplicate execution is acceptable for each job
- Which jobs require stronger no-overlap guarantees

## ADMINJOB-006: Durable job-control audit — application behavior resolved

Confirmed application behavior:

- Schedule changes and manual execution produce application log messages.
- Scheduler errors create durable `APPLICATION_ERROR` records and may generate
  notifications.
- The administrator API exposes current local scheduler information, not a
  historical action ledger.
- No dedicated application-job action-audit table or record was found for
  actor, action, target job, old and new schedule, request time, or outcome.
- Application-error rows document failures, not successful job-control actions
  or complete administrative history.

Still deployment-specific:

- Whether centralized logs retain authenticated actor and request context
- Log retention and access controls
- External administrative or platform auditing
- Failure-notification acknowledgement and ownership
- Required audit retention for schedule changes and manual execution
- Whether a dedicated durable job-control audit must be added

# Phase 5: Notification Generation and Delivery

## NOTIFY-001: Lifecycle recipient stabilization

**Application behavior resolved.**

Lifecycle activation and deactivation announcements are selected through
`STUDY_ACTIVE_INTERVAL` queries and sent to the complete current recipient set
returned for Other Announcements.

The mechanism is not limited to the PI and does not apply a separate
stabilization rule per recipient. The set may include the current PI, other
selected accepted study team members, and configured external addresses.
Recipients are resolved at dispatch time.

The lifecycle query does not distinguish manual, date-driven, and
publishability-driven causes. It operates on active intervals recorded by the
application.

## NOTIFY-002: Stabilization calculation

**Application behavior resolved.**

The lifecycle-announcement stage evaluates the previous calendar day:

- Start: previous day at 00:00:00
- End: current day at 00:00:00 minus one second

This is not a rolling 24-hour delay after each transition and is not controlled
by a configurable stabilization duration. Processing occurs when the daily
batch job next runs.

Calendar boundaries use the application or Java virtual machine system-default
time zone. The effective deployment time zone remains deployment-specific.

## NOTIFY-003: Upcoming-deactivation warning timing

**Application behavior resolved.**

Upcoming-deactivation warnings use the configurable integer list
`STUDY_ANNOUNCEMENTS_DAYS_AHEAD`. For every configured offset, the daily job
queries the calendar day exactly that many days after the beginning of the
current day.

The installation seed is `2,14`, so the reviewed default configuration checks
for deactivations two and fourteen calendar days ahead. The behavior is not
hard-coded as approximately one week.

Calendar boundaries use the application or Java virtual machine system-default
time zone. The current deployed setting values and effective time zone remain
deployment-specific.

## NOTIFY-004: Changed deactivation dates

**Application behavior resolved.**

The warning workflow stores no sent-warning state or warning history. Changing
the current interval's deactivation date updates the date used by later daily
queries.

A study may receive multiple warnings when:

- More than one warning offset is configured
- Its deactivation date changes and later enters another configured target day
- A configured target day is encountered again after another date change
- The batch job executes more than once for the same window

There is no old warning state to clear and no lifecycle-warning deduplication
marker or idempotency key in the reviewed implementation.

## NOTIFY-005: Ask if interested frequency

**Application behavior resolved.**

The promoted-study email uses the represented participant profile's general
`recommendationNotificationFrequency`, the same preference used for ordinary
new-recommendation email.

Supported values are:

- `DAILY`
- `WEEKLY`
- `BI_WEEKLY`
- `MONTHLY`
- `NEVER`

There is no immediate value and no separate Ask if interested frequency
setting. A `NEVER` preference disables this recommendation-email path.

## NOTIFY-006: Last-login definition

**Application behavior resolved.**

The batch compares Redis recommendation scores with the active represented
participant `User` object's `lastLoginDate`, persisted as
`APP_USER.LAST_LOGIN_DATE`. It does not query `LOGIN_AUDIT` or a session record
for this comparison.

A successful authentication updates `LAST_LOGIN_DATE` and
`NEXT_TO_LAST_LOGIN_DATE` for the authenticated account and updates the local
active-user copy when applicable.

For loved-one accounts:

- The owner's authentication updates the owner account, not all represented
  accounts.
- Authentication directly as a loved-one account updates that loved one's
  timestamp.
- The ordinary change-account endpoint reloads the selected account into the
  security context but does not call `recordLoginTime()`.
- A context switch therefore does not itself update the represented loved
  one's last-login timestamp.

## NOTIFY-007: Repeated promotion

**Application behavior resolved.**

Ask if interested first checks for an existing study-side
`ASKED_IF_INTERESTED` exclusion. If one exists, the operation returns false
without further recommendation or relational-message operations.

While that exclusion remains, a repeated promotion therefore:

- Is rejected
- Does not replace or append the message
- Does not update the `USER` recommendation timestamp
- Does not generate a new qualifying recommendation event for email
- Does not add another `RECOMMENDED_STUDY_MESSAGE` row

The first successful promotion's relational message row remains unless another
business action removes promotion-message rows for the pair. No ordinary
reverse transition was found that clears `ASKED_IF_INTERESTED` solely to allow
repeat promotion.

## NOTIFY-008: Digest grouping

**Application behavior resolved.**

Recommendation email is evaluated per active represented participant and per
applicable recommendation-frequency run.

For one participant, the batch queries all participant-facing recommendation
source sets, including both `SYSTEM` and `USER`, for scores at or after the
participant's `LAST_LOGIN_DATE`. If at least one result refers to a currently
active study, the application sends one generic new-recommendations email.

Therefore:

- Multiple studies are collapsed into one participant email for the run.
- System matches and Ask if interested promotions are not emailed separately.
- The email is not grouped by study or event type.
- Each represented loved-one account is evaluated independently.
- Accounts sharing one email address are not consolidated by recipient
  address.
- Frequency selection determines which batch run evaluates the account.
- Branding and template selection occur during email generation for the
  deployed instance; they are not a cross-instance grouping mechanism.

## NOTIFY-009: Delivery evidence

**Application behavior resolved.**

The application distinguishes these stages:

1. A business event occurs.
1. Notification-selection logic decides whether to notify.
1. `EmailServiceImpl` renders the configured subject and body and creates an
   `EmailMessage`.
1. The rewriter chain may replace or remove recipients and append a change
   description.
1. The active profile selects console, Java Mail, or Java Message Service
   handoff.
1. Local logging records only selected outcomes.

`EMAIL_LOG` stores the rewritten message, attempt date, sender, reply-to,
recipients, subject, body, and `SUCCESS` or `FAILURE`.

Local status meanings are limited:

- Non-JMS `SUCCESS` means the configured client returned without an observed
  exception.
- Java Mail success establishes an observed SMTP transport handoff, not final
  mailbox delivery.
- Console success represents a simulated send only.
- JMS queue-submission success is not written to this application's
  `EMAIL_LOG`.
- A non-JMS message with no recipients can still be recorded as `SUCCESS`
  despite no client call.
- `FAILURE` is written when `SendEmailException` reaches the web controller
  advice. This is not proven for every scheduled or background exception path.

`resendFailedEmailsJob` is seeded hourly and retries every `FAILURE` row. A
successful non-JMS retry changes the row to `SUCCESS`; a successful JMS queue
submission deletes the old row.

The reviewed application has no retry count, maximum, backoff, next-attempt
time, transport message ID, queue ID, bounce status, delivery timestamp,
per-message retry isolation, or idempotency key. Duplicate delivery is possible
after ambiguous handoff/status-update failures or overlapping job execution.

Final mailbox delivery, bounce, provider rejection after initial acceptance,
downstream queue consumption, dead-letter handling, and open/read events require
deployment-specific queue, relay, provider, or recipient-system evidence.

Still deployment-specific:

- Active email-client profile
- Queue consumer implementation and topology
- Provider and relay logging
- Queue redelivery and dead-letter policy
- Bounce and complaint processing
- Monitoring, alerting, retention, and operational runbooks

# Phase 6: CSV Import Transactions and Failure Handling

The row-order rule is resolved. Transaction and error boundaries remain open.

## IMPORT-001: One-row transaction boundary

**Application behavior resolved.**

A CSV row does not have an independent database transaction. The importer uses an explicit
transaction processor with a default batch size of 500 processed rows. One entity manager and one
transaction span the current batch.

For each valid row, the importer stages:

- `IMPORTED_STUDY`
- `IMPORTED_TEAM_MEMBER`
- `IMPORTED_STUDY_TEAM_MEMBER`
- Operational study reconciliation
- Publishability and PI changes
- Membership and active-interval changes applicable to an existing posting

The batch is flushed and committed after each 500 processed rows and again at end of file. Therefore,
these relational changes share the batch transaction, not a one-row transaction.

Process-local active-study updates and asynchronous matching submission occur before batch commit.
They are not part of an atomic transaction with the relational changes. Notification email is not
sent per row; lifecycle selection occurs later from recorded interval state, while the interactive
import-result email is sent after `processFile(...)` returns.

## IMPORT-002: Partial row failure

**Application behavior resolved with a known implementation concern.**

A validation failure occurs before persistence and is recorded as a row error. Processing continues.

A `PersistenceException` during row persistence or reconciliation is caught and recorded, and the
loop continues. The importer does not explicitly roll back that row, mark the shared batch transaction
rollback-only, clear the persistence context, or begin a replacement transaction. If some entity
operations were staged before the exception, source inspection does not guarantee their removal.
The persistence provider may instead mark the entire transaction rollback-only, causing batch commit
to fail. This is a known implementation concern.

If batch flush or commit fails, the current batch is rolled back when still active and all rows held
in the batch's successful-row list are marked unable to commit. Earlier committed batches remain
applied. An uncaught runtime exception stops processing and cleanup rolls back the current
uncommitted batch.

A later row can proceed after validation, CSV-tokenization, or caught persistence errors. It cannot
proceed after an uncaught runtime failure. Process-local memory or asynchronous matching work already
started before rollback cannot be reversed by the database transaction.

## IMPORT-003: Continuation after invalid row

**Application behavior resolved.**

- Invalid publishability: bean-validation error; record the row and continue.
- Missing PI username: bean-validation error; record the row and continue.
- Missing PI email: bean-validation error; record the row and continue. An empty string is rejected
  by email validation even though the field uses `NotNull` rather than `NotBlank`.
- Missing PI first or last name: bean-validation error; record the row and continue.
- Missing PI relationship as a separate concept: the CSV schema supplies one PI identity per row;
  malformed or missing required PI fields are handled by validation.
- Unknown, missing, duplicate, or otherwise invalid header column: record an invalid-header error and
  stop before ordinary row processing.
- CSV tokenization error: record the malformed row, skip it, and continue reading when possible.
- Database `PersistenceException`: record the row and continue in the same batch transaction, subject
  to the partial-row and rollback-only concern in `IMPORT-002`.
- Batch flush or commit failure: roll back the current batch when possible, mark tracked batch rows
  failed, and do not continue into another transaction.
- Uncaught runtime exception: stop processing and roll back the current uncommitted batch during
  cleanup.
- Matching-task failure after asynchronous submission: handle it in the matching future by recording
  an application error and attempting an error notification; it does not fail or retry the import
  row.
- Interactive import-result notification failure: occurs after import processing and does not roll
  back committed import batches.

## IMPORT-004: Intermediate lifecycle effects

**Application behavior resolved.**

For successful sequential rows that cause:

```text
ACTIVE → INACTIVE → ACTIVE
```

the importer does not collapse the rows before reconciliation.

- The active-to-inactive row closes the most recent `STUDY_ACTIVE_INTERVAL`.
- The inactive-to-active row resets the posting activation timestamp to the current time and normally
  creates a new interval when it follows the just-closed interval.
- This produces two interval mutations: one update closing the prior interval and one insert creating
  the reactivation interval, assuming interval validation succeeds.
- Each effective status change invokes the process-local active-study update path during its row.
- Each effective status change submits asynchronous matching or deactivation work during its row.
- Recalculation is not deferred until the import batch or file commits.
- The two rows may share one database transaction, so relational rollback can coexist with
  already-initiated memory or matching side effects.
- The later daily lifecycle query can suppress the superseded deactivation announcement within its
  previous-calendar-day window. Stabilization affects notification selection, not the underlying
  interval, memory, or matching work.

## IMPORT-005: Import-run identity

**Application behavior resolved.**

There is no single end-to-end import-run or transaction identifier.

The closest run-level signals are:

- A processed CSV filename containing the original base and an epoch-millisecond suffix
- A same-basename text result log
- A generated `CSV_FILE_UPLOAD_LOG.ID`
- The processed filename base, authenticated user ID, audit time, counts, and status in that row
- `CSV_FILE_UPLOAD_DETAILS_LOG` error rows linked to the upload-log ID

Limitations:

- Detail rows omit the transient CSV row number.
- Successful rows have no upload-detail records.
- `IMPORTED_STUDY_SYNC_LOG` has action timestamps and entity information but no upload-log ID,
  filename, CSV row number, batch number, request ID, or token ID.
- Memory updates, matching tasks, Redis writes, lifecycle selection, result email, and transport
  evidence do not carry the upload-log ID.
- The audit row is created only after processing returns. Earlier failure can leave an archived CSV
  or text log without an upload audit.
- `SUCCESS` means only that the `ImportResult` has no recorded errors. It does not prove complete
  database-memory-Redis consistency or notification delivery.

Filename and timestamp proximity can support an investigation, but they are not a durable
application-enforced correlation relationship.

## IMPORT-006: Recovery and correction

**Application behavior resolved.**

The application has no resume cursor, last-committed-row checkpoint, or command that continues an
interrupted processed file. Recovery requires a new CSV submission.

Earlier committed batches remain applied. The current uncommitted batch is rolled back when possible,
but process-local memory changes and asynchronous matching work may already have escaped the
transaction. Operators must establish current state before deciding whether to submit a corrective
subset or the whole file.

Replay behavior is only conditionally idempotent:

- Imported entities are found by primary key and inserted or merged, so replay normally updates
  existing imported rows rather than creating duplicate keyed rows.
- Stable PI attributes and publishability are compared with current operational state, so an
  identical row usually avoids those reconciliation changes.
- Reprocessing is not globally idempotent: each completed submission creates new processed artifacts
  and an upload audit; errors create new detail rows; changed state can append reconciliation and
  interval history; and memory, matching, Redis, and notification effects have separate duplication
  and recovery boundaries.
- The caught-persistence-exception path does not prove row-level rollback, so uncertain rows require
  direct state verification.

A safe correction procedure preserves the processed artifacts, identifies committed batches, checks
upload and reconciliation evidence, compares imported and operational state, inspects interval,
memory, matching, and Redis effects, and submits a new incremental file expressing the intended
authoritative state.

## IMPORT-007: Token controls

**Status: application behavior resolved; deployment controls remain open.**

`STUDY_IMPORT_TOKEN_GRACE_PERIOD` is the CSV-upload JWT lifetime in hours, not a post-expiration grace period. The installation seed is `17520` hours, approximately two years. Each deployment's effective value may differ.

An authenticated `ADMIN` or `STUDY_IMPORTER` can generate a token. Claims include the current user ID as JWT ID, username as subject, issuer `YourHealthResearch`, audience `You`, not-before, issued-at, and expiration.

Generation stores one current per-user signing record by application expectation. Its ID is the token's `kid`. Each generation creates a new random HMAC key using `HS512`, updates the stored key and creation time, and immediately invalidates earlier tokens for that user.

Validation resolves the key from `kid`, verifies signature, requires issuer `YourHealthResearch`, and applies expiration, not-before, and parser time validation with 180 seconds of clock skew. Audience `You` is generated but not explicitly required by the parser. The subject selects the application user, and current roles populate the security context.

Automated upload authorization still depends on current roles: URL security requires `STAFF`, and the method requires `STUDY_IMPORTER` or `ADMIN`. The JWT filter is global rather than upload-specific and skips bearer processing when the request is already authenticated.

Regeneration rotates the key. The authenticated user can delete only a record matching their user ID and supplied record ID. Administrator removal of `STUDY_IMPORTER` deletes that user's signing information. Role removal also prevents upload authorization. Tokens are reusable until expiration or invalidation; no nonce, one-use marker, or use counter exists.

Generation audit records user ID and time. JWT login writes ordinary successful login audit evidence and updates login time. Completed upload audit records the authenticated user. No record links an upload to `kid`, claim ID, generation audit, token fingerprint, or specific reuse.

CSV-upload JWTs are distinct from study-importer invitation tokens. Invitation tokens are stored in `USER_SECURITY_TOKEN`, grant the importer role when redeemed, and use a separately seeded 24-hour lifetime.

Deployment-specific or policy-controlled items remain the effective lifetime, signing-key protection at rest, rotation cadence, acceptability of the installation default, perimeter restrictions, rate limits, log redaction, monitoring, retention, and operational ownership.

______________________________________________________________________

# Phase 7: PI Reconciliation Edge Cases

## PI-001: Separate ordinary membership

**Application behavior resolved for Java CSV reconciliation.**

`STUDY_TEAM_MEMBER` has a unique `(STUDY_ID, USER_ID)` constraint, so a user cannot retain a separate
ordinary and PI membership for the same study.

When the incoming PI already has an ordinary membership, reconciliation deletes that row, removes it
from the study's in-memory membership collection, and flushes. It then reassigns the former PI
membership row to the incoming PI. The incoming PI ends with one `PRINCIPAL_INVESTIGATOR` row, not two
memberships.

The former PI is not downgraded or retained as an ordinary member. The reused former-PI row now points
to the incoming PI.

## PI-002: Atomic replacement

**Application behavior resolved with cross-store limits.**

The following relational operations and their synchronization logs run inside the current CSV import
batch transaction:

1. Create the incoming PI `APP_USER` and `STAFF` role if absent.
1. Delete any existing incoming-PI membership and write a deletion log.
1. Flush that deletion.
1. Reassign the former PI membership row and write an update log.
1. Flush the replacement.
1. Update the `piUserId` property and write its update log.
1. Update changed PI identity values and write an identity-update log.

These operations are not a separate PI-only transaction; as many as 500 processed rows may share the
batch. A batch rollback normally rolls back the relational replacement and logs together.

The active-study refresh occurs after relational mutations but before batch commit. It is
process-local and cannot be rolled back by the database transaction. A PI-only change refreshes the
local active-study entry but does not directly invoke matching.

Notification-recipient behavior is handled separately under `PI-004`.

## PI-003: Reconciliation failure

**Application behavior resolved with the existing caught-persistence concern.**

Explicit flushes enforce delete-before-reassign ordering and can surface membership conflicts before
later steps. If an unexpected runtime exception escapes, processing stops and cleanup attempts to
roll back the current uncommitted batch. If final flush or commit fails, the current batch is rolled
back when still active and the tracked batch rows are marked failed.

A later valid import can retry the authoritative PI state. There is no separate automatic PI-repair
job.

If a `PersistenceException` is caught during the row, the importer records the row error and
continues in the same batch transaction without explicitly rolling back, clearing, or restarting it.
Source inspection therefore does not guarantee clean row-level rollback after a partially staged PI
replacement; the provider may instead mark the full transaction rollback-only.

A process-local active-study refresh already performed before rollback is not transactionally
restored. Operators must compare operational memberships, `piUserId`, reconciliation logs, import
errors, and the affected process's local study before preparing a corrective row.

## PI-004: Notification migration — resolved as current implementation

The existing PI membership row is reassigned to the new PI. Notification
recipient joins attached to that membership ID therefore resolve to the new
PI. If the incoming PI also has a duplicate ordinary membership, that row is
deleted and its notification joins cascade-delete rather than being merged.

External recipient strings are unchanged. The reviewed reconciliation path
does not generate a separate PI-change announcement.

This is an implementation finding, not a policy decision that every deployment
must preserve this migration model.

## PI-005: Historical PI evidence — resolved as current implementation

`IMPORTED_STUDY_SYNC_LOG` records the former and new application user IDs for
the PI membership update and `piUserId` property update, plus related
duplicate-membership deletion and account changes.

It is technical reconciliation history, not a complete immutable person
history: it lacks a source-upload foreign key, durable person identifier,
username-alias chain, and notification-delivery proof.

## PI-006: Username changes — resolved as current implementation

`USER_NAME` is the imported identity key. Reconciliation looks up the
normalized username, updates names and email but not username, and creates a
new staff `APP_USER` when the new username does not match an existing account.
It reassigns the current PI membership but does not automatically transfer or
consolidate the former account's other memberships, agreements, login history,
or account-specific evidence.

Authorized manual intervention and institutional identity evidence are needed
when two usernames must be treated as one person.

______________________________________________________________________

# Phase 8: Loved-One Age-Out

## AGEOUT-001: Deployed warning interval — application behavior resolved

The setting keys are:

- `DAYS_BEFORE_MATURE_TO_NOTIFY`
- `YEARS_TO_BE_CONSIDERED_MATURE`

Installation seed values are 14 days and 18 years. No institution-specific seed override for either key
exists in the reviewed source.

The warning comparison is open at both endpoints. With value 14, a child is eligible 1 through 13
calendar days before the configured maturity date, not exactly 14 days ahead. The installation cron is
daily at 5:10 a.m. in the scheduler or Java virtual machine effective default time zone.

Application behavior is resolved. Still deployment-specific:

- Current persisted setting values
- Current persisted cron expression
- Effective time zone
- Number of application schedulers
- External duplicate-execution controls
- Monitoring proving that a run occurred during the warning window

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

## AGEOUT-005: Adult self-registration and historical data — application behavior resolved

Age-out disables the loved-one account but does not delete it, remove its `LOVED_ONE` relationship, or
change its generated username. Existing profile, agreement, study, questionnaire, message, and other
history remains associated with that original user ID.

Public self-registration is a separate create-only workflow:

- The entered email becomes the new self account's username.
- The unique `APP_USER.USER_NAME` constraint rejects an existing username.
- Email is not unique.
- Registration does not match by old user ID, generated username, owner email, name, date of birth, or
  relationship.
- Registration does not claim, merge, transfer, or migrate the aged-out account or its history.
- New agreement acceptance is stored under the new username.

The new self account and disabled loved-one account are isolated identities. Historical consolidation
or transfer requires an authorized support, privacy, and records-handling procedure not implemented by
the reviewed application.

## AGEOUT-006: Age-out failure operations — application behavior resolved with known concerns

The warning and deactivation passes execute in one required job transaction, warning first. There is no
per-child catch, savepoint, retry, or durable run ledger.

An uncaught runtime, data, date-parsing, template, or email exception stops later work and ordinarily
rolls back relational writes. It cannot compensate:

- Email already handed off
- Process-local active-user removal
- Asynchronous Redis cleanup already submitted or completed

Known failure windows:

- Warning email precedes saving `CHILD_DEACTIVATION_NOTICE`, allowing delivery without committed
  deduplication evidence and possible repeat warning.
- Deactivation removes local memory and starts asynchronous cleanup before the final age-out email. A
  later email failure can roll back database disablement and `USER_DEACTIVATION` while external state
  has escaped.
- Asynchronous cleanup failures create `APPLICATION_ERROR`, may notify, are consumed by the future
  handler, and are not automatically retried.
- Cooperative interruption leaves completed work in place and unvisited children for a later run.
- Scheduler infrastructure errors have durable handling, but a durable `APPLICATION_ERROR` is not
  confirmed for every business exception escaping `runJob()`.

Recovery requires diagnosis across relational state, local memory, Redis, application errors, logs, and
email evidence, followed by a corrected rerun and targeted memory or recommendation repair. Deployment
monitoring, alerting, log retention, ownership, and external delivery evidence remain
deployment-specific.

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

## SCHEMA-001: Interested participants — application behavior resolved

`STUDY_VOLUNTEER` is the durable expression-of-interest and workflow relationship.

Confirmed physical and application behavior:

- Sequence primary key `ID`
- Foreign keys from `USER_ID` to `APP_USER` and `STUDY_ID` to `STUDY`
- Unique `(USER_ID, STUDY_ID)`, enforcing one interest relationship per pair
- Interest timestamp, current workflow status, and status-update timestamp
- Fixed status values `NEW`, `ELIGIBLE`, `PENDING`, and `INELIGIBLE`
- `ALL` is an aggregate query, not stored state
- Active-profile list, statistics, and export queries hide deactivated participants without deleting
  the row
- Labels use `VOLUNTEER_LABEL` and composite-key `STUDY_VOLUNTEER_LABEL`
- Participant list and profile reads create PHI audit events
- Hard deletion deletes messages first, then label joins and `STUDY_VOLUNTEER`

Show interest is a required relational transaction, but process-local memory, Redis exclusions, and
email are not one atomic resource transaction. The duplicate-submit handler catches a data-integrity
exception, continues to undismiss, and can report success; this is a known implementation concern.

Known authorization concern: the interested-participant PATCH URL requires a staff or administrator
role and CSRF protection but does not call study-membership or publishability authorization. This is
not intended permission.

No separate enrollment state, withdrawal state, status history, transition actor, transition reason,
or retention period is stored.

## SCHEMA-002: Questionnaires — application behavior resolved

Confirmed physical schema:

- `STUDY_SCREEN_QNAIRE`: questionnaire header, study reference, and concurrency `VERSION`
- `STUDY_SCREENING_QUESTION`: ordered question, required/editable flags, text, help text, and input
  type
- `STUDY_SCR_QUES_OPTION`: ordered response choices
- `VOL_SCR_QUESTION_ANSWER`: user, study, question, answer date, and free-text answer
- `VOL_QSTN_ANSWR_SLCTD_OPTNS`: composite-key answer-to-option selections

Definitions cascade from study to questionnaire, question, and option. Question deletion explicitly
deletes answer rows. Option deletion cascades selected-option joins and can leave the parent answer row
without a selection. User deletion cascades answers.

`VERSION` and `If-Match` provide concurrency control but no historical questionnaire version.
Question and option text are mutable in place; answers do not retain submission-time text snapshots.
Current display and export use current definitions, so deleted or changed definitions limit historical
reconstruction.

Profile-backed fixed questions update ordinary profile-property tables. User-defined study questions
write the answer tables.

Known authorization concern: staff URL security applies, but question POST and PUT do not call
study-level membership authorization. DELETE, reorder PATCH, answer-count, and questionnaire GET do.
This is a backend authorization gap, not intended behavior.

Definition-change audit, answer history, external definition archives, and retention requirements
remain unestablished.

## SCHEMA-003: Messaging — application behavior resolved

`USER_MESSAGE` is the durable in-application message table. A conversation is derived from all
messages sharing one `STUDY_VOLUNTEER_ID`; no conversation table exists.

Confirmed schema and behavior:

- Message sequence primary key, sender, interested-participant relationship, body, sent timestamp, and
  `READ` or `UNREAD`
- Restrictive foreign keys to sender and `STUDY_VOLUNTEER`
- `MESSAGE_ATTACHMENT` composite-key join to reusable study-owned `ATTACHMENT`
- Study-specific `MESSAGE_TEMPLATE` with unique `(STUDY_ID, TYPE, NAME)`
- `MESSAGE_TEMPLATE_ATTACHMENT` composite-key join
- Conversation views derive shared study-team and participant inbox summaries
- Fetching a conversation marks messages addressed to the logged-in side as `READ`
- Read state is shared for the study team; no reader identity or read timestamp exists
- Message sending requires sender identity, interest, and staff study membership where applicable
- Message send does not independently enforce study publishability
- Single-message persistence and notification run in one Spring transaction, but external email or
  queue effects cannot be rolled back
- Bulk messages use one new transaction per participant
- Hard participant deletion removes messages before the interest relationship

Attachment metadata is relational while bytes are filesystem state. Creation writes the file before
the row; deletion removes the row and file in one service call, but database and filesystem are not
atomic. No automatic orphan reconciliation was found.

Current client validation allows any file type and limits size to 5 MB; the reviewed backend service
does not independently enforce those controls.

No separate message audit, message edit/delete history, per-reader receipt, retained template link, or
application-enforced retention period is established.

## SCHEMA-004: Labels

**Status:** Resolved for current application and code behavior.

**Current implementation:** `VOLUNTEER_LABEL` stores a study-specific name and style token. `STUDY_VOLUNTEER_LABEL` is the many-to-many assignment between a label and an interested-participant relationship, so one participant can hold multiple labels. Label deletion cascades assignment joins. The database does not enforce label-name or style uniqueness within a study.

Study members can create, edit, and delete definitions. Definition mutation checks study access and ownership. Assignment mutation checks that the label and interested-participant relationship belong to the same study. The interface supports create, edit, delete, bulk apply, bulk remove, and no change. Export emits one comma-joined label-name column.

**Known implementation concern:** The interested-participant PATCH endpoint has staff URL-role and cross-site request forgery controls and validates same-study objects, but does not independently require caller membership in that study or study publishability.

**Remaining policy decisions:** Naming rules, maximum count, duplicate-name policy, style governance, retention, and dedicated label audit requirements remain product or institutional decisions. No dedicated definition or assignment audit event was established.

See [Interested participant management](../06-recruitment/interested-participant-management.md), [Operational schema](../07-data-model/operational-schema.md), and [Recruitment operations model](../07-data-model/recruitment-operations-model.md).

## SCHEMA-005: Notifications

**Status:** Resolved for current application and code behavior.

**Current implementation:** `NOTIFICATION_SETTING_FREQ` defines event/frequency compatibility and display order. `STUDY_NOTIFICATION_SETTING` enforces one row per study and event and stores the shared frequency plus an external-recipient string. `STUDY_NOTIFICATION_RECIPIENT` joins selected study members to a setting. Current seed behavior permits immediate, daily, or weekly delivery for new interest and messages; daily or weekly delivery for new matches; and no selectable frequency for Other Announcements.

New studies receive every setting. Save/update validates event and frequency lookup types and selected-member ownership, runs transactionally, and invokes notification-update auditing. Dispatch combines member and external addresses into a set. Participant recommendation timing is separate participant preference state.

`EMAIL_LOG` records local attempt outcomes but not mailbox delivery. Successful queue submissions are not `EMAIL_LOG.SUCCESS`. Checked-in retention jobs move records older than 180 days to body-free backup and remove backup records after 1,461 days; separate recommendation audit files expire after 31 days when enabled. These definitions do not prove effective deployment execution.

**Known implementation concerns:** The interface treats external recipients as one address while the transfer-object contract permits comma- or space-separated addresses; application validation was not established. Configuration, queue, attempt, transport, and mailbox-delivery states must remain distinct.

**Remaining deployment and policy decisions:** Effective email profile, provider and queue topology, schedules, time zone, monitoring, runbooks, recipient policy, external-address validation, and executed retention remain deployment or institutional concerns.

See [Study notifications](../05-study-management/study-notifications.md), [Operational schema](../07-data-model/operational-schema.md), and [Recruitment operations model](../07-data-model/recruitment-operations-model.md).

## SCHEMA-006: Promotion and deactivation

**Status:** Resolved for current application and code behavior.

**Current implementation — promotion:** `RECOMMENDED_STUDY_MESSAGE` stores participant, study, recommending user, reason, and a message of at most 512 characters. It has no promotion timestamp, active marker, participant-study-reason uniqueness, Redis score, or durable email-attempt link. Ask if interested writes relational context plus Redis state: participant-side `USER` score is the promotion time, and study-side `ASKED_IF_INTERESTED` prevents repetition. The interface limits notes to 275 characters, shows promoted studies separately from system matches, and does not create expression of interest, direct messaging, or enrollment. Participant Not Interested or Enrolled actions remove relational promotion rows for the pair.

**Current implementation — user and child deactivation:** `USER_DEACTIVATION` permits one current row per retained user reference. User deletion nulls the reference and preserves history; reactivation deletes the row. Owner deactivation disables enabled loved-one accounts through service behavior. Durable recruitment records remain but active-profile paths hide them. Asynchronous Redis cleanup removes ordinary recommendations, not exclusions or `USER` promotions.

`CHILD_DEACTIVATION_NOTICE` records parent, child, date of birth, and sent date and deduplicates by that combination. A corrected date of birth can permit another notice. Warning email is handed off before the notice row is committed, so delivery can occur without committed deduplication evidence. Age-out later writes `CHILD_TURNED_ADULT`; warning and deactivation are separate operations.

**Current implementation — study deactivation:** Posting dates and `STUDY_ACTIVE_INTERVAL` change, participant discovery and matched-participant work stop, and management of existing interest continues. Ordinary Redis cleanup is asynchronous; exclusions and `USER` promotions remain. Notification follows through the daily batch, and archive is separate.

**Known implementation concerns:** Relational promotion rows cannot reconstruct current Redis state or original timestamps. Hard deletion can leave orphaned Redis state. Deployment-specific numeric reason IDs are not universal, including the current hard-coded `261001` interface check. No distinct age-out PHI audit event was established.

**Remaining policy and deployment decisions:** Promotion and deactivation retention, orphan reconciliation, Redis reconstruction, delivery proof, scheduler configuration and time zone, monitoring, recovery, and institutional reason visibility remain open operational or policy concerns.

See [Ask if interested](../06-recruitment/ask-if-interested.md), [Matching and visibility](../06-recruitment/matching-and-visibility.md), [Operational schema](../07-data-model/operational-schema.md), [Recruitment operations model](../07-data-model/recruitment-operations-model.md), and [Redis match model](../07-data-model/redis-match-model.md).

# Phase 11: Audit, Export, and Security Controls

## AUDIT-001: Export auditing

**Status: application behavior resolved; audit policy remains open.**

Interested-participant CSV is authorized through the interested-participant study-access check and is
streamed directly to the browser. The application retains neither an export-job entity nor a
server-side output file and creates no definitive export audit event.

List and profile PHI events, request logs, and timestamps provide only indirect investigative
correlation. They do not prove request completion, returned participant scope or fields, failure after
headers were committed, or handling of the downloaded file.

Whether to add a dedicated export event, and its actor, study, source address, scope or count, result,
and failure semantics, remains an institutional privacy, security, and product decision.

## AUDIT-002: CSV formula injection

**Status: implementation gap established; remediation policy remains open.**

Super CSV performs structural quoting but does not neutralize spreadsheet formulas. Questionnaire
answer values receive a trailing tab intended to reduce spreadsheet type or date conversion. That does
not neutralize a leading equals sign, plus sign, minus sign, or at sign.

Fixed profile and contact values, labels, questionnaire headers, current option text, and free-text
answers do not pass through one general formula-control policy. Current tests do not cover malicious
formula-leading headers or values.

Whether remediation is required and which neutralization contract to apply remain security and
product decisions. Any remediation must cover every exported header and cell and include tests for
each supported formula-leading character.

## AUDIT-003: Job auditing

**Status: application behavior resolved; audit policy and deployment controls remain open.**

Administrator schedule changes and manual execution require `ADMIN`. Schedule changes persist a new
cron expression and recreate the local Quartz job and trigger. Manual execution invokes Quartz with
supplied parameters.

The application writes log messages but no dedicated durable action record containing actor, target
job, parameters, prior and new schedule, request and completion times, outcome, counts, or process
identity. Quartz's previous fire time is not proof of business success. Scheduler infrastructure
errors and selected application errors are failure evidence, not a complete execution ledger.

Whether control-action and job-run events are required remains an institutional security and
operations decision. Effective schedules, time zone, server topology, external concurrency controls,
centralized logging, and retention remain deployment-specific.

## AUDIT-004: Invitation auditing

**Status: application behavior resolved; historical-audit and retention policy remain open.**

A live invitation row temporarily retains inviter, recipient metadata, creation, expiration, type,
and applicable study. Resending reuses the token and replaces expiration without retaining resend
history. Revocation, successful acceptance, and expiration cleanup delete the live row.

No dedicated historical event was established for invitation creation, resend, revocation,
acceptance, or expiration. Email evidence is partial and does not form a complete lifecycle ledger.
Because invitation links are transferable, accepting identity may differ from intended recipient.

Whether to retain historical security events, their fields, access controls, and retention remains an
institutional security, privacy, and product decision. A future audit must not retain raw invitation
tokens.

## AUDIT-005: Membership auditing

**Status: Java application behavior resolved; unified audit and override policy remain open.**

Ordinary membership creation and deletion change current `STUDY_TEAM_MEMBER` state without a dedicated
history identifying actor, source, reason, prior and resulting role, notification effects, times, and
outcome.

Java CSV PI replacement writes selected `IMPORTED_STUDY_SYNC_LOG` evidence for membership
reassignment, `piUserId`, duplicate-membership deletion, and identity changes. It lacks an immutable
person identifier and direct upload, source-row, request, batch, or token correlation and does not
prove complete cross-store success. U-M Oracle reconciliation is separate and requires database or
deployment evidence.

Whether ordinary changes, PI replacement, and authorized backend interventions require one durable
audit model remains an institutional security and operations decision.

## AUDIT-006: Attachment security

**Status: application behavior and gaps resolved; deployment and policy controls remain open.**

The application stores relational metadata and filesystem bytes separately. Study or attachment
authorization protects reviewed operations, but no creator-only deletion rule is established.

The current attachment service does not independently enforce the client 5 MiB limit and does not
establish extension allowlisting, content-type validation, extension-content agreement, malware
scanning, quarantine, archive inspection, or active-content controls. Download MIME detection is not
upload validation.

Filesystem and database operations are non-atomic. Creation can leave bytes without metadata;
deletion can remove metadata while file deletion fails and leaves an orphan. No automatic
reconciliation, retry, recycle bin, tombstone, restore path, or dedicated lifecycle audit was found.

Encryption, filesystem permissions, backup controls, external scanning, retention, secure disposal,
authoritative content rules, deletion guarantees, orphan handling, audit requirements, and
creator-versus-study-member deletion policy remain deployment, security, privacy, and institutional
decisions.

## AUDIT-007: Backend overrides

**Status: reviewed application behavior resolved; approval and unified audit policy remain open.**

No single backend-override mechanism exists. Privileged changes occur through imported reconciliation,
administrator and Customer Support interfaces, ordinary authorized study workflows, settings and job
administration, scheduled automation, and direct backend or database intervention.

The reviewed application establishes no common approval process, dual authorization, ticket
requirement, reason field, or durable override ledger spanning membership, publishability, activation
dates, participant state, job schedules, and related settings.

Publishability is normally institutionally governed; no general administrator interface for direct
editing was established. Participant deactivation retains target, time, and reason, but reactivation
deletes current deactivation evidence and service records do not identify the administrator actor for
every path. Job controls lack durable action history. Direct backend and database changes remain
outside ordinary application evidence.

Approval, actor and approver identity, source channel, prior and resulting values, reason or ticket,
outcome, correction linkage, sensitive-value handling, and retention remain institutional security
and operations decisions.

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
