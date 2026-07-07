# C4 Component

Components inside the single container (the repo on disk).

```mermaid
flowchart TD
    Fetch["scripts/fetch-candidates.sh<br/>fetch candidate repos"]
    Profiles["docs/plans/profiles/<br/>per-candidate profiles"]
    Matrix["docs/plans/comparison-matrix.md<br/>scoring matrix"]
    Rubric["docs/plans/rubric.md<br/>scoring rubric"]
    ADRs["docs/adr/<br/>keep/reject/merge decisions"]
    Recommendation["docs/plans/recommendation.md<br/>final synthesis"]

    Fetch -->|"populates"| Skills["skills/<br/>(gitignored)"]
    Skills -->|"input to"| Profiles
    Rubric -->|"scores against"| Profiles
    Profiles -->|"feeds"| Matrix
    Matrix -->|"informs"| ADRs
    ADRs -->|"synthesizes into"| Recommendation
```

## Component responsibilities

| Component | Responsibility |
|---|---|
| `scripts/fetch-candidates.sh` | Clone candidate repos into `skills/<short-name>/` |
| `docs/plans/rubric.md` | Define scoring criteria |
| `docs/plans/profiles/<name>.md` | Per-candidate summary, SHA reviewed, feature inventory |
| `docs/plans/comparison-matrix.md` | Side-by-side scoring table |
| `docs/adr/` | Immutable decisions citing profiles + matrix |
| `docs/plans/recommendation.md` | Final synthesis once enough candidates are scored |