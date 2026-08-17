---
title: Architecture Overview
summary: Architectural boundaries and links to detailed system pages.
status: authoritative
---

# Architecture Overview

The application consists of two primary data layers:

## Imported governance layer

The `IMPORTED_*` tables hold institutionally supplied study, personnel, role, and publishability information.

This layer is not editable by ordinary study team members.

## Operational application layer

Operational tables hold:

- Application users
- Study postings
- Study memberships
- Participant accounts and profiles
- Matching results
- Prompts
- Expressions of interest
- Questionnaires and responses
- Exports
- Audit history

A scheduled reconciliation process applies imported governance information to the operational layer.

## Architecture pages

- [System context](system-context.md)
- [Multi-institution deployment](multi-institution-deployment.md)
- [Data ownership](data-ownership.md)
- [Import pipeline](../03-institutional-governance/import-pipeline.md)