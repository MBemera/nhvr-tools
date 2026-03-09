# Contributing to NHVR Tools

Thanks for your interest in contributing! Here's how to get started.

## Setup

```bash
git clone https://github.com/MBemera/nhvr-tools.git
cd nhvr-tools
pip install -e ".[dev]"
```

## Running Tests

```bash
pytest
```

## Code Style

This project uses [Ruff](https://docs.astral.sh/ruff/) for linting and formatting:

```bash
ruff check .
ruff format .
```

## Making Changes

1. Fork the repo and create a branch from `main`
2. Make your changes
3. Add tests for new functionality
4. Run `pytest` and `ruff check .` to verify
5. Open a pull request

## Updating the Knowledge Base

The built-in data in `nhvr_mcp/knowledge.py` is sourced from the NHVR website and HVNL legislation. When updating:

- Cite the source URL or legislation reference
- Keep the dict structure consistent with existing entries
- Add tests in `tests/test_knowledge.py` for new entries

## Reporting Issues

Open an issue on GitHub with:

- What you expected to happen
- What actually happened
- Steps to reproduce
- Python version and OS
