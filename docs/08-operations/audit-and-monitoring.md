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

## Related pages

- [PHI Audit](phi-audit.md)
- [Interested-Participant Management](../06-recruitment/interested-participant-management.md)
- [Questionnaires and Exports](../06-recruitment/questionnaires-and-exports.md)
- [Open Questions](../09-decisions/open-questions.md)
