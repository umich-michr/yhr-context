---
title: Terminology
summary: Canonical definitions used throughout the documentation.
status: authoritative
---

# Terminology

| Term | Definition |
|---|---|
| YourHealthResearch.org | The platform and product name. The same domain is also used for a public marketing website directed toward prospective adopting organizations. |
| Branded instance | A separately configured deployment of the YourHealthResearch.org platform with its own name, URL, servers, database, infrastructure, institutional integrations, and data. |
| Participant | A person represented by a local application account and participant profile. |
| Volunteer | A participant. The application and database may use volunteer-oriented terminology such as `VOLUNTEER` or `VOL`. |
| Account owner | The person who authenticates and manages their own account and, when applicable, one or more loved-one accounts. |
| Owning account | The account used by an account owner to authenticate and manage loved-one accounts. |
| Parent account | A legacy or informal synonym for owning account. It does not necessarily mean that the owner is the represented participant's legal parent. |
| Represented participant | The person whose profile, matching, interests, questionnaires, and messages belong to the current participant-account context. |
| Loved-one account | A separate participant account managed by an owning participant account through `LOVED_ONE`. |
| Signup for a loved one | Registration flow that creates a minimal owning account and a complete loved-one participant account. |
| Add Loved One | Workflow used by an existing owning account to create another loved-one participant account. |
| Institutional user | A person who authenticates through an institutional SAML identity provider. |
| Study team member | A `STAFF` user associated with a study as `STUDY_TEAM_MEMBER` or `PRINCIPAL_INVESTIGATOR`. |
| Current imported PI | The person currently identified as PI by the institution's imported source-of-truth data. |
| Principal investigator / PI | The current imported PI unless a page explicitly discusses the operational `PRINCIPAL_INVESTIGATOR` membership. |
| Application-wide role | `ADMIN`, `STUDY_IMPORTER`, `STAFF`, or `VOLUNTEER`. |
| Study-association role | `PRINCIPAL_INVESTIGATOR` or `STUDY_TEAM_MEMBER`. |
| Study number / `study_num` | Institutionally assigned study identifier corresponding to `IMPORTED_STUDY.ID`. |
| Imported study | Read-only institutional study data used for governance and posting validation. |
| Study posting | Participant-facing recruiting representation of an imported study. |
| Publishable | Institutionally governed Boolean indicating whether the study may recruit through the application. |
| Active study | A study with `PUBLISHABLE = 1` whose inclusive activation and deactivation boundaries contain the current date/time. |
| Manual activation | Study-team action that sets the activation boundary to the current date/time and records a future deactivation boundary. |
| Manual deactivation | Study-team action that sets the deactivation boundary to the current date/time, causing the study to become inactive as current time passes that boundary. |
| Active interval | A persisted period in `STUDY_ACTIVE_INTERVAL` during which the derived study status was active. |
| Archived study | An inactive study placed in Archived Studies. Archive status does not itself change otherwise permitted historical participant-data access. |
| Participant agreement | Agreement applicable to a participant or volunteer account, represented by an agreement type such as `VOL`. |
| Study-team agreement | Agreement applicable to a study team member, represented by an agreement type such as `STM`. |
| Agreement version | Current version for an agreement type in `USER_AGREEMENT`. A user must have a matching acceptance in `USER_AGREEMENT_AUDIT`. |
| Discoverable visibility | Participant choice allowing all study teams using the branded instance to see the profile when the participant appears to be a suitable match. |
| Restricted visibility | Participant choice allowing only study teams whose studies the participant has shown interest in to see the profile. |
| Interest match | Result of comparing participant study interests with study properties. |
| Exact eligibility match | Eligibility evaluation whose overall result is `TRUE`. |
| Partial eligibility match | Eligibility evaluation whose overall result is `MAYBE`. |
| Ask if interested | Study-team action that promotes a visible matching study to a participant without creating interest or opening direct messaging. |
| System-matched study | Participant-facing study recommendation created by the ordinary matching process. |
| Study-team-promoted study | Matching study emphasized through Ask if interested and displayed separately from ordinary system matches. |
| Expression of interest | Finalized participant action creating a `STUDY_VOLUNTEER` relationship. |
| Interested participant | Participant associated with a study through `STUDY_VOLUNTEER`. |
| Workflow list | One of `NEW`, `ELIGIBLE`, `INELIGIBLE`, or `PENDING`, used to organize interested participants. |
| Label | Study-specific, study-team-created tag applied to interested participants. |
| Conversation | Study-specific message history between the study team and an interested participant, initiated by the study team. |
| Screening questionnaire | Optional study-specific questionnaire presented during show interest; its answers are not used by matching. |
| Temporal profile property | Past conditions, present conditions, or parent/guardian status refreshed during show interest. |
| In-memory matching data | Active participant and study entities maintained in application memory so match calculations do not need to repeatedly load every entity from the database. |
| Memory synchronization | Processing that keeps in-memory matching entities aligned with authoritative database records and removes entities that become inactive. |
| Redis recommendation data | Directional participant-study recommendations, promotions, and exclusions derived from application data and stored in Redis. |
| Hard deletion | Support-initiated permanent removal of participant data, subject to the retained internal participant identifier and deletion reason. |

## Study identifier naming

The following refer to the authoritative institutional identifier:

```text
study number
study_num
IMPORTED_STUDY.ID
```

Participant-facing URLs may also include an internal sequence-based identifier.

## Product and instance examples

| Adopting organization | Branded instance |
|---|---|
| Michigan Institute for Clinical and Health Research, University of Michigan | `UMHealthResearch.org` |
| Clinical and Translational Science Institute, University of Miami | `UMiamiHealthResearch.org` |
| Institute for Translational Medicine | `BeTheNewNormalMatch.org` |
| University of Illinois Chicago | `healthresearch.ccts.uic.edu` |

The Institute for Translational Medicine is a consortium involving Rush
University, Northwestern University, Loyola University Chicago, and the
University of Chicago, led by the University of Chicago.

## Important distinctions

These terms must not be treated as interchangeable:

```text
YourHealthResearch.org platform
≠ Branded application instance

Account owner
≠ Represented participant

Application-wide role
≠ Study-association role

Current imported PI
≠ Arbitrary institutional study role

Imported institutional role
≠ Operational study membership

Study-interest matching
≠ Eligibility matching

Matching
≠ Ask if interested
≠ Expression of interest
≠ Messaging

Inactive
≠ Archived

Relational database record
≠ In-memory matching representation
≠ Redis recommendation or exclusion

Export availability
≠ A retained server-side export file
```
