#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="$REPO_DIR/competition/analysis"
OUT_TXT="$OUT_DIR/lif_energy_summary.txt"
OUT_MD="$OUT_DIR/lif_energy_summary.md"
ENERGY_NETLIST="$REPO_DIR/results/lif_neuron/lif_neuron_energy_tmp.scs"
ENERGY_RAW="$REPO_DIR/results/lif_neuron/lif_neuron_energy.raw"

mkdir -p "$OUT_DIR"

source "$REPO_DIR/setup_cadence.sh"

# Ensure waveform data is current.
"$REPO_DIR/build.sh" lif_neuron >/dev/null

# Build a temporary netlist variant that saves supply current for energy analysis.
REPO_DIR="$REPO_DIR" python3 - <<'PY'
from pathlib import Path
import os
repo = Path(os.environ["REPO_DIR"])
src = (repo / "netlists" / "lif_neuron.scs").read_text(encoding="utf-8")
src = src.replace("save mem spike out", "save mem spike out V_VDD:p")
(repo / "results" / "lif_neuron" / "lif_neuron_energy_tmp.scs").write_text(src, encoding="utf-8")
PY

(cd "$REPO_DIR/results/lif_neuron" && spectre "$ENERGY_NETLIST" -raw "$ENERGY_RAW" +log spectre_energy.log >/dev/null)
ocean -nograph < "$REPO_DIR/ocean/extract_lif_energy.ocn" >/dev/null

total_j="$(grep -m1 "Total energy" "$OUT_TXT" | awk '{print $4}')"
spikes="$(grep -m1 "Detected spikes" "$OUT_TXT" | awk '{print $3}')"
eps_j="$(grep "Energy per spike:" "$OUT_TXT" | head -n1 | awk '{print $4}')"
eps_pj="$(grep "Energy per spike:" "$OUT_TXT" | tail -n1 | awk '{print $4}')"

cat > "$OUT_MD" <<EOF
# LIF Energy Summary

Source artifact: \`$OUT_TXT\`

- Total energy (0-200ns): \`$total_j\` J
- Detected spikes: \`$spikes\`
- Energy per spike: \`$eps_j\` J (\`$eps_pj\` pJ)

Method:
- Integrate \`P(t) = VDD * (-I(V_VDD))\` over the transient window.
- Count spikes from \`spike\` threshold crossings at 0.9V.
EOF

# Cleanup temporary simulation artifacts used only for energy extraction.
rm -f "$ENERGY_NETLIST" "$REPO_DIR/results/lif_neuron/spectre_energy.log"
rm -rf "$ENERGY_RAW"

echo "Wrote:"
echo "  $OUT_TXT"
echo "  $OUT_MD"
