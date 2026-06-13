# Production Deployment Notes

This document explains how production deployment should differ from development
or staging deployment.

## Production Principles

- Build artifacts should be created before deployment.
- The deployed artifact should be traceable to a commit.
- Secrets should come from Jenkins credentials or a secret manager.
- Production deployment should have rollback expectations.
- Health checks should run after deployment.
- Logs and metrics should be watched during rollout.

## Approval Gate

Manual approval is useful when:

- customer-facing behavior changes;
- database migrations are included;
- infrastructure changes are included;
- rollback requires coordination;
- the deployment window matters.

## Rollback Plan

A rollback plan should answer:

- what artifact was previously running;
- how to redeploy it;
- whether database changes are reversible;
- who approves rollback;
- which health checks confirm recovery.

## Interview Talking Points

- CI and CD are related but not identical.
- A build can be automatic while production release requires approval.
- Traceability matters because teams need to know what is running.
- Rollback planning is part of deployment design.
