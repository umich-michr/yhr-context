---
title: Administrative Scheduled Jobs
summary: Administrator-visible application jobs, Quartz schedules, execution controls, status, authorization, and the boundary with Oracle database jobs.
status: authoritative
canonical_for:
  - administrative_scheduled_jobs
  - quartz_job_controls
  - job_schedule_management
relevant_when:
  - administering_jobs
  - changing_job_schedules
  - running_jobs_manually
  - troubleshooting_scheduled_jobs
---

# Administrative Scheduled Jobs

The application has two distinct scheduled-job systems:

1. Application-managed Quartz jobs
1. Database-native Oracle Scheduler jobs

These systems have different discovery, authorization, scheduling, and
monitoring behavior.

## Application-managed Quartz jobs

The administrator jobs API discovers Spring beans implementing
`DynamicallyReschedulableJob`.

Seeded application-job names include:

- `securityTokenCleanupJob`
- `childAccountDeactivationJob`
- `activeStudiesSynchronizationJob`
- `activeUsersSynchronizationJob`
- `batchNotificationJob`
- `updateAllRecommendationsJob`
- `resendFailedEmailsJob`
- `lookupValuesSynchronizationJob`
- `updateActiveIntervalsJob`

A seeded schedule appears in the administrator API only when the deployed
application also contains a corresponding dynamic-job bean.

`updateActiveIntervalsJob` is present in the schedule seed with a 3:00 a.m. cron expression, but the
reviewed Java source contains no corresponding dynamic-job class or Spring bean. The seed row alone
does not execute interval updates and should be treated as stale or orphaned unless a deployment adds
the missing bean externally.

## Authorization

All administrator job-controller endpoints require the application-wide
`ADMIN` role.

No finer-grained job-control permission is implemented by this controller.

## Exposed actions

The administrator API supports:

- Listing all dynamic jobs
- Viewing one dynamic job
- Running a job immediately
- Adding or replacing a persisted cron expression
- Validating a proposed cron expression
- Previewing the next 12 execution times

The underlying scheduling service also contains pause, resume, clear, and
interrupt operations. Those operations are not exposed by the current
administrator job controller and must not be described as administrator UI
capabilities.

## Schedule representation

Application job schedules use Quartz cron expressions stored in:

```text
APPLICATION_JOB_SCHEDULE.CRON_EXPRESSION
```

Updating a schedule deletes the existing Quartz job, persists the new cron
expression, and creates a new Quartz job and trigger.

At application startup, all dynamic jobs are deleted from that application
process's local scheduler and recreated from persisted schedules. If multiple
application servers share the schedule rows, each server can create and run its
own equivalent triggers. The reviewed scheduler configuration uses the default
in-memory Quartz job store and does not enable Quartz clustering.

Cron validation uses the Quartz parser. The backend does not impose an
additional minimum or maximum frequency beyond Quartz validity.

No explicit time zone is assigned when the application constructs these
cron triggers. Quartz therefore uses the scheduler/JVM effective default time
zone unless deployment configuration overrides it. Previewed and most-recent
execution times are also converted through `ZoneId.systemDefault()`.

The source and seed data establish application behavior and installation
defaults only. A deployment's current persisted cron expressions, JVM or host
time zone, application-server count, and external duplicate-execution controls
must be verified from that environment.

## Job information

The administrator API reports:

- Name
- Group
- Description
- Cron expression
- Next 12 execution times
- Most recent trigger execution time, when available
- Trigger state
- Number of currently running instances

It does not report a confirmed persistent completion time, duration, processed
count, failure count, or last business-error message.

## Manual execution and concurrency

Administrators may trigger a dynamic job immediately and may supply supported parameters.

The confirmed recovery-related manual jobs are:

- `activeUsersSynchronizationJob` — reconciles active-user membership in the
  handling process's local store
- `activeStudiesSynchronizationJob` — reconciles active-study membership in the
  handling process's local store
- `updateAllRecommendationsJob` — recomputes ordinary recommendations from the
  handling process's current active stores

The synchronization jobs do not reload entities whose IDs already exist in
both the database active view and local store. They therefore cannot repair
stale fields for an entity that remains active. Full recommendation
recomputation does not reconstruct Redis-only exclusions or study-team `USER`
promotions after complete Redis loss.

`updateAllRecommendationsJob` has two confirmed process-local protections:

1. Before a manual trigger, `JobSchedulingService` asks Quartz for currently executing instances with
   the same job key and rejects the request when at least one is visible.
1. `MatchingServiceImpl.updateAllRecommendations(...)` is `synchronized`, serializing calls on that
   Spring service instance within one Java virtual machine.

The manual guard can reject:

- A second administrator-triggered run while an existing run is already visible to that scheduler
- A manual run while a scheduled run is already visible as executing

The protection is limited:

- The running-instance check and `triggerJob(...)` call are separate operations, not an atomic lock.
  Two nearly simultaneous requests could both observe zero running instances.
- The guard is special-cased only for `updateAllRecommendationsJob`.
- `DynamicallyReschedulableQuartzJob` is not annotated with Quartz
  `@DisallowConcurrentExecution`.
- The reviewed Quartz configuration enables interruption on shutdown but does not configure a JDBC
  job store or Quartz clustering.
- The scheduler therefore does not establish cluster-wide single execution across independent
  application servers.
- The `synchronized` method protects one service object in one process, not another server.

Other dynamic jobs can overlap unless their own implementation, deployment topology, or an
unreviewed external control prevents it. Scheduled/manual overlap and two-administrator overlap
should therefore be treated as possible outside the narrow protections above.

Matching task IDs provide a separate stale-work safeguard: an older asynchronous recommendation or
deactivation task checks whether it remains valid before changing Redis. That limits stale Redis
writes but is not a scheduler-level duplicate-execution lock.

## Interruption

Dynamic jobs implement an interrupt contract. Long-running jobs may inspect an
interrupt flag between units of work.

Interruption is cooperative:

- Work already completed remains completed.
- Unvisited items are left for a later run.
- Application shutdown is configured to interrupt running Quartz jobs.

The current administrator job controller does not expose an interrupt endpoint.

## Failure handling and audit

Scheduler errors are stored as application errors and generate error
notifications.

Job-control actions such as schedule changes and manual execution produce
application log messages. The reviewed application does not persist a dedicated
job-control action-audit record containing actor, action, target job, prior and
new schedule, request time, or outcome.

Scheduler and matching exceptions are durable application-error records, but
they are failure evidence rather than a complete audit of job-control actions.
The administrator job API likewise exposes scheduler state, not a durable action
history.

Production retention of logs, authenticated-actor attribution, centralized
collection, failure acknowledgement, and any external administrative audit
remain deployment-specific. See [Audit and Monitoring](audit-and-monitoring.md).

## Oracle Scheduler jobs

Oracle deployments may also define database-native jobs through
`DBMS_SCHEDULER`.

Examples include usage reports, study reports, audit/log backup, and U-M
eResearch synchronization.

Oracle jobs are not discovered by the application administrator jobs API.
Their time zones, enablement, logging, concurrency, and notifications are
managed by Oracle Scheduler and deployment-specific database configuration.

## Related pages

- [Matching and Visibility](../06-recruitment/matching-and-visibility.md)
- [Audit and Monitoring](audit-and-monitoring.md)
- [Troubleshooting](troubleshooting.md)
- [Study Lifecycle](../05-study-management/study-lifecycle.md)

## Batch notification lifecycle windows

`batchNotificationJob` performs lifecycle announcement and
upcoming-deactivation warning work using calendar-day windows in the
application or Java virtual machine system-default time zone.

For activation and deactivation announcements, it queries the previous calendar
day:

- Start: previous day at midnight
- End: one second before the current day at midnight

The active-interval query rules suppress superseded transitions. There is no
separate rolling 24-hour or configurable stabilization timer.

For upcoming-deactivation warnings, the job reads
`STUDY_ANNOUNCEMENTS_DAYS_AHEAD`. For every configured integer, it queries the
calendar day exactly that many days ahead. The installation seed is `2,14`.

Both lifecycle announcements and warnings resolve the current Other
Announcements recipients at dispatch time. The warning workflow stores no
delivery history or deduplication state. Repeated execution of the same window
can therefore repeat delivery, and changing a deactivation date can place the
study into a configured warning day again.

## Failed-email resend job

`resendFailedEmailsJob` is seeded to run hourly.

For each `EMAIL_LOG` row with status `FAILURE`, the job reconstructs an
`EmailMessage` and invokes the active raw `emailClient` directly.

After the call returns:

- For a Java Mail or other non-JMS client, the row is changed to `SUCCESS`.
- For `JmsEmailClient`, the old failure row is deleted after queue submission.

The job does not use `EmailSenderImpl`, so retries do not rerun the recipient
rewriter chain and do not create a second success row through that wrapper.

The reviewed implementation has no:

- Retry-attempt counter
- Maximum attempt limit
- Exponential backoff
- Next-attempt timestamp
- Last-error field
- Per-message exception isolation
- Idempotency key

An exception while processing one row can stop the current job run before later
rows are visited. Rows left in `FAILURE` remain eligible for a later run.

A transport may accept a message before a later database status update fails.
The unchanged `FAILURE` row can then be retried, so duplicate delivery is
possible. Multiple overlapping job executions can also process the same
failure row because the application has no general cluster-wide no-overlap
protection.
