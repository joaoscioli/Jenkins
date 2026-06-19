# Quality Gates

Quality gates are checks that must pass before code is merged, packaged, or
deployed.

## Goal

The pipeline should make engineering standards visible and repeatable. A strong
quality gate catches common problems early and gives reviewers more confidence
that the branch is safe to merge.

## Recommended Gates

- compile the project;
- run unit tests;
- publish test reports;
- run integration tests when the project defines them;
- package the application artifact;
- keep failed quality checks visible in the pull request.

## Pipeline Example

The repository includes a Spring Boot quality gate pipeline:

```text
pipelines/spring-boot-quality-gates/Jenkinsfile
```

The stages are intentionally simple:

- `Compile`;
- `Unit Tests`;
- `Integration Tests`;
- `Package`.

## Interview Talking Point

Quality gates show that CI/CD is not only a deployment mechanism. It is also a
team feedback system that protects the main branch and reduces manual review
burden.
