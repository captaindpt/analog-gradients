# AGENTS.md

Instructions for any agent working in this repository.

## What This Is

A testbed for AI-driven hardware design. You have tools to design, simulate, and verify digital circuits using Cadence Spectre on CMC Cloud.

## Your Task

Build digital circuits from specifications. Use existing building blocks when available, create new ones when needed, verify everything via simulation.

## Available Tools

### Environment
```bash
source setup_cadence.sh   # Must run first
```

### Build & Test
```bash
./build.sh all            # Test all components
./build.sh <component>    # Test specific component
```

### Create New Components

1. **Write netlist** in `netlists/<name>.scs`
2. **Write test** in `ocean/test_<name>.ocn`
3. **Add to build.sh** if needed
4. **Run verification**

## Netlist Template

```
// <name>.scs
simulator lang=spectre

parameters vdd_val=1.8

model nch mos1 type=n vth=0.4 kp=120u
model pch mos1 type=p vth=-0.4 kp=40u

V_VDD (vdd 0) vsource dc=vdd_val

// Your circuit here
// Instance format: NAME (drain gate source bulk) MODEL w=Xu l=Yu

tran_test tran stop=50n
save out in
```

## OCEAN Test Template

```lisp
; test_<name>.ocn
out = outfile("/path/to/results/<name>_test.txt" "w")
fprintf(out "=== <NAME> Verification ===\n")

simulator('spectre)
openResults("/path/to/results/<name>/<name>.raw")
selectResult("tran_test-tran")

vout = v("out")
; Sample and verify: value(vout 5n)
; Write PASS/FAIL

close(out)
exit()
```

## Verified Building Blocks

| Component | File | Function |
|-----------|------|----------|
| Inverter | `netlists/inverter.scs` | OUT = ~IN |
| NAND2 | `netlists/nand2.scs` | OUT = ~(A & B) |
| NOR2 | `netlists/nor2.scs` | OUT = ~(A \| B) |

## Build Hierarchy

```
Level 5: CMOS ✅      → inverter, nand2, nor2
Level 4: Logic        → and2, or2, xor2 (use Level 5)
Level 3: Blocks       → adder, mux (use Level 4)
Level 2: RTL          → ALU, registers (use Level 3)
Level 1: Functional   → PE, memory (use Level 2)
Level 0: System       → GPU core (use Level 1)
```

Build bottom-up. Each level uses components from the level below.

## File Locations

- Netlists: `netlists/*.scs`
- Tests: `ocean/*.ocn`
- Results: `results/<component>/`
- Docs: `my-workspace/docs/`
- Tickets: `my-workspace/tickets/`

## Constraints

- Simulation only (no layout)
- Headless operation (no GUI)
- Results go to `results/` directory
- All components must pass verification before use
