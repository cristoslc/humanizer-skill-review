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
# Fetch all candidate skills (clones into skills/, then build the committed trove at docs/troves/humanizer-skills/)
./scripts/fetch-candidates.sh
python3 ./tests/harness/build-trove.py

# Review a candidate: read its SKILL.md, write a profile
# Score it against comparison/rubric.md, update comparison/matrix.md via the harness
# Record the decision in docs/adr/
```

See `docs/agents-detail/project-navigation.md` for the full review workflow.