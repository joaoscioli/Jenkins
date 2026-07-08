# Reviewer Guide

This guide helps a technical reviewer scan the CI/CD material and understand the
pipeline engineering signals in this repository.

## What To Review First

1. `README.md` for repository purpose.
2. `docs/pipeline-review-playbook.md` for review approach.
3. `docs/quality-gates.md` for quality criteria.
4. `docs/credentials-and-secrets.md` for security posture.
5. `pipelines/` for runnable Jenkinsfile examples.

## Strong Signals

- Pipelines are documented as delivery systems, not isolated scripts.
- Quality gates, artifacts, credentials, and rollback are treated explicitly.
- Examples separate build, test, packaging, and deployment responsibilities.
- Review checklists make operational risks visible.

## Interview Talking Points

- Explain why CI/CD design is also software architecture.
- Discuss how credentials should move through a pipeline safely.
- Show where quality gates prevent bad deployments.
