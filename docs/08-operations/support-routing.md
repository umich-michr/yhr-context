---
title: Support Routing
summary: Minimal-page routing for common participant, study-team, matching, messaging, lifecycle, and account questions.
status: authoritative
---

# Support Routing

Use this page to load only the documentation needed for a support question.

| Question                                     | Primary page                                                                                          | Also check                                                                                  |
| -------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------- |
| What does the application do?                | [Application Overview](../01-overview/index.md)                                                       | [System Context](../02-architecture/system-context.md)                                      |
| Why did signup or activation fail?           | [Participant Registration](../04-users-and-access/participant-registration-consent-and-loved-ones.md) | [Participants](../04-users-and-access/participants.md)                                      |
| How does a loved-one account work?           | [Participant Registration](../04-users-and-access/participant-registration-consent-and-loved-ones.md) | [Participant Account Model](../07-data-model/participant-account-consent-model.md)          |
| Why can’t I create a posting?                | [Posting Creation](../05-study-management/posting-creation.md)                                        | [Imported Institutional Data](../03-institutional-governance/imported-data.md)              |
| What information appears in a posting?       | [Study Information Authoring](../05-study-management/study-information-authoring.md)                  | [Public Study Discovery](../06-recruitment/public-study-discovery.md)                       |
| Why is a study not active?                   | [Study Lifecycle](../05-study-management/study-lifecycle.md)                                          | [Publishability](../03-institutional-governance/publishability.md)                          |
| Why did a study reactivate automatically?    | [Study Lifecycle](../05-study-management/study-lifecycle.md)                                          | [Publishability](../03-institutional-governance/publishability.md)                          |
| Why can’t a study be archived?               | [Study Archiving](../05-study-management/study-archiving.md)                                          | [Study Lifecycle](../05-study-management/study-lifecycle.md)                                |
| Why is the PI missing?                       | [Governance Reconciliation](../03-institutional-governance/reconciliation.md)                         | [Institutional Users](../04-users-and-access/institutional-users.md)                        |
| Why can’t a team member access a study?      | [Study Membership](../04-users-and-access/study-membership.md)                                        | [Study-Team Invitations](../04-users-and-access/invitations.md)                             |
| Why can’t I find a public study?             | [Public Study Discovery](../06-recruitment/public-study-discovery.md)                                 | [Study Lifecycle](../05-study-management/study-lifecycle.md)                                |
| Why can’t a participant see a matched study? | [Matching and Visibility](../06-recruitment/matching-and-visibility.md)                               | [Redis Match Model](../07-data-model/redis-match-model.md)                                  |
| Why can’t the study team see a participant?  | [Matching and Visibility](../06-recruitment/matching-and-visibility.md)                               | [Study Membership](../04-users-and-access/study-membership.md)                              |
| What does Ask if interested do?              | [Ask if Interested](../06-recruitment/ask-if-interested.md)                                           | [Matching and Visibility](../06-recruitment/matching-and-visibility.md)                     |
| Why did show interest fail?                  | [Expressions of Interest](../06-recruitment/expressions-of-interest.md)                               | [Questionnaires and Exports](../06-recruitment/questionnaires-and-exports.md)               |
| Why can’t a participant send a message?      | [Messaging](../06-recruitment/messaging.md)                                                           | [Interested-Participant Management](../06-recruitment/interested-participant-management.md) |
| Why is a conversation hidden?                | [Messaging](../06-recruitment/messaging.md)                                                           | [Study Lifecycle](../05-study-management/study-lifecycle.md)                                |
| Why can’t a questionnaire be edited?         | [Questionnaires and Exports](../06-recruitment/questionnaires-and-exports.md)                         | [Study Lifecycle](../05-study-management/study-lifecycle.md)                                |
| Why was a participant moved or labeled?      | [Interested-Participant Management](../06-recruitment/interested-participant-management.md)           | [PHI Audit](phi-audit.md)                                                                   |
| Why was an email notification not sent?      | [Study Notifications](../05-study-management/study-notifications.md)                                  | [Study Membership](../04-users-and-access/study-membership.md)                              |
| Why is an export unavailable?                | [Questionnaires and Exports](../06-recruitment/questionnaires-and-exports.md)                         | [Publishability](../03-institutional-governance/publishability.md)                          |
| Who viewed participant data?                 | [PHI Audit](phi-audit.md)                                                                             | [Audit and Monitoring](audit-and-monitoring.md)                                             |
| Which database entities are involved?        | [Data-Model Overview](../07-data-model/index.md)                                                      | [Relationship Model](../07-data-model/relationship-model.md)                                |

## Investigation order

1. Identify the institutional deployment.
1. Identify the actor and current account context.
1. Confirm authentication.
1. Confirm participant or institutional account status.
1. Confirm imported study existence and publishability.
1. Confirm operational study dates, active state, and archive state.
1. Confirm study membership.
1. Confirm participant visibility and activity.
1. Confirm exact, partial, interest, and exclusion state.
1. Confirm interested-participant workflow state.
1. Confirm the requested operation:
   - Profile access
   - Messaging
   - Questionnaire editing
   - Notification delivery
   - Export
1. Review `PHI_AUDIT`, Redis, application logs, and email-delivery evidence as applicable.
