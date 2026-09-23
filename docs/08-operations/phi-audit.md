---
title: PHI Audit
summary: Participant-data view auditing and known PHI_AUDIT event types.
status: authoritative
canonical_for:
  - phi_audit
  - participant_profile_audit
  - participant_list_view_audit
relevant_when:
  - auditing_participant_access
  - investigating_profile_views
  - interpreting_phi_audit
---

# PHI Audit

Participant-data access is audited through:

```text
PHI_AUDIT
```

## Confirmed event types

```text
ADMIN_VOLUNTEER_SEARCH_RESULT
INTERESTED_PARTICIPANTS_LIST_VIEW
RECOMMENDED_PARTICIPANTS_LIST_VIEW
RECOMMENDED_PARTICIPANT_PROFILE_VIEW
ADMIN_RESET_PASSWORD
ADMIN_DEACTIVATE_USER
INTERESTED_PARTICIPANT_PROFILE_VIEW
```

The legacy term:

```text
RECOMMENDED
```

means matched.

## List-view events

A list-view audit record may identify multiple participant IDs in one viewed-target value.

For example, opening a page containing several matched or interested participant snippets may create
one event identifying the participant IDs visible on that page.

## Profile-view events

Opening one participant profile creates the applicable profile-view event.

The event distinguishes:

- Matched participant profile access
- Interested participant profile access
- Administrator actions where applicable

## Actions not separately audited

The following actions are not separately recorded as dedicated audit events:

- Moving an interested participant between workflow lists
- Creating, renaming, applying, or deleting labels
- Export generation
- Message lifecycle actions

Messages retain sender, recipient, and timestamp as business data.

Export investigations may correlate list/profile-view events with application request logs, but that
does not create a definitive export audit event.

## Related pages

- [Interested-Participant Management](../06-recruitment/interested-participant-management.md)
- [Messaging](../06-recruitment/messaging.md)
- [Audit and Monitoring](audit-and-monitoring.md)
- [Questionnaires and Exports](../06-recruitment/questionnaires-and-exports.md)
