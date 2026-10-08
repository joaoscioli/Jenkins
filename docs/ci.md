# CI Workflow

This repository uses GitHub Actions for lightweight repository checks around
the Jenkins pipeline examples.

## What The Workflow Checks

- Every pipeline example has a `Jenkinsfile`.
- Each `Jenkinsfile` keeps the basic declarative pipeline structure:
  `pipeline`, `agent`, and `stages`.
- Each pipeline directory contains a Jenkinsfile, including newly added directories.
- Each example declares a timeout, skips implicit checkout, prevents concurrent
  builds and performs an explicit `checkout scm`.
- Core documentation files remain present.
- Every `scripts/*.sh` file passes `bash -n` syntax validation without execution.

Run the same checks locally with `bash scripts/check-repository.sh` (Git Bash
on Windows). The script resolves paths from its own location. Failures identify
both the missing guardrail and affected file. These are textual checks; they
cannot prove Groovy syntax or Jenkins plugin compatibility. The validation
Jenkinsfile provides the separate controller-based declarative validation.

The validation job runs the same repository guardrails after checkout and
before controller validation. Its agent needs a Unix shell and Bash. The
controller validates all four examples, including the validation Jenkinsfile
itself; validating that file parses its model without starting another build.
Configure the job to use `pipelines/validation/Jenkinsfile` from SCM. A failed
guardrail stops the job before declarative validation.

Run `python3 scripts/test-check-repository.py` to exercise isolated fixtures
for every missing guardrail, each required document, and a new pipeline without
a Jenkinsfile. The suite also checks successful execution from another working
directory. It requires Python 3 and Bash on PATH (use `python` from Git Bash on
Windows) and runs in GitHub Actions without a Jenkins controller.

The check job has a five-minute timeout and grants `GITHUB_TOKEN` only
`contents: read`. Repository validation needs checkout access without write
permissions. See the [GitHub Actions workflow syntax](https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax)
for token permissions and job runtime limits.

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
