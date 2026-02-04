#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUT_DIR="$REPO_DIR/competition/analysis"
OUT_MD="$OUT_DIR/matmul4x4_binary_comparison.md"
OUT_CSV="$OUT_DIR/matmul4x4_binary_comparison.csv"
DIGITAL_TXT="$REPO_DIR/results/matmul4x4_binary_digital_test.txt"
NEURO_TXT="$REPO_DIR/results/matmul4x4_binary_neuro_test.txt"

mkdir -p "$OUT_DIR"

"$REPO_DIR/build.sh" matmul4x4_binary_digital
"$REPO_DIR/build.sh" matmul4x4_binary_neuro

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
        raise SystemExit("Missing {} in report".format(label))
    return float(m.group(1))


def req_int(pattern, text, label):
    m = re.search(pattern, text)
    if not m:
        raise SystemExit("Missing {} in report".format(label))
    return int(m.group(1))


def req_vector(text, label):
    m = re.search(r"Decoded output vector:\s*([0-9 ]+)", text)
    if not m:
        raise SystemExit("Missing decoded output vector in {}".format(label))
    vals = [int(x) for x in m.group(1).split()]
    if len(vals) != 16:
        raise SystemExit("Decoded vector in {} does not have 16 entries".format(label))
    return vals


expected = [2, 2, 2, 3, 1, 1, 2, 1, 1, 3, 2, 2, 1, 2, 1, 2]
ops = 112

dig_latency_ns = req_float(r"Latency to full output-valid:\s*([0-9.+-eE]+)\s*ns", dig, "digital latency")
neu_latency_ns = req_float(r"Latency to full output-valid:\s*([0-9.+-eE]+)\s*ns", neu, "neuro latency")

dig_energy_j = req_float(r"Total energy \(0-120ns\):\s*([0-9.+-eE]+)\s*J", dig, "digital energy")
neu_energy_j = req_float(r"Total energy \(0-120ns\):\s*([0-9.+-eE]+)\s*J", neu, "neuro energy")

dig_eop_j = req_float(r"Energy per operation \(112 ops\):\s*([0-9.+-eE]+)\s*J/op", dig, "digital energy/op")
neu_eop_j = req_float(r"Energy per operation \(112 ops\):\s*([0-9.+-eE]+)\s*J/op", neu, "neuro energy/op")

neu_spikes = req_int(r"Total partial spikes:\s*([0-9]+)", neu, "neuro total spikes")
neu_spike_est_j = req_float(
    r"Spike-model energy estimate \(3\.27 pJ/spike\):\s*([0-9.+-eE]+)\s*J",
    neu,
    "neuro spike estimate",
)

dig_vec = req_vector(dig, "digital")
neu_vec = req_vector(neu, "neuro")

dig_ok = (dig_vec == expected)
neu_ok = (neu_vec == expected)

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
        "decoded_ok": str(dig_ok),
        "latency_ns": "{:.6f}".format(dig_latency_ns),
        "energy_j": "{:.9e}".format(dig_energy_j),
        "energy_pj": "{:.6f}".format(dig_energy_pj),
        "energy_per_op_pj": "{:.6f}".format(dig_eop_pj),
        "spike_count": "",
        "spike_energy_est_pj": "",
        "decoded_vector": " ".join(str(v) for v in dig_vec),
        "result_file": str(digital_txt),
    },
    {
        "architecture": "neuro_path",
        "operations": ops,
        "decoded_ok": str(neu_ok),
        "latency_ns": "{:.6f}".format(neu_latency_ns),
        "energy_j": "{:.9e}".format(neu_energy_j),
        "energy_pj": "{:.6f}".format(neu_energy_pj),
        "energy_per_op_pj": "{:.6f}".format(neu_eop_pj),
        "spike_count": str(neu_spikes),
        "spike_energy_est_pj": "{:.6f}".format(neu_spike_est_pj),
        "decoded_vector": " ".join(str(v) for v in neu_vec),
        "result_file": str(neuro_txt),
    },
]

with out_csv.open("w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
    w.writeheader()
    for r in rows:
        w.writerow(r)

lines = []
lines.append("# Binary 4x4 Matmul: Digital vs Neuro Checkpoint")
lines.append("")
lines.append("Generated: {}".format(dt.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")))
lines.append("")
lines.append("Scope: binary-only transistor checkpoint (`A,B ∈ {0,1}`), fixed stimulus point.")
lines.append("- A = `[[1,0,1,1],[0,1,1,0],[1,1,0,1],[1,0,0,1]]`")
lines.append("- B = `[[1,1,0,1],[0,1,1,0],[1,0,1,1],[0,1,1,1]]`")
lines.append("- Expected Y = `[[2,2,2,3],[1,1,2,1],[1,3,2,2],[1,2,1,2]]`")
lines.append("")
lines.append("| Metric | Digital Baseline | Neuro Path |")
lines.append("|--------|------------------|------------|")
lines.append("| Operations | {} | {} |".format(ops, ops))
lines.append("| Decoded output match | `{}` | `{}` |".format(dig_ok, neu_ok))
lines.append("| Latency to full output-valid | {:.3f} ns | {:.3f} ns |".format(dig_latency_ns, neu_latency_ns))
lines.append("| Measured energy (0-120ns) | {:.3f} pJ | {:.3f} pJ |".format(dig_energy_pj, neu_energy_pj))
lines.append("| Energy / op (112 ops) | {:.3f} pJ/op | {:.3f} pJ/op |".format(dig_eop_pj, neu_eop_pj))
lines.append("| Neuro partial spikes | n/a | {} |".format(neu_spikes))
lines.append("| Neuro spike-model estimate | n/a | {:.3f} pJ |".format(neu_spike_est_pj))
lines.append("")
lines.append("Derived deltas:")
lines.append("- Neuro measured energy vs digital: `{:+.2f}%`.".format(neuro_vs_digital_energy_pct))
lines.append("- Neuro/digital latency ratio: `{:.3f}x`.".format(latency_ratio))
lines.append("")
lines.append("Reproduce:")
lines.append("- `./build.sh matmul4x4_binary_digital`")
lines.append("- `./build.sh matmul4x4_binary_neuro`")
lines.append("- `scripts/run_matmul4x4_binary_comparison.sh`")
lines.append("")
lines.append("Sources:")
lines.append("- `{}`".format(digital_txt))
lines.append("- `{}`".format(neuro_txt))
lines.append("- `{}`".format(out_csv))

out_md.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY

echo "Binary 4x4 matmul comparison complete:"
echo "  report: $OUT_MD"
echo "  csv:    $OUT_CSV"
