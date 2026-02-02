# AGENTS.md

Instructions for any agent working in this repository.

## What This Is

A testbed for AI-driven hardware design. You have tools to design, simulate, and verify digital circuits using Cadence Spectre on CMC Cloud.
Current mission: evolve the verified GPU stack into a neuromorphic analog
compute core (NeuroCore) while keeping reproducible verification.

## Source of Truth

- Knowledgebase navigation: `my-workspace/docs/INDEX.md`
- Vision and product direction: `my-workspace/docs/vision.md`
- Development workflow: `my-workspace/docs/DEVELOPMENT.md`
- Technical status: `my-workspace/docs/STATUS.md`

## Agent Bootstrap Order

Read these before making changes:

1. `my-workspace/docs/INDEX.md`
2. `my-workspace/docs/vision.md`
3. `my-workspace/docs/DEVELOPMENT.md`
4. `my-workspace/docs/STATUS.md`
5. `my-workspace/docs/armory/snapshot-2026-02-02/armory-summary.md`

## Your Task

Build and verify digital/analog circuit blocks from specifications. Reuse
existing building blocks when possible, create new ones when needed, and keep
the repo aligned to the NeuroCore mission.

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

### Level 5: CMOS Primitives

- Inverter: `netlists/inverter.scs`
- NAND2: `netlists/nand2.scs`
- NOR2: `netlists/nor2.scs`

### Level 4: Logic

- AND2: `netlists/and2.scs`
- OR2: `netlists/or2.scs`
- XOR2: `netlists/xor2.scs`
- XNOR2: `netlists/xnor2.scs`

### Level 3: Blocks

- MUX2: `netlists/mux2.scs`
- Half Adder: `netlists/half_adder.scs`
- Full Adder: `netlists/full_adder.scs`

### Level 2: RTL

- ALU1: `netlists/alu1.scs`
- ALU4: `netlists/alu4.scs`

### Level 1: Functional

- PE1: `netlists/pe1.scs`
- PE4: `netlists/pe4.scs`

### Level 0: System

- GPU Core: `netlists/gpu_core.scs`

### Experimental / In Progress

- LIF Neuron: `netlists/lif_neuron.scs` with `ocean/test_lif_neuron.ocn`

## Build Hierarchy

```
Level 5: CMOS ✅      → inverter, nand2, nor2
Level 4: Logic ✅     → and2, or2, xor2, xnor2
Level 3: Blocks ✅    → mux2, half_adder, full_adder
Level 2: RTL ✅       → alu1, alu4
Level 1: Functional ✅→ pe1, pe4
Level 0: System ✅    → gpu_core
```

Build bottom-up. Each level uses components from the level below.

## Next Build Track (Neuromorphic)

1. Verify `lif_neuron`
2. Build neuron array/tile blocks
3. Integrate with existing PE/GPU scaffold where useful

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
