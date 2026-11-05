# Repo Health Kit

A lightweight Python tool that checks whether a local repository includes basic project documentation and configuration.

## Requirements

Python 3.6 or newer. No third-party packages.

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

Run tests with:

```bash
python -m unittest -v
```

## Limitations

This is an initial hygiene check, not a security scanner or a full code-quality audit. It checks only exact file names in the selected directory.
