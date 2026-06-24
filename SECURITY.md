# Security Policy

This repository is a CI/CD lab. Security review is important because pipeline
examples often touch credentials, artifacts, environments, and deployment flow.

## Supported Scope

Security review focuses on:

- credentials handling in Jenkinsfiles;
- unsafe shell commands in pipeline examples;
- artifact publishing and retention risks;
- environment variable exposure;
- deployment and rollback guidance.

## Reporting A Security Concern

Open a concise issue describing the affected pipeline or document. Do not post
real credentials, tokens, internal URLs, or private deployment details.

## Development Practices

- Use Jenkins credentials binding for secrets.
- Avoid printing sensitive values in logs.
- Keep deployment examples explicit about safety gates.
