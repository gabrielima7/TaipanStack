## Description

This PR syncs all project documentation, specifically the MkDocs site and the `README.md`, to accurately reflect the latest changes in the codebase.

### Changes Made
- Updated the total test count from `1315` to `1318` in the following files:
  - `README.md`
  - `docs/index.md`
  - `docs/architecture.md`
- Moved the `agents.md` file from the repository root into the `docs/` folder to ensure it correctly builds with MkDocs.
- Modified `mkdocs.yml` to reflect `agents.md` correctly linking it to the navigation.

### Validation
- **Documentation Build:** Successfully ran `poetry run mkdocs build --strict`. The build completed cleanly without any non-informational warnings or errors.
- **Test Suite:** Successfully ran `poetry run pytest`. All 1318 tests passed.
