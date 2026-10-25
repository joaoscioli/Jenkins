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
- Concurrent builds queue with `disableConcurrentBuilds()` or explicit
  `abortPrevious: false`; aborting an active deployment fails the textual gate.
- Core documentation files remain present.
- `skipDefaultCheckout` uses `true` or its empty default; `false` fails the gate.
- Every `scripts/*.sh` file passes `bash -n` syntax validation without execution.

Run the same checks locally with `bash scripts/check-repository.sh` (Git Bash
on Windows). The script resolves paths from its own location. Failures identify
both the missing guardrail and affected file. Full-line `//` comments (including
indented comments) are ignored, so commenting out a guardrail fails the gate.
These are textual checks; block comments and string literals are not parsed. They
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

The Docker image example runs Maven `verify` before building or pushing an image.
The application stage always publishes Surefire reports, including when tests
fail, and missing reports fail the gate. The target application must contain
unit tests producing `target/surefire-reports/TEST-*.xml`. A failing application
stage prevents the later image stages from running.

After a successful application stage, the Docker example archives `target/*.jar`
and records Jenkins fingerprints so reviewers can trace the build artifact.
A missing JAR fails the archive step before image construction. The target Maven
project must produce a JAR directly under `target/`; adapt the glob for multi-module
projects. Fingerprints support traceability, not cryptographic artifact signing.
The Python suite checks this pipeline contract; executing the archive step still
requires a Jenkins controller and its artifact archiver.

The registry shell block uses `set -eu` so a failed login stops before `docker push`.
It rejects missing or empty image names, tags, usernames, and passwords before
running any Docker command. Offline Bash tests cover all eight unset/empty cases;
this prevents an incomplete environment from reaching registry authentication.
The push stage scopes `DOCKER_CONFIG` to the job's temporary workspace, avoiding
the shared agent's default Docker credentials. An EXIT trap logs out on both
success and failure, using the same isolated configuration. Logout failure is
best effort and preserves the original login/push result. The agent must isolate
workspaces between jobs; this is configuration isolation, not a security sandbox.
The Python suite executes that actual block with a shell function standing in for
Docker, checking failed login/push and logout paths without a registry or daemon.

The Spring Boot quality-gates example publishes Failsafe integration-test reports
in the integration stage's `post { always { ... } }`, including failed Maven runs.
Its target application's `integration-tests` profile must run Maven Failsafe and
produce `target/failsafe-reports/TEST-*.xml`; absent reports fail the gate rather
than silently accepting a profile that did not execute integration tests.

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
