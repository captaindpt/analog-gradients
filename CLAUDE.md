# CLAUDE.md

Context and guidance for Claude Code working in this repository.

## What This Is

Neuromorphic computing research repository. Building a GPU core from transistors up using Cadence tools on CMC Cloud.

## Repository Structure

```
analog-gradients/
├── CLAUDE.md             # This file - general context
├── skill.md              # How-to guides and commands
├── setup_cadence.sh      # Cadence environment (bash)
├── build.sh              # Build and test runner
├── netlists/             # Spectre simulation files (.scs)
├── ocean/                # OCEAN verification scripts (.ocn)
├── skill/                # Virtuoso SKILL scripts (.il)
├── results/              # Simulation outputs
├── lib/                  # Reusable subcircuit library
└── my-workspace/         # Reference docs only
    ├── docs/             # Vision, status, reference
    ├── tickets/          # Work items
    └── logs/             # Session logs
```

## Current State

**Level 5 COMPLETE:** Inverter, NAND2, NOR2 verified.

See `my-workspace/docs/STATUS.md` for full progress.

## Build Hierarchy

```
Level 5: CMOS (inverter, NAND, NOR)        ✅ DONE
Level 4: Logic gates (AND, OR, XOR)        🔜 NEXT
Level 3: Building blocks (adder, mux)
Level 2: RTL (ALU, SRAM, FSM)
Level 1: Functional blocks (PE array)
Level 0: System (GPU core)
```

## CMC Cloud

```bash
ssh -Y -p 31487 v71349@130.15.52.59
```

- Shell: tcsh (scripts use bash workaround)
- Tools: Virtuoso IC23, Spectre 23, OCEAN
- Claude: `--print` mode only (TUI broken)

## Key Constraint

Schematic creation via SKILL requires X11. We use netlist-based simulation flow for headless operation.

## Quick Commands

```bash
source setup_cadence.sh   # Setup environment
./build.sh all            # Build and test everything
./build.sh inverter       # Test single component
```
