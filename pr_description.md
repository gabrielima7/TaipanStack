## Description

This PR fixes multiple inconsistencies in documentation regarding test counts. The test count was mistakenly referenced as `1347`, `1318` and `1315` across the site and documentation instead of `1334`. The correct test amount was unified across:
- `CHANGELOG.md`
- `README.md`
- `docs/architecture.md`
- `docs/index.md`
- `docs/releases/v0.4.8.md`

I additionally removed a duplicated line in `docs/architecture.md` and `docs/index.md` regarding test counts and the coverage report, respectively.

## Checks

- Ran `mkdocs build --strict` which resulted in an error-free successful build.
- Ran `make all` and verified all 1334 tests passed and coverage reached 100%. No architectural checks failed.
