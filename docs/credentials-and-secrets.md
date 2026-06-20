# Credentials And Secrets

Jenkins pipelines should never hardcode secrets in the repository.

## Goal

Credentials should be managed by Jenkins and injected into pipeline steps only
when needed.

## Examples Of Sensitive Values

- Docker registry passwords;
- cloud provider tokens;
- deployment SSH keys;
- database passwords;
- API keys;
- signing keys.

## Recommended Practice

- Store secrets in Jenkins Credentials.
- Reference credentials by id, not by raw value.
- Scope credentials to the smallest useful pipeline stage.
- Avoid printing secrets in logs.
- Rotate credentials when exposure is suspected.

## Example Shape

```groovy
withCredentials([string(credentialsId: 'docker-token', variable: 'DOCKER_TOKEN')]) {
    sh 'docker login --username "$DOCKER_USER" --password "$DOCKER_TOKEN"'
}
```

## Portfolio Signal

Secret handling is a senior engineering topic because it connects CI/CD,
security, operations, and team process. A pipeline that builds successfully but
leaks credentials is not production-ready.
