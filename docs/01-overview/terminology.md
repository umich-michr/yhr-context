---
title: Terminology
summary: Canonical definitions used throughout the documentation.
status: authoritative
---

# Terminology

 Term | Definition |
|---|---|
| Participant | A person who creates a local account and may participate in research recruitment. Participants normally have the application-wide role `VOLUNTEER`. |
| Institutional user | A person who authenticates through an institution's SAML identity provider. |
| Study team member | An institutional `STAFF` user associated with a particular study through a `STUDY_TEAM_MEMBER` or `PRINCIPAL_INVESTIGATOR` study role. |
| Principal investigator / PI | The institutional person currently identified as PI by the authoritative imported study data. |
| Application-wide role | A role controlling general application capabilities: `ADMIN`, `STUDY_IMPORTER`, `STAFF`, or `VOLUNTEER`. |
| Study-association role | A role connecting a `STAFF` user to a specific study: `PRINCIPAL_INVESTIGATOR` or `STUDY_TEAM_MEMBER`. |
| `ADMIN` | An application-wide superuser role that can access all studies and participant data and perform supported participant-account administration. |
| `STUDY_IMPORTER` | An application-wide role limited to importing institutional CSV data into the `IMPORTED_*` tables. |
| `STAFF` | An application-wide institutional-user role. A `STAFF` user must also be associated with a study to access that study's data. |
| `VOLUNTEER` | The application-wide role used for participant accounts. |
| Institutional source of truth | The governed institutional system or dataset that identifies studies, institutional roles, PIs, and recruitment permissions. |
| eResearch | The University of Michigan workflow application containing IRB applications and related study information. |
| Study number / `study_num` | The institutionally assigned identifier for a study. It maps to `IMPORTED_STUDY.ID`. |
| Imported study | The local, read-only representation of a study supplied by the institution. |
| Study posting | The participant-facing recruiting representation of an imported study. |
| Institutional role | A role maintained outside the application, such as PI or study coordinator. |
| Publishable | A required Boolean value indicating whether the institution currently permits the study to recruit through the application. |
| Reconciliation | Processing that aligns operational study, PI, and user data with imported institutional data. |
| Exact match | A match for which all evaluated eligibility expressions resolve to `TRUE`. |
| Partial match | A match containing one or more `MAYBE` results caused by missing optional participant profile values. |
| Interest match | A result indicating that a study corresponds to a participant's stated study interests. |
| Eligibility match | A `TRUE`, `MAYBE`, or `FALSE` result indicating whether a participant appears to satisfy study eligibility criteria. |
| Restricted participant | A participant hidden from study teams until the participant expresses interest. |
| Discoverable participant | A participant who may be visible to an eligible study before expressing interest. |
| Ask if interested | A study-team action that promotes a study in the participant interface without creating an expression of interest. |
| Expression of interest | An explicit participant action indicating interest in a study. |
| Temporal profile property | Participant information expected to change over time and therefore refreshed when the participant expresses interest. |
| Deactivation | Disabling current application or recruitment activity while retaining applicable historical records. |
| Hard deletion | Permanent deletion of a participant account and its application records through the support-request process. |

## Naming note

The following terms refer to the same authoritative identifier:

```text
study number
study_num
IMPORTED_STUDY.ID
```

Documentation should prefer:

study_num when discussing application workflows
IMPORTED_STUDY.ID when discussing database storage

Study URLs expose both:

The institutionally assigned study_num
An internally assigned sequence-based study identifier 

The institutionally assigned study number is intentionally included in user-friendly, bookmarkable study-posting URLs.
