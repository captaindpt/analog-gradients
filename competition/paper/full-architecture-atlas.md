# Full Architecture Atlas (All Components)

Date: 2026-02-03

Goal: provide a "draw-it-all" map for every verified component in the repo.

Legend:
- `[X]` block
- `->` signal/data direction
- `||` parallel channels

---

## Level 5: CMOS primitives

### inverter (`netlists/inverter.scs`)

```
in -> gate(PMOS top + NMOS bottom) -> out
```

### nand2 (`netlists/nand2.scs`)

```
pull-up:   PMOS(a) || PMOS(b)
pull-down: NMOS(a) -> NMOS(b)
out = ~(a & b)
```

### nor2 (`netlists/nor2.scs`)

```
pull-up:   PMOS(a) -> PMOS(b)
pull-down: NMOS(a) || NMOS(b)
out = ~(a | b)
```

---

## Level 4: logic gates

### and2 (`netlists/and2.scs`)

```
a,b -> [NAND2] -> [INV] -> out
```

### or2 (`netlists/or2.scs`)

```
a,b -> [NOR2] -> [INV] -> out
```

### xor2 (`netlists/xor2.scs`)

```
a,b -> [NAND net x4] -> out
```

### xnor2 (`netlists/xnor2.scs`)

```
a,b -> [XOR2] -> [INV] -> out
```

---

## Level 3: blocks

### mux2 (`netlists/mux2.scs`)

```
         s -> [INV] -> s_n
a,s_n -> [AND] --\
                  -> [OR] -> out
b,s   -> [AND] --/
```

### half_adder (`netlists/half_adder.scs`)

```
a,b -> [XOR2] -> sum
a,b -> [AND2] -> carry
```

### full_adder (`netlists/full_adder.scs`)

```
a,b -> [XOR2] -> axb --\
                        -> [XOR2 with cin] -> sum
a,b -> [AND2] ------\
                     -> [OR2] -> cout
cin,axb -> [AND2] --/
```

---

## Level 2: RTL-like arithmetic

### alu1 (`netlists/alu1.scs`)

```
a,b -> AND/OR/XOR paths
a,b,cin -> ADD path

op[1:0] controls 3-stage MUX select tree:
{AND,OR,XOR,ADD} -> y
```

### alu4 (`netlists/alu4.scs`)

```
[ALU1 bit0] -> carry1 -> [ALU1 bit1] -> carry2 -> [ALU1 bit2] -> carry3 -> [ALU1 bit3]
op shared across all 4 bits
```

---

## Level 1: functional

### pe1 (`netlists/pe1.scs`)

```
PE1 = [ALU4 wrapper]
```

### pe4 (`netlists/pe4.scs`)

```
shared op -> [PE1_0] || [PE1_1] || [PE1_2] || [PE1_3]
```

---

## Level 0: system

### gpu_core (`netlists/gpu_core.scs`)

```
GPU core = [PE4 wrapper]
```

---

## Neuromorphic track

### synapse (`netlists/synapse.scs`)

```
pre -> charge switch -> post node
post node = C_POST || R_DECAY
post -> buffer -> out
```

### lif_neuron (`netlists/lif_neuron.scs`)

```
input current -> mem node
mem node = Cmem || Rleak
mem -> threshold inverters -> spike
spike -> reset NMOS -> mem discharge
```

### neuron_tile (`netlists/neuron_tile.scs`)

```
pre -> [Synapse RC] -> [R_COUPLE] -> [LIF membrane + threshold/reset] -> spike/out
```

### neuro_tile4 (`netlists/neuro_tile4.scs`)

```
4 x neuron_tile in parallel (staggered pre delays)
```

### neuro_tile4_coupled (`netlists/neuro_tile4_coupled.scs`)

```
channel0 externally driven
spike0 -> channel1 injection
spike1 -> channel2 injection
spike2 -> channel3 injection
```

### neuro_tile4_mixed_signal (`netlists/neuro_tile4_mixed_signal.scs`)

```
digital en -> gates feed-forward coupling switches
before en: downstream quiet
after en: downstream propagation active
```

---

## Singular primitive-to-system map (intent)

```
CMOS primitives
   |- digital chain: logic -> blocks -> ALU -> PE -> GPU core
   |- analog chain: synapse -> LIF -> tile -> coupled tile -> mixed-signal gate
```

This singular map is rendered as Figure `fig:singular-unified-map` in
`competition/paper/neurocore_workthrough.tex`.
