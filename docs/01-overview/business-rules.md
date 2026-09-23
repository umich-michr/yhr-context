---
title: Business Rules
summary: Canonical cross-cutting application invariants.
status: authoritative
---

# Business Rules

This page contains confirmed cross-cutting rules.

For detailed workflows, use the canonical topic pages linked throughout the documentation rather
than treating this page as a complete user manual.

## Product and deployment identity

1. YourHealthResearch.org is the platform and product name.
1. `YourHealthResearch.org` is also the public marketing website for prospective adopting
   organizations.
1. Each adopting organization operates a separately branded instance of the platform.
1. Each instance has its own:
   - Application URL
   - Branding and configuration
   - Application servers
   - Database
   - Supporting IT infrastructure
   - Institutional identity and governance integrations
1. Examples include:
   - Michigan Institute for Clinical and Health Research at the University of Michigan:
     `UMHealthResearch.org`
   - Clinical and Translational Science Institute at the University of Miami:
     `UMiamiHealthResearch.org`
   - Institute for Translational Medicine: `BeTheNewNormalMatch.org`
   - University of Illinois Chicago: `healthresearch.ccts.uic.edu`
1. The Institute for Translational Medicine is a consortium involving Rush University, Northwestern
   University, Loyola University Chicago, and the University of Chicago, led by the University of
   Chicago.
1. Data from one branded instance does not authorize access to data in another instance.

## Identity and authorization

1. The application has four application-wide roles:
   - `ADMIN`
   - `STUDY_IMPORTER`
   - `STAFF`
   - `VOLUNTEER`
1. Study associations use:
   - `PRINCIPAL_INVESTIGATOR`
   - `STUDY_TEAM_MEMBER`
1. Application-wide roles and study-association roles are separate authorization domains.
1. Institutional users authenticate through SAML.
1. SAML authentication alone does not grant access to a study.
1. A `STAFF` user ordinarily requires a study association to access a study.
1. `PRINCIPAL_INVESTIGATOR` and `STUDY_TEAM_MEMBER` have equivalent study-data permissions.
1. `ADMIN` users may access all studies and participant data without ordinary study membership.
1. `STUDY_IMPORTER` grants institutional import capability but not study or participant-data access.
1. Participant accounts use the application-wide role `VOLUNTEER`.

## Participant accounts

1. Participants use local, database-backed accounts.
1. A self account ordinarily uses the participant's email address as its username and communication
   email address.
1. A loved-one account uses an application-generated GUID-based email-like username.
1. The loved-one account retains the owning account's real email address for communication.
1. The database prevents duplicate active usernames.
1. The application does not determine whether accounts using different usernames represent the same
   real-world person.
1. Participant registration requires acceptance of the applicable current agreement.
1. Agreement acceptance records:
   - Username
   - Agreement type
   - Agreement version
   - Timestamp
   - IP address
   - User agent
1. An activation email is sent after required registration and agreement processing succeeds.
1. Activation links contain expiring Java UUID tokens.
1. Participants choose profile visibility during signup.
1. The visibility choices are:
   - All study teams using the branded application instance
   - Only study teams whose studies the participant shows interest in
1. Participants may change visibility after registration.
1. Participants may deactivate their own accounts.
1. Deactivating an owning self account also deactivates its loved-one accounts.
1. Participants request reactivation through support.
1. Hard deletion requires an explicit support request and administrator confirmation.
1. Hard deletion removes participant data while retaining the internal participant ID and deletion
   reason.
1. Previously downloaded participant-data files cannot be recalled.

## Loved-one accounts

1. One participant login may manage multiple loved-one participant accounts.
1. Each loved one has a separate account and profile.
1. Loved-one ownership is represented through `LOVED_ONE`.
1. The owning account switches participant context without authenticating separately as the loved
   one.
1. Visibility, matching, interest, questionnaires, and messages belong to the represented
   participant account.
1. Agreement acceptance for a loved-one account is performed by the owning account.
1. A loved-one account may be created:
   - During initial registration using the signup-for-a-loved-one flow
   - Later through Add Loved One
1. The signup-for-a-loved-one flow creates:
   - A minimal owning account
   - A complete loved-one participant account
1. The minimal owning account collects:
   - Communication email, which is also its username
   - First name
   - Last name
1. Country and ZIP code entered for the loved one are copied to the owning account.
1. Required participant-profile fields not collected for the owning account remain incomplete.
1. The minimal owning profile defaults to hidden from study teams.
1. The loved one's visibility is selected during signup.
1. The loved-one account receives an application-generated GUID-based email-like username.
1. The owner's real email address is used as the communication email for both accounts.
1. Child-versus-adult relationship selection is validated against date of birth.
1. Child loved-one accounts are deactivated by a scheduled job at the configured maturity age.
1. The owning account is notified before the age-based deactivation.
1. Age-based deactivation removes the loved-one account from active in-memory matching data and
   prevents continued proxy access.
1. The represented participant cannot assume control of the existing loved-one account.

## Agreement-version enforcement

1. `USER_AGREEMENT` identifies the current version for each agreement type.
1. `USER_AGREEMENT_AUDIT` records versions accepted by individual users.
1. At login, the application checks whether the user has accepted the current version for the
   applicable agreement type.
1. If no matching audit record exists, the user must review the current agreement.
1. Agreement types include participant/volunteer and study-team agreements, represented by values
   such as:
   - `VOL`
   - `STM`
1. When a participant accepts the current agreement, a new `USER_AGREEMENT_AUDIT` record is created.
1. When a participant declines:
   - The participant is warned that the account will be deactivated.
   - The participant must confirm the decision.
   - On confirmation, the participant account is deactivated.
   - Deactivation of an owning self account cascades to its loved-one accounts.
1. When a study team member declines:
   - The user is denied access to application features.
   - The user is returned to or removed from the authenticated application workflow.
1. A user who has not accepted the current version cannot continue ordinary application use.

## Participant profile and system boundaries

1. Participant profile properties may be used for eligibility matching.
1. Participant study interests determine which exact-matching studies are recommended to the
   participant.
1. The required Where did you learn about us? value:
   - Uses institution-configured lookup values
   - Is not used in matching
   - Is not displayed to study teams
1. YourHealthResearch.org does not integrate with an electronic health record system.
1. The application does not retrieve participant profile or clinical data from an EHR.

## Institutional governance

1. Imported institutional data is stored in read-only `IMPORTED_*` tables.
1. Ordinary study team members cannot modify imported data.
1. Institutional imports are incremental.
1. Imported rows absent from a later import remain unchanged.
1. CSV import rows are processed independently and in file order.
1. If multiple rows modify the same study property, the last successfully processed row affecting
   that property determines its final value.
1. Intermediate rows may temporarily modify operational state before a later row overwrites the same
   value.
1. A valid imported study has one current institutional PI.
1. PI status is controlled by the institutional source of truth.
1. When the imported PI changes:
   - The new PI receives the operational `PRINCIPAL_INVESTIGATOR` membership.
   - The former PI's operational PI membership is removed.
1. Other imported institutional roles do not automatically grant study access.
1. Imported PI `USER_NAME` must correspond to the institutional SAML ePPN attribute.
1. `PUBLISHABLE` must be `0` or `1`.
1. A missing or invalid publishability value is an application error.

## Study-posting creation

1. A posting may be created only for a `study_num` found in `IMPORTED_STUDY`.
1. Only one operational posting may exist for one `study_num`.
1. Beginning Add Study creates a posting-attempt audit record; it does not by itself create the
   final operational study posting.
1. The operational study posting is created only after successful final submission of the Study
   Information and eligibility-authoring workflow.
1. On successful creation:
   - The non-PI creator receives `STUDY_TEAM_MEMBER`
   - The current imported PI receives `PRINCIPAL_INVESTIGATOR`
   - The PI is notified when applicable
1. A new posting begins inactive.
1. Study postings cannot be deleted through ordinary application UIs.

See:

- [Posting Creation](../05-study-management/posting-creation.md)
- [AI-Assisted Study Posting Authoring](../05-study-management/ai-assisted-posting-authoring.md)

## Study membership and invitations

1. Any associated study member may invite another SAML-authenticated institutional user.
1. Accepting an invitation creates a `STUDY_TEAM_MEMBER` membership.
1. Invitation links are expiring, single-use bearer links.
1. The invitation is not bound to the emailed recipient.
1. Membership creation and invitation-record deletion occur atomically.
1. Any associated study member may remove an ordinary `STUDY_TEAM_MEMBER`.
1. The current imported PI cannot be removed through ordinary application UIs.
1. A change in imported PI data removes the former PI's operational PI membership and associates the
   new current PI.

## Study active status

1. Study active status is derived; there is no independent persisted active Boolean.
1. A study is active only when:
   - `PUBLISHABLE = 1`
   - The current date/time falls within the inclusive activation and deactivation boundaries
1. Initial activation requires explicit study-team action.
1. A study cannot be activated or assigned new activation dates while `PUBLISHABLE = 0`.
1. Explicit activation:
   - Sets the activation boundary to the current date/time
   - Requires a future deactivation boundary
1. Manual deactivation:
   - Is immediate
   - Sets the deactivation boundary to the current date/time
   - Prompts for optional total enrollment
1. After manual deactivation, the derived state becomes inactive as the current time passes the
   saved deactivation boundary.
1. Total enrollment is stored through `STUDY_PROPERTY_VALUE`.
1. Date-based expiration makes the study inactive.
1. `PUBLISHABLE = 0` makes the study inactive without changing its dates.
1. `PUBLISHABLE: 0 → 1` automatically reactivates a study only when its unchanged activation range
   still contains the current date/time.
1. After the deactivation boundary has passed, publishability alone cannot reactivate the study.
1. Every derived active/inactive transition creates or closes a `STUDY_ACTIVE_INTERVAL`.
1. Lifecycle announcements are handled asynchronously rather than being sent synchronously in the
   status-changing request.
1. A PI receives a warning approximately one week before a scheduled deactivation date.
1. Stable active-status changes participate in delayed PI-notification handling.

See [Study Lifecycle](../05-study-management/study-lifecycle.md).

## Study archiving

1. Archive status is independent of active status.
1. Only an inactive study may be archived.
1. Archived studies are not publicly accessible.
1. Archived studies may be unarchived.
1. An archived study cannot be activated before being unarchived.
1. Archiving does not hide participant data, block otherwise permitted new exports, or hide existing
   messages.
1. `ARCHIVED_DATE` is stored through `STUDY_PROPERTY_VALUE`.

## Matching runtime and memory synchronization

1. Active studies and active participants are maintained in application memory to reduce matching
   latency.
1. Match calculations read eligible study and participant entities from memory rather than
   repeatedly loading every entity from the database.
1. The relational database remains the authoritative persistent source.
1. When a participant or study is updated:
   - The database record is updated.
   - The corresponding in-memory representation is updated.
1. Temporal participant-profile updates must also update the in-memory representation.
1. Deactivated participants and inactive studies must be removed from active in-memory matching
   collections.
1. Scheduled synchronization jobs reconcile memory with database state and handle time-based
   transitions.
1. Redis stores current directional recommendations and exclusions separately from the in-memory
   source entities.
1. Matching recomputation is asynchronous.

## Matching and visibility

1. Study-interest matching and eligibility matching are separate evaluations.
1. Eligibility expressions and aggregated eligibility results use:
   - `TRUE`
   - `MAYBE`
   - `FALSE`
1. `TRUE` means the available participant properties satisfy the applicable
   structured eligibility expression or aggregated criteria.
1. `MAYBE` means the known participant properties do not establish a mismatch,
   but the available information is insufficient to decide one or more
   applicable eligibility expressions.
1. A missing participant property ordinarily produces `MAYBE` when referenced
   by an eligibility expression.
1. Calculated properties may define property-specific missing-value behavior.
   Pregnancy at enrollment is calculated from due date, and a missing due date
   is currently treated as not pregnant.
1. A known value representing none is different from a missing value.
   `NO_CONDITION` is explicitly supplied information and is not equivalent to a
   missing or null condition property.
1. Missing values ordinarily produce `MAYBE` for negated operators as well as
   positive operators.
1. `FALSE` means the available participant properties establish that the
   applicable structured eligibility expression or aggregated criteria are not
   satisfied.
1. Expression results are aggregated using the documented three-valued `AND`,
   `OR`, and `NOT` rules.
1. Within a criteria group, current-UI structured expressions use `AND`.
1. Multiple criteria groups are alternatives and use `OR`.
1. If a study has no saved structured eligibility groups, structured
   eligibility evaluates to `TRUE`.
1. `OTHER` eligibility text is displayed to participants but is skipped by
   structured matching.
1. An `OTHER`-only current-UI group has no evaluated structured
   expressions. Its empty `AND` expression set evaluates to `TRUE` and does not
   restrict structured eligibility.
1. Participant-facing recommendations ordinarily require:
   - An active participant
   - An active study
   - Exact eligibility
   - A study-interest match
   - No participant-side exclusion
1. Partial matches are not shown in ordinary participant-facing matched-study
   lists.
1. Study-facing recommendations may include exact and partial eligibility
   matches.
1. A participant who selects visibility to all study teams may participate in
   pre-interest study-facing matching.
1. Restricted visibility does not change eligibility and does not prevent
   participant-facing matching.
1. Restricted visibility causes a participant-study pair to be treated as not
   recommendable in the pre-interest study-facing direction. No exact or
   partial study-facing Redis recommendation is retained.
1. A restricted-visibility participant does not appear in Matched Participants.
1. After successful interest, the participant appears in the applicable
   study's Interested Participants workflow, where authorized study-team
   members may access the available participant information.
1. Interest does not make the participant visible to unrelated study teams.
1. Matching recommendations and directional exclusions are stored in Redis.
1. Matching recomputation is asynchronous.

## Public discovery

1. Public users may browse and search active, non-archived studies without an account.
1. An account is required to express interest.
1. Public study details may display study contact information.
1. Direct and bookmarked posting URLs are supported.
1. Inactive postings display a not-currently-recruiting message through valid URLs.
1. Public pages may be indexed by external search engines.
1. The participant-facing interested count uses an application-configured threshold.

## Ask if interested

1. Ask if interested is available only for a visible matching participant.
1. It does not create an expression of interest.
1. It does not create a direct-message conversation.
1. It promotes the study in the participant interface.
1. It moves the participant-study pair from the ordinary system-matched presentation to the
   study-team-promoted presentation.
1. It creates the applicable Redis promotion and exclusion records and updates the promotion
   timestamp.
1. A scheduled notification job identifies promoted matches newer than the participant's last login
   and may email the participant to return to the application.
1. The study-team-authored text is displayed with the promoted study rather than delivered as a
   direct participant message.

## Expressing interest

1. A participant may express interest only once in one study.
1. The show-interest UI uses one form containing:
   - Temporal profile updates
   - Screening questions, when configured
1. The temporal profile properties are:
   - Past medical conditions
   - Present medical conditions
   - Parent or guardian of a child under 18
1. The complete form is submitted in one request.
1. Backend processing occurs in one transaction.
1. Temporal profile updates are applied before eligibility is reevaluated.
1. `TRUE` and `MAYBE` may proceed.
1. `FALSE` prevents interest.
1. Screening answers do not affect matching or resolve `MAYBE`.
1. On success, the transaction:
   - Updates the participant profile
   - Updates the participant's in-memory representation
   - Stores questionnaire answers, when applicable
   - Creates `STUDY_VOLUNTEER`
   - Creates applicable Redis exclusions
1. On any failure, none of those changes are committed.
1. The study must remain active until transaction completion.
1. Later eligibility changes do not remove interest.
1. Participants cannot withdraw finalized interest through the application.

## Interested-participant operations

1. New interested participants begin in `NEW`.
1. Fixed workflow lists are:
   - `NEW`
   - `ELIGIBLE`
   - `INELIGIBLE`
   - `PENDING`
1. `ALL` is an aggregate view.
1. One participant-study interest occupies one fixed workflow list at a time.
1. Workflow-list movement does not affect matching, messaging, exports, or Redis exclusions.
1. Labels are study-specific tags.
1. One interested participant may have multiple labels.
1. Labels are included in CSV exports.
1. List movement and label changes are not separately audited.

## Messaging

1. Study teams may message only interested participants.
1. A study team member must initiate the conversation.
1. The participant may reply only after study-team initiation.
1. Conversations are shared among all study members.
1. Templates and reusable attachments are study-specific.
1. Attachment file types are unrestricted.
1. Maximum attachment size is 5 MB.
1. Date-based study inactivity does not hide existing conversations.
1. `PUBLISHABLE = 0` hides conversations.
1. Participant deactivation hides historical conversations from study teams.

## Questionnaires and exports

1. A study may have at most one screening questionnaire.
1. Questionnaire completion is required only when a questionnaire exists.
1. Questionnaires may be edited only while the study is inactive.
1. Question type cannot change after creation.
1. Deleting a response option deletes only answers selecting that option.
1. Deleting a question deletes answers for that question after confirmation.
1. Questionnaires and responses are not versioned.
1. Concurrent stale edits are rejected.
1. Participants cannot edit submitted answers.
1. Interested-participant exports may include:
   - Visible profile fields
   - Contact information
   - Questionnaire answers
   - Workflow-list information
   - Labels
1. `PUBLISHABLE = 0` blocks participant-data access, conversations, and new exports.
1. Downloaded files cannot be recalled.

## Study notifications

1. Notification settings are configured per study and event.
1. One event uses one shared frequency for its selected recipients.
1. New interested-participant and new-message events support:
   - Immediate
   - Daily digest
   - Weekly digest
1. New matched-participant events support:
   - Daily digest
   - Weekly digest
1. The posting creator is subscribed by default.
1. The current PI is automatically subscribed to Other Announcements.
1. External non-member email addresses may receive notifications.
1. Membership removal removes that member's notification settings.
1. Email settings do not control in-application badges.
1. Lifecycle announcements are dispatched by scheduled processing.
1. The PI receives a warning approximately one week before the scheduled study deactivation date.
1. Participant promotion notifications are evaluated by a scheduled job using the promotion
   timestamp and participant's last-login time.

## Administrative scheduled jobs

1. Application-managed jobs use persisted Quartz cron expressions.
1. The administrator job API exposes dynamic Spring job beans, not
   database-native Oracle Scheduler jobs.
1. The administrator job controller requires the application-wide `ADMIN`
   role.
1. The controller supports viewing jobs, immediate execution, cron updates,
   and cron validation with execution-time previews.
1. Pause, resume, clear, and interrupt operations exist in the scheduling
   service but are not exposed by the current administrator job controller.
1. Only full recommendation recomputation has a confirmed explicit
   manual-execution overlap guard.
1. Application jobs use the effective server or Quartz default time zone
   unless configured otherwise.

## Audit

1. Participant-data access is audited through `PHI_AUDIT`.
1. List-view records may identify multiple visible participant IDs.
1. The legacy term `RECOMMENDED` means matched.
1. Workflow-list movement is not separately audited.
1. Label changes are not separately audited.
1. Message records retain sender, recipient, and timestamp as business data.
1. CSV export generation is not separately audited.

## Multi-institution deployment

1. Each adopting organization has a separately branded application instance.
1. Each instance operates on its own application servers, database, and supporting infrastructure.
1. Schemas are intended to remain structurally compatible while data and configuration differ.
1. U-M imports eResearch-derived data.
1. Other institutions may use authenticated incremental CSV imports.
1. No cross-instance access is granted merely because identifiers or email addresses match.
