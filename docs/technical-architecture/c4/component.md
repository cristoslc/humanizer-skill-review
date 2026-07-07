# C4 Component

Components inside the single container (the repo on disk).

```mermaid
flowchart TD
    Fetch["scripts/fetch-candidates.sh<br/>fetch candidate repos"]
    Profiles["comparison/profiles/<br/>per-candidate profiles"]
    Matrix["comparison/matrix.md<br/>scoring matrix"]
    Rubric["comparison/rubric.md<br/>scoring rubric"]
    ADRs["docs/adr/<br/>keep/reject/merge decisions"]
    Recommendation["comparison/recommendation.md<br/>final synthesis"]

    Fetch -->|"populates"| Skills["skills/<br/>(gitignored raw)"]
    Skills -->|"mirrors into"| Trove["docs/troves/humanizer-skills/<br/>(committed)"]
    Trove -->|"input to"| Profiles
    Rubric -->|"scores against"| Profiles
    Profiles -->|"feeds"| Matrix
    Matrix -->|"informs"| ADRs
    ADRs -->|"synthesizes into"| Recommendation
```

## Component responsibilities

| Component | Responsibility |
|---|---|
| `scripts/fetch-candidates.sh` | Clone candidate repos into `skills/<short-name>/` (raw, gitignored) |
| `tests/harness/build-trove.py` | Mirror raw clones into committed trove at `docs/troves/humanizer-skills/` |
| `comparison/rubric.md` | Define scoring criteria |
| `comparison/profiles/<name>.md` | Per-candidate summary, SHA reviewed, feature inventory |
| `comparison/matrix.md` | Side-by-side scoring table |
| `comparison/recommendation.md` | Final synthesis once enough candidates are scored |