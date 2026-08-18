from pathlib import Path
import re
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
CONTEXT_MAP_PATH = DOCS_DIR / "context-map.yaml"
LLMS_PATH = DOCS_DIR / "llms.txt"


def load_context_map() -> dict[str, Any]:
    """Load the machine-readable documentation routing map."""

    with CONTEXT_MAP_PATH.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    if not isinstance(data, dict):
        raise ValueError(
            "docs/context-map.yaml must contain a YAML mapping at its root."
        )

    return data


def read_front_matter(path: str) -> dict[str, Any]:
    """
    Read YAML front matter from a documentation file.

    Returns an empty dictionary when the file does not exist, does not use
    front matter, or contains front matter that cannot be parsed.
    """

    file_path = DOCS_DIR / path

    if not file_path.is_file():
        return {}

    text = file_path.read_text(encoding="utf-8")

    if not text.startswith("---\n"):
        return {}

    closing_delimiter = text.find("\n---\n", 4)

    if closing_delimiter == -1:
        return {}

    front_matter_text = text[4:closing_delimiter]

    try:
        metadata = yaml.safe_load(front_matter_text)
    except yaml.YAMLError:
        return {}

    return metadata if isinstance(metadata, dict) else {}


def fallback_label(path: str) -> str:
    """
    Produce a readable label when the path has no configured label and its
    Markdown file has no front-matter title.
    """

    stem = Path(path).stem
    words = re.split(r"[-_]+", stem)

    return " ".join(word.capitalize() for word in words if word)


def page_label(
    path: str,
    configured_label: str | None = None,
) -> str:
    """
    Resolve a page's display label using this priority:

    1. Label explicitly configured in context-map.yaml
    2. Front-matter title in the target Markdown page
    3. Humanized filename
    """

    if configured_label:
        return configured_label

    metadata = read_front_matter(path)
    title = metadata.get("title")

    if isinstance(title, str) and title.strip():
        return title.strip()

    return fallback_label(path)


def page_summary(
    path: str,
    configured_note: str | None = None,
) -> str | None:
    """
    Resolve an optional page description using this priority:

    1. Note explicitly configured in context-map.yaml
    2. Front-matter summary in the target Markdown page
    """

    if configured_note:
        return configured_note.strip()

    metadata = read_front_matter(path)
    summary = metadata.get("summary")

    if isinstance(summary, str) and summary.strip():
        return summary.strip()

    return None


def format_link(
    path: str,
    label: str,
    note: str | None = None,
) -> str:
    """Format one Markdown-compatible llms.txt link."""

    line = f"- [{label}]({path})"

    if note:
        line += f": {note}"

    return line


def collect_section_primary_paths(
    context_map: dict[str, Any],
) -> set[str]:
    """
    Collect primary pages that have their own topics in generated sections.

    A page with its own primary topic is reserved for that canonical position.
    If it appears as a related page in an earlier section, it is not emitted
    early.
    """

    topics = context_map.get("topics", {})
    sections = context_map.get("sections", [])

    primary_paths: set[str] = set()

    if not isinstance(topics, dict):
        return primary_paths

    if not isinstance(sections, list):
        return primary_paths

    for section in sections:
        if not isinstance(section, dict):
            continue

        topic_names = section.get("topics", [])

        if not isinstance(topic_names, list):
            continue

        for topic_name in topic_names:
            topic = topics.get(topic_name)

            if not isinstance(topic, dict):
                continue

            primary = topic.get("primary")

            if isinstance(primary, str) and primary:
                primary_paths.add(primary)

    return primary_paths


def generate_llms_text(context_map: dict[str, Any]) -> str:
    """
    Generate llms.txt with global path deduplication.

    Rules:

    - A path is emitted no more than once.
    - Start-here pages are emitted first.
    - Related pages that have primary topics elsewhere are reserved for their
      canonical sections.
    - Other related pages are emitted the first time they are encountered.
    """

    document = context_map.get("document", {})
    topics = context_map.get("topics", {})
    sections = context_map.get("sections", [])
    start_here = context_map.get("start_here", [])

    if not isinstance(document, dict):
        document = {}

    if not isinstance(topics, dict):
        topics = {}

    if not isinstance(sections, list):
        sections = []

    if not isinstance(start_here, list):
        start_here = []

    title = document.get(
        "title",
        "YourHealthResearch.org Application Context",
    )

    tagline = document.get("tagline")

    emitted_paths: set[str] = set()
    output: list[str] = []

    reserved_primary_paths = collect_section_primary_paths(context_map)

    start_here_paths = {
        entry.get("path")
        for entry in start_here
        if isinstance(entry, dict)
        and isinstance(entry.get("path"), str)
    }

    output.append(f"# {title}")
    output.append("")

    if isinstance(tagline, str) and tagline.strip():
        output.append(f"> {tagline.strip()}")
        output.append("")

    output.append(
        "Use this file as a routing index. Read only the pages relevant "
        "to the current question."
    )
    output.append("")

    interpretation_rules = context_map.get("interpretation_rules", [])

    if isinstance(interpretation_rules, list) and interpretation_rules:
        output.append("## Interpretation rules")
        output.append("")

        rule_number = 1

        for rule in interpretation_rules:
            if isinstance(rule, str) and rule.strip():
                output.append(f"{rule_number}. {rule.strip()}")
                rule_number += 1

        output.append("")

    if start_here:
        output.append("## Start here")
        output.append("")

        for entry in start_here:
            if not isinstance(entry, dict):
                continue

            path = entry.get("path")

            if not isinstance(path, str) or not path:
                continue

            if path in emitted_paths:
                continue

            label = page_label(
                path,
                entry.get("label"),
            )

            note = page_summary(
                path,
                entry.get("note"),
            )

            output.append(
                format_link(
                    path=path,
                    label=label,
                    note=note,
                )
            )

            emitted_paths.add(path)

        output.append("")

    for section in sections:
        if not isinstance(section, dict):
            continue

        heading = section.get("heading")
        topic_names = section.get("topics", [])

        if not isinstance(heading, str) or not heading.strip():
            continue

        if not isinstance(topic_names, list):
            continue

        section_lines: list[str] = []

        for topic_name in topic_names:
            topic = topics.get(topic_name)

            if not isinstance(topic, dict):
                continue

            primary = topic.get("primary")

            if isinstance(primary, str) and primary:
                if primary not in emitted_paths:
                    label = page_label(
                        primary,
                        topic.get("label"),
                    )

                    summary = page_summary(primary)

                    section_lines.append(
                        format_link(
                            path=primary,
                            label=label,
                            note=summary,
                        )
                    )

                    emitted_paths.add(primary)

            related_pages = topic.get("related", [])

            if not isinstance(related_pages, list):
                continue

            for related_path in related_pages:
                if not isinstance(related_path, str) or not related_path:
                    continue

                if related_path in emitted_paths:
                    continue

                if related_path in start_here_paths:
                    continue

                if related_path in reserved_primary_paths:
                    continue

                label = page_label(related_path)
                summary = page_summary(related_path)

                section_lines.append(
                    format_link(
                        path=related_path,
                        label=label,
                        note=summary,
                    )
                )

                emitted_paths.add(related_path)

        if section_lines:
            output.append(f"## {heading}")
            output.append("")
            output.extend(section_lines)
            output.append("")

    output.append("## Retrieval guidance")
    output.append("")
    output.append(
        "- Begin with the canonical topic page for a narrow question."
    )
    output.append(
        "- Load related pages only when the question crosses module "
        "boundaries or requires implementation detail."
    )
    output.append(
        "- Consult open-question pages before inferring behavior that is not "
        "explicitly documented."
    )
    output.append(
        "- Do not present recommended, mixed-page proposals, or unresolved "
        "behavior as implemented functionality."
    )
    output.append("")

    return "\n".join(output)


def write_llms_file() -> None:
    """Generate docs/llms.txt from docs/context-map.yaml."""

    context_map = load_context_map()
    generated_text = generate_llms_text(context_map)

    existing_text = None

    if LLMS_PATH.is_file():
        existing_text = LLMS_PATH.read_text(encoding="utf-8")

    if existing_text == generated_text:
        print("Hook: docs/llms.txt is already current")
        return

    LLMS_PATH.write_text(
        generated_text,
        encoding="utf-8",
    )

    print("Hook: regenerated docs/llms.txt")


def on_config(config, **kwargs):
    """
    MkDocs hook invoked after configuration is loaded.

    The generated file is written before MkDocs scans and builds the
    documentation site.
    """

    write_llms_file()

    return config


if __name__ == "__main__":
    write_llms_file()
