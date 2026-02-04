# 2026-02-03: Warning Baseline Drift Gate

## Scope

Add fail-closed protection against warning-count creep for allowlisted Spectre warning codes.

## Changes

- `build.sh`
  - added warning-code counting (`spectre_warning_counts`)
  - added per-component warning summary (`spectre_warning_summary`)
  - added baseline lookup/check (`baseline_warning_count`, `check_spectre_warning_baseline`)
  - simulation now fails if current warning count for any code/component exceeds baseline
  - baseline file path supports override via `SPECTRE_WARNING_BASELINE_FILE`
  - manifest records include `warnings=...` for each component
- Added baseline file:
  - `config/spectre_warning_baseline.csv`
  - baseline source: green run `results/_runlogs/build_all_20260203_134652.manifest.txt`

## Validation

- `./build.sh pe4` PASS
- `./build.sh all` PASS
  - `results/_runlogs/build_all_20260203_135841.{log,manifest.txt}`
- negative test (expected fail):
  - `SPECTRE_WARNING_BASELINE_FILE=/tmp/spectre_warning_baseline_test.csv ./build.sh pe4`
  - fails with `Strict Spectre baseline violation` when baseline count is below observed count

## Outcome

The harness now blocks gradual warning rot even when warning codes remain allowlisted.
