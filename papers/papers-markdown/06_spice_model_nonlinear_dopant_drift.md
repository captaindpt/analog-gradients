# 06_spice_model_nonlinear_dopant_drift.pdf

210 Z. BIOLEK, D. BIOLEK, V. BIOLKOVÁ, SPICE MODEL OF MEMRISTOR WITH NONLINEAR DOPANT DRIFT 
SPICE Model of Memristor with Nonlinear Dopant Drift 
Zdeněk BIOLEK1, Dalibor BIOLEK2,3, Viera BIOLKOVÁ4 
1 SŠIEŘ Rožnov pod Radhoštěm, Školní 1610, 756 61 Rožnov p.R., Czech Republic 
2 Dept. of Electrical Engineering, University of Defense, Kounicova 65, 612 00 Brno, Czech Republic 
3 Dept. of Microelectronics/4 Radio Electronics, Brno University of Technology, Purkyňova 118, 612 00 Brno, Czech Rep. 
zdenek.biolek@roznovskastredni.cz,  dalibor.biolek@unob.cz,  biolkova@feec.vutbr.cz 
 
Abstract. A mathematical model of the prototype of mem-
ristor, manufactured in 2008 in Hewlett-Packard Labs, is 
described in the paper. It is shown that the hitherto pub-
lished approaches to the m odeling of boundary conditions 
need not conform with the requirements for the behavior of 
a practical circuit element. The described SPICE model of 
the memristor is thus constr ucted as an open model, ena-
bling additional modifica tions of non-linear boundary 
conditions. Its functionality is illustrated on computer 
simulations. 
Keywords 
Memristor, drift, window function, SPICE. 
1. Introduction 
On May 1 st, 2008, a research group from Hewlett-
Packard laboratories, led by Dr. Williams, published 
a report [1] about the manufacture of a memristor, the so-
called fourth elementary passive element. Its existence was 
predicted in 1971 by professor Chua in his famous paper 
[2]. The future of this circuit element seems to be promis-
ing. Intensive research is under way in HP labs, focusing 
on revolutionary applications of the memristor in ultra-
dense memory cells (RRAM, Resistive Random-Access 
Memory), when this element act s as a crossbar switch [3]. 
Also, the utilization of memristors in the analog mode as 
synapses in a neural computi ng architecture is anticipated 
because such a technology seems to be dense enough to 
simulate processes in the human brain [4]. 
Over the 10 months since the announcement of the 
above break-through in [1], numerous papers have 
appeared with the ai m to analyze the elementary attributes 
of the memristor as a passive circuit element, manufactured 
in HP labs [5], [6]. The input data for such analyses, i.e. 
information about the physical model of the memristor, 
were taken particularly from the original work [1]. Since 
real samples of the memristor are inaccessible to most 
researchers, it is useful to have a computer model of the 
memristor as a tool for speed ing-up the analysis of the 
behavior and developing appli cations of this interesting 
circuit element via simulation experiments. 
With regard to the fact that memristor is specified as 
the fourth, newly discovered passive circuit element, 
supplementing the well-known R, C, L triplet (resistor, 
capacitor, inductor), it is logical to suggest extending the 
model libraries of SPICE-family simulating programs just 
with the model of the memristor.  
The purpose of this paper is a description of the 
working SPICE model of the memristor, manufactured in 
HP labs. The paper structure is as follows: Section 2, 
which follows this Introduction, summarizes the informa-
tion about the physical and mathematical models of the 
memristor, already published in [1] and [5]. Section 3 
introduces the SPICE model of the memristor, which starts 
from the mathematical model in Section 2. Section 4 is 
devoted to the demonstrations of SPICE simulations that 
are based on the proposed model. Some open problems and 
pending issues of the boundary effects modeling are 
discussed in Section 5.  
2. Model of the Memristor from HP 
Labs 
The physical model of the memristor from [1], shown 
in Fig. 1, consists of a two-layer thin film (size D ≈ 10 nm) 
of TiO2, sandwiched between platinum contacts. One of the 
layers is doped with oxygen v acancies and thus it behaves 
as a semiconductor. The second, undoped region, has an 
insulating property. As a consequence of complex material 
processes, the width w of the doped region is modulated 
depending on the amount of electric charge passing 
through the memristor. With electric current passing in a 
given direction, the boundary between the two regions is 
moving in the same direction. The total resistance of the 
memristor, R
MEM, is a sum of the resistances of the doped 
and undoped regions,  
 ( )( ) xRxRxR OFFONMEM −+= 1 ,  (1) 
 where () 1,0∈= D
wx   (2) 
is the width of the doped region, referenced to the total 
length D of the TiO 2 layer, and ROFF and RON are the limit 
values of the memristor resistance for w=0 and w=D. The 
ratio of the two resistances is usually given as 102 - 103. 

RADIOENGINEERING, VOL. 18, NO. 2, JUNE 2009 211 
 
v
i
w
D
doped undoped
 
Fig. 1. Memristor model according to [1]. 
The Ohm’s law relation is applicable between the 
memristor voltage and current:  
 () ( ) () tiwRtv MEM= . (3) 
The speed of the movement of the boundary between the 
doped and undoped regions depends on the resistance of 
doped area, on the passing current, and on other factors 
according to the state equation [1]  
 
() )(xftikdt
dx = ,  
2D
Rk ONvμ=  (4) 
where μv ≈ 10-14 m2s-1V-1 is the so-called dopant mobility. 
As mentioned in [1], in nanoscale devices, small voltages 
can yield enormous electric fields, which can secondarily 
produce significant nonlinearities in ionic transport. These 
nonlinearities manifest themselves particularly at the thin 
film edges, where the speed of the boundary between the 
doped and undoped regions gradually decreases to zero. 
This phenomenon, called nonlinear dopant drift, can be 
modeled by the so-called window function f(x) on the right 
side of (4). A concrete window function that would 
correspond to the memristor from HP labs is not available 
at this moment. 
The paper [5] proposes the window function in the 
following form: 
 
() ( )
p
xxf
2
121 −−=  (5) 
where p is a positive integer.  
The form of function (5) guarantees zero speed of the 
x-coordinate when approaching either boundary. More-
over, the differences between the models with linear and 
nonlinear drift disappear when p increases.  
3. SPICE Model 
State equation (4) and port equation (3) of the memristor 
can be modeled by the block-oriented diagram in Fig. 3. 
The memory effect of the memristor is modeled via a feed-
back-controlled integrator. With regard to the limiting 
boundary conditions, it stores the effects of the passing 
current, and controls the memr istor resistance via modify-
ing the boundary position. The nonlinear drift and the in-
fluence of the boundary cond itions are modeled by the 
feedback via the nonlinear window function f( ). 
x
 ()xf
1
1
0.5
0.50
0
p= 1
p= 10
 
Fig. 2. The window function (5) for different values of integer 
p. 
 
ƒ( ) 
x 
∫ 
v 
i 
±
k  
x  
 
Fig. 3. Block diagram of the memristor model. 
plus
minus
x
flux charge
Emem
 ∫ dtVmem  ∫ dtImem
))(( xVf Ik
x
mem
0
 )(xRVΔ−
 
memV
Imem
Roff
Gx
Eflux Echarge
Cx
 
Fig. 4. Structure of the SPICE model. 
The structure of the SPICE model is shown in Fig. 4. 
The relation between the memristor voltage and current is 
modeled on the basis of the modified equation (1):  
 
( ) RxRxR OFFMEM Δ−= , ONOFF RRR −=Δ . (6) 
In Fig. 4, equation (6) corresponds to the ROFF resistor in 
series with the E-type voltage source whose terminal volt-

212 Z. BIOLEK, D. BIOLEK, V. BIOLKOVÁ, SPICE MODEL OF MEMRISTOR WITH NONLINEAR DOPANT DRIFT 
age is controlled according to the formula “- xΔR”. The 
normalized width x of the doped layer is modeled by the 
voltage V(x) of the capacitor Cx, which serves as an inte-
grator of the quantities on the right side of state equation 
(4). The initial state of the normalized width of the doped 
layer x0, which is modeled as initial voltage of the capaci-
tor, is determined by the initial resistance RINIT of the mem-
ristor according to the formula, derived from (6): 
 
R
RRx INITOFF
Δ
−=0 . (7) 
The model is implemented as a SPICE subcircuit with 
parameters which can pass the following values into the 
subcircuit as arguments: the initial 
RINIT resistance, the ROFF 
and RON resistances, the width of the thin film D, the 
dopant mobility μv, and the exponent p of the window 
function. The list of the SPICE subcircuit mentioned below 
includes conventional model of the window function ac-
cording to Joglekar [5], which is open to any modifications 
of the functions describing the nonlinear drift, including 
the import of experimentally acquired data.  
The SPICE model is also complemented with direct 
computation of the integral quantities which define the 
memristor, i.e. the time integrals of electrical voltage (flux) 
and of electric current (charg e). These quantities belong to 
the results of the SPICE anal ysis, being available as volt-
ages of the internal controlled sources 
Eflux and Echarge. 
4. Demonstrations of SPICE Analyses 
The SPICE model from Section 3 was used for the 
simulation of experiments described in [1]. The appropriate 
results are shown in Figs 5 (a), (b), and (c). In each case, 
the memristor is driven by a voltage source.  
As follows from the waveforms of voltages Vx in Figs 
5 (a, b), the memristor works in a regime such that the 
boundary between the doped and undoped layers does not 
approach the edges with domin ant nonlinear effects. More 
detailed simulations prove the fact from [1] that the typical 
loops in I-V curves are gradually suppressed when 
increasing the frequency of the applied voltage. 
Fig. 5 (c) demonstrates the simulation results for 
lower 
ROFF/RON ratios which cause, in conjunction with the 
sufficiently high amplitude of the applied voltage, the hard-
switching cases [1]. As shown in Fig. 5 (c), the normalized 
width 
x of the doped region is switched between the low 
and high levels near the limiting values of 0 and 1. The 
corresponding typical pattern of the I-V characteristic in 
Fig. 5 (c) is also in agreement with [1]. 
The charge&flux curves in Fig. 5, i.e. relationship 
between the time-domain integrals of electric cur-
rent&voltage of the memristor confirm the well known fact 
that there is a one-to-one co rrespondence between them, in 
spite of the I-V hysteresis effects. 
The simulation results in Fi g. 5 agree well with the 
graphs published in [1]. This, however, cannot be claimed 
for the remaining results, given in [1] in Figs 3 (a, b), 
which show the simulations of the memristor behavior with 
and without dynamic negative differential resistance in 
conditions of linear drift. An analysis, given in the follow-
ing Section, indicates that th e cause can consist in the cur-
rent methodology of modeling the boundary conditions via 
the window functions. 
* HP Memristor SPICE Model  
* For Transient Analysis only 
* created by Zdenek and Dalibor Biolek 
************************** 
* Ron, Roff  - Resistance in ON / OFF States 
* Rinit      - Resistance at T=0 
* D          - Width of the thin film 
* uv         - Migration coefficient 
* p  - Parameter of the WINDOW-function  
*  for modeling nonlinear boundary conditions 
* x          - W/D Ratio, W is the actual width  
* of the doped area (from 0 to D) 
* 
.SUBCKT memristor Plus Minus PARAMS: 
+ Ron=1K Roff=100K Rinit=80K D=10N uv=10F p=1 
*********************************************** 
* DIFFERENTIAL EQUATION MODELING  * 
*********************************************** 
Gx 0 x value={ I(Emem)*uv*Ron/D^2*f(V(x),p)} 
Cx x 0 1 IC={(Roff-Rinit)/(Roff-Ron)} 
Raux x 0 1T 
* RESISTIVE PORT OF THE MEMRISTOR * 
******************************* 
Emem plus aux value={-I(Emem)*V(x)*(Roff-Ron)} 
Roff aux minus {Roff} 
*********************************************** 
*Flux computation* 
*********************************************** 
Eflux flux 0 value={SDT(V(plus,minus))} 
*********************************************** 
*Charge computation* 
*********************************************** 
Echarge charge 0 value={SDT(I(Emem))} 
*********************************************** 
* WINDOW FUNCTIONS 
* FOR NONLINEAR DRIFT MODELING * 
*********************************************** 
*window function, according to Joglekar 
.func f(x,p)={1-(2*x-1)^(2*p)} 
*proposed window function 
;.func f(x,i,p)={1-(x-stp(-i))^(2*p)} 
.ENDS memristor 
Tab. 1. SPICE model of memristor. SDT and STP are standard PSPICE functions (time-domain integration, unity step). 

RADIOENGINEERING, VOL. 18, NO. 2, JUNE 2009 213 
5. Modeling the Boundary Effects – 
the Pending Issue 
The testing of the developed SPICE model of the 
memristor manufactured in HP laboratories under hard 
switching conditions pointed out  two problems, associated 
with the so-called boundary effects, both related to the way 
of defining window function (5). 
The first problem consists in the fact that when setting 
the memristor to the terminal state 
RON or ROFF, no external 
stimulus can change this stat e back to another value. In 
other words, such a memristor would be bound to hold its 
state forever. This conclusion is a direct consequence of 
state equation (4) and the zer o-value of the window func-
tion in either boundary state. 
According to the currently available information, the 
memristor from HP labs “remembers” the 
x-coordinate of 
the boundary between the two layers, not the amount of 
electric charge that passed th rough it. This coordinate is 
proportional to the charge only within the active area of the 
memristor. However, the second problem of window func-
tion (5) consists in modeling the memristor as a component 
which exactly remembers the entire charge which is pass-
ing through. This conclusion al so follows from state equa-
tion (4): if window function (5 ) is only a function of the 
x 
variable, then the electric charge  
 
()∫=
1
0
1
x
x fk
dq ξ
ξ  (8) 
is necessary for transposing the memristor state from x0 to 
x1, and the same charge but with different sign,  
 
() ()
12
1
0
0
1
qfk
d
fk
dq
x
x
x
x
−=−== ∫∫ ξ
ξ
ξ
ξ , (9) 
is required for its return from x1 to x0. When driving the 
memristor by a constant current within a time interval, e.g. 
one minute, the same time interval, one minute, would be 
necessary for restoring the st ate before this driving, 
regardless of the fact that the memristor could be in its 
terminal state all the time wh en the current flows. Such 
delays are unambiguously confirmed by SPICE simulations 
of the current-driven memristors. Unfortunately, such an 
operating regime of the memristor is not referenced in the 
current literature. 
As results from the above, the window function can 
be considered a measure of how precisely the memristor 
stores the amount of electric charge: the memory effect is 
lost at the boundaries. When th e current direction is re-
versed at this moment, the boundary starts to move in the 
opposite direction regardless of the past, which is lost, i.e. 
along another curve.  
The above discrepancy between the behavior of the 
model and the requirements fo r the operation of a real 
circuit element can be resolv ed by designing a modified 
window function which models the fact that the boundary 
speeds of approaching and r eceding from the thin film 
limits are different.  
The following function (10) with the graph in Fig. 6 
meets the above requirements:  
 
( )( )
p
ixxf
2
)(1 −−−= stp  (10) 
where p is a positive integer, i is the memristor current, and  
50u
0
0 0.1 0.3 0.4flux [Vs]
charge
[As]
200u
-200u
-1 0 1Vmem [V]
2
-2
Vmem
[V]
01 2 3time [s]
01 2 3time [s]
x
[-]
0
1
200u
-200u
Imem
[A]
Imem[A]
 
2
[V]
100u
0
charge
[As]
200u
-200u
Imem
[A]
Vmem
-2
200u
-200u
Imem
[A]
x
[-]
0
1
flux [Vs]0 1.20.4 0.8
Vmem [V]0-1.5 1.5
0 1 2 3time [s]
01 2 3time [s]
0 0.6flux [Vs]
-2 0 2Vmem [V]
23 4 5time [s]
23 4 5time [s]
7m
5m
charge[As]
20m
-20m
Imem
[A]
2
-2
Vmem
[V]
x
[-]
0
1
20m
-20m
Imem
[A]
-0.5
0.2 1.0 0.2
1.0-1.0 -0.5 -1
(a) (b) (c)
 
 
Fig. 5. Memristor with the parameters RON=100 Ω, p=10, driven by a voltage: (a) harmonic with an amplitude of 1.2 V and a frequency of 
1 Hz, (b) ±V0 (sinω0t)2 with V0= 1.5 V and f0=1 Hz, (c) harmonic with an amplitude of 2 V and a frequency of 1 Hz. Other parameters 
are: (a) ROFF=16 kΩ, RINIT=11 kΩ, (b) ROFF=38 kΩ, RINIT=28 kΩ, (c) ROFF=5 kΩ, RINIT=1 kΩ. Simulation in Fig. (c) confirms the hard 
switching effects [1].  

214 Z. BIOLEK, D. BIOLEK, V. BIOLKOVÁ, SPICE MODEL OF MEMRISTOR WITH NONLINEAR DOPANT DRIFT 
 ()
⎩
⎨
⎧
<
≥= 00
01
i
ii pro
prostp
. (11) 
The current is considered to be positive if it increases the 
width of the doped layer, or x → 1. Function (10) is zero at 
either edge. Increasing the p yields a flat window function 
with steep throughs to zeros at x = 0 and x = 1.  
x
 ()xf
1
1
0.5
0.50
0
 
Fig. 6. Proposal of a new window function, see (10), p = 2. 
Our hitherto results indicat e that all the conclusions 
from [1] can be proved by means of the above approach, 
but with the exception of the hard switching effects gov-
erned by nonlinear ionic drift wh ich is characterized by the 
symmetrical hysteresis loop in  Fig. 5 (c). On the other 
hand, this case is truly modeled via the window function 
according to Joglekar whose general utilization is problem-
atic in the light of the above an alysis. It has turned out that 
subsequent development of the memristor model should 
consist in a proper modifica tion of the window function 
which should not depend onl y on the state variable 
x. 
However, an acceleration of such a development may be 
expected as soon as detailed information about the 
nonlinear ionic drift is released. 
6. Conclusions 
The SPICE model of the memristor, made up on the 
basis of state equations and equations modeling the bound-
ary effects, offers results which are in good agreement with 
a part of the hitherto publishe d experiments. It should be 
noted that the differences be tween the behavior of the 
model in some concrete regimes of the operation and the 
anticipated behavior of the r eal circuit element may be due 
to the current methods of modeling nonlinear dopant drift. 
That is why the SPICE model of the memristor is designed 
such that it enables easy m odification of the nonlinear 
relations describing the boundary effects. Such a modifica-
tion can be done when the rele vant data are specified by 
the manufacturer. The usefulness of the model is amplified 
by the fact that samples of the memristor will be probably 
not available for a long time. Today, a lot of institutions are 
involved in research into the basic features of the memris-
tor. The results of SPICE simulations from Section 4 point 
to the possibility of conducti ng interesting simulation ex-
periments which can be of great importance for such 
a research.  
Acknowledgements 
The research described in the paper was supported by 
the Czech Grant Agency under grants Nos. 102/08/0784, 
102/09/1628, and by the research programmes of BUT No. 
MSM0021630503/513 and UDB No. MO FVT 0000403. 
References 
[1] STRUKOV, D.B., SNIDER, G.S., STEWART, D.R., WILLIAMS, 
R.S. The missing memristor found. Nature, 2008, vol. 453, 1 May 
2008, p. 80 – 83. 
[2] CHUA, L.O. Memristor – the missing circuit element. IEEE Trans. 
Circuit Theory, 1971, vol. CT-18, no. 5, p. 507 – 519. 
[3] WILLIAMS, R. S. Electrically actuated switch. United States 
Patent Application 20080090337, 04/17/2008. 
[4] WILLIAMS, R. S. How we found the missing memristor. IEEE 
Spectrum, 12/01/2008, p. 1-11, www.spectrum.ieee.org/print/7024. 
[5] JOGLEKAR, Y.N., WOLF, S. J. The elusive memristor: properties 
of basic electrical circuits. arXiv:0807.3994 v2 [cond-mat.mes-
hall] 13 January 2009, p.1-24. 
[6] WANG, F.Y. Memristor for introductory physics. 
arXiv:0808.0286 v1 [physics.class-ph], 4 August 2008, p.1-4. 
About Authors... 
Zdeněk BIOLEK received the M.Sc. degree in 1983, and 
the Ph.D. degree in 2001 from the Brno University of 
Technology (BUT), Czech Re public, both in Electrical 
Engineering with a view to thermodynamics. Until 1992 he 
was the principal research wo rker at Czech Semiconductor 
Company TESLA Rožnov. He is currently with the SŠIE Ř 
Rožnov p. R. He has authored  several special electronic 
instruments for manufacturi ng and testing integrated 
circuits. He is also the author  and co-author of papers from 
the area of the utilization of vari ational principles in circuit 
theory and the stability testing of resistive circuits. 
Dalibor BIOLEK received the M.Sc. degree in Electrical 
Engineering from the BUT, in 1983, and the Ph.D. degree 
in Electronics from the Milita ry Academy Brno, in 1989. 
He is with the Dept. of EE, University of Defense Brno 
(UDB), and with the Dept. of Microelectronics, BUT, as 
professor in Theoretical Elect rical Engineering. His scien-
tific activity is directed to the areas of general circuit 
theory, frequency filters, and computer simulation of elec-
tronic systems. For years, he has been engaged in algo-
rithms of the symbolic and num erical computer analysis of 
electronic circuits with a view to the linear continuous-time 
and switched filters. He has published over 250 papers and 
a book on circuit analysis and simulation. At present, he is 
member of the CAS/COM C zech National Group of IEEE, 
and the president of Commission C of the URSI National 
Committee for the Czech Republic. 
Viera BIOLKOVÁ received her M.Sc. degree in EE from 
the BUT in 1983. Since 1985 she has been with the Dept. 
of Radio Electronics, BUT. He r research interests include 
signal theory, analog signal processing, digital electronics.
