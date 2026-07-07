# C4 Context

## System context

```mermaid
flowchart LR
    Reviewer["Human reviewer & agents"]
    Workspace["humanizer-skill-review<br/>(this repo)"]
    Candidates["Candidate skill repos<br/>(GitHub, read-only)"]
    Output["~/code/output-humanizer-skill/<br/>(future personal skill)"]

    Reviewer -->|"fetch, score, decide"| Workspace
    Workspace -->|"git clone (read-only)"| Candidates
    Workspace -->|"inform selection/construction"| Output
```

## Actors

- **Human reviewer & agents** — consult the workspace to compare candidates and record decisions.

## External systems

- **Candidate skill repos** — public GitHub repos fetched into `skills/<short-name>/` (gitignored raw snapshots), then mirrored into the committed trove at `docs/troves/humanizer-skills/`.
- **`~/code/output-humanizer-skill/`** — the future personal humanizer skill that this workspace informs. Not part of this repo.