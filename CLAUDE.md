# CLAUDE.md

Context for Claude Code in this repository.

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

## Current Verified Stack

- Level 5: inverter, nand2, nor2
- Level 4: and2, or2, xor2, xnor2
- Level 3: mux2, half_adder, full_adder
- Level 2: alu1, alu4
- Level 1: pe1, pe4
- Level 0: gpu_core

## Current Development Focus

- Bring up and verify `lif_neuron`
- Create neuromorphic tile-level composition
- Preserve digital baseline while extending analog path

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
