# Pipeline Review Checklist

Use this checklist before treating a Jenkins pipeline as portfolio-ready.

## Structure

- stages have clear names;
- each stage has one main responsibility;
- failures are easy to locate;
- commands use reproducible project tooling;
- artifacts are archived when useful.

## Safety

- credentials are not committed to Git;
- secrets are read from Jenkins credentials or a secret manager;
- production deployment has an approval path;
- rollback expectations are documented;
- destructive steps are explicit.

## Reliability

- tests run before packaging;
- packaging runs before image build;
- generated reports are published;
- image tags are traceable;
- logs are readable.

## Maintainability

- pipeline assumptions are documented;
- required tools are named;
- environment variables are explained;
- duplicated shell scripts are avoided;
- failure troubleshooting is documented.

## Interview Talking Points

- A pipeline should be understandable under pressure.
- CI should fail before release when quality gates fail.
- Secrets and production approvals are part of engineering discipline.
- Traceability connects code, build, artifact, and deployment.
