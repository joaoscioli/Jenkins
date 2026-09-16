# Implementation Priority

This file defines the next implementation order for turning the repository into
a stronger CI/CD portfolio.

## P1: Runnable Java Pipeline

- Add a minimal Maven build pipeline.
- Publish test results.
- Archive the build artifact.
- Fail fast on compilation or test errors.

## P2: Release Confidence

- Add quality gate documentation near the pipeline.
- Document artifact promotion expectations.
- Define manual approval points for risky environments.

## P3: Operational Recovery

- Add rollback notes to the delivery flow.
- Document troubleshooting for common pipeline failures.
- Connect deployment checks to release readiness.

## Why This Order

The repository should prove delivery feedback first. A clear pipeline matters
most when it helps developers understand failures quickly and release safely.
