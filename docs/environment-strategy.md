# Environment Strategy

This document describes how CI/CD pipelines should treat different deployment
environments.

## Environment Types

### Development

Purpose:

- fast feedback;
- frequent deployments;
- early integration checks.

Deployment can usually be automatic.

### Staging

Purpose:

- production-like validation;
- release candidate testing;
- smoke tests;
- stakeholder review.

Deployment may be automatic after CI, depending on team maturity.

### Production

Purpose:

- serve real users;
- protect business continuity;
- preserve data integrity.

Deployment should include approval, health checks, observability, and rollback
expectations.

## Configuration Rules

- keep secrets out of Git;
- use environment variables or secret managers;
- document required variables;
- avoid changing artifacts per environment;
- prefer promoting the same artifact through environments.

## Interview Talking Points

- Environments have different risk profiles.
- The same artifact should move through environments when possible.
- Configuration changes should be explicit.
- Production needs approval and rollback thinking.
