# Docker Image Pipeline

This pipeline demonstrates how Jenkins can build and optionally push a Docker
image for a Java or Spring Boot application.

## Pipeline Goal

The goal is to separate application packaging from container image delivery.
A successful run proves that Jenkins can create an immutable image candidate
from the source code.

The pipeline also uses a global timeout and explicit checkout so stalled Docker
builds do not consume agents indefinitely.

## Stages

### Checkout

Fetches the source code from Git.

Why it matters:

- the image must be built from versioned source code;
- the build can be traced back to a commit.

### Build Application

Packages the Java application:

```bash
./mvnw -B --no-transfer-progress package -DskipTests
```

Why it matters:

- Docker should receive a compiled artifact;
- packaging failures are isolated before the Docker build starts.

### Build Docker Image

Builds a Docker image tagged with the Jenkins build number:

```bash
docker build -t $IMAGE_NAME:$IMAGE_TAG .
```

Why it matters:

- each build gets a unique image tag;
- the image can be traced to a pipeline execution;
- the Dockerfile becomes part of the delivery contract.

### Inspect Image

Runs `docker image inspect` to verify the image exists and expose metadata.

Why it matters:

- Jenkins confirms the image was created;
- logs include image metadata for debugging.

### Push Docker Image

Pushes the image only when the `PUSH_IMAGE` parameter is enabled.

Why it matters:

- local validation and registry publishing are separate decisions;
- accidental pushes are avoided;
- credentials stay managed by Jenkins.

## Jenkins Requirements

This example expects Jenkins to have:

- Docker available on the build agent;
- permission to run Docker commands;
- a project with a valid `Dockerfile`;
- a credential named `docker-registry-credentials` when image push is enabled.

## Security Notes

- never commit registry passwords to Git;
- use Jenkins credentials or a secret manager;
- avoid printing secrets in logs;
- prefer immutable tags for release images;
- treat `latest` as a convenience tag, not a deployment guarantee.

## Interview Talking Points

- CI can build images without always deploying them.
- Image tags should be traceable to pipeline runs or commits.
- Registry credentials belong outside source control.
- Build and deploy stages should be separated when release control matters.
