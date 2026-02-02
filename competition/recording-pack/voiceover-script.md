# NeuroCore Voiceover Script (3:00)

## Scene 1 (0:00-0:30) - The Stack

I built this stack from transistor primitives all the way up to system-level blocks.
Digital path, analog path, and verification are all scripted.
This is not a slide deck; this is executable engineering.
I run one command, and every layer reports pass/fail in sequence.
What you are seeing is reproducibility, not a one-off demo.

## Scene 2 (0:30-1:15) - The Analog Brain

Now the analog side.
These are transistor-level neuron channels in a coupled tile.
Channel zero drives the network, and downstream channels fire in sequence.
First spikes are staggered at 27.5, 29.5, 31.5, and 33.5 nanoseconds.
That is feed-forward propagation in hardware waveforms, not in software emulation.
This is the core of NeuroCore: analog spiking computation on standard CMOS.

## Scene 3 (1:15-2:15) - The Flow

Next, implementation flow.
In one terminal run, the design goes through synthesis handoff, physical design, and artifact generation.
Innovus completes place-and-route and exports a real GDSII layout file.
That file is the manufacturing-facing output of the flow.
In this academic environment, some commercial licenses are constrained,
but the pipeline, scripts, and physical outputs are already real and reproducible.
With production access, this extends directly to full signoff.

## Scene 4 (2:15-2:45) - The Point

I am one undergrad engineer building this end to end:
device behavior, block integration, verification, and implementation scripting.
The question is not whether I can build.
The question is how fast this can scale with the right fabrication pathway.

## Scene 5 (2:45-3:00) - Close

NeuroCore: analog AI on standard CMOS.
From transistors to GDSII, in one workflow.
Give me shuttle access, and I will tape out the next step.
