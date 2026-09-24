---
title: Source Repository Routing
summary: Maintenance reference for locating current implementation evidence without coupling canonical domain documentation to source layout.
status: authoritative
content_scope:
  - maintenance_reference
  - current_implementation_routing
implementation_dependency: high
last_verified: "2026-09-24"
canonical_for:
  - source_repository_routing
relevant_when:
  - validating_documented_behavior_against_source
  - locating_implementation_ownership
  - investigating_cross_application_behavior
---

# Source Repository Routing

This page routes implementation investigations to current source repositories.

It is a maintenance reference, not a business-rule definition. Canonical functional pages should
describe domain rules and expected behavior without depending on repository names, class names, or
source paths. Use this page only when implementation evidence is required.

## Current repositories

| Application area                      | Repository       | Current technology               | Primary implementation responsibilities                                                                                                                                  |
| ------------------------------------- | ---------------- | -------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Participant and loved-one frontend    | `yhr-volunteer`  | Backbone                         | Registration, participant agreements, account-context switching, participant profiles, study discovery, participant-facing matching, interest, and participant messaging |
| Study-team and administrator frontend | `yhr-study-team` | React                            | Study-team workflows, current administrator functions, Customer Support, participant reactivation, job administration, posting authoring, and recruitment operations     |
| Backend and database migrations       | `yhr-backend`    | Spring/Java and Liquibase        | Authorization, persistence, scheduled jobs, email dispatch, matching orchestration, process-local active stores, Redis integration, and database mappings                |
| Application routing                   | `yhr-routing`    | Deployment routing configuration | Routing between application clients and backend services where applicable                                                                                                |

## Obsolete repository

`umhr-admin` is abandoned, obsolete, and deprecated.

Do not use it as evidence of current administrator behavior. Current administrator functionality is
implemented in `yhr-study-team`.

Historical comments and README files may use older names such as `umhr`, `umhr-study-team`, or
`umhr-volunteer`. Determine current ownership from the repository containing the active implementation,
not from a historical repository label alone.

## Investigation guidance

Use the narrowest repository that owns the behavior:

- Participant-page display or interaction: begin with `yhr-volunteer`.
- Study-team or administrator display or interaction: begin with `yhr-study-team`.
- Authorization, persistence, job execution, email generation, memory, or Redis effects: inspect
  `yhr-backend`.
- Browser routing or deployment path ownership: inspect `yhr-routing`.

Cross-cutting behavior ordinarily requires the applicable frontend plus `yhr-backend`.

Examples:

- Agreement decline scope requires `yhr-volunteer` for the submitted account context and
  `yhr-backend` for cascade behavior.
- Administrator reactivation requires `yhr-study-team` for account selection and confirmation plus
  `yhr-backend` for reactivation scope and matching effects.
- Study activation requires `yhr-study-team` for the interaction and `yhr-backend` for persisted
  dates, active-view membership, memory synchronization, and Redis effects.

## Documentation boundaries

Do not move implementation details into business documentation merely because they were used as
evidence.

Prefer this pattern:

1. State the domain or business rule on the canonical functional page.
1. State technically important architecture or storage behavior on the applicable technical page.
1. Record unresolved policy or implementation conflicts in the decision register.
1. Use this routing page to locate source evidence.
1. Add source paths or class names only when they materially help developers investigate or modify the
   behavior.

Repository ownership can change without changing the business rule. When that happens, update this
page and routing links rather than rewriting unrelated domain pages.

## Evidence quality

Repository location identifies where to investigate; it does not by itself prove behavior.

Authoritative implementation findings should be supported by one or more of:

- Executed production path
- Automated test
- Persistence mapping or database definition
- Configuration or seed data
- Verified deployment behavior
- Recorded product, policy, privacy, legal, or security decision

Generated fixtures, mocks, obsolete repositories, and comments may guide investigation but should not
be treated as sufficient evidence by themselves.

## Related pages

- [Architecture Overview](index.md)
- [System Context](system-context.md)
- [Business Rules](../01-overview/business-rules.md)
- [Open Questions](../09-decisions/open-questions.md)
