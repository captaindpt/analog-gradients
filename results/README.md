# Results Directory Policy

This folder is for simulation outputs.

## Keep in version control

- `results/*_test.txt` verification summaries
- `results/inverter_verify.txt` (legacy inverter verifier output)

## Generated Audit Artifacts

- `build.sh` emits timestamped run logs/manifests under `results/_runlogs/`:
  - `build_<component>_<timestamp>.log`
  - `build_<component>_<timestamp>.manifest.txt`
- These are machine-audit artifacts (local provenance), not canonical source
  evidence.

## Do not keep in version control

- Spectre raw waveforms (`*.raw/`, `*.tran`, `*.psfxl`, `*.sig`)
- Spectre/OCEAN logs (`spectre.log`, `ocean.log`, `logFile`, run logs)
- Sweep run archives under `results/**/sweeps/`
- Temporary debug/environment files

The root `.gitignore` is configured to ignore generated artifacts while keeping
human-readable verification summaries.
