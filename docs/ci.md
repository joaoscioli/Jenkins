# CI Workflow

This repository uses GitHub Actions for lightweight repository checks around
the Jenkins pipeline examples.

## What The Workflow Checks

- Every pipeline example has a `Jenkinsfile`.
- Each `Jenkinsfile` keeps the basic declarative pipeline structure:
  `pipeline`, `agent`, and `stages`.
- Core documentation files remain present.

## Why This Matters

GitHub Actions does not replace Jenkins in this repository. The goal is to use
it as a fast repository quality gate while Jenkins remains the subject of the
examples.

For portfolio review, this shows an important senior habit: the repository has
guardrails even when the main technology being studied is a different CI/CD
platform.

## Future Improvements

- Add Jenkinsfile linting against a real Jenkins controller.
- Add markdown link checks.
- Add examples that publish artifacts and test reports from Jenkins.
