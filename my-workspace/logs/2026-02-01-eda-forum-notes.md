# Session: 2026-02-01 - EDA Forum Notes (OCEAN/Spectre/SKILL)

## Summary

Captured reusable notes for answering common Cadence/Spectre/OCEAN questions.

## Notes

- **License error LMC-01902** → set `CDS_LIC_FILE` or `LM_LICENSE_FILE`.
  On this CMC host, `CDS_LIC_FILE=6055@licaccess.cmc.ca` works.
- **OCEAN batch mode** → stdout is buffered; write results to a file.
- **Result selection** → use `selectResult("tran_test-tran")` (string with hyphen).
- **SKILL/OCEAN syntax** → avoid lambdas in batch scripts; explicit checks are safer.
- **Spectre netlists** → keep `subckt` pin lists on a single line to avoid parse errors.
- **Headless Virtuoso** → `./scripts/virtuoso_replay.sh` is the stable entry point.
