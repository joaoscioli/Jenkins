# Jenkins CI/CD Lab

> Portfolio status: active CI/CD learning lab.

This repository is being rebuilt as a practical Jenkins lab for Java and
Spring Boot delivery workflows. The goal is to document CI/CD concepts and
turn them into small, reproducible pipeline examples.

## Why This Repository Exists

Modern backend engineering is not only about writing application code. Strong
software engineers also understand how code is built, tested, packaged, and
delivered safely.

This lab focuses on Jenkins as a CI/CD tool and connects it to real backend
engineering practices:

- Maven builds;
- automated tests;
- pipeline stages;
- Docker-based delivery;
- artifact retention and runtime bounds;
- environment variables and credentials;
- release discipline;
- troubleshooting failed builds.

## Current Scope

The first version of this repository will focus on a Java and Spring Boot
pipeline.

Current sections:

- [Jenkins Fundamentals](docs/jenkins-fundamentals.md);
- [CI Workflow](docs/ci.md);
- [Jenkins Agent Strategy](docs/agent-strategy.md);
- [Artifact Strategy](docs/artifact-strategy.md);
- [Java Maven Pipeline](docs/java-maven-pipeline.md);
- [Pipeline Review Checklist](docs/pipeline-review-checklist.md);
- [Pipeline Review Playbook](docs/pipeline-review-playbook.md);
- [Docker Image Pipeline](docs/docker-image-pipeline.md);
- [Deployment Checklist](docs/deployment-checklist.md);
- [Environment Strategy](docs/environment-strategy.md);
- [Credentials And Secrets](docs/credentials-and-secrets.md);
- [CI Security Checklist](docs/ci-security-checklist.md);
- [Quality Gates](docs/quality-gates.md);
- [Production Deployment Notes](docs/production-deployment.md);
- [Release Strategy](docs/release-strategy.md);
- [Rollback Strategy](docs/rollback-strategy.md);
- [Spring Boot Delivery Notes](docs/spring-boot-delivery.md);
- [Troubleshooting Guide](docs/troubleshooting.md);
- [Repository Roadmap](docs/roadmap.md).

Pipeline examples:

- [Java Maven Pipeline](pipelines/java-maven/Jenkinsfile);
- [Docker Image Pipeline](pipelines/docker-image/Jenkinsfile);
- [Spring Boot Quality Gates Pipeline](pipelines/spring-boot-quality-gates/Jenkinsfile).

Planned sections:

- production deployment examples.

## Portfolio Role

This is a supporting repository in my backend portfolio. It complements the
main Java and Spring Boot projects by showing delivery awareness, CI/CD
discipline, and the ability to explain engineering workflows clearly.

## Interview Checkpoint

A reviewer should compare the Java Maven, Docker image, and Spring Boot quality
gate pipelines. They show build separation, test reports, artifact handling,
timeouts, credentials, and release discipline.

## Portfolio Proof

This repository proves delivery awareness. It shows that backend engineering
does not stop at code: build feedback, artifacts, credentials, and release
control are part of the system.

## Roadmap

- [x] Add a first declarative Jenkins pipeline for a Maven project.
- [x] Document each pipeline stage and its purpose.
- [x] Add a troubleshooting guide for common Jenkins failures.
- [x] Add a Docker-oriented pipeline example.
- [x] Add a deployment checklist.
- [x] Connect the examples to a Spring Boot API repository.

## Repository Principles

- Keep examples small and readable.
- Prefer practical pipeline snippets over abstract notes.
- Explain trade-offs in plain language.
- Preserve learning history while improving presentation quality.
- Use small commits with clear messages.
