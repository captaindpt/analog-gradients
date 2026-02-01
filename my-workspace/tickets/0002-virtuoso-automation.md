# 0002: Virtuoso Headless Automation

**Status:** Open
**Priority:** High
**Created:** 2026-02-01

## Description

Make Virtuoso automation reproducible and headless-friendly, so schematics can
be generated from SKILL scripts without manual GUI steps.

## Tasks

- [x] Add repo runner: `scripts/virtuoso_replay.sh`
- [ ] Create reusable SKILL helpers (wiring, pin placement, net creation)
- [ ] Update L5 NAND2/NOR2 SKILL scripts to be fully wired (no GUI wiring)
- [ ] Add L4 gate SKILL scripts (and2/or2/xor2/xnor2)
- [ ] Document headless requirements (DISPLAY / xvfb-run)

## Acceptance Criteria

1. `./scripts/virtuoso_replay.sh skill/L5_inverter.il` runs without manual steps
2. L5 NAND2/NOR2 scripts create fully wired schematics
3. L4 gates can be generated via SKILL replay only
4. Documentation covers headless workflows and common errors
