# Technical Risks

This file captures the main risks in CI/CD pipeline design and how the project
plans to reduce them.

## Risks

- Slow pipelines can train teams to ignore feedback.
- Secrets can leak through logs or unsafe configuration.
- Missing artifact strategy can make releases hard to reproduce.
- Weak rollback planning can turn deployment into a high-risk event.

## Mitigations

- Keep early validation fast and visible.
- Use credentials management instead of hardcoded secrets.
- Archive build artifacts and publish test results.
- Document release and rollback decision points.

## Interview Angle

The strongest discussion is how pipeline design improves developer feedback,
release confidence, and operational recovery.
