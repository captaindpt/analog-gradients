#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
NETLIST_SRC="$REPO_DIR/netlists/lif_neuron.scs"
RESULT_ROOT="$REPO_DIR/results/lif_neuron_corners"
ANALYSIS_ROOT="$REPO_DIR/competition/analysis/lif_corners"
RUN_TS="$(date +%Y%m%d_%H%M%S)"
RUN_RESULT_DIR="$RESULT_ROOT/$RUN_TS"
RUN_ANALYSIS_DIR="$ANALYSIS_ROOT/$RUN_TS"
RUN_MANIFEST="$RUN_ANALYSIS_DIR/run_manifest.txt"
SUMMARY_CSV="$RUN_ANALYSIS_DIR/lif_corner_summary.csv"
SUMMARY_MD="$RUN_ANALYSIS_DIR/lif_corner_summary.md"

RLEAK_LIST="${RLEAK_LIST:-8M,10M,12M}"
IIN_LIST="${IIN_LIST:-400u,500u,600u}"

IFS=',' read -r -a rleak_vals <<< "$RLEAK_LIST"
IFS=',' read -r -a iin_vals <<< "$IIN_LIST"

mkdir -p "$RUN_RESULT_DIR" "$RUN_ANALYSIS_DIR"

source "$REPO_DIR/setup_cadence.sh"

{
  echo "run_id=$RUN_TS"
  echo "start_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "rleak_list=$RLEAK_LIST"
  echo "iin_list=$IIN_LIST"
  echo "result_root=$RUN_RESULT_DIR"
  echo "analysis_root=$RUN_ANALYSIS_DIR"
} > "$RUN_MANIFEST"

echo "corner_id,rleak,iin_amp,spike_count,energy_per_spike_pj,energy_ci95_low_pj,energy_ci95_high_pj,ode_global_r2,ode_piecewise_r2,ode_delta_r2,ode_global_rmse_v,ode_piecewise_rmse_v,raw_dir,analysis_dir" > "$SUMMARY_CSV"

for rleak in "${rleak_vals[@]}"; do
  for iin in "${iin_vals[@]}"; do
    corner_id="rleak_${rleak}_iin_${iin}"
    corner_tag="$(printf '%s' "$corner_id" | tr -c 'A-Za-z0-9._-' '_')"
    corner_res="$RUN_RESULT_DIR/$corner_tag"
    corner_ana="$RUN_ANALYSIS_DIR/$corner_tag"
    mkdir -p "$corner_res" "$corner_ana"

    netlist="$corner_res/lif_neuron_${corner_tag}.scs"
    raw_dir="$corner_res/lif_neuron.raw"
    spectre_log="$corner_res/spectre.log"

    wave_csv="$corner_ana/lif_neuron_waveform.csv"
    trace_csv="$corner_ana/lif_energy_trace.csv"
    ode_trace="$corner_ana/lif_ode_fit_trace.csv"
    ode_summary="$corner_ana/lif_ode_fit_summary.md"
    energy_txt="$corner_ana/lif_energy_summary.txt"
    energy_md="$corner_ana/lif_energy_summary.md"
    energy_boot="$corner_ana/lif_energy_bootstrap.csv"
    ocean_log="$corner_ana/ocean_extract.log"

    sed -e "s/^parameters .*/parameters vdd_val=1.8 cmem=1p rleak=${rleak} iin_amp=${iin}/" \
        -e "s/^save mem spike out$/save mem spike out V_VDD:p/" \
      "$NETLIST_SRC" > "$netlist"

    rm -rf "$raw_dir"
    rm -f "$wave_csv" "$trace_csv" "$ode_trace" "$ode_summary" "$energy_txt" "$energy_md" "$energy_boot" "$ocean_log"
    sim_start_epoch="$(date +%s)"
    (
      cd "$corner_res"
      spectre "$netlist" -raw lif_neuron.raw +log spectre.log >/dev/null 2>&1
    )

    if ! grep -q "completes with 0 errors" "$spectre_log"; then
      echo "Corner failed (spectre errors): $corner_id"
      continue
    fi
    raw_psfxl="$raw_dir/tran_test.tran.tran.psfxl"
    if [[ ! -f "$raw_psfxl" ]] || (( $(stat -c %Y "$raw_psfxl") < sim_start_epoch )); then
      echo "Corner failed (stale/missing raw): $corner_id"
      continue
    fi

    ocean_start_epoch="$(date +%s)"
    LIF_CORNER_RAW="$raw_dir" \
    LIF_CORNER_WAVE_CSV="$wave_csv" \
    LIF_CORNER_ENERGY_TRACE="$trace_csv" \
      ocean -nograph < "$REPO_DIR/ocean/extract_lif_corner_metrics.ocn" >"$ocean_log" 2>&1

    if [[ ! -f "$wave_csv" || ! -f "$trace_csv" ]]; then
      echo "Corner failed (missing extracted CSV): $corner_id"
      tail -n 50 "$ocean_log" || true
      continue
    fi
    if (( $(stat -c %Y "$wave_csv") < ocean_start_epoch )) || (( $(stat -c %Y "$trace_csv") < ocean_start_epoch )); then
      echo "Corner failed (stale extracted CSV): $corner_id"
      tail -n 50 "$ocean_log" || true
      continue
    fi

    python3 "$REPO_DIR/scripts/analyze_lif_ode_fit.py" \
      --input-csv "$wave_csv" \
      --trace-out "$ode_trace" \
      --summary-out "$ode_summary" >/dev/null

    python3 "$REPO_DIR/scripts/analyze_lif_energy_trace.py" \
      --trace-csv "$trace_csv" \
      --summary-txt "$energy_txt" \
      --summary-md "$energy_md" \
      --bootstrap-csv "$energy_boot" \
      --title "LIF Energy Summary (${corner_id})" >/dev/null

    row="$(python3 - "$corner_id" "$rleak" "$iin" "$ode_summary" "$energy_md" "$raw_dir" "$corner_ana" <<'PY'
import re
import sys
from pathlib import Path

corner_id, rleak, iin, ode_path, en_path, raw_dir, ana_dir = sys.argv[1:]
ode = Path(ode_path).read_text(encoding="utf-8")
en = Path(en_path).read_text(encoding="utf-8")

def grab(text, pat, default="nan"):
    m = re.search(pat, text, re.MULTILINE)
    return m.group(1) if m else default

spikes = grab(en, r"Detected spikes: `([^`]+)`")
eps_pj = grab(en, r"Energy per spike \(total/spike\): `[^`]+` J \(`([^`]+)` pJ\)")
ci_lo_j = grab(en, r"Bootstrap 95% CI: `\[([^,]+),")
ci_hi_j = grab(en, r"Bootstrap 95% CI: `\[[^,]+, ([^\]]+)\]` J")
g_r2 = grab(ode, r"- derivative R\^2 = ([0-9eE+\-.]+)")
p_r2 = grab(ode, r"- piecewise derivative R\^2 = ([0-9eE+\-.]+)")
g_rmse = grab(ode, r"- one-step reconstruction RMSE = ([0-9eE+\-.]+) V")
p_rmse = grab(ode, r"- piecewise one-step reconstruction RMSE = ([0-9eE+\-.]+) V")
try:
    delta = f"{float(p_r2) - float(g_r2):.6f}"
except Exception:
    delta = "nan"
try:
    ci_lo_pj = f"{float(ci_lo_j) * 1e12:.6f}"
except Exception:
    ci_lo_pj = "nan"
try:
    ci_hi_pj = f"{float(ci_hi_j) * 1e12:.6f}"
except Exception:
    ci_hi_pj = "nan"

print(",".join([
    corner_id, rleak, iin, spikes, eps_pj, ci_lo_pj, ci_hi_pj,
    g_r2, p_r2, delta, g_rmse, p_rmse, raw_dir, ana_dir
]))
PY
)"
    echo "$row" >> "$SUMMARY_CSV"
  done
done

python3 - "$SUMMARY_CSV" "$SUMMARY_MD" <<'PY'
import csv
import sys
from pathlib import Path

csv_path = Path(sys.argv[1])
md_path = Path(sys.argv[2])
rows = list(csv.DictReader(csv_path.open("r", encoding="utf-8")))

lines = []
lines.append("# LIF Corner Evidence Summary")
lines.append("")
lines.append(f"Total corners: {len(rows)}")
lines.append("")
lines.append("| Corner | rleak | iin_amp | Spikes | Energy/spike (pJ) | CI95 low (pJ) | CI95 high (pJ) | ODE R2 global | ODE R2 piecewise | Delta R2 |")
lines.append("|--------|-------|---------|--------|--------------------|---------------|----------------|---------------|------------------|----------|")
for r in rows:
    lines.append(
        f"| {r['corner_id']} | {r['rleak']} | {r['iin_amp']} | {r['spike_count']} | {r['energy_per_spike_pj']} | {r['energy_ci95_low_pj']} | {r['energy_ci95_high_pj']} | {r['ode_global_r2']} | {r['ode_piecewise_r2']} | {r['ode_delta_r2']} |"
    )
lines.append("")
lines.append(f"CSV source: `{csv_path}`")
md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
PY

{
  echo "end_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "summary_csv=$SUMMARY_CSV"
  echo "summary_md=$SUMMARY_MD"
} >> "$RUN_MANIFEST"

echo "Corner evidence run complete:"
echo "  $RUN_ANALYSIS_DIR"
echo "  $SUMMARY_CSV"
echo "  $SUMMARY_MD"
