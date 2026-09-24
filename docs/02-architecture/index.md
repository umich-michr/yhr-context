---
title: Architecture Overview
summary: Architectural boundaries and links to detailed system pages.
status: authoritative
---

# Architecture Overview

The application contains several storage and processing areas.

## Imported governance layer

The `IMPORTED_*` tables hold institutionally supplied:

- Study information
- Personnel information
- Institutional roles
- PI assignments
- Publishability

This layer is not editable by ordinary study team members.

## Operational relational layer

Operational application tables hold:

- Application users
- Study postings
- Study memberships
- Participant accounts and profiles
- Study properties
- Eligibility criteria
- Prompts
- Expressions of interest
- Questionnaires and responses
- Audit history

## Nonrelational match layer

Current participant-study recommendations and directional exclusions are stored in Redis sorted
sets.

Redis match data is derived from operational application data and is asynchronously recomputed after
relevant changes.

See [Redis Match and Exclusion Model](../07-data-model/redis-match-model.md).

## Generated exports

Participant-data CSV exports are generated in memory and streamed to the browser.

The application does not retain them as relational export records or server-side files.

## Reconciliation

A reconciliation process applies imported governance information to the operational relational
layer.

The implementation differs by ingestion path:

- U-M uses a scheduled database workflow and Oracle package.
- CSV-based institutions use Java application code during import processing.

## Architecture pages

- [System Context](system-context.md)
- [Multi-Institution Deployment](multi-institution-deployment.md)
- [Data Ownership](data-ownership.md)
- [Source Repository Routing](source-repository-routing.md)
- [Import Pipeline](../03-institutional-governance/import-pipeline.md)
- [Data-Model Overview](../07-data-model/index.md)
