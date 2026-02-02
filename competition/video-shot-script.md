# NeuroCore Video Shot Script (3 Minutes)

Use this runbook to record a clean "one terminal" demo.

## Pre-Flight (Before Recording)

```bash
source setup_cadence.sh
scripts/run_competition_visuals.sh
scripts/run_fullflow_smoke.sh
scripts/build_recording_pack.sh
```

Confirm these exist before filming:
- `competition/plots/neuro_tile4_coupled_spikes.svg`
- `competition/plots/neuro_tile4_coupled_mems.svg`
- `implementation/fullflow_demo/work/innovus/out/alu4_flow_demo.gds`
- `competition/recording-pack/`

## Scene 1 (0:00-0:30) - The Stack

Commands:

```bash
source setup_cadence.sh
./build.sh all
```

Capture cue:
- Keep terminal full-screen and let PASS lines scroll.

Voice cue:
- "This is a full verified stack: digital blocks and analog neurons."

## Scene 2 (0:30-1:15) - The Analog Brain

Commands:

```bash
ls -1 competition/plots
```

Capture cue:
- Show `neuro_tile4_coupled_spikes.svg` and `neuro_tile4_coupled_mems.svg`.
- Call out staggered first spikes (27.5 -> 29.5 -> 31.5 -> 33.5 ns).

Voice cue:
- "Channel-0 drive propagates across the coupled tile in sequence."

## Scene 3 (1:15-2:15) - The Semiconductor Flow

Commands:

```bash
scripts/run_fullflow_smoke.sh
ls -la implementation/fullflow_demo/work/innovus/out/alu4_flow_demo.gds
```

Capture cue:
- Show Innovus stage start banner and final GDS output line.
- If GUI access is available, include short placement/routing clips from Innovus.

Voice cue:
- "This is synthesis, place/route, and physical flow automation in one run."

## Scene 4 (2:15-2:45) - The Point

Slide/text cue:
- "One engineer. One terminal. Transistors to GDS."
- "Ready for shuttle-level execution with production licenses."

## Scene 5 (2:45-3:00) - Close

Slide/text cue:
- "NeuroCore: Analog AI on standard CMOS"
- Contact + ICTGC ask.

## Recording Notes

- Use fast-forward/time-lapse only inside long tool runs.
- Keep command font large and high contrast.
- Keep one consistent prompt format across scenes.
- Guided mode: `scripts/demo_narrator.sh`
