# docs/

Review and comparison workspace for humanizer agent skills. The tree splits into two architectural surfaces plus cross-cutting hubs.

## Technical architecture (how the workspace is built)

- `ARCHITECTURE.md` — C4 model references (system context, containers, components, deployment), tech stack per container, deployment topology.
- `technical-architecture/` — spoke directory for `ARCHITECTURE.md` (C4 diagrams, tech-stack detail).

## Domain architecture (what the workspace means)

- `DOMAIN-MODEL-L1.md` — L1 prose glossary of domain terms, aggregate narratives, conceptual groupings.
- `domain-architecture/` — spoke directory: `CONTEXT-MAP.md` (bounded context relationships), `DOMAIN-EVENTS.md` (cross-context integration events), `DOMAIN-MODEL-L2.md` (L2 ubiquitous language with ERDs and invariants), `events/` (event contract YAML specs).

## Cross-cutting

- `DEVELOPER-WORKFLOWS.md` — build, test, deploy, CI/CD, local dev (none apply; this is a docs-only repo).
- `USER-EXPERIENCE.md` — UI conventions, user journeys (none; no UI).
- `AGENTS.md` (at repo root) — project-specific agent guidance; spokes in `agents-detail/`.
- `adr/` — numbered decision records (immutable once adopted; supersede, don't edit).
- `plans/` — implementation plans, candidate profiles, rubric, comparison matrix, recommendation.
- `musings/` — pre-artifact thought capture (freeform markdown).
- `retros/` — post-session reflection docs from the Retro ritual.
- `tech-debt/` — pre-existing LSP errors and other tech debt (none expected in a docs repo).

Read the hub first, then drill into spokes when you need detail.