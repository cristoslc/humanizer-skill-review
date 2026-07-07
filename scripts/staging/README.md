# Staging

No staging target exists for this repo.

## Why

This is a documentation-only review workspace. It produces no executable code, no library, and no deployable artifact. There is nothing to stage or deploy.

## Alternative validation

Verification is by human review of:
- Candidate profiles (`comparison/profiles/`)
- The comparison matrix (`comparison/matrix.md`)
- Architecture decision records (`docs/adr/`)

The only shell scripts (`scripts/fetch-candidates.sh`, `scripts/build-matrix.sh`) are read-only git operations and markdown generation. They are validated by running them locally.

See `~/.agents/agents-md-detail/two-stage-pipelines.md` → "For projects that cannot deploy to an external target" for the rationale.