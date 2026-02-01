# Session: 2026-01-31 - Pipeline Setup

## Summary

Established working simulation pipeline on CMC Cloud. Verified Level 5 CMOS primitives.

## Accomplished

1. **Environment Setup**
   - Created `setup_cadence.sh` for bash (CMC scripts are tcsh)
   - Verified Virtuoso, Spectre, OCEAN accessible
   - Set up `~/cds.lib` with gpu_lib and analogLib

2. **Level 5 Components Built**
   - Inverter: PASS
   - NAND2: PASS
   - NOR2: PASS

3. **Pipeline Infrastructure**
   - Spectre netlists using `mos1` model
   - OCEAN verification scripts
   - `build.sh` master runner
   - Automated truth table verification

4. **Repository Organization**
   - Created my-workspace structure
   - Separated docs, tickets, logs, src

## Key Learnings

- Spectre uses `mos1` primitive, not `nmos`/`pmos`
- Model syntax: `model name mos1 type=n vth=0.4 kp=120u`
- PSF results named `tran_test-tran` not `tran_test`
- OCEAN needs string for hyphenated result names: `selectResult("tran_test-tran")`

## Blockers

- Schematic creation via SKILL requires X11 (can't do headless)
- Workaround: Use netlist-based simulation flow

## Next Session

- Build Level 4 logic gates (AND, OR, XOR, XNOR)
- See ticket #0001

## Files Created

- `src/setup_cadence.sh`
- `src/build.sh`
- `src/netlists/{inverter,nand2,nor2}.scs`
- `src/ocean/{verify_inverter,test_nand2,test_nor2}.ocn`
- `src/skill/L5_{inverter,nand2,nor2}.il`
