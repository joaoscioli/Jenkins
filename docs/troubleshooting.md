# Jenkins Troubleshooting Guide

This guide documents a practical way to investigate failed Jenkins pipelines.
The goal is to debug failures methodically instead of guessing.

## Debugging Workflow

When a pipeline fails, inspect it in this order:

1. Identify the failed stage.
2. Read the first meaningful error in the console log.
3. Compare the failing command with the command used locally.
4. Check whether the failure is caused by code, configuration, credentials, or environment.
5. Fix the smallest cause and rerun the pipeline.

## Common Failure Types

### Tests Failed

Typical signs:

- the `Test` stage fails;
- JUnit reports show failed assertions;
- Maven exits with a test failure status.

How to investigate:

- open the Jenkins test report;
- identify the failing test class and method;
- reproduce locally with `./mvnw test`;
- fix the production code or the test expectation;
- rerun the pipeline.

Interview signal:

- a strong engineer treats failing tests as useful feedback, not noise.

### Maven Wrapper Not Found

Typical signs:

- the log shows `./mvnw: not found`;
- the repository does not contain Maven Wrapper files;
- the pipeline assumes Linux shell execution.

How to investigate:

- confirm that `mvnw`, `mvnw.cmd`, and `.mvn/wrapper` exist;
- verify file permissions for `mvnw`;
- use `sh 'chmod +x mvnw'` when needed;
- decide whether the pipeline should use Maven Wrapper or a Jenkins Maven tool.

Interview signal:

- build tooling should be reproducible from the repository whenever possible.

### Wrong Java Version

Typical signs:

- Maven compiler errors mention an unsupported release;
- Jenkins uses Java 17 while the project targets Java 21;
- tests pass locally but fail in CI.

How to investigate:

- check the JDK configured in Jenkins tools;
- confirm the project `pom.xml` compiler release;
- print `java -version` in the pipeline when debugging;
- align Jenkins tool configuration with the project target.

Interview signal:

- CI environments must match project requirements to avoid false failures.

### Missing Credentials

Typical signs:

- Docker login fails;
- deployment fails with access denied;
- the log references missing credentials IDs.

How to investigate:

- check the Jenkins credentials store;
- confirm the credential ID used by the pipeline;
- avoid printing secrets in logs;
- validate that the job has permission to read the credential.

Interview signal:

- secrets belong in Jenkins credentials or a secret manager, not in source code.

### Artifact Not Archived

Typical signs:

- the pipeline succeeds but no JAR appears in build artifacts;
- `archiveArtifacts` reports no matching files;
- the project uses a different packaging output path.

How to investigate:

- inspect the `target` directory after package;
- confirm whether the module is single-module or multi-module;
- adjust the artifact pattern;
- keep fingerprints enabled for traceability.

Interview signal:

- delivery pipelines should make build outputs visible and traceable.

## Good Debugging Questions

- Did this fail before or after tests ran?
- Is the error deterministic or intermittent?
- Can I reproduce it locally with the same command?
- Is this a code issue or a Jenkins configuration issue?
- Which pipeline assumption was wrong?

## Portfolio Note

This troubleshooting guide shows that CI/CD knowledge includes diagnosis,
environment awareness, and clear operational reasoning.
