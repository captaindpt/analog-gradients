# Vision

## One-Liner

Build **NeuroCore**: an analog neuromorphic compute core in standard CMOS, and
prove a reproducible **transistor-to-GDSII-ready** development path from one
terminal workflow.

## Demo Thesis

**One terminal. Transistors to tape-out path. One engineer.**

For judging, the visual proof sequence is:
1. Full verification cascade (`./build.sh all`)
2. Analog coupled-neuron waveforms (`neuro_tile4_coupled`)
3. Implementation flow replay (`scripts/run_fullflow_smoke.sh`)
4. Concrete physical artifact (`alu4_flow_demo.gds`)

## Founder Thesis (Milestone Upgrade)

**Clockless continuous-time compute** is the original idea:
the architecture computes in voltage trajectories and spike timing, not only in
clocked boolean transitions.

Core claim:
- conventional digital flows optimize state transitions on clocks,
- NeuroCore uses transistor dynamics where latency and membrane evolution carry
  information and computation.
- Mixed-signal proof now exists: a digital enable signal can gate analog
  propagation timing in one reproducible Spectre run.

## What We Are Making

We are building a development path, not just a single demo:

1. Preserve and maintain the verified digital foundation (Level 0-5 stack).
2. Expand analog neuron and spiking primitives into coupled neuromorphic tiles.
3. Demonstrate end-to-end implementation credibility:
   simulation -> synthesis -> place/route -> physical verification -> GDS.
4. Package a competition-ready narrative and evidence bundle for ICTGC.

## Why This Repo Exists

- To prove AI-assisted hardware development can move from device primitives to
  system-level verified behavior.
- To make the workflow reproducible for future agents and collaborators.
- To turn simulation assets into credible competition and research artifacts.

## Scope

### In Scope (Now)

- Spectre/OCEAN simulation and verification
- Reusable netlist building blocks
- Deterministic PASS/FAIL reporting
- Full-flow demo planning for DC -> Innovus -> Calibre handoff
- Scripted artifact generation (metrics, diagrams, waveform plots)
- Clear development docs under `my-workspace/docs/`

### Out of Scope (For Now)

- Full custom analog layout for the entire NeuroCore system
- Actual shuttle submission/tape-out execution
- Process-porting beyond the current verified flow and selected demo nodes
- New EDA toolchain adoption without explicit planning

## North Star Outcomes

- A clear, testable analog neuromorphic progression from current assets
- A live-demo-capable flow that reaches GDS-ready evidence for ICTGC judges
- A defensible original-idea thesis backed by math-oriented evidence (ODE fit,
  temporal sensitivity, energy/event)
- Clean and navigable knowledgebase for future agent onboarding
- Competition-ready narrative backed by real simulation evidence
- Transparent reporting of tool-access constraints (license blockers) while
  preserving reproducible flow evidence

## Key References

- Development process: `my-workspace/docs/DEVELOPMENT.md`
- Progress tracker: `my-workspace/docs/STATUS.md`
- Armory capability snapshot: `my-workspace/docs/armory/snapshot-2026-02-02/armory-summary.md`
- Competition strategy: `competition/competition-plan.md`
- Full-flow demo strategy: `competition/full-flow-demo-plan.md`
- Founder thesis framing: `competition/founder-thesis.md`
- Current evidence bundle: `competition/verification-evidence.md`
- Full-flow smoke evidence: `competition/full-flow-smoke-evidence.md`
