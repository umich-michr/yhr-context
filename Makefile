SHELL := /usr/bin/env bash

UV ?= uv
PYTHON := $(UV) run python
MKDOCS := $(UV) run mkdocs
PRE_COMMIT := $(UV) run pre-commit
PIP_AUDIT := $(UV) run pip-audit
MDFORMAT := $(UV) run mdformat
MARKDOWN_FILES := README.md $(shell find docs .github -type f -name '*.md' | sort)

.PHONY: help
.PHONY: lock sync setup hooks
.PHONY: generate validate build check test ci serve audit
.PHONY: clean distclean
.PHONY: upgrade upgrade-hooks outdated
.PHONY: format format-check

.DEFAULT_GOAL := help

help:
	@printf '%s\n' \
	  'YourHealthResearch.org context documentation' \
	  '' \
	  'Environment:' \
	  '  make lock          Create or update uv.lock' \
	  '  make sync          Create/update .venv from uv.lock' \
	  '  make setup         Sync dependencies and install Git hooks' \
	  '  make hooks         Install pre-commit and pre-push hooks' \
	  '' \
	  'Documentation:' \
	  '  make generate      Generate docs/llms.txt' \
	  '  make validate      Validate context routing and generated links' \
	  '  make format        Format Markdown documentation' \
	  '  make format-check  Check Markdown formatting without modifying files' \
	  '  make build         Validate and build site/' \
	  '  make check         Run the complete local/CI validation workflow' \
	  '  make test          Alias for make check' \
	  '  make serve         Run the local MkDocs development server' \
	  '  make audit         Audit Python dependencies for vulnerabilities' \
	  '' \
	  'Maintenance:' \
	  '  make upgrade        Upgrade locked Python dependencies and validate' \
	  '  make upgrade-hooks  Update pre-commit hook revisions and validate' \
	  '  make outdated       Show outdated Python dependencies' \
	  '' \
	  'Cleanup:' \
	  '  make clean         Remove generated documentation and caches' \
	  '  make distclean     Also remove .venv'

uv.lock: pyproject.toml
	$(UV) lock

format:
	$(MDFORMAT) $(MARKDOWN_FILES)

format-check:
	$(MDFORMAT) --check $(MARKDOWN_FILES)

lock:
	$(UV) lock

sync: uv.lock
	$(UV) sync --locked

hooks: sync
	$(PRE_COMMIT) install --hook-type pre-commit --hook-type pre-push

setup: sync hooks
	@printf '%s\n' \
	  'Environment ready.' \
	  'Run "make serve" to edit or "make check" to validate.'

upgrade-hooks: sync
	$(PRE_COMMIT) autoupdate
	$(PRE_COMMIT) run --all-files
	$(MAKE) check

outdated: sync
	$(UV) tree --outdated

upgrade:
	$(UV) lock --upgrade
	$(UV) sync --locked
	$(MAKE) check

generate: sync
	$(PYTHON) scripts/hooks.py

validate: sync
	$(PYTHON) scripts/validate_context_map.py
	$(PYTHON) scripts/hooks.py
	$(PYTHON) scripts/validate_llms_links.py

build: validate
	$(MKDOCS) build --strict

audit: sync
	$(PIP_AUDIT)

check: format-check build audit
	git diff --check

test: check

ci: check

serve: sync
	$(MKDOCS) serve

clean:
	rm -rf site
	rm -f docs/llms.txt
	rm -rf .pytest_cache .mypy_cache .ruff_cache
	rm -rf scripts/__pycache__
	rm -f scripts/*.pyc scripts/*.pyo

distclean: clean
	rm -rf .venv
