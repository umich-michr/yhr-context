"""
MkDocs event hook: regenerate docs/llms.txt from docs/context-map.yaml
before every build (mkdocs build and mkdocs serve).

Registered in mkdocs.yml under the `hooks:` key:

    hooks:
      - scripts/hooks.py
"""

import sys
from pathlib import Path


def on_pre_build(config) -> None:  # noqa: ANN001
    """Called by MkDocs before the build starts."""
    # Add the repo root to sys.path so the script can be imported directly.
    repo_root = Path(__file__).parent.parent
    if str(repo_root) not in sys.path:
        sys.path.insert(0, str(repo_root))

    from scripts.generate_llms_txt import load_yaml, validate, generate, OUTPUT

    data = load_yaml()
    errors = validate(data)
    if errors:
        joined = "\n".join(errors)
        raise SystemExit(
            f"context-map.yaml validation failed — fix these before building:\n{joined}"
        )

    content = generate(data)
    OUTPUT.write_text(content, encoding="utf-8")
    print(f"Hook: regenerated {OUTPUT.relative_to(repo_root)}")
