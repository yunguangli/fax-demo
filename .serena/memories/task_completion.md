# Task Completion

No linter, formatter, or test runner is configured in pyproject.toml or CI. After code changes:

1. Verify syntax: `python -m py_compile src/<file>.py` for each modified file
2. If a linter is desired, ask user to add one (e.g. `ruff`, `mypy`)
