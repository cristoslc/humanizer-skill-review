# Domain Model L2 — Humanizer Skill Review

L2 ubiquitous language for developers and agents: entities, value objects, aggregates, ERDs, and invariants.

## ERD

```mermaid
erDiagram
    REVIEW ||--o{ CANDIDATE : evaluates
    REVIEW ||--|| RUBRIC : defines
    REVIEW ||--|| MATRIX : maintains
    REVIEW ||--o| RECOMMENDATION : produces
    CANDIDATE ||--o| PROFILE : summarized_by
    CANDIDATE ||--o{ ADR : decided_by
    RUBRIC ||--o{ CRITERION : contains
    MATRIX ||--o{ ROW : contains
    ROW }o--|| CANDIDATE : represents
    ROW ||--o{ SCORE : holds
    SCORE }o--|| CRITERION : rates

    REVIEW {
        string id PK
        date startDate
        date endDateNullable
    }
    CANDIDATE {
        string shortName PK
        string repoUrl
        string owner
        string repo
        string license
        date fetchedAt
        string shaReviewed
        string status "fetched|profiled|scored|decided"
    }
    PROFILE {
        string shortName PK_FK
        string path
        date updatedAt
    }
    RUBRIC {
        string id PK
        date version
    }
    CRITERION {
        string name PK
        string description
        int weight
    }
    MATRIX {
        string id PK
        date updatedAt
    }
    ROW {
        string shortName PK_FK
    }
    SCORE {
        string shortName PK_FK
        string criterion PK_FK
        string rating "low|med|high|n/a"
        string notes
    }
    ADR {
        string id PK "ADR-NNNN"
        string shortName FK
        string decision "keep|reject|merge"
        date adoptedAt
        string supersedesNullable
    }
    RECOMMENDATION {
        string id PK
        string path
        date publishedAt
    }
```

## Aggregates

### Review (root)

- Singleton. Owns the rubric, the matrix, and (eventually) the recommendation.
- Invariant: a recommendation cannot be published until enough candidates have adopted ADRs (threshold set by reviewer).

### Candidate (root)

- Identified by `shortName` (`<owner>-<repo>` lowercased, hyphenated).
- Owns exactly one profile (1:1) and zero or more ADRs (1:N — a candidate may be re-decided via supersession).
- Lifecycle: `fetched → profiled → scored → decided`. Status transitions are monotonic except supersession.
- Invariant: cannot be scored before profiled; cannot appear in an ADR before scored.
- Invariant: candidate source is never committed to this repo; only referenced by SHA.

### Rubric (root, owned by Review)

- Contains criteria. Each criterion has a name, description, and weight.
- Versioned as a whole — changing criteria produces a new rubric version and may invalidate prior scores.

### Matrix (root, owned by Review)

- Contains one row per candidate. Each row holds scores keyed by criterion.
- Row order is stable once scored; column order may change freely.

## Value objects

- **ShortName** — `<owner>-<repo>` lowercased, hyphenated. Used as identity for Candidate.
- **SHA** — a git commit SHA. References a specific version of a candidate's source.
- **Rating** — one of `low`, `med`, `high`, `n/a`. Stored per Score.
- **Decision** — one of `keep`, `reject`, `merge`. Stored per ADR.

## Invariants

1. A candidate cannot be scored before it is profiled.
2. A candidate cannot appear in an ADR before it is scored.
3. Candidate source code is never committed to this repo.
4. ADRs are immutable once adopted; supersede, don't edit.
5. Profiles are mutable; updated versions note the SHA reviewed.
6. The recommendation cannot be published until enough candidates have adopted ADRs.