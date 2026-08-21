# Tough Interview Questions

Use these questions to prepare direct, technical answers.

## What risk does CI/CD reduce?

It reduces late feedback, inconsistent local builds, unclear failures, unsafe
credentials handling, and untraceable release artifacts.

## Should every pipeline auto-deploy?

No. Deployment automation should match risk. Production changes often need
approval gates, rollback plans, environment controls, and clear ownership.

## What makes a Jenkinsfile maintainable?

Readable stages, bounded runtime, clear credentials handling, useful artifacts,
and documentation that explains operational trade-offs.

## What would you defend in a code review?

Treating pipeline design as part of backend system reliability.
