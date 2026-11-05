# Repo Health Kit

[![Python tests](https://github.com/sumiEmpire001/repo-health-kit/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/sumiEmpire001/repo-health-kit/actions/workflows/python-tests.yml)

A lightweight Python tool that checks whether a local repository includes basic project documentation and configuration.

## Requirements

Python 3.6 or newer. No third-party packages are required to run the audit tool.

## Run

From the repository root:

```bash
python audit.py
```

Check another repository directory:

```bash
python audit.py /path/to/repository
```

Generate JSON for automation:

```bash
python audit.py --json /path/to/repository
```

Example JSON output:

```json
{
  "checks": {
    "README": true,
    "Git ignore": false,
    "License": true
  },
  "healthy": false
}
```

The script checks for `README.md`, `.gitignore`, and `LICENSE` in the selected directory and prints `OK` or `MISSING` by default. JSON mode reports the same checks plus an overall `healthy` boolean. Missing files do not cause a nonzero exit status; invalid directories and arguments do.

## Testing and coverage

Run the unit tests (no dependencies required):

```bash
python -m unittest discover -v
```

To measure coverage locally, install the optional developer dependency and run:

```bash
python -m pip install 'coverage>=7,<8'
python -m coverage run --source=audit -m unittest discover -v
python -m coverage report -m --fail-under=85
python -m coverage xml -o coverage.xml
```

GitHub Actions runs tests on Python 3.9, 3.11 and 3.13, and separately generates a coverage report on Python 3.11. Download `python-coverage-xml` from a completed workflow run's **Artifacts** section. CI requires at least **85% statement coverage** for `audit.py`; a lower result fails the coverage job. The coverage percentage measures executed lines in `audit.py`, not overall correctness.

## Limitations

This is an initial hygiene check, not a security scanner or a full code-quality audit. It checks only exact file names in the selected directory.
