---
title: Audit and Monitoring
summary: Confirmed PHI auditing and recommended operational monitoring.
status: mixed
---

# Audit and Monitoring

This page separates confirmed audit behavior from recommended monitoring.

## Confirmed participant-data audit

Participant-data access is audited through `PHI_AUDIT`.

See [PHI Audit](phi-audit.md).

Confirmed audited activities include:

- Administrator participant search results
- Interested-participant list views
- Matched-participant list views
- Interested-participant profile views
- Matched-participant profile views
- Administrator password resets
- Administrator participant deactivation

## Confirmed non-audited actions

Dedicated audit events are not created for:

- Interested-participant workflow-list movement
- Label changes
- Invitation lifecycle
- CSV export generation
- Message lifecycle

Messages retain sender, recipient, and timestamp as business data.

## Recommended operational events

Potential future audit or monitoring includes:

- Participant registration
- Consent acceptance
- Participant visibility changes
- Import receipt and validation
- Reconciliation runs
- Publishability changes
- PI membership changes
- Study activation and deactivation
- Study archiving
- Invitation creation and acceptance
- Label changes
- Workflow-list movement
- Export generation
- Redis recomputation failures

## Recommended reconciliation metrics

Monitor:

- Last successful import
- Last successful reconciliation
- Record counts
- Rejected records
- Publishability changes
- Active-status changes
- PI changes
- Job duration
- Failure reasons

## Export investigation

Because exports are streamed and not separately audited, investigation may correlate:

- Interested-participant list views
- Participant profile views
- Application request logs
- Request timestamps

This is indirect evidence and not a definitive export event.

## Matching and memory observability

### Store population and refresh

At startup and during a full store refresh, each process-local store writes
informational logs for:

- Load start
- Number of database objects returned
- Database-load duration
- Total store-load duration

The store exposes its current process-local size through its Java interface, but
the reviewed administrator and operations controllers do not expose a store-size
or database-versus-memory comparison endpoint.

An uncaught `@PostConstruct` load failure is exposed through Spring
application-context startup failure and its logs. The reviewed application and
routing source do not provide a dedicated health or readiness endpoint tied to
successful completion of all store loads.

### Scheduled membership synchronization

Active-user and active-study synchronization writes debug messages when
synchronization starts and returns, plus debug messages for individual
additions. The job wrapper writes an informational success message after the
synchronizer returns.

The synchronization path does not persist or expose:

- Start, completion, or last-success timestamps
- Duration
- Database, memory, added, removed, skipped, or failed counts
- An explicit complete-versus-interrupted result
- Server or process identity
- A database-versus-memory comparison

Interruption is cooperative and is checked while visiting candidate additions
and removals. Returning after interruption still reaches the wrapper's
“successfully” log message, so that message confirms that the method returned
without an uncaught exception; it does not prove that every candidate was
visited or that reconciliation completed.

### Matching and recomputation

The application provides a transient process-local Boolean indicating whether
matching is finished for one participant or study. Internally, task identifiers,
thread identifiers, and outstanding task counts are held in concurrent maps.
They are not durable, cluster-wide, or a history of completion.

Matching chunks write debug duration messages. Entity-level matching and full
recomputation write informational completion messages. Full recomputation
continues to later studies after a study-specific failure and can also return
early when interrupted.

Matching and scheduler exceptions are persisted in `APPLICATION_ERROR` with a
time, exception type, message or stack trace, and limited request context when
available. Error notifications depend on application configuration. Successful
matching, synchronization, and full recomputation do not create corresponding
durable success records.

The administrator jobs API exposes local scheduler data:

- Previous trigger fire time, when available
- Next execution times
- Trigger state
- Currently running instance count

The previous trigger fire time is not a durable business-success timestamp and
does not establish complete synchronization or successful Redis writes.

### Redis and consistency

Redis sorted-set scores retain recommendation, promotion, and exclusion
timestamps. The recommendation data-access layer supports entity-specific
retrieval and selected per-study recommendation counts. These values support
application behavior and troubleshooting, but the reviewed application does not
provide a global Redis key inventory or expected-versus-actual consistency
comparison.

No application implementation was found for:

- Database-active-view versus process-local store comparison
- Database-to-memory-to-Redis consistency checking
- Expected versus actual Redis recommendation or exclusion key counts
- Cross-server in-memory divergence detection
- Last successful full-recomputation tracking
- Failed-entity thresholds
- A dedicated health, readiness, liveness, metrics, or Prometheus endpoint for
  matching and store freshness

### Deployment observability

The checked-in production logging configuration sets application logging to
`WARN`; the synchronization and success messages described above are emitted at
`INFO` or `DEBUG`. A deployment must override or supplement that configuration
for those messages to be retained.

Whether production infrastructure provides centralized logs, dashboards,
alerts, health probes, traffic gates, retention, server attribution, or
freshness thresholds remains deployment-specific and must be verified for each
instance.

## Related pages

- [PHI Audit](phi-audit.md)
- [Interested-Participant Management](../06-recruitment/interested-participant-management.md)
- [Questionnaires and Exports](../06-recruitment/questionnaires-and-exports.md)
- [Open Questions](../09-decisions/open-questions.md)
