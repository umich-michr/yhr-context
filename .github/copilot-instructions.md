# UMHealthResearch / YourHealthResearch.org Context Repository Instructions

This repository contains the functional and technical context for the UMHealthResearch platform and
its institution-specific branded application instances, including YourHealthResearch.org.

## Context routing

1. Start with `docs/context-map.yaml`.
1. Identify the topic that best matches the question.
1. Read the topic's `primary` page.
1. Read `related` pages only when the question crosses module boundaries.
1. Use `docs/01-overview/business-rules.md` only for cross-cutting invariants or conflict
   resolution.
1. Consult `docs/09-decisions/` before inferring behavior that is not explicitly documented.
1. When a page contains deployment-specific behavior, confirm that the behavior applies to the
   institution or branded instance in question.

`docs/llms.txt` is generated during local and CI builds and may not exist in a fresh repository
checkout. Do not depend on it as the repository source of truth.

When source inspection is required, use the canonical
[Source Repository Routing](../docs/02-architecture/source-repository-routing.md) maintenance
reference rather than inferring ownership from historical repository names.

## Documentation status

- `authoritative`: confirmed current behavior
- `recommended`: proposed controls, designs, or improvements
- `mixed`: confirmed context combined with clearly identified proposals
- `open`: unresolved behavior

Do not present recommended, proposed, mixed-page proposals, or open content as implemented behavior.

A page-level `authoritative` status does not resolve a known contradiction recorded in
`docs/09-decisions/`. When an authoritative page conflicts with an open reconciliation item,
describe the behavior as unresolved until the conflict is formally resolved.

## Source precedence and conflict handling

Use the following order when interpreting documentation:

1. A current canonical page with implementation evidence and a recorded verification date
1. A resolved decision record
1. Cross-cutting business rules
1. Other authoritative topic pages
1. Historical summary documents
1. Mixed, recommended, and open pages

A historical or summary context document may identify missing behavior, but it must not silently
overwrite newer implementation findings.

When two sources conflict:

1. Do not choose one solely because it is more detailed.
1. Check the applicable deployment, application version, and authoring era.
1. Check implementation evidence such as source code, schema definitions, configuration, tests, job
   definitions, or verified production behavior.
1. Record the conflict in `docs/09-decisions/open-questions.md`.
1. Treat the behavior as unresolved until a decision is recorded.
1. After resolution, update every canonical page that states the old behavior.

## Required distinctions

Keep the following concepts separate:

```text
UMHealthResearch platform
≠ Institution-specific branded instance

Account owner
≠ Represented participant

Application-wide role
≠ Study-association role

Current imported PI
≠ Any user retaining an operational PRINCIPAL_INVESTIGATOR membership

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

Event creation
≠ Notification recipient configuration
≠ Email dispatch

Relational source data
≠ In-memory matching objects
≠ Redis recommendation data

Export permission
≠ A retained server-side export file
```

## Functional and technical answers

For nontechnical questions:

- Prefer participant-facing and study-team-facing terminology.
- Explain behavior before implementation.
- Avoid exposing physical table names unless they help answer the question.
- State privacy and authorization boundaries clearly.

For technical questions:

- Identify the authoritative source of data.
- Distinguish relational storage, Redis storage, in-memory state, and generated output.
- Name physical tables only when verified.
- Do not use conceptual entity names as production table names.
- Identify asynchronous jobs, delayed processing, and recomputation where they affect observed
  behavior.
- State whether behavior applies to all deployments or only one ingestion path.

## Editing rules

When changing application behavior documentation:

1. Update the canonical topic page.
1. Update `docs/01-overview/business-rules.md` if the change is cross-cutting.
1. Update `docs/01-overview/terminology.md` if a term or distinction changes.
1. Update `docs/context-map.yaml` if routing changes.
1. Update open-question pages when a question is resolved or newly discovered.
1. Update technical schema and relationship pages when physical storage changes.
1. Update support and troubleshooting pages when operational behavior changes.
1. Avoid duplicating full explanations across several pages; prefer concise summaries and links to
   canonical pages.
1. Preserve newer, independently verified functionality that is absent from an older summary
   document.
1. Run `make check` before proposing or committing changes.

## Evidence expectations

An authoritative technical assertion should be supported by one or more of:

- Current application source code
- Database DDL or an authoritative schema extract
- Configuration or seed data
- Automated tests
- Scheduled-job definitions
- Verified production behavior
- A recorded product, legal, privacy, security, or institutional decision

Examples and inferred behavior are not sufficient by themselves to establish an authoritative rule.

When possible, page front matter should identify:

```yaml
last_verified: "YYYY-MM-DD"
scope:
  deployments: ["all"]
implementation_refs:
  - "source, schema, test, or job reference"
```

Do not invent verification metadata when it is unavailable.

## Generated files

Do not manually edit:

```text
docs/llms.txt
site/
```
