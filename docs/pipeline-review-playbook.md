# Pipeline Review Playbook

This playbook helps review Jenkins pipelines with the same discipline used in
code review.

## Review Questions

- Does each stage have a clear purpose?
- Are tests executed before packaging or deployment?
- Are credentials referenced through Jenkins credentials instead of hardcoded
  values?
- Are artifacts versioned or fingerprinted?
- Can a failed stage be diagnosed from logs and published reports?
- Is deployment separated from build when manual approval is needed?
- Is there a rollback or recovery path?

## What A Reviewer Should Notice

A strong pipeline is readable, boring, and predictable. It should show the
delivery flow without hiding important behavior inside unclear shell scripts.

## Portfolio Signal

This document shows that CI/CD is treated as engineering design. The pipeline is
not only something that runs; it is something that can be reviewed, improved,
and trusted by a team.
