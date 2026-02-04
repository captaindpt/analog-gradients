# Development Playbook

This file defines how agents should execute work in this repo.

## Mission

Build and verify a transistor-up hardware stack that evolves from digital GPU
building blocks into an analog neuromorphic compute core, then demonstrate
credible implementation readiness through a reproducible full-flow path.

## Agent Bootstrap (First 5 Minutes)

Follow the canonical order in `my-workspace/docs/INDEX.md`. Quick copy:

1. Read `AGENTS.md`.
2. Read `my-workspace/README.md`.
3. Read `my-workspace/docs/INDEX.md`.
4. Read `my-workspace/docs/vision.md`.
5. Read `my-workspace/docs/DEVELOPMENT.md`.
6. Read `my-workspace/docs/STATUS.md`.
7. Read `my-workspace/docs/RANDEZVOUS.md`.
8. Read `my-workspace/docs/armory/snapshot-2026-02-02/armory-summary.md`.
9. Read `my-workspace/docs/reference/README.md` (secondary context).

## Workflow

1. `source setup_cadence.sh`
2. Validate current baseline with `./build.sh all` (or impacted components).
   - `build.sh` is fail-closed: stale `*_test.txt` and `.raw` artifacts are
     removed before each run, and fresh raw/result timestamps are required.
   - Result parsing is strict: exactly one terminal verdict line is required,
     and any in-file `FAIL:`/`[FAIL]`/`ERROR:` marker fails the component.
   - OCEAN runtime errors are fatal: any `*Error*` in `results/<component>/ocean.log`
     fails the component, even if OCEAN exits `0`.
   - Spectre strict warning policy is active: any unallowlisted
     `WARNING (SPECTRE-xxxxx)` in `results/<component>/spectre.log` is fatal.
   - Warning allowlist is explicit and auditable:
     `config/spectre_warning_allowlist.txt`.
   - Warning-count drift is fail-closed against prior green baseline:
     each component/code count must be `<=` baseline in
     `config/spectre_warning_baseline.csv`.
   - Run manifests include per-component warning summaries (`warnings=...`).
   - OCEAN scripts use repo-relative paths (`results/...`) to avoid machine-locked
     absolute path dependencies.
   - Every invocation writes a timestamped log + manifest:
     `results/_runlogs/build_<component>_<timestamp>.{log,manifest.txt}`.
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
- `scripts/sweep_neuro_tile4_coupled.sh`
- `python3 scripts/analyze_lif_ode_fit.py`
- `python3 scripts/analyze_temporal_sensitivity.py`
- `scripts/analyze_lif_energy.sh`
- `scripts/run_lif_corner_evidence.sh`
- `./build.sh coincidence_detector` (spike-domain temporal AND compute demo)
- `./build.sh xor_spike2` (spike-domain XOR compute demo)
- `./build.sh neuro_tile4_mixed_signal` (digital-enable / analog-propagation smoke)

Reference thesis: `competition/founder-thesis.md`

### Current Smoke Command Set

- Stage-by-stage:
  - `scripts/run_dc_smoke.sh`
  - `scripts/run_innovus_smoke.sh`
  - `scripts/run_calibre_smoke.sh`
- End-to-end:
  - `scripts/run_fullflow_smoke.sh`
  - `FULLFLOW_STRICT=1 scripts/run_fullflow_smoke.sh` (fails on any degraded stage)

License defaults for full-flow stages are auto-seeded by:
- `scripts/setup_fullflow_licenses.sh`
  - `SNPSLMD_LICENSE_FILE=6053@licaccess.cmc.ca`
  - `MGLS_LICENSE_FILE=6056@licaccess.cmc.ca`
  - `SALT_LICENSE_SERVER=$MGLS_LICENSE_FILE`
  - user-provided environment values still override defaults.

### Current Environment Caveat

- As of 2026-02-03 investigation, DC and Calibre license behavior in this VM is
  configuration-sensitive (not hard entitlement blockers by default):
  - `SNPSLMD_LICENSE_FILE=6053@licaccess.cmc.ca`
  - `MGLS_LICENSE_FILE=6056@licaccess.cmc.ca`
  - `SALT_LICENSE_SERVER=$MGLS_LICENSE_FILE`
- `scripts/setup_fullflow_licenses.sh` now seeds these defaults for full-flow
  smoke scripts.
- Remaining DC blocker after license env is set:
  - `DB-1` target-library format/path issue (`.lib` vs expected `.db` flow usage).

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
