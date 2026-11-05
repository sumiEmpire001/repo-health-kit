# Repo Health Kit

[![Python tests](https://github.com/sumiEmpire001/repo-health-kit/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/sumiEmpire001/repo-health-kit/actions/workflows/python-tests.yml)

A lightweight Python tool that checks whether a local repository includes basic project documentation and configuration.

## Requirements

Python 3.9 or newer for the installable package. No third-party runtime packages are required; installing from source uses Python packaging tools.

## Install

Clone the repository, then from its root run:

```bash
python -m pip install .
```

You can now run the command from any working directory:

```bash
repo-health --help
repo-health --strict --json /path/to/repository
```

For development, use `python -m pip install -e .` instead. This package is installable from source; it has **not** been published to PyPI.

## Run

From the repository root:

```bash
python audit.py
```

Check another repository directory:

```bash
python audit.py /path/to/repository
```

Fail a CI job when required files are missing:

```bash
python audit.py --strict /path/to/repository
```

Combine strict mode with JSON output:

```bash
python audit.py --strict --json /path/to/repository
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

The script checks for a supported README (`README.md`, `README.rst`, `README.txt`, or `README`), `.gitignore`, and a supported license (`LICENSE`, `LICENSE.md`, `LICENSE.txt`, `LICENCE`, `LICENCE.md`, or `LICENCE.txt`) in the selected directory and prints `OK` or `MISSING` by default. JSON mode reports the same checks plus an overall `healthy` boolean. By default, missing files do not cause a nonzero exit status. With `--strict`, missing files return exit code **1**; a complete repository returns **0**. Invalid directories and arguments return **2** from argparse. Output format is unchanged by strict mode.

## Testing and coverage

Run the unit tests (no dependencies required):

```bash
python -m unittest discover -v
```

To measure coverage locally, install the optional developer dependency and run:

```bash
python -m pip install 'coverage>=7,<8'
python -m coverage run --source=audit -m unittest discover -v
python -m coverage report -m --fail-under=100
python -m coverage xml -o coverage.xml
```

GitHub Actions runs tests on Python 3.9, 3.11 and 3.13, and separately generates a coverage report on Python 3.11. Download `python-coverage-xml` from a completed workflow run's **Artifacts** section. CI requires **100% statement coverage** for `audit.py`; a lower result fails the coverage job. The coverage percentage measures executed lines in `audit.py`, not overall correctness.

## Package build verification

GitHub Actions also builds a wheel and source distribution on pull requests and pushes to `main`. The package workflow validates distribution metadata with Twine, installs the built wheel, smoke-tests the `repo-health` command outside the repository, and uploads both files as a workflow artifact. This is a build verification process, not an automatic PyPI release.

To build distributions locally:

```bash
python -m pip install 'build>=1,<2' 'twine>=5,<7'
python -m build
python -m twine check dist/*
```

## Limitations

This is an initial hygiene check, not a security scanner or a full code-quality audit. It checks only the listed filename variants in the selected directory; filename matching is case-insensitive on all supported filesystems. Only regular files count; directories with matching names do not.
