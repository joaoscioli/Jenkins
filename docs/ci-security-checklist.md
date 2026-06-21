# CI Security Checklist

This checklist helps review Jenkins pipelines from a security perspective.

## Checklist

- Secrets are stored in Jenkins Credentials.
- Secrets are not printed in logs.
- Build agents do not reuse production-only credentials.
- Deployment stages require approval when the target environment is sensitive.
- Pull request builds do not receive production secrets.
- Artifacts are traceable to a commit SHA.
- Docker image tags are deterministic.
- Failed builds do not leave partial deployments running.

## Why This Matters

CI/CD systems often have access to source code, credentials, artifacts, and
deployment targets. That makes pipeline security part of application security.

## Interview Talking Point

A mature engineer can discuss not only how to make a pipeline pass, but also how
to prevent the pipeline from becoming a security risk.
