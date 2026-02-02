# Session: 2026-02-02 - Full-Flow Smoke Bring-Up

## Summary

Completed initial DC -> Innovus -> Calibre smoke-flow bring-up for the
competition "transistor-to-GDS" narrative.

## Implemented

- Added smoke scripts:
  - `scripts/run_dc_smoke.sh`
  - `scripts/run_innovus_smoke.sh`
  - `scripts/run_calibre_smoke.sh`
  - `scripts/run_fullflow_smoke.sh`
- Added flow assets:
  - `implementation/fullflow_demo/rtl/alu4_flow_demo.v`
  - `implementation/fullflow_demo/rtl/alu4_flow_demo_fallback_mapped.v`
  - `implementation/fullflow_demo/constraints/alu4_flow_demo.sdc`
  - `implementation/fullflow_demo/scripts/dc_synth.tcl`
  - `implementation/fullflow_demo/scripts/innovus_pnr.tcl`

## Execution Outcome

- DC stage: binary executes, synthesis blocked by `DCSH-1` license; fallback
  mapped netlist used for downstream flow continuity.
- Innovus stage: PASS; emits DEF/post-route netlist/GDS and timing/area/power
  reports.
- Calibre stage: binary executes, DRC blocked by license; blocked summary and
  warning artifact emitted.
- Strict mode validated:
  `FULLFLOW_STRICT=1 scripts/run_fullflow_smoke.sh` exits with code `20` when
  any stage is license-blocked.

## Documentation Updates

- `competition/full-flow-smoke-evidence.md` added as artifact index.
- `competition/verification-evidence.md` updated with full-flow commands and status.
- `my-workspace/docs/STATUS.md` and ticket `0010` updated with blocker-aware state.
