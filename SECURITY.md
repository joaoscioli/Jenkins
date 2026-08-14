# Security Policy

This repository contains CI/CD examples, so security concerns are especially
important around credentials, logs, artifacts, and deployment behavior.

## Supported Scope

Security feedback is welcome for:

- unsafe Jenkinsfile examples;
- credentials or secret handling issues;
- artifact or log exposure risks;
- dependency or build vulnerabilities;
- misleading release or deployment guidance.

## Reporting

Please do not open a public issue with sensitive details.

Send a private report to `joaoscioli@outlook.com` with the affected file, the
risk, and a suggested mitigation when possible.

## Security Expectations

- Secrets must live in Jenkins credentials or a secret manager, not in code.
- Logs should not expose tokens, passwords, or private environment values.
- Deployment examples should make approval and rollback expectations clear.
