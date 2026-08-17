---
title: Business Rules
summary: Canonical cross-cutting application invariants.
status: authoritative
---

# Business Rules

This page is the canonical source for confirmed cross-cutting rules.

## Role systems

1. The application has four application-wide roles:
   - `ADMIN`
   - `STUDY_IMPORTER`
   - `STAFF`
   - `VOLUNTEER`
2. Study associations use two separate roles:
   - `PRINCIPAL_INVESTIGATOR`
   - `STUDY_TEAM_MEMBER`
3. Application-wide roles and study-association roles must not be treated as the same type of role.
4. A `STAFF` user must have a study association to access a particular study.
5. For study-data access, `PRINCIPAL_INVESTIGATOR` and `STUDY_TEAM_MEMBER` have equivalent permissions.
6. `STUDY_IMPORTER` is limited to institutional CSV import functions.
7. `ADMIN` is a superuser with access to all studies and participant data.
8. `VOLUNTEER` represents a participant account.

## Participant identity

9. Participants use local, database-backed accounts.
10. A participant's email address functions as the username.
11. A participant must activate a new account using an expiring email link.
12. The activation link contains a randomly generated Java UUID token.
13. The activation-link expiration duration is an application setting.
14. Participants may deactivate their own accounts and request reactivation through support.
15. Administrators may activate, reactivate, and deactivate participant accounts and reset participant passwords.
16. Participant deletion is a hard deletion initiated only after the participant explicitly emails support.
17. A deleted participant email address may be reused.
18. The database prevents duplicate active email usernames, but the application does not attempt to detect that two accounts represent the same person.
19. Hard deletion removes participant account, profile, preferences, matches, expressions of interest, questionnaire data, and application audit records after administrator confirmation.

## Institutional identity and access

20. Institutional users authenticate through SAML.
21. Institutional accounts are managed through institutional identity providers.
22. Institutional accounts cannot be deactivated or deleted through the application.
23. SAML authentication alone does not grant access to a study.
24. Study access normally requires an active study association.
25. Administrators may access all studies without an ordinary study association.

## Institutional governance

26. Institutional data is loaded into read-only `IMPORTED_*` tables.
27. Ordinary study team members cannot modify imported data.
28. Each institutional import is incremental.
29. Imported rows absent from a subsequent import remain unchanged.
30. PI status is controlled by the institutional source.
31. A valid imported study has exactly one current institutional PI.
32. Only the imported PI role automatically produces application study access.
33. Other imported institutional roles do not automatically grant application access.
34. `PUBLISHABLE` must be either `0` or `1`.
35. A null, missing, or otherwise invalid publishable value is an application error.
36. An operational study missing from a later incremental import remains unchanged.

## Study posting creation

36. A posting can be created only for a `study_num` in `IMPORTED_STUDY`.
37. Only one operational study posting may exist for a `study_num`.
38. Study postings cannot be deleted through application UIs.
39. A posting may be edited but cannot be deleted and recreated through the UI.
40. The posting creator becomes associated with the study.
41. A non-PI creator receives the study role `STUDY_TEAM_MEMBER`.
42. The imported PI receives the study role `PRINCIPAL_INVESTIGATOR`.
43. An `APP_USER` is created for an imported PI when one does not already exist.
44. A PI record missing email or ePPN is an application error.
45. When a PI `APP_USER` already exists, imported name and email changes are not copied into the existing record.
46. When a PI `APP_USER` is newly created, the imported identity information is copied into it.
47. The PI is notified of posting creation according to the posting-notification workflow.

## Study memberships

48. Any study team member associated with a study may invite another SAML-authenticated institutional user.
49. Any associated study team member may remove an ordinary `STUDY_TEAM_MEMBER`.
50. A posting creator may be removed unless the creator is also the institutionally identified PI.
51. An invited member may be removed.
52. A current PI cannot be removed through ordinary application UIs.
53. Administrators cannot directly create study memberships through application UIs.
54. Backend database intervention may create memberships but is outside the normal UI workflow.
55. Ordinary study team members may export permitted study data.

## Publishability and active status

56. A study's active status depends on:
   - The current date falling within the activation and deactivation dates
   - `PUBLISHABLE` being `1`
57. Activation and deactivation date boundaries are inclusive.
58. `PUBLISHABLE = 0` makes the study inactive.
59. If `PUBLISHABLE` returns to `1` while the date range remains active, the study becomes active again automatically.
60. The application currently does not change the study's deactivation date when publishability becomes `0`.
61. An expired study may be reactivated by changing its dates, provided `PUBLISHABLE = 1`; there is no separate manual-deactivation control.
62. An inactive study loses current matches; fresh matches are recomputed when it becomes active again.
63. Historical interested-participant data remains accessible while `PUBLISHABLE = 1`, even if the study is inactive.
64. When an inactive study is accessed through its valid `study_num` URL, the participant sees a message that the study is no longer recruiting.

## Import processing

63. CSV imports are authenticated using expiring JSON Web Tokens.
64. Token timing is governed by the `STUDY_IMPORT_TOKEN_GRACE_PERIOD` application setting.
65. CSV anomalies are detected by application validation.
66. Validation problems are written to logs and emailed to the responsible study importer.
67. CSV reconciliation occurs through Java application code when imported data is applied.
68. U-M reconciliation is performed through a scheduled database workflow and Oracle package.
69. A CSV may contain multiple chronological updates for the same study.
70. Only the latest update for a study is applied to operational application data.
71. Intermediate rows for the same study must not cause temporary study deactivation or notification.
72. Import batches cannot be rolled back through the application.

## Matching

73. Interest matching and eligibility matching are separate evaluations.
74. Eligibility uses three-valued logic:
   - `TRUE`
   - `MAYBE`
   - `FALSE`
75. A missing optional participant profile value referenced by a criterion produces `MAYBE`.
76. Three-valued `AND`, `OR`, and `NOT` follow the truth tables in [Matching and visibility](../06-recruitment/matching-and-visibility.md).
77. `TRUE` eligibility matches are exact matches.
78. `MAYBE` eligibility matches are partial matches.
79. Restricted participants are hidden from study teams until they express interest.
80. Discoverable participants may be visible as exact (`TRUE`) or partial (`MAYBE`) matches; participants themselves are not shown partial matches.
81. Ask if interested does not create an expression of interest.
82. Participants cannot withdraw an expression of interest.

## Match recalculation

83. When a participant profile property referenced by eligibility criteria changes, matches between that participant and all active studies are recalculated.
84. When a participant's study interests change, that participant's matched-study list is recalculated.
85. A participant-interest change does not recalculate study-side matched-participant lists.
86. When a study property referenced by participant study interests changes, matched-study lists are recalculated for affected participants.
87. When study eligibility criteria change:
   - The study's matched-participant list is recalculated
   - Participants' matched-study lists are recalculated
88. Match results are stored in Redis and recomputed asynchronously; failed recalculations require a manually triggered recomputation job.

## Expressing interest

89. At the time of expressing interest, participants are asked to refresh specified temporal profile values.
90. Temporal values include:
   - Past medical conditions
   - Present medical conditions
   - Whether the participant is a parent or guardian of a child under 18
91. Eligibility is rechecked using current participant information; `TRUE` and `MAYBE` may proceed, while `FALSE` cannot.
92. Interest is created only after successful questionnaire completion, with temporal-profile updates and questionnaire submission committed atomically.
93. If the study is inactive or non-publishable at submission, interest is not created and the participant sees a not-recruiting message.
94. After interest is successfully recorded, later eligibility changes do not alter the interest relationship.
95. Historical interest remains visible when an active participant later becomes ineligible.

## Questionnaires and exports

94. A study can have only one screening questionnaire.
95. Questionnaire completion is required to finalize the interest workflow.
96. Individual questions may be required or optional.
97. Participants cannot edit submitted questionnaire answers.
98. A study must be deactivated before its questionnaire structure can be changed.
99. Study teams may add or delete questionnaire questions while the study is inactive.
100. Existing question content cannot be edited; question display order may be changed while the study is inactive.
101. Questionnaires are not versioned.
102. Only the current questionnaire structure is retained; deleting a question also deletes its prior answers after confirmation.
103. Authorized study team members may export all participant profile fields, including contact information, and all questionnaire answers.
104. Exports are allowed whenever `PUBLISHABLE = 1`, including for inactive studies; export actions are not separately audited.
105. A downloaded CSV cannot be invalidated or recalled by the application.

## Deactivation and historical visibility

106. A deactivated participant no longer participates in matching.
107. A non-publishable or otherwise inactive study no longer participates in active matching.
108. Historical expressions of interest may remain after participant or study deactivation.
109. Participant profile information is hidden when applicable participant or study deactivation rules require it.
110. Historical relationship retention and current profile visibility are separate concepts.

## Multi-institution deployment

111. Each adopting institution has a separately branded application instance.
112. Each institutional instance has a separate database schema.
113. Schemas are structurally identical, while data and configuration differ.
114. U-M imports eResearch-derived data.
115. Other institutions upload incremental CSV data through an authenticated application API.
