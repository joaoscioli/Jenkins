# Interview Questions

Use these questions to prepare a CI/CD discussion.

## What should a good pipeline prove?

A good pipeline should prove that code can be built, tested, packaged, and
reviewed with clear feedback and traceable artifacts.

## Why are timeouts and artifacts important?

Timeouts prevent blocked builds from consuming resources indefinitely.
Artifacts preserve evidence that helps engineers review, debug, and release
software with more confidence.

## Where should secrets live?

Secrets should be managed by Jenkins credentials or a dedicated secret manager,
not hardcoded in Jenkinsfiles, shell scripts, logs, or repository files.

## What is the senior-level signal?

The senior signal is treating CI/CD as part of system design: fast feedback,
clear ownership, controlled release gates, rollback thinking, and secure
credential handling.
