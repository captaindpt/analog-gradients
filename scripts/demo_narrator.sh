#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PACK_DIR="$REPO_DIR/competition/recording-pack"
SKIP_LONG="${DEMO_SKIP_LONG:-0}"

banner() {
  local title="$1"
  echo
  echo "==================================================="
  echo "$title"
  echo "==================================================="
}

wait_enter() {
  local prompt="$1"
  read -r -p "$prompt" _
}

run_cmd() {
  local cmd="$1"
  echo
  echo "$ $cmd"
  if [[ "$SKIP_LONG" == "1" ]]; then
    echo "[SKIP] DEMO_SKIP_LONG=1"
    return 0
  fi
  bash -lc "$cmd"
}

echo "NeuroCore demo narrator mode"
echo "Recording pack: $PACK_DIR"
echo "Tip: run DEMO_SKIP_LONG=1 for dry rehearsal."

banner "SCENE 1 (0:00-0:30) - THE STACK"
echo "Voice cue: full verified stack, automated PASS cascade."
wait_enter "Press ENTER to run ./build.sh all "
run_cmd "cd '$REPO_DIR' && source setup_cadence.sh && ./build.sh all"
wait_enter "Scene 1 complete. Press ENTER for Scene 2 "

banner "SCENE 2 (0:30-1:15) - THE ANALOG BRAIN"
echo "Voice cue: coupled-neuron propagation and staggered spikes."
echo "Open these assets in your viewer:"
echo "  $PACK_DIR/02-waveforms/neuro_tile4_coupled_spikes.svg"
echo "  $PACK_DIR/02-waveforms/neuro_tile4_coupled_mems.svg"
run_cmd "ls -la '$PACK_DIR/02-waveforms/' | sed -n '1,80p'"
wait_enter "Press ENTER once waveform visuals are on screen "
wait_enter "Scene 2 complete. Press ENTER for Scene 3 "

banner "SCENE 3 (1:15-2:15) - THE FLOW"
echo "Voice cue: synthesis, place/route, and GDS artifact path."
wait_enter "Press ENTER to run full-flow smoke orchestration "
run_cmd "cd '$REPO_DIR' && scripts/run_fullflow_smoke.sh"
run_cmd "ls -la '$REPO_DIR/implementation/fullflow_demo/work/innovus/out/alu4_flow_demo.gds'"
wait_enter "Scene 3 complete. Press ENTER for Scene 4 "

banner "SCENE 4 (2:15-2:45) - THE POINT"
echo "Read from:"
echo "  $REPO_DIR/competition/voiceover-script.md"
echo "  $PACK_DIR/04-slides/title-card.txt"
wait_enter "Press ENTER when Scene 4 delivery is complete "

banner "SCENE 5 (2:45-3:00) - CLOSE"
echo "Read from:"
echo "  $PACK_DIR/04-slides/close-card.txt"
wait_enter "Press ENTER to finish demo narrator run "

echo
echo "Demo narrator run complete."
