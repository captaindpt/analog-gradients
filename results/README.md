# Results Directory Policy

This folder is for simulation outputs.

## Keep in version control

- `results/*_test.txt` verification summaries
- `results/inverter_verify.txt` (legacy inverter verifier output)

## Do not keep in version control

- Spectre raw waveforms (`*.raw/`, `*.tran`, `*.psfxl`, `*.sig`)
- Spectre/OCEAN logs (`spectre.log`, `ocean.log`, `logFile`, run logs)
- Auto-generated run manifests (`results/_runlogs/*.manifest.txt`)
- Temporary debug/environment files

The root `.gitignore` is configured to ignore generated artifacts while keeping
human-readable verification summaries.
