# 0001: Build Level 4 Logic Gates

**Status:** Open
**Priority:** High
**Created:** 2026-01-31

## Description

Build AND, OR, XOR, XNOR gates using the verified Level 5 primitives.

## Tasks

- [ ] AND2 = NAND2 → Inverter
- [ ] OR2 = NOR2 → Inverter
- [ ] XOR2 = NAND-based implementation
- [ ] XNOR2 = XOR2 → Inverter
- [x] Create netlists
- [x] Create OCEAN test scripts
- [x] Verify all truth tables
- [x] Update STATUS.md

## Notes

- Verified successfully after setting `CDS_LIC_FILE=6055@licaccess.cmc.ca`.

## Technical Notes

**AND2:** Cascade NAND2 output through inverter
```
A ──┐
    ├── NAND ──── INV ──── OUT
B ──┘
```

**XOR2:** Using NAND gates only (4 NANDs)
```
    ┌─────────────────┐
A ──┼── NAND1 ────────┼── NAND3 ──┐
    │      │          │           │
    │      └── NAND2 ─┘           ├── NAND4 ── OUT
    │             │               │
B ──┼─────────────┘               │
    └─────────────────────────────┘
```

## Acceptance Criteria

1. Files created:
   - `netlists/and2.scs`
   - `netlists/or2.scs`
   - `netlists/xor2.scs`
   - `netlists/xnor2.scs`
   - `ocean/test_and2.ocn`
   - `ocean/test_or2.ocn`
   - `ocean/test_xor2.ocn`
   - `ocean/test_xnor2.ocn`

2. All truth tables verified:
   - AND2: 0,0→0 | 1,0→0 | 0,1→0 | 1,1→1
   - OR2:  0,0→0 | 1,0→1 | 0,1→1 | 1,1→1
   - XOR2: 0,0→0 | 1,0→1 | 0,1→1 | 1,1→0
   - XNOR2: 0,0→1 | 1,0→0 | 0,1→0 | 1,1→1

3. `./build.sh all` passes with all gates

4. STATUS.md updated with Level 4 results

## How To

1. Read `AGENTS.md` for templates
2. Read `skill.md` for workflow
3. Use `netlists/nand2.scs` as reference
4. Run `source setup_cadence.sh` first
