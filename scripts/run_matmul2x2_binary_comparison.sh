#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="$REPO_DIR/competition/analysis"
OUT_MD="$OUT_DIR/matmul2x2_binary_comparison.md"
OUT_CSV="$OUT_DIR/matmul2x2_binary_comparison.csv"
DIGITAL_TXT="$REPO_DIR/results/matmul2x2_binary_digital_test.txt"
NEURO_TXT="$REPO_DIR/results/matmul2x2_binary_neuro_test.txt"

mkdir -p "$OUT_DIR"

"$REPO_DIR/build.sh" matmul2x2_binary_digital
"$REPO_DIR/build.sh" matmul2x2_binary_neuro

python3 - "$DIGITAL_TXT" "$NEURO_TXT" "$OUT_MD" "$OUT_CSV" <<'PY'
import csv
import datetime as dt
import re
import sys
from pathlib import Path

digital_txt = Path(sys.argv[1])
neuro_txt = Path(sys.argv[2])
out_md = Path(sys.argv[3])
out_csv = Path(sys.argv[4])

dig = digital_txt.read_text(encoding="utf-8")
neu = neuro_txt.read_text(encoding="utf-8")

def req_float(pattern, text, label):
    m = re.search(pattern, text)
    if not m:
        raise SystemExit(f"Missing {label} in report")
    return float(m.group(1))

def req_int(pattern, text, label):
    m = re.search(pattern, text)
    if not m:
        raise SystemExit(f"Missing {label} in report")
    return int(m.group(1))

dig_latency_ns = req_float(r"Latency to full output-valid:\s*([0-9.+-eE]+)\s*ns", dig, "digital latency")
neu_latency_ns = req_float(r"Latency to full output-valid:\s*([0-9.+-eE]+)\s*ns", neu, "neuro latency")

dig_energy_j = req_float(r"Total energy \(0-90ns\):\s*([0-9.+-eE]+)\s*J", dig, "digital energy")
neu_energy_j = req_float(r"Total energy \(0-90ns\):\s*([0-9.+-eE]+)\s*J", neu, "neuro energy")

dig_eop_j = req_float(r"Energy per operation \(12 ops\):\s*([0-9.+-eE]+)\s*J/op", dig, "digital energy/op")
neu_eop_j = req_float(r"Energy per operation \(12 ops\):\s*([0-9.+-eE]+)\s*J/op", neu, "neuro energy/op")

neu_spikes = req_int(r"Total partial spikes:\s*([0-9]+)", neu, "neuro total spikes")
neu_spike_est_j = req_float(
    r"Spike-model energy estimate \(3\.27 pJ/spike\):\s*([0-9.+-eE]+)\s*J",
    neu,
    "neuro spike estimate",
)

dig_out = re.search(r"Decoded output matrix:\s*\[\[([0-9]+)\s+([0-9]+)\]\s+\[([0-9]+)\s+([0-9]+)\]\]", dig)
neu_out = re.search(r"y11=([0-9]+)\s+y12=([0-9]+)\s+y21=([0-9]+)\s+y22=([0-9]+)", neu)
if not dig_out or not neu_out:
    raise SystemExit("Missing decoded output matrix values")
dig_matrix = tuple(int(dig_out.group(i)) for i in range(1, 5))
neu_matrix = tuple(int(neu_out.group(i)) for i in range(1, 5))

ops = 12
dig_energy_pj = dig_energy_j * 1e12
neu_energy_pj = neu_energy_j * 1e12
dig_eop_pj = dig_eop_j * 1e12
neu_eop_pj = neu_eop_j * 1e12
neu_spike_est_pj = neu_spike_est_j * 1e12

neuro_vs_digital_energy_pct = ((neu_energy_j - dig_energy_j) / dig_energy_j * 100.0) if dig_energy_j > 0 else 0.0
latency_ratio = (neu_latency_ns / dig_latency_ns) if dig_latency_ns > 0 else 0.0

rows = [
    {
        "architecture": "digital_baseline",
        "operations": ops,
        "latency_ns": f"{dig_latency_ns:.6f}",
        "energy_j": f"{dig_energy_j:.9e}",
        "energy_pj": f"{dig_energy_pj:.6f}",
        "energy_per_op_pj": f"{dig_eop_pj:.6f}",
        "spike_count": "",
        "spike_energy_est_pj": "",
        "decoded_matrix": f"[[{dig_matrix[0]} {dig_matrix[1]}] [{dig_matrix[2]} {dig_matrix[3]}]]",
        "result_file": str(digital_txt),
    },
    {
        "architecture": "neuro_path",
        "operations": ops,
        "latency_ns": f"{neu_latency_ns:.6f}",
        "energy_j": f"{neu_energy_j:.9e}",
        "energy_pj": f"{neu_energy_pj:.6f}",
        "energy_per_op_pj": f"{neu_eop_pj:.6f}",
        "spike_count": str(neu_spikes),
        "spike_energy_est_pj": f"{neu_spike_est_pj:.6f}",
        "decoded_matrix": f"[[{neu_matrix[0]} {neu_matrix[1]}] [{neu_matrix[2]} {neu_matrix[3]}]]",
        "result_file": str(neuro_txt),
    },
]

with out_csv.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    for r in rows:
        w.writerow(r)

lines = []
lines.append("# Binary 2x2 Matmul: Digital vs Neuro Comparison")
lines.append("")
lines.append(f"Generated: {dt.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
lines.append("")
lines.append("Scope: binary-only first proof (`A,B ∈ {0,1}`), fixed stimulus point:")
lines.append("- A = `[[1,0],[1,1]]`")
lines.append("- B = `[[1,1],[0,1]]`")
lines.append("- Expected Y = `[[1,1],[1,2]]`")
lines.append("")
lines.append("| Metric | Digital Baseline | Neuro Path |")
lines.append("|--------|------------------|------------|")
lines.append(f"| Operations | {ops} | {ops} |")
lines.append(f"| Decoded output | `[[{dig_matrix[0]} {dig_matrix[1]}] [{dig_matrix[2]} {dig_matrix[3]}]]` | `[[{neu_matrix[0]} {neu_matrix[1]}] [{neu_matrix[2]} {neu_matrix[3]}]]` |")
lines.append(f"| Latency to full output-valid | {dig_latency_ns:.3f} ns | {neu_latency_ns:.3f} ns |")
lines.append(f"| Measured energy (0-90ns) | {dig_energy_pj:.3f} pJ | {neu_energy_pj:.3f} pJ |")
lines.append(f"| Energy / op (12 ops) | {dig_eop_pj:.3f} pJ/op | {neu_eop_pj:.3f} pJ/op |")
lines.append(f"| Neuro partial spikes | n/a | {neu_spikes} |")
lines.append(f"| Neuro spike-model estimate | n/a | {neu_spike_est_pj:.3f} pJ |")
lines.append("")
lines.append("Derived deltas:")
lines.append(f"- Neuro measured energy vs digital: `{neuro_vs_digital_energy_pct:+.2f}%` (negative means lower).")
lines.append(f"- Neuro/digital latency ratio: `{latency_ratio:.3f}x`.")
lines.append("- Caveat: this digital baseline is a minimal combinational transistor netlist, not a clocked PE-array workload.")
lines.append("")
lines.append("Reproduce:")
lines.append("- `./build.sh matmul2x2_binary_digital`")
lines.append("- `./build.sh matmul2x2_binary_neuro`")
lines.append("- `scripts/run_matmul2x2_binary_comparison.sh`")
lines.append("")
lines.append("Sources:")
lines.append(f"- `{digital_txt}`")
lines.append(f"- `{neuro_txt}`")
lines.append(f"- `{out_csv}`")

out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY

echo "Binary matmul comparison complete:"
echo "  report: $OUT_MD"
echo "  csv:    $OUT_CSV"
