# Developer Workflows

This is a documentation-only repo. Most standard workflows do not apply.

## Build

None. There is no code to compile or bundle.

## Test

No automated test suite. See `AGENTS.md` → "Test command exemption". Verification is by human review of profiles, the comparison matrix, and ADRs.

## Deploy

No deployment target. See `scripts/staging/README.md`.

## CI/CD

None. This repo is not gated by a pipeline.

## Local dev

```bash
# Fetch all candidate skills locally (clones into skills/, which is gitignored)
./scripts/fetch-candidates.sh

# Review a candidate: read its SKILL.md, write a profile
# Score it against docs/plans/rubric.md, update docs/plans/comparison-matrix.md
# Record the decision in docs/adr/
```

See `docs/agents-detail/project-navigation.md` for the full review workflow.