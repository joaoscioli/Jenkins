# Jenkins Agent Strategy

Agent strategy defines where pipeline work runs and what each agent needs.

## Goal

A pipeline should use agents that match the workload. Builds, tests, Docker
packaging, and deployments may need different tools and permissions.

## Common Agent Types

### Maven Build Agent

Needs:

- JDK;
- Maven or Maven Wrapper;
- access to dependency repositories;
- enough CPU and memory for test execution.

### Docker Build Agent

Needs:

- Docker engine or compatible build environment;
- registry credentials;
- disk cleanup policy;
- image tagging convention.

### Deployment Agent

Needs:

- deployment credentials;
- network access to the target environment;
- stricter access control;
- audit-friendly logs.

## Review Questions

- Does the agent have only the permissions it needs?
- Can the pipeline run on a clean agent?
- Are tools installed explicitly or assumed?
- Could concurrent builds interfere with each other?

## Portfolio Signal

Agent strategy shows that CI/CD design includes infrastructure thinking, not
only stage syntax.
