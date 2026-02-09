#!/usr/bin/env bash
set -euo pipefail
#
# Run a single memristor TCAD sweep point.
#
# Usage:
#   scripts/run_memristor_tcad_sweep.sh <sweep_row_number>
#
# Prerequisites:
#   source scripts/setup_sentaurus.sh
#
# Reads parameters from tcad/memristor/config/sweep_matrix.csv row N,
# generates decks from templates, runs SDE -> snmesh -> SDevice,
# extracts I-V data, and saves everything to a timestamped run directory.

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TCAD_ROOT="$REPO_DIR/tcad/memristor"
SWEEP_CSV="$TCAD_ROOT/config/sweep_matrix.csv"
TEMPLATES="$TCAD_ROOT/templates"

ROW_NUM="${1:?Usage: $0 <sweep_row_number>}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"

scale_value() {
  local base="${1:-}"
  local factor="${2:-}"
  python3 - "$base" "$factor" <<'PY'
import sys

base = float(sys.argv[1])
factor = float(sys.argv[2])
value = "{:g}".format(base * factor)
print(value.replace("e+", "e"))
PY
}

resolve_symbol() {
  local raw="${1:-}"
  case "$raw" in
    BEST_P1) echo "${BEST_P1:-}" ;;
    BEST_P2_TRAP) echo "${BEST_P2_TRAP:-}" ;;
    BEST_P2_ENERGY) echo "${BEST_P2_ENERGY:-}" ;;
    BEST_P3_VAC) echo "${BEST_P3_VAC:-}" ;;
    BEST_P3_MOB) echo "${BEST_P3_MOB:-}" ;;
    BEST_P4_VAC) echo "${BEST_P4_VAC:-${BEST_P3_VAC:-}}" ;;
    BEST_P4_MOB) echo "${BEST_P4_MOB:-${BEST_P3_MOB:-}}" ;;
    REFINE_VAC_LO) scale_value "${BEST_P3_VAC:-}" "0.5" ;;
    REFINE_VAC_HI) scale_value "${BEST_P3_VAC:-}" "2.0" ;;
    REFINE_MOB_LO) scale_value "${BEST_P3_MOB:-}" "0.5" ;;
    REFINE_MOB_HI) scale_value "${BEST_P3_MOB:-}" "2.0" ;;
    *) echo "$raw" ;;
  esac
}

# --- Verify Sentaurus is on PATH ---
if ! command -v sde &>/dev/null; then
  echo "ERROR: sde not found. Run: source scripts/setup_sentaurus.sh" >&2
  exit 1
fi

# --- Read sweep matrix row ---
# CSV columns: row,phase,oxide_material,oxide_thickness_nm,trap_density_cm3,
#   trap_energy_ev_below_cb,vacancy_conc_cm3,vacancy_mobility_cm2vs,
#   sweep_type,sweep_vmax_v,sweep_cycles,notes

ROW_LINE=$(awk -F',' -v r="$ROW_NUM" '$1 == r' "$SWEEP_CSV")

if [[ -z "$ROW_LINE" ]]; then
  echo "ERROR: Row $ROW_NUM not found in $SWEEP_CSV" >&2
  exit 1
fi

# Parse CSV fields
IFS=',' read -r _row PHASE OXIDE_MAT OXIDE_T_NM TRAP_DENS TRAP_ENERGY \
  VAC_CONC VAC_MOB SWEEP_TYPE SWEEP_VMAX SWEEP_CYCLES NOTES <<< "$ROW_LINE"

OXIDE_T_NM="$(resolve_symbol "$OXIDE_T_NM")"
TRAP_DENS="$(resolve_symbol "$TRAP_DENS")"
TRAP_ENERGY="$(resolve_symbol "$TRAP_ENERGY")"
VAC_CONC="$(resolve_symbol "$VAC_CONC")"
VAC_MOB="$(resolve_symbol "$VAC_MOB")"

for _name in OXIDE_T_NM TRAP_DENS TRAP_ENERGY VAC_CONC VAC_MOB; do
  _value="${!_name}"
  if [[ "$_value" =~ ^(BEST_|REFINE_) ]]; then
    echo "ERROR: unresolved sweep placeholder '$_value' for $_name on row $ROW_NUM" >&2
    echo "Set required BEST_* variables in the environment before running." >&2
    exit 1
  fi
done

echo "=== Memristor TCAD Run: Row $ROW_NUM (Phase $PHASE) ==="
echo "  Material:   $OXIDE_MAT"
echo "  Thickness:  ${OXIDE_T_NM}nm"
echo "  Traps:      density=$TRAP_DENS energy=$TRAP_ENERGY"
echo "  Vacancies:  conc=$VAC_CONC mobility=$VAC_MOB"
echo "  Sweep:      $SWEEP_TYPE Vmax=$SWEEP_VMAX cycles=$SWEEP_CYCLES"
echo "  Notes:      $NOTES"

# --- Create run directory ---
RUN_TAG="phase${PHASE}_row${ROW_NUM}"
RUN_DIR="$TCAD_ROOT/runs/${TIMESTAMP}_${RUN_TAG}"
mkdir -p "$RUN_DIR"

WALL_START=$(date +%s)

# --- Convert oxide thickness to um for SDE ---
if ! OXIDE_T_UM=$(python3 - "$OXIDE_T_NM" <<'PY'
import sys

value_nm = float(sys.argv[1])
print(value_nm / 1000.0)
PY
); then
  echo "ERROR: invalid oxide thickness '$OXIDE_T_NM' on row $ROW_NUM" >&2
  exit 1
fi

# --- Generate SDE deck ---
sed "s/%%OXIDE_THICKNESS_UM%%/${OXIDE_T_UM}/g" \
  "$TEMPLATES/mim_sde.scm.tmpl" > "$RUN_DIR/mim.scm"

# --- Select and generate SDevice deck ---
case "$PHASE" in
  1)
    TMPL="$TEMPLATES/mim_sdevice_phase1.cmd.tmpl"
    sed "s/%%SWEEP_VMAX%%/${SWEEP_VMAX}/g" "$TMPL" > "$RUN_DIR/mim_device.cmd"
    ;;
  2)
    TMPL="$TEMPLATES/mim_sdevice_phase2.cmd.tmpl"
    sed -e "s/%%SWEEP_VMAX%%/${SWEEP_VMAX}/g" \
        -e "s/%%TRAP_DENSITY%%/${TRAP_DENS}/g" \
        -e "s/%%TRAP_ENERGY_EV%%/${TRAP_ENERGY}/g" \
        "$TMPL" > "$RUN_DIR/mim_device.cmd"
    ;;
  3)
    TMPL="$TEMPLATES/mim_sdevice_phase3.cmd.tmpl"
    sed -e "s/%%SWEEP_VMAX%%/${SWEEP_VMAX}/g" \
        -e "s/%%TRAP_DENSITY%%/${TRAP_DENS}/g" \
        -e "s/%%TRAP_ENERGY_EV%%/${TRAP_ENERGY}/g" \
        -e "s/%%VACANCY_CONC%%/${VAC_CONC}/g" \
        -e "s/%%VACANCY_MOBILITY%%/${VAC_MOB}/g" \
        "$TMPL" > "$RUN_DIR/mim_device.cmd"
    ;;
  4|5)
    # Phase 4 and 5 reuse phase 3 template (or phase 5 pulse template when created)
    TMPL="$TEMPLATES/mim_sdevice_phase3.cmd.tmpl"
    sed -e "s/%%SWEEP_VMAX%%/${SWEEP_VMAX}/g" \
        -e "s/%%TRAP_DENSITY%%/${TRAP_DENS}/g" \
        -e "s/%%TRAP_ENERGY_EV%%/${TRAP_ENERGY}/g" \
        -e "s/%%VACANCY_CONC%%/${VAC_CONC}/g" \
        -e "s/%%VACANCY_MOBILITY%%/${VAC_MOB}/g" \
        "$TMPL" > "$RUN_DIR/mim_device.cmd"
    ;;
  *)
    echo "ERROR: Unknown phase $PHASE" >&2
    exit 1
    ;;
esac

# --- Run SDE (geometry + mesh) ---
OUTCOME="CONVERGED"
echo ""
echo "--- Running SDE (geometry + mesh) ---"
pushd "$RUN_DIR" > /dev/null

if ! sde -e -l mim.scm > sde.log 2>&1; then
  echo "WARNING: SDE exited with error"
  OUTCOME="FAIL:mesh"
fi

# Check mesh output exists
if [[ ! -f memdev_msh.tdr ]]; then
  echo "ERROR: Mesh file not produced"
  OUTCOME="FAIL:mesh"
fi

# --- Run SDevice (physics simulation) ---
if [[ "$OUTCOME" == "CONVERGED" ]]; then
  echo "--- Running SDevice (physics) ---"
  if ! sdevice mim_device.cmd > sdevice_stdout.log 2>&1; then
    echo "WARNING: SDevice exited with error"
    OUTCOME="FAIL:convergence"
  fi

  # Check for successful completion
  if [[ -f sdevice.log ]]; then
    # SDevice writes its own log file
    if ! grep -q "Good Bye" sdevice.log 2>/dev/null; then
      # Sometimes log goes to stdout capture
      if ! grep -q "Good Bye" sdevice_stdout.log 2>/dev/null; then
        OUTCOME="FAIL:convergence"
      fi
    fi
  else
    # Log might be in stdout capture
    if ! grep -q "Good Bye" sdevice_stdout.log 2>/dev/null; then
      OUTCOME="FAIL:convergence"
    fi
  fi
fi

popd > /dev/null

# --- Extract I-V data ---
if [[ "$OUTCOME" == "CONVERGED" && -f "$RUN_DIR/memdev_des.plt" ]]; then
  echo "--- Extracting I-V data ---"
  ELECTRODE="top"
  python3 "$REPO_DIR/scripts/extract_plt_to_csv.py" \
    "$RUN_DIR/memdev_des.plt" "$RUN_DIR/iv_data.csv" \
    --electrode "$ELECTRODE" 2>&1 || {
      echo "WARNING: PLT extraction failed, trying 'left' electrode"
      python3 "$REPO_DIR/scripts/extract_plt_to_csv.py" \
        "$RUN_DIR/memdev_des.plt" "$RUN_DIR/iv_data.csv" \
        --electrode "left" 2>&1 || true
    }
fi

# --- Run waveform analysis ---
if [[ -f "$RUN_DIR/iv_data.csv" ]]; then
  echo "--- Analyzing waveform ---"
  python3 "$REPO_DIR/scripts/analyze_memristor_waveform.py" \
    --csv "$RUN_DIR/iv_data.csv" \
    --out-json "$RUN_DIR/metrics.json" \
    --out-md "$RUN_DIR/metrics.md" 2>&1 || true
fi

# --- Write manifest ---
WALL_END=$(date +%s)
WALL_TIME=$((WALL_END - WALL_START))

cat > "$RUN_DIR/manifest.txt" <<EOF
run_id=$TIMESTAMP
sweep_row=$ROW_NUM
phase=$PHASE
oxide_material=$OXIDE_MAT
oxide_thickness_nm=$OXIDE_T_NM
trap_density_cm3=$TRAP_DENS
trap_energy_ev_below_cb=$TRAP_ENERGY
vacancy_conc_cm3=$VAC_CONC
vacancy_mobility_cm2vs=$VAC_MOB
sweep_type=$SWEEP_TYPE
sweep_vmax_v=$SWEEP_VMAX
sweep_cycles=$SWEEP_CYCLES
outcome=$OUTCOME
wall_time_s=$WALL_TIME
notes=$NOTES
has_iv_data=$(test -f "$RUN_DIR/iv_data.csv" && echo "yes" || echo "no")
has_metrics=$(test -f "$RUN_DIR/metrics.json" && echo "yes" || echo "no")
EOF

echo ""
echo "=== Run Complete ==="
echo "  Outcome:  $OUTCOME"
echo "  Wall time: ${WALL_TIME}s"
echo "  Run dir:  $RUN_DIR"
echo "  Manifest: $RUN_DIR/manifest.txt"

if [[ "$OUTCOME" != "CONVERGED" ]]; then
  exit 1
fi
