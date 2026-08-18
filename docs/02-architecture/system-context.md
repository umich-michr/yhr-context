---
title: System Context
summary: Actors, external systems, import processing, operational storage, and exports.
status: authoritative
---

# System Context

```mermaid
flowchart LR
    P[Participant]
    STM[Study Team Member]
    PI[Principal Investigator]
    ADMIN[Administrator]
    SI[Study Importer or Importing Process]

    subgraph YHR["Institution-Specific YourHealthResearch.org Instance"]
        APP[Web Application]
        INGEST[Import Processing]
        IMPORTED[(IMPORTED_* Tables)]
        RECON[Governance Reconciliation]
        OPERATIONAL[(Operational Tables)]

        APP <--> OPERATIONAL
        APP -->|Read governance and validate study_num| IMPORTED
        INGEST -->|Insert or update imported data| IMPORTED
        IMPORTED -->|Read final imported state| RECON
        RECON -->|Update publishability, users, and PI memberships| OPERATIONAL
    end

    IDP[Institutional SAML Identity Provider]
    SOURCE[Institutional Governance Source]
    EMAIL[Email Service]
    CSVOUT[Authorized Participant CSV Export]

    P -->|Account, profile, interest, questionnaire| APP
    STM -->|SAML login and study operations| APP
    PI -->|SAML login and PI access| APP
    ADMIN -->|Administrative operations| APP
    SI -->|Authenticated incremental CSV upload| INGEST

    APP <--> IDP
    SOURCE -->|eResearch extract or institutional CSV| INGEST
    APP --> EMAIL
    APP --> CSVOUT
```

## External systems and actors

### Institutional identity provider

Authenticates institutional users through SAML, including:

- Study team members
- PIs
- Administrators
- Study importers

### Institutional governance source

Supplies authoritative information about:

- Studies
- Institutional study roles
- The current PI
- Recruitment governance
- Publishability

At U-M, this information originates from eResearch.

### Study importer or importing process

For CSV-based institutions, an authorized study importer or automated process uploads incremental institutional data using an expiring JSON Web Token.

### Email service

Sends:

- Participant account-activation links
- Study-team invitation links
- PI posting notifications
- Import-error reports
- Delayed study-status notifications
- Other configured notices

### Participant CSV export

Authorized users may generate and download permitted interested-participant and questionnaire data.

The application streams the export to the browser and does not retain a server-side export file.

## Internal boundaries

The application must distinguish:

- Imported data from operational data
- Import processing from reconciliation
- Authentication from authorization
- Institutional roles from application-wide roles
- Application-wide roles from study-association roles
- Active recruitment from access to historical interested-participant data
- Historical relationships from current participant-profile visibility
