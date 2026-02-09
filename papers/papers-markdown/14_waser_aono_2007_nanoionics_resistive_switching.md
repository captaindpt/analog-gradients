# 14_waser_aono_2007_nanoionics_resistive_switching.pdf

nature materials | VOL 6 | NOVEMBER 2007 | www.nature.com/naturematerials 833
REVIEW ARTICLES | insight
Nanoionics-based resistive switching 
memories
 
Many metal–insulator–metal systems show electrically induced resistive switching effects and have 
therefore been proposed as the basis for future non-volatile memories. They combine the advantages 
of Flash and DRAM (dynamic random access memories) while avoiding their drawbacks, and they 
might be highly scalable. Here we propose a coarse-grained classification into primarily thermal, 
electrical or ion-migration-induced switching mechanisms. The ion-migration effects are coupled to 
redox processes which cause the change in resistance. They are subdivided into cation-migration 
cells, based on the electrochemical growth and dissolution of metallic filaments, and anion-migration 
cells, typically realized with transition metal oxides as the insulator, in which electronically conducting 
paths of sub-oxides are formed and removed by local redox processes. From this insight, we take a 
brief look into molecular switching systems. Finally, we discuss chip architecture and scaling issues.
Raine R WaseR1,2* and Masakazu aono 3,4
1Institut für Werkstoffe der Elektrotechnik 2, RWTH Aachen University, 52056 
Aachen, Germany
2Institut für Festkörperforschung/CNI—Center of Nanoelectronics for 
Information Technology, Forschungszentrum Jülich, 52425 Jülich, Germany
3Nanomaterials Laboratories, National Institute for Material Science,  
1-1 Namiki, Tsukuba, Ibaraki 305-0044, Japan
4ICORP/Japan Science and Technology Agency, 4-1-8 Honcho, Kawaguchi, 
Saitama 332-0012, Japan
*e-mail: r.waser@fz-juelich.de
Memory concepts that have been recently pursued range from 
spin-based memories (magnetoresistive random access memories, 
or MRAM for short, and related ideas), in which a magnetic field 
is involved in the resistance switching, to phase-change RAM 
(PCRAM), in which thermal processes control a phase transition in 
the switching material from the amorphous to the crystalline state. 
Y et another class of resistive switching phenomena is based on the 
electrically stimulated change of the resistance of a metal–insulator–
metal (MIM) memory cell, usually called resistance switching RAM, 
or RRAM for short. The ‘M’ in MIM denotes any reasonably good 
electron conductor, often different for the two sides, and the ‘I’ stands 
for an insulator, often ion-conducting material. Typically, an initial 
electroforming step such as a current-limited electric breakdown is 
induced in the virgin sample. This step preconditions the system 
which can subsequently be switched between a conductive ON state 
and a less conductive OFF state. The necessity of this initial step 
and its mechanism strongly depend on the switching class, as will 
be described.
Starting with the report on oxide insulators by Hickmott 1 in 
1962, a huge variety of materials in a MIM configuration have been 
reported to show hysteretic resistance switching. In general, the ‘I’ 
in MIM can be one of a wide range of binary and multinary oxides 
and higher chalcogenides as well as organic compounds, and the 
‘M’ stands for a similarly large variety of metal electrodes including 
electron-conducting non-metals. A first period of high research 
activity up to the mid-1980s has been comprehensively reviewed 
elsewhere2–4. The current period started in the late 1990s, triggered 
by Asamitsu et al.5, Kozicki et al.6 and Beck et al.7.
Before we turn to the basic principles of these switching 
phenomena, we need to distinguish between two schemes with 
respect to the electrical polarity required for resistively switching 
MIM systems. Switching is called unipolar (or symmetric) when the 
switching procedure does not depend on the polarity of the voltage 
and current signal. A system in its high-resistance state (OFF) is 
switched (‘set’) by a threshold voltage into the low-resistance state 
(ON) as sketched in Fig. 1a. The current is limited by the compliance 
current of the control circuit. The ‘reset’ into the OFF state takes 
place at a higher current and a voltage below the set voltage. In this 
respect, PCRAMs show unipolar switching (without compliance 
current in this case). In contrast, the characteristic is called bipolar 
(or antisymmetric) when the set to an ON state occurs at one voltage 
polarity and the reset to the OFF state on reversed voltage polarity 
(Fig. 1b). The structure of the system must have some asymmetry, 
such as different electrode materials or the voltage polarity during 
the initial electroforming step, in order to show bipolar switching 
behaviour. In both characteristics, unipolar and bipolar, reading of 
the state is conducted at small voltages that do not affect the state.
Classifi Cation of s Wit Ching MeChanis Ms
In conjunction with the discussion of conceivable switching 
mechanisms, we must address the question of the geometrical location 
of the switching event in a MIM structure. With respect to the cross-
section of the electrode pad, the switching to the ON state is typically 
reported as a confined, filamentary effect rather than a homogeneously 
distributed one, leading to a resistance that is independent of pad size. 
In planar MIM structures, filaments along the surface are observed 
© 2007 Nature Publishing Group 

834	 nature materials | VOL 6 | NOVEMBER 2007 | www.nature.com/naturematerials
REVIEW ARTICLES | insight
(Fig. 2). For both cases, in the perpendicular direction (along the 
path between the electrodes), evidence for interface effects are more 
frequently described than bulk switching effects.
Conceivable mechanisms for the resistive switching in MIM 
systems often consist of a combination of physical and/or chemical 
effects. As a first approach, however, they can be classified according 
to whether the dominant contribution comes from a thermal effect, 
an electronic effect, or an ionic effect. Caution must be exercised, 
because in many reports the switching mechanism has not yet 
been elucidated or suggestions are based on little experimental 
and theoretical evidence. Unfortunately, papers often do not report 
full details of the sample preparation and electrode deposition, the 
polarity of voltage applied during electroforming and during the first 
voltage pulse or voltage sweep, the electrode pad-size dependence of 
the current, the temperature dependence of the electrical response, 
the yield and the statistics in the cell-to-cell data, or the shift of 
characteristics on repeated cycling. As a consequence, in many 
cases we cannot make a comparison of the results and a reasonable 
assignment of a switching mechanism. Therefore, we attempt a 
coarse-grained classification of conceivable mechanisms and try to 
assign selected examples.
A typical resistive switching based on a thermal effect shows a 
unipolar characteristic. It is initiated by a voltage-induced partial 
dielectric breakdown in which the material in a discharge filament 
is modified by Joule heating. Because of the compliance current, only 
a weak conductive filament with a controlled resistance is formed. 
This filament may be composed of the electrode metal transported 
into the insulator, carbon from residual organics 4 or decomposed 
insulator material such as sub-oxides8. During the reset transition, 
this conductive filament is again disrupted thermally because of high 
power density of the order of 1012 W cm–3 generated locally, similar to 
a traditional household fuse but on the nanoscale. Hence, we refer to 
this mechanism as the fuse–antifuse type. One candidate out of many 
is NiO, first reported in the 1960s9. Recently, the filamentary nature 
of the conductive path in the ON state has been confirmed for NiO 
(ref. 10) and TiO2 (ref. 11). Cells based on Pt/NiO/Pt thin films have 
been successfully integrated into CMOS (complementary metal oxide 
semiconductor) technology to demonstrate non-volatile memory 
operation12. A critical parameter for this unipolar switching effect 
seems to be the value of the compliance current. In fact, it has recently 
been demonstrated that a TiO 2 thin film shows bipolar switching, 
and that this can be changed to unipolar switching characteristics by 
setting the compliance current to a larger value13.
Electronic charge injection and/or charge displacement effects 
can be considered as another origin of resistive switching. One 
possibility is the charge-trap model14, in which charges are injected by 
Fowler–Nordheim tunnelling at high electric fields and subsequently 
trapped at sites such as defects or metal nanoparticles in the insulator. 
This modifies the electrostatic barrier character of the MIM structure 
and hence its resistance, resembling the gate–channel resistance in 
a Flash field-effect transistor (FET). For example, gold nanoclusters 
incorporated in either polymeric 15,16 or inorganic insulator films 17 
can be trapping sites. In a modified model, trapping at interface 
states is thought to affect the adjacent Schottky barrier at various 
metal/semiconducting perovskite interfaces18–20. A similar mechanism 
has been reported for ZnSe–Ge heterojunctions21.
Another possible model is the insulator–metal transition (IMT), 
in which electronic charge injection acts like doping to induce an 
IMT in perovskite-type oxides such as (Pr,Ca)MnO 3 (refs 5,22,23) 
and SrTiO3:Cr (ref. 24). A generic model by Rozenberg et al.25 has 
recently been extended to bipolar switching26.
Finally, a model based on ferroelectricity has been proposed 
by Esaki27 and theoretically described by Kohlstedt et al.28, 29. Here, 
an ultrathin ferroelectric insulator is assumed whose ferroelectric 
polarization direction influences the tunnelling current through 
the insulator.
Current
(mA range)
Current
(µA to mA range)
Voltage
(few volt range)
0
Voltage
(few volt range)
0
Unipolar Bipolar
CC
OFF
OFF
CC
CC
ON
ON
OFF
OFF
ON
ON
Figure 2 sketch of filamentary conduction in MiM structures. Redrawn with 
modifications from ref. 4. a, Vertical stack configuration. b, l ateral, planar 
configuration. t he red tube indicates the filament responsible for the on  state.
Figure 1 Classification of the switching characteristics in a voltage sweeping experiment. depending on the specific system, the curves vary considerably. t he purpose of 
these sketches is to differentiate between the two possible switching directions. dashed lines indicate that the real voltage at the system will differ from the control voltage 
because of the compliance current (CC) in action. a, unipolar switching. t he set voltage is always higher than the voltage at which reset takes place, and the reset current is 
always higher than the CC during set operation. b, Bipolar switching. t he set operation takes place on one polarity of the voltage or current, and the reset operation requires 
the opposite polarity. in some systems, no CC is used.
ba
Filament
Filament
M
M
I
© 1998 WILEY
© 2007 Nature Publishing Group 

nature materials | VOL 6 | NOVEMBER 2007 | www.nature.com/naturematerials 835
REVIEW ARTICLES | insight
In this review, we will focus on MIM systems in which ionic 
transport and electrochemical redox reactions provide the essential 
mechanism for bipolar resistive switching. It is this area in which 
nanoelectronics30 becomes intimately connected to nanoionics31. One 
class in this category relies on the sequence of the following processes: 
the oxidation of an electrochemically active electrode metal such as 
Ag; the drift of the mobile Ag + cations in the ion-conducting layer; 
their discharge at the (inert) counterelectrode leading to a growth 
of Ag dendrites, which form a highly conductive filament in the ON 
state of the cell32. When the polarity of the applied voltage is reversed, 
an electrochemical dissolution of the conductive bridges takes place, 
resetting the system into the OFF state. Instead of silver, it is possible 
to use copper and other metals in the moderate area of the standard 
electrochemical potential series. A second class in this category operates 
through the migration of anions, typically oxygen ions, towards the 
anode (better described by the migration of oxygen vacancies towards 
the cathode), a subsequent change of the stoichiometry, and a valence 
change of the cation sublattice associated with a modified electronic 
conductivity. W e will outline the main similarities and differences 
between the two classes, summarize the current state of knowledge 
and technology, and sketch future work in this area.
Redox p RoCesses indu Ced By Cation MigRation 
Silver growth from heated argentite (α-Ag2S) was reported more than 
400 years ago33. Extensive studies following the first study of electric 
conduction of Ag 2S by Faraday in the early nineteenth century 34 
established the thermodynamical theory of ionic conduction which 
is a key characteristic of a solid electrolyte. A galvanic cell was used 
to control stoichiometric deviation of Ag+ cations in Ag2S crystals35, 
and this revealed a mechanism for the silver whisker growth.
By using solid electrolytes in which conduction is due to metal 
cations, the formation and annihilation of a metal filament in the 
MIM system can be controlled. T o achieve the bipolar switching 
behaviour, the MIM system consists of an electrode made from an 
electrochemicall active metal, a solid electrolyte as an ion-conducting 
‘I’ layer, and a counter electrode made from an inert metal. Switching 
behaviour due to silver dendrite formation and annihilation was first 
reported by Hirose in 1976 using Ag-photodoped amorphous As2S3 as 
‘I’ of a MIM system with a lateral structure36. Kozicki et al. succeeded 
in developing the MIM system in a vertical configuration by using 
GeSe as the ion conductor and applied this to making non-volatile 
memory6. Recently, resistive switching GeSe structures as small as 
20 nm have been fabricated (Fig. 3).
In these systems, metal cations in the ionic conductors migrate 
towards the cathode made of inert materials and are reduced there. The 
reduced metal atoms form a metal filament which grows towards the 
anode to turn on the switch. As the anode is made of electrochemically 
active material, metal atoms of the anode are oxidized and dissolved 
into the ionic conductor, maintaining the number of metal cations 
for continuous electrochemical deposition. In the case of Ag 2S, the 
following chemical reaction occurs at the anode and the cathode:
 
Ag+(Ag2S) + e– Ag
Reduction
Oxidation  
(1)
On changing the polarity of the bias voltage, metal atoms dissolve 
at the edge of the metal filament, eventually annihilating the filament 
so that the switch is turned off. Because the chemical reaction ideally 
does not cause any damage to the MIM system, the switch may in 
principle be expected to work indefinitely6.
Solid electrolyte can be used as one of the ‘metal’ electrodes of the 
MIM system. Terabe et al. developed this type of MIM switch using 
an electronic and ionic mixed conductor for one of the electrodes32. In 
this case, a vacuum nano-gap is used as an insulator layer, and a metal 
filament grows in the gap to bridge the mixed conductor electrode 
and the counterelectrode (Fig.  4). Because the switching is caused 
by an electrochemical reaction, increasing a switching bias voltage 
shortens the switching time exponentially37. Reducing the size of a 
metal filament also produces faster switching.
In both types of MIM system, the switching effect is most easily 
found for material systems that are cation conductors for the redox active 
species (such as Ag+ in Ag2S) or, alternatively, compounds with high 
solubility of the redox active cation (such as Ag+ in GeSex). The switches 
can be operated with smaller bias voltage, such as 0.2 V , which may be 
preferable for memory devices with low power consumption6,38.
Some applications, such as non-volatile switches in reconfigurable 
large-scale integrated systems (LSIs), require higher threshold bias 
Figure 3 Cross-section of a vertical type of MiM switch using ag+ conducting solid 
electrolyte. a silver filament is electrochemically formed in the gese layer to turn on 
the switch. t he cross-section is shown for the device for which the inset I–V curve 
was recorded. Reprinted with permission from ref. 44.
0.0
0.5
1.0
1.5
–0.1 0.0 0.1 0.2 0.3
Current (µA)
Voltage (V) 200 nm        
–0.2–0.3
20 nm Ag layer
GeSe layer
W plug
Si3N4
Tungsten
bottom
electrode       
–0.5
© 2005 IEEE
Figure 4 scanning electron micrograph of an atomic switch and its operating 
mechanism32. silver atoms precipitated from the ag2s electrode make a bridge in a 
vacuum gap of 1 nm between the two electrodes. f rom ref. 32.
b ONa
PtAg
OFF
ON
Ag2S
10 µm
Pt
Ag2S
© 2007 Nature Publishing Group 

836	 nature materials | VOL 6 | NOVEMBER 2007 | www.nature.com/naturematerials
REVIEW ARTICLES | insight
voltages than that of CMOS devices 38. Because the switching bias 
voltage is mainly determined by the activation energy for the chemical 
reaction and the ionic diffusion constant, the operating bias voltage 
can be tuned by choice of materials for MIM systems, especially the 
ion-conducting material. For instance, Ta 2O5 with Cu cations has 
been reported39 to have an operating bias voltage of 2  V . Therefore, 
switches using a variety of solid electrolyte materials such as (Zn,Cd)S, 
WO3, and SiO2 are being investigated40–42. It is interesting to note that 
systems such as Ag/(Zn,Cd)S/Pt, which were initially attributed to a 
completely different category43, are now shown to fall into this cation-
migration class40. The state of the art with respect to non-volatile 
memories is demonstrated by Ag/GeSe x/W cells integrated into 
90-nm CMOS technology44,45. In this work, an active matrix concept 
with one access transistor per switching cell has been used and a 
prototype integration density of 2 Mbit has been achieved.
Making use of an electrochemical reaction makes it possible to 
configure three-terminal devices in which switching can be controlled 
by the gate electrode. Gate-controlled formation and annihilation of 
a metal filament was first demonstrated by using (liquid) electrolyte46, 
and it has been confirmed with fully solid-state three-terminal devices 
(Fig. 5)47. Such devices, in which the control line is separated from 
the conduction line, widen the possibility of practical use of the solid 
electrolyte switches.
Although the electrochemistry of the cation-migration-based 
resistive switching cells is reasonably well understood, some 
questions remain open: for example, the microscopic nature of the 
cation conduction paths; the impact of thermal effects, details of the 
electrode reactions in particular for the OFF switching, as well as 
the interrelationship of the electrolyte nature, the cell geometry and 
the morphology of the metal dendrites on the nanoscale. In specific 
systems, such as the GeSex electrolyte, the role of defects that are also 
known to affect phase-change alloys has not been clarified yet48.
Redox p RoCesses indu Ced By anion MigRation 
In many oxides, in particular in transition metal oxides, oxygen 
ions defects, typically oxygen vacancies, are much more mobile 
than cations. If the cathode blocks ion exchange reactions during an 
electroforming process, an oxygen-deficient region starts to build and 
to expand towards the anode. Transition metal cations accommodate 
Figure 5 t hree-terminal solid electrolyte switch. electrochemical reaction for formation and annihilation of a metal filament between the source and the drain electrodes is 
controlled by the gate voltage. Reprinted with permission from ref. 47. 
Figure 6 Multilevel switching in a Cr-doped srz ro3 MiM cell operated at 77 k. a, Voltage stimulation. b, Current response. Reprinted with permission from ref. 7. By applying 
voltage pulses of appropriate levels, the system can be set to three different on  state resistances (levels 1 to 3). t ogether with the off  state (level 0) this represents a two-bit 
memory cell.
 lD (A)
Cycle
OFF
ON
VD = 10 mV VG = 0 mV
0 20 40
10-10
10-8
10-6
10-4
10-2
Cu electrode
 Cu: 120 nm
Solid electrolyte
 Cu2-αS: 40 nm
Insulating layer
 Calixarene: 140 nm
Top electrode
 Pt: 40 nm
Gate (Cu) Cu2-α S
1 µm
Drain (Pt)
Source (Cu)
Nanobridge
A: Initialization
C: ON
B: OFF
Source
gap
Drain
Gate
+VG
Cu+
–VG
Cu+
–VD
Cu+
© 2006 OUP
5.3 V
4.8 V
-6.5 V
6.5 V 
0 100 200 300
Time (s)
400 500
-8
-6
-4
-2
0
2
4
6
8
 
 
V (V)
a
-100
-50
0
Level 1 
Level 3 
Level 2 
Level 0 
 
 
0 100 200 300
Time (s)
400 500
b
I (µA)
© 2000 AIP
© 2007 Nature Publishing Group 

nature materials | VOL 6 | NOVEMBER 2007 | www.nature.com/naturematerials 837
REVIEW ARTICLES | insight
this deficiency by trapping electrons emitted from the cathode. In 
the case of TiO2 or titanates, for example, this reduction reaction
 ne– + Ti4+→Ti (4–n)+ (2)
is equivalent to filling the Ti 3d band. The reduced valence states of the 
transition metal cations which are generated by this electrochemical 
process typically turn the oxide into a metallically conducting phase, 
such as TiO 2–n/2 for approximately n > 1.5. This ‘virtual cathode’ 
moves towards the anode and will finally form a conductive path49. At 
the anode, the oxidation reaction may lead to the evolution of oxygen 
gas, according to
 OO →V
..
O + 2e– + 1/2O2 (3)
where V
..
O denotes oxygen vacancies with a double positive charge 
with respect to the regular lattice and O O represents an oxygen ion 
on a regular site according to the Kröger–Vink notation. As an 
alternative to reaction (3), the anode or the material nearby may 
be oxidized. The electroforming conditions depend on the MIM 
system. Macroscopic single crystals typically require some 100  V 
for several hours, whereas for thin films the first switching cycle 
at about 1 V may be sufficient. The total charge has been found to 
control the electroforming50. Once the electroforming is completed, 
the bipolar switching obviously takes place through local redox 
reactions between the virtual cathode and the anode, by forming or 
breaking the conductive contact. Depending on the charge transfer 
during the switching, the resistance of the system can be established 
at intermediate levels, which might help in creating multibit storage 
in future memory cells (Fig. 6)7.
As in the case of the electrochemical metallization process, RON 
is usually not pad-size dependent, indicating a filamentary switching 
in MIM structures, as reported, for example, for nanocrystalline 
Ta2O5 and Nb 2O5 thin films 51, VO2 thin films 52, TiO 2 thin films 11, 
nanoscale confined TiO 2 (ref. 53) and epitaxial SrZrO 3:Cr thin 
films54. Use of a conductive-tip atomic force microscope (C-AFM) 
technique has shown the conductive filaments to be identical 
to dislocations in the case of undoped SrTiO 3 single crystals and 
thin films55. Figure 7 shows that the conductivity enhancement by 
several orders of magnitude is confined to a region 1–2 nm wide 
at the exit of a dislocation. By repeated scanning with a suitably 
biased AFM tip, the dislocation can be made to switch between 
an ON and an OFF state. In the ON state, the conductivity shows 
metallic behaviour, in accordance with first principles calculations55. 
At the surface of ultrathin epitaxial SrTiO 3 films, entire areas can 
be reversibly switched between an ON and OFF state by C-AFM 
(Fig. 8). For these films also, high-resolution studies reveal the 
filamentary nature of the conductivity and their possible correlation 
to dislocations56. In the case of other materials, such as (La,Sr)MnO3 
thin films, the conductivity is confined to boundary regions between 
islands of about 100 nm diameter57.
Lateral MIM configurations allow for the observation of 
filaments along their extension between the electrodes. In undoped 
SrTiO3 single crystals, the formation of conductive filaments 
within a network of dislocations has been verified by combining 
electrocoloration studies by optical microscopy with C-AFM scans 
(Fig. 9)55. Infrared thermal microscopy of a Cr-doped SrTiO3 single 
crystal during a current load of 5  mA confirms the confinement of 
the current path and shows a ‘hot spot’ near the electrode, where the 
virtual cathode touches the anode (Fig. 10)58.
It must be noted that this class of ion-migration-based switching 
effects is much less well understood than the switching induced by 
cation migration that was described in the previous section. Open 
questions remain about the microscopic details of the ion transport, 
the defect structure and electronic charge transport properties of the 
conductive channels formed, details of the electrochemical redox 
reactions involved, and so forth. In several cases, it is not even clear 
what ions are involved in the process and whether the system falls 
into the cation- or anion-migration class.
R (Ω)
1.4 × 1010 Ω
3.2 × 106 Ω
0 40 80
D (nm)
AB (n1)
AB (n15)
I (nA)
50 nm
8.0
0.8
0.08
0.008
1012
1010
108
106
A
B
n1
n15
25 nm
25 nm
A
B
–—
–—
a
b
1 nm
0.008 nA
3.5 nA
Figure 7 Conductance of individual dislocations in srt io3. a, a conductivity map of 
the surface of an undoped srt io3 single crystal as recorded by C-af M after modest 
thermal reduction. b, l ine scan across the selected spot (D denoting the distance 
along aB) showing the dynamic range of the conductance increase as a result of 
the application of a negative voltage to the af M tip. Right: conductivity maps of the 
selected spot before and after electroformation. f rom ref. 55.
Figure 8 area-wide switching of an epitaxial 10-nm srt io3 thin film by C-af M. 
t he left scan is produced with a tip voltage of –6 V and subsequently with +6 V in 
the inner area; the right scan is subsequently scanned with –6 V within the inner 
on -state area. Reprinted with permission from ref. 56.
500 
nm
10
1
0.1
0.01
OFF
OFF
ON
ON
ON
© 2007 WILEY
© 2007 Nature Publishing Group 

838	 nature materials | VOL 6 | NOVEMBER 2007 | www.nature.com/naturematerials
REVIEW ARTICLES | insight
Resisti Vely s Wit Ching syste Ms in Vol Ving o Rgani C Mole Cules
Resistive switching has been seen in a large variety of MIM systems 
in which the ‘I’ layer is represented by organic molecules or polymers 
of typically 30 nm to >1 μm thickness59–61. The characteristics of the 
organic compounds include redox activity, the formation of a charge-
transfer complex, and the formation of donor–acceptor couples. 
A recent review 62 summarizes the literature comprehensively and 
classifies the conceivable switching mechanisms, but in many cases 
the database is too weak to draw definite conclusions. Note that 
in several studies an aluminium top electrode has been used that 
is deposited onto the organic layer in an ex situ deposition step. 
Recent control experiments indicate that the organic layer is not 
always essential for the switching. Instead the switching event seems 
to take place in a thin Al 2O3 layer inevitably formed between the 
organic layer and the aluminium metal, as found for rose Bengal 63, 
for polyethylenedioxythiophene (PEDOT)64, and for Cu-tetracyano-
quinodimethane (Cu-TCNQ)65. In the latter case, a thin aluminium 
oxide/hydroxide layer was suggested as the conducting layer for 
copper ions in a cation-migration-based electrochemical switch.
In another class of potential molecular memories, the ‘I’ layer in 
a MIM system is a monomolecular film or even a single molecule 
contacted by a metal tip on the nanoscale. The aim of these molecular 
electronic studies is to make use of processes such as molecular redox, 
molecular configuration and conformation changes, or molecular 
electronic excitations, as well as molecular spin properties that may 
affect the electron transfer coefficient66. In one of the experiments, 
however, in which a redox process within a specific catenane molecule 
was originally attributed to the resistive switching of a monolayer67, 
a control experiment using electronically inactive alkanoic acids 
revealed a very similar I–V behaviour68, and a conceivable mechanism 
based on the electrochemistry of the oxide layers formed at the metal 
electrodes has been suggested69.
These examples show that great care must be exercised in 
attributing mechanistic models to observed switching events and 
that many critical control experiments are required to obtain an 
microscopic understanding. Certainly, specific organic molecules 
have advantageous electronic properties. But the inherent 
characteristics of these molecules are easily masked by the electrode 
materials and the experimental boundary conditions. The redox 
activity of viologen molecules unveiled in an electrochemical in situ 
experiment using scanning tunnelling microscopy (STM) 70,71 and 
of specific oligophenylene molecules in mechanically controllable 
break-junction experiments72 are some of of the rare examples in 
which inherent molecular properties are observed.
Chip aRChite Ctu Re, Relia Bility , s Caling and outlook
In a random access memory (RAM) the storage cells are organized 
in a matrix. Along the rows and columns of the matrix, there are 
write and read lines, respectively, which are connected to electronic 
line drives and sense amplifiers in the periphery of the matrix 30. 
Optical microscope
100 µm
2,000 nm
20 µm
AFM tapping mode
[010]
[100]
30 µm
Cathode Anode
a
b c
100 nm
LC-AFM contact current mode
105 nA 102 nA
1,000 nm
Figure 9 f ilamentary structure induced by electroformation in an undoped srt io3 single crystal. f rom ref. 55. a, optical micrograph of the filamentary structure created in the 
skin region of a thermally pre-reduced crystal by electroformation between planar gold electrodes. segments from left to right: near the cathode, in the central region, and near 
the anode. Clearly visible is the orthogonal network along the crystallographic [100] direction of the crystal. insets show the possible fine structure of filaments at the cathode 
(left) and gas bubble that have developed under the anode metal (right). b, high resolution of the scene as recorded by C-af M at a location between the electrodes, where 
filaments have terminated at the surface. Measurements support the filamentary character of conductance and the fine structure of the high-conductivity spots. c, etch pits of the 
same kind of crystal give an example of the distribution of disl ocations crossing the surface, highlighting the natural tendency to agglomerate along crystallographic directions.
© 2007 Nature Publishing Group 

nature materials | VOL 6 | NOVEMBER 2007 | www.nature.com/naturematerials 839
REVIEW ARTICLES | insight
Resistively switching storage cells may be organized in a passive cross-
bar matrix, just connecting the word and bit lines at each node. The 
detailed circuit requirements depend on the type (unipolar or bipolar) 
of switch. Alternatively, in an active matrix, there is a select transistor 
at each node which decouples the storage cell if it is not addressed. 
This concept significantly reduces crosstalk and disturb signals in the 
matrix. Although a passive matrix can, in principle, be fabricated on 
a (4/n)F2 scheme per cell (where F denotes the minimum feature size 
of the fabrication technology and n the number of memory layers in a 
multilayer stack), the cells in an active matrix require somewhat more 
space, of the order of 4 to 8F2. Both passive matrices38,73,74 and active 
matrices12,45 have been realized in prototype RRAMs. In passive arrays 
the storage cells need to incorporate diodes in series with the switchable 
resistors in order to avoid signal bypasses by cells in the ON state. For 
oxide-based unipolar cells, a sandwich concept has been proposed to 
integrate the diode function75. In the case of bipolar cells, serial elements 
with a Zener diode or varistor characteristic are required. In addition, 
for medium and large passive matrices the interconnect resistances 
must be taken into account, requiring dedicated reference schemes76.
Resistive switching cells offer application opportunities that 
go beyond mere high-density memory devices. In particular, they 
can be used as reconfigurable switches in field-programmable 
gate-array (FPGA) type logic too. About 10 years ago, the Hewlett-
Packard research labs developed a prototype computer, called the 
T eramac, entirely built from conventional, CMOS-based FPGAs, 
interconnected through several hierarchical levels by a ‘fat tree’ 77. 
They replaced the traditional computer programming based on von 
Neumann architecture by reconfiguration of the look-up matrices in 
the FPGAs of the T eramac. The concept proved to be efficient and, 
as a particular benefit, highly defect-tolerant because during the 
configuration phase routes could be made around all defects. Defect 
tolerance is one of the essential demands on any future computer as 
the defect rate will inherently increase with decreasing feature sizes. 
The far-reaching idea of the T eramac project has been to replace the 
complex cells in the conventional FPGAs by nanoscale two-terminal 
resistive switches. In recent years, considerable progress has been 
made in resistively switching matrices (described in this review) and 
in the further elaboration of the architecture concept78–81.
Compared with several other emerging memory concepts, the 
RRAM concept including its different variants is immature. As a 
consequence, the performance and reliability, and in particular the 
microscopic mechanism of processes limiting the reliability, have 
not yet been studied in detail. First results look promising. Switching 
times of under 10 ns have been reported for individual oxide cells82. 
In the case of cation-migration-induced processes, fatigue of the 
switching hysteresis of high-density RRAM prototypes did not occur 
within 106 write cycles and 1012 read cycles12,83. A data retention time 
of over 10  years has been extrapolated, for example, for Ag/GeSe x 
RRAMs83. Y et these are just first results. Once we fully understand 
the particular switching mechanisms, we will need detailed studies of 
reliability, including a thorough investigation of all conceivable failure 
mechanisms, and optimization steps based on these.
For the further evolution of nanoelectronics, the question of 
inherent physical limits to scaling as well as possible technological 
barriers to scaling is most important. One ultimate limit will be 
given by the tunnelling distance between neighbouring cells as well 
as the leakage current from the word and bit line, again potentially 
dominated by tunnelling 84. Another limit is obviously set by the 
lateral extension of the switching area, typically the cross-section of 
the switching filament as described above. These limits depend on the 
class of the resistive switching mechanism. The scaling of thermally 
switching cells will depend on the specific heat capacities and thermal 
conductivities of the materials involved in the cell, limiting the scaling 
by the onset of thermal cross-talk as in PCRAMs 48. Cells based on 
electrical effects depend on the size of electrostatic barriers controlled 
by the shift of the charges involved 85. Ionic switching cells may be 
limited in scaling by the random diffusion of migrating ions involved 
as well as the metal atoms, in the case of cation-migration-induced 
redox switching. They may also be limited by poor uniformity due to 
inherent impurities in the materials. If this is the case, then obviously 
the downscaling may be limited by the requirements of data retention. 
Proper selection of materials for their diffusion rates and precisely 
defined material interfaces on the atomic scale may limit this problem 
to the point that it falls beyond the ultimate tunnelling limit. In this 
respect, ion-migration-induced redox-type switching might offer 
huge potential for future high-density non-volatile memories.
T echnologically, the scaling of the RRAMs will be determined by the 
fabrication of efficient and reliable electrode contacts and interconnects 
within the matrix. Although great progress has been made in recent 
years74,78, the structures are still far from any tunnelling limit. Another 
obvious limit to scaling of the chip size will be the size of the periphery 
circuit and, for active matrices, the size of the access transistors within 
the matrix. Concepts have been proposed in which the resistive 
switching cross-bar matrix is slightly rotated against the array of CMOS 
cells underneath, lifting the alignment constraints considerably80,86. 
This approach can be used to continue the downscaling of the resistive 
switching cells without having to shrink the access transistors.
Much research effort is still needed to explore the potential of 
the resistive switching effect in general, and ion-migration-based 
redox effects in particular, and to exploit this potential to its limits. 
Questions requiring further attention include a deeper understanding 
of the microscopic mechanism of the switching, the process and 
material optimization, the effects limiting the reliability, all aspects of 
fabrication technology, and the guidelines for scaling.
doi:10.1038/nmat2023
References
1. Hickmott, T. W . Low-frequency negative resistance in thin anodic oxide films. J. Appl. Phys. 
33, 2669–2682 (1962). 
2. Dearnaley, G., Stoneham, A. M. & Morgan, D. V . Electrical phenomena in amorphous oxide films. 
Rep. Prog. Phys. 33, 1129–1191 (1970). 
3. Oxley, D. P . Electroforming, switching and memory effects in oxide thin films. 
Electrocomponent Sci. Technol. UK 3, 217–224 (1977). 
4. Pagnia, H. & Sotnik, N. Bistable switching in electroformed metal-insulator-metal devices. 
Phys. Status Solidi 108, 11–65 (1988). 
5. Asamitsu, A., Tomioka, Y ., Kuwahara, H. & Tokura, Y . Current switching of resistive states in 
magnetoresistive manganites. Nature 388, 50–52 (1997). 
6. Kozicki, M. N., Yun, M., Hilt, L. & Singh, A. Applications of programmable resistance changes in 
metal-doped chalcogenides. Pennington NJ USA: Electrochem. Soc. 298–309 (1999). 
Figure 10 infrared thermal micrograph of a planar Cr-doped srt io3 single-crystal 
cell. t he cell has a current of 5 ma at an applied voltage of 30 V. in the colour scale, 
blue and red represent room temperature and elevated temperature, respectively. 
f rom ref. 58.
Anode
Cathode
25 µm
© 2007 WILEY
© 2007 Nature Publishing Group 

840	 nature materials | VOL 6 | NOVEMBER 2007 | www.nature.com/naturematerials
REVIEW ARTICLES | insight
7. Beck, A., Bednorz, J. G., Gerber, C., Rossel, C. & Widmer, D. Reproducible switching effect in thin 
oxide films for memory applications. Appl. Phys. Lett. 77, 139–141 (2000). 
8. Chudnovskii, F . A., Odynets, L. L., Pergament, A. L. & Stefanovich, G. B. Electroforming and 
switching in oxides of transition metals: the role of metal-insulator transition in the switching 
mechanism. J. Solid State Chem. 122, 95–99 (1996). 
9. Bruyere, J. C. & Chakraverty, B. K. Switching and negative resistance in thin films of nickel oxide. 
Appl. Phys. Lett. 16, 40–43 (1970). 
10. Kim, D. C. et al. Electrical observations of filamentary conductions for the resistive memory 
switching in NiO films. Appl. Phys. Lett. 88, 202102 (2006). 
11. Choi, B. J. et al. Resistive switching mechanism of TiO2 thin films grown by atomic-layer deposition. 
J. Appl. Phys. 98, 033715 (2005). 
12. Baek, I. G. et al. Highly scalable nonvolatile resistive memory using simple binary oxide driven by 
asymmetric unipolar voltage pulses. IEDM Tech. Digest, 587–590 (2005). 
13. Jeong, D. S., Schroeder, H. & Waser, R. Coexistence of bipolar and unipolar resistive switching 
behaviors. Electrochem. Solid-State Lett. 10, G51-G53 (2007). 
14. Simmons, J. G. & Verderber, R. R. New conduction and reversible memory phenomena in thin 
insulating films. Proc. R. Soc.Lond. A 301, 77–102 (1967). 
15. Ouyang, J. Y ., Chu, C. W ., Szmanda, C. R., Ma, L. P . & Y ang, Y . Programmable polymer thin film and 
non-volatile memory device. Nature Mater. 3, 918–922 (2004). 
16. Bozano, L. D. et al. Organic materials and thin-film structures for cross-point memory cells based 
on trapping in metallic nanoparticles. Adv. Funct. Mater. 15, 1933–1939 (2005). 
17. Guan, W . et al. Fabrication and charging characteristics of MOS capacitor structure with metal 
nanocrystals embedded in gate oxide. J. Phys. D 40, 2754–2758 (2007). 
18. Sawa, A., Fujii, T., Kawasaki, M. & Tokura, Y . Interface resistance switching at a few nanometer thick 
perovskite manganite active layers. Appl. Phys. Lett. 88, 232112 (2006). 
19. Fujii, T. et al. Hysteretic current–voltage characteristics and resistance switching at an epitaxial oxide 
Schottky junction SrRuO3/SrTi0.99Nb0.01O3. Appl. Phys. Lett. 86, 012107 (2005). 
20. Lee, D. et al. in Proc. Non-Volatile Memory Technology Symposium (ed. Campbell, K.) 89–93 (IEEE, 
Piscataway, New Jersey, 2006).
21. Hovel, H. J. & Urgell, J. J. Switching and memory characteristics of ZnSe–Ge heterojunctions. 
J. Appl. Phys. 42, 5076–5083 (1971). 
22. Fors, R., Khartsev, S. I. & Grishin, A. M. Giant resistance switching in metal-insulator-manganite 
junctions: evidence for Mott transition. Phys. Rev. B 71, 045305 (2005). 
23. Kim, D. S., Kim, Y . H., Lee, C. E. & Kim, Y . T. Colossal electroresistance mechanism in a  
Au/Pr0.7Ca0.3MnO3/Pt sandwich structure: evidence for a Mott transition. Phys. Rev. B 
74, 174430 (2006). 
24. Meijer, G. I. et al. Valence states of Cr and the insulator-to-metal transition in Cr-doped SrTiO3. 
Phys. Rev. B 72, 155102 (2005). 
25. Rozenberg, M. J., Inoue, I. H. & Sanchez, M. J. Nonvolatile memory with multilevel switching: a 
basic model. Phys. Rev. Lett. 92, 178302 (2004). 
26. Rozenberg, M. J., Inoue, I. H. & Sanchez, M. J. Strong electron correlation effects in nonvolatile 
electronic memory devices. Appl. Phys. Lett. 88, 033510 (2006). 
27. Esaki, L., Laibowitz, R. B. & Stiles, P . J. Polar Switch. IBM Tech. Discl. Bull. 13, 2161 (1971). 
28. Kohlstedt, H., Pertsev, N. A., Contreras, J. R. & Waser, R. Theoretical current–voltage characteristics 
of ferroelectric tunnel junctions. Phys. Rev. B 72, 125341 (2005). 
29. Tsymbal, E. Y . & Kohlstedt, H. Tunneling across a ferroelectric. Science 313, 181–183 (2006). 
30. Waser, R. Nanoelectronics and Information Technology 2nd edn (Wiley-VCH, Weinheim, 2003). 
31. Maier, J. Nanoionics: ion transport and electrochemical storage in confined systems. Nature Mater. 
4, 805–818 (2005). 
32. Terabe, K., Hasegawa, T., Nakayama, T. & Aono, M. Quantized conductance atomic switch. Nature 
433, 47–50 (2005). 
33. Ercker, L. Treatise on Ores and Assaying (1547) (transl. Sisco, A. G. & Smith, C. S., Univ. Chicago, 
1951), p. 177. 
34. Faraday, M. Phil. Trans. R. Soc. Lond. 123, 507–522 (1833). 
35.  Wagner, C. Physical chemistry of ionic crystals involving small concentrations of foreign substances. 
J. Phys. Chem. 57, 738–742 (1953). 
36. Hirose, Y . & Hirose, H. Polarity-dependent memory switching and behaviour of Ag dendrite in 
Ag-photodoped amorphous As2S3 films. J. Appl. Phys. 47, 2767–2772 (1976). 
37. Tamura, T. et al. Switching property of atomic switch controlled by solid electrochemical reaction. 
Jpn. J. Appl. Phys. 45, L364-L366 (2006). 
38. Kaeriyama, S. et al. A nonvolatile programmable solid-electrolyte nanometer switch. 
IEEE J. Solid-State Circuits USA 40, 168–176 (2005). 
39. Sakamoto, T. et al. A Ta2O5 solid-electrolyte switch with improved reliability. VLSI Technol. Digest 
Tech. Pap. (in the press). 
40. Zheng-Wang et al. Resistive switching mechanism in ZnxCd1–xS nonvolatile memory devices. 
IEEE Electron Dev. Lett. 28, 14–16 (2007). 
41. Kozicki, M. N., Gopalan, C., Balakrishnan, M. & Mitkova, M. A low-power nonvolatile 
switching element based on copper-tungsten oxide solid electrolyte. IEEE Trans. Nanotechnol. 
5, 535–544 (2006). 
42. Schindler, C., Puthen Thermadam, S. C., Kozicki, R. &Waser, M. N. Bipolar and unipolar resistive 
switching in Cu-doped SiO2. IEEE Trans. Electron Dev. (in the press). 
43. van-der-Sluis, P . Non-volatile memory cells based on ZnxCd1–xS ferroelectric Schottky diodes. 
Appl. Phys. Lett. 82, 4089–4091 (2003). 
44. Kund, M. et al. Conductive bridging RAM (CBRAM): an emerging non-volatile memory technology 
scalable to sub 20 nm. IEDM Tech. Digest, 754–757 (2005). 
45. Dietrich, S. et al. A nonvolatile 2-Mbit CBRAM memory core featuring advanced read and program 
control. IEEE J.Solid-State Circuits 42, 839–845 (2007). 
46. Xie, F . Q., Nittler, L., Obermair, C. & Schimmel, T. Gate-controlled atomic quantum switch. 
Phys. Rev. Lett. 93, 128303 (2004). 
47. Banno, N., Sakamoto, T., Hasegawa, T., Terabe, K. & Aono, M. Effect of ion diffusion on switching 
voltage of solid-electrolyte nanometer switch. Jpn. J. Appl. Phys. 45, 3666–3668 (2006). 
48. Wuttig, M. & Y amada, N. Phase change materials for rewriteable data storage. Nature Mater. 
6, 824–832 (2007). 
49. Baiatu, T., Waser, R. & Hardtl, K. H. DC electrical degradation of perovskite-type titanates. III. 
A model of the mechanism. J. Am. Ceram. Soc. 73, 1663–1673 (1990). 
50. Watanabe, Y . et al. Current-driven insulator-conductor transition and nonvolatile memory in 
chromium-doped SrTiO3 single crystals. Appl. Phys. Lett. 78, 3738–3740 (2001). 
51. Pinto, R. Filamentary switching and memory action in thin anodic oxides. Phys. Lett. A 
35, 155–156 (1971). 
52. Beaulieu, R. P ., Sulway, D. V . & Cox, C. D. The detection of current filaments in VO2 thin-film 
switches using the scanning electron microscope. Solid-State Electron. 3, 428–429 (1973).
53. Ogimoto, Y ., Tamia, Y ., Kawasaki, M. & Tokura, Y . Resistance switching memory device with a 
nanoscale confined current path. Appl. Phys. Lett. 90, 143515 (2007).
54. Rossel, C., Meijer, G. I., Bremaud, D. & Widmer, D. Electrical current distribution across a 
metal-insulator-metal structure during bistable switching. J. Appl. Phys.  
90, 2892–2898 (2001). 
55. Szot, K., Speier, W ., Bihlmayer, G. & Waser, R. Switching the electrical resistance of individual 
dislocations in single-crystalline SrTiO3. Nature Mater. 5, 312–320 (2006). 
56. Szot, K., Dittmann, R., Speier, W . & Waser, R. Nanoscale resistive switching. Phys. Status Solidi 
1, R86–R88 (2007). 
57. Chen, X., Wu, N., Strozier, J. & Ignatiev, A. Spatially extended nature of resistive switching in 
perovskite oxide thin films. Appl. Phys. Lett. 89, 063507 (2006). 
58. Janousch, M. et al. Role of oxygen vacancies in Cr-doped SrTiO3 for resistance-change memory. 
Adv. Mater. 19, 2232–2235 (2007). 
59. Pender, L. F . & Fleming, R. J. Memory switching in glow discharge polymerized thin films. 
J. Appl. Phys. 46, 3426–3431 (1975). 
60. Potember, R. S., Poehler, T. O. & Cowan, D. O. Electrical switching and memory phenomena in 
Cu-TCNQ thin films. Appl. Phys. Lett. 34, 405–407 (1979). 
61. Bandyopadhyay, A. & Pal, A. J. Large conductance switching and memory effects in organic 
molecules for data-storage applications. Appl. Phys. Lett. 82, 1215–1217 (2003). 
62. Scott, J. C. & Bozano, L. D. Nonvolatile memory elements based on organic materials. Adv. Mater. 
19, 1452–1463 (2007). 
63. Karthauser, S. et al. Resistive switching of rose bengal devices: a molecular effect? J. Appl. Phys. 
100, 094504 (2006). 
64. Colle, M., Buchel, M. & de-Leeuw, D. M. Switching and filamentary conduction in non-volatile 
organic memories. Org. Electron. 7, 305–312 (2006). 
65. Kever, T., Boettger, U., Schindler, Ch. & Waser, R. On the origin of bistable resistive switching in 
Cu:TCNQ. Appl. Phys. Lett. 91, 083506 (2007).
66. Feringa, B. L. Molecular Switches (Wiley-VCH, Weinheim, 2001). 
67.  Collier, C. P . et al. A [2]catenane-based solid state electronically reconfigurable switch. Science 
289, 1172–1175 (2000). 
68. Stewart, D. R. et al. Molecule-independent electrical switching in Pt/organic monolayer/Ti devices. 
Nano Lett. 4, 133–136 (2004). 
69. Blackstock, J. J. et al. Internal structure of a molecular junction device: chemical reduction of PtO2 
by Ti. J. Phys. Chem. C 111, 16–20 (2007). 
70. Li, Z. et al. Two-dimensional assembly and local redox-activity of molecular hybrid structures in an 
electrochemical environment. Faraday Disc. 131, 121–143 (2005). 
71. Li, Z., Pobelov, I., Han, B., Wandlowski, T., Blaszczyk, A. & Mayor, M. Conductance of  
redox-active single molecular junctions: an electrochemical approach. Nanotechnology 
18, 1–8 (2007). 
72. Lörtscher, E., Ciszek, J. W ., Tour, J. & Riel, H. Reversible and controllable switching of a single-
molecule junction. Small 2, 973–977 (2006).
73. Wu, W . et al. One-kilobit cross-bar molecular memory circuits at 30-nm half-pitch fabricated by 
nanoimprint lithography. Appl. Phys. A 80, 1173–1178 (2005). 
74. Green, J. E. et al. A 160-kilobit molecular electronic memory patterned at 1011 bits per square 
centimetre. Nature 445, 14–17 (2007). 
75. Lee, M. J. et al. A low-temperature grown oxide diode as a new switch element for high-density, 
nonvolatile memories. Adv. Mater. 19, 73–76 (2007). 
76. Mustafa, J. & Waser, R. A novel reference scheme for reading passive resistive crossbar memories. 
IEEE Trans. Nanotechnol. 5, 687–691 (2006). 
77. Heath, J. R., Kuekes, P . J., Snider, G. S. & Williams, R. S. A defect-tolerant computer architecture: 
opportunities for nanotechnology. Science 280, 1716–1721 (1998). 
78. Snider, G., Kuekes, P ., Hogg, T. & Williams, R. S. Nanoelectronic architectures. Appl. Phys. A 
80, 1183–1195 (2005). 
79. DeHon, A., Randy Huang, & Wawrzynek, J. Stochastic spatial routing for reconfigurable networks. 
Microprocessors Microsyst. 30, 301–318 (2006). 
80. Likharev, K. K. & Strukov, D. B. in Introducing Molecular Electronics. Lecture Notes in Physics 
Vol. 680 (eds Cuniberti, G., Richter, K. & Fagas, G.) 447–477 (Springer, Berlin, 2006).
81. Lu, W . & Lieber, C. M. Nanoelectronics from the bottom up. Nature Mater.  
6, 841–850 (2006).
82. Ignatiev, A. et al. Resistance switching in perovskite thin films. Phys. Stat. Sol. B 
243, 2089–2097 (2006). 
83. Honigschmid, H. et al. A non-volatile 2Mbit CBRAM memory core featuring advanced read and 
program control. VLSI Circuits Symp. Tech. Digest, 110–11(2006). 
84. Zhirnov, V . V ., Cavin-R-K-III, Hutchby, J. A. & Bourianoff, G. I. Limits to binary logic switch 
scaling—a gedanken model. Proc. IEEE USA 91, 1934–1939 (2003). 
85. Cavin, R. K., Zhirnov, V . V ., Herr, D. J. C., Alba Avila, & Hutchby, J. Research directions and 
challenges in nanoelectronics. J.Nanoparticle Res. 8, 841–858 (2006). 
86. Snider, G. S. & Williams, R. S. Nano/CMOS architectures using a field-programmable nanowire 
interconnect. Nanotechnology 18, 1–11 (2007). 
acknowledgements
We thank J. G. Bednorz (IBM Research, Zurich), U-In Chung, I. G. Baek and S. O. Park (Samsung 
Electronics), Y. Zhang (Intel, Santa Clara), R. Bruchhaus (Qimonda, Munich), V . Zhirnov (SRC), and 
K. Szot and R. Dittmann (Research Center Jülich) for valuable comments.
Correspondence and requests for materials should be addressed to R.W.
© 2007 Nature Publishing Group
