# Architecture Review Checklist

Use this checklist to review the project's delivery architecture. Support each item with code, tests, configuration, or documentation.

## Pipeline Boundary

- [ ] Build, test, package, scan, and deploy stages have distinct responsibilities.
- [ ] Pipelines obtain credentials through approved secret mechanisms.
- [ ] Artifacts are traceable from commit to release candidate.

## Delivery Safety

- [ ] Quality gates fail early with actionable feedback.
- [ ] Production deployment defines approval, ownership, and rollback.
- [ ] Environment-specific behavior is explicit and reviewable.

## Operational Readiness

- [ ] Logs and metrics expose pipeline duration and failure points.
- [ ] Another engineer can repeat the release from documented steps.
- [ ] Security checks run in the delivery path and block unsafe releases.

## Architecture Defense

Be ready to explain how the pipeline supports safe delivery, the evidence that it works, and the next production risk to address.
