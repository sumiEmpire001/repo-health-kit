# Publishing Repo Health Kit to PyPI

The release workflow is intentionally **manual** and uses PyPI Trusted Publishing (GitHub Actions OIDC), not long-lived API tokens.

## One-time setup

1. Create or sign in to your account at https://pypi.org/ and enable two-factor authentication.
2. Confirm the `repo-health-kit` project name is available. A missing PyPI project page is not proof of availability; PyPI validates names when publishing.
3. On GitHub, open **Settings → Environments**, create an environment named exactly `pypi`, and add protection rules (at minimum restrict deployment to the `main` branch; requiring reviewer approval is recommended).
4. In your PyPI account, open **Publishing → Add a new pending publisher** (for a project not yet on PyPI), and enter:

   - PyPI project name: `repo-health-kit`
   - GitHub owner: `sumiEmpire001`
   - Repository: `repo-health-kit`
   - Workflow filename: `publish-pypi.yml`
   - Environment: `pypi`

   If the project already exists and you own it, configure a trusted publisher under that project's publishing settings instead.

5. Merge the publishing workflow after CI passes.
6. In GitHub **Actions → Publish to PyPI → Run workflow**, choose `main` and run it. Approve the `pypi` environment deployment if required. This will upload version `0.1.0` **only if that exact name/version is not already on PyPI**.
7. Verify https://pypi.org/project/repo-health-kit/ and install in a clean virtual environment:

   ```bash
   python -m pip install repo-health-kit==0.1.0
   repo-health --help
   ```

## Safety notes

- Never paste PyPI passwords or API tokens into GitHub, chat, or source files.
- PyPI does not permit replacing an already uploaded distribution for the same name/version. Increment the version before subsequent releases.
- The manual workflow builds from the selected branch; restrict the `pypi` GitHub environment to `main` to avoid publishing unreviewed changes.
- If the name is unavailable, choose another distribution name and update `pyproject.toml`, the workflow's project URL, and the PyPI pending publisher details consistently.
- The existing GitHub `v0.1.0` release does not automatically publish to PyPI.
