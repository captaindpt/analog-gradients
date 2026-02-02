# GPU Core Diagram (GPU-Lite)

This diagram reflects the current netlist structure:
`gpu_core.scs` → `pe4.scs` → `pe1.scs` → `alu4.scs`.

```mermaid
flowchart TB
  %% GPU-Lite core (Level 0)
  GPU[GPU Core<br/>gpu_core.scs]

  %% Level 1: PE array
  GPU --> PE4[PE Array (4x PE)<br/>pe4.scs]

  %% Level 1: four PEs
  PE4 --> PE0[PE0<br/>pe1.scs]
  PE4 --> PE1[PE1<br/>pe1.scs]
  PE4 --> PE2[PE2<br/>pe1.scs]
  PE4 --> PE3[PE3<br/>pe1.scs]

  %% Level 2: ALU per PE
  PE0 --> ALU0[ALU4<br/>alu4.scs]
  PE1 --> ALU1[ALU4<br/>alu4.scs]
  PE2 --> ALU2[ALU4<br/>alu4.scs]
  PE3 --> ALU3[ALU4<br/>alu4.scs]

  %% IO summary
  OP[Shared Opcode<br/>OP[1:0]] --> PE4
  A0[A0[3:0]] --> PE0
  B0[B0[3:0]] --> PE0
  A1[A1[3:0]] --> PE1
  B1[B1[3:0]] --> PE1
  A2[A2[3:0]] --> PE2
  B2[B2[3:0]] --> PE2
  A3[A3[3:0]] --> PE3
  B3[B3[3:0]] --> PE3

  PE0 --> Y0[Y0[3:0]]
  PE1 --> Y1[Y1[3:0]]
  PE2 --> Y2[Y2[3:0]]
  PE3 --> Y3[Y3[3:0]]
```

ASCII fallback:

```
GPU Core (gpu_core.scs)
  └─ PE Array (pe4.scs)
       ├─ PE0 (pe1.scs) → ALU4 (alu4.scs) → Y0[3:0]
       ├─ PE1 (pe1.scs) → ALU4 (alu4.scs) → Y1[3:0]
       ├─ PE2 (pe1.scs) → ALU4 (alu4.scs) → Y2[3:0]
       └─ PE3 (pe1.scs) → ALU4 (alu4.scs) → Y3[3:0]

Shared inputs: OP[1:0], A0..A3[3:0], B0..B3[3:0]
Outputs: Y0..Y3[3:0], COUT0..COUT3
```
