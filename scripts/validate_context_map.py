from collections import Counter
from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
CONTEXT_MAP_PATH = DOCS_DIR / "context-map.yaml"


def load_context_map() -> dict:
    with CONTEXT_MAP_PATH.open("r", encoding="utf-8") as stream:
        data = yaml.safe_load(stream)

    if not isinstance(data, dict):
        raise ValueError(
            "context-map.yaml must contain a YAML mapping at its root."
        )

    return data


def validate_file_references(
    value,
    location: str,
    errors: list[str],
) -> None:
    """
    Recursively validate documentation paths referenced in the YAML map.
    """

    if isinstance(value, str) and value.endswith((".md", ".txt")):
        target = DOCS_DIR / value

        if not target.is_file():
            errors.append(
                f"{location}: missing file: {value}"
            )

        return

    if isinstance(value, dict):
        for key, child in value.items():
            validate_file_references(
                child,
                f"{location}.{key}",
                errors,
            )

        return

    if isinstance(value, list):
        for index, child in enumerate(value):
            validate_file_references(
                child,
                f"{location}[{index}]",
                errors,
            )


def validate_topics(
    data: dict,
    errors: list[str],
) -> None:
    topics = data.get("topics")

    if not isinstance(topics, dict):
        errors.append(
            "context-map.topics must be a YAML mapping."
        )
        return

    for topic_name, topic in topics.items():
        location = f"context-map.topics.{topic_name}"

        if not isinstance(topic, dict):
            errors.append(
                f"{location} must be a YAML mapping."
            )
            continue

        primary = topic.get("primary")

        if not isinstance(primary, str) or not primary:
            errors.append(
                f"{location}.primary must be a non-empty path."
            )

        label = topic.get("label")

        if label is not None and not isinstance(label, str):
            errors.append(
                f"{location}.label must be a string when present."
            )

        related = topic.get("related", [])

        if not isinstance(related, list):
            errors.append(
                f"{location}.related must be a list when present."
            )
            continue

        duplicate_related = [
            path
            for path, count in Counter(related).items()
            if count > 1
        ]

        for duplicate in sorted(duplicate_related):
            errors.append(
                f"{location}.related contains duplicate path: "
                f"{duplicate}"
            )

        if primary in related:
            errors.append(
                f"{location}.related repeats its primary path: "
                f"{primary}"
            )


def validate_sections(
    data: dict,
    errors: list[str],
) -> None:
    topics = data.get("topics", {})
    sections = data.get("sections")

    if not isinstance(sections, list):
        errors.append(
            "context-map.sections must be a YAML list."
        )
        return

    for section_index, section in enumerate(sections):
        location = f"context-map.sections[{section_index}]"

        if not isinstance(section, dict):
            errors.append(
                f"{location} must be a YAML mapping."
            )
            continue

        heading = section.get("heading")

        if not isinstance(heading, str) or not heading.strip():
            errors.append(
                f"{location}.heading must be a non-empty string."
            )

        topic_names = section.get("topics")

        if not isinstance(topic_names, list):
            errors.append(
                f"{location}.topics must be a list."
            )
            continue

        duplicate_topics = [
            topic_name
            for topic_name, count in Counter(topic_names).items()
            if count > 1
        ]

        for duplicate in sorted(duplicate_topics):
            errors.append(
                f"{location}.topics repeats topic: {duplicate}"
            )

        for topic_index, topic_name in enumerate(topic_names):
            if topic_name not in topics:
                errors.append(
                    f"{location}.topics[{topic_index}] "
                    f"references undefined topic: {topic_name}"
                )


def validate_start_here(
    data: dict,
    errors: list[str],
) -> None:
    entries = data.get("start_here")

    if not isinstance(entries, list):
        errors.append(
            "context-map.start_here must be a YAML list."
        )
        return

    paths: list[str] = []

    for index, entry in enumerate(entries):
        location = f"context-map.start_here[{index}]"

        if not isinstance(entry, dict):
            errors.append(
                f"{location} must be a YAML mapping."
            )
            continue

        path = entry.get("path")

        if not isinstance(path, str) or not path:
            errors.append(
                f"{location}.path must be a non-empty string."
            )
            continue

        paths.append(path)

    duplicate_paths = [
        path
        for path, count in Counter(paths).items()
        if count > 1
    ]

    for duplicate in sorted(duplicate_paths):
        errors.append(
            f"context-map.start_here contains duplicate path: "
            f"{duplicate}"
        )


def main() -> int:
    errors: list[str] = []

    if not CONTEXT_MAP_PATH.is_file():
        print(
            f"Context-map validation failed: "
            f"missing {CONTEXT_MAP_PATH}",
            file=sys.stderr,
        )
        return 1

    try:
        data = load_context_map()
    except (OSError, ValueError, yaml.YAMLError) as error:
        print(
            f"Context-map validation failed: {error}",
            file=sys.stderr,
        )
        return 1

    validate_file_references(
        data,
        "context-map",
        errors,
    )
    validate_topics(data, errors)
    validate_sections(data, errors)
    validate_start_here(data, errors)

    if errors:
        print(
            "Context-map validation failed:",
            file=sys.stderr,
        )

        for error in errors:
            print(
                f"- {error}",
                file=sys.stderr,
            )

        return 1

    print(
        "context-map.yaml structure and file references are valid."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
