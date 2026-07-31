# Demo Script

Use this short script to present the repository in a technical interview.

## 3-Minute Walkthrough

1. Start with the goal: Jenkins pipelines for Java and Spring Boot delivery.
2. Compare the Maven, Docker image, and quality-gate pipelines.
3. Explain how timeouts, artifacts, credentials, and stage separation reduce
   operational risk.
4. Close with the next step: a before-and-after pipeline review example.

## What To Emphasize

- CI/CD design is part of software architecture.
- Pipelines should fail early and explain why.
- Artifacts and logs are review tools, not only build outputs.

## Before The Interview

- Open one Jenkinsfile and explain each stage.
- Be ready to discuss where secrets should live.
- Prepare one example of a pipeline failure and how to debug it.

## Evidence To Open

- `pipelines/java-maven/Jenkinsfile`
- `pipelines/docker-image/Jenkinsfile`
- `pipelines/spring-boot-quality-gates/Jenkinsfile`
- `docs/pipeline-review-playbook.md`

## Avoid Saying

- "The pipeline deploys automatically." Instead, explain where approval is
  needed.
- "CI just runs tests." Instead, explain traceability from code to artifact.
