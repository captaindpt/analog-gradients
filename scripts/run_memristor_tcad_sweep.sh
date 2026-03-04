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
#   MEMRISTOR_KEEP_TRANSIENT_SNAPSHOTS=1  # keep set_/reset_ per-step TDR/SAV files

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
TCAD_ROOT="$REPO_DIR/tcad/memristor"
TEMPLATES="$TCAD_ROOT/templates"
SWEEP_CSV="${MEMRISTOR_SWEEP_CSV:-$TCAD_ROOT/config/sweep_matrix_reram.csv}"

ROW_NUM="${1:?Usage: $0 <sweep_row_number>}"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
KEEP_TRANSIENT_SNAPSHOTS="${MEMRISTOR_KEEP_TRANSIENT_SNAPSHOTS:-0}"
SDEVICE_LOG_MODE="${MEMRISTOR_SDEVICE_LOG_MODE:-compact}"
SDEVICE_TIMEOUT_S="${MEMRISTOR_SDEVICE_TIMEOUT_S:-0}"
SDEVICE_THROTTLE_SPAM="${MEMRISTOR_SDEVICE_THROTTLE_SPAM:-1}"
SDEVICE_SPAM_SAMPLE_LINES="${MEMRISTOR_SDEVICE_SPAM_SAMPLE_LINES:-20}"
SDEVICE_SPAM_PROGRESS_INTERVAL="${MEMRISTOR_SDEVICE_SPAM_PROGRESS_INTERVAL:-10000}"
SDEVICE_LOG_MAX_MB="${MEMRISTOR_SDEVICE_LOG_MAX_MB:-512}"
SDEVICE_LOG_HEAD_LINES="${MEMRISTOR_SDEVICE_LOG_HEAD_LINES:-2000}"
SDEVICE_LOG_TAIL_LINES="${MEMRISTOR_SDEVICE_LOG_TAIL_LINES:-2000}"

sanitize_uint() {
  local value="$1"
  local fallback="$2"
  if [[ "$value" =~ ^[0-9]+$ ]]; then
    echo "$value"
  else
    echo "$fallback"
  fi
}

cap_log_file() {
  local file="$1"
  local max_mb="$2"
  local head_lines="$3"
  local tail_lines="$4"
  local size_bytes max_bytes tmp

  [[ -f "$file" ]] || return 0
  if [[ "$max_mb" -le 0 ]]; then
    return 0
  fi

  size_bytes=$(wc -c < "$file" 2>/dev/null || echo 0)
  max_bytes=$((max_mb * 1024 * 1024))
  if (( size_bytes <= max_bytes )); then
    return 0
  fi

  tmp="${file}.tmp.$$"
  {
    echo "[log-cap] original_size_bytes=$size_bytes cap_mb=$max_mb"
    echo "[log-cap] preserved_head_lines=$head_lines preserved_tail_lines=$tail_lines"
    echo "[log-cap] ---- BEGIN HEAD ----"
    sed -n "1,${head_lines}p" "$file"
    echo "[log-cap] ---- TRUNCATED ----"
    tail -n "$tail_lines" "$file"
    echo "[log-cap] ---- END TAIL ----"
  } > "$tmp"
  mv "$tmp" "$file"
}

SDEVICE_TIMEOUT_S="$(sanitize_uint "$SDEVICE_TIMEOUT_S" 0)"
SDEVICE_THROTTLE_SPAM="$(sanitize_uint "$SDEVICE_THROTTLE_SPAM" 1)"
SDEVICE_SPAM_SAMPLE_LINES="$(sanitize_uint "$SDEVICE_SPAM_SAMPLE_LINES" 20)"
SDEVICE_SPAM_PROGRESS_INTERVAL="$(sanitize_uint "$SDEVICE_SPAM_PROGRESS_INTERVAL" 10000)"
SDEVICE_LOG_MAX_MB="$(sanitize_uint "$SDEVICE_LOG_MAX_MB" 512)"
SDEVICE_LOG_HEAD_LINES="$(sanitize_uint "$SDEVICE_LOG_HEAD_LINES" 2000)"
SDEVICE_LOG_TAIL_LINES="$(sanitize_uint "$SDEVICE_LOG_TAIL_LINES" 2000)"

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

IFS=',' read -r _row PHASE SWEEP_GROUP OXIDE_T_NM LATERAL_NM GEN_FREQ GEN_EA GEN_DIPOLE \
  RECOMB_FREQ RECOMB_EA DIFF_EA FIL_GROWTH_EA FIL_GROWTH_FREQ FIL_RECESS_EA FIL_RECESS_FREQ SWEEP_VMAX \
  COMPLIANCE SET_TIME RESET_TIME INITIAL_VAC_CONC INITIAL_FIL_CONC MAX_TRAP_NUMBER NOTES <<< "$ROW_LINE"

for v in PHASE SWEEP_GROUP OXIDE_T_NM LATERAL_NM GEN_FREQ GEN_EA GEN_DIPOLE RECOMB_FREQ RECOMB_EA DIFF_EA FIL_GROWTH_EA FIL_GROWTH_FREQ FIL_RECESS_EA FIL_RECESS_FREQ SWEEP_VMAX COMPLIANCE SET_TIME RESET_TIME INITIAL_VAC_CONC INITIAL_FIL_CONC MAX_TRAP_NUMBER; do
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

if ! KMC_MAX_X=$(python3 - "$OXIDE_T_UM" <<'PY'
import sys
print(float(sys.argv[1]) + 0.005)
PY
); then
  echo "ERROR: failed to compute KMC_MAX_X from oxide_thickness_um '$OXIDE_T_UM' on row $ROW_NUM" >&2
  exit 1
fi

if ! LATERAL_UM=$(python3 - "$LATERAL_NM" <<'PY'
import sys
print(float(sys.argv[1]) / 1000.0)
PY
); then
  echo "ERROR: invalid lateral_nm '$LATERAL_NM' on row $ROW_NUM" >&2
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
echo "  lateral_nm:   $LATERAL_NM"
echo "  gen_ea:       $GEN_EA"
echo "  diff_ea:      $DIFF_EA"
echo "  fil_grow_ea:  $FIL_GROWTH_EA"
echo "  fil_grow_f:   $FIL_GROWTH_FREQ"
echo "  fil_rec_ea:   $FIL_RECESS_EA"
echo "  fil_rec_f:    $FIL_RECESS_FREQ"
echo "  init_vac:     $INITIAL_VAC_CONC"
echo "  init_fil:     $INITIAL_FIL_CONC"
echo "  max_traps:    $MAX_TRAP_NUMBER"
echo "  vmax:         $SWEEP_VMAX"
echo "  compliance:   $COMPLIANCE"

sed -e "s/%%OXIDE_THICKNESS_UM%%/${OXIDE_T_UM}/g" \
    -e "s/%%LATERAL_Y_UM%%/${LATERAL_UM}/g" \
    -e "s/%%LATERAL_Z_UM%%/${LATERAL_UM}/g" \
  "$TEMPLATES/mim_sde_3d.scm.tmpl" > "$RUN_DIR/mim.scm"

sed -e "s/%%OXIDE_THICKNESS_UM%%/${OXIDE_T_UM}/g" \
    -e "s/%%KMC_MAX_X%%/${KMC_MAX_X}/g" \
    -e "s/%%LATERAL_Y_UM%%/${LATERAL_UM}/g" \
    -e "s/%%LATERAL_Z_UM%%/${LATERAL_UM}/g" \
    -e "s/%%MAX_TRAP_NUMBER%%/${MAX_TRAP_NUMBER}/g" \
    -e "s/%%GEN_FREQ%%/${GEN_FREQ}/g" \
    -e "s/%%GEN_EA%%/${GEN_EA}/g" \
    -e "s/%%GEN_DIPOLE%%/${GEN_DIPOLE}/g" \
    -e "s/%%RECOMB_FREQ%%/${RECOMB_FREQ}/g" \
    -e "s/%%RECOMB_EA%%/${RECOMB_EA}/g" \
    -e "s/%%DIFF_EA%%/${DIFF_EA}/g" \
    -e "s/%%FIL_GROWTH_EA%%/${FIL_GROWTH_EA}/g" \
    -e "s/%%FIL_GROWTH_FREQ%%/${FIL_GROWTH_FREQ}/g" \
    -e "s/%%FIL_RECESS_EA%%/${FIL_RECESS_EA}/g" \
    -e "s/%%FIL_RECESS_FREQ%%/${FIL_RECESS_FREQ}/g" \
    -e "s/%%INITIAL_VAC_CONC%%/${INITIAL_VAC_CONC}/g" \
    -e "s/%%INITIAL_FIL_CONC%%/${INITIAL_FIL_CONC}/g" \
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
  SDEVICE_RC=0
  if [[ "$SDEVICE_LOG_MODE" == "full" ]]; then
    if [[ "$SDEVICE_THROTTLE_SPAM" == "1" ]]; then
      if [[ "$SDEVICE_TIMEOUT_S" -gt 0 ]]; then
        set +e
        timeout --signal=TERM --kill-after=60 "${SDEVICE_TIMEOUT_S}s" \
          sdevice mim_device.cmd 2>&1 | awk \
          -v sample_lines="$SDEVICE_SPAM_SAMPLE_LINES" \
          -v progress_interval="$SDEVICE_SPAM_PROGRESS_INTERVAL" '
            BEGIN { spam=0; shown=0; }
            /location is already occupied\. Discarded\./ {
              spam++;
              if (shown < sample_lines) {
                print;
                shown++;
                next;
              }
              if (progress_interval > 0 && (spam % progress_interval) == 0) {
                printf("[log-throttle] suppressed %d repeated location-is-occupied lines so far\n", spam - shown);
              }
              next;
            }
            { print; }
            END {
              if (spam > shown) {
                printf("[log-throttle] total_suppressed_repeated_lines=%d shown=%d\n", spam - shown, shown);
              }
            }
          ' > sdevice_stdout.log
        SDEVICE_RC=$?
        set -e
      else
        set +e
        sdevice mim_device.cmd 2>&1 | awk \
          -v sample_lines="$SDEVICE_SPAM_SAMPLE_LINES" \
          -v progress_interval="$SDEVICE_SPAM_PROGRESS_INTERVAL" '
            BEGIN { spam=0; shown=0; }
            /location is already occupied\. Discarded\./ {
              spam++;
              if (shown < sample_lines) {
                print;
                shown++;
                next;
              }
              if (progress_interval > 0 && (spam % progress_interval) == 0) {
                printf("[log-throttle] suppressed %d repeated location-is-occupied lines so far\n", spam - shown);
              }
              next;
            }
            { print; }
            END {
              if (spam > shown) {
                printf("[log-throttle] total_suppressed_repeated_lines=%d shown=%d\n", spam - shown, shown);
              }
            }
          ' > sdevice_stdout.log
        SDEVICE_RC=$?
        set -e
      fi
    else
      if [[ "$SDEVICE_TIMEOUT_S" -gt 0 ]]; then
        set +e
        timeout --signal=TERM --kill-after=60 "${SDEVICE_TIMEOUT_S}s" \
          sdevice mim_device.cmd > sdevice_stdout.log 2>&1
        SDEVICE_RC=$?
        set -e
      else
        set +e
        sdevice mim_device.cmd > sdevice_stdout.log 2>&1
        SDEVICE_RC=$?
        set -e
      fi
    fi
    if [[ "$SDEVICE_RC" -ne 0 ]]; then
      if [[ "$SDEVICE_RC" -eq 124 || "$SDEVICE_RC" -eq 137 ]]; then
        OUTCOME="FAIL:timeout"
      elif grep -q "Errors in parsing command file" sdevice_stdout.log 2>/dev/null; then
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
  else
    set +e
    if [[ "$SDEVICE_TIMEOUT_S" -gt 0 ]]; then
      timeout --signal=TERM --kill-after=60 "${SDEVICE_TIMEOUT_S}s" \
        sdevice mim_device.cmd 2>&1 | awk '
      NR <= 200 { print; next }
      /Errors in parsing command file/ { print; next }
      /Curve trace finished/ { print; next }
      /Good Bye/ { print; next }
      /total conductance/ { print; next }
      /KMC Events Summary/ { print; next }
      /FrenkelPair1 Bulk Generation count/ { print; next }
      /FrenkelPair1 Bulk Recombination count/ { print; next }
      /Oxygen diffusion count/ { print; next }
      /Vacancy diffusion count/ { print; next }
      /ImmobileVacancy Growth count/ { print; next }
      /ImmobileVacancy Recession count/ { print; next }
      /KMC Particles Summary/ { print; next }
      /Number of Oxygen/ { print; next }
      /Number of Vacancy/ { print; next }
      /Number of ImmobileVacancy/ { print; next }
      /contact        voltage/ { print; next }
      /^ top/ { print; next }
      /^ bottom/ { print; next }
      /Computing BE-step from/ { print; next }
      /ERROR/ { print; next }
      /Error/ { print; next }
    ' > sdevice_stdout.log
    else
      sdevice mim_device.cmd 2>&1 | awk '
      NR <= 200 { print; next }
      /Errors in parsing command file/ { print; next }
      /Curve trace finished/ { print; next }
      /Good Bye/ { print; next }
      /total conductance/ { print; next }
      /KMC Events Summary/ { print; next }
      /FrenkelPair1 Bulk Generation count/ { print; next }
      /FrenkelPair1 Bulk Recombination count/ { print; next }
      /Oxygen diffusion count/ { print; next }
      /Vacancy diffusion count/ { print; next }
      /ImmobileVacancy Growth count/ { print; next }
      /ImmobileVacancy Recession count/ { print; next }
      /KMC Particles Summary/ { print; next }
      /Number of Oxygen/ { print; next }
      /Number of Vacancy/ { print; next }
      /Number of ImmobileVacancy/ { print; next }
      /contact        voltage/ { print; next }
      /^ top/ { print; next }
      /^ bottom/ { print; next }
      /Computing BE-step from/ { print; next }
      /ERROR/ { print; next }
      /Error/ { print; next }
    ' > sdevice_stdout.log
    fi
    SDEVICE_RC=$?
    set -e
    if [[ "$SDEVICE_RC" -ne 0 ]]; then
      if [[ "$SDEVICE_RC" -eq 124 || "$SDEVICE_RC" -eq 137 ]]; then
        OUTCOME="FAIL:timeout"
      elif grep -q "Errors in parsing command file" sdevice_stdout.log 2>/dev/null; then
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
fi

popd > /dev/null

# Apply a final safety cap to avoid runaway logs filling the filesystem.
cap_log_file "$RUN_DIR/sdevice_stdout.log" \
  "$SDEVICE_LOG_MAX_MB" \
  "$SDEVICE_LOG_HEAD_LINES" \
  "$SDEVICE_LOG_TAIL_LINES"

# By default, delete transient per-step snapshots. They can create thousands
# of files and quickly exhaust disk/inodes in long KMC runs.
if [[ "$KEEP_TRANSIENT_SNAPSHOTS" != "1" ]]; then
  find "$RUN_DIR" -maxdepth 1 -type f \
    \( -name 'set_*_des.tdr' -o -name 'reset_*_des.tdr' -o \
       -name 'set_*_circuit_des.sav' -o -name 'reset_*_circuit_des.sav' \) \
    -delete
fi

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
lateral_nm=$LATERAL_NM
lateral_um=$LATERAL_UM
gen_freq=$GEN_FREQ
gen_ea=$GEN_EA
gen_dipole=$GEN_DIPOLE
recomb_freq=$RECOMB_FREQ
recomb_ea=$RECOMB_EA
diff_ea=$DIFF_EA
fil_growth_ea=$FIL_GROWTH_EA
fil_growth_freq=$FIL_GROWTH_FREQ
fil_recess_ea=$FIL_RECESS_EA
fil_recess_freq=$FIL_RECESS_FREQ
initial_vac_conc=$INITIAL_VAC_CONC
initial_fil_conc=$INITIAL_FIL_CONC
max_trap_number=$MAX_TRAP_NUMBER
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
keep_transient_snapshots=$KEEP_TRANSIENT_SNAPSHOTS
sdevice_log_mode=$SDEVICE_LOG_MODE
sdevice_timeout_s=$SDEVICE_TIMEOUT_S
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
