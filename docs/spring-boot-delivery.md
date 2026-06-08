# Spring Boot Delivery Notes

This document connects the Jenkins CI/CD lab to a realistic Spring Boot
portfolio project: `subscription-billing-api`.

## Target Repository

The Jenkins examples are designed to be applied to a Spring Boot API with:

- Java 21;
- Maven Wrapper;
- automated tests;
- Docker Compose for local dependencies;
- Spring Boot Actuator;
- OpenAPI documentation;
- quality gates documented in the repository.

In this portfolio, the main target project is:

- `joaoscioli/subscription-billing-api`

## Recommended Pipeline Flow

For a Spring Boot API, the first Jenkins delivery flow should be:

1. Checkout source code.
2. Run automated tests.
3. Package the application.
4. Archive the generated JAR.
5. Build a Docker image.
6. Inspect the image.
7. Push the image only when release conditions are met.

This flow separates build confidence from release approval.

## What Jenkins Should Prove

The pipeline should prove that:

- the project compiles with the expected Java version;
- tests run without depending on a developer machine;
- the generated artifact is traceable;
- the application can become a Docker image;
- secrets are not stored in source control;
- release actions can be controlled with parameters or approvals.

## Suggested Jenkinsfile Mapping

Use these lab files as starting points:

- [Java Maven Pipeline](../pipelines/java-maven/Jenkinsfile);
- [Docker Image Pipeline](../pipelines/docker-image/Jenkinsfile).

For `subscription-billing-api`, the Maven commands should use Maven Wrapper:

```bash
./mvnw -B --no-transfer-progress test
./mvnw -B --no-transfer-progress package -DskipTests
```

On Windows agents, the equivalent commands would use:

```powershell
.\mvnw.cmd -B --no-transfer-progress test
.\mvnw.cmd -B --no-transfer-progress package -DskipTests
```

## Health and Observability Checks

After deployment, Jenkins or a deployment tool should verify:

- `/actuator/health`;
- startup logs;
- expected environment variables;
- database connectivity;
- API documentation availability at `/swagger-ui.html`;
- metrics emission when observability is enabled.

## Interview Talking Points

- A portfolio API is stronger when it includes delivery thinking.
- CI/CD should validate code, packaging, and operational readiness.
- Actuator health checks connect application code with deployment confidence.
- Pipeline examples are more valuable when they are tied to a real project.
