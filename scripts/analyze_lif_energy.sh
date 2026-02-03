#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="$REPO_DIR/competition/analysis"
OUT_TXT="$OUT_DIR/lif_energy_summary.txt"
OUT_MD="$OUT_DIR/lif_energy_summary.md"
OUT_BOOT_CSV="$OUT_DIR/lif_energy_bootstrap.csv"
TRACE_CSV="$OUT_DIR/lif_energy_trace.csv"
ENERGY_NETLIST="$REPO_DIR/results/lif_neuron/lif_neuron_energy_tmp.scs"
ENERGY_RAW="$REPO_DIR/results/lif_neuron/lif_neuron_energy.raw"

mkdir -p "$OUT_DIR"

source "$REPO_DIR/setup_cadence.sh"

# Ensure waveform data is current.
"$REPO_DIR/build.sh" lif_neuron >/dev/null

# Temporary netlist variant that saves supply current for energy analysis.
REPO_DIR="$REPO_DIR" python3 - <<'PY'
from pathlib import Path
import os
repo = Path(os.environ["REPO_DIR"])
src = (repo / "netlists" / "lif_neuron.scs").read_text(encoding="utf-8")
src = src.replace("save mem spike out", "save mem spike out V_VDD:p")
(repo / "results" / "lif_neuron" / "lif_neuron_energy_tmp.scs").write_text(src, encoding="utf-8")
PY

(cd "$REPO_DIR/results/lif_neuron" && spectre "$ENERGY_NETLIST" -raw "$ENERGY_RAW" +log spectre_energy.log >/dev/null 2>&1)
ocean -nograph < "$REPO_DIR/ocean/extract_lif_energy.ocn" >/dev/null

python3 "$REPO_DIR/scripts/analyze_lif_energy_trace.py" \
  --trace-csv "$TRACE_CSV" \
  --summary-txt "$OUT_TXT" \
  --summary-md "$OUT_MD" \
  --bootstrap-csv "$OUT_BOOT_CSV" \
  --title "LIF Energy Summary"

# Cleanup temporary simulation artifacts used only for energy extraction.
rm -f "$ENERGY_NETLIST" "$REPO_DIR/results/lif_neuron/spectre_energy.log"
rm -rf "$ENERGY_RAW"

echo "Wrote:"
echo "  $OUT_TXT"
echo "  $OUT_MD"
echo "  $OUT_BOOT_CSV"
