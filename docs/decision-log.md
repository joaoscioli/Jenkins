# Decision Log

This log summarizes important technical choices in a review-friendly format.

## Decisions

| Decision | Reason | Trade-off |
| --- | --- | --- |
| Separate build, test, package, and deploy stages. | Makes pipeline feedback easier to diagnose. | More stages require clear naming and maintenance. |
| Treat credentials as pipeline-managed secrets. | Reduces accidental exposure in scripts and logs. | Local reproduction needs documented setup. |
| Include rollback and approval thinking. | Shows production safety beyond happy-path automation. | Adds process around risky deployments. |

## Interview Use

Use this file to explain how CI/CD choices affect release reliability,
traceability, and team ownership.
