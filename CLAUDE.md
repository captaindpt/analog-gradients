# CLAUDE.md

Context for Claude Code in this repository.

## Context Trail (Read in Order)

1. `AGENTS.md` (repo-level agent operating rules)
2. `my-workspace/README.md` (workspace map)
3. `my-workspace/docs/INDEX.md` (navigation root)
4. `my-workspace/docs/vision.md` (mission + success criteria)
5. `my-workspace/docs/DEVELOPMENT.md` (execution workflow)
6. `my-workspace/docs/STATUS.md` (current state + blockers)
7. `my-workspace/docs/armory/snapshot-2026-02-02/armory-summary.md` (tooling ceiling)

If documents conflict, treat that order as precedence.

## What This Is

Testbed for AI-driven hardware design with Cadence Spectre on CMC Cloud.
Build bottom-up from transistor primitives to system-level netlists.
Current mission: extend the stack toward a neuromorphic analog compute core.

## Source of Truth

- Knowledgebase navigation: `my-workspace/docs/INDEX.md`
- Vision and direction: `my-workspace/docs/vision.md`
- Development workflow: `my-workspace/docs/DEVELOPMENT.md`
- Technical progress: `my-workspace/docs/STATUS.md`
- Agent workflow details: `AGENTS.md`
- Armory capabilities: `my-workspace/docs/armory/snapshot-2026-02-02/armory-summary.md`
- Reference docs (secondary context): `my-workspace/docs/reference/README.md`

## Current Verified Stack

- Level 5: inverter, nand2, nor2
- Level 4: and2, or2, xor2, xnor2
- Level 3: mux2, half_adder, full_adder
- Level 2: alu1, alu4
- Level 1: pe1, pe4
- Level 0: gpu_core

## Current Development Focus

- Preserve strict, fail-closed verification credibility
- Expand neuromorphic compute evidence (robustness + benchmark quality)
- Keep implementation-flow path reproducible toward manufacturable pre-silicon package

## Repo Layout

```
analog-gradients/
├── netlists/             # Spectre netlists
├── ocean/                # OCEAN verification scripts
├── results/              # Simulation outputs and test reports
├── scripts/              # Automation scripts
├── competition/          # ICTGC strategy + source docs
└── my-workspace/         # Docs, logs, tickets
```

## Constraints

- Simulation only (no layout)
- Headless-first workflow
- Prefer reusable building blocks and verify each layer before reuse

## Quick Commands

```bash
source setup_cadence.sh
./build.sh all
./build.sh <component>
```
