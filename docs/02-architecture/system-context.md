---
title: System Context
summary: Actors, external systems, imports, operational storage, and exports.
status: authoritative
---

# System Context

```mermaid
flowchart LR
    P[Participant]
    STM[Study Team Member]
    PI[Principal Investigator]
    ADMIN[Administrator]

    subgraph YHR["Institution-Specific YourHealthResearch.org Instance"]
        APP[Web Application]
        IMPORTED[(IMPORTED_* Tables)]
        OPERATIONAL[(Operational Tables)]
        RECON[Reconciliation]

        APP <--> OPERATIONAL
        APP --> IMPORTED
        RECON --> IMPORTED
        RECON --> OPERATIONAL
    end

    IDP[Institutional SAML Identity Provider]
    SOURCE[Institutional Governance Source]
    INGEST[Import Adapter]
    EMAIL[Email Service]
    CSV[Authorized CSV Export]

    P -->|Account, profile, interest, questionnaire| APP
    STM -->|SAML login and study operations| APP
    PI -->|SAML login and PI access| APP
    ADMIN -->|Administrative operations| APP

    APP <--> IDP
    SOURCE --> INGEST
    INGEST -->|Refresh institutional data| IMPORTED
    APP --> EMAIL
    APP --> CSV
```

## External systems

### Institutional identity provider

Authenticates study team members and PIs through SAML.

### Institutional governance source

Supplies authoritative study, role, PI, and recruitment-governance information.

At U-M, this information originates from eResearch.

### Email service

Sends study-team invitations, PI notifications, and other configured notices.

### CSV export

Provides authorized study teams with permitted interested-participant and questionnaire data.

## Internal boundaries

The application must distinguish:

- Imported data from operational data
- Authentication from authorization
- Institutional roles from application roles
- Historical relationships from current data visibility
