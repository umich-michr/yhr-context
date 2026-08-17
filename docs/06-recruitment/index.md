---
title: Recruitment Overview
summary: Eligibility authoring, matching, promotion, participant interest, screening, and export.
status: authoritative
---

# Recruitment Overview

The recruitment workflow combines:

1. Participant profile information
2. Participant study preferences
3. Study attributes
4. Eligibility criteria
5. Participant visibility settings
6. Study-team promotion
7. Participant expressions of interest
8. Screening questionnaires
9. Authorized exports

## Workflow summary

```mermaid
flowchart LR
    PROFILE[Participant Profile]
    PREF[Participant Preferences]
    STUDY[Study Posting]
    MATCH[Matching]
    PROMPT[Ask if Interested]
    INTEREST[Expression of Interest]
    RECHECK[Eligibility Recheck]
    QUESTION[Questionnaire]
    EXPORT[Authorized Export]

    PROFILE --> MATCH
    PREF --> MATCH
    STUDY --> MATCH
    MATCH --> PROMPT
    MATCH --> INTEREST
    PROMPT --> INTEREST
    INTEREST --> RECHECK
    RECHECK --> QUESTION
    QUESTION --> EXPORT
```

Read:

- [Eligibility-criteria authoring](eligibility-criteria-authoring.md)
- [Matching and visibility](matching-and-visibility.md)
- [Ask if interested](ask-if-interested.md)
- [Expressions of interest](expressions-of-interest.md)
- [Questionnaires and exports](questionnaires-and-exports.md)
