# Knowledgebase Index

This is the primary navigation root for planning and development.

## Source of Truth (Use in This Order)

1. Vision and product direction: `my-workspace/docs/vision.md`
2. Development workflow: `my-workspace/docs/DEVELOPMENT.md`
3. Technical progress tracker: `my-workspace/docs/STATUS.md`
4. Armory capability snapshot: `my-workspace/docs/armory/snapshot-2026-02-02/armory-summary.md`
5. Agent operating rules: `AGENTS.md`
6. Tooling quick reference: `skill.md`

## Core Docs

- GPU demo spec: `my-workspace/docs/gpu-spec.md`
- Personal roadmap: `my-workspace/docs/mani-plan.md`
- Full-flow competition demo plan: `competition/full-flow-demo-plan.md`
- Founder thesis reference: `competition/founder-thesis.md`
- Founder evidence artifacts: `competition/analysis/README.md`
- Mixed-signal founder evidence: `competition/mixed-signal-smoke-evidence.md`
- Competition evidence index: `competition/verification-evidence.md`
- Full-flow smoke evidence: `competition/full-flow-smoke-evidence.md`
- Competition video shot script: `competition/video-shot-script.md`
- Competition voiceover script: `competition/voiceover-script.md`
- Competition recording pack: `competition/recording-pack/README.md`
- Competition LaTeX workthrough: `competition/paper/README.md`

## Armory / Environment

- Armory index: `my-workspace/docs/armory/README.md`
- Latest snapshot: `my-workspace/docs/armory/snapshot-2026-02-02/armory-summary.md`
- Full raw capture: `my-workspace/docs/armory/snapshot-2026-02-02/raw/`

## Execution Records

- Session logs: `my-workspace/logs/`
- Tickets: `my-workspace/tickets/`
- Competition strategy docs: `competition/`

## Auditability References

- Build artifact policy: `results/README.md`
- Full-run logs/manifests: `results/_runlogs/`
- Hardening log: `my-workspace/logs/2026-02-02-audit-hardening.md`
- Coverage hardening log: `my-workspace/logs/2026-02-02-pe4-gpu-coverage-hardening.md`

## Repo Hygiene Rules

- Keep generated simulation waveforms/logs out of commits unless explicitly needed.
- Keep `results/*_test.txt` as the durable verification artifacts.
- Add new docs under `my-workspace/docs/` only when they are reusable references.
- Put time-stamped work notes in `my-workspace/logs/`.
