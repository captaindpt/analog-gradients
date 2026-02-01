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

**Port changes each session.** Get current credentials:
1. Log into CMC Cloud portal
2. Start VM session
3. Click "Open Terminal SSH" - downloads `.moba` file
4. Check `~/Downloads/*.moba` for current port:
   ```bash
   cat ~/Downloads/My\ Linux\ CAD\ Workstation*.moba
   # Look for port number (e.g., 130.15.52.59%30189%v71349)
   ```

**Connect:**
```bash
ssh -Y -p <PORT> v71349@130.15.52.59
```

**VSCode Remote:** Cmd+Shift+P → "Remote-SSH: Connect to Host" → `ssh -p <PORT> v71349@130.15.52.59`

**On the machine:**
- Shell: tcsh (`setenv` not `export`)
- Claude/gh in PATH: `~/.tcshrc` has `setenv PATH "$HOME/.local/bin:$PATH"`
- Claude: `--print` mode only (TUI broken)
- Tools: `source /CMC/scripts/cadence.ic23.10.140.csh`

**First-time setup (already done):**
```tcsh
curl -fsSL https://claude.ai/install.sh | bash
echo 'setenv PATH "$HOME/.local/bin:$PATH"' >> ~/.tcshrc
source ~/.tcshrc
```

## Key Constraint

Schematic creation via SKILL requires X11. We use netlist-based simulation flow for headless operation.

## Quick Commands

```bash
source setup_cadence.sh   # Setup environment
./build.sh all            # Build and test everything
./build.sh inverter       # Test single component
```
