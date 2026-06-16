# Release Strategy

This document defines a simple release strategy for Jenkins-based Java backend
projects.

## Release Flow

1. Merge reviewed code into the release branch.
2. Run CI tests.
3. Package the application.
4. Build a traceable artifact or Docker image.
5. Run deployment checklist.
6. Request approval for production.
7. Deploy.
8. Verify health checks, logs, and metrics.

## Versioning Direction

Useful version identifiers:

- semantic version for public releases;
- commit SHA for traceability;
- build number for Jenkins run correlation;
- Docker image tag for deployment.

## Release Notes

Release notes should include:

- what changed;
- risk level;
- migration notes;
- rollback notes;
- validation performed.

## Interview Talking Points

- Release strategy connects CI, artifacts, approval, and operations.
- Traceability matters during incidents.
- Production releases should include rollback thinking.
- Release notes are engineering communication, not bureaucracy.
