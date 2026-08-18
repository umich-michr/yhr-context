#!/usr/bin/env python3
"""
Generate docs/llms.txt from docs/context-map.yaml and validate that every
path referenced in context-map.yaml resolves to a real file under docs/.

Run directly:
    python scripts/generate_llms_txt.py

Or via MkDocs hooks (see mkdocs.yml hooks configuration).

Exits non-zero if any referenced path is missing, so it acts as both a
generator and a consistency check.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
DOCS_DIR = REPO_ROOT / "docs"
CONTEXT_MAP = DOCS_DIR / "context-map.yaml"
OUTPUT = DOCS_DIR / "llms.txt"


def load_yaml() -> dict:
    with CONTEXT_MAP.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def all_paths(data: dict) -> list[tuple[str, str]]:
    """Return all (field_description, path) pairs from context-map.yaml."""
    paths: list[tuple[str, str]] = []

    interp = data.get("document", {}).get("interpretation", {})
    for field, path in interp.items():
        paths.append((f"document.interpretation.{field}", path))

    for entry in data.get("start_here", []):
        paths.append(("start_here", entry["path"]))

    for topic_key, topic in data.get("topics", {}).items():
        paths.append((f"topics.{topic_key}.primary", topic["primary"]))
        for rel in topic.get("related", []):
            paths.append((f"topics.{topic_key}.related", rel))

    return paths


def validate(data: dict) -> list[str]:
    """Return a list of error strings for every missing file."""
    errors: list[str] = []
    for field, path in all_paths(data):
        if not (DOCS_DIR / path).is_file():
            errors.append(f"  Missing file referenced by {field}: docs/{path}")

    # Check that every topic referenced in sections exists in the topics map.
    topic_keys = set(data.get("topics", {}).keys())
    for section in data.get("sections", []):
        for ref in section.get("topics", []):
            if ref not in topic_keys:
                errors.append(
                    f"  Section '{section['heading']}' references unknown "
                    f"topic key: {ref!r}"
                )
    return errors


def path_label(path: str, topics: dict) -> str:
    """
    Derive a clean link-text label for a path.
    Prefers the label of the topic whose primary matches the path; falls back
    to title-casing the filename stem.
    """
    for topic in topics.values():
        if topic.get("primary") == path:
            return topic["label"]
    stem = Path(path).stem.replace("-", " ")
    return stem.capitalize()


def generate(data: dict) -> str:
    doc = data["document"]
    topics = data.get("topics", {})
    lines: list[str] = []

    # Header
    lines.append(f"# {doc['title']}")
    lines.append("")
    tagline = doc.get("tagline", "").strip().replace("\n", " ")
    lines.append(f"> {tagline}")
    lines.append("")
    lines.append(
        "Use this file as a routing index. Read only the pages relevant to the "
        "current question. Do not infer unresolved behavior from recommendations "
        "or open questions."
    )
    lines.append(
        "Load business-rules.md only for cross-cutting invariants, conflict "
        "checks, or multi-module questions; for narrow questions start with the "
        "canonical topic page."
    )
    lines.append("")

    # Start here
    lines.append("## Start here")
    lines.append("")
    for entry in data.get("start_here", []):
        path = entry["path"]
        label = entry.get("label", path_label(path, topics))
        note = entry.get("note", "")
        suffix = f": {note}" if note else ""
        lines.append(f"- [{label}]({path}){suffix}")
    lines.append("")

    # Topic sections — deduplicate pages within each section
    lines.append("## Route questions by topic")
    lines.append("")
    for section in data.get("sections", []):
        lines.append(f"### {section['heading']}")
        lines.append("")
        # Use an ordered dict to deduplicate while preserving insertion order.
        seen: dict[str, str] = {}
        for topic_key in section.get("topics", []):
            topic = topics[topic_key]
            primary = topic["primary"]
            if primary not in seen:
                seen[primary] = topic["label"]
            for rel in topic.get("related", []):
                if rel not in seen:
                    seen[rel] = path_label(rel, topics)
        for path, label in seen.items():
            lines.append(f"- [{label}]({path})")
        lines.append("")

    # Interpretation rules
    lines.append("## Interpretation rules")
    lines.append("")
    for i, rule in enumerate(doc.get("interpretation_rules", []), start=1):
        lines.append(f"{i}. {rule}")
    lines.append("")

    return "\n".join(lines)


def main() -> None:
    data = load_yaml()

    errors = validate(data)
    if errors:
        print("context-map.yaml validation failed:", file=sys.stderr)
        for err in errors:
            print(err, file=sys.stderr)
        sys.exit(1)

    content = generate(data)
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"Generated {OUTPUT.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
