# Architecture

This is a documentation-only review workspace. There is no runtime, no container, no deployment. The "architecture" is the review process itself.

## C4 model

- **Context**: A human reviewer (and their agents) consult this repo to decide which humanizer skill to adopt or merge into a personal skill at `~/code/output-humanizer-skill/`. External systems are the candidate skill repos on GitHub (read-only git clones).
- **Container**: Single static artifact — a collection of markdown documents and shell scripts that fetch read-only git repos. No server, no database, no build step.
- **Component**: `scripts/fetch-candidates.sh` (fetch), `comparison/profiles/` (per-candidate profiles), `comparison/matrix.md` (scoring matrix), `docs/adr/` (decisions), `comparison/recommendation.md` (synthesis).
- **Deployment**: None. The repo is consumed directly on disk by humans and agents.

## Tech stack

- Shell scripts (POSIX-ish) for fetching candidate repos.
- Markdown for all artifacts.
- No runtime dependencies, no package manager, no build tool.

See `docs/technical-architecture/` for C4 diagrams and tech-stack detail.