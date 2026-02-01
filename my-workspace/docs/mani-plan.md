# Mani Rash Ahmadi — Roadmap to Hardware AI / Neuromorphic Access (Canada)

## Context
- Fourth-year Engineering Systems & Computing student, University of Guelph.
- Refugee status; passport/PR expected in ~2–3 years.
- Interested in **neuromorphic chips**, **analog AI**, and **ASML-level system design**.
- Goal: build practical, fundable experience in Canadian microfabrication ecosystem before travel is possible.

---

## Mission Objective
Gain **CMC Microsystems access** and build a **prototype analog/edge-AI project** that can evolve into a **FABrIC IoT Challenge** submission (2026).

---

## Step 1 — Anchor Your Intent (Professor + Positioning)

**Target professors:**  
- Dr. Petros Spachos (IoT / Embedded Systems)  
- Dr. Moussa (VLSI / Analog)  
- Dr. Donald (Computer Engineering)  
- Dr. Chiang (Circuits / RF)  

**Approach script:**
> “I found the FABrIC IoT Device Challenge. It funds Canadian teams developing advanced sensors and edge-AI devices.  
> I want to explore neuromorphic hardware and prepare a concept for next year’s call.  
> Could I register under your **CMC Microsystems** account so I can access the design tools and begin prototyping?”

Professors already have free CMC memberships through UofG.  
They can add you as a **student researcher** under their account — no payment required.

---

## Step 2 — Access Pipeline (How CMC Works)

| Level | Requirement | Access Granted |
|:--|:--|:--|
| **Student User** | Be added to a prof’s CMC project | Cadence, Synopsys, Lumerical, COMSOL, KLayout, etc. |
| **Research Project** | Short internal proposal (~1 page) | Project storage, simulation, MPW eligibility |
| **FABrIC Proposal** | Academic + SME team | Up to $1M non-repayable funding for prototype development |

**Goal**: Secure *student user status* under a professor’s account by **November 2025**.

---

## Step 3 — Seed Project Concept

**Working title:** *Analog Edge-AI Sensor Node for Environmental Monitoring*  
> A low-power, neuromorphic edge sensor platform combining an analog learning core (simulated crossbar) and microcontroller logic.

**Why this fits:**
- FABrIC’s call targets *edge-AI and sensor design*.  
- Reuses your experience with Arduino/RFID (“The Box”) as sensor infrastructure.  
- Bridges toward neuromorphic analog AI for future proposals.

**Core Components:**
- Microcontroller or FPGA-based analog emulator.  
- Analog AGAD / TTv2 gradient loop simulation.  
- Energy audit spreadsheet (E = E_DAC + E_wire + E_ADC + E_update).  
- Optional optical front-end (SLM + camera simulation).

---

## Step 4 — Tactical Timeline (Oct 2025 → Oct 2026)

| Month | Focus | Deliverable |
|:--|:--|:--|
| **Oct–Nov 2025** | Secure supervisor & CMC access | CMC account under UofG prof |
| **Nov–Jan** | Define project scope & materials | 2-page project brief + schematic |
| **Jan–Mar** | Build emulator prototype | Microcontroller + analog front-end |
| **Mar–May** | Develop simulation models | AIHWKIT + PyTorch analog training demo |
| **May–Jul** | Use CMC layout tools | Sky130 synapse+neuron macro |
| **Jul–Sep** | Draft FABrIC Expression of Interest | Preliminary proposal w/ visuals |
| **Oct 2026** | Submit EOI | University + SME co-lead team |

---

## Step 5 — Public Signal & Content Strategy

You can use public visibility as leverage for lab and funding access.

**Actions:**
- Post visual threads on **X (Twitter)** or **LinkedIn**:  
  *“Visualizing analog learning: how AGAD crossbars work”*,  
  *“Canada’s path to neuromorphic edge-AI hardware”*.  
- Tag: `@cmcmicrosystems`, `@FabricInnovation`, `#HardwareAI`, `#Photonics`, `#Neuromorphic`.
- Publish simulation notebooks and visuals on **GitHub**.
- Write short technical essays: *“Why Analog Computing Isn’t Dead”*, *“Drift, Symmetry, and AGAD Loops.”*

Visibility = credibility → professors + CMC + FABrIC will take you seriously.

---

## Step 6 — Learning Targets (Next 6 Months)

| Area | Skill | Resource |
|:--|:--|:--|
| **Analog Crossbars** | Hardware-aware training (AGAD, TTv2) | IBM AIHWKIT notebooks |
| **Photonic Neural Nets** | Free-space diffractive simulation | Meep, *Optical Neural Networks (Miscuglio 2022)* |
| **CAD & Layout** | CMOS design, Sky130 | CMC training + KLayout tutorials |
| **Energy Audits** | Power & efficiency modeling | IEEE JSSC & ISSCC papers |
| **Proposal Writing** | Funding & challenge style | CMC and FABrIC templates |

---

## Step 7 — Email Template (to Send to Prof)

**Subject:** Interest in CMC / FABrIC IoT Challenge and Access to Design Tools  

Hi Professor Spachos,

I came across the FABrIC IoT Device Challenge, which supports Canadian teams developing advanced sensors and edge-AI devices.
I’m very interested in neuromorphic and analog AI hardware, and I’d like to prepare a concept for the next round of the challenge next year.

To begin, I’d love to gain access to CMC Microsystems tools through the University of Guelph.
My plan is to design and simulate a small analog or mixed-signal edge-AI node this semester — something we could eventually evolve into a formal project or proposal.

Would you be open to supervising or co-signing my CMC access so I can get started?
I can share a 1-page concept summary if that helps.

Best,
Mani Rash Ahmadi

---

## Step 8 — Long-Term Pathway (Post-Passport)

Once you can travel (2027–2028):

- **IMEC (Belgium)** — internships or PhD in neuromorphic / analog computing.  
- **TU Eindhoven / Delft / Twente** — MSc or PhD in precision mechatronics or photonic integration.  
- **NRC / CPFC (Ottawa)** — Canadian photonics & microfab research.  
- **Hardware AI startups** (Lightmatter, Xanadu, Tenstorrent) — hybrid analog-compute projects.

Your public portfolio + CMC prototypes will open those doors.

---

## Step 9 — Tools Stack to Learn Now

| Type | Tool | Purpose |
|:--|:--|:--|
| Circuit sim | ngspice, Cadence | Analog loop and periphery |
| Neural sim | PyTorch + AIHWKIT | Hardware-aware training |
| Optics sim | Meep / Lumerical | Diffractive neural nets |
| Layout | KLayout / L-Edit (via CMC) | CMOS macro design |
| PCB proto | KiCad | Physical board design |
| Docs | Markdown + LaTeX | Proposal writing & visuals |

---

## Final Philosophy

> You don’t need ASML’s machines to learn ASML’s mindset.  
> The Canadian fab and photonics ecosystem lets you **practice the art of precision and feedback** on a smaller scale — until the doors open wider.

Start now, build the signal, and when you have your passport, you’ll already be fluent in the language of machines that think in light and charge.

---

## Useful Links

- FABrIC IoT Challenge Portal → https://fabricinnovation.ca  
- CMC Microsystems → https://cmc.ca  
- AIHWKIT (IBM) → https://github.com/IBM/aihwkit  
- SkyWater 130 PDK → https://skywater-pdk.readthedocs.io  
- Meep FDTD Simulator → https://meep.readthedocs.io  
- Open Source ASIC Tools → https://efabless.com  
- IMEC Research → https://imec-int.com  

---

**Version:** v1.0 — Oct 2025  
**Author:** *Mani Rash Ahmadi*  
**Theme:** “Building ASML-level understanding from Canadian soil.”
