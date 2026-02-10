#!/usr/bin/env bash
set -euo pipefail

# Remove transient per-step Sentaurus KMC snapshot files that can consume
# significant disk/inode resources.
#
# Usage:
#   scripts/prune_memristor_snapshots.sh            # dry-run summary only
#   scripts/prune_memristor_snapshots.sh --apply    # delete matching files

ROOT_DIR="${1:-tcad/memristor/runs}"
APPLY=0

if [[ "${1:-}" == "--apply" ]]; then
  ROOT_DIR="tcad/memristor/runs"
  APPLY=1
elif [[ "${2:-}" == "--apply" ]]; then
  APPLY=1
fi

if [[ ! -d "$ROOT_DIR" ]]; then
  echo "ERROR: directory not found: $ROOT_DIR" >&2
  exit 1
fi

TMP_LIST="$(mktemp)"
trap 'rm -f "$TMP_LIST"' EXIT

find "$ROOT_DIR" -type f \
  \( -name 'set_*_des.tdr' -o -name 'reset_*_des.tdr' -o \
     -name 'set_*_circuit_des.sav' -o -name 'reset_*_circuit_des.sav' \) \
  -print > "$TMP_LIST"

COUNT="$(wc -l < "$TMP_LIST")"
echo "root=$ROOT_DIR"
echo "candidate_files=$COUNT"

if [[ "$COUNT" -eq 0 ]]; then
  echo "No transient snapshot files found."
  exit 0
fi

BYTES="$(xargs -a "$TMP_LIST" stat -c '%s' | awk '{s+=$1} END{print s+0}')"
HUMAN="$(awk -v b="$BYTES" 'function h(x){s=\"B KMGTPE\";while(x>=1024&&length(s)>1){x/=1024;s=substr(s,3)}return sprintf(\"%.1f%s\",x,substr(s,1,1))} BEGIN{print h(b)}')"
echo "candidate_bytes=$BYTES ($HUMAN)"

if [[ "$APPLY" -ne 1 ]]; then
  echo "dry_run=true"
  echo "Use --apply to delete candidates."
  exit 0
fi

xargs -a "$TMP_LIST" rm -f
echo "deleted_files=$COUNT"
