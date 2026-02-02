#!/usr/bin/env bash
set -euo pipefail

REPO_DIR="$(cd "$(dirname "$0")/.." && pwd)"
OUT_FILE="$REPO_DIR/competition/metrics-summary.md"

synapse_file="$REPO_DIR/results/synapse_test.txt"
lif_file="$REPO_DIR/results/lif_neuron_test.txt"
tile_file="$REPO_DIR/results/neuron_tile_test.txt"
tile4_file="$REPO_DIR/results/neuro_tile4_test.txt"
tile4c_file="$REPO_DIR/results/neuro_tile4_coupled_test.txt"

require_file() {
    local file="$1"
    if [[ ! -f "$file" ]]; then
        echo "Missing required result file: $file" >&2
        exit 1
    fi
}

require_file "$synapse_file"
require_file "$lif_file"
require_file "$tile_file"
require_file "$tile4_file"
require_file "$tile4c_file"

synapse_vpost_max="$(grep -m1 "Vpost max" "$synapse_file" | awk -F: '{print $2}' | xargs)"
synapse_pulses="$(grep -m1 "Output pulse count" "$synapse_file" | awk -F: '{print $2}' | xargs)"

lif_spikes="$(grep -m1 "Total spikes detected" "$lif_file" | awk -F: '{print $2}' | xargs)"
lif_vmem_max="$(grep -m1 "Max membrane voltage" "$lif_file" | awk -F: '{print $2}' | xargs)"

tile_spikes="$(grep -m1 "Spike node pulses detected" "$tile_file" | awk -F: '{print $2}' | xargs)"
tile_vmem_max="$(grep -m1 "Vmem max" "$tile_file" | awk -F: '{print $2}' | xargs)"

tile4_first_spikes="$(grep -m1 "First spike times" "$tile4_file" | awk -F: '{print $2}' | xargs)"
tile4_spike0="$(grep -m1 "spike0:" "$tile4_file" | awk -F: '{print $2}' | xargs)"
tile4_spike1="$(grep -m1 "spike1:" "$tile4_file" | awk -F: '{print $2}' | xargs)"
tile4_spike2="$(grep -m1 "spike2:" "$tile4_file" | awk -F: '{print $2}' | xargs)"
tile4_spike3="$(grep -m1 "spike3:" "$tile4_file" | awk -F: '{print $2}' | xargs)"

tile4c_mem_max="$(grep -m1 "Membrane maxima" "$tile4c_file" | awk -F: '{print $2}' | xargs)"
tile4c_spike_counts="$(grep -m1 "spike0=" "$tile4c_file" | xargs)"
tile4c_spike_max="$(grep -m1 "Spike maxima" "$tile4c_file" | awk -F: '{print $2}' | xargs)"

generated_ts="$(date -u +"%Y-%m-%d %H:%M:%S UTC")"

cat > "$OUT_FILE" <<EOF
# Competition Metrics Summary

Generated: $generated_ts

## Analog Primitive Metrics

| Block | Key Metric | Value |
|------|------------|-------|
| Synapse | Vpost max | $synapse_vpost_max |
| Synapse | Output pulse count | $synapse_pulses |
| LIF Neuron | Total spikes detected | $lif_spikes |
| LIF Neuron | Max membrane voltage | $lif_vmem_max |

## Composition Metrics

| Block | Key Metric | Value |
|------|------------|-------|
| Neuron Tile | Spike node pulses detected | $tile_spikes |
| Neuron Tile | Vmem max | $tile_vmem_max |
| Neuro Tile4 | First spike times (ns) | $tile4_first_spikes |
| Neuro Tile4 | Spike0 count | $tile4_spike0 |
| Neuro Tile4 | Spike1 count | $tile4_spike1 |
| Neuro Tile4 | Spike2 count | $tile4_spike2 |
| Neuro Tile4 | Spike3 count | $tile4_spike3 |
| Neuro Tile4 Coupled | Membrane maxima | $tile4c_mem_max |
| Neuro Tile4 Coupled | Spike counts | $tile4c_spike_counts |
| Neuro Tile4 Coupled | Spike maxima | $tile4c_spike_max |

## Source Artifacts

- \`results/synapse_test.txt\`
- \`results/lif_neuron_test.txt\`
- \`results/neuron_tile_test.txt\`
- \`results/neuro_tile4_test.txt\`
- \`results/neuro_tile4_coupled_test.txt\`
EOF

echo "Wrote $OUT_FILE"
