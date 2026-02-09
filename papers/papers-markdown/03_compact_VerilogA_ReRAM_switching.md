# 03_compact_VerilogA_ReRAM_switching.pdf

1 
  
Abstract— The translation of emerging application concepts 
that exploit Resistive Random Access Memory (ReRAM) into  
large-scale practical systems requires realistic, yet 
computationally efficient, empirical models that can capture all  
observed physical devices. Here, we present a Verilog-A ReRAM 
model built upon experimental routines performed on TiOx-based 
prototypes. This model was based on custom biasing protocols, 
specifically designed to reveal device switching rate dependencies 
on a) bias voltage and b) initial resistive state. Our model is based 
on the assumption that a stationary switching rate surface m(R,v) 
exists for sufficiently low voltage stimulation. The proposed model 
comes in compact  form as it is expressed by a simple voltage 
dependent exponential fu nction multiplied with a voltage and 
initial resistive state dependent second order polynomial 
expression, which makes  it suitable for fast and/or large -scale 
simulations. 
 
Index Terms — memristor, modelling, ReRAM, simulation, 
testing, Verilog-A 
I. INTRODUCTION 
INCE 2008 when the basic resistive switching property of a 
double-layer nano -scale film based on Titanium dioxide 
was studied [1] and linked to Chua’s theory of the ‘memristor’  
[2], understanding of practical memristor realisations has 
moved far beyond the simple ‘moving barrier’ model. 
Solid-state memristor devices stem from different 
technological roots (phase -change memory, spin -torque 
transfer, metal-oxide etc. [3], [4], [5] ) and employ a variety of 
electrode/active layer materials and geometries . Such devices 
are becoming more and more accessible to researches,  and it is 
now clear that each  implementation feature s properties that 
render them suitable for different applications. There are 
memristors that have been reported to switch quickly and in a 
probabilistic fashion [6], while others can have their resistive 
state (RS) shifted in small steps (analogue mode) [7] which is 
ideal for synaptic learning [8]. 
Resistive Random Access Memory (ReRAM) devices have 
perhaps received the largest attention as they support 
multi-state programming, can be programmed swiftly and with 
This work was supported in part by the EU COST Action IC1401  
“MEMOCIS” and the Engineering and Physical Sciences Research Council 
under Grant EP/K017829/1. 
The data from this paper can be obtained from University of Southampton 
e-Prints Repository   DOI:10.5258/SOTON/403321. 
Ioannis Messaris and  Spyridon Nikolaidis are with the Department of 
Physics, Aristotle University of Thessaloniki, 54124 Thessaloniki Greece 
(email: imessa@physics.auth.gr). 
Alexander Serb , Ali Khiat  and Themis Prodromakis are with  the Nano 
Group, ECS, University of Southampton, H ighfield, Southampton SO17 1BJ. 
(email: A.Serb@soton.ac.uk.) 
low energy and can be compatible with post-CMOS processing. 
As Re RAM technology matures , a need develops for: a) 
automated testing routi nes intended to accelerate the process 
development cycle [7], [9] and b) robust com puter models 
enabling informed memristor -based system design before 
committing to silicon. To date, s everal empirical and 
semi-empirical models have been published accounting for 
either only non -volatile [10], [11] or both volatile and 
non-volatile behaviours [12] , [13]. The majority of the 
published compact  memristor models are SPICE models and 
although helpful guidelines for accurate and reliable modelling 
of memristors in the SPICE environment have been published 
[14], the fact remains that such models lack industrial 
multi-simulator compatibility. On the other hand, Verilog -A is 
a behavioural language promoted by t he Compact Model 
Council and thus has emerged as the de facto standard language 
for defining and distributing compact models for both academic 
and industrial research groups, mainly due to its flexibility to 
run in numerous industrial electrical simulators  (Spectre, 
A Compact Verilog-A ReRAM Switching Model 
Ioannis Messaris Student Member, IEEE, Alexander Serb Member, IEEE, Ali Khiat, Spyridon 
Nikolaidis Senior Member, IEEE, Themistoklis Prodromakis Senior Member IEEE 
S 
 
Fig. 1. (a) Example switching rate surface ( 𝑚𝑚(𝑅𝑅, 𝑣𝑣) - gray surface ) 
characteristics as reproduced by the proposed model (8). Green lines 
correspond to 𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑 vs 𝑅𝑅 plots for constant bias stimulation ( 𝑉𝑉𝑏𝑏) 
(𝑚𝑚(𝑅𝑅, ±𝑉𝑉𝑏𝑏𝑏𝑏)) while red line captures 𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑 dependence on bias voltage ( 𝑣𝑣) 
when switching from the same initial RS ( 𝑅𝑅0 ) ( 𝑚𝑚(𝑅𝑅0, 𝑣𝑣)). Purple lines 
delineate the ‘absolute voltage threshold’ function and are projected on the 𝑅𝑅−
𝑣𝑣 plane to mark the interface between finite non -zero (white) and zero (gray) 
switching regions. Points N and P pinpoint the absolute voltage threshold 
points exhibited when the device is at  𝑅𝑅=  𝑅𝑅0 for both voltage  polarities. 
Conversely, the purple lines can also be interpreted as the ‘max/min resistive 
state for which a fixed bias voltage is effective. For example, points k1 and k2 
mark the max. RS for which stimulation at 𝑉𝑉=  𝑉𝑉𝑏𝑏1is effective, similar for 
mix. RS and 𝑉𝑉=  −𝑉𝑉𝑏𝑏2.      
 

 2 
HSPICE, ADS, Eldo etc.).  
In this work, we employ two testing biasing routines 
specifically designed for characterising TiO 2-based ReRAM 
prototypes in an operationally relevant environment and use the 
resulting measured data sets in order to model the technology. 
Data from these routines is aggregated to create a data- driven 
ReRAM model  that captures the switching rate ( 𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑) 
dependency on both RS and bias conditions ( 𝑅𝑅, 𝑣𝑣), i.e. 
reconstructs the 𝛥𝛥𝑅𝑅(𝑅𝑅, 𝑣𝑣) surface (assumed to be stationary for 
sufficiently low voltage biasing) (Fig. 1). The resulting model 
combines a simple voltage controlled exponential  expression 
𝑠𝑠(𝑣𝑣) with a second order voltage and RS dependent polynomial 
expression 𝑓𝑓(𝑅𝑅, 𝑣𝑣) thus is suitable for integr ation in circuit 
simulators.  
Section II describes model functionality, operating principles 
and explains the experimental algorithms performed on the 
Device Under Test (DUT). Section III specifies the processing 
of the extracted measurements to the end of producing 
meaningful data. This data is then exploited for the extraction 
of the proper parameter values that fit the proposed model to the 
DUT. Section IV : a) approximates the extracted model with 
continuous and differential expressions  and b) reveals crucial 
coding details adopted in the proposed Verilog -A 
implementation. Finally, section VI concludes the paper.  
II. MODEL AND METHODS 
This section focuses on revealing the operating principles of 
the proposed model . These result from targeted experimental 
testing which is also described. We demonstrate the modeled 
RS switching rate expression which is based on the following 
concepts and assumptions:  a) switching sensitivity is a 
stationary function of initial RS and bias voltage 𝛥𝛥𝑅𝑅(𝑅𝑅, 𝑣𝑣), b) 
the switching rate surface ( 𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑= 𝑚𝑚(𝑅𝑅, 𝑣𝑣) ) can be 
approximated by a product of the form: 𝑠𝑠(𝑣𝑣) ×  𝑓𝑓(𝑅𝑅, 𝑣𝑣), where 
the terms correspond to  the functional forms of the ‘switching 
sensitivity’ function 𝑠𝑠(𝑣𝑣) and the ‘window function’  𝑓𝑓(𝑅𝑅, 𝑣𝑣) 
and c) finite and zero switching resistive regions are separated 
by the presence of an absolute threshold curve that traverses the 
𝑅𝑅− 𝑣𝑣 plane. This is defined by the ‘absolute voltage threshold’ 
function 𝑟𝑟(𝑣𝑣) that is nested in 𝑓𝑓 and essentially regulates its 
windowing behavior. 
The stated assumptions are validated in section III where 
functions  𝑠𝑠, 𝑓𝑓 and 𝑟𝑟 are derived from measurements of 
switching ( 𝛥𝛥𝑅𝑅) recorded using  the described biasing schemes 
on an in-house 𝑇𝑇𝑇𝑇𝑂𝑂𝑥𝑥-based sample. 
Importantly, throughout this work,  device RS is formally 
defined as static resistance at a standardized read -out voltage. 
Regardless of the voltage used to bias the device for the 
purposes of switching, all assessments of RS are carried out at 
the standard voltage ( 0.2𝑉𝑉). Thus the model i s designed to 
describe changes in RS as measured by a standardized way in 
response to input stimulation. 
A. The switching rate model expressions 
Experimentally, device RS is defined as:  
 
𝑅𝑅= 𝑉𝑉/𝐼𝐼 at 𝑉𝑉= 𝑉𝑉𝑟𝑟𝑟𝑟𝑟𝑟𝑟𝑟,                                                                  (1) 
 
where 𝑉𝑉= 𝑉𝑉𝑟𝑟𝑟𝑟𝑟𝑟𝑟𝑟 is the read voltage applied and 𝐼𝐼 is the current 
flowing through device terminals during read-out. 
We present an empirical, RS and voltage controlled 
switching rate memristor model ( 𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑) that describes 
changes in RS as a result of stimulation given at a well-defined 
RS 𝑅𝑅0 and with a fixed voltage 𝑣𝑣:  
 
𝑟𝑟𝑑𝑑
𝑟𝑟𝑑𝑑= 𝑚𝑚(𝑅𝑅, 𝑣𝑣) = 𝑠𝑠(𝑣𝑣)𝑓𝑓� 𝑅𝑅, 𝑟𝑟(𝑣𝑣)� ,                                          (2) 
 
where, 𝑚𝑚(𝑅𝑅, 𝑣𝑣) manifests the three dimensional surface that 
tracks device switching rate as a function of initial RS (𝑅𝑅0) and 
bias voltage application ( 𝑣𝑣) (Fig. 1). Function  𝑠𝑠(𝑣𝑣) 
corresponds to the ‘switching sensitivity’ and is solely voltage 
controlled expressed in units 𝑠𝑠
−1𝛺𝛺−1 . Function 𝑓𝑓(𝑅𝑅, 𝑣𝑣), the 
device Window Function (WF) , is both RS and voltage 
dependent measured in units 𝛺𝛺2  with its specific voltage 
dependency regulated by the nested ‘absolute voltage 
threshold’ function 𝑟𝑟(𝑣𝑣). What is interesting with 𝑟𝑟 is that it is 
measured in 𝛺𝛺 and thus is found on the 𝑅𝑅− 𝑣𝑣 plane. Its 
physical interpretation is of particular importance as it models 
the device ab solute threshold curve (plotted on the 𝑅𝑅− 𝑣𝑣 
plane) that separates finite from zer o switching rate regions 
(Fig. 1). Importantly, a ll functions in (2) have a piecewise 
nature where for each one, positive and negative stimulation 
branches have the same functional forms but with different 
parameter values. 
B. Experimental testing 
Fig. 1 displays a sample switching rate surface that 
resembles the form of the experimentally measured data 
according to which 𝑚𝑚(𝑅𝑅, 𝑣𝑣) is modeled in Section III (Fig. 7). 
In order to reconstruct m  from measured results the DUT is 
subjected to two distinct experimental protocols:  
 
1) The ‘biasing optimizer’ 
Pulsed voltage ramps of alternating polarities are employed 
and the DUT reacts by oscillating its RS around an initial 
value 𝑅𝑅0  revealing the relation between 𝛥𝛥𝑅𝑅 and bias 
voltage around 𝑅𝑅0 𝑠𝑠(𝑣𝑣)|𝑑𝑑=𝑑𝑑0 ∝ 𝛥𝛥𝑅𝑅(𝑅𝑅0, 𝑣𝑣) (the ‘switching 
sensitivity’ function). Each ramp level is a pulse train that 
consists of 𝑁𝑁 𝑝𝑝𝑝𝑝𝑝𝑝𝑠𝑠𝑝𝑝𝑠𝑠/𝑑𝑑𝑟𝑟𝑡𝑡𝑇𝑇𝑡𝑡 with fixed duration 𝑑𝑑𝑤𝑤. The 
observed, bipolar DUT behaviour exhibiting SET 
transitions under positive voltage bias and RESET under 
negative is exploited by the algorithm in order to restrict 
DUT RS within a narrow resistive range. Pulse train 
polarity is changed each time DUT RS exits a user defined 
tolerance band 𝜀𝜀
𝑜𝑜𝑜𝑜𝑑𝑑 (in % of 𝑅𝑅0) around 𝑅𝑅0. The result is an 
estimate of the switchin g rate function around 𝑅𝑅0 
( 𝑚𝑚(𝑅𝑅0, 𝑣𝑣) ). For both routines, 𝛥𝛥𝑅𝑅 measurements are 
converted into a switching rate ( 𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑) by dividing 𝛥𝛥𝑅𝑅 
with the duration of the stimulus [7].  
 
2) The ‘operating RS sweeper’ 
This algorithm applies a  train consisting of 𝑆𝑆 identical 
pulses of fixed pulse duration 𝑑𝑑𝑤𝑤. The DUT reacts by 
changing its RS and the relation between switching 𝛥𝛥𝑅𝑅 and 

 3 
running 𝑅𝑅 is revealed at the chosen bias voltage 
𝑓𝑓(𝑅𝑅)|𝑣𝑣=𝑉𝑉𝑏𝑏∝ 𝛥𝛥𝑅𝑅(𝑅𝑅, 𝑉𝑉𝑏𝑏) (device WF). This is performed for 
multiple voltage levels 𝑉𝑉𝑏𝑏. In its fl ow, the algorithm is 
carried out by changing polarity with each applied train and 
increasing the amplitude every two trains by a defined step 
voltage 𝑉𝑉𝑠𝑠𝑑𝑑𝑟𝑟𝑜𝑜. The absolute amplitude of the pulses applied 
will scale according to 𝑉𝑉𝑠𝑠𝑑𝑑𝑟𝑟𝑜𝑜 from an initia l voltage 𝑉𝑉𝑠𝑠𝑑𝑑𝑟𝑟𝑟𝑟𝑑𝑑, 
up to a user defined value 𝑉𝑉𝑠𝑠𝑑𝑑𝑜𝑜𝑜𝑜 and the algorithm will 
terminate after pulse trains featuring this value in both 
polarities are applied. 
 
These experimental routines are designed to isolate the 𝑅𝑅 
and 𝑣𝑣 dependencies by slicing the 𝑚𝑚(𝑅𝑅, 𝑣𝑣) surface parallel to 
the RS ( 𝑅𝑅) (sweeper) and voltage ( 𝑣𝑣) (optimizer) axes 
respectively. In Fig. 1, r ed line corresponds to the 𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑− 𝑣𝑣 
plot for fixed initial 𝑅𝑅0 (𝑚𝑚(𝑅𝑅0, 𝑣𝑣)) while green lines capture 
𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑− 𝑅𝑅 dependency for  constant bias voltage  ±𝑉𝑉𝑏𝑏1,2 
(𝑚𝑚� 𝑅𝑅, ±𝑉𝑉𝑏𝑏1,2� ). Both testing routines where implemented on a 
general purpose R eRAM characterisation instrument 
previously described in [15] , [16] in order to characterise a 
𝑇𝑇𝑇𝑇𝑂𝑂𝑥𝑥 sample, cell of a stand -alone R eRAM device array, 
described in [5].  The specific experimental routines employed 
on the modeled DUT are shown in Fig. 5: (a) corresponds to the 
‘optimizer’ routine while (b) to the ‘sweeper’. The parameter 
values of the testing schemes designed to characterize the DUT 
along with the data processing  of the exported data towards 
gaining meaningful resistive switching information are 
described in section III. 
C. Switching rate surface properties 
Fig. 2(a) plots a family of sample switching rate functions 
𝑚𝑚(𝑅𝑅, 𝑉𝑉𝑏𝑏) for various bias voltages 𝑉𝑉𝑏𝑏 of both polarities, where 
device RS is swept in its resistive region of operation. The 
forms of  the illustrated curves follow the forms of the plots 
fitted to the corresponding experimental data ( Fig. 3 (a-c)) 
measured from the DUT. We notice bipolar switching, where 
higher absolute voltage amplitudes provoke higher switching 
rates and switching intensifies as we move away from the 
resistive range boundaries 𝑅𝑅𝑚𝑚𝑏𝑏𝑚𝑚 and 𝑅𝑅𝑚𝑚𝑟𝑟𝑥𝑥 for constant voltage 
stimulation. We also see that switching bey ond these 
boundaries is set to zero  (for the corresponding bias voltage 
amplitude) i.e. the plots in Fig. 2(a) embody device WF 
characteristics. Furthermore, the positions  of these resistive 
limits are monotonically dependent on voltage. Higher negative 
voltages push 𝑅𝑅𝑚𝑚𝑏𝑏𝑚𝑚 to lower resistive values while more 
invasive positive biases push 𝑅𝑅𝑚𝑚𝑟𝑟𝑥𝑥 to higher RSs. The physical 
interpretation of the se boundaries is that for any RS below 
𝑅𝑅𝑚𝑚𝑟𝑟𝑥𝑥 (active region) at a given positive voltage, applying this 
voltage can push the device to 𝑅𝑅𝑚𝑚𝑟𝑟𝑥𝑥, but no further (saturation). 
If the device is already above  𝑅𝑅𝑚𝑚𝑟𝑟𝑥𝑥, no switching occurs (for 
positive stimulation). The same applies for negative biasing and 
the 𝑅𝑅𝑚𝑚𝑏𝑏𝑚𝑚 limit. 
Fig. 2(b) illustrates the corresponding to Fig. 2(a), family of 
switching rate plots 𝑚𝑚(𝑅𝑅0, 𝑣𝑣) starting from different initial RSs 
(𝑅𝑅0) and sweeping the applied voltage (𝑣𝑣) for each case. Again, 
the curve  forms shown in this figure resemble the 
corresponding experimental data demonstrated in Fig. 4(d). 
Stronger voltage biases cause  higher switching rate s, as does  
moving away from the resistive range boundaries of operation, 
i.e. towards lower RS values for 𝑣𝑣> 0 and higher RS values 
for 𝑣𝑣< 0. This is consistent with the 𝑚𝑚(𝑅𝑅, 𝑉𝑉𝑏𝑏) plots of Fig. 
2(a). 
What is particularly notable in the presented characteristic 
plots is that Fig. 2(a) exhibits resistive thresholds while Fig. 
2(b) shows voltage thresholds. In Fig. 1 the two purple lines    
(for the positive and negative stimulation cases) delineate the 
zero switching surface 𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑= 𝑧𝑧(𝑅𝑅, 𝑣𝑣) = 0 (projected on the 
base of Fig. 1  as the grey area), where 𝑧𝑧 defines a bijective 
function between 𝑅𝑅 and 𝑣𝑣 (which as mentioned are 
monotonically linked) for which voltage and resistive 
thresholds are given by  𝑉𝑉𝑑𝑑𝑜𝑜𝑚𝑚=  𝑟𝑟−1(𝑅𝑅)  and 𝑅𝑅𝑚𝑚𝑏𝑏𝑚𝑚/𝑚𝑚𝑟𝑟𝑥𝑥=
𝑉𝑉−1(𝑣𝑣) respectively. These boundaries are modeled in (2) by 
the ‘absolute voltage threshold’ function 𝑟𝑟(𝑣𝑣), where  𝑟𝑟𝑜𝑜(𝑣𝑣) 
and 𝑟𝑟𝑚𝑚(𝑣𝑣) correspond to the positive and negative branches 
respectively. The switching rate plots 𝑚𝑚(𝑅𝑅, 𝑉𝑉𝑏𝑏1)  and 
𝑚𝑚(𝑅𝑅, −𝑉𝑉𝑏𝑏1) (green lines) represent  the plots of Fig. 2(a) and 
cross 𝑟𝑟 at points 𝑘𝑘1(𝑅𝑅𝑚𝑚𝑟𝑟𝑥𝑥,𝑏𝑏, 𝑉𝑉𝑏𝑏1) and  𝑘𝑘2(𝑅𝑅𝑚𝑚𝑏𝑏𝑚𝑚,𝑏𝑏, −𝑉𝑉𝑏𝑏1), thus 
defining the values of  the resistive thresholds ( 𝑅𝑅𝑚𝑚𝑟𝑟𝑥𝑥,𝑏𝑏,𝑅𝑅𝑚𝑚𝑏𝑏𝑚𝑚,𝑏𝑏). 
Similarly, the red  line ( 𝑚𝑚(𝑅𝑅0, 𝑣𝑣) ), which exemplifies  the 
switching rate plot family of Fig. 2(b), crosses 𝑟𝑟𝑜𝑜 and 𝑟𝑟𝑚𝑚 at 
points 𝑃𝑃� 𝑅𝑅0, 𝑉𝑉𝑑𝑑𝑜𝑜�  and 𝑁𝑁(𝑅𝑅0, 𝑉𝑉𝑑𝑑𝑚𝑚), where 𝑉𝑉𝑑𝑑𝑜𝑜 and 𝑉𝑉𝑑𝑑𝑚𝑚 are the 
positive and negative voltage thresholds that correspond to 
device RS equal to 𝑅𝑅0. According to the bijective property of 𝑧𝑧, 
points 𝑃𝑃 and 𝑁𝑁 serve also as resistive threshold points for the 
RS dependent switching rate plots 𝑚𝑚� 𝑅𝑅, 𝑉𝑉𝑏𝑏2 ≡ 𝑉𝑉𝑑𝑑𝑜𝑜� 
and 𝑚𝑚(𝑅𝑅, −𝑉𝑉𝑏𝑏2 ≡ 𝑉𝑉𝑑𝑑𝑚𝑚)  (the green curves in Fig. 1).  
D. Functional forms 
Next, we define the mathematical forms of the functions 
comprising (2). In order to fit the experimental switching rate 
plots of Fig. 3(a-c) for constant voltage bias 𝑉𝑉𝑏𝑏, we seek for an 
RS dependent expression that matches the demonstrated data 
and is formulated in a way so as to model zero switching at a 
defined resistive threshold value. Accordingly, they can be 
described with an RS dependent second order law of the form,   
 
𝑟𝑟𝑑𝑑
𝑟𝑟𝑑𝑑�
𝑉𝑉𝑏𝑏
= � 𝑠𝑠𝑜𝑜(𝑉𝑉𝑏𝑏)� 𝑟𝑟𝑜𝑜(𝑉𝑉𝑏𝑏) − 𝑅𝑅�
2
𝑠𝑠𝑑𝑑𝑝𝑝� 𝑟𝑟𝑜𝑜(𝑣𝑣) − 𝑅𝑅� , 𝑉𝑉𝑏𝑏> 0, 𝑅𝑅< 𝑟𝑟𝑜𝑜(𝑣𝑣)  
𝑠𝑠𝑚𝑚(𝑉𝑉𝑏𝑏)� 𝑅𝑅− 𝑟𝑟𝑚𝑚(𝑉𝑉𝑏𝑏)�
2
𝑠𝑠𝑑𝑑𝑝𝑝� 𝑅𝑅− 𝑟𝑟𝑚𝑚(𝑉𝑉𝑏𝑏)� , 𝑉𝑉𝑏𝑏≤ 0, 𝑅𝑅≥ 𝑟𝑟𝑚𝑚(𝑣𝑣) 
,         
(4) 
 
Fig. 2. Example switching rate plots for (a) 𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑 vs 𝑅𝑅 for three voltage s 
where |𝑉𝑉𝑏𝑏1| < |𝑉𝑉𝑏𝑏2| < |𝑉𝑉𝑏𝑏3| and (b) 𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑 vs 𝑣𝑣  for various initial RSs for 
which 𝑅𝑅0 < 𝑅𝑅1 < 𝑅𝑅2 < 𝑅𝑅3 < 𝑅𝑅4  Round symbols on the 𝑥𝑥-axis correspond to 
the absolute threshold values which are resistive for (a) and voltages for (b).      


 4 
where 𝑅𝑅 is device RS, 𝑓𝑓(𝑅𝑅, 𝑣𝑣) is the device WF  and 𝑠𝑠𝑜𝑜/𝑚𝑚(𝑉𝑉𝑏𝑏),  
𝑟𝑟𝑜𝑜/𝑚𝑚(𝑉𝑉𝑏𝑏) = 𝑅𝑅𝑚𝑚𝑟𝑟𝑥𝑥/𝑚𝑚𝑏𝑏𝑚𝑚𝑉𝑉𝑏𝑏, are the switching sensitivity and 
resistive boundary values . Subscripts 𝑝𝑝 and 𝑡𝑡 denote the 
positive and negative stimulation cases respectively. The latter 
(𝑟𝑟𝑜𝑜/𝑚𝑚) determine the device resistive range of operation for bias 
voltage 𝑉𝑉𝑏𝑏. Practically the squared  parenthetic term ensures 
zero switching at the resistive threshold point determined 
by 𝑟𝑟(𝑣𝑣), while the step function 𝑠𝑠𝑑𝑑𝑝𝑝(∙) imposes zero switching 
beyond this point.   Fig. 3(a-c) also demonstrates the voltage 
dependent nature of the 𝑅𝑅𝑚𝑚𝑏𝑏𝑚𝑚/𝑚𝑚𝑟𝑟𝑥𝑥 values modeled by the 
‘absolute threshold’ function 𝑟𝑟(𝑣𝑣) and switching activity that 
coincides with the conditionals in (4). The behavior of the 
switching sensitivity function 𝑠𝑠𝑜𝑜/𝑚𝑚 will be examined towards 
the end of this section. 
The expression that fits the zero switching boundary values  
𝑅𝑅𝑚𝑚𝑏𝑏𝑚𝑚/𝑚𝑚𝑟𝑟𝑥𝑥 is a first order expression ( Fig. 3(d)), thus defining 
the form of the 𝑟𝑟(𝑣𝑣) function in (2) as: 
 
𝑟𝑟(𝑣𝑣) = �𝑟𝑟𝑜𝑜(𝑣𝑣) = 𝑡𝑡0 + 𝑡𝑡1𝑣𝑣,   𝑣𝑣> 0
𝑟𝑟𝑚𝑚(𝑣𝑣) = 𝑏𝑏0 + 𝑏𝑏1𝑣𝑣,   𝑣𝑣≤ 0,                                      (5) 
 
where 𝑡𝑡0 , 𝑡𝑡1 , 𝑏𝑏0 , 𝑏𝑏1  are fitting parameters. Higher positive 
biases (𝑣𝑣> 0) push 𝑅𝑅𝑚𝑚𝑟𝑟𝑥𝑥 from its minimum value 𝑡𝑡0 (for 𝑣𝑣=
0) to higher resistive values , while more invasive negative 
biases ( 𝑣𝑣< 0 ) push the highest exhibited 𝑅𝑅𝑚𝑚𝑏𝑏𝑚𝑚 value 𝑏𝑏0 
(for 𝑣𝑣= 0) to lower resistive val ues. Parameters 𝑡𝑡1  and 𝑏𝑏1 
define the rate at  which the boundary resistive values change 
proportionally to the applied voltage. 
Solving the equations in (5), with respect to voltage gives us 
the switching threshold voltages 𝑉𝑉𝑑𝑑𝑜𝑜𝑚𝑚 for which an RS on the 
𝑟𝑟(𝑣𝑣) curve becomes a resistive range boundary: 
 
𝑉𝑉𝑑𝑑(𝑅𝑅) = �𝑉𝑉𝑑𝑑𝑚𝑚(𝑅𝑅) = (𝑅𝑅− 𝑡𝑡0)/𝑡𝑡1,   𝑣𝑣> 0
𝑉𝑉𝑑𝑑𝑜𝑜(𝑅𝑅) = (𝑅𝑅− 𝑏𝑏0)/𝑏𝑏1,   𝑣𝑣< 0,                            (6) 
       
We proceed on defining the form of the ‘switching 
sensitivity’ function 𝑠𝑠(𝑣𝑣)  by investigating DUT switching 
dependency on biasing conditions when stimulated from the 
same initial RS 𝑅𝑅0. As 𝑓𝑓 and 𝑟𝑟 are given in (4), (5) , only 𝑠𝑠 is 
left to be determined for the complete functional form of the 
switching rate function 𝑚𝑚(𝑅𝑅, 𝑣𝑣) to be revealed. Expression (2) 
combined with (4 ), (5)  fits the corresponding experimental 
results shown in Fig. 4(d) when s takes the form of a simple 
exponential function defined as: 
 
𝑠𝑠(𝑣𝑣) =
⎩⎪⎨
⎪⎧𝐴𝐴𝑜𝑜� −1 + 𝑝𝑝
|𝑣𝑣|
𝑡𝑡𝑝𝑝� ,   𝑣𝑣> 0
𝐴𝐴𝑚𝑚�−1 + 𝑝𝑝
|𝑣𝑣|
𝑡𝑡𝑛𝑛� , 𝑣𝑣≤ 0
,                                           (7) 
   
where 𝐴𝐴𝑜𝑜, 𝐴𝐴𝑚𝑚, 𝑑𝑑𝑜𝑜, 𝑑𝑑𝑚𝑚 are fitting parameters. The simple  form of 
(7) renders the device RS to be idle in the absence of voltage 
stimulation (𝑠𝑠(0) = 0 => 𝑚𝑚(𝑅𝑅, 𝑣𝑣) = 0) and therefore ensures 
non-volatile behavior for the model.  
The final model expression results from combining (2),  (4), 
(5) and (7). The proposed RS and voltage dependent switching 
rate function 𝑚𝑚(𝑅𝑅, 𝑣𝑣) governing the device is expressed as: 
 
𝑟𝑟𝑑𝑑
𝑟𝑟𝑑𝑑= 𝑚𝑚(𝑅𝑅, 𝑣𝑣) =  
𝐴𝐴𝑜𝑜� −1 + 𝑝𝑝
|𝑣𝑣|
𝑑𝑑𝑝𝑝� � 𝑟𝑟𝑜𝑜(𝑣𝑣) − 𝑅𝑅�
2
𝑠𝑠𝑑𝑑𝑝𝑝� 𝑟𝑟𝑜𝑜(𝑣𝑣) − 𝑅𝑅�  𝑠𝑠𝑑𝑑𝑝𝑝(𝑣𝑣) + 
𝐴𝐴𝑚𝑚� −1 + 𝑝𝑝
|𝑣𝑣|
𝑡𝑡𝑛𝑛� � 𝑅𝑅− 𝑟𝑟𝑚𝑚(𝑣𝑣)�
2
𝑠𝑠𝑑𝑑𝑝𝑝� 𝑅𝑅− 𝑟𝑟𝑚𝑚(𝑣𝑣)�  𝑠𝑠𝑑𝑑𝑝𝑝(−𝑣𝑣),                (8) 
 
where 𝑟𝑟𝑜𝑜, 𝑟𝑟𝑚𝑚 are those defined in (5), and 𝐴𝐴𝑜𝑜, 𝐴𝐴𝑚𝑚, 𝑑𝑑𝑜𝑜, 𝑑𝑑𝑚𝑚, 𝑡𝑡0, 𝑡𝑡1, 
𝑏𝑏0, 𝑏𝑏1 are fitting parameters.  
III. RESULTS 
We proceed by specifying  the parameters for the 
experimental testing and using the resulting switching data 
(𝛥𝛥𝑅𝑅) to extract the model parameter values that fit ( 8) to the 
DUT, i.e. our modelling target.  
A. ‘Optimizer’ parameters and data refinement 
The optimizer routine run employed on the DUT is shown in 
Fig. 5(a). The routine parameter values are, 𝑁𝑁= 10 𝑝𝑝𝑝𝑝𝑝𝑝𝑠𝑠𝑝𝑝𝑠𝑠/
𝑑𝑑𝑟𝑟𝑡𝑡𝑇𝑇𝑡𝑡, 𝑑𝑑𝑤𝑤= 100𝜇𝜇𝑠𝑠/𝑝𝑝𝑝𝑝𝑝𝑝𝑠𝑠𝑝𝑝 and 𝜀𝜀𝑜𝑜𝑜𝑜𝑑𝑑= 10% . The result is an 
estimate of the switching rate function around 𝑅𝑅0 = 13.65𝐾𝐾𝛺𝛺 
(𝑚𝑚(𝑅𝑅0, 𝑣𝑣)) (Fig. 5(a)). 
 
Fig. 3.  (a-c) Red and blue symbols correspond to experimental 𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑 vs 𝑅𝑅 points after suitable processing of the data exported by the sweeper testing routine. Red 
and blue lines are reproduced by the 2 nd order expression (4). Fille d dots indicate the resistive boundaries of operation beyond which switching is nullified 
(𝑅𝑅𝑚𝑚𝑏𝑏𝑚𝑚/𝑚𝑚𝑟𝑟𝑥𝑥). Three absolute voltage levels are investigated, 0.6V, 0.7V and 0.8V. The positive stimulation case for 0.6V is omitted as the obtained data for this 
voltage level was too noisy to provide meaningful information. (d) Linear fitting of the resistive boundary values revealed after fitting (4) to the switching rate data 
shown in (a-c). Left panel: Red symbols are the calculated 𝑅𝑅𝑚𝑚𝑏𝑏𝑚𝑚 points while red line is reproduced by 𝑟𝑟𝑚𝑚(𝑣𝑣) (5). Right panel: Blue symbols correspond to the 
𝑅𝑅𝑚𝑚𝑟𝑟𝑥𝑥 points while blue line is exhibited by 𝑟𝑟𝑜𝑜(𝑣𝑣) (5).   


 5 
Naturally, the optimiser process causes excursions of DUT 
RS away from 𝑅𝑅0, so the estimate of 𝑚𝑚(𝑅𝑅0, 𝑣𝑣) is imperfect. To 
mitigate this effect, data extracted via the ‘optimizer’ could be 
filtered so that 𝑚𝑚(𝑅𝑅0, 𝑣𝑣) is estimated using only data for 𝑅𝑅∈
[𝑅𝑅0 − 𝜀𝜀𝑟𝑟𝑟𝑟𝑟𝑟, 𝑅𝑅0 + 𝜀𝜀𝑟𝑟𝑟𝑟𝑟𝑟] for some chosen 𝜀𝜀𝑟𝑟𝑟𝑟𝑟𝑟 (expressed as % 
of 𝑅𝑅0). This data refinement process helps define an RR range 
that is both narrow enough to be ‘sufficiently close’ to its centre 
RS and yet  at the same time adequately populated with 
measurements to offer useful information. 
However, in practice most of the data 𝛥𝛥𝑅𝑅(𝑅𝑅, 𝑣𝑣) is not always 
clustered around the optimiser’s operating 𝑅𝑅0. Therefore, it is 
more useful to determine the value of 𝑅𝑅0 a posteriori, i.e. after 
the completion of the optimiser run. The 𝑅𝑅0 around which most 
gathered data is clustered can be defined as the central value of 
𝑅𝑅𝑥𝑥 for which the interval [𝑅𝑅𝑥𝑥− 𝜀𝜀𝑟𝑟𝑟𝑟𝑟𝑟, 𝑅𝑅𝑥𝑥+ 𝜀𝜀𝑟𝑟𝑟𝑟𝑟𝑟] contains the  
maximum number of data points . We then consider that the 
results of the optimiser trace a line in the 𝑅𝑅− 𝑉𝑉 plane at 
𝛥𝛥𝑅𝑅(𝑅𝑅𝑥𝑥, 𝑣𝑣) instead of 𝛥𝛥𝑅𝑅(𝑅𝑅0, 𝑣𝑣) as a fairer approximation . Fig. 
4(b, c) illustrates the refinement process as applied on positive 
and negative stimulation data for 𝜀𝜀𝑟𝑟𝑟𝑟𝑟𝑟= 5%. For (b), the most 
populated interval has its centre at 12.60𝐾𝐾𝛺𝛺 while for (c), the 
most populated interval has its centre at 14.90𝐾𝐾𝛺𝛺, even though 
according to the optimiser the central value of 𝑅𝑅0 should be 
13.65𝐾𝐾𝛺𝛺 (Fig. 5(a)). The resulting refined ‘switching’ plot is 
shown in Fig. 4(d). Finally, amount of switching data (𝛥𝛥𝑅𝑅) is 
converted into switching rate data ( 𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑): 𝛥𝛥𝑅𝑅/(𝑁𝑁× 𝑑𝑑𝑤𝑤) =
𝛥𝛥𝑅𝑅/1𝑚𝑚𝑠𝑠. 
B. ‘Sweeper’ parameters and data processing 
Fig. 5(b) shows the sweeper test run results on the same 
DUT. Parameter values are 𝑆𝑆= 500 𝑝𝑝𝑝𝑝𝑝𝑝𝑠𝑠𝑝𝑝𝑠𝑠/𝑑𝑑𝑟𝑟𝑡𝑡𝑇𝑇𝑡𝑡, 𝑑𝑑𝑤𝑤=
100𝜇𝜇𝑠𝑠/𝑝𝑝𝑝𝑝𝑝𝑝𝑠𝑠𝑝𝑝, 𝑉𝑉𝑠𝑠𝑑𝑑𝑟𝑟𝑜𝑜= 0.1𝑉𝑉, 𝑉𝑉𝑠𝑠𝑑𝑑𝑟𝑟𝑟𝑟𝑑𝑑= 0.6𝑉𝑉 and 𝑉𝑉𝑠𝑠𝑑𝑑𝑜𝑜𝑜𝑜= 0.8𝑉𝑉.  
The resulting information linking RS switching to 
stimulation voltage seen in Fig. 5(b) is processed by converting 
𝑅𝑅𝑆𝑆(𝑝𝑝𝑝𝑝𝑝𝑝𝑠𝑠𝑝𝑝) into 𝑅𝑅𝑆𝑆(𝑑𝑑) by taking into acc ount the amplitude 
(𝑉𝑉𝑏𝑏) and duration ( 𝑑𝑑𝑤𝑤) of the voltage pulses. Subsequently, a 
smoothing time derivative of the RS measurements is 
employed and the switching rate, 𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑 versus RS, 𝑅𝑅 for 
constant voltage application, 𝑉𝑉𝑏𝑏 is captured in Fig. 3(a-c). 
Besides DUT RS sensitivity , Fig. 3(a-c) also shows the 
dependency of 𝑅𝑅𝑚𝑚𝑏𝑏𝑚𝑚/𝑚𝑚𝑟𝑟𝑥𝑥 on voltage stimulation. 
It is important to note that timing between successive reads 
and successive writes is not under user control in the current 
‘optimizer’ and ‘sweeper’ implementations. Instead, pulses are 
sent as soon as the system is ready to source them (syst em 
automatically determines how long to measure in order to 
obtain a reliable measurement). Timing choices for these 
actions may affect DUT behavio ur and results (e.g. timing  
between writes may affect DUT behavio ur through possible 
thermal effects [13]  and timing between reads will affect 
algorithm results in samples exhibiting noticeable RS volatility 
[17]). These effects are subjects of further, ongoing work. 
C. Model parameter extraction for the DUT 
In this sub-section we fit the proposed model expression ( 8) 
to the corresponding data conceived by the presented device 
testing schemes. 
1) Window function 𝑓𝑓 
The switching rate plots of Fig. 3(a-c) are fitted quite well 
with the suitable second order expression (4) where 𝑠𝑠𝑚𝑚/𝑜𝑜(𝑉𝑉𝑏𝑏) 
and 𝑟𝑟𝑜𝑜/𝑚𝑚(𝑉𝑉𝑏𝑏) = 𝑅𝑅𝑚𝑚𝑟𝑟𝑥𝑥/𝑚𝑚𝑏𝑏𝑚𝑚 reduce to constant values when 𝑉𝑉𝑏𝑏 is 
fixed.  
Fig. 3(d) plots the 𝑅𝑅𝑚𝑚𝑏𝑏𝑚𝑚/𝑚𝑚𝑟𝑟𝑥𝑥 points that result after fitting the 
switching rate data of Fig. 3(a-c). The linear expressions in (5) 
are used to express the resistive boundary point trends thus 
defining the relevant parameter values for the specific DUT as:  
 
𝑡𝑡0 = 17.16𝐾𝐾𝛺𝛺, 𝑡𝑡1 = 0.15𝐾𝐾𝛺𝛺/𝑣𝑣, 𝑏𝑏0 = 24.81𝐾𝐾𝛺𝛺, 𝑏𝑏1 =
17.91𝐾𝐾𝛺𝛺/𝑣𝑣                          (9) 
 
We notice that the DUT exhibits rather stable 𝑅𝑅
𝑚𝑚𝑟𝑟𝑥𝑥 points in 
contrast to 𝑅𝑅𝑚𝑚𝑏𝑏𝑚𝑚 which, depending on the voltage applied, span 
to the entire DUT range of operation ( 10𝐾𝐾𝛺𝛺− 17𝐾𝐾𝛺𝛺, Fig. 
3(d)).  
2) Switching sensitivity function 𝑠𝑠 
We use (8) for 𝑣𝑣> 0 to fit the positive branch of the refined 
switching rate data ( Fig. 4(d)) for 𝑅𝑅= 𝑅𝑅𝑆𝑆0𝑜𝑜= 12.60𝐾𝐾𝛺𝛺 and 
the corresponding parameter values in ( 9) ( 𝑡𝑡0 , 𝑡𝑡1 ). 
 
Fig. 4. (a) Change in RS recorded after application of each train of programming pulses as a function of pulse voltage ( 𝛥𝛥𝑅𝑅(𝑣𝑣)). (b) and (c ): Application of the 
refinement algorithm on ‘optimizer’ measurement s that correspond to positive (b) and negative (c ) pulse stimulation. Grey shadings highlight the most 
data-populated resistive bands along with the band’s resistive limits and the corresponding tolerance 𝜀𝜀𝑟𝑟𝑟𝑟𝑟𝑟 according to which they are defined. (d ) Left y-axis: 
Symbols correspond to change in RS (𝛥𝛥𝑅𝑅) recorded after refining measurements, vs bias voltage 𝑉𝑉𝑏𝑏. Red line is repr oduced by the proposed model (8 ). The 
reference RS for positive (𝑅𝑅𝑆𝑆0𝑜𝑜= 12.60𝐾𝐾𝛺𝛺) and negative (𝑅𝑅𝑆𝑆0𝑚𝑚= 14.90𝐾𝐾𝛺𝛺) stimulation is also shown. Right y-axis: RS switching rate versus bias voltage 𝑉𝑉𝑏𝑏. 
Green symbols are switching rate points calculated by (4), for the fitted 𝑘𝑘𝑚𝑚(𝑉𝑉𝑏𝑏), 𝑘𝑘𝑜𝑜(𝑉𝑉𝑏𝑏), 𝑟𝑟𝑚𝑚(𝑉𝑉𝑏𝑏), 𝑟𝑟𝑜𝑜(𝑉𝑉𝑏𝑏) for the sweeper voltages 𝑉𝑉𝑏𝑏= {−0.6𝑉𝑉, ±0.7𝑉𝑉, ±0.8𝑉𝑉} 
(0.6𝑉𝑉 case is neglected). As (4) results solely from sweeper data, the allocation of these points corroborate device stability hypothesis.       


 6 
Analogously, we fit the negative branch for 𝑅𝑅= 𝑅𝑅𝑆𝑆0𝑚𝑚=
14.90𝐾𝐾𝛺𝛺 and the 𝑏𝑏0 , 𝑏𝑏1  parameter values in ( 9). The two 
discreet fittings reveal the values of the remaining parameters 
𝐴𝐴𝑜𝑜, 𝐴𝐴𝑚𝑚, 𝑑𝑑𝑜𝑜 and 𝑑𝑑𝑚𝑚: 
    
𝐴𝐴𝑜𝑜= −4.86 × 10−5𝛺𝛺−1𝑠𝑠−1 , 𝑑𝑑𝑜𝑜= 0.12𝑉𝑉, 𝐴𝐴𝑚𝑚= 1.09 ×
10−3𝛺𝛺−1𝑠𝑠−1, 𝑑𝑑𝑚𝑚= 0.18𝑉𝑉           (10) 
 
3) Combining f and s. 
Experimentally we find that 𝑓𝑓 and 𝑠𝑠 are mutually consistent: 
Fig. 4(d), plots experimental 𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑 points versus 𝑣𝑣 (f) for the 
same initial, 𝑅𝑅0 . Green 𝑥𝑥-points show corresponding 𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑 
values resulting from (4) (Fig. 3(a-c)) along with the parameter 
values ( 9) for 𝑅𝑅= 𝑅𝑅𝑆𝑆0𝑜𝑜= 12.60𝐾𝐾𝛺𝛺 and 𝑅𝑅= 𝑅𝑅𝑆𝑆0𝑚𝑚=
14.90𝐾𝐾𝛺𝛺. We notice that the resulting points are consistent 
with the refined switching rate measurements therefore 
supporting the  device response stability  hypothesis. Fig. 6 
displays simulated switching rate plot families that correlate to 
the modeled DUT for a) constant biasing conditions (𝑚𝑚(𝑅𝑅, 𝑉𝑉𝑏𝑏)) 
and b) steady initial RS ( 𝑚𝑚(𝑅𝑅0, 𝑣𝑣)), in the resistive range and 
for the bias voltages the physical DUT was tested. 
Fig. 7 reveals the switching rate surface reproduced by the 
proposed model expressions ( 8) and the parameter values ( 9), 
(10) along with the switching rate measurements that resulted 
by the application of the optimizer routine on the DUT. The 
particularly good matching of the proposed expression ( 8) 
versus experimental results corroborates  the assumptions upon 
which our model was structured. 
IV. MODEL INTEGRATION IN CIRCUIT SIMULATOR 
A continuous and differentiable mathematical description is 
a mandatory requirement for any model implementation to 
work properly with the iterative solution methods used by 
computer solvers. Furthermore, for model integration into a 
circuit simulator with the use of the Verilog -A (VA) language, 
the choice of the appropriate coding approach determines the 
simulator’s performance in efficiently simulating the model . 
Here, we start by producing a continuous and differentiable 
approximation of the proposed memristor model according to 
the guidelines depicted in [18] , [19]. Next, we proceed in 
presenting the VA coding approach selected for robust 
simulation of the model mathematical expression 
A. Model Approximation 
By inspecting the model’s mathematical formulation (8), we 
notice that its behaviour is regulated by the discontinuous step 
function 𝑠𝑠𝑑𝑑𝑝𝑝(∙). Thus, it is replaced by its continuous sigmoid 
approximation 𝜃𝜃
𝑏𝑏(𝑥𝑥) = 1/(1 + 𝑝𝑝𝑥𝑥𝑝𝑝(−𝑥𝑥/𝑏𝑏𝑇𝑇) (11), by properly 
adjusting the parameter 𝑏𝑏𝑏𝑏 for each case to facilitate simulator 
convergence and to keep the model’s dynamics  practically 
unaffected. The role of 𝑏𝑏𝑏𝑏 is to control the slope of the sigmoid 
function around the discontinuous corner points imposed by the 
piecewise nature of the step function. Thus, 
 
𝑠𝑠𝑑𝑑𝑝𝑝� 𝑟𝑟𝑜𝑜(𝑣𝑣) − 𝑅𝑅� ≈ 𝜃𝜃� 𝑟𝑟𝑜𝑜(𝑣𝑣) − 𝑅𝑅� ,                                        (12) 
 
𝑠𝑠𝑑𝑑𝑝𝑝� 𝑅𝑅− 𝑟𝑟𝑚𝑚(𝑣𝑣)� ≈ 𝜃𝜃� 𝑅𝑅− 𝑟𝑟𝑚𝑚(𝑣𝑣)� ,                                        (13) 
 
𝑠𝑠𝑑𝑑𝑝𝑝(±𝑣𝑣) ≈ 𝜃𝜃(±𝑣𝑣),                                                              (14) 
 
where 𝑏𝑏𝑑𝑑= 1 (for (12), (13)) and 𝑏𝑏𝑣𝑣= 10−3 (for (14)). 
The specific parameter values for 𝑏𝑏𝑣𝑣 and 𝑏𝑏𝑤𝑤 where chosen 
so as to r etain the models dynamics practically unaffected and 
at the same time facilitate the simulator to produce solutions 
 
Fig. 5.  (a ) Optimizer test results  and (b) Sweeper test results . Both display 
evolution of measured DUT RS with input programming pulse sequence. Top 
traces for each : RS measurements. Bottom trace s: Programming pulse 
sequences. Gray striations in (a) and (b) separate SET transitions under positive 
voltage bias and RESET unde r negative.  The 𝑅𝑅0 = 13.65𝐾𝐾𝛺𝛺 value in (a) 
denotes the RS around witch the device cycles under the optimizer routine.       
 
Fig. 6.  Switching rate plots resulting from the proposed model (8). (a) 𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑 
vs 𝑣𝑣 for initial RSs that belong to the RR the DU T visits during our 
experiments (10𝐾𝐾𝛺𝛺− 18𝐾𝐾𝛺𝛺). (b) 𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑 vs 𝑅𝑅 for the three absolute voltage 
levels employed by the sweeper testing routine (𝑉𝑉𝑏𝑏= ±(0.6𝑉𝑉− 0.8𝑉𝑉)).  


 7 
adequately fast. Further accuracy may be achieved by lowering 
these values at the cost though of simulation speed.      
B. Verilog-A coding details 
In probably every SPICE memristor model published so far 
[10], [11], [12], [13], [20], [21] the memory effect of the 
memristor is modelled via a feedback controlled integrator 
circuit where the value of the device’s state variable is 
represented by the voltage across a unitary capacitance which 
serves as an integrator of the internal state variable function. 
We follow a similar approach in the presented VA 
implementation in the sense that our model also captu res RS 
evolution by assigning this on an internal voltage node. 
What we propose is the straightforward integration of the 
state variable function ( 8) with the use of the built in VA 
time-domain integration operator “ idt()”. Numerical 
integration may produce errors in sensitive models with 
extremely long time constants but this operation is far more 
preferable than time -domain differentiation  [8]. The integral 
present in ( 8) corresponds to a recursive relationship. VA 
supports the calculation of a differential system that contains 
recursive relationships as long as the variables that express 
recurrence are assigned on voltage nodes or branch current 
flows [22]. Similar to SPICE implementations, the state 
variable (device RS) in our proposed implementation is 
assigned on an internal voltage node. By following this 
approach, the DAE set is integrated with the use of simulator 
dedicated algorithms w ith a plethora of available settings for 
the user designed to produce reliable solutions when properly 
adjusted. Integration in our model is executed rather fast in the 
Spectre simulator since all of the model expressions resulting 
from the smoothing procedure are continuous. 
Another important point is the potential of numerical 
overflows imposed by the exponential functions in the sigmoid 
approximation kernels ( 12) - (14). This is dealt by using the  
limiting exponential function “exp(∙)” . Function 
“limexp(∙)” limits potentially overflowed values by 
linearizing the exponential response after an internally defined 
threshold [22]. 
The VA code for the proposed ReRAM model after applying 
all aforementioned modifications and  specific implementation 
strategies (such as the integration scheme), can be found in  
[23]. The parameter values are defined according to the tested 
device (9), (10). The code is ready to use and can be compiled 
in any electrical circuit simulator that supports VA modules. 
V. C
ONCLUSIONS 
In this work,  we have presented a novel ReRAM model 
implementation method based on  data from  experiments and 
measurement analysis procedures  specifically designed for 
capturing the switching behaviour of a typical 𝑇𝑇𝑇𝑇𝑂𝑂2 ReRAM 
prototype as a function of bias voltage and device resistive 
state. The proposed model captures the aforementioned 
dependencies in a compact functional form that  is able to 
reproduce the evolution of the device resistive state on voltage 
stimulation in its resistive range of operation. Our m odel 
expressions are validated by comparing measured and 
modelled ‘switching surface’ plot for the resistive region the 
DUT exhibits during the experiments. Furthermore, the 
mathematical formulation of the model is  approximated as a 
continuous and differentiable algebraic equation set suitable for 
integration in circuit simulators. Finally, p ractical guidelines 
for coding the model expressions in a robust Verilog-A module 
are discussed.  
R
EFERENCES 
[1] D. B. Strukov, G. S. Snider, D. R. Stewart, and R. S. Williams, “The 
missing memristor found.,” Nature , vol. 453, no. 7191, pp. 80 –3, 
2008. 
[2] L. O. Chua, “Memristor —The Missing Circuit Element,” IEEE 
Trans. Circuit Theory, vol. 18, no. 5, pp. 507–519, 1971. 
[3] F. Bedeschi, R. Fackenthal, C. Resta, E. M. Donze, M. Jagasivamani, 
E. C. Buda, F. Pellizzer, D. W. Chow, A. Cabrini, G. M. A. Calvi, R. 
Faravelli, A. Fantini, G. Torelli, D. Mills, R. Gastaldi, and G. 
Casagrande, “A  bipolar-selected phase change memory featuring 
multi-level cell storage,” in IEEE Journal of Solid -State Circuits , 
2009, vol. 44, no. 1, pp. 217–227. 
[4] A. F. Vincent, J. Larroque, N. Locatelli, N. Ben Romdhane, O. 
Bichler, C. Gamrat, W. S. Zhao, J. O. K lein, S. Galdin -Retailleau, 
and D. Querlioz, “Spin -transfer torque magnetic memory as a 
stochastic memristive synapse for neuromorphic systems,” IEEE 
Trans. Biomed. Circuits Syst., vol. 9, no. 2, pp. 166–174, 2015. 
 
Fig. 7.  Measured (blue symbols) and exhibited by the proposed model (8) ‘switching surface’ (gray surface) for three angles of observation. The model shows 
excellent agreement with measured data thus validating the stationary switching surface assumption and the considered form of  the models DAE set (1), (2) in 
capturing device RS evolution. Red lines reproduce 𝑑𝑑𝑅𝑅/𝑑𝑑𝑑𝑑 vs 𝑣𝑣 responses calculated by (8) for the RSs data was conceived ( 𝑅𝑅𝑆𝑆0𝑜𝑜= 12.60𝐾𝐾𝛺𝛺 and 𝑅𝑅𝑆𝑆0𝑚𝑚=
14.90𝐾𝐾𝛺𝛺). Purple symbols with grey lines are the surface and blue point projections on the 𝑑𝑑𝑅𝑅− 𝑉𝑉 plane for the refined data and the fittings also shown in Fig. 
4(d). Green lines are calculated from (8) by sweeping 𝑅𝑅 for 𝑣𝑣= 𝑉𝑉𝑏𝑏= 0.8𝑉𝑉. 


 8 
[5] T. Prodromakis, K. Michelakis, and C.  Toumazou, “Switching 
mechanisms in microscale memristors,” Electron. Lett., vol. 46, no. 
1, p. 63, 2010. 
[6] S. Gaba, P. Sheridan, J. Zhou, S. Choi, and W. Lu, “Stochastic 
memristive devices for computing and neuromorphic applications.,” 
Nanoscale, vol. 5, no. 13, pp. 5872–8, 2013. 
 [7] A. Serb, A. Khiat, and T. Prodromakis, “An RRAM Biasing 
Parameter Optimizer,” IEEE Trans. Electron Devices, vol. 62, no. 11, 
pp. 3685–3691, 2015. 
[8] A. Serb, J. Bill, A. Khiat, R. Berdan, R. Legenstein, and T. 
Prodromakis, “Unsupervised learning in probabilistic neural 
networks with multi- state metal -oxide memristive synapses,” Nat. 
Commun., vol. 7, p. 12611, Sep. 2016. 
[9] I. Gupta, A. Serb, R. Berdan, A. Khiat, A. Regoutz, and T. 
Prodromakis, “A Cell Classifier for RRAM P rocess Development,” 
IEEE Trans. Circuits Syst. II Express Briefs, vol. 62, no. 7, pp. 676–
680, 2015. 
[10] Z. Biolek, D. Biolek, and V. Biolková, “SPICE model of memristor 
with nonlinear dopant drift,” Radioengineering, vol. 18, no. 2, pp. 
210–214, 2009. 
[11] Y. V. Pershin and M. Di Ventra, “SPICE model of memristive 
devices with threshold,” Radioengineering, vol. 22, no. 2, pp. 485 –
489, 2013. 
[12] R. Berdan, C. Lim, A. Khiat, C. Papavassiliou, and T. Prodromakis, 
“A memristor SPICE model accounting for volatile characteristics of 
practical ReRAM,” IEEE Electron Device Lett. , vol. 35, no. 1, pp. 
135–137, 2014. 
[13] Q. Li, A. Serb, T. Prodromakis, and H. Xu, “A memristor SPICE 
model accounting for synaptic activity dependence,” PLoS One, vol. 
10, no. 3, 2015. 
[14] D. Biolek, M. Di Ventra, and Y. V. Pershin, “Reliable SPICE 
simulations of memristors, memcapacitors and meminductors,” 
Radioengineering, vol. 22, no. 4, pp. 945–968, 2013. 
[15] A. Serb, R. Berdan, A. Khiat, C. Papavassiliou, and T. Prodromakis, 
“Live demonstration: A versatile, low-cost platform for testing large 
ReRAM cross -bar arrays,” in Proceedings - IEEE International 
Symposium on Circuits and Systems, 2014, p. 441. 
[16] R. Berdan, A. Serb, A. Khiat, A. Regoutz, C. Papavassiliou, and T. 
Prodromakis, “A ??- Controller-Based System for Interfacing 
Selectorless RRAM Crossbar Arrays,” IEEE Trans. Electron 
Devices, vol. 62, no. 7, pp. 2190–2196, 2015. 
[17] R. Berdan, T. Prodromakis, A. Khiat, I. Salaoru, C. Toumazou, F. 
Perez-Diaz, and E. Vasilaki, “Te mporal processing with volatile 
memristors,” in Proceedings - IEEE International Symposium on 
Circuits and Systems, 2013, pp. 425–428. 
[18] G. J. Coram, “How to (and how not to) write a compact model in 
Verilog-A,” Proc. 2004 IEEE Int. Behav. Model. Simul. Conf. 2004. 
BMAS 2004., no. Bmas, pp. 97–106, 2004. 
[19] C. C. McAndrew, G. J. Coram, K. K. Gullapalli, J. R. Jones, L. W. 
Nagel, A. S. Roy, J. Roychowdhury, A. J. Scholten, G. D. J. Smit, X. 
Wang, and S. Yoshitomi, “Best Practices for Compact Modeling in  
Verilog-A,” IEEE J. Electron Devices Soc. , vol. 3, no. 5, pp. 383 –
396, 2015. 
[20] H. Abdalla and M. D. Pickett, “SPICE modeling of memristors,” in 
Proceedings - IEEE International Symposium on Circuits and 
Systems, 2011, pp. 1832–1835. 
[21] S. Kvatinsky, E. G. Friedman, A. Kolodny, and U. C. Weiser, 
“TEAM: Threshold adaptive memristor model,” IEEE Trans. 
Circuits Syst. I Regul. Pap., vol. 60, no. 1, pp. 211–221, 2013. 
[22] Accellera, “Verilog -AMS Language Reference Manual,” 
http://accellera.org/images/downloads/standards/v-ams/VAMS-LR
M-2-3-1.pdf, 2009. . 
[23] Messaris, I. A compact Verilog -A ReRAM model (2016). [Online]. 
Available: http://doi.org/10.5258/SOTON/403321
