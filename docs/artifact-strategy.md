# Artifact Strategy

Build artifacts connect source code to deployable software.

## Goal

Every artifact should be traceable to the commit, pipeline run, and version
that produced it.

## Artifact Examples

- JAR files;
- Docker images;
- test reports;
- coverage reports;
- generated API documentation;
- deployment manifests.

## Recommended Practices

- Build once and promote the same artifact.
- Fingerprint artifacts when Jenkins supports it.
- Tag Docker images with commit SHA and release version.
- Archive test reports even when builds fail.
- Avoid rebuilding differently per environment.

## Review Questions

- Can we identify exactly what was deployed?
- Can we reproduce the artifact from source?
- Are artifacts stored long enough for debugging?
- Does rollback know which previous artifact was safe?

## Portfolio Signal

Artifact strategy shows that delivery is not just running commands. It is about
traceability, reproducibility, and operational confidence.
