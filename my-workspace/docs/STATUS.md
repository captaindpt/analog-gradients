# GPU Building Blocks - Status

**Last Updated:** 2026-02-01

## Build Hierarchy

```
Level 5: CMOS Primitives     ✅ COMPLETE
Level 4: Logic Gates         🔜 NEXT
Level 3: Building Blocks     ⏳ PENDING
Level 2: RTL Components      ⏳ PENDING
Level 1: Functional Blocks   ⏳ PENDING
Level 0: System              ⏳ PENDING
```

## Level 5: CMOS Primitives ✅

| Component | Netlist | Simulation | Verification |
|-----------|---------|------------|--------------|
| Inverter  | ✅ | ✅ | ✅ PASS |
| NAND2     | ✅ | ✅ | ✅ PASS |
| NOR2      | ✅ | ✅ | ✅ PASS |

### Verification Results

**Inverter:**
- Vin=HIGH → Vout=0.007V (LOW) ✓
- Vin=LOW → Vout=1.783V (HIGH) ✓

**NAND2:** `OUT = ~(A & B)`
- A=0, B=0 → 1.792V (HIGH) ✓
- A=1, B=0 → 1.769V (HIGH) ✓
- A=0, B=1 → 1.772V (HIGH) ✓
- A=1, B=1 → 0.015V (LOW) ✓

**NOR2:** `OUT = ~(A | B)`
- A=0, B=0 → 1.766V (HIGH) ✓
- A=1, B=0 → 0.014V (LOW) ✓
- A=0, B=1 → 0.012V (LOW) ✓
- A=1, B=1 → 0.004V (LOW) ✓

## Level 4: Logic Gates (Next)

| Component | Netlist | Simulation | Verification |
|-----------|---------|------------|--------------|
| AND2      | ✅ | ⏳ | ⏳ |
| OR2       | ✅ | ⏳ | ⏳ |
| XOR2      | ✅ | ⏳ | ⏳ |
| XNOR2     | ✅ | ⏳ | ⏳ |

## Level 3: Building Blocks

| Component  | Netlist | Simulation | Verification |
|------------|---------|------------|--------------|
| MUX2       | ✅ | ⏳ | ⏳ |
| Half Adder | ✅ | ⏳ | ⏳ |
| Full Adder | ✅ | ⏳ | ⏳ |

## Tooling

- Headless-friendly Virtuoso runner: `scripts/virtuoso_replay.sh`

## Quick Commands

```bash
# Build and test all components
./build.sh all

# Build specific component
./build.sh inverter
./build.sh nand2
./build.sh nor2

# Source Cadence environment
source setup_cadence.sh
```

## Repository Structure

```
analog-gradients/
├── setup_cadence.sh      # Bash env setup for Cadence
├── build.sh              # Master build/test script
├── STATUS.md             # This file
├── netlists/             # Spectre netlists (.scs)
│   ├── inverter.scs
│   ├── nand2.scs
│   └── nor2.scs
├── ocean/                # OCEAN verification scripts (.ocn)
│   ├── verify_inverter.ocn
│   ├── test_nand2.ocn
│   └── test_nor2.ocn
├── skill/                # Virtuoso SKILL scripts (.il)
│   ├── L5_inverter.il
│   ├── L5_nand2.il
│   └── L5_nor2.il
├── results/              # Simulation outputs
│   ├── inverter/
│   ├── nand2/
│   └── nor2/
└── lib/                  # Future: Reusable subcircuits
```

## Open Tickets

See `my-workspace/tickets/` for work items.
