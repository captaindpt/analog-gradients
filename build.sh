#!/usr/bin/env bash
# build.sh - Master build and verification runner
# Usage: ./build.sh [component]

set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")" && pwd)"
NETLISTS="$REPO_DIR/netlists"
OCEAN_DIR="$REPO_DIR/ocean"
RESULTS_DIR="$REPO_DIR/results"
RUNLOG_DIR="$RESULTS_DIR/_runlogs"

source "$REPO_DIR/setup_cadence.sh"

RED=""
GREEN=""
YELLOW=""
NC=""
if [[ -t 1 ]]; then
  RED='\033[0;31m'
  GREEN='\033[0;32m'
  YELLOW='\033[1;33m'
  NC='\033[0m'
fi

COMPONENT="${1:-all}"
RUN_ID="$(date +%Y%m%d_%H%M%S)"
RUN_LOG="$RUNLOG_DIR/build_${COMPONENT}_${RUN_ID}.log"
RUN_MANIFEST="$RUNLOG_DIR/build_${COMPONENT}_${RUN_ID}.manifest.txt"
BUILD_STATUS="FAILED"

mkdir -p "$RUNLOG_DIR"
exec > >(tee -a "$RUN_LOG") 2>&1

finish_run() {
  {
    echo "end_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
    echo "status=$BUILD_STATUS"
    echo "log=$RUN_LOG"
  } >> "$RUN_MANIFEST"
}
trap finish_run EXIT

{
  echo "run_id=$RUN_ID"
  echo "component=$COMPONENT"
  echo "start_utc=$(date -u +%Y-%m-%dT%H:%M:%SZ)"
  echo "repo=$REPO_DIR"
  echo "host=$(hostname)"
  echo "user=${USER:-unknown}"
  echo "git_head=$(git -C "$REPO_DIR" rev-parse --short HEAD 2>/dev/null || echo unknown)"
  echo "git_dirty=$(git -C "$REPO_DIR" diff --quiet && echo clean || echo dirty)"
  echo "records:"
} > "$RUN_MANIFEST"

component_result_path() {
  local name="$1"
  if [[ "$name" == "inverter" ]]; then
    echo "$RESULTS_DIR/inverter_verify.txt"
  else
    echo "$RESULTS_DIR/${name}_test.txt"
  fi
}

component_ocean_path() {
  local name="$1"
  if [[ "$name" == "inverter" ]]; then
    echo "$OCEAN_DIR/verify_inverter.ocn"
  else
    echo "$OCEAN_DIR/test_${name}.ocn"
  fi
}

raw_marker_file() {
  local raw_dir="$1"
  local marker="$raw_dir/tran_test.tran.tran.psfxl"
  if [[ -f "$marker" ]]; then
    echo "$marker"
    return 0
  fi
  find "$raw_dir" -type f ! -name "logFile" 2>/dev/null | head -n 1
}

check_verification_result() {
  local result_file="$1"
  local verdict_lines
  local verdict_count
  local verdict
  local last_nonempty

  verdict_lines="$(grep -E '^=== (PASS|FAIL):' "$result_file" || true)"
  verdict_count="$(printf '%s\n' "$verdict_lines" | sed '/^$/d' | wc -l | tr -d ' ')"
  if [[ "$verdict_count" != "1" ]]; then
    echo "Invalid verification output: expected exactly one final verdict line."
    echo "Found $verdict_count verdict lines in $result_file"
    return 1
  fi

  verdict="$(printf '%s\n' "$verdict_lines" | awk '{print $2}' | tr -d ':')"
  if [[ "$verdict" != "PASS" ]]; then
    echo "Verification verdict is not PASS: $verdict"
    return 1
  fi

  last_nonempty="$(sed '/^[[:space:]]*$/d' "$result_file" | tail -n 1)"
  if [[ -z "$last_nonempty" || ! "$last_nonempty" =~ ^===\ (PASS|FAIL): ]]; then
    echo "Invalid verification output: missing terminal verdict line."
    return 1
  fi
  if [[ ! "$last_nonempty" =~ ^===\ PASS: ]]; then
    echo "Invalid verification output: terminal verdict is not PASS."
    return 1
  fi

  # Any explicit per-check FAIL marker invalidates the result even if a PASS line exists.
  if grep -q '\[FAIL\]' "$result_file"; then
    echo "Per-check failure markers detected in $result_file"
    return 1
  fi
  if grep -q 'FAIL:' "$result_file"; then
    echo "Failure markers detected in $result_file"
    return 1
  fi
  if grep -q '^ERROR:' "$result_file"; then
    echo "Error markers detected in $result_file"
    return 1
  fi

  return 0
}

check_spectre_log_strict() {
  local spectre_log="$1"
  local allowlist_file="$REPO_DIR/config/spectre_warning_allowlist.txt"
  local failed=0
  local entry
  local warning_line
  local re

  # Strict policy: every Spectre warning code is fatal unless allowlisted.
  while IFS= read -r entry; do
    warning_line="${entry#*:}"
    local allowlisted=0

    if [[ -f "$allowlist_file" ]]; then
      while IFS= read -r re; do
        [[ -z "$re" || "$re" =~ ^[[:space:]]*# ]] && continue
        if [[ "$warning_line" =~ $re ]]; then
          allowlisted=1
          break
        fi
      done < "$allowlist_file"
    fi

    if (( allowlisted == 0 )); then
      echo "Strict Spectre policy violation: unallowlisted warning"
      echo "$entry"
      failed=1
    fi
  done < <(grep -En 'WARNING \(SPECTRE-[0-9]+' "$spectre_log" || true)

  if (( failed != 0 )); then
    return 1
  fi
  return 0
}

spectre_warning_counts() {
  local spectre_log="$1"
  grep -Eo 'WARNING \(SPECTRE-[0-9]+\)' "$spectre_log" \
    | sed -E 's/.*\((SPECTRE-[0-9]+)\).*/\1/' \
    | sort \
    | uniq -c \
    | awk '{print $2 " " $1}'
}

spectre_warning_summary() {
  local spectre_log="$1"
  local summary=""
  local code
  local count
  while read -r code count; do
    [[ -z "${code:-}" ]] && continue
    if [[ -n "$summary" ]]; then
      summary="${summary};"
    fi
    summary="${summary}${code}:${count}"
  done < <(spectre_warning_counts "$spectre_log")

  if [[ -z "$summary" ]]; then
    echo "none"
  else
    echo "$summary"
  fi
}

baseline_warning_count() {
  local baseline_file="$1"
  local component="$2"
  local code="$3"
  awk -F',' -v comp="$component" -v warn_code="$code" '
    BEGIN { found=0 }
    $0 ~ /^#/ { next }
    NF < 3 { next }
    {
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", $1)
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", $2)
      gsub(/^[[:space:]]+|[[:space:]]+$/, "", $3)
    }
    $1 == "component" && $2 == "code" { next }
    $1 == comp && $2 == warn_code {
      print $3
      found=1
      exit 0
    }
    END {
      if (!found) {
        print 0
      }
    }
  ' "$baseline_file"
}

check_spectre_warning_baseline() {
  local component="$1"
  local spectre_log="$2"
  local baseline_file="${SPECTRE_WARNING_BASELINE_FILE:-$REPO_DIR/config/spectre_warning_baseline.csv}"
  local failed=0
  local code
  local count
  local baseline_count

  if [[ ! -f "$baseline_file" ]]; then
    echo "Missing Spectre warning baseline file: $baseline_file"
    return 1
  fi

  while read -r code count; do
    [[ -z "${code:-}" ]] && continue
    baseline_count="$(baseline_warning_count "$baseline_file" "$component" "$code")"
    if [[ ! "$baseline_count" =~ ^[0-9]+$ ]]; then
      echo "Invalid baseline count for $component/$code in $baseline_file: $baseline_count"
      return 1
    fi
    if (( count > baseline_count )); then
      echo "Strict Spectre baseline violation: $component $code count increased ($count > $baseline_count)"
      failed=1
    fi
  done < <(spectre_warning_counts "$spectre_log")

  if (( failed != 0 )); then
    return 1
  fi
  return 0
}

check_ocean_log() {
  local ocean_log="$1"
  # OCEAN can report runtime script failures while still exiting 0.
  if grep -q '\*Error\*' "$ocean_log"; then
    echo "OCEAN runtime errors detected in $ocean_log"
    return 1
  fi
  return 0
}

run_component() {
  local name="$1"
  local netlist="$NETLISTS/${name}.scs"
  local ocean_script
  local result_file
  local comp_dir
  local raw_dir
  local spectre_log
  local ocean_log
  local sim_start
  local ocean_start
  local marker
  local marker_mtime
  local result_mtime
  local warning_summary

  ocean_script="$(component_ocean_path "$name")"
  result_file="$(component_result_path "$name")"
  comp_dir="$RESULTS_DIR/$name"
  raw_dir="$comp_dir/${name}.raw"
  spectre_log="$comp_dir/spectre.log"
  ocean_log="$comp_dir/ocean.log"

  echo -e "${YELLOW}=== Building $name ===${NC}"

  if [[ ! -f "$netlist" ]]; then
    echo -e "${RED}Missing netlist: $netlist${NC}"
    return 1
  fi
  if [[ ! -f "$ocean_script" ]]; then
    echo -e "${RED}Missing OCEAN script: $ocean_script${NC}"
    return 1
  fi

  mkdir -p "$comp_dir"

  # Fail closed on stale artifacts.
  rm -rf "$raw_dir"
  rm -f "$spectre_log" "$ocean_log" "$result_file"

  echo "Running Spectre simulation..."
  sim_start="$(date +%s)"
  if ! (cd "$comp_dir" && spectre "$netlist" -raw "${name}.raw" +log spectre.log >/dev/null 2>&1); then
    echo -e "${RED}Simulation: FAILED${NC}"
    return 1
  fi

  if ! grep -q "completes with 0 errors" "$spectre_log"; then
    echo -e "${RED}Simulation: FAILED${NC}"
    tail -n 20 "$spectre_log" || true
    return 1
  fi
  if ! check_spectre_log_strict "$spectre_log"; then
    echo -e "${RED}Simulation: FAILED (strict warning policy)${NC}"
    return 1
  fi
  if ! check_spectre_warning_baseline "$name" "$spectre_log"; then
    echo -e "${RED}Simulation: FAILED (warning baseline drift)${NC}"
    return 1
  fi
  warning_summary="$(spectre_warning_summary "$spectre_log")"

  marker="$(raw_marker_file "$raw_dir")"
  if [[ -z "$marker" || ! -f "$marker" ]]; then
    echo -e "${RED}Simulation: FAILED (missing raw marker)${NC}"
    return 1
  fi
  marker_mtime="$(stat -c %Y "$marker")"
  if (( marker_mtime < sim_start )); then
    echo -e "${RED}Simulation: FAILED (stale raw marker)${NC}"
    echo "  marker=$marker mtime=$marker_mtime start=$sim_start"
    return 1
  fi
  echo -e "${GREEN}Simulation: OK${NC}"

  echo "Running OCEAN verification..."
  ocean_start="$(date +%s)"
  if ! (cd "$REPO_DIR" && ocean -nograph < "$ocean_script" > "$ocean_log" 2>&1); then
    echo -e "${RED}Verification: FAILED${NC}"
    tail -n 50 "$ocean_log" || true
    return 1
  fi
  if ! check_ocean_log "$ocean_log"; then
    echo -e "${RED}Verification: FAILED${NC}"
    tail -n 50 "$ocean_log" || true
    return 1
  fi

  if [[ ! -f "$result_file" ]]; then
    echo -e "${RED}Verification: FAILED (missing result file)${NC}"
    return 1
  fi
  result_mtime="$(stat -c %Y "$result_file")"
  if (( result_mtime < ocean_start )); then
    echo -e "${RED}Verification: FAILED (stale result file)${NC}"
    echo "  result=$result_file mtime=$result_mtime start=$ocean_start"
    return 1
  fi
  if ! check_verification_result "$result_file"; then
    echo -e "${RED}Verification: FAILED${NC}"
    cat "$result_file"
    return 1
  fi
  echo -e "${GREEN}Verification: PASS${NC}"

  {
    echo "  - component=$name,status=PASS,raw=$raw_dir,raw_marker=$marker,result=$result_file,warnings=$warning_summary"
  } >> "$RUN_MANIFEST"
  echo ""
}

run_sequence() {
  local level_name="$1"
  shift
  local components=("$@")
  echo "$level_name"
  echo "=================================="
  local comp
  for comp in "${components[@]}"; do
    run_component "$comp"
  done
  echo ""
}

echo "========================================"
echo "GPU Building Blocks - Build & Test"
echo "========================================"
echo "Run log: $RUN_LOG"
echo "Run manifest: $RUN_MANIFEST"
echo ""

case "$COMPONENT" in
  inverter|nand2|nor2|and2|or2|xor2|xnor2|mux2|half_adder|full_adder|alu1|alu4|pe1|pe4|gpu_core|synapse|lif_neuron|neuron_tile|neuro_tile4|neuro_tile4_coupled|neuro_tile4_mixed_signal|coincidence_detector|xor_spike2|matmul2x2_binary_neuro|matmul2x2_binary_digital)
    run_component "$COMPONENT"
    ;;
  all)
    run_sequence "Building Level 5: CMOS primitives" inverter nand2 nor2
    run_sequence "Building Level 4: Logic gates" and2 or2 xor2 xnor2
    run_sequence "Building Level 3: Blocks" mux2 half_adder full_adder
    run_sequence "Building Level 2: RTL Components" alu1 alu4
    run_sequence "Building Level 1: Functional Blocks" pe1 pe4
    run_sequence "Building Level 0: System" gpu_core
    run_sequence "Building Competition Analog Primitives" synapse lif_neuron
    run_sequence "Building Competition Analog Compositions" neuron_tile neuro_tile4 neuro_tile4_coupled neuro_tile4_mixed_signal coincidence_detector xor_spike2 matmul2x2_binary_neuro
    run_sequence "Building Binary Matmul Comparison Baselines" matmul2x2_binary_digital
    echo "=================================="
    echo -e "${GREEN}All Level 0-5 components + analog competition path verified!${NC}"
    ;;
  *)
    echo "Unknown component: $COMPONENT"
    echo "Available: inverter, nand2, nor2, and2, or2, xor2, xnor2, mux2, half_adder, full_adder, alu1, alu4, pe1, pe4, gpu_core, synapse, lif_neuron, neuron_tile, neuro_tile4, neuro_tile4_coupled, neuro_tile4_mixed_signal, coincidence_detector, xor_spike2, matmul2x2_binary_neuro, matmul2x2_binary_digital, all"
    exit 1
    ;;
esac

BUILD_STATUS="PASS"
