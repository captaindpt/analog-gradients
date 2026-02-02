# Development Playbook

This file defines how agents should execute work in this repo.

## Mission

Build and verify a transistor-up hardware stack that evolves from digital GPU
building blocks into an analog neuromorphic compute core.

## Agent Bootstrap (First 5 Minutes)

1. Read `my-workspace/docs/INDEX.md`.
2. Read `my-workspace/docs/vision.md`.
3. Read `my-workspace/docs/STATUS.md`.
4. Read `AGENTS.md`.
5. Read `my-workspace/docs/armory/snapshot-2026-02-02/armory-summary.md`.

## Workflow

1. `source setup_cadence.sh`
2. Validate current baseline with `./build.sh all` (or impacted components).
3. Implement circuit in `netlists/<name>.scs`.
4. Implement verification in `ocean/test_<name>.ocn`.
5. Add component wiring in `build.sh` if new top-level target.
6. Re-run verification and record outcomes in `results/<name>_test.txt`.

## Documentation Update Contract

For every meaningful change:

- Update `my-workspace/docs/STATUS.md` for milestone progress.
- Add a dated note in `my-workspace/logs/`.
- Update or create a ticket in `my-workspace/tickets/` when scope changes.

## Armory-Aware Rules

- Preferred stack for this repo: Cadence Spectre + OCEAN + optional Virtuoso SKILL.
- Treat the armory snapshot as capability evidence, not as permission to switch
  toolchains mid-task.
- Do not introduce Synopsys/Siemens/other tool dependencies unless explicitly
  requested and documented in ticket/log files.

## Definition of Development-Ready

- Clear objective in `my-workspace/docs/vision.md`
- Current progress reflected in `my-workspace/docs/STATUS.md`
- Reproducible run path (`setup_cadence.sh` + `build.sh`)
- Tests produce readable PASS/FAIL reports under `results/*_test.txt`
