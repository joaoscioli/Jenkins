# Java Maven Pipeline

This pipeline is a first practical Jenkins example for Java and Spring Boot
repositories that use Maven Wrapper.

## Pipeline Goal

The goal is to prove that every change can be checked, tested, packaged, and
stored as a build artifact before it is considered ready for delivery.

## Stages

### Checkout

Fetches the source code from the configured repository.

Why it matters:

- Jenkins must build the same version that was reviewed in Git.
- The pipeline should be reproducible from source control.

### Test

Runs the automated test suite with Maven Wrapper:

```bash
./mvnw -B --no-transfer-progress test
```

Why it matters:

- tests catch regressions before packaging;
- `-B` keeps logs stable in CI;
- `--no-transfer-progress` makes output easier to read.

### Package

Builds the application artifact without rerunning tests:

```bash
./mvnw -B --no-transfer-progress package -DskipTests
```

Why it matters:

- tests already ran in the previous stage;
- packaging creates the deployable artifact;
- separating test and package stages makes failures easier to diagnose.

### Archive Artifacts

Stores generated JAR files as Jenkins build artifacts.

Why it matters:

- build outputs remain attached to the pipeline run;
- artifacts can be inspected later;
- artifact fingerprints help trace what was produced by a build.

## Jenkins Requirements

This example expects Jenkins to have:

- JDK 21 configured with the name `jdk-21`;
- Maven configured with the name `maven-3`;
- JUnit plugin available for test reports;
- a Java project with `mvnw` committed at the repository root.

## Interview Talking Points

- CI should fail fast when tests fail.
- Pipeline stages should explain where a failure happened.
- Build artifacts should be traceable.
- CI/CD is part of engineering quality, not an afterthought.
