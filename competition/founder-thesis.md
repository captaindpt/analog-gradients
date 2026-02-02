# NeuroCore Founder Thesis

## Core Reframe

This project is not "I can use EDA tools."  
This project is "I am building a compute primitive that clocked digital flows do not natively represent."

## Original Idea

**Clockless continuous-time compute using analog spike dynamics.**

Computation is encoded in:
1. membrane trajectory \(V_{mem}(t)\),
2. spike timing \(t_{spike}\),
3. event propagation latency across coupled channels,
instead of synchronous logic state transitions.

## Why This Is Founder-Level (Not Job-Applicant-Level)

Existing digital-centric flows optimize boolean + clock behavior.
NeuroCore demonstrates:
- asynchronous event-driven propagation in transistor circuits,
- timing-coded computation (latency as signal),
- sensitivity of timing to physical parameters (temporal gradients).

## Evidence Already in Repo

| Claim | Current Evidence |
|------|------------------|
| Analog neurons compute via continuous-time dynamics | `results/synapse_test.txt`, `results/lif_neuron_test.txt` |
| Multi-channel timing encodes information | `results/neuro_tile4_test.txt` (27.5/29.5/31.5/33.5 ns first spikes) |
| Feed-forward event propagation | `results/neuro_tile4_coupled_test.txt` |
| Parameter robustness | `competition/sweeps/neuro_tile4_coupled_sweep_summary.md` (9/9 PASS) |
| Implementation credibility | `competition/full-flow-smoke-evidence.md` |

## Next Evidence Targets (Math-Heavy)

1. **ODE-fit validation** ✅
   - Artifact: `competition/analysis/lif_ode_fit_summary.md`
   - Highlight: decay-window fit (12ns-19ns) reaches \(R^2 = 0.931\).
2. **Temporal sensitivity extraction** ✅
   - Artifact: `competition/analysis/temporal_sensitivity_summary.md`
   - Highlight: \(dt_{spike0}/dr_{fb} \approx -0.663 \,\text{ns}/\text{k}\Omega\) across tested \(r_{leak}\).
3. **Energy-per-event estimate** ✅
   - Artifact: `competition/analysis/lif_energy_summary.md`
   - Highlight: first-pass estimate \(\approx 4.718\,\text{pJ/spike}\) (0-200ns window).
4. **Mixed-signal coupling demo** ✅
   - Artifact: `competition/mixed-signal-smoke-evidence.md`
   - Highlight: downstream spikes are suppressed before digital `en` and activate after `en` rises.

## Competition Pitch Line

> Conventional chips compute in clocked logic states.  
> NeuroCore computes in continuous-time physics, where voltage trajectories and spike timing are the program.
