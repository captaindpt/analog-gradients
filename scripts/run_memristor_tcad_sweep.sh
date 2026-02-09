#!/usr/bin/env bash
set -euo pipefail
#
# Run one KMC ReRAM sweep point.
#
# Usage:
#   scripts/run_memristor_tcad_sweep.sh <sweep_row_number>
#
# Optional env:
#   MEMRISTOR_SWEEP_CSV=tcad/memristor/config/sweep_matrix_reram.csv

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TCAD_ROOT="$REPO_DIR/tcad/memristor"
TEMPLATES="$TCAD_ROOT/templates"
SWEEP_CSV="${MEMRISTOR_SWEEP_CSV:-$TCAD_ROOT/config/sweep_matrix_reram.csv}"

ROW_NUM="${1:?Usage: $0 <sweep_row_number>}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"

if ! command -v sde >/dev/null 2>&1; then
  echo "ERROR: sde not found. Run: source scripts/setup_sentaurus.sh" >&2
  exit 1
fi

for f in "$SWEEP_CSV" "$TEMPLATES/mim_sde_3d.scm.tmpl" "$TEMPLATES/mim_sdevice_reram.cmd.tmpl" "$TEMPLATES/reram.par"; do
  if [[ ! -f "$f" ]]; then
    echo "ERROR: required file missing: $f" >&2
    exit 1
  fi
done

ROW_LINE=$(awk -F',' -v r="$ROW_NUM" '$1 == r {print; exit}' "$SWEEP_CSV")
if [[ -z "$ROW_LINE" ]]; then
  echo "ERROR: row $ROW_NUM not found in $SWEEP_CSV" >&2
  exit 1
fi

IFS=',' read -r _row PHASE SWEEP_GROUP OXIDE_T_NM GEN_FREQ GEN_EA GEN_DIPOLE \
  RECOMB_FREQ RECOMB_EA DIFF_EA FIL_GROWTH_EA FIL_RECESS_EA SWEEP_VMAX \
  COMPLIANCE SET_TIME RESET_TIME NOTES <<< "$ROW_LINE"

for v in PHASE SWEEP_GROUP OXIDE_T_NM GEN_FREQ GEN_EA GEN_DIPOLE RECOMB_FREQ RECOMB_EA DIFF_EA FIL_GROWTH_EA FIL_RECESS_EA SWEEP_VMAX COMPLIANCE SET_TIME RESET_TIME; do
  if [[ -z "${!v}" ]]; then
    echo "ERROR: missing value for $v on row $ROW_NUM" >&2
    exit 1
  fi
done

if ! OXIDE_T_UM=$(python3 - "$OXIDE_T_NM" <<'PY'
import sys
print(float(sys.argv[1]) / 1000.0)
PY
); then
  echo "ERROR: invalid oxide_thickness_nm '$OXIDE_T_NM' on row $ROW_NUM" >&2
  exit 1
fi

if [[ "$PHASE" == "B" && "$ROW_NUM" == "1" ]]; then
  RUN_TAG="reram_baseline"
else
  RUN_TAG="reram_row${ROW_NUM}_${SWEEP_GROUP}"
fi
RUN_DIR="$TCAD_ROOT/runs/${TIMESTAMP}_${RUN_TAG}"
mkdir -p "$RUN_DIR"

WALL_START=$(date +%s)

echo "=== KMC ReRAM Run: row $ROW_NUM ==="
echo "  phase:        $PHASE"
echo "  sweep_group:  $SWEEP_GROUP"
echo "  oxide_nm:     $OXIDE_T_NM"
echo "  gen_ea:       $GEN_EA"
echo "  diff_ea:      $DIFF_EA"
echo "  fil_grow_ea:  $FIL_GROWTH_EA"
echo "  fil_rec_ea:   $FIL_RECESS_EA"
echo "  vmax:         $SWEEP_VMAX"
echo "  compliance:   $COMPLIANCE"

sed -e "s/%%OXIDE_THICKNESS_UM%%/${OXIDE_T_UM}/g" \
  "$TEMPLATES/mim_sde_3d.scm.tmpl" > "$RUN_DIR/mim.scm"

sed -e "s/%%OXIDE_THICKNESS_UM%%/${OXIDE_T_UM}/g" \
    -e "s/%%GEN_FREQ%%/${GEN_FREQ}/g" \
    -e "s/%%GEN_EA%%/${GEN_EA}/g" \
    -e "s/%%GEN_DIPOLE%%/${GEN_DIPOLE}/g" \
    -e "s/%%RECOMB_FREQ%%/${RECOMB_FREQ}/g" \
    -e "s/%%RECOMB_EA%%/${RECOMB_EA}/g" \
    -e "s/%%DIFF_EA%%/${DIFF_EA}/g" \
    -e "s/%%FIL_GROWTH_EA%%/${FIL_GROWTH_EA}/g" \
    -e "s/%%FIL_RECESS_EA%%/${FIL_RECESS_EA}/g" \
    -e "s/%%COMPLIANCE%%/${COMPLIANCE}/g" \
    -e "s/%%SET_TIME%%/${SET_TIME}/g" \
    -e "s/%%RESET_TIME%%/${RESET_TIME}/g" \
    -e "s/%%SWEEP_VMAX%%/${SWEEP_VMAX}/g" \
  "$TEMPLATES/mim_sdevice_reram.cmd.tmpl" > "$RUN_DIR/mim_device.cmd"

cp "$TEMPLATES/reram.par" "$RUN_DIR/reram.par"

OUTCOME="CONVERGED"
pushd "$RUN_DIR" > /dev/null

echo "--- Running SDE ---"
if ! sde -e -l mim.scm > sde.log 2>&1; then
  OUTCOME="FAIL:mesh"
fi

if [[ ! -f memdev_msh.tdr ]]; then
  OUTCOME="FAIL:mesh"
fi

if [[ "$OUTCOME" == "CONVERGED" ]]; then
  echo "--- Running SDevice ---"
  if ! sdevice mim_device.cmd > sdevice_stdout.log 2>&1; then
    if grep -q "Errors in parsing command file" sdevice_stdout.log 2>/dev/null; then
      OUTCOME="FAIL:syntax"
    else
      OUTCOME="FAIL:convergence"
    fi
  elif ! grep -q "Good Bye" sdevice_stdout.log 2>/dev/null; then
    if grep -q "Errors in parsing command file" sdevice_stdout.log 2>/dev/null; then
      OUTCOME="FAIL:syntax"
    else
      OUTCOME="FAIL:convergence"
    fi
  fi
fi

popd > /dev/null

SET_CURRENT_ABS_MAX_A="NA"
RESET_CURRENT_ABS_MAX_A="NA"
CURRENT_RATIO_SET_OVER_RESET="NA"
HAS_SET_CSV="no"
HAS_RESET_CSV="no"

if [[ "$OUTCOME" == "CONVERGED" ]]; then
  SET_PLT=""
  RESET_PLT=""
  for f in "$RUN_DIR/SET_des.plt" "$RUN_DIR/SETmemdev_des.plt" "$RUN_DIR/V-1_des.plt"; do
    if [[ -f "$f" ]]; then
      SET_PLT="$f"
      break
    fi
  done
  for f in "$RUN_DIR/RESET_des.plt" "$RUN_DIR/RESETmemdev_des.plt" "$RUN_DIR/V-2_des.plt"; do
    if [[ -f "$f" ]]; then
      RESET_PLT="$f"
      break
    fi
  done

  if [[ -n "$SET_PLT" ]]; then
    python3 "$REPO_DIR/scripts/extract_plt_to_csv.py" \
      "$SET_PLT" "$RUN_DIR/set_current.csv" \
      --electrode top >/dev/null 2>&1 || \
    python3 "$REPO_DIR/scripts/extract_plt_to_csv.py" \
      "$SET_PLT" "$RUN_DIR/set_current.csv" \
      --electrode anode >/dev/null 2>&1 || true
  fi

  if [[ -n "$RESET_PLT" ]]; then
    python3 "$REPO_DIR/scripts/extract_plt_to_csv.py" \
      "$RESET_PLT" "$RUN_DIR/reset_current.csv" \
      --electrode top >/dev/null 2>&1 || \
    python3 "$REPO_DIR/scripts/extract_plt_to_csv.py" \
      "$RESET_PLT" "$RUN_DIR/reset_current.csv" \
      --electrode anode >/dev/null 2>&1 || true
  fi

  if [[ -f "$RUN_DIR/set_current.csv" ]]; then
    HAS_SET_CSV="yes"
    SET_CURRENT_ABS_MAX_A=$(awk -F',' 'NR>1{v=$3+0; if(v<0) v=-v; if(v>m) m=v; n++} END{if(n>0) print m; else print "NA"}' "$RUN_DIR/set_current.csv")
  fi

  if [[ -f "$RUN_DIR/reset_current.csv" ]]; then
    HAS_RESET_CSV="yes"
    RESET_CURRENT_ABS_MAX_A=$(awk -F',' 'NR>1{v=$3+0; if(v<0) v=-v; if(v>m) m=v; n++} END{if(n>0) print m; else print "NA"}' "$RUN_DIR/reset_current.csv")
  fi

  if [[ "$SET_CURRENT_ABS_MAX_A" != "NA" && "$RESET_CURRENT_ABS_MAX_A" != "NA" ]]; then
    CURRENT_RATIO_SET_OVER_RESET=$(python3 - "$SET_CURRENT_ABS_MAX_A" "$RESET_CURRENT_ABS_MAX_A" <<'PY'
import sys
s = float(sys.argv[1])
r = float(sys.argv[2])
if r == 0:
    print("NA")
else:
    print(s / r)
PY
)
  fi
fi

WALL_END=$(date +%s)
WALL_TIME=$((WALL_END - WALL_START))

cat > "$RUN_DIR/manifest.txt" <<EOF_MANIFEST
run_id=$TIMESTAMP
sweep_row=$ROW_NUM
phase=$PHASE
sweep_group=$SWEEP_GROUP
oxide_thickness_nm=$OXIDE_T_NM
oxide_thickness_um=$OXIDE_T_UM
gen_freq=$GEN_FREQ
gen_ea=$GEN_EA
gen_dipole=$GEN_DIPOLE
recomb_freq=$RECOMB_FREQ
recomb_ea=$RECOMB_EA
diff_ea=$DIFF_EA
fil_growth_ea=$FIL_GROWTH_EA
fil_recess_ea=$FIL_RECESS_EA
sweep_vmax_v=$SWEEP_VMAX
compliance_a=$COMPLIANCE
set_time_s=$SET_TIME
reset_time_s=$RESET_TIME
outcome=$OUTCOME
wall_time_s=$WALL_TIME
has_set_csv=$HAS_SET_CSV
has_reset_csv=$HAS_RESET_CSV
set_current_abs_max_a=$SET_CURRENT_ABS_MAX_A
reset_current_abs_max_a=$RESET_CURRENT_ABS_MAX_A
current_ratio_set_over_reset=$CURRENT_RATIO_SET_OVER_RESET
notes=$NOTES
EOF_MANIFEST

echo
echo "=== Run Complete ==="
echo "  outcome: $OUTCOME"
echo "  run_dir: $RUN_DIR"
echo "  manifest: $RUN_DIR/manifest.txt"

if [[ "$OUTCOME" != "CONVERGED" ]]; then
  exit 1
fi
