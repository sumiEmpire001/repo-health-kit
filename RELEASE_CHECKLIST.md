# Release readiness checklist

## Verified by GitHub Actions

- [x] Unit tests on Python 3.9, 3.11 and 3.13
- [x] 100% statement-coverage gate for `audit.py`
- [x] Installable CLI smoke test
- [x] JSON and HTML output tests
- [x] Deterministic HTML example and downloadable artifact
- [x] Wheel and source distribution build, metadata validation, and wheel smoke test

These checks execute on pull requests and pushes to `main`. Always verify the latest run before announcing a release.

## Release blockers / decisions

- [x] **Choose and add a LICENSE.** The maintainer selected the MIT License; the repository includes the full license text.
- [ ] **Confirm release version and tag.** The current package version is `0.1.0`; no PyPI publication is configured.
- [ ] **Test installation on a real Windows machine** if Windows compatibility is to be advertised. CI currently runs on Ubuntu.
- [ ] **Decide whether to publish to PyPI.** The existing workflow builds artifacts only; it does not publish.

## Scope and limitations

This is a filename-based repository hygiene checker, not a vulnerability scanner, dependency auditor, or license-validity checker. It does not inspect file contents, nested directories, or Git history. A passing health report does not mean the project is secure or production-ready.

## Manual release verification

1. Download the latest successful GitHub Actions distribution and HTML artifacts.
2. Install the wheel into a clean virtual environment and run `repo-health --help`.
3. Run `repo-health --json .` and `repo-health --html .`.
4. Verify `repo-health --strict` returns 1 for an intentionally incomplete directory and 0 for one containing supported README, .gitignore, and LICENSE filenames.
5. Confirm the package metadata, version, MIT license notice, and changelog before creating a tag.
