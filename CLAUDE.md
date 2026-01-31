# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Purpose

This is a **neuromorphic computing research repository** focused on analog AI hardware, memristor-based computing-in-memory (CIM), and hardware-aware training algorithms. The work supports preparation for the FABrIC IoT Device Challenge and CMC Microsystems-based prototyping efforts.

## Repository Structure

```
analog-gradients/
├── skill.md                     # ACTIVE WORKFLOW - CMC Cloud + Claude + OCEAN
├── Cadence/                     # Setup guides and automation docs
├── papers/                      # Research paper collection
│   ├── papers-markdown/         # Converted summaries and analyses
│   └── BOOKS/                   # Reference books
└── mani-plan.md                 # Strategic roadmap
```

## CMC Cloud Workflow (PRIMARY)

**See [skill.md](skill.md) for full details.**

### Quick Connect
```bash
ssh -Y -p 31487 v71349@130.15.52.59
```

### On CMC Cloud
```bash
source /CMC/scripts/cadence.ic23.10.140.csh
source /CMC/scripts/cadence.spectre23.10.802.csh

# Claude (print mode only - TUI broken)
claude --print "your task"

# OCEAN simulation
ocean -nograph

# Virtuoso GUI (needs X11)
virtuoso &
```

### Build Hierarchy
```
Level 5: CMOS (inverter, NAND, NOR)
Level 4: Logic gates (AND, OR, XOR)
Level 3: Building blocks (adder, mux, register)
Level 2: RTL (ALU, SRAM, FSM)
Level 1: Functional blocks (PE array, memory)
Level 0: System (GPU core)
```

### Constraints
- Headless schematic creation fails (needs X11)
- Use GUI + SKILL scripts loaded via CIW
- OCEAN simulations work headlessly

## Current Mission

**Goal:** Build circuit elements bottom-up using Claude + OCEAN on CMC Cloud.

**Immediate target:** Transistors → gates → adders → ALU, verified at each level via Spectre simulation.

**Demo concept:** "Watch AI design a GPU core in 60 seconds" - building from transistors up, verified at each level.

**Longer-term:** FABrIC IoT Challenge 2026 - Analog Edge-AI Sensor Node

## Tools Stack

| Tool | Status | Purpose |
|------|--------|---------|
| Cadence Virtuoso | ✅ CMC Cloud | Schematic capture, layout |
| Cadence Spectre | ✅ CMC Cloud | Circuit simulation |
| OCEAN | ✅ CMC Cloud | Scriptable simulation interface |
| Claude --print | ✅ CMC Cloud | AI-assisted SKILL generation |
| PyTorch + AIHWKIT | 🔜 Next | Hardware-aware neural training |


## Resources

- CMC Microsystems: https://cmc.ca
- FABrIC IoT Challenge: https://fabricinnovation.ca
- IBM AIHWKIT: https://github.com/IBM/aihwkit
