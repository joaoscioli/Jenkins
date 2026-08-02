# Reviewer Scorecard

Use this scorecard to review the repository quickly during portfolio screening.

## Strong Signals

- Pipelines separate build, test, package, and quality feedback.
- Jenkinsfiles include timeouts and artifact handling.
- Secrets and credentials are treated as operational design concerns.
- Release, rollback, and troubleshooting notes show delivery maturity.

## Evidence

- `pipelines/java-maven/Jenkinsfile`
- `pipelines/docker-image/Jenkinsfile`
- `pipelines/spring-boot-quality-gates/Jenkinsfile`
- `docs/credentials-and-secrets.md`

## Next Senior Step

Add a compact before-and-after pipeline review example showing how a weak
pipeline becomes safer and easier to debug.
