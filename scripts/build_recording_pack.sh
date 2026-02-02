#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
PACK_DIR="$REPO_DIR/competition/recording-pack"
BUILD_DIR="$PACK_DIR/01-build-all"
WAVE_DIR="$PACK_DIR/02-waveforms"
FLOW_DIR="$PACK_DIR/03-innovus"
SLIDE_DIR="$PACK_DIR/04-slides"

mkdir -p "$BUILD_DIR" "$WAVE_DIR" "$FLOW_DIR" "$SLIDE_DIR"

cp "$REPO_DIR/competition/plots/"*.svg "$WAVE_DIR/"
python3 "$REPO_DIR/scripts/render_waveform_pngs.py" \
  --data-dir "$REPO_DIR/competition/data" \
  --out-dir "$WAVE_DIR"

cp "$REPO_DIR/competition/full-flow-smoke-evidence.md" "$FLOW_DIR/"
cp "$REPO_DIR/implementation/fullflow_demo/work/innovus/out/alu4_flow_demo.def" "$FLOW_DIR/"
cp "$REPO_DIR/implementation/fullflow_demo/work/innovus/out/alu4_flow_demo.gds" "$FLOW_DIR/"
cp "$REPO_DIR/implementation/fullflow_demo/work/innovus/out/alu4_flow_demo_postroute.v" "$FLOW_DIR/"
cp "$REPO_DIR/implementation/fullflow_demo/work/innovus/reports/alu4_flow_demo_area.rpt" "$FLOW_DIR/"
cp "$REPO_DIR/implementation/fullflow_demo/work/innovus/reports/alu4_flow_demo_power.rpt" "$FLOW_DIR/"
cp "$REPO_DIR/implementation/fullflow_demo/work/innovus/reports/alu4_flow_demo_timing.rpt" "$FLOW_DIR/"

cp "$REPO_DIR/competition/video-shot-script.md" "$PACK_DIR/"
cp "$REPO_DIR/competition/voiceover-script.md" "$PACK_DIR/"

cat > "$BUILD_DIR/run_scene1.sh" <<'EOF'
#!/usr/bin/env bash
set -euo pipefail
source setup_cadence.sh
./build.sh all
EOF
chmod +x "$BUILD_DIR/run_scene1.sh"

echo "Recording pack is ready at: $PACK_DIR"
