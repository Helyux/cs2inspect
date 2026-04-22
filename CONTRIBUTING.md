# Contributing

Contributions are welcome! Here's how to get set up.

## Development Setup

```bash
# Install dependencies
pip install poetry
poetry install

# Enable automatic code formatting on commit
pre-commit install
```

## Running Tests

```bash
pytest tests/ -v
```

## Code Style

This project uses [ruff](https://github.com/astral-sh/ruff) for linting and formatting.
Code style is enforced automatically:

- **Locally**: `pre-commit install` enables auto-formatting on every commit.
- **CI**: PRs that don't pass `ruff check` / `ruff format --check` will fail.

To manually check and fix formatting:

```bash
ruff check --fix .
ruff format .
```

## Pull Requests

- All PRs must pass CI (lint + tests).
- Target the `dev` branch for new features, `main` for hotfixes.
