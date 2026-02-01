# analog-gradients

Testbed for AI-driven hardware design. Build digital circuits bottom-up with
Cadence Spectre/OCEAN using netlist-first, headless-friendly workflows.

## Quick Start

```bash
source setup_cadence.sh
./build.sh all
```

## Repository Structure

```
analog-gradients/
├── AGENTS.md             # Agent instructions
├── README.md             # This file
├── setup_cadence.sh      # Cadence environment (bash)
├── build.sh              # Build and test runner
├── netlists/             # Spectre simulation files (.scs)
├── ocean/                # OCEAN verification scripts (.ocn)
├── skill/                # Virtuoso SKILL scripts (.il)
├── scripts/              # Automation helpers
├── results/              # Simulation outputs
├── lib/                  # Reusable subcircuit library
└── my-workspace/         # Docs, tickets, logs
```

## Docs & Tracking

- Status: `my-workspace/docs/STATUS.md`
- Vision: `my-workspace/docs/vision.md`
- GPU spec: `my-workspace/docs/gpu-spec.md`
- Tickets: `my-workspace/tickets/`
- Logs: `my-workspace/logs/`
