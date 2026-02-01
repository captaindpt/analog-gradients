# Vision

## One-Liner

**Voice-to-Silicon.** Ask an AI to build a GPU, watch it happen.

---

## The Demo

A terminal. A voice command. An AI designs a GPU core from transistors up, verified at every level, in under a minute.

```
"Build me a 4-bit ALU"

→ Agent reads AGENTS.md
→ Finds building blocks (inverter, nand2, nor2)
→ Composes gates (and2, or2, xor2)
→ Builds adder from gates
→ Builds ALU from adders
→ Each step: simulate, verify, proceed
→ Done. Verified ALU.
```

---

## What We're Building

A **testbed for AI-driven hardware design**.

- **Not** a full EDA tool
- **Not** layout or tape-out ready
- **Yes** a demonstration of speed and automation
- **Yes** a library of verified building blocks
- **Yes** a workflow any agent can follow

---

## The Moat

Experience encoded into:

1. **Verified netlists** - Working circuits, tested
2. **Clear templates** - How to create new components
3. **Automated verification** - OCEAN scripts for truth tables
4. **Documentation** - AGENTS.md, skill.md, CLAUDE.md

An agent walks in cold, reads the docs, builds hardware.

---

## Build Hierarchy

```
Level 0: GPU Core        ← The demo goal
   ↑
Level 1: PE Array, Memory, Control
   ↑
Level 2: ALU, SRAM, Registers
   ↑
Level 3: Adder, Mux, Decoder
   ↑
Level 4: AND, OR, XOR
   ↑
Level 5: Inverter, NAND, NOR  ← Foundation (DONE)
```

---

## Current State

- **Level 5:** ✅ Complete (inverter, nand2, nor2)
- **Tooling:** ✅ Working (build.sh, setup_cadence.sh)
- **Docs:** ✅ Ready (AGENTS.md, skill.md, CLAUDE.md)
- **Tickets:** ✅ Set up

---

## What's Next

1. **Codex builds Level 4** - AND, OR, XOR gates
2. **Then Level 3** - Adders, muxes
3. **Then Level 2** - ALU
4. **Record the demo**

---

## Constraints We Accept

- No layout (simulation only)
- No GUI (headless Spectre/OCEAN)
- CMC Cloud dependency
- Simple mos1 models (not PDK)

These are fine. The point is **speed and automation**, not tape-out.

---

## Success Criteria

- [ ] Agent can build a component from spec without human help
- [ ] Full hierarchy from transistor to ALU, verified
- [ ] Demo video: Voice → GPU core in 60 seconds
- [ ] Repository usable by any agent or human

---

## Long-Term

This is a stepping stone to:

1. FABrIC IoT Challenge 2026
2. Hardware-aware neural network training
3. Neuromorphic computing research

But for now: **make the demo work.**
