# Technical Debt Register

This register makes project trade-offs visible instead of hiding unfinished work.

## Current Debt

| Area | Debt | Impact | Next Action |
| --- | --- | --- | --- |
| Runtime Demo | Some flows are documented more than executed. | Reviewers may ask for runnable validation. | Add a minimal sample app pipeline. |
| Security Gates | Security checklist exists before all automated scans. | Manual review still carries part of the load. | Add dependency and image scan examples. |
| Deployments | Production strategy is modeled, not connected to a live environment. | Release path is conceptual. | Add a staging deployment example. |

## Review Rule

Debt is acceptable when it is explicit, bounded, and connected to a follow-up
decision. Hidden debt is what damages engineering trust.
