# 2026-02-03: Strict Spectre Warning Policy

## Scope

Enabled strict warning fail-close behavior in `build.sh` for Spectre logs.

## Change

- Added `check_spectre_log_strict()` to `build.sh`.
- Build now fails simulation if `spectre.log` contains known warning classes:
  - tolerance relaxation (`SPECTRE-17192`)
  - zero saturation channel conductance model notices
  - bad pivoting in DC analysis
  - Gmin materially affecting DC solution
  - trapezoidal ringing notices

## Validation

- `bash -n build.sh` PASS
- `./build.sh pe4` now FAILS as expected under strict policy with explicit violation lines.

## Outcome

CI-style warning enforcement is now active; model/convergence warning cleanup is now required to restore all-green runs under strict mode.
