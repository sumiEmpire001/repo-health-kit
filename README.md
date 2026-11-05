# Repo Health Kit

A lightweight Python tool that checks whether a local repository includes basic project documentation and configuration.

## Requirements

Python 3.6 or newer. No third-party packages.

## Run

From the repository root:

```bash
python audit.py
```

The script checks for `README.md`, `.gitignore`, and `LICENSE` in the current directory and prints `OK` or `MISSING` for each. Missing files are reported for your attention; the script does not modify them.

## Limitations

This is an initial hygiene check, not a security scanner or a full code-quality audit. It checks only exact file names in the working directory.
