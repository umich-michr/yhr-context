# YourHealthResearch.org Context Repository Instructions

This repository contains the authoritative functional and technical context for
YourHealthResearch.org.

## Context routing

1. Start with `docs/context-map.yaml`.
2. Find the topic that best matches the question.
3. Read the topic's `primary` page.
4. Read `related` pages only when the question crosses module boundaries.
5. Use `docs/01-overview/business-rules.md` only for cross-cutting invariants or
   conflict resolution.
6. Consult `docs/09-decisions/` before inferring behavior not explicitly
   documented.

`docs/llms.txt` is generated during local and CI builds and may not exist in a
fresh repository checkout. Do not depend on it as the repository source of
truth.

## Documentation status

- `authoritative`: confirmed current behavior
- `recommended`: proposed controls or improvements
- `mixed`: confirmed context combined with clearly identified proposals
- `open`: unresolved behavior

Do not present recommended, proposed, or open content as implemented behavior.

## Editing rules

When changing application behavior documentation:

1. Update the canonical topic page.
2. Update `docs/01-overview/business-rules.md` if the change is cross-cutting.
3. Update `docs/context-map.yaml` if routing changes.
4. Update open-question pages when a question is resolved or newly discovered.
5. Avoid duplicating full explanations across several pages; prefer concise
   summaries and links to canonical pages.
6. Run `make check` before proposing or committing changes.

## Generated files

Do not manually edit:

```text
docs/llms.txt
site/
