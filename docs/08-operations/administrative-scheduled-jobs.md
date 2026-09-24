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

At application startup, all dynamic jobs are deleted from the local scheduler
and recreated from persisted schedules.

Cron validation uses the Quartz parser. The backend does not impose an
additional minimum or maximum frequency beyond Quartz validity.

Execution times use the application server's effective default time zone
unless the deployment configures Quartz otherwise.

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
application log messages. No dedicated durable application-job action-audit
table is confirmed.

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
