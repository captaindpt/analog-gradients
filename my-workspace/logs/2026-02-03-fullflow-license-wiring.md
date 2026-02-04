# Full-Flow License Wiring + Verification

- Date: 2026-02-03
- Goal: wire Synopsys/Siemens license defaults into flow scripts and verify replay behavior.

## Changes

- Added `scripts/setup_fullflow_licenses.sh`:
  - seeds defaults when unset:
    - `SNPSLMD_LICENSE_FILE=6053@licaccess.cmc.ca`
    - `MGLS_LICENSE_FILE=6056@licaccess.cmc.ca`
    - `SALT_LICENSE_SERVER=$MGLS_LICENSE_FILE`
- Updated stage scripts to source defaults directly:
  - `scripts/run_dc_smoke.sh`
  - `scripts/run_calibre_smoke.sh`
  - `scripts/run_fullflow_smoke.sh`
- Hardened DC smoke stage status handling:
  - detect `DCSH-1` (license) and `DB-1`/`UIO-3` (target-library incompatibility)
  - emit explicit warn artifacts
  - force fallback mapped netlist when degraded

## Verification Runs

- `scripts/run_dc_smoke.sh`
  - license checkout succeeded (no `DCSH-1`)
  - detected target-library incompatibility (`DB-1` / `UIO-3`)
  - fallback warn emitted:
    `implementation/fullflow_demo/work/dc/reports/alu4_flow_demo_dc_target_lib.warn`
- `scripts/run_calibre_smoke.sh`
  - PASS with DRC licenses acquired (`calibrehdrc`, `calibredrc`)
- `scripts/run_fullflow_smoke.sh`
  - PASS (degraded due DC target-library fallback)
- `FULLFLOW_STRICT=1 scripts/run_fullflow_smoke.sh`
  - FAIL (expected fail-closed behavior on degraded stage; exit 20)
