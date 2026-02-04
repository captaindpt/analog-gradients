# NeuroCore Architecture Dissection (Paper Notes)

Date: 2026-02-03

This is the working dissection notebook for `competition/paper/neurocore_workthrough.tex`.

## Dissection method (systematic, repeatable)

Three passes are used for every block:

1. **Structure pass**: identify devices, topology, and control paths.
2. **Dynamics pass**: identify dominant state variables and governing equations.
3. **Evidence pass**: map claims to `results/*_test.txt` and derived analysis artifacts.

Build path under study:

1. `synapse`
2. `lif_neuron`
3. `neuron_tile`
4. `neuro_tile4`
5. `neuro_tile4_coupled`
6. `neuro_tile4_mixed_signal`

---

## First sketch (draw it once)

```
pre spikes --> [Synapse RC] --> [Membrane RC] --> [Threshold + Reset] --> spike
                                  |                                     |
                                  +--------- continuous state ----------+

channel0 spike --(feed-forward links)--> channel1 --> channel2 --> channel3
                         ^
                         |
                   digital en gate (mixed-signal experiment)
```

This sketch is the seed for the larger assembled architecture figure in the paper.

---

## 1) Synapse primitive

Sources:
- `netlists/synapse.scs`
- `ocean/test_synapse.ocn`
- `results/synapse_test.txt`

Structure:
- `MN_DRV` opens charge path into `post`.
- `C_POST` and `R_DECAY` set integrate/decay behavior.
- inverter buffer chain exports a robust readout.

Dynamics:
- `dVpost/dt = Iinj/Cpost - Vpost/(Rdecay*Cpost)`
- `tau_syn = Rdecay * Cpost = 16ns` with current defaults.

Evidence:
- `Vpost(max)=1.575V`, pulse count `6`, repeated integrate/decay/recharge confirmed.

Dictation note:
> This block is not just a pulse shaper; it is the first analog state machine
> in the path, where stored charge carries short-term memory between events.

---

## 2) LIF neuron

Sources:
- `netlists/lif_neuron.scs`
- `ocean/test_lif_neuron.ocn`
- `results/lif_neuron_test.txt`

Structure:
- pulse current input charges membrane node `mem`,
- leak resistor creates passive discharge,
- inverter chain performs thresholding,
- reset NMOS discharges membrane after spike.

Dynamics:
- subthreshold: `Cmem * dVmem/dt = Iin - Vmem/Rleak`
- event/reset: threshold crossing enables a nonlinear reset current.

Evidence:
- 10 spikes in 200ns window, `Vmem(max)=1.573V`.

Dictation note:
> Computation appears here as *when* the membrane crosses threshold, not just
> whether an input pulse exists.

---

## 3) Neuron tile (synapse + LIF composition)

Sources:
- `netlists/neuron_tile.scs`
- `ocean/test_neuron_tile.ocn`
- `results/neuron_tile_test.txt`

Structure:
- synapse output couples into membrane via `R_COUPLE`,
- threshold/reset loop reused from LIF cell.

Evidence:
- decay at synapse node is preserved after composition,
- spike-node pulses detected: `12`.

Dictation note:
> This is the minimum complete compute channel: event input -> analog state
> evolution -> event output.

---

## 4) Neuro Tile4 (parallel temporal channels)

Sources:
- `netlists/neuro_tile4.scs`
- `ocean/test_neuro_tile4.ocn`
- `results/neuro_tile4_test.txt`

Structure:
- four replicated channels with offset presynaptic pulse delays.

Evidence:
- all channels spike (`14` pulses each),
- first spikes: `27.5, 29.5, 31.5, 33.5 ns`.

Dictation note:
> The signal is encoded as relative timing between channels; this is temporal
> coding at transistor level, not clocked cycle-indexed logic.

---

## 5) Neuro Tile4 Coupled (feed-forward propagation)

Sources:
- `netlists/neuro_tile4_coupled.scs`
- `ocean/test_neuro_tile4_coupled.ocn`
- `results/neuro_tile4_coupled_test.txt`

Structure:
- only channel-0 receives external drive,
- downstream channels receive injected activity via feed-forward links.

Evidence:
- membrane maxima: `0.569, 0.974, 1.268, 0.873V`,
- spike counts: `15, 15, 1, 1`,
- downstream activation confirmed.

Dictation note:
> Propagation exists, but strict ordering is not monotonic in this snapshot;
> this should be reported explicitly as behavior, not hidden.

---

## 6) Neuro Tile4 mixed-signal (digital gating over analog path)

Sources:
- `netlists/neuro_tile4_mixed_signal.scs`
- `ocean/test_neuro_tile4_mixed_signal.ocn`
- `results/neuro_tile4_mixed_signal_test.txt`

Structure:
- digital `en` controls coupling transistors between channels.

Evidence:
- enable rises near `140.5ns`,
- downstream spikes pre-enable: `0`,
- downstream spikes post-enable: `7` each for channels `1..3`.

Dictation note:
> This is the bridge experiment: digital control signal selects when analog
> continuous-time propagation is allowed.

---

## Assembled architecture statement

Computation in this path is distributed across:

- **state variables**: synaptic and membrane voltages,
- **event surfaces**: threshold crossings in inverter detector chains,
- **propagation links**: feed-forward coupling paths carrying timing,
- **gates**: digital enable controlling analog transport.

Paper-level claim:
> NeuroCore computes in trajectory and latency space, with a reproducible
> evidence chain from transistor simulation to implementation-flow artifacts.

---

## Next paper hardening checkpoints

- Add one dedicated assembled architecture figure (channel internals + coupling + digital gate).
- Add claim-to-artifact traceability table in manuscript.
- Keep metric tables synchronized to latest `results/*_test.txt` and sweep CSV.
- Add explicit limitation paragraph (coarse sensitivity grid, full-window ODE weakness).
