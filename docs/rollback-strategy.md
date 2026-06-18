# Rollback Strategy

This document explains how a Jenkins delivery workflow should handle failed or
unsafe releases.

## Goal

A deployment pipeline is not complete when it only knows how to move forward.
Production-minded delivery also needs a clear way to recover when a release
causes errors, performance degradation, or business risk.

## Rollback Triggers

A rollback may be needed when:

- health checks fail after deployment;
- error rate increases above the accepted threshold;
- latency increases for critical endpoints;
- database migration creates unexpected behavior;
- a manual smoke test fails;
- stakeholders identify a business-critical issue.

## Recommended Release Model

For portfolio-level Java and Spring Boot projects, a practical release model is:

1. Build the application artifact.
2. Run automated tests.
3. Build and tag the Docker image.
4. Deploy to staging.
5. Run smoke tests.
6. Promote the same artifact to production.
7. Monitor health checks and logs.

The same artifact should move between environments. Rebuilding for production
can hide differences and make rollback harder.

## Rollback Options

### Previous Image Tag

Redeploy the previous known-good Docker image tag.

This is usually the fastest rollback when the application package is the source
of the problem.

### Feature Flag Disablement

Disable the risky feature while keeping the deployment active.

This is useful when the infrastructure is healthy but one behavior needs to be
turned off quickly.

### Database Roll Forward

For database changes, prefer forward-compatible migrations. A risky migration
should have a mitigation path, such as adding a corrective migration instead of
manually editing production data.

## Jenkins Pipeline Responsibilities

The pipeline should make rollback easier by:

- keeping build artifacts traceable;
- tagging Docker images with commit SHA and version;
- recording the deployed version;
- exposing a manual rollback stage when appropriate;
- separating build, deploy, and promote steps;
- publishing deployment logs.

## Portfolio Signal

Rollback strategy shows delivery maturity. It tells reviewers that the engineer
does not think of CI/CD as only automation, but as a reliability practice.
