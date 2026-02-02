# Session: 2026-02-02 - Robustness Sweep (Neuro Tile4 Coupled)

## Summary

Started robustness work by adding and running an automated parameter sweep for
`neuro_tile4_coupled`.

## Accomplished

1. **Sweep automation**
   - Added `scripts/sweep_neuro_tile4_coupled.sh`
   - Sweeps:
     - `r_fb` in `{700, 1k, 1500}`
     - `rleak` in `{6M, 8M, 10M}`

2. **Metrics extraction**
   - Captures PASS/FAIL, membrane maxima, spike counts, and spike maxima
   - Outputs:
     - `competition/sweeps/neuro_tile4_coupled_sweep.csv`
     - `competition/sweeps/neuro_tile4_coupled_sweep_summary.md`

3. **Results**
   - Total sweep points: 9
   - PASS points: 9
   - FAIL points: 0

## Notes

- Current coupled-tile behavior is stable across tested `r_fb`/`rleak` ranges.
- Downstream channels show low but valid propagation pulse counts in this setup.

## Next Steps

- Add first-spike latency extraction to sweep output
- Extend sweep harness to `synapse`, `lif_neuron`, and `neuron_tile`
