# Vision

## One-Liner

Build **NeuroCore**: an analog neuromorphic compute core in standard CMOS,
starting from the verified transistor-up GPU stack in this repo.

## What We Are Making

We are building a development path, not just a single demo:

1. Preserve and maintain the verified digital foundation (Level 0-5 stack).
2. Add analog neuron and spiking primitives (starting with `lif_neuron`).
3. Compose those primitives into a small neuromorphic compute tile.
4. Package the story and technical evidence for ICTGC execution.

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
- Clear development docs under `my-workspace/docs/`

### Out of Scope (For Now)

- Layout, DRC/LVS, tape-out execution
- Process-porting beyond the current verified flow
- New EDA toolchain adoption without explicit planning

## North Star Outcomes

- A clear, testable analog neuromorphic progression from current assets
- Clean and navigable knowledgebase for future agent onboarding
- Competition-ready narrative backed by real simulation evidence

## Key References

- Development process: `my-workspace/docs/DEVELOPMENT.md`
- Progress tracker: `my-workspace/docs/STATUS.md`
- Armory capability snapshot: `my-workspace/docs/armory/snapshot-2026-02-02/armory-summary.md`
- Competition strategy: `competition/competition-plan.md`
