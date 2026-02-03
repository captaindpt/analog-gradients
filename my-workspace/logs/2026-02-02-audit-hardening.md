# Session: 2026-02-02 - Audit Hardening

## Summary

Implemented hardening changes requested after audit review so the build flow is
fail-closed and evidence is auditable.

## Changes Applied

1. **`build.sh` fail-closed behavior**
   - Switched to `set -euo pipefail`.
   - Removed stale-result pass risk by deleting prior `*_test.txt` before each
     OCEAN run.
   - Deleted prior raw output directories before Spectre runs.
   - Added explicit fresh-raw checks for
     `tran_test.tran.tran.psfxl` generation time.

2. **Valid MOS model threshold parameter**
   - Replaced invalid `vth=` usage with valid `vto=` in all netlists.
   - Digital stack netlists now use explicit `vto` values.
   - Analog path netlists use explicit `vto` values tuned to preserve verified
     behavior after parameter activation.

3. **Run logs and manifests for `./build.sh all`**
   - Added automatic timestamped run log emission under
     `results/_runlogs/build_all_<timestamp>.log`.
   - Added per-run manifest under
     `results/_runlogs/build_all_<timestamp>.manifest.txt`.
   - Manifest records start/end UTC, exit status, failed component (if any),
     and per-component PASS records with raw/result files and timestamps.

## Verification

- Full build executed and passed with hardening in place:
  - `./build.sh all` at local time ~18:23-18:26 (2026-02-02)
  - Log: `results/_runlogs/build_all_20260202_182329.log`
  - Manifest: `results/_runlogs/build_all_20260202_182329.manifest.txt`
- Confirmed no Spectre warnings remain for ignored threshold parameter in latest
  `results/*/spectre.log` outputs.
