# Releasing

A user-visible change landing on `main` triggers a release without waiting for a request. Versions follow [SemVer](https://semver.org/).

- **Releasable**: changes under `skills/`, `templates/`, `AGENTS.md`, `install.sh` that alter skill behavior, artifact structure, or lint results
- **Not releasable**: README or `docs/` wording, `tests/` only, `.gitignore`, `LICENSE`; they ride the next release
- **Bump** (`0.x`): new skill, rule, lint check, or template change is MINOR; an artifact format change that needs migration is MINOR plus an upgrade note in `README.md`; bug fix or wording fix is PATCH; mixed takes the largest
- **Version**: `VERSION` only; the tag `vX.Y.Z` mirrors it
- **Steps**
  1. `git fetch --tags`, then `git log vX.Y.Z..HEAD` to judge releasability and bump size
  2. `./release.sh X.Y.Z --dry-run` to run every check without writing
  3. `./release.sh X.Y.Z -m "<user-visible changes>"`: runs tests, commits `VERSION`, creates the annotated tag, pushes `main` and the tag together
  4. Consumers pin with `git -C methodology checkout vX.Y.Z`, then re-run `methodology/install.sh`
- **Forbidden**: moving or deleting a pushed tag, force push, releasing from a branch other than `main` or from a dirty tree
