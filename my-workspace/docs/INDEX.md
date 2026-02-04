# Knowledgebase Index

This is the primary navigation root for planning and development.

## Entry Trail

From repo entry points, the intended context trail is:
`CLAUDE.md` / `AGENTS.md` -> `my-workspace/README.md` -> this file.

## Canonical Context Trail (Single Source)

Use this exact order for agent bootstrap. Other docs should mirror this list.

1. `AGENTS.md`
2. `my-workspace/README.md`
3. `my-workspace/docs/INDEX.md`
4. `my-workspace/docs/vision.md`
5. `my-workspace/docs/DEVELOPMENT.md`
6. `my-workspace/docs/STATUS.md`
7. `my-workspace/docs/RANDEZVOUS.md`
8. `my-workspace/docs/armory/snapshot-2026-02-02/armory-summary.md`
9. `my-workspace/docs/reference/README.md` (secondary context)

## Source of Truth Precedence (When Docs Conflict)

1. Vision and product direction: `my-workspace/docs/vision.md`
2. Development workflow: `my-workspace/docs/DEVELOPMENT.md`
3. Technical progress tracker: `my-workspace/docs/STATUS.md`
4. Workspace operating loop: `my-workspace/docs/RANDEZVOUS.md`
5. Reference docs: `my-workspace/docs/reference/README.md`

## Tooling/Agent Quick References

- Agent operating rules: `AGENTS.md`
- Tooling quick reference: `skill.md`

## Core Docs

- Workspace rendezvous contract: `my-workspace/docs/RANDEZVOUS.md`
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

## References

- Reference docs index: `my-workspace/docs/reference/README.md`
- Cadence setup/troubleshooting notes: `my-workspace/docs/reference/Cadence/`

## Execution Records

- Session logs: `my-workspace/logs/`
- Tickets: `my-workspace/tickets/`
- Competition strategy docs: `competition/`

## Repo Hygiene Rules

- Keep generated simulation waveforms/logs out of commits unless explicitly needed.
- Keep `results/*_test.txt` as the durable verification artifacts.
- Add new docs under `my-workspace/docs/` only when they are reusable references.
- Put time-stamped work notes in `my-workspace/logs/`.
