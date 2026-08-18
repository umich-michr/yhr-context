from collections import Counter
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
DOCS_DIR = ROOT / "docs"
LLMS_FILE = DOCS_DIR / "llms.txt"


def extract_markdown_targets(text: str) -> list[str]:
    """
    Extract Markdown link targets without regular expressions.

    The generated llms.txt uses links in this form:

        - [Label](path/to/page.md): Optional summary
    """

    targets: list[str] = []

    for line_number, line in enumerate(text.splitlines(), start=1):
        search_from = 0

        while True:
            opening = line.find("](", search_from)

            if opening == -1:
                break

            target_start = opening + 2
            target_end = line.find(")", target_start)

            if target_end == -1:
                raise ValueError(
                    f"Malformed Markdown link on line {line_number}: "
                    f"missing closing parenthesis"
                )

            target = line[target_start:target_end].strip()

            if target:
                targets.append(target)

            search_from = target_end + 1

    return targets


def local_markdown_path(target: str) -> str | None:
    """
    Convert a Markdown target into a local documentation path.

    Removes:
    - Heading fragments
    - Optional query strings

    Ignores:
    - HTTP and HTTPS links
    - Mail links
    - Anchor-only links
    - Non-Markdown targets
    """

    lowered = target.lower()

    if lowered.startswith(
        (
            "http://",
            "https://",
            "mailto:",
            "tel:",
        )
    ):
        return None

    if target.startswith("#"):
        return None

    path_without_fragment = target.split("#", 1)[0]
    path_without_query = path_without_fragment.split("?", 1)[0]

    if not path_without_query.endswith(".md"):
        return None

    return path_without_query


def main() -> int:
    if not LLMS_FILE.is_file():
        print(
            f"llms.txt validation failed: missing {LLMS_FILE}",
            file=sys.stderr,
        )
        return 1

    text = LLMS_FILE.read_text(encoding="utf-8")

    try:
        all_targets = extract_markdown_targets(text)
    except ValueError as error:
        print(
            f"llms.txt validation failed: {error}",
            file=sys.stderr,
        )
        return 1

    markdown_targets = [
        path
        for target in all_targets
        if (path := local_markdown_path(target)) is not None
    ]

    errors: list[str] = []

    counts = Counter(markdown_targets)

    for target, count in sorted(counts.items()):
        if count > 1:
            errors.append(
                f"Duplicate target appears {count} times: {target}"
            )

    for target in sorted(set(markdown_targets)):
        target_path = DOCS_DIR / target

        if not target_path.is_file():
            errors.append(
                f"Link target does not exist: {target}"
            )

    if errors:
        print(
            "llms.txt validation failed:",
            file=sys.stderr,
        )

        for error in errors:
            print(
                f"- {error}",
                file=sys.stderr,
            )

        return 1

    print(
        "llms.txt contains "
        f"{len(markdown_targets)} unique, valid Markdown links."
    )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
