# Demo Evaluation Rubric

Use this rubric to evaluate a technical walkthrough of this project.

| Area | Strong Signal | Weak Signal |
| --- | --- | --- |
| Pipeline design | Explains build, test, package, scan, and deploy stages. | Shows a pipeline as a generic script. |
| Security | Describes safe credential handling and scan gates. | Stores secrets or ignores credential boundaries. |
| Release safety | Covers approvals, rollback, artifacts, and traceability. | Treats deployment as only pushing code. |
| Operations | Makes failures diagnosable and repeatable. | Leaves troubleshooting undocumented. |

## Passing Bar

A strong demo shows that CI/CD is part of engineering reliability, not only a
tooling detail.
