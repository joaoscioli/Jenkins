# Jenkins Fundamentals

This document explains the Jenkins concepts used by this repository.

## Pipeline

A pipeline describes how code moves from source control to a validated build
artifact.

Typical stages:

- checkout;
- test;
- package;
- build image;
- archive artifact;
- deploy or wait for approval.

## Agent

An agent is the machine or container where the pipeline runs.

Good pipeline design should make agent requirements explicit:

- Java version;
- Maven or Gradle;
- Docker availability;
- credentials access;
- network access.

## Stage

A stage groups a meaningful part of the workflow.

Good stages make failures easier to diagnose. A failed `Test` stage tells a
different story than a failed `Docker Build` stage.

## Artifact

An artifact is the output produced by a build.

Examples:

- JAR file;
- test report;
- Docker image;
- generated documentation.

Artifacts should be traceable to a commit and pipeline run.

## Credentials

Secrets should live in Jenkins credentials or a secret manager, never in Git.

Examples:

- registry username and password;
- deployment tokens;
- cloud provider credentials.

## Interview Talking Points

- CI validates every change before release.
- Pipelines should make failures easy to locate.
- Artifacts should be reproducible and traceable.
- Credentials do not belong in source code.
- Production deployment often needs approval and rollback planning.
