# {{label.title_deployment_standards}}

[Purpose: safe, repeatable releases with clear environment and pipeline patterns]

## {{label.philosophy}}
- Automate; test before deploy; verify after deploy
- Prefer incremental rollout with fast rollback
- Production changes must be observable and reversible

## {{label.environments}}
- Dev: fast iteration; debugging enabled
- Staging: mirrors prod; release validation
- Prod: hardened; monitored; least privilege

## {{label.ci_cd_flow}}
```
Code → Test → Build → Scan → Deploy (staged) → Verify
```
Principles:
- Fail fast on tests/scans; block deploy
- Artifact builds are reproducible (lockfiles, pinned versions)
- Manual approval for prod; auditable trail

## {{label.deployment_strategies}}
- Rolling: gradual instance replacement
- Blue-Green: switch traffic between two pools
- Canary: small % users first, expand on health
Choose per risk profile; document default.

## {{label.zero_downtime_migrations}}
- Health checks gate traffic; graceful shutdown
- Backwards-compatible DB changes during rollout
- Separate migration step; test rollback paths

## {{label.rollback}}
- Keep previous version ready; automate revert
- Rollback faster than fix-forward; document triggers

## {{label.configuration_secrets}}
- 12-factor config via env; never commit secrets
- Secret manager; rotate; least privilege; audit access
- Validate required env vars at startup

## {{label.health_monitoring}}
- Endpoints: `/health`, `/health/live`, `/health/ready`
- Monitor latency, error rate, throughput, saturation
- Alerts on SLO breaches/spikes; tune to avoid fatigue

## {{label.incident_response_dr}}
- Standard playbook: detect → assess → mitigate → communicate → resolve → post-mortem
- Backups with retention; test restore; defined RPO/RTO

<!-- Focus on rollout patterns and safeguards. No provider-specific steps. -->
