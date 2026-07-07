# Domain Events (Cross-Context)

Integration events that cross bounded context boundaries within the workspace.

## Events

### `CandidateFetched`

| Field | Value |
|---|---|
| Producing context | Review Process |
| Consuming context | Candidate Evaluation |
| Payload | `{ shortName, repoUrl, sha }` |
| Delivery | In-process (agent workflow) |
| Meaning | A candidate repo has been cloned into `skills/<short-name>/`. Triggers profiling. |

### `CandidateProfiled`

| Field | Value |
|---|---|
| Producing context | Candidate Evaluation |
| Consuming context | Review Process |
| Payload | `{ shortName, sha, profilePath }` |
| Delivery | In-process (agent workflow) |
| Meaning | A profile has been written at `comparison/profiles/<short-name>.md`. Triggers scoring. |

### `CandidateScored`

| Field | Value |
|---|---|
| Producing context | Candidate Evaluation |
| Consuming context | Review Process |
| Payload | `{ shortName, scores: { criterion: rating } }` |
| Delivery | In-process (agent workflow) |
| Meaning | The candidate's row in the comparison matrix is complete. Triggers a decision (ADR). |

### `DecisionRecorded`

| Field | Value |
|---|---|
| Producing context | Candidate Evaluation |
| Consuming context | Review Process |
| Payload | `{ shortName, adrId, decision: keep|reject|merge }` |
| Delivery | In-process (agent workflow) |
| Meaning | An ADR has been adopted. When enough candidates have decisions, triggers synthesis. |

### `RecommendationPublished`

| Field | Value |
|---|---|
| Producing context | Candidate Evaluation |
| Consuming context | Output Humanizer Skill (external) |
| Payload | `{ recommendationPath, summary }` |
| Delivery | File on disk (`comparison/recommendation.md`) |
| Meaning | The final synthesis is available for consumption by the output skill effort. |

## Notes

- All events are in-process within the agent workflow — there is no message bus.
- Internal domain events (within a single bounded context) belong in that context's narrative, not here.
- Event contract YAML specs live in `events/`.