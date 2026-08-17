# YourHealthResearch.org Application Context

This repository contains functional, architectural, data-model, governance, and support documentation for YourHealthResearch.org.

The documentation is intended for:

- Application developers
- Product owners
- Support personnel
- Security and privacy reviewers
- Institutional partners
- AI assistants and LLM-based support tools

## Documentation site

The published GitHub Pages site is the preferred interface for human readers.

Start with:

- `docs/index.md` for the main documentation portal
- `docs/context-map.yaml` for machine-readable topic routing
- `docs/llms.txt` is generated from that map during the MkDocs build

## Local development

Install the documentation dependencies:

```bash
python -m pip install -r requirements.txt
```

Run the site locally:

```bash
mkdocs serve
```

Open:

```
http://127.0.0.1:8000
```

## Publishing

The GitHub Actions workflow in `.github/workflows/deploy-docs.yml` publishes the site to GitHub Pages whenever changes are pushed to the `main` branch.

In the GitHub repository settings:

1. Open **Settings**.
2. Select **Pages**.
3. Set the source to **GitHub Actions**.

## Documentation conventions

- Confirmed behavior is stated as a business rule.
- Recommendations are labeled as recommendations.
- Unresolved behavior is documented under `docs/09-decisions/`.
- Each concept should have one canonical page.
- Other pages should link to the canonical page instead of duplicating its full content.
