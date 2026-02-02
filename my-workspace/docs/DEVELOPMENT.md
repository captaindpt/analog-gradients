# Development Playbook

This file defines how agents should execute work in this repo.

## Mission

Build and verify a transistor-up hardware stack that evolves from digital GPU
building blocks into an analog neuromorphic compute core, then demonstrate
credible implementation readiness through a reproducible full-flow path.

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

## Competition Edge Workflow (Transistor -> GDSII Demo)

Use this track to support the ICTGC "one-terminal full-flow" narrative.

1. Keep analog proof current (`synapse`, `lif_neuron`, tile-level PASS results).
2. Select a digital implementation target (initially `alu4` or `pe1` class block).
3. Run synthesis smoke flow (Synopsys DC) and capture netlist/timing artifacts.
4. Run place-and-route smoke flow (Cadence Innovus) and capture floorplan/route outputs.
5. Run physical verification smoke flow (Siemens Calibre) and capture DRC/LVS status.
6. Export and archive implementation artifacts under `competition/`.
7. Keep the flow script-driven so it can be demonstrated in one terminal session.

## Founder-Evidence Workflow (Original Idea Track)

Use this track to prove the compute thesis beyond tool operation.

1. Keep raw analog traces exportable (`competition/data/*.csv`) with no smoothing assumptions.
2. Maintain deterministic timing evidence (`neuro_tile4`, `neuro_tile4_coupled`).
3. Run parameter sweeps and quantify timing sensitivity (temporal gradients).
4. Fit measured dynamics to governing equations (LIF/RC ODE checks).
5. Estimate energy-per-event from transient supply behavior.
6. Keep each claim mapped to a reproducible artifact under `competition/`.

Current analysis commands:
- `python3 scripts/analyze_lif_ode_fit.py`
- `python3 scripts/analyze_temporal_sensitivity.py`
- `scripts/analyze_lif_energy.sh`
- `./build.sh neuro_tile4_mixed_signal` (digital-enable / analog-propagation smoke)

Reference thesis: `competition/founder-thesis.md`

### Current Smoke Command Set

- Stage-by-stage:
  - `scripts/run_dc_smoke.sh`
  - `scripts/run_innovus_smoke.sh`
  - `scripts/run_calibre_smoke.sh`
- End-to-end:
  - `scripts/run_fullflow_smoke.sh`
  - `FULLFLOW_STRICT=1 scripts/run_fullflow_smoke.sh` (fails on license-blocked stages)

### Current Environment Caveat

- DC and Calibre binaries run in this environment, but licenses may be
  unavailable; scripts emit explicit warning artifacts instead of silently
  failing.

## Documentation Update Contract

For every meaningful change:

- Update `my-workspace/docs/STATUS.md` for milestone progress.
- Add a dated note in `my-workspace/logs/`.
- Update or create a ticket in `my-workspace/tickets/` when scope changes.

## Armory-Aware Rules

- Preferred stack for this repo: Cadence Spectre + OCEAN + optional Virtuoso SKILL.
- Treat the armory snapshot as capability evidence, not as permission to switch
  toolchains mid-task.
- Synopsys/Siemens flow usage is now in-scope for the ICTGC full-flow demo
  track; document all usage in ticket/log files and keep scripts reproducible.

## Definition of Development-Ready

- Clear objective in `my-workspace/docs/vision.md`
- Current progress reflected in `my-workspace/docs/STATUS.md`
- Reproducible run path (`setup_cadence.sh` + `build.sh`)
- Tests produce readable PASS/FAIL reports under `results/*_test.txt`
- Competition evidence assets are reproducible under `competition/` scripts
