# 05_reliable_spice_memristors.pdf

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 945
Reliable SPICE Simulations of Memristors,
Memcapacitors and Meminductors
Dalibor BIOLEK1, Massimiliano DI VENTRA2, Yuriy V . PERSHIN3
1 Department of Electrical Engineering/Microelectronics, University of Defence/Brno University of Technology,
Brno, Czech Republic
2Department of Physics, University of California, San Diego, La Jolla, CA 92093-0319, USA
3Department of Physics and Astronomy and USC Nanocenter, University of South Carolina, Columbia, SC 29208, USA
dalibor.biolek@unob.cz, diventra@physics.ucsd.edu, pershin@physics.sc.edu
Abstract. Memory circuit elements, namely memristive,
memcapacitive and meminductive systems, are gaining con-
siderable attention due to their ubiquity and use in diverse
areas of science and technology. Their modeling within the
most widely used environment, SPICE, is thus critical to
make substantial progress in the design and analysis of com-
plex circuits. Here, we present a collection of models of
different memory circuit elements and provide a methodol-
ogy for their accurate and reliable modeling in the SPICE
environment. We also provide codes of these models writ-
ten in the most popular SPICE versions (PSpice, LTspice,
HSPICE) for the beneﬁt of the reader. We expect this to be
of great value to the growing community of scientists inter-
ested in the wide range of applications of memory circuit
elements.
Keywords
Memristors, memcapacitors, meminductors, analog cir-
cuits, SPICE modeling.
1. Introduction
There is presently a large interest in what are com-
monly called memristors, memcapacitors and meminduc-
tors (or collectively simply memelements), namely resis-
tors, capacitors and inductors with memory, respectively [1].
This class of circuit elements offers considerable advantages
compared to traditional devices. Speciﬁcally, these are two-
terminal electronic devices that can store analog informa-
tion even in the absence of a power source. From the point
of view of potential applications, memelements open up the
possibility of manipulating and storing information within
a totally different computing paradigm [2, 3, 4, 5, 6, 7], ex-
tend functionality of traditional devices [8], as well as serve
as model systems for certain biological processes and sys-
tems [9, 10, 11, 12].
Mathematically, an nth-order u-controlled memele-
ment is deﬁned by the equations [1]
y(t) = g (x,u,t)u(t), (1)
˙x = f (x,u,t) . (2)
Here, u(t) and y(t) are any two circuit variables (current,
charge, voltage, or ﬂux) denoting input and output of the
system, x is an n-dimensional vector of internal state vari-
ables, g is a generalized response, and f is a continuous
n-dimensional vector function. Special interest is devoted
to devices determined by three pairs of circuit variables:
current-voltage (memristive systems), charge-voltage (mem-
capacitive systems), and ﬂux-current (meminductive sys-
tems). Two other pairs (charge-current and voltage-ﬂux) are
linked through equations of electrodynamics and therefore
are of no practical interest. Devices deﬁned by the relation
of charge and ﬂux (the latter being the integral of the voltage)
are not considered as a separate group since such devices can
be redeﬁned in the current-voltage basis [13].
However, future progress in the analysis of complex
circuits involving any of these elements requires reliable
simulation tools that are easy to implement and ﬂexible
enough to provide solid predictions on a wide range of phys-
ically realizable models. The Simulation Program with In-
tegrated Circuit Emphasis (SPICE) environment is one such
general-purpose simulator that has been successfully used in
the analysis of integrated circuits for forty years. SPICE al-
lows the testing of complex circuits before they are actually
implemented experimentally, thus saving a lot of time and
resources in their fabrication.
Being new on the circuit scene, memelements do not
have many years of testing within the SPICE environment.
Nonetheless, more and more SPICE models are being con-
sidered with different levels of complexity [14, 15, 16, 17,
18, 19, 20, 21, 22]. Oftentimes, readers are interested in the
SPICE code itself and its reliability within the range of phys-
ical parameters used. Unfortunately, both the codes and reli-
ability criteria are not always available in the literature thus
limiting the use of some of the most popular SPICE models
of memelements.
This paper attempts to ﬁll this gap by providing sev-

946 D. BIOLEK, M. DI VENTRA, Y . V . PERSHIN, RELIABLE SPICE SIMULA TIONS OF MEMRISTORS, MEMCAP ACITORS . . .
eral models of ideal and non-ideal memristive, memcapac-
itive and meminductive elements and their implementation
(codes) in the most popular SPICE versions (PSpice, LT-
spice, HSPICE), focusing on the well-known PSpice. Our
goal is also to provide a general methodology for accurate
modeling within this environment so that readers interested
in implementing different models can easily build from the
examples we provide in this paper and venture out on their
own. We think this could also serve as an excellent teach-
ing tool complementing others (e.g., experiment-based ones
[23]) for the next generation of scientists and engineers in-
terested in this ﬁeld. This methodology is given in Sec-
tion 2 which follows this Introduction. In later Sections we
will then focus on speciﬁc examples of memristive, mem-
capacitive and meminductive systems and their modeling in
SPICE.
Importantly, instead of focusing on different levels of
sophistication in describing the same electronic device, we
concentrate on SPICE models of physically different mem-
ory devices (e.g., bipolar, unipolar, etc.) that are generally
classiﬁed as memristive, memcapacitive or meminductive
systems. For completeness, such a presentation is integrated
with models of ideal memory elements – memristors, mem-
capacitors and meminductors. For each device, we select
a reasonable complexity in modeling essential features of
device operation relying, in some cases, on original models
proved to be useful in device simulations.
2. Methodology for Accurate and
Reliable Modeling of Memelements
with SPICE
Throughout the development of memelement models
and their implementation in SPICE-family simulation pro-
grams, several limitations and speciﬁc features of these pro-
grams should be taken into consideration. This way situa-
tions can be avoided in which the program ﬁnds a solution
which is burdened with errors, either evident or not apparent
at ﬁrst sight, or when the solution is not found at all. The
above two kind of problems, i.e., imperfections and non-
convergence issues, can be magniﬁed in circuits contain-
ing memelements, i.e., which have speciﬁc hysteresis behav-
ior. For example, it is shown in [24] that the classical algo-
rithms of ﬁnding the periodical steady states, which are im-
plemented in several simulation programs such as HSPICE
RF, Micro-Cap, and partially in LTspice, can be ineffective
for circuits containing memelements. In addition, the work
[25] calls attention to the fact that the periodic solution of
the circuit containing the classical model of the HP memris-
tor [14, 15, 16, 17, 26, 27], found within the transient anal-
ysis, can be entirely corrupted via common numerical errors
accumulated throughout the analysis. Nevertheless, without
an extended analysis, these results can be easily accepted as
correct.
Paradoxically, problems with precision and reliability
can also arise when working with the ideal memelement
models whose behavior is free from the ubiquitous para-
sitic effects. Such simpliﬁcation can produce poor condi-
tions for the operation of SPICE computational core. On the
other hand, the analysis of the behavior of such ideal mod-
els is of great importance, if understanding the fundamental
properties of memelements is the key aim of the simulation.
Clearly, any deviation from the ideal behavior due to para-
sitic effects is undesirable and troublesome.
The SPICE modeling and simulation is about the com-
promise between accuracy of the results and the speed and
reliability of the procedure to obtain them. Since the ac-
curacy of the analysis of memelements is frequently a key
factor, it is advisable to build the model just in relation to
this criterion. If convergence problems appear, such model
should be modiﬁed, taking into account the well-known rules
of the reliable behavioral modeling [28], combining them
with proper settings of the program options and the parame-
ters of concrete analysis [29].
The transient analysis is the most widely used SPICE
analysis of circuits containing memelements. That is why we
focus on the rules on how to build such memelement models
in SPICE which would comply with speciﬁc limitations of
the numerical algorithms used throughout the transient anal-
ysis in the SPICE environment. Some of these rules should
be applied with the aim of achieving results as accurate as
possible. The purpose of other rules is to prevent conver-
gence problems while analyzing the circuits with memele-
ments, or to solve them as early as they appear.
The mathematical model of each memelement can be
divided into the submodel of the element port (of memris-
tive, memcapacitive, or meminductive nature), and into the
part modeling the differential equations for the internal state
variables which control the port parameters (the memris-
tance, memcapacitance, and meminductance). Both groups
are modeled in SPICE environment via a mix of the tools of
conventional and behavioral modeling. The behavioral mod-
eling uses especially the controlled sources and mathemati-
cal formulae. The accuracy and reliability of the simulation
results depend on the following factors which are then dis-
cussed below:
• Numerical limits, given by a ﬁnite precision and ﬁnite
dynamic range of the number representation in SPICE
environment.
• Rules of building-up behavioral models, resulting in
continuous equations and their derivatives, bearing in
mind the numerical limits.
• The way of modeling the state and port equations.
• Setting the parameters of transient analysis and the
global parameters.
The recommendations discussed below are applicable
to a wide class of SPICE-family simulation programs. Some

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 947
speciﬁcs of concrete programs are analyzed separately. De-
tails which are beyond this text can be found in the program
documentation, e.g., [30, 31, 32].
2.1 Numerical Limits Affecting Accuracy and
Convergence in SPICE-Family Programs
Double-precision binary ﬂoating-point (a “double” in
short) is a commonly used format on PCs, enabling the num-
ber representation within the dynamic range from 2−1022 to
21023, thus from about 10−308 to 10308. The signiﬁcant pre-
cision is 53 bits with 52 explicitly stored, which gives about
16 digits of accuracy. The maximum relative rounding error
(the machine epsilon) is 2−53, i.e., approximately 10−16. In
SPICE environment, this format shares all voltages and cur-
rents and also the system variable TIME used throughout the
transient analysis. However, the above limits are modiﬁed by
concrete SPICE-family programs. For example, PSpice lim-
its the voltages and currents larger than 10 10 volts and am-
peres and the maximum derivatives are 10 14. These limits
are rather higher in HSPICE, LTspice and Micro-Cap. The
smallest nonzero numbers which the programs can process
are not commonly documented. For example, it is 10−30 for
PSpice. The above limits together with other items, which
are deﬁned in global settings (acceptable relative and abso-
lute errors, number of iterations, etc.) affect the accuracy but
also the program (in)ability to ﬁnd the solution within these
limits.
2.2 Rules of Building-Up Behavioral Models
Some of the rules are well documented in the literature
[28, 29, 30, 31, 32]. Below is given a brief account with
reference to the memelement modeling for the subsequent
transient analysis. Speciﬁc details are omitted. They appear
in Section 6.
2.2.1 Components with (Un)realistic Parameters
Behavioral modeling of non-electric quantities in
SPICE, based on various analogies, for example modeling
of the position of the boundary between the doped and un-
doped layers of a TiO2 memristor, can lead to the selection of
atypical values of the parameters of the elements in the sub-
stitutive electric circuit. As a result, the computed voltages
and currents can be extremely high or low, causing numer-
ical difﬁculties. It is useful to avoid small ﬂoating resistors
because any error in the computed nodal voltages of such re-
sistors results in large error currents [28]. If the resistor was
included in the circuit as a current probe, then it should be
replaced by a 0-V olt voltage source. Note that a large num-
ber of such probes increases the size of the circuit matrix
which can negatively inﬂuence the program operation. Sim-
ilar difﬁculties as small ﬂoating resistors can arise with large
ﬂoating capacitors. Also note that convergence problems can
appear in the feedback systems with large loop gains. Some
modeling techniques use passive R, C, and L elements with
negative parameters. These methods are not recommended
because they can cause unstable behavior of the model.
2.2.2 (Dis)continuous Models
Discontinuous models result from the operation of sev-
eral memory elements, for example memristive systems with
threshold [21] or multi-state memristor switching memo-
ries with discontinuous memristance versus state character-
istics [33]. The rigorous modeling of these discontinuities is
thus desirable for providing high precision of the model. On
the other hand, it is a potential source of numerical prob-
lems which can cut down the precision. A possible strategy,
which can work well especially for not so large-scale sys-
tems, is to model rigorously the discontinuous characteris-
tics of memory elements in the ﬁrst step. In the case of con-
vergence problems or unrealistic results, some of the tech-
niques of smoothing the characteristics can be applied sub-
sequently. For example, the step function (STP in PSpice,
U in LTspice), which is frequently used for modeling the sat-
urations inside memdevices, can be replaced by a sigmoid
function with adjustable parameters, which sets the maxi-
mum possible slope of the transition between two states. The
IF function for modeling piece-wise constitutive relations
of memelements, can be modeled such that the derivatives
are not changed abruptly in order to remove the discontinu-
ities of the ﬁrst derivatives at the corner points. The signal
waveforms can serve as other sources of discontinuities. The
well-known conventions should be followed here, for exam-
ple that the pulses should be modeled with realistic rise/fall
times.
2.2.3 Models (In)sensitive to Numerical Errors
Models of some analog circuits are highly sensitive to
numerical errors which originate from a ﬁnite precision of
the number representation, and which can be due to speciﬁc
operations of computational algorithms. The model, built up
from such blocks, can then behave differently in the envi-
ronments of various simulation programs, even if the simu-
lations run under apparently identical conditions. The simu-
lation outputs can be far away from the real behavior of the
systems being modeled. However, it is entirely up to the user
to notice it. The errors are obvious in several cases but not
always.
It is also necessary to distinguish the source of the
model sensitivity: it can be either the nature of the modeled
circuit or the improper way of constructing the mathemati-
cal model. The models with extremely long time constants
exhibit high sensitivities to numerical errors, which work as
accumulators of these errors during the transient simulation
run where the differential equations are solved numerically.
A typical example of a sensitive circuit is an ideal integrator
which is, however, the basic building block of ideal mem-
ristors, memcapacitors, and meminductors. Any numerical
problem at arbitrary instants of time during the integration
algorithm of the transient analysis run can then inﬂuence the
results computed at all the subsequent instants. A more im-
portant source of numerical problems can be the block of
time-domain differentiation. It does not work as an accumu-
lator but as an ampliﬁer of the truncation errors, with unlim-

948 D. BIOLEK, M. DI VENTRA, Y . V . PERSHIN, RELIABLE SPICE SIMULA TIONS OF MEMRISTORS, MEMCAP ACITORS . . .
ited bandwidth since its gain increases by 6 dB with doubling
the frequency.
The d /dt operation should be avoided in behavioral
modeling, for example via a substitution of the d /dt-type
model by its dual integrating version (see Section B.6). As
an interesting consequence, the capacitor currents and in-
ductor voltages are not computed in SPICE as accurately as
the capacitor voltages and inductor currents. For example,
the capacitor current is proportional to the differentiation of
voltage with respect to time. Then any numerical error in the
voltage is ampliﬁed to the current waveform. This suggests
a useful rule: as far as possible, we should prefer computa-
tions within the behavioral models with capacitor voltages
and inductor currents rather than with capacitor currents or
inductor voltages.
Since the above circuits either accumulate or amplify
errors, the only thing we can do against such effects is
to minimize the consequences, for example via selecting
a proper integration method and tuning its parameters (see
Section 6). On the other hand, the model sensitivity to nu-
merical errors can be undesirably increased via an improper
construction of the model. For example, if the model gain is
spread unreasonably among individual cascade blocks, it can
bring the local attenuation of the signal near the low limit
of the dynamic range of the number representation or, on
the contrary, its overﬂow. Another typical case is an im-
proper subtraction of two commensurate numbers which re-
sults in a high truncation error. An example of this is the
well-known Joglekar window function for modeling nonlin-
ear dopant drift in TiO2 memristors, which for the parameter
p = 1 [27] can be written in two following ways:
f (x) = 1− (2x− 1)2 (3)
or
f (x) = 4x (1− x) . (4)
For the memristor in its boundary state with a maxi-
mum memristance, when x is close to 0, the ﬁrst model gen-
erates signiﬁcantly larger errors. Due to the ﬁnite dynamic
range of the double format, the term (2x− 1)2 cannot differ
from 1 by less than the value of 2−53. Then one can conclude
that for all values x < 2.776× 10−17 the values of window
function are cut to zero. For the second model, however,
such limitation appears ifx is less than its minimum value for
the double type, i.e., for x < 2−1022 = 2.225× 10−308. Such
a model sensitivity to truncation errors can play a detrimen-
tal role within all commonly used models of memelements
which utilize window functions (see Section 2.2.4).
2.2.4 Selection of State Variables of Memelements –
the Key to Accurate Computation
Truncation errors and their accumulation throughout
the integration process of the transient analysis can be the
cause of mistaken results even for the simulation of sim-
ple circuits containing memelements. The reason can be in
an improper form of the differential state equation(s) of the
memelement which results in high sensitivity of its solution
to the truncation errors. It is shown in [25] that such high
sensitivity occurs for the well-known differential equation
of the TiO2 memristor where the time-domain derivative of
the normalized positionx of the boundary between the doped
and undoped layers is directly proportional to the memristor
current and the window function f (x), which tends to zero
at boundary points x = 0 and x = 1. If the memelement ap-
proaches very closely the boundary state, then SPICE can
erroneously evaluate, due to the truncation errors, that this
state is already attained. Then the memelement state is
frozen since the derivative of the state variable with respect
to time is zero. The element can change from this state only
due to some other numerical errors. In doing so, however,
the duration of this “pseudo-ﬁxed” state, which is of a ran-
dom character, can signiﬁcantly affect subsequent computa-
tions.
The fact that something is wrong with the simulation
results is obvious only when it is found that some memele-
ments ﬁngerprints are violated. This is of particular concern
because it takes effect latently and without any warnings or
error messages of the simulation program. However, it can
corrupt the simulation results for complex circuits with other
memelements utilizing the window functions, such as mem-
capacitors [18] and meminductors [19]. For cases when the
element state is swept far from the boundary states, the sim-
ulation is correct. However, it fails when trying to simulate,
for example, the hard switching effects.
The above troubles can be avoided via a selection of
a more suitable state variable which would lead to another
differential equation. Its solution must be much less sen-
sitive to numerical errors. Evaluating this state variable,
the memelement parameter, for instance the memristance,
is computed in the second step, either directly from the state
variable-to-parameter relationship, or by the medium of the
state variable which has caused troubles in the classical ap-
proach. It is shown in [25] that the so-called native state
variable (for example the charge or ﬂux for the memristor),
is the good choice for modeling ideal memelements. Then
the state equation is a simple model of ideal integrator. It is
a potential accumulator of the truncation errors though, but
the resulting effect is much better than for the above sensitive
case.
2.2.5 Behavioral Modeling of Integrators
The model of the integrator is necessary for modeling
the state equations. SPICE implementation of the integrator
is usually in the form of a grounded 1-Farad capacitor with
a controlled current source in parallel. If the source current is
equal to the quantity which is integrated, then the capacitor
voltage in volts is equal to the computed integral during the
transient analysis. The initial state at time 0 can be set via the
IC attribute of the capacitor. Shunt resistor with a large re-
sistance, not disturbing the integration process, is necessary
for providing DC path to the ground.
Note that extremely high capacitances can generate
non-convergence issues. The integration capacitance can be

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 949
decreased simultaneously with decreasing charging current.
Then it is useful to analyze if this current, which models the
quantity being integrated, has realistic values. Otherwise,
the numerical problems at the bottom area of the dynamic
range can take effect.
Several SPICE-family programs offer built-in func-
tions for signal integration, for example the SDT function
in PSpice and Micro-Cap and the IDT function in LTspice.
The properties of these functions are not documented. It is
proved for PSpice Cadence v. 16.3 that the SDT function ac-
cumulates the truncation errors slightly more than the con-
ventional integrator model. In other words, both models pro-
vide the same accuracy if a smaller step ceiling is used for
the integration via SDT function. The precision of the inte-
gration process also depends on the parameters of transient
analysis, on the integration method, and on other simulator
options (see Section 6).
2.2.6 Modeling Memristive, Memcapacitive, and
Meminductive Ports
These ports are modeled as R, C, and L two-terminal
devices with varying parameters. For example, the memris-
tor is modeled as a resistor whose resistance is controlled
by the state quantity. The model of more general memris-
tive systems can use a resistor with nonlinear current-voltage
characteristic which is controlled by a set of state variables.
Similar structures can be used for modeling memcapacitive
and meminductive systems, utilizing capacitors and induc-
tors with varying characteristics. The SPICE standard does
not support a direct modeling of R, C, and L elements with
varying parameters. Apart from speciﬁc features of several
programs, these elements can be modeled indirectly via tools
of behavioral modeling, namely with the help of the con-
trolled sources and mathematical formulae.
Memristive systems
Resistors with varying resistance R or conductance
G are modeled either as voltage source controlled by the
equation V = R(x,I,t)I, where I is the source current, or as
a current source controlled by the formula I = G(x,V,t)V ,
where V is the source voltage and x are internal state vari-
ables. Several rules should be followed:
1) During the simulation, the source formulae should
not generate any divisions by small numbers, let alone zero,
and they should not generate other numerical errors (for ex-
ample, any subtraction of commensurate numbers which is
sensitive to rounding errors). If the memristance of the mod-
eled device is close to zero, it is more preferable to work with
the memristance than with the memductance, and to use the
model based on the voltage, not the current source.
2) If it is possible to divide the formula for the mod-
eled memristance or memductance into ﬁxed and variable
parts, then the ﬁxed part can be modeled by a classical ﬁxed
element and the remaining part by a behavioral controlled
source. The variable part should comply with the above
rule 1). The ﬁxed part must represent positive value of the
memristance or memductance. This provides reliable models
of the memristive/memconductive port via Th´evenin/Norton
models without any potential conﬂicts due to such connec-
tions of ideal sources violating the Kirchoff’s voltage law/
Kirchoff’s current law.
Note that several SPICE-family programs enable a di-
rect modeling of resistors via equations. In HSPICE, the re-
sistance can be a function of arbitrary voltage or current, or
of any other system variable such as TIME. Similar features
are provided also by Micro-Cap.
Memcapacitive systems
The capacitive port of charge-controlled memcapaci-
tive systems can be modeled by the formula V = D(x,q,t)q,
where q is charge and D is inverse of the memcapacitance,
which depends on the state variables x and on the charge.
This implies that such port can be modeled via a voltage
source with the voltage computed from the state variables
and the charge. The charge is calculated as the integral of
the port current.
Accordingly, the capacitive port of voltage-controlled
memcapacitive systems can be modeled as q = C(x,V,t)V ,
where C is a memcapacitance, which depends on state vari-
ables x and on the voltage. It appears from this that such port
can be modeled via a controlled charge source. Nevertheless,
such a source is not commonly available in all the SPICE-
family programs. Then the current should be computed via
differentiating the charge with respect to time, and the ca-
pacitive port should be implemented by the current source.
However, the differentiation is not suggested as a reliable
numerical procedure.
It is advisable to follow the rules No. 1) and 2) for the
memristance modeling, with the appropriate modiﬁcations
for the memcapacitive model. In the case of partitioning the
(inverse) memcapacitance into the ﬁxed and varying parts,
the capacitive port can be modeled by a ﬁxed capacitor and
controlled source in (series) parallel.
Note that some SPICE-family programs enable more
general modeling of the capacitors. Micro-Cap provides the
capacitance deﬁnition via a formula, or the capacitor charge
can be described as a function of the capacitor voltage. LT-
spice can model the capacitor charge as a general function of
a special variable x which is the capacitor voltage. HSPICE
enables the capacitance deﬁnition as a function of its termi-
nal voltages, external voltages and currents, or their combi-
nations (HSPICE RF), or the capacitor charge can be deﬁned
as a function of the terminal and other voltages and currents.
Also, some present versions of OrCAD/Cadence PSpice can
work with the charge sources, namely through the extended
syntax of the G-type controlled source, which uses a formula
for the charge. Such programs enable convenient modeling
of memcapacitive systems, controlled via the current or volt-
age.

950 D. BIOLEK, M. DI VENTRA, Y . V . PERSHIN, RELIABLE SPICE SIMULA TIONS OF MEMRISTORS, MEMCAP ACITORS . . .
The following rule should be applied when working
with the memcapacitive models: every node must have its
DC path to ground. If it is not the case, a large shunting
resistor must be added to the circuit such that its resistance
cannot affect the simulation.
Meminductive systems
The inductive port of voltage- (or ﬂux)-controlled me-
minductive systems can be modeled by the formula I =
Λ(x, φ,t)φ, where φ is ﬂux linkage and Λ is the inverse of
meminductance, which depends on the state variables x and
on the ﬂux. This implies that such port can be modeled via
a controlled current source. The current can be calculated
from the state variables and the ﬂux, the latter one via inte-
grating of the port voltage.
Accordingly, the inductive port of current-controlled
meminductive systems can be modeled as φ = L(x,I,t)I,
where L is the meminductance which depends on the state
variables x and on the current. Such port can be modeled
via a controlled ﬂux source. Nevertheless, such a source is
not commonly available in all the SPICE-family programs.
Then the voltage should be computed via differentiating the
ﬂux with respect to time, and the inductive port should be
implemented by the voltage source. Remember that the dif-
ferentiation is not a preferred procedure. In the case of par-
titioning the (inverse) inductance into the ﬁxed and varying
parts, the inductive port can be modeled by a ﬁxed inductor
and controlled source in (parallel) series.
Several SPICE-family programs enable more general
modeling of the inductors, thus they can be recommended
for a more comfortable modeling of current-controlled me-
minductive systems. Micro-Cap provides the inductance def-
inition via a formula. Alternatively, the inductor can be de-
ﬁned by a ﬂux formula which must depend on the inductor
current. LTspice can model the inductor ﬂux as a general
function of a special variable x, which is the inductor cur-
rent. HSPICE enables the inductance deﬁnition as a func-
tion of nodal voltages and branch currents. The inductor
can be also deﬁned by the ﬂux formula. Present OrCAD/-
Cadence PSpice versions use special F-syntax of the E-type
controlled source (the ﬂux source), which generates the volt-
age as a time-derivative of the ﬂux. The ﬂux can be deﬁned
by a formula.
If the convergence or other numerical problems appear
due to the inductors in the circuit, the rule should be applied
that all inductors should have a parallel resistor, which limits
the impedance at high frequencies. The resistance must be
high enough in order to prevent its inﬂuence to the circuit
parameters. Its value should be set equal to the inductor’s
impedance at the frequency at which its quality factor begins
to roll off. The purpose of such resistor is to prevent undesir-
able voltage spikes associated with abrupt changes of the in-
ductor current, causing the convergence problems. Also note
that the SPICE programs do not allow the loops containing
only ideal voltage sources and inductors. Such loops must
be completed by resistors. Corresponding resistances must
be low enough but not extremely low (see Section 2.2.1).
3. SPICE Modeling of Memristive
Devices
3.1 Model R.1: Ideal Memristor
Model: In a current-controlled memristor [34], the
memristance R depends only on charge, namely,
VM = R(q(t))I (5)
with the charge related to the current via time derivative
I = dq/dt. The direct use of Eq. (5), however, is uncom-
mon. More common are models inspired by physics of re-
sistance switching. In particular, a popular model [26] is
based on the assumption that the memristive device consists
of two regions (of a low and high resistance) with a moving
boundary. The total memristance can be written as a sum of
resistances of two regions
R(x) = Ronx + Roff(1− x). (6)
Here, x∈ [0,1] parameterizes the position of boundary, and
Ron and Roff are limiting values of memristance. The equa-
tion of motion forx can be written, for example, using a win-
dow function W (x) as
dx
dt = kW(x)I (7)
where k is a constant, and W (x) is often selected as [27]
W (x) = 1− (2x− 1)2p (8)
where p is a positive integer number, which is related to
switching linearity. Physical devices with higher switching
linearity are described by larger values of p.
Features: The above model takes into account bound-
ary values of memristance. It does not involve a switch-
ing threshold, is not stable against ﬂuctuations, and exhibits
over-delayed switching [35]. We emphasize that (6)-(8) de-
scribe an ideal current-controlled memristor. In principle,
(7) can be integrated for an arbitrary function W (x) and thus
x can be expressed as a function of q. For example, if W (x)
is given by Eq. (8) with p = 1, then one ﬁnds
1
4ln x
1− x = k(q(t) +q0) (9)
where q0 is the integration constant (initial condition). Con-
sequently,
R(q(t)) = Roff + Ron− Roff
e−4k(q(t)+q0) + 1 . (10)

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 951
It can be more convenient to re-writeq0 in terms of the initial
memristance Rini = R(q = 0) resulting in
R(q(t)) = Roff + Ron− Roff
ae−4kq(t) + 1 , a = Rini− Ron
Roff− Rini
. (11)
Equation (11) represents a reliable model for SPICE simula-
tion: the memristance is derived as a function of the native
state variable q, thus the state equation is not sensitive to the
truncation errors in contrast to (7). In SPICE, the charge can
be obtained via integrating the port current I by the capac-
itor Cint according to Fig. 1. Then the charge in coulombs
is equal to the voltage of the node Q in volts. It is obvious
from (11) that the memristive port can be modeled as a serial
connection of the ﬁxedRoff resistor and a controlled voltage
source (see Fig. 1 (a)). For modeling large circuits, which
can be prone to convergence problems, the Norton equiva-
lent according to Fig. 1 (b) can be more advantageous. For
the sake of brevity, only the codes of the ﬁrst model are given
in the Supplementary Materials 1.
Fig. 1 (a)
R
plus
I Q
I
 offR
RR
intC
auxR
resE QG
1F 100MΩ
Iae
RR
QkV
offon
1)(4 +
−
−
minus
plus
(a)
plus
I
I
1F 100MΩ
Q
 offR
minus
intC
auxRresG
QG
 I
ae
RR
QkV
offon
1
/1
)(4 +
−
−
(b)
Fig. 1. Possible SPICE implementations of the ideal memristor
model (5), (11). The memristive port can be modeled via
a voltage source with a serial resistor (a) or via an equiv-
alent current source with a parallel resistor (b). Here,
V (Q) is the voltage of the node Q, which has the same
numerical value in volts as the charge q(t) in coulombs.
Results: Figure 2 shows the simulation results in
PSpice for the memristor model from the Supplementary
Materials 1, utilizing the circuit ﬁle therein. The correct-
ness of the results can be evaluated via the charge waveform
(i.e., the voltage of the internal node Q of the subcircuit)
which must be periodical without any initial transients. For
LTspice, it is preferable to use Gear integration which leads
to the best results. Note that PSpice user cannot select the
Gear method.
We emphasize that the memristive port can be modeled
in HSPICE also by a direct formula:
Rmem plus minus R=
+ ’ Roff +( Ron - Roff )/(1+ a* exp ( -4* k*V(q ))) ’
However, the accuracy of the computation cuts down. It can
be increased back by decreasing the maximum time step.
10mA
Fig. 2(a)
-10mA
0A
SEL>>
1.0V1
 
10mA2
 
           V(in)
-1.0V -0.5V 0V 0.5V 1.0V
I(Xmem.Eres)
10mA
0V 0A(b)
2.0mV
1  V(in) 2  I(Xmem.Eres)
-1.0V -10mA
   >>
0V
1.0mV
(c)
           Time
0s 2s 4s 6s 8s 10s
V(Xmem.q)
-1.0mV
Fig. 2. PSpice outputs for the case of an ideal memristor driven
by the sine-wave 1 V/1 Hz voltage source: (a) current-
voltage pinched hysteresis loop, (b) voltage and cur-
rent waveforms, and (c) charge (i.e., integral of current)
waveform.
3.2 Model R.2: Bipolar Memristive System
with Threshold
Model: Several approaches to take into account
a threshold-type switching are available in the literature
[9, 36, 37, 22]. Here, we consider a model of a voltage-
controlled memristive system with voltage threshold sug-
gested in [9] by two of us (YVP and MD). For the sake of
simplicity, we consider its reduced version (without switch-
ing below the threshold) [38]. In this model, the memris-
tance R plays the role of the internal state variablex, namely,

952 D. BIOLEK, M. DI VENTRA, Y . V . PERSHIN, RELIABLE SPICE SIMULA TIONS OF MEMRISTORS, MEMCAP ACITORS . . .
x≡ R, deﬁning the device state via the following equations
I = x−1VM, (12)
dx
dt = f (VM)W (x,VM) (13)
where f (.) is a function modeling the device threshold prop-
erty (see Fig. 3) and W (.) is a window function:
f (VM) = β (VM− 0.5 [|VM +Vt|−| VM−Vt|]) , (14)
W (x,VM) = θ (VM) θ (Roff− x) +θ (−VM) θ (x− Ron)(15)
Here θ(·) is the step function, β is a positive constant charac-
terizing the rate of memristance change when |VM| > Vt, Vt
is the threshold voltage, and Ron and Roff are limiting values
of the memristance R. In Eq. (15), the role of θ-functions
is to conﬁne the memristance change to the interval between
Ron and Roff.
 
 
 
 
  
VM
f
0 Vt
β
β
-Vt
Fig. 3. Sketch of the function f (VM) modeling the voltage
threshold property.
Fig. 4
plus x)),(()( MM VxVWVf
minus
VM
intC
auxRpmG
xG
1F 
IC=R
100MΩ
)(/ xVVM
minus IC=Rinit
Fig. 4. SPICE model of the memristive device with threshold.
Features: Equations (12)-(15) provide a compact real-
istic description of bipolar memristive devices. The model
takes into account boundary values of memristance and
threshold-type switching behavior. In many real memristive
devices, the resistance change is related to the atomic migra-
tion induced by the applied ﬁeld and not by the electric cur-
rent ﬂow. Therefore, models with voltage threshold [9, 37]
are physically better justiﬁed than those with the current one
[36, 22]. From the point of view of the numerical analysis
of (12), the division by the state variable x is not a problem
since the memristance varies only within the Ron to Roff lim-
its. Based on (12) and (13), the basic schematics of SPICE
implementation is presented in Fig. 4.
In this approach, the derivative of the memristance (13)
is modeled by the current of the controlled sourceGx, and its
integral - the memristance in ohms - is equal to the voltage of
the node x in volts. According to (12), the memristive port is
modeled by the current source Gpm. Its current is computed
as a ratio of the terminal voltage and the memristance. Equa-
tions (14) and (15) contain discontinuous function (step) and
function with discontinuous derivatives (absolute value). It
can be a source of serious convergence problems, especially
for applications utilizing large-scale models. In such cases,
smoothed functions can be used based on sigmoid modeling
of the step function according to the formula
θS(x) = 1
1 + e−x/b (16)
where b is a smoothing parameter.
Then the smoothed version of the absolute value func-
tion, absS(x), can be
absS(x) = x [θS(x)− θS(−x)] . (17)
If a convergence problem appears, a proper trade-off be-
tween the accuracy and reliability can be usually found via
tweaking the b parameter. For the simplicity, the correspond-
ing smoothed functions stp S(x), abs S(x) and the functions
fS(x) and WS(x) derived from them are deﬁned in the source
codes 2 directly within the individual subcircuits.
Results: Examples of the PSpice outputs, generated
from the source codes from the Supplementary Materials 2,
are shown in Fig. 5. As follows from Fig. 3, the func-
tion f (VM) generates narrow pulses when the memristive de-
vice is excited by sine-wave voltage VM with the amplitude
Vmax > Vt. Considering the positive pulse in Fig. 5, it will
be integrated into the voltage of the nodex until the memris-
tance R = V (x) approaches its boundary value Roff. At this
instant, the window function W and also the current of the
source Gx are set to zero, and the memristance is ﬁxed to
the value Roff. This state persists until the voltage VM drops
below the negative threshold level −Vt. Then the function
f (VM) becomes negative. It causes the negative current pulse
of the source Gx, and its integral will decrease the memris-
tance towards Ron. It is obvious from Fig. 5 that, although
the memristance did not drop to its bottom limit, the current
is cut off at the instant when the voltageVM has exceeded the
threshold Vt (the effect of the window W). The memristance
is held on the low level all the time when the voltage VM
travels within the stable zone between both threshold levels.
Then the system continues in the motion in the frame of its
periodical steady state.

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 953
It follows from the above analysis that the combina-
tion of unreasonably time step and error criteria can result in
an incorrect determination of the boundary conditions in the
integration of current pulses. If this happens, then the sim-
ulated waveforms can be distorted due to signiﬁcant errors.
One can make certain of this via step-by-step selection of
various parameters/options of the transient analysis or error
criteria. To identify incorrect results or to achieve the neces-
sary accuracy, we can use the following guides (they are true
for the speciﬁc netlist in the Supplementary Materials 2):
1. The upper level of the memristance (the curve
V(Xmem.x)) must be Roff. Each declination from this
value is a numerical error.
2. The bottom value of the memristance (if it does not
reach the boundary Ron, see Fig. 5), must be
Roff− β
2π f Vt

2
√(Vmax
Vt
)2
− 1− π + 2sin−1 Vt
Vmax

 (18)
where f is the signal frequency.
For the simulation example from Fig. 5, the neces-
sary accuracy can be accomplished e.g. via a low relative
error RELTOL=1u in combination with the maximum time
step equal to one thousandth of the simulation time. Then
for PSpice results in Fig. 5, the low-level memristance is
3.1819 kΩ whereas the accurate value according to (18) is
3.1847 kΩ. Note that the simulation in HSPICE according
to code 2 provides even more accurate computation. If the
simulation program enables to select the integration method,
then the Gear integration is preferable in this case due to its
stability throughout the analysis over many repeating peri-
ods.
Note that the current of the source Gx in the SPICE
code 2 is multiplied by a number 1p and that the integrating
capacitor has the capacitance of 1 pF. It is due to the opti-
mization of the dynamic range of the source current. With-
out this multiplication, the current would reach extreme val-
ues of 4 TA, which is not optimal with regard to the stan-
dard analysis options. In addition, since the voltage of the
node x in volts is equal to the memristance in ohms, this
voltage appears in kilovolts, being also out of the typical
values. That is why, if necessary, the following optimiza-
tion step would lead to set and compute the memristance in
kiloohms, not in ohms, with an increase of the capacitance
Cint by three orders to 1nF. Then the voltageV (x) would ap-
pear on the common level of volts. HSPICE provides the
most accurate results among all three simulation programs.
The option RUNLVL=6 forces HSPICE into the regime of
enhanced precision (see Section 6).
Fig. 5
2.0mA
(a)
0A
4.0A
           V(1)
-6.0V -4.0V -2.0V 0V 2.0V 4.0V 6.0V
I(Xmem.Gpm)
-2.0mA
0A
(b)
5.0V1
 
2.0mA2
 
12KV3
 
I(Xmem.Gx)
-4.0A
SEL>>
I(Xmem.Gx)
0V 0A
4KV
8KV(c)
           Time
0s 50ns 100ns
1  V(1) 2  I(Xmem.Gpm) 3  V(Xmem.x)
-5.0V -2.0mA 0V
   >>
Fig. 5. PSpice outputs for the memristive device with threshold
driven by a sine-wave excitation. The parameters are de-
ﬁned in the SPICE code in the Supplementary Materi-
als 2.
3.3 Model R.3: Phase Change Memristive Sys-
tem
Model: In phase change memory (PCM) cells [39], the
information storage is based on the reversible phase transfor-
mation of relevant materials. In terms of memristive formal-
ism, PCM cells can be described as unipolar second-order
current- or voltage- controlled memristive systems. Follow-
ing general ideas of [40], we consider here a simple model of
PCM cells based on equations describing thermal and phase
change processes. Using the temperature T and the crys-
talline fraction Cx as internal state variables, the model of
PCM cells can be written as
I = R−1(Cx,VM)VM, (19)
dT
dt = V 2
M
ChR(Cx,VM) + δ
Ch
(Tr− T ) , (20)
dCx
dt = α (1−Cx) θ (T− Tx) θ (Tm− T )
−βCxθ (T− Tm) (21)
where
R(Cx,V ) = Ron + (1−Cx) Roff− Ron
e
V−Vt
V0 + 1
, (22)

954 D. BIOLEK, M. DI VENTRA, Y . V . PERSHIN, RELIABLE SPICE SIMULA TIONS OF MEMRISTORS, MEMCAP ACITORS . . .
Ch is the heat capacitance, δ is the heat dissipation constant,
Tr is the ambient temperature, θ[.] is the step function, Tm
is the melting point, Tx is the glass transition point, α and β
are constant deﬁning crystallization and amorphization rates,
respectively,Vt is the threshold voltage, Ron and Roff are lim-
iting values of memristance, andV0 is parameter determining
the shape of I−V curve.
Features: This simple model takes into account crys-
tallization (when T > Tm) and amorphization (when Tm >
T > Tx) processes neglecting, however, a negative differ-
ential resistance region close to the threshold voltage Vt.
Although this region can be straightforwardly incorporated
into the model (written in the current-controlled form), it is
not important for the memory cell operation (reading/writ-
ing voltages are always beyond that region). Several other
approaches to model PCM cells in SPICE are available
[41, 42, 43].
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
 
Fig. 6. Model of phase change memristive system for SPICE implementation. 
 
onR
minus
plus
I
CxCint auxCxR
resE
CxG
100MΩ
Cx
1F IC=Cxini
VM I
e
RRCV
V
VV
onoff
x trM
1
))(1(
0 +
−− −
TCint auxTRTG
100MΩ
T
))(()())(())(())(1( mxmxx TTVCVTVTTTVCV −−−−− θβθθα
))(( TVTIV rM −+ δ
{Ch} IC=Tini
Fig. 6. Model of phase change memristive system for SPICE im-
plementation.
The schematic in Fig. 6 represents three submodels of
the phase change memory: the submodel of the resistive port
(Ron, Eres) according to (19) and (22), and submodels of inte-
grators for computing the temperature (GT , CintT , RauxT ) and
Cx (GCx, CintCx, RauxCx) according to (20) and (21). Note that
the power V 2
M/R in (20) dissipated on the memristive port
can be also computed as a product of voltage and current as
shown in Fig. 6.
Results: The transient analysis results provided by
PSpice code from Supplementary Materials 3 are given in
Fig. 7. The 4 V/300 ns voltage pulse sets the temperature to
ca 339◦C, i.e. above the crystallization temperature, which
causes the transition to the crystalline phase (see the transi-
tion in Cx from 0 to 1). The second 6 V/100 ns pulse sets the
temperature to ca 739◦C, which is above the melting point,
and the crystalline fraction Cx drops close to zero.
 
 
 
Fig. 7. PSpice results of transient analysis of PCM excited by voltage pulses V(1). 
  
           Time
0s 200ns 400ns 600ns
1  V(1) 2  V(Xmem.T) 3  V(Xmem.Cx)
0V
5V
10V1
 
0V
200V
400V
600V
800V2
0V
0.5V
1.0V3
 
   >>
Fig. 7. PSpice results of transient analysis of PCM excited by
voltage pulses V(1).
3.4 Model R.4: Insulator-To-Metal Transition
Memristive System
Model: A model [44] of insulator-to-metal phase tran-
sition device employs the metallic phase fraction expressed
in radial coordinates, u = rmet/rch, as an internal state vari-
able. The model equations are
V = Rch(u)I (23)
du
dt =
(d∆H
du
)−1 (
Rch(u)I2− Γth(u)∆T
)
(24)
where
Rch(u) = ρinsL
πr2
ch
[
1 +
( ρins
ρmet
− 1
)
u2
]−1
, (25)
Γth(u) = 2πLκ
(
ln1
u
)−1
, (26)
d∆H
du = πLr2
ch
[
ˆcp∆T 1− u2 + 2u2lnu
2u(lnu)2 + 2∆ˆhtru
]
. (27)
Here, rmet is the radius of metallic core,rch is the conduction
channel radius, H is the enthalpy, Γth is the thermal con-
ductance of the insulating shell, ρins is the insulating phase
electrical resistivity, ρmet is the metallic phase electrical re-
sistivity, L is the conduction channel length, κ is the ther-
mal conductivity, ˆcp is the volumetric heat capacity, ∆ˆhtr is
the volumetric enthalpy of transformation. Typical values of
model parameters can be found in [44].
Features: This model describes unipolar current-
controlled memristive device based on a thermally-driven
insulator-to-metal phase transition. As demonstrated in [44],
it provides realistic modeling of complex dynamic behavior
of the device including sub-nanosecond switching times. On
the other hand, the structure of (26) and (27), containing log-
arithms of the phase composition state variable u, divisions

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 955
by u, and divisions by logarithm of u, where u can vary be-
tween 0 and 1, indicates potential numerical problems. To
prevent them, it is useful to provide artiﬁcial limitations of
the variable u in SPICE code.
Fig. 8
plus see Eq. (24)
R
I
CG G
10GΩ
u
1pF 
dt
du1210−
fixR
minus
uC
auxRvarG
uG
V
VuVG ))((var IC=uini
see Eq. (30)
Fig. 8. Model of phase change memristive system for SPICE im-
plementation.
Equations (23) and (25) can be rewritten in the form
I = R−1
ﬁxV + Gvar(u)V, (28)
Rﬁx = ρinsL
πr2
ch
, (29)
Gvar(u) = πr2
ch
L
( 1
ρmet
− 1
ρins
)
u2. (30)
The corresponding modeling of the memristive port via
a parallel combination of a resistorR f ix and a controlled cur-
rent source Gvar is shown in Fig. 8. The variable u is found
through the integration of the right-side of (24) using a ca-
pacitor Cu which is charged by a current source Gu. Since
the time derivatives of u come up to high values, a proper
scaling by the factor of 10−12 is provided according to Fig. 8
to prevent convergence problems.
Fig. 9
VDC 18 V
RL
4.2k
Re
2.7k
XIMTM
1 2 3
VDC 1.8V
Rscope
50Cp 23p
XIMTM
40
Fig. 9. Insulator-to-metal transition memristive system
(XIMTM) as a part of the relaxation oscillator [44].
Results: For demonstrating the features of the corre-
sponding SPICE model R.4 in Supplementary Materials 4,
the simulation of the experimental Pearson-Anson relaxation
oscillator, described in [44], has been performed. As shown
in Fig. 9, the oxide switch is used here as current-controlled
NDR (Negative Differential Resistor) element. The simula-
tion outputs in Fig. 10 correspond to the results originally
published in [44].
Fig. 10
200uA
300uA1
 
400mV
600mV2
0A
100uA
0V
200mV
   >>
400uA1 600mV2
           Time
9.761us 9.762us 9.763us 9.764us 9.765us
1  I(XIMTM.Vsense) 2  V(XIMTM.u)
0A 0V
V(XIMTM.u) (a)
200uA
 
200mV
400mV
 
           Time
8.0us 8.5us 9.0us 9.5us 10.0us
1  I(XIMTM.Vsense) 2  V(XIMTM.u)
0A
SEL>>
0V
SEL>>
(b)
Fig. 10. Transient analysis of circuit from Fig. 9 in PSpice: cur-
rent pulses through the memristive system (solid lines),
phase composition state variable u (dashed lines).
4. SPICE Modeling of Memcapacitive
Devices
4.1 Model C.1: Ideal Memcapacitor
Model: A voltage-controlled memcapacitor is deﬁned
by [1]
q = C (φ(t))VC (31)
where
φ(t) =
t∫
0
VC(τ)dτ (32)
is the ”ﬂux”. From application point of view, a memcapac-
itor switching between two limiting values of memcapaci-
tance would be of value. This property is achieved, for exam-
ple, in the following model resembling the memristor model
given by (10)
C(φ(t)) = Clow + Chigh−Clow
e−4k(φ(t)+φ0) + 1 (33)
where Clow and Chigh are limiting values of memcapacitance
(Clow < Chigh), k is a constant and φ0 is a constant deﬁning
the initial value of the capacitance Cini = C(φ = 0). In terms
of the initial capacitance, (33) can be rewritten as follows:
C(φ(t)) = Clow + Chigh−Clow
ae−4kφ(t) + 1 , a = Chigh−Cini
Cini−Clow
. (34)
Features: The positive aspects of (34) model include
its simplicity and switching between two limiting values.

956 D. BIOLEK, M. DI VENTRA, Y . V . PERSHIN, RELIABLE SPICE SIMULA TIONS OF MEMRISTORS, MEMCAP ACITORS . . .
Among the negative ones we note a lack of switching thresh-
old, sensitivity to ﬂuctuations, over-delayed switching [35],
and a possibility of active behavior [1].
Fig. 11
l
see Eq. (34)
Q
VphiVC *))((
plus
phi
V
QE
minus
intC
auxR
capG
vG
100MΩ
V
))(( QVddt
1F
Fig. 11. Model of ideal memcapacitor from Section 4.1.
The memcapacitor can be modeled as shown in Fig. 11.
The ﬂux is computed as an integral of terminal voltageV : the
controlled source Gv whose current is equal to the voltage V
charges the capacitor Cint, thus the voltage of the node phi
is equal to the ﬂux. This ﬂux is then used to compute the
memcapacitance according to (34). The charge is provided
as a voltage of node Q of the controlled voltage source EQ.
In such a way, the charge is available as a simulation result
for inspection, without a necessity of its subsequent compu-
tation from the terminal current. The charge is then used for
evaluating the terminal current via time-domain differentia-
tion (see the source Gcap).
Note that in the simulation programs, which provide
the feature of direct modeling of the charge sources (e.g. Or-
CAD PSpice v. 16, HSPICE, Micro-Cap), the source Gcap
can be implemented via this kind of source without the use of
ddt operation (see the codes in Supplementary Materials 5).
In case of need, the memcapacitive port can be also mod-
eled as a parallel connection of a ﬁxed capacitor Clow and
a variable capacitor according to (34).
Results: The subcircuit of ideal memcapacitor from
Supplementary Materials 5, based on the model from
Fig. 11, is used for simulating hard-switching phenomena
which appear when exciting the memcapacitor with the pa-
rameters given in SPICE code of this subcircuit by 1 V/1 Hz
sinusoidal voltage source. Figure 12 shows the PSpice out-
puts.
For checking the accuracy of the computation, several
criteria can be used, for example the rule of the immedi-
ate steady state. HSPICE provides the best results for Gear
method and with the options RUNLVL=0 and LVLTIM=1.
4.2 Model C.2: Multilayer Memcapacitive
System
Model: In a multilayer memcapacitive system, several
metal layers are embedded into the dielectric medium sepa-
rating capacitor plates [45]. Here, we consider the simplest
Fig. 12
100pV
(a)
-100pV
0V
SEL>>
100p1
 
20nA2
 
           V(1)
-1.0V -0.5V 0V 0.5V 1.0V
V(XMC.Q)
p
(b)
50p
0A
10nA
()
1.0V1
 
100pV2
 
1  V(XMC.Q)/v(1) 2  -I(Vin)
0
   >>
-10nA
(c)
0V 0V
()
           Time
0s 50ms 100ms 150ms 200ms
1  V(1) 2  V(XMC.Q)
-1.0V
   >>
-100pV
Fig. 12. Transient analysis of the ideal memcapacitor using
Fig. 11 model: (a) pinched hysteresis loop, (b) memca-
pacitance (dashed blue line) and terminal current (solid
red line), (c) terminal voltage (solid blue line) and
charge (dashed red line).
realization of such system involving two internal metal lay-
ers, which can be described as a ﬁrst-order charge-controlled
memcapacitive system [45]:
VC = C−1(Q,q)q, (35)
dQ
dt = I12 (36)
where
C(Q,q) = C0
1 + δ
d
Q
q
, (37)
I12 = S e
2πhδ2
[(
U− eV1
2
)
e− 4πδ
√
2m
h
√
U− eV1
2 −
−
(
U + eV1
2
)
e− 4πδk
√
2m
h
√
U+ eV1
2
]
(38)
if eV1 < U, and
I12 = S e3V 2
1
4πhUδ2
[
e− 4πδ√mU3/2
ehV1 −
−
(
1 + 2eV1
U
)
e− 4πδ√mU3/2
ehV1
√
1+ 2eV1
U
]
(39)

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 957
if eV1 > U. Here,
V1 = (q + Q)δ/(Sε0εr) (40)
is the voltage drop across internal layers, Q is the internal
layer charge, S is the plate area, d is the distance between
plates, δ is the distance between internal layers placed sym-
metrically between the plates, ε0 is the vacuum permittivity,
εr is the relative dielectric constant of the insulating material,
U is the potential barrier height between two internal metal
layers, m and e are electron mass and charge, respectively, h
is the Planck constant, and C0 = ε0εrS/d is the capacitance
of the system without internal metal layers. Note that (38)
and (39) are given for V1 > 0. For V1 < 0, the sign of I12
should be changed and|V1| should be used in (38), (39).
 
  
plus
minus
1C
2C
VC
dt
dQI =12
I
dt
dqI =
I
I2
I2 V1
GQ
Fig. 13. Model of two-layer memcapacitive system described by
(35)-(40).
Features: Multilayer memcapacitive system is an ex-
ample of memory device with the possibility of zero and neg-
ative response [35]. As such, hysteresis curves of this device
may not pass through the origin [45, 35]. It is shown in [45]
that the multilayer memcapacitive system can be modeled
by an equivalent circuit, consisting of linear capacitors and
nonlinear resistors. For the case of two layers, such circuit is
modiﬁed to the form in Fig. 13, with nonlinear resistor mod-
eled via a controlled current source GQ. It can be shown that
if capacitances C1 and C2 are set to values
C1 = ε0εrS
d− δ = C0
1− δ/d , C2 = ε0εrS
δ = C0
δ/d (41)
and if the current ﬂowing through the source GQ is I12, given
by (38) and (39), then the circuit in Fig. 13 behaves as mem-
capacitive system with the memcapacitance given by (37),
and that the voltage across C2 is the voltage (40) across the
internal layers. Then I2 = I− I12 = d(q− Q)/dt and thus
C2 is charged to the charge q− Q. The voltage V1 will be
(q− Q)/C2 which gives (40). The sum of voltages across
C1 and C2 is VC = q/C(Q,q) = q/C1 + (q− Q)/C2. After
substituting (41) we get the formulae (37) for the memca-
pacitance.
The current I12 from (38) and (39), representing formu-
lae for current-voltage characteristic of electric tunnel junc-
tion, takes the values from a large dynamic range which ex-
ceeds the numerical limits of SPICE-family simulation pro-
grams. For typical numerical values given in Supplemen-
tary Materials 6, I12 is of about 10 −127 for eV1/U = 0.1,
10−116 for eV1/U = 1, 10−56 for eV1/U = 2, and 10 −6
for eV1/U = 10. It turns out that the low-voltage range
eV1 < U (38) generates the currents much below the numer-
ical threshold of SPICE, and that the ﬁrst term of (39) ap-
proximates well the I12 versus V1 dependence in the form
I12≈ aV1|V1|e
− b
|V1| , a = Se3
4πhUδ2 , b = 4πδ√mU
3
2
eh (42)
both for positive and negative values ofV1. The SPICE codes
presented below can be easily modiﬁed to include the second
term of (39) if required.
To prevent numerical underﬂow, it is useful to com-
pute logarithm of I12 from (42), to limit artiﬁcially its range,
and then to compute I12 via inverse logarithm from this lim-
ited values. Examples of the corresponding SPICE codes,
providing reliable computation, are given in Supplementary
Materials 6. Note that due to undocumented errors in Or-
CAD PSpice v. 16 and HSPICE, they handle incorrectly nu-
merical parameters which underﬂow the limit of ca 10−30. In
this model, such parameters are electron mass m and Planck
constant h. That is why the codes for PSpice and HSPICE
are modiﬁed accordingly for computing auxiliary variables
a and b from (42) which depend on these quantities.
Results: The SPICE codes from Supplementary Ma-
terials 6 can provide all the simulation results from [45].
Figure 14 conﬁrms the nonpinched charge-voltage hysteresis
loop. This model enables studying all the interesting phe-
nomena described in [45], including frequency dependent
hysteresis, diverging and negative capacitance.
4.3 Model C.3: Bistable Membrane
Memcapacitive System
Model: The model of bistable membrane memcapaci-
tive system [46] is speciﬁed by
q(t) = C(y)V (t), (43)
dy
dτ = ˙y, (44)
d ˙y
dτ = −4π2 y
(( y
y0
)2
− 1
)
− Γ ˙y−
( β(τ)
1 + y
)2
(45)
where
C(y) = C0
1 + y , (46)
y0 = z0/d, Γ = 2π γ/ω0, β(t) = [2π/ (ω0 d)]
√
C0/ (2m)V (t)
and time derivatives are taken with respect to the dimen-
sionless time τ = t ω0/ (2π). Here, ±z0 are the equilibrium
positions of the membrane, d is the separation between the
bottom plate and middle position of the ﬂexible membrane,

958 D. BIOLEK, M. DI VENTRA, Y . V . PERSHIN, RELIABLE SPICE SIMULA TIONS OF MEMRISTORS, MEMCAP ACITORS . . .
Fig. 140V
1.0uV
(a)
1.0u
           V(2)
-8.0V -4.0V 0V 4.0V 8.0V
V(Q)
-1.0uV
SEL>>
0
(b)
0A
500uA
0A
500uA2
 
V(Q) S(I(XMC.GQ))
-1.0u
(c)
10V
1  -I(Vin) 2  I(XMC.GQ)
-500uA
0A
-500uA
0A
   >>
0V
(d)
           Time
20ms 25ms 30ms 35ms 40ms 45ms 50ms
V(2)
-10V
Fig. 14. Transient analysis of memcapacitive system from
Fig. 13 which is driven by sinusoidal 7.5 V/100 Hz volt-
age source with 1Ω serial resistance, (a) charge-voltage
hysteresis loop, (b) memcapacitor charge (solid blue)
and charge of the internal layers (dashed red), (c) termi-
nal current (solid red) and current I12 (dashed blue), (d)
exciting voltage.
γ is the damping constant, ω0 is the natural angular fre-
quency of the system, m is the mass of the membrane and
C0 = ε0 S/d. The dimensionless membrane displacement y
and membrane’s velocity ˙y play the role of the internal state
variables.
Features: This model describes a memcapacitive de-
vice with two well-deﬁned equilibrium states ideally suited
for binary applications. In order to model reliably the mem-
capacitive port, (43) and (46) are arranged to the form
V (t) = 1
C0
q(t) + y
C0
q(t), (47)
which represents the serial connection of two capacitors,
with ﬁxed capacitance C0 and with the capacitance depen-
dent on the variabley (the fact that y can take negative values
does not cause any problems). The second one is modeled
in Fig. 15 via a controlled voltage source Ec. The charge,
which is necessary for computing the source voltage, can be
obtained by integrating the terminal current, or more con-
veniently, it is directly the product of voltage across the ca-
pacitor C0 and its capacitance. The charge value is available
as a voltage of the voltage source EQ. Two classical inte-
grator circuits provide the computation of y and ˙y quantities
according to (44) and (45), representing them as voltages of
nodes y and yd. Surprisingly, HSPICE provides low preci-
sion of the simulated waveforms with this model. The pre-
cision is considerably increased after modeling the variable
part of the memcapacitive port directly by a capacitor with
formula-controlled capacitance (see the Supplementary Ma-
terials 7).
Fig. 15
Q
plus
0C
C0 V(plus,c)QE
100MΩ1F
)( ydV
0C
c
y
)()( QVyVE
yC yRyG
see Eq. (45)
minus
V
100MΩ1F
yd
0
)()(
C
QVyV
cE
IC=y0
minus
ydC ydRydG IC=yd0
Fig. 15. Model of bistable membrane memcapacitive system de-
scribed by (43)-(46).
Results: Figure 16 shows some outputs of PSpice tran-
sient analysis of bistable memcapacitive device under the si-
nusoidal excitation. The simulation model conﬁrms all the
phenomena which are analyzed in [46], including the fact
that the hysteresis is seen at intermediate frequencies com-
pared to the natural frequency of the system. This model
also offers the ability to analyze the dynamics of membrane
under the voltage pulse excitation. In addition, the chaotic
behavior of the device can be observed under the conditions
speciﬁed in [46].
4.4 Model C.4: Bipolar Memcapacitive System
with Threshold
Model: Here we consider a generic model of memca-
pacitive devices with threshold. This model is formulated
similarly to the model of memristive device with threshold
(Section 3.2) proved to be useful in many cases. We assume
that the memcapacitanceC plays the role of the internal state
variable x, namely, x≡ C, deﬁning the device state via the
following equations
q = xVC, (48)
dx
dt = f (VC)W (x,VC) (49)
where f (.) is a function modeling the device threshold prop-
erty (see Fig. 3) and W (.) is a window function:

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 959
Fig. 16
40pV
80pV
(a)
0V
-80pV
-40pV
SEL>>
4.0V1
 
80pV2
 
           V(2)
-3.0V -2.0V -1.0V -0.0V 1.0V 2.0V 3.0V
V(XMC.Q)
80pV
(b)
0V
2.0V
0V
40pV
-2.0V -40pV
           Time
16s 17s 18s 19s 20s
1  V(1) V(XMC.y) 2  V(XMC.Q)
-4.0V -80pV
   >>
Fig. 16. Transient analysis of bistable elastic memcapacitive
system from Fig. 15 in the periodical steady state un-
der conditions deﬁned in SPICE codes in Supplemen-
tary Materials 7: (a) charge-voltage pinched hysteresis
loop, (b) exciting sinusoidal voltage (dashed blue line),
membrane position y (green line), memcapacitor charge
(red line).
f (VC) = β (VC− 0.5 [|VC +Vt|−| VC−Vt|]) , (50)
W (x,VC) = θ (VC) θ
(
Chigh− x
)
+ θ (−VC) θ (x−Clow) .(51)
Here θ(·) is the step function, β is a positive constant charac-
terizing the rate of memcapacitance change when|VC| > Vt,
Vt is the threshold voltage, and Clow and Chigh are limiting
values of the memcapacitance C. In (51), the role of θ-
functions is to conﬁne the memcapacitance change to the
interval between Clow and Chigh.
Features: The threshold property is not only
a widespread attribute of many physical devices but also an
attractive feature from the application point of view. While
the present model is formulated without keeping any speciﬁc
memcapacitive device in mind, its structure is closely related
to the model of bipolar memristive devices with threshold
and thus can describe a memcapacitive component of such
devices, which might be the major one in properly designed
structures. The positive aspects of the present model include
the existence of the switching threshold and limiting values
Fig. 17 (a) Fig. 17 (b)
plus
Q
V(x)*VC
(a)
CG 1F    
100MΩ
)),(()( CC VxVWVf x
QE
VC
C
IC=Cinit
100MΩ
minus
xC
xRxG))(( QVddt
Q(b)
QC QRQG
100MΩ1Fplus
Q
CI
CI(b)
Q QQ
100MΩ1F
x
)(
)(
V
QV
cE
)),(()( CC VxVWVf
minus xC xRxG
)(xV
IC=Cinit
VC
Fig. 17. Two equivalent models of the memcapacitive device
with threshold.
of memcapacitance. We note, however, that such a model
may, in some cases, result in an active device behavior.
Fig. 17 shows two possible models based on (48)-(51).
Both of them compute uniformly the state variable x via in-
tegrating (49) (see Gx, Cx, Rx). In the model (a), charge
is computed as a product of memcapacitor voltage VC and
memcapacitance which is represented by the voltage V (x)
(see the controlled source EQ). The memcapacitor current,
i.e. time derivative of the charge, is provided by the con-
trolled current source GC. The model (b) avoids the differ-
entiation: the charge is computed via integrating the current
IC ﬂowing through the memcapacitive port, and the terminal
voltage is computed as a ratio of the charge and capacitance.
The division byV (x) is not dangerous since the denominator
is changing within the limits from Clow to Chigh.
Both models provide good results in PSpice and LT-
spice. However, simulations in HSPICE are accompanied
by serious accuracy (model (a)) and convergence (model
(b)) problems. Their nature probably consists in undocu-
mented problems in HSPICE Version A-2008.03. They can
be overcome via running the HSPICE-RF simulator from
the software package instead of HSPICE. The Supplemen-
tary Materials 8 provides PSpice and LTspice codes based
on the model in Fig. 17 (b), and HSPICE code for the same
model which can be run on HSPICE-RF. Fig. 18 shows the
simulation results from PSpice, demonstrating the periodi-
cal switching of the memcapacitance betweenClow and Chigh
states.

960 D. BIOLEK, M. DI VENTRA, Y . V . PERSHIN, RELIABLE SPICE SIMULA TIONS OF MEMRISTORS, MEMCAP ACITORS . . .
500pV
Fig. 18
(a)
0V
SEL>>
()
100uA
           V(2)
-5.0V 0V 5.0V
V(Xmem.Q)
-500pV
SEL>>
0A(b)
4.0V1
 
500pV2
 
120pV3
 
I(Xmem.Gx)
-100uA
0V 0V
40pV
80pV
(c)
           Time
20us 40us 60us 80us 100us
1  V(2) 2  V(Xmem.Q) 3  V(Xmem.x)
-4.0V -500pV 0V
   >>
Fig. 18. Transient analysis of the model from Fig. 17(b). Mem-
capacitive device with threshold voltage Vt = 3 V is
driven by sinusoidal 4 V/50 kHz signal: (a) charge-
voltage pinched hysteresis loop, (b) time derivative
of the memcapacitance (i.e. current charging Cx in
Fig. 17), (c) exciting voltage (blue dashed line), memca-
pacitor charge (red line), memcapacitance (green line).
5. SPICE Modeling of Meminductive
Devices
5.1 Model L.1: Ideal Meminductor
Fig. 17
IQVL *))((
plus
see Eq. (52)
phi
IQVL ))((
E 100MΩ
Q
1F
I
phiEI
minus
intC
auxR
LE
QGV
)) ( (phi V ddt
1F
Fig. 19. Ideal meminductor implementation in SPICE.
Model: A current-controlled meminductor is deﬁned
as [1]
φ = L(q(t))I (52)
Fig. 18
0V
50uV
(a)
-50uV
0V
SEL>>
4.0mV1
 
20m2
           I(Iin)
-5.0mA 0A 5.0mA
V(XMC.phi)
(b)
0V 10m
(b)
5.0mA1
 
50uV2
 
1  V(1) 2  V(XMC.phi)/ I(Iin)
-4.0mV 0
   >>
0A 0V
(c)
          Time
0s 50ms 100ms 150ms 200ms
1  I(Iin) 2  V(XMC.phi)
-5.0mA -50uV
   >>
Fig. 20. Transient analysis of meminductor from Fig. 19: (a)
pinched hysteresis loop, (b) meminductance (dashed
blue line) and terminal voltage (solid red line), (c) ter-
minal current (solid blue line) and ﬂux (dashed red
line).
where the charge q(t) is the integral of the current. From
application point of view, a meminductor switching between
two limiting values of meminductance is desirable. Similarly
to (10) and (33), we formulate a model of such meminductor
as
L(q(t)) = Llow + Lhigh− Llow
e−4k(q(t)+q0) + 1 (53)
where Llow and Lhigh are limiting values of meminductance
(Llow < Lhigh). The meminductance can be derived also as
a function of the initial inductance Lini = L(q = 0):
L(q(t)) = Llow + Lhigh− Llow
ae−4kq(t) + 1 , a = Lhigh− Lini
Lini− Llow
(54)
Features: Positive aspects of (54) model include
its simplicity and switching between two limiting values.
Among the negative ones we note a lack of switching thresh-
old, sensitivity to ﬂuctuations, over-delayed switching [35],
and the possibility of active behavior [1]. The meminductor
can be modeled in a similar way as the memcapacitor from
Section 4.1, see Fig. 19. The port current I is integrated into
the voltage of node Q, representing the charge. According

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 961
to (52) and (54), the ﬂux is evaluated as the voltage of the
controlled voltage source Ephi. This voltage is then used for
computing the terminal voltage via time-domain differenti-
ation (see the source EL). Note that in the simulation pro-
grams, which provide the feature of direct modeling of the
ﬂux sources (e.g. OrCAD PSpice v. 16, HSPICE, Micro-
Cap), the source EL can be implemented via this kind of
source without the use of ddt operation (see the codes in
Supplementary Materials 9). If necessary, the meminductive
port can be also modeled as a serial connection of a ﬁxed
inductor Llow and a variable inductor according to (54).
Results: Results of the transient analysis in PSpice in
Fig. 20 were obtained from the code in Supplementary Ma-
terials 9. The meminductor is driven by the ideal current
source, generating sinusoidal 5 mA/10 Hz waveform. The
simulation results exhibit all basic ﬁngerprints of the memin-
ductor, i.e. odd-symmetric ﬂux-current pinched hysteresis
loop and its high-frequency shrinking property, unambigu-
ous meminductance-charge state map, etc.
5.2 Model L.2: Effective Meminductive System
12
L
R
CL2 C
M =
L1
Fig. 13. Flux-controlled meminductive system based on the inductive
coupling of a coil L1 with a LCR contour [42]. Here, the mutual inductance
M is equal to k√L1L2, where 0≤k≤1 is the coupling coefﬁcient.
Fig. 14. Steady-state transient analysis of system from Fig. 13: (a)
Meminductance vs. current according to Eq. (47), (b) nonpinched ﬂux-current
hysteresis loop, (c) ﬂux (red line) and terminal current (blue line), (d) currents
through L1 (solid red line) and L2 (dashed red line) and voltage across L1
(blue line).
B. Model L.2: Effective meminductive system
Model: Let us consider an example of an effective memin-
ductive system that can be realized using traditional circuit
elements [42]. It consists of an LCR contour inductively
coupled to an inductor as shown in Fig. 13. In this scheme, two
inductorsL1 andL2 interact with each other magnetically. The
charge on the capacitor C and the current through the inductor
L2 play the role of internal state variables, namely, x1 =qC
and x2 =IL2. The system is described by
φ = L (x2,I )I, (44)
dx1
dt = −x2, (45)
dx2
dt = 1
L2
(x1
C −Rx2−M dI
dt
)
, (46)
where
L (x2,I ) =L1 +Mx2
I . (47)
Features: The circuit sketched in Fig. 13 does not offer non-
volatile information storage and has certain similarities with
elastic memcapacitive systems [43]. Additional functionalities
open if the resistor or capacitor (or both) is replaced by a
memristive or memcapacitive system, respectively. We note
that although dI/dt enters into the right-hand-side of Eq. (46)
and thus this equation differs from the canonical equations of
meminductive systems [1], such a deﬁnition of meminductive
system can be considered as a reduced (effective) one [44] that
can be written in the canonical form using additional internal
state variables [44].
Results: Since the circuit in Fig. 13 is a simple linear
dynamical system containing conventional passive elements,
its SPICE modeling does not require any special approach.
Figure 14 shows some results of PSpice transient analysis.
The inductor L1 is driven by a current source with sinusoidal
1mA/100kHz waveform. Since x2 = I(L2), the effective
meminductance according to Eq. (47) depends on the ratio
of currents ﬂowing through inductors L2 andL1. It is obvious
from the waveforms I(L1) and I(L2) in Fig. 14 (d) that the
meminductance can take inﬁnite values when I(L1) crosses
zero level and that both positive and negative values can be
possible. This fact is conﬁrmed in Fig. 14 (a). Figure 14
(c) shows that, due to the frequency dependent phase shift
between ﬂux and exciting current, the zero-crossing points of
these waveforms are not identical, and thus the ﬂux-current
hysteresis loop in Fig. 14 (b) cannot be pinched.
VI. C ONCLUSIONS
APPENDIX A
SPICE CODES FOR MODEL R.1
PSpice and LTspice code
.subckt memristorR1 plus minus params: Ron=100 Roff=10k Rini=5k
.param uv=10f D=10n k={uv*Ron/D**2} a={(Rini-Ron)/(Roff-Rini)}
*model of memristive port
Roff plus aux {Roff}
Eres aux minus value={(Ron-Roff)/(1+a*exp(-4*k*V(q)))*I(Eres)}
*end of the model of memristive port
*integrator model
GQ 0 Q value={i(Eres)}
Cint Q 0 1
Raux Q 0 100meg
*end of integrator model
*alternative integrator model; SDT function for PSpice must be replaced by IDT for LTspice
;Eq Q 0 value={SDT(I(Eres))}
.ends memristorR1
.options method=gear ;use only for LTspice
Vin in 0 sin 0 1 1
Xmem in 0 memristorR1
.tran 0 20 0 1m; for LTspice, 1m can be replaced by larger step ceiling (up to 200m)
.probe
.end
Fig. 21. Flux-controlled meminductive system based on the in-
ductive coupling of a coil L1 with a LCR contour [47].
Here, the mutual inductance M is equal to k√L1L2,
where 0≤ k≤ 1 is the coupling coefﬁcient.
Model: Let us consider an example of an effective me-
minductive system that can be realized using traditional cir-
cuit elements [47]. It consists of an LCR contour induc-
tively coupled to an inductor as shown in Fig. 21. In this
scheme, two inductors L1 and L2 interact with each other
magnetically. The charge on the capacitor C and the current
through the inductor L2 play the role of internal state vari-
ables, namely, x1 = qC and x2 = IL2. The system is described
by
φ = L (x2,I)I, (55)
dx1
dt = −x2, (56)
dx2
dt = 1
L2
(x1
C− Rx2− M dI
dt
)
(57)
where
L (x2,I) = L1 + M x2
I . (58)
Fig. 20
0
2.0m
(a)
           I(I)
-10uA -5uA 0A 5uA 10uA
V(flux)/I(L1)
-2.0m
SEL>>
0V
2.0nV
(b)
2.0nV1 1.0mA2
           I(I)
-1.0mA -0.5mA 0A 0.5mA 1.0mA
V(flux)
-2.0nV
()
1 V(fl ) 2 I(I)
-2.0nV
0V
 
-1.0mA
0A
 
   >>
(c)
0A
1.0mA1
 
0V
1.0mV2
 
1  V(flux) 2  I(I)
(d)
           Time
40us 45us 50us 55us 60us
1  I(L1) I(L2) 2  V(in)
-1.0mA -1.0mV
   >>
Fig. 22. Steady-state transient analysis of system from Fig. 21:
(a) Meminductance vs. current according to (58),
(b) nonpinched ﬂux-current hysteresis loop, (c) ﬂux
(red line) and terminal current (blue line), (d) currents
through L1 (solid red line) and L2 (dashed red line) and
voltage across L1 (blue line).
Features: The circuit sketched in Fig. 21 does not
offer non-volatile information storage and has certain sim-
ilarities with elastic memcapacitive systems [48]. Addi-
tional functionalities open if the resistor or capacitor (or
both) is replaced by a memristive or memcapacitive sys-
tem, respectively. We note that although d I/dt enters into
the right-hand-side of (57) and thus this equation differs
from the canonical equations of meminductive systems [1],
such a deﬁnition of meminductive system can be consid-
ered as a reduced (effective) one [12] that can be written in
the canonical form using additional internal state variables
[12].
Results: Since the circuit in Fig. 21 is a simple linear
dynamical system containing conventional passive elements,
its SPICE modeling does not require any special approach.
Figure 22 shows some results of PSpice transient analysis.
The inductor L1 is driven by a current source with sinusoidal
1 mA/100 kHz waveform. Since x2 = I(L2), the effective
meminductance according to (58) depends on the ratio of
currents ﬂowing through inductors L2 and L1. It is obvious
from the waveforms I(L1) and I(L2) in Fig. 22 (d) that the
meminductance can take inﬁnite values when I(L1) crosses
zero level and that both positive and negative values can be
possible. This fact is conﬁrmed in Fig. 22 (a). Figure 22 (c)
shows that, due to the frequency dependent phase shift be-

962 D. BIOLEK, M. DI VENTRA, Y . V . PERSHIN, RELIABLE SPICE SIMULA TIONS OF MEMRISTORS, MEMCAP ACITORS . . .
tween ﬂux and exciting current, the zero-crossing points of
these waveforms are not identical, and thus the ﬂux-current
hysteresis loop in Fig. 22 (b) cannot be pinched.
5.3 Model L.3: Bipolar Meminductive System
with Threshold
Model: Here we consider a generic model of memin-
ductive devices with current threshold. This model is for-
mulated similarly to the model of memristive device with
threshold proved to be useful in many cases. We assume
that the meminductance L plays the role of the internal state
variable x, namely, x≡ L, deﬁning the device state via the
following equations
φ = LI, (59)
dx
dt = f (I)W (x,I) (60)
where f (.) is a function modeling the device threshold prop-
erty (see Fig. 3) and W (.) is a window function:
f (I) = β (I− 0.5 [|I + It|−| I− It|]) , (61)
W (x,I) = θ (I) θ
(
Lhigh− x
)
+ θ (−I) θ (x− Llow) . (62)
Here θ(·) is the step function, β is a positive constant charac-
terizing the rate of meminductance change when|I| > It, It is
the threshold current, and Llow and Lhigh are limiting values
of the meminductance L. In (62), the role of θ-functions is
to conﬁne the meminductance change to the interval between
Llow and Lhigh.
Features: The threshold property is not only
a widespread attribute of many physical devices but also an
attractive feature from the application point of view. The
present model, however, is formulated without keeping any
speciﬁc meminductive device in mind. The positive aspects
of this model include the existence of the switching threshold
and limiting values of meminductance. We note, however,
that such a model may, in some cases, result in an active
device behavior.
Two kinds of SPICE-oriented models of the memin-
ductive system with threshold are shown in Fig. 23(a) and
(b). In both cases, the state variable x, denoting the memin-
ductance, is represented by the voltage of the node x which
is computed via time-domain integration according to (60).
For model (a), the ﬂux is computed via the Ephi controlled
voltage source as a product of this meminductance and the
current I ﬂowing through the meminductive port. The port
voltage is then evaluated as time derivative of this ﬂux (see
the controlled voltage source EL). For model (b), the ﬂux
is computed via integration of the port voltage, and the port
current is derived as a ratio of the ﬂux and the meminduc-
tance, thus obeying the differentiation.
Fig. 22 (a) Fig. 22 (b)
plus
phi
V(x)*I
(a)
)),(()( IxVWIf
I
LE 1F 
100MΩ
x
phiE
VL
IC=Linit
100MΩ
minus
intC
auxRxG))(( phiVddt
hi(b)
phiC phiRphiG
100MΩ1Fplus
phi
LV
I
(b)
phi pphi
100MΩ1F
x
)(
)(
xV
phiV
LG
V
)),(()( IxVWIf
minus xC xRxG
)(xV
IC=Linit
VL
Fig. 23. Two equivalent models of the meminductive device
with threshold.
In PSpice and LTSpice, both models work well. How-
ever, HSPICE operates only with the model (a) whereas con-
vergence problems are reported for model (b). They can be
overcome after running HSPICE RF instead of HSPICE.
Supplementary Materials 11 summarizes SPICE codes for
more reliable model in Fig. 23(a). A demonstration of PSpice
outputs is shown in Fig. 24. It can be observed that the low
level of the meminductance is not Llow but it is preserved to
the initial value Linit (see Fig. 24 and SPICE code in Sup-
plementary Materials 11). The boundary value is switched
to Llow after increasing the magnitude of the exciting current
above a proper value.
6. Setting the Analysis Parameters
and SPICE Options
In this Section we discuss several rules for solving ac-
curacy and convergence problems in SPICE via tweaking
analysis parameters and global settings. The common rules
are described in a number of references including a couple
of excellent books [28, 29]. Some of the rules discussed be-
low are focused on the speciﬁcs of memelement simulation
within the transient analysis, which is most frequently used
for this type of components.
Incorrect modeling is a common source of the problems
burdening the transient analysis. The rules of building-up

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 963
2.0nV
Fig. 23(a)
0V
SEL>>
20A
           I(Isin)
-10uA -5uA -0uA 5uA 10uA-14uA 14uA
V(Xmem.phi)
-2.0nV
0A
(b)
20uA1
 
400uV2
 
100uV3
 
I(Xmem.Gx)
-20A
0A 0V
60uV
80uV(c)
           Time
40us 60us 80us 100us
1  I(Isin) 2  V(1) 3  
V(Xmem.x)
-20uA -400uV 40uV
   >>
Fig. 24. Transient analysis of the model from Fig. 23(a). Me-
minductive device with threshold current It = 10 µA
is driven by sinusoidal 12 µA/50 kHz signal: (a) ﬂux-
current pinched hysteresis loop, (b) time derivative of
the meminductance (i.e. current chargingCx in Fig. 23),
(c) exciting current (blue dashed line), meminductor
voltage (red line), meminductance (green line).
correct models of memsystems have been described in Sec-
tion 2.2, thus they will not be dealt with below. The prob-
lems appearing within the analysis can be of the following
two types. Convergence problems: SPICE does not ﬁnd the
solution (fatal problems indicating by error message). Ac-
curacy problems: The solution is found but it is modiﬁed by
errors (problems which can be hidden particularly if we have
no idea of the correct result). Since the attempts at increas-
ing the accuracy attracts the convergence problems, the tran-
sient analysis of systems requiring extremely high accuracy
can be considered as art of compromise. Ideal memelements
or memristive systems with threshold are typical representa-
tives of the above systems (see models R.1, R.2, C.1, C.4,
L.1 and L.3 in Sections 3-5). The above convergence and
accuracy problems, if they appear, must be handled in the
sequence as they are mentioned. If the circuit does not con-
verge, one cannot deal with the accuracy of the solution.
Note that the SPICE command for the transient analy-
sis can be in one of two basic forms:
. TRAN Tprint Tstop [ skipbp ]
(*)
or
. TRAN Tprint Tstop Tstart Hmax [ skipbp ] (**)
with an optional ﬂag skipbp or uic. In addition to the com-
mands (*), (**), the algorithms of the analysis can be af-
fected by the attributes deﬁned by the .OPTIONS command,
especially the error and other iteration criteria. The transient
analysis has two stages, the DC bias point calculation and the
timepoint sweep analysis. The analysis result depends on the
behavior of the numerical algorithms acting in both stages.
The ﬁrst stage can be skipped via the skipbp ﬂag although it
is not generally recommended [28].
Convergence aids for DC bias point computation
If SPICE fails to converge to a DC bias point, it aborts
the Newton-Raphson (NR) iteration and prints the error mes-
sage ”No convergence in DC operating point”. Note that
most simulation examples from Sections 3 to 5 with SPICE
codes from the Appendices, work without any convergence
problems, since their models were built up according to rules
from Section 2.2. The main difﬁculties are related to im-
plementations of C.4. and L.3 in HSPICE. Moreover, the
convergence strongly depends on application deteriorating
in circuits leading to large sets of equations. The suggested
sequence of the actions is summarized below.
1. Raise ITL1, i.e. the upper iteration limit of the Newton-
Raphson (NR) method from its default value 150 to 500
or more via the command
.OPTION ITL1=500
2. Via the .NODESET command, set the qualiﬁed estima-
tion of DC values of as many nodal voltages as possi-
ble.
3. Call the Source Stepping algorithm via the command
.OPTION ITL6=500
4. Increase the GMIN parameter above its default value
10−12 Ω−1, for example
.OPTION GMIN=1E-10
GMIN is estimated as reciprocal value of the smallest
parasitic resistance which could be placed across any
two nodes without inﬂuencing the model behavior [29].
5. Consider if the relative error of voltages and currents
can be higher than the default value 0.1 %. If yes, then
raise RELTOL:
.OPTION RELTOL=0.01
6. Determine the magnitude of the smallest voltage of in-
terest, e.g. 1uV , and compute the absolute voltage error
VNTOL=RELTOL*1u =1E-8. Then redeﬁne VNTOL
from its default value 1uV:
.OPTION VNTOL=1E-8
If you cannot estimate the smallest voltage, then use
the rule that VNTOL should be by 6 to 9 orders smaller
than the largest voltage in the circuit [28].
7. Determine the magnitude of the smallest current of in-
terest, e.g. 1uA, and compute the absolute current er-
ror ABSTOL=RELTOL*1u =1E-8. Then redeﬁne AB-
STOL from its default value 1pA:

964 D. BIOLEK, M. DI VENTRA, Y . V . PERSHIN, RELIABLE SPICE SIMULA TIONS OF MEMRISTORS, MEMCAP ACITORS . . .
.OPTION ABSTOL=1E-8
If you cannot estimate the smallest current, then use the
rule that ABSTOL should be by 6 to 9 orders smaller
than the largest current in the circuit [28].
8. If the above hints do not help, remove the skipbp from
the .TRAN command. If concrete nodal voltages can
be estimated, deﬁne them via .IC command
Note that steps 4-7 solve the convergence problems at
the expense of the accuracy. In addition to SPICE standard,
HSPICE offers additional convergence aids, particularly
”Modiﬁed Source-Stepping Algorithm” (MSSA), ”Gmin
Ramping” (GMR), and ”Pseudo-Transient Analysis” (PTA).
MSSA, which can be enabled via the .OPTION CONVER-
GENCE=3, can be used instead of step No. 3). GMR can
replace the step No. 4). It can be initiated as .OPTION
GRAMP=X where X is for example 6. PTA is an efﬁcient
generalization of the step No. 3). It can be activated via the
command .OPTION CONVERGENCE=1. Details are avail-
able in [30].
If PSpice fails to converge within ITL1 limit, the
Source Stepping Algorithm (SSA) is switched on automat-
ically, without a possibility of controlling this process by
the user. If SSA also fails to converge, the Gmin Step-
ping (ramping) can be initiated via the command .OPTION
STEPGMIN. This method is then applied ﬁrst, and if it will
not converge, PSpice comes to SSA algorithm. If LTspice
does not converge, it tries the algorithms of adaptive GMR,
adaptive SSA, and PTA in successive steps. The user can
deactivate individual algorithms from the queue via the cor-
responding ﬂags [32].
Convergence aids for timepoint sweep analysis
The DC bias solution is a starting point of the tran-
sient analysis which computes the solution at timepoints via
numerical integration of circuit equations. The methods of
the numerical integration used in SPICE are Backward Eu-
ler (BE), Trapezoidal (TRAP), and Gear (GEAR)). LTspice
offers TRAP, GEAR2 (i.e. second-order GEAR), a special
modiﬁcation of TRAP, and BE (it is initiated by undocu-
mented command .OPTIONS MAXORD=1). PSpice uses
only TRAP combined with BE. HSPICE provides TRAP
and GEAR of orders 1 to 6, with GEAR1 being the BE
method.
The circuit solution at each timepoint is found via the
NR iteration. The timepoints are not evenly spaced on the
time axis but their density is controlled via the TimeStep
Control (TSC) algorithm depending on how fast the circuit
voltages and currents are moving. The SPICE standard de-
ﬁnes two methods of timestep control, Iteration Count (IC)
and Local Truncation Error (LTE). In addition, HSPICE of-
fers the third method called DVDT Dynamic Timestep [30].
PSpice and LTspice use only LTE method.
The convergence problems appear as a consequence of
the simultaneous action of NR and TSC algorithms. They
are accompanied by ”Internal Timestep Too Small” or ”No
Convergence During Transient Analysis” error messages, in-
dicating that the solution was not found even though the
timestep reached its minimum allowable limit. In the ﬁrst
step, it should be checked if the improper model of the cir-
cuit is not the key source of convergence problems (see Sec-
tion 2.2). The other recommended steps are summarized be-
low.
1. Raise ITL4, i.e. the upper iteration limit at each time-
point, to 50 or more via the command
.OPTION ITL4=50
2. Select GEAR2 integration method (not for PSpice).
3. Loosen error criteria of NR algorithm according to
steps 5-7 from the Convergence aids for DC bias point
computation.
4. Increase TRTOL tentatively above its default value
(7 for HSPICE, 1 for LTspice).
Accuracy aids for transient analysis of memsystems
After resolving prospective convergence problems, the
options of NR and TSC algorithms can be tweaked to maxi-
mize the accuracy. Note that there are two fundamental lim-
its of the accuracy increase:
• numerical limits in the representation of voltages, cur-
rents, and system variable TIME as well as numerical
noise which can be ampliﬁed or accumulated by the
circuit model (see Section 2.2, Item 3),
• increase of the accuracy promotes the convergence
problems.
SPICE provides the following options for increasing the ac-
curacy of the transient analysis: Selection of the integration
method (not in PSpice), selection of the type of TSC algo-
rithm (not in PSpice and LTspice) and its parameters, selec-
tion of the parameters of the NR algorithm and .TRAN com-
mand options. In addition to the above tools, it is important
to ﬁnd a suitable guideline for checking the correctness and
the accuracy of the analysis of concrete systems. Demonstra-
tions of such guidelines, which start from the fundaments of
the analyzed memelements, in particular of ideal memristor
(R.1) and memcapacitor (C.1) or bipolar memristive system
(R.2) are given in Sections 3 and 4.
In virtue of the experience in SPICE simulation of as-
sorted types of memristive, memcapacitive and meminduc-
tive systems, the key factors inﬂuencing the accuracy of the
transient analysis are identiﬁed and summarized in the fol-
lowing steps.
1. Tighten RELTOL below its default value 0.001. Set the
other error criteria according to steps 6 and 7 from the
Convergence aids for DC bias point computation.
2. Analyze if the default value of Gmin=10 −12 does not
affect the accuracy. If possible, set Gmin=0 [28].

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 965
3. LTspice, HSPICE: Select GEAR2 as integration
method.
4. The parasitic ringing generated by TRAP method [29]
can be solved either by switching to GEAR2 or via step
No. 7.
5. The parasitic overshoot generated by GEAR2 method
[29] can be solved via step No. 7.
6. Accumulated errors (divergence from the correct solu-
tion during long transient run) [29] can be solved via
step No. 7.
7. Tighten maximum timestep Tmax (via parameter
Hmax or Tprint, see details below).
8. Tweaking the options of LTE algorithm of dynamic
timestep control [28] (via TRTOL or RELTOL, see de-
tails below).
9. HSPICE: Select the algorithm of dynamic timestep
control and its parameters [30] (see details below).
The recommendation 3) is based on the practice that
GEAR2 method is suitable for the analysis of memelements
of various natures. Since the models of memory systems
contain ideal integrators, GEAR2 is a good choice ow-
ing to its stable behavior when evaluating integrals of cir-
cuit quantities within many repeating periods. In addition,
GEAR2 provides good results for stiff systems where the
signals move too fast with respect to the actual timestep size.
Typical cases are voltage-controlled memcapacitive systems
or current-controlled meminductive systems where the port
quantities, namely the capacitor current and inductor volt-
age, are computed via numerical differentiation of control-
ling voltage and current. Examples are given in Sections 4
and 5 under the codes C.1 and L.1. Though the BE method
is the best for stiff systems, we should avoid it because it ac-
cumulates errors when analyzing integration blocks. PSpice
does not provide Gear integration. Fortunately, PSpice com-
bines TRAP with BE, this way eliminating trapezoidal oscil-
lations and its negative effects. For memelements with hard-
switching effects and other systems which exhibit fast signal
transitions, GEAR2 behaves well with regard to the accu-
mulated errors. Bipolar memristive system R.2 from Sec-
tion 3 is a typical representative of such systems exhibiting
the switching phenomena.
It turns out from the above that GEAR2 can be optimal
choice for memelements. The possible imperfections can be
suppressed by decreasing the maximum step size (see be-
low). On the other hand, Gear method may not provide the
best results, and the standard trapezoidal algorithm can solve
the task in some cases (see memristive systems R.3 and R.4,
memcapacitive systems C.2 and C.3, and meminductive sys-
tem L.2 in Sections 3 to 5). If we can select among the meth-
ods, then it is useful to try out the model behavior with all
the methods and to face the results with the expected wave-
forms.
After selecting the integration algorithm, increasing
the accuracy and eliminating the inherent parasitic behav-
ior of the method can be accomplished via tightening the
timestep. An indirect method of tightening the timestep
is decreasing the maximum timestep Tmax (see Item 7 in
the above steps). In PSpice and LTspice, which utilize the
LTE method of dynamic timestep control, Tmax is set as
Tmax=MIN(Tstop/50, Hmax). The extended syntax (**)
of the .TRAN command should be used with Hmax small
enough (e.g. Tstop/1000). In HSPICE, the stepsize control
is rather complicated. Tmax can be set via Tprint which ap-
pears in the simple syntax (*) of .TRAN command. Note
that it depends also on other ﬂags such as RMAX. HSPICE
also provides direct Tmax control via the ﬂag DELMAX.
See [30] for details.
If the LTE method of dynamic step control is used,
then the step size can be tightened directly via error crite-
ria, particularly TRTOL and RELTOL (see Item 8 in the
above steps). The size of the actual step is proportional to
the root of the product of TRTOL and RELTOL [29]. Tight-
ening RELTOL (see Item 1 in the above steps) improves
the precision of both NR and integration algorithms. Tight-
ening TRTOL reﬁnes only the integration method without
inﬂuencing NR algorithm. TRTOL default value is 7 for
PSpice and 1 for LTspice, thus LTspice should produce ca
2.6 times (root of 7) smaller timestep than PSpice. Even if
lowering TRTOL much below its default value is not gen-
erally recommended [28], this method can signiﬁcantly im-
prove the accuracy. Section III demonstrates one example
R.4 (Insulator-to-metal transition memristive system) where
TRTOL=0.1 provides the regime of enhanced precision for
LTspice. Similar effect can provide the option RELTOL=1u
for PSpice. Refer to [28] for more details about the accuracy
issue related to LTE method.
HSPICE offers inexhaustible options of improving
the accuracy of the analysis of memelements. It enables
combination of various integration methods, algorithms
of dynamic timestep control, and error criteria. In this
sense, it goes far beyond the SPICE standard. The so-
called RUNLVL algorithms with 6 discrete levels (1-fastest,
6-most accurate) can be used for simplifying the optimiza-
tion of transient analysis. These algorithms use LTE method
for dynamic timestep control. The command .OPTION
RUNLVL=6 is used in the source code for the simulation
of bipolar memristive system R.2 from Section 3 to provide
high precision of computing time instants of switching the
memristance states.
HSPICE provides excellent performance for complex
semiconductor devices but it sometimes fails when analyz-
ing behavioral models based on formulae and controlled
sources. Two examples are given in Sections 4 and 5 (bipo-
lar memcapacitive and meminductive systems with thresh-
old). The ”Golden Reference for Options” is recommended
for ﬁnding the acceptable trade-off between HSPICE accu-
racy and transient analysis simulation performance [49]:

966 D. BIOLEK, M. DI VENTRA, Y . V . PERSHIN, RELIABLE SPICE SIMULA TIONS OF MEMRISTORS, MEMCAP ACITORS . . .
. OPTION RUNLVL =6 ACCURATE KCLTEST
+ DELMAX =< something_small >
Via this option, DELMAX can be decreased tentatively in or-
der to acquire as accurate results as HSPICE allows (see the
HSPICE codes of threshold devices C.4 and L.3 in Appen-
dices 8 and 11). The ﬂag KCLTEST activates Kirchhoff’s
Current Law for every circuit node via tightening the error
criteria. Note that it was used for increasing the accuracy of
the simulation of meminductive threshold device L.3 (see the
Supplementary Materials 11). The ﬂag ACCURATE sets ad-
ditional HSPICE options to stricter tolerances. See [49] for
more details.
Although the LTE algorithm is allowed to be more pre-
cise than IC method of timestep control [28, 29], it gener-
ates inaccurate results for some types of circuits contain-
ing memelements. It relates to the circuits employing ideal
memristors, memcapacitors, and meminductors (see exam-
ples R.1, C.1, and L.1 in Sections 3 to 5). HSPICE controls
the timestep by means of a complicated mix of DVDT, IC
and LTE algorithms. The type of the method is set by the
ﬂag LVLTIM, but the RUNLVL algorithm must be disabled
ﬁrst via the command .OPTION RUNLVL=0. For circuits
containing ideal memelements, the DVDT algorithm in com-
bination with IC algorithm is the choice which provides most
accurate analysis. It can be set via the command .OPTION
LVLTIM=1 (see the HSPICE source codes for circuits R.1,
C.1, and L.1).
7. Conclusions
In summary, we have presented a coherent approach to
reliably simulate memristive, memcapacitive, and memin-
ductive systems in the SPICE environment. Apart from gen-
eral considerations on the “best practices” to carry out the
simulations for these particular devices, we have provided
a lot of examples for all three classes of memelements. For
the beneﬁt of the reader, we have also provided in the Ap-
pendices many codes of these models written in the most
popular SPICE versions (PSpice, LTspice, HSPICE) that can
be simply “cut and paste” in the appropriate environment for
immediate test and execution. Our goal would be accom-
plished if we could help researchers build from our own ex-
perience, avoid common pitfalls in the simulation of these
new devices, and venture into their own simulations.
Acknowledgements
This work has been partially supported by NSF grants
DMR-0802830 and ECCS-1202383, the Center for Mag-
netic Recording Research at UCSD, the SIX Research Cen-
ter of Sensor, Information and Communication Systems at
BUT, and by the development project K217 at UD.
References
[1] DI VENTRA, M., PERSHIN, Y . V ., CHUA, L. O. Circuit elements
with memory: Memristors, memcapacitors, and meminductors. Pro-
ceedings of the IEEE, 2009, vol. 97, no. 10, p. 1717 - 1724.
[2] DI VENTRA, M., PERSHIN, Y . V . The parallel approach. Nature
Physics, 2013, vol. 9, p. 200 - 202.
[3] ALIBART, F., PLEUTIN, S., GUERIN, D., NOVEMBRE, C.,
LENFANT, S., LMIMOUNI, K., GAMRAT, C., VUILLAUME, D.
An organic nanoparticle transistor behaving as a biological spik-
ing synapse. Advanced Functional Materials , 2010, vol. 20, no. 2,
p. 330 - 337.
[4] PERSHIN, Y . V ., DI VENTRA, M. Solving mazes with memris-
tors: a massively-parallel approach. Physical Review E , 2011, vol.
84, p. 046703.
[5] PERSHIN, Y . V ., DI VENTRA, M. Neuromorphic, digital and quan-
tum computation with memory circuit elements. Proceedings of the
IEEE, 2012, vol. 100, p. 2071 - 2080.
[6] LINN, E., ROSEZIN, R., TAPPERTZHOFEN, S., B ¨OTTGER, U.,
W ASER, R. Beyond von Neumann-logic operations in passive cross-
bar arrays alongside memory operations. Nanotechnology, 2012,
vol. 23, no. 30, p. 305205.
[7] THOMAS, A. Memristor-based neural networks. Journal of Physics
D: Applied Physics, 2013, vol. 46, no. 9, p. 093001.
[8] SACCHETTO, D., DE MICHELI, G., LEBLEBICI, Y . Multitermi-
nal memristive nanowire devices for logic and memory applications:
A review. Proceedings of the IEEE, 2012, vol. 100, p. 2008 - 2020.
[9] PERSHIN, Y . V ., LA FONTAINE, S., DI VENTRA, M. Memris-
tive model of amoeba learning. Physical Review E , 2009, vol. 80,
p. 021926.
[10] EROKHIN, V ., BERZINA, T., SMERIERI, A., CAMORANI, P.,
EROKHINA, S., FONTANA, M. Bio-inspired adaptive networks
based on organic memristors.Nano Communication Networks, 2010,
vol. 1, no. 2, p. 108 - 117.
[11] JOHNSEN, G. K., L ¨UTKEN, C. A., MARTINSEN, O. G.,
GRIMNES, S. Memristive model of electro-osmosis in skin. Phys-
ical Review E, 2011, vol. 83, p. 031916.
[12] TRA VERSA, F. L., PERSHIN, Y . V ., DI VENTRA, M. Mem-
ory models of adaptive behaviour. IEEE Transactions on Neural
Networks and Learning Systems , vol. 24, no. 9, p. 1437 - 1448,
arXiv:1301.0209.
[13] CHUA, L. O. Memristor - the missing circuit element. IEEE Trans-
actions on Circuit Theory, 1971, vol. 18, no. 5, p. 507 - 519.
[14] BIOLEK, Z., BIOLEK, D., BIOLKOV A, V . SPICE model of mem-
ristor with nonlinear dopant drift. Radioengineering, 2009, vol. 18,
no. 2, p. 210 - 214.
[15] BIOLEK, Z., BIOLEK, D., BIOLKOV A, V . SPICE modeling of
memristive, memcapacitative and meminductive systems. Proc. of
ECCTD ’09, European Conference on Circuit Theory and Design .
Antalya (Turkey), 2009, p. 249 - 252.
[16] BENDERLI, S., WEY , T. A. On SPICE macromodelling of TiO2
memristors. Electronics Letters, 2009, vol. 45, no. 7, p. 377 - 378.
[17] RAK, A., CSEREY , G. Macromodeling of the memristor in SPICE.
IEEE Transactions on Computer-Aided Design of Integrated Circuits
and Systems, 2010, vol. 29, no. 4, p. 632 - 636.
[18] BIOLEK, D., BIOLEK, Z., BIOLKOV A, V . SPICE modelling of
memcapacitor. Electronics Letters, 2010, vol. 46, p. 520 - 522.

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 967
[19] BIOLEK, D., BIOLEK, Z., BIOLKOV A, V . PSPICE modeling of
meminductor. Analog Integrated Circuits and Signal Processing ,
2011, vol. 66, no. 1, p. 129 - 137.
[20] KOLKA, Z., BIOLEK, D., BIOLKOV A, V . Hybrid modelling and
emulation of mem-systems. International Journal of Numerical
Modelling, 2011, vol. 25, no. 3, p. 216 - 225.
[21] PERSHIN, Y . V ., DI VENTRA, M. Spice model of memristive
devices with threshold. Radioengineering, 2013, vol. 22, no. 2,
p. 485 - 489.
[22] KV ATINSKY , S., FRIEDMAN, E. G., KOLODNY , A., WEISER,
U. C. TEAM: ThrEshold adaptive memristor model. IEEE Transac-
tions on Circuits and Systems I, 2013, vol. 60, no. 1, p. 211 - 221.
[23] PERSHIN, Y . V ., DI VENTRA, M. Teaching memory circuit el-
ements via experiment-based learning. IEEE Circuits and Systems
Magazine, 2012, vol. 12, no. 1, p. 64 - 74.
[24] KOLKA, Z., BIOLEK, D., BIOLKOV A, V . Frequency-domain
steady-state analysis of circuits with mem-elements. Analog In-
tegrated Circuits and Signal Processing , 2013, vol. 74, no. 1,
p. 79 - 89.
[25] TETZLAFF, R. et al. The Memristor Theory. Springer, 2013 (to be
published).
[26] STRUKOV , D. B., SNIDER, G. S., STEW ART, D. R., WILLIAMS,
R. S. The missing memristor found. Nature, 2008, vol. 453,
p. 80 - 83.
[27] JOGLEKAR, Y . N., WOLF, S. J. The elusive memristor: proper-
ties of basic electrical circuits. European Journal of Physics , 2009,
vol. 30, p. 661.
[28] KUNDERT, K. S., FOREWORD BY-GRAY , P. The Designer’s
Guide to SPICE and SPECTRE. Kluwer Academic Publishers, 1995.
[29] KIELKOWSKI, R. M. Inside Spice. New York (USA): McGraw-Hill,
1998.
[30] HSPICE User Guide: Simulation and Analysis . Synopsys, Version
A-2008.03, 2008.
[31] PSpice A/D Reference Guide. Product Version 16.5, 2011.
[32] LTspice IV user guide. Linear Technology Corporation, 1998-2012.
[33] CHUA, L. Resistance switching memories are memristors. Applied
Physics A, 2011, vol. 102, no. 4, p. 765 - 783.
[34] CHUA, L. O., KANG, S. M. Memristive devices and systems. Pro-
ceedings of the IEEE, 1976, vol. 64, p. 209 - 223.
[35] DI VENTRA, M., PERSHIN, Y . V . On the physical properties of
memristive, memcapacitive, and meminductive systems. Nanotech-
nology, 2013, vol. 24, p. 255201.
[36] PICKETT, M. D., STRUKOV , D. B., BORGHETTI, J. L., Y ANG,
J. J., SNIDER, G. S., STEW ART, D. R., WILLIAMS, R. S. Switch-
ing dynamics in titanium dioxide memristive devices.Journal of Ap-
plied Physics, 2009, vol. 106, no. 7, p. 074508.
[37] Y AKOPCIC, C., TAHA, T. M., SUBRAMANY AM, G., PINO, R. E.,
ROGERS, S. A memristor device model. IEEE Electron Device Let-
ters, 2011, vol. 32, no. 10, p. 1436 - 1438.
[38] PERSHIN, Y . V ., SLIPKO, V . A., DI VENTRA, M. Complex dynam-
ics and scale invariance of one-dimensional memristive networks.
Physical Review E, 2013, vol. 87, p. 022116.
[39] BURR, G. W., BREITWISCH, M. J. et al. Phase change memory
technology. Journal of Vacuum Science & Technology B: Microelec-
tronics and Nanometer Structures, 2010, vol. 28, no. 2, p. 223 - 262.
[40] DAO-LIN, C., ZHI-TANG, S., XI, L., HOU-PENG, C., XIAO-
GANG, C. A compact spice model with verilog-a for phase change
memory. Chinese Physics Letters, 2011, vol. 28, no. 1, p. 018501.
[41] COBLEY , R. A., WRIGHT, C. D. Parameterized spice model for
a phase-change ram device. IEEE Transactions on Electron Devices,
2006, vol. 53, no. 1, p. 112 - 118.
[42] VENTRICE, D., FANTINI, P., REDAELLI, A., PIROV ANO, A.,
BENVENUTI, A., PELLIZZER, F. A phase change memory com-
pact model for multilevel applications.IEEE Electron Device Letters,
2007, vol. 28, no. 11, p. 973 - 975.
[43] SONODA, K., SAKAI, A., MONIW A, M., ISHIKAW A, K.,
TSUCHIY A, O., INOUE, Y . A compact model of phase-change
memory based on rate equations of crystallization and amorphiza-
tion. IEEE Transactions on Electron Devices , 2008, vol. 55, no. 7,
p. 1672 - 1681.
[44] PICKETT, M. D., WILLIAMS, R. S. Sub-100 fj and sub-nanosecond
thermally driven threshold switching in niobium oxide crosspoint
nanodevices. Nanotechnology, 2012, vol. 23, no. 21, p. 215202.
[45] MARTINEZ-RINCON, J., DI VENTRA, M., PERSHIN, Y . V . Solid-
state memcapacitive system with negative and diverging capacitance.
Physical Review B, 2010, vol. 81, p. 195430.
[46] MARTINEZ-RINCON, J., PERSHIN, Y . V . Bistable non-volatile
elastic membrane memcapacitor exhibiting chaotic behavior. IEEE
Transactions on Electron Devices , 2011, vol. 58, no. 6, p. 1809 -
1812.
[47] COHEN, G. Z., PERSHIN, Y . V ., DI VENTRA, M. Lagrange for-
malism of memory circuit elements: Classical and quantum formu-
lations. Physical Review B, 2012, vol. 85, p. 165428.
[48] PERSHIN, Y . V ., DI VENTRA, M. Memory effects in complex ma-
terials and nanoscale systems. Advances in Physics , 2011, vol. 60,
p. 145 - 227.
[49] HSPICE Reference Manual: Commands and Options . Synopsys,
Version A-2008.03, 2008.
About Authors . . .
Dalibor BIOLEK received the M.Sc. degree in Electrical
Engineering from Brno University of Technology, Czech Re-
public, in 1983, and the Ph.D. degree in Electronics from the
Military Academy Brno, Czech Republic, in 1989. He is
currently with the Department of EE, University of Defense
Brno (UDB), and with the Department of Microelectronics,
Brno University of Technology (BUT), Czech Republic. His
scientiﬁc activity is directed to the areas of general circuit
theory, frequency ﬁlters, and computer simulation of elec-
tronic systems. For years, he has been engaged in algorithms
of the symbolic and numerical computer analyses of elec-
tronic circuits with a view to the linear continuous-time and
switched ﬁlters. He has published over 300 papers and is the
author of two books on circuit analysis and simulation. At
present, he is a professor at BUT and UDB in the ﬁeld of
Theoretical Electrical Engineering. Prof. Biolek is a mem-
ber of the CAS/COM Czech National Group of IEEE. He is
also the president of Commission C of the URSI National
Committee for the Czech Republic.
Massimiliano DI VENTRA received his Ph.D. degree in
theoretical physics from the Ecole Polytechnique Federale
de Lausanne, Switzerland, in 1997. His research inter-

968 D. BIOLEK, M. DI VENTRA, Y . V . PERSHIN, RELIABLE SPICE SIMULA TIONS OF MEMRISTORS, MEMCAP ACITORS . . .
ests are in the theory of electronic and transport properties
of nanoscale systems, nonequilibrium statistical mechan-
ics, DNA sequencing/ polymer dynamics in nanopores, and
memory effects in nanostructures for applications in uncon-
ventional computing and biophysics. He is a fellow of the
American Physical Society and the Institute of Physics. He
has co-edited the textbook Introduction to Nanoscale Sci-
ence and Technology (Springer, 2004) for undergraduate stu-
dents, and he is single author of the graduate-level textbook
Electrical Transport in Nanoscale Systems (Cambridge Uni-
versity Press, 2008).
Yuriy V . PERSHIN received the Ph.D. degree in theoreti-
cal physics from the University of Konstanz, Konstanz, Ger-
many, in 2002. He is an Assistant Professor of Physics at
the University of South Carolina, Columbia. During his
career, he has been with the University of California San
Diego, Michigan State University, Clarkson University, and
Grenoble High Magnetic Field Laboratory. He has authored
over 85 research papers and three reviews. His recent re-
search interests span broad areas of nanotechnology, includ-
ing physics of semiconductor nanodevices, spintronics, and
biophysics.

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 i
Supplementary materials
1. SPICE codes for model R.1
PSpice and LTspice code
**** Ideal memristor model R1 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for PSpice and LTspice ; tested with Cadence PSpice v. 16.3 and LTspice v. 4*
**********************************************************************
. subckt memristorR1 plus minus params : Ron =100 Roff =10 k Rini =5 k
. param uv =10 f D =10 n k ={ uv * Ron /D **2} a ={( Rini - Ron )/( Roff - Rini )}
* model of memristive port
Roff plus aux { Roff }
Eres aux minus value ={( Ron - Roff )/(1+ a* exp ( -4* k*V(q )))* I( Eres )}
* end of the model of memristive port
* integrator model
Gx 0 Q value ={ i( Eres )}
Cint Q 0 1
Raux Q 0 100 meg
* end of integrator model
* alternative integrator model ; SDT function for PSPICE can be replaced by IDT for LTspice
* Eq Q 0 value ={ SDT (I( Eres ))}
. ends memristorR1
*. options method = gear ; use only for LTSpice
Vin in 0 sin 0 1 1
Xmem in 0 memristorR1
. tran 0 10 0 1m
. probe
. end
HSPICE code
**** Ideal memristor model R1 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for HSPICE ; tested with HSPICE Version A -2008.03*
**********************************************************************
. subckt memristorR1 plus minus Ron =100 Roff =10 k Rini =5 k
. param uv =10 f D =10 n k= ’uv * Ron /D **2 ’ a= ’( Rini - Ron )/( Roff - Rini ) ’
* model of memristive port
Roff plus aux ’ Roff ’
Eres aux minus vol = ’( Ron - Roff )/(1+ a* exp ( -4* k*V(q )))* I( Eres ) ’
* end of the model of memristive port
* integrator model
Gx 0 Q cur = ’i( Eres ) ’
Cint Q 0 1
Raux Q 0 100 meg
* end of integrator model
. ends memristorR1
. options post runlvl =0 lvltim =1 method = gear
Vin in 0 sin (0 ,1 ,1)
Xmem in 0 memristorR1
. tran 0.1 m 10
. probe v(x *.*) i(x *.*)
. end

ii D. BIOLEK, M. DI VENTRA, Y . V . PERSHIN, RELIABLE SPICE SIMULA TIONS OF MEMRISTORS, MEMCAP ACITORS . . .
2. SPICE codes for model R.2
PSpice and LTspice code
**** Bipolar memristive system with threshold R2 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for PSpice and LTspice ; tested with Cadence PSpice v. 16.3 and LTspice v. 4*
**********************************************************************
. subckt memR_TH plus minus PARAMS :
+ Ron =1 K Roff =10 K Rinit =5 K beta =1 E13 Vt =4.6
* model of memristive port
Gpm plus minus value ={ V( plus , minus )/ V(x )}
* end of the model of memristive port
* integrator model
Gx 0 x value ={ fs (V( plus , minus ), b1 )* ws (v(x),V( plus , minus ),b1 , b2 )*1 p}
Raux x 0 1T
Cx x 0 1p IC ={ Rinit }
* end of integrator model
* smoothed functions
. param b1 =10 u b2 =10 u
. func stps (x ,b )={1/(1+ exp (-x/b ))}
. func abss (x ,b )={ x *( stps (x ,b)- stps (-x ,b ))}
. func fs (v ,b )={ beta *(v -0.5*( abss (v+Vt ,b)- abss (v -Vt ,b )))}
. func ws (x ,v ,b1 , b2 )={ stps (v , b1 )* stps (1 - x/ Roff , b2 )+ stps (-v , b1 )* stps (x/ Ron -1 , b2 )}
* end of smoothed functions
. ends memR_TH
. options reltol =1 u
*. options method = gear ; use only for LTspice
Vsin 1 0 sin 0 5 50 meg
Xmem 1 0 memR_TH
. tran 0 0.1 u 0 0.1 n
. probe
. end
HSPICE code
**** Bipolar memristive system with threshold R2 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for HSPICE ; tested with HSPICE Version A -2008.03*
**********************************************************************
. subckt memR_TH plus minus
+ Ron =1 K Roff =10 K Rinit =5 K beta =1 E13 Vt =4.6
* model of memristive port
Gpm pl mn cur = ’V( plus , minus )/ V(x) ’
* end of the model of memristive port
* integrator model
Gx 0 x cur = ’fs (V( plus , minus ), b1 )* ws (v(x),V( plus , minus ),b1 , b2 )*1 p ’
Raux x 0 1T
Cx x 0 1p
. IC v(x )= ’ Rinit ’
* end of integrator model
* smoothed functions
. param b1 =10 u b2 =10 u
. param stps (x ,b )= ’ 1/(1+ exp (-x/b )) ’
. param abss (x ,b )= ’x *( stps (x ,b)- stps (-x ,b )) ’
. param fs (v ,b )= ’ beta *(v -0.5*( abss (v+Vt ,b)- abss (v -Vt ,b ))) ’
. param ws (x ,v ,b1 , b2 )= ’ stps (v , b1 )* stps ( Roff -x , b2 )+ stps (-v , b1 )* stps (x - Ron , b2 ) ’
* end of smoothed functions
. ends memR_TH

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 iii
. option post runlvl =6 method = gear
Vsin 1 0 sin (0 ,5 ,50 meg )
Xmem 1 0 memR_TH
. tran 0.1 n 0.1 u
. probe v(x *.*) i(x *.*)
. end
3. SPICE code for model R.3
PSpice and LTspice code
**** Phase change memristive system R3 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for PSpice and LTspice ; tested with Cadence PSpice v. 16.3 and LTspice v. 4*
**********************************************************************
. subckt PCM plus minus PARAMS :
+ Ron =10 K Roff =1 meg Rini =100 k alpha =20 meg beta =100 meg
+ Tr =20 Tx =200 Tm =600 Tini =20 Ch =2e -15 d =5 u
+ Vtr =1.8 V0 =50 m Cxini =0
* resistive port modeling
Ron plus aux { Ron }
Eres aux minus value ={( Roff - Ron )*(1 - V( Cx ))/(1+ exp (( V( plus , minus )- Vtr )/ V0 ))* I( Eres )}
* end of resistive port modeling
* temperature computation
GT 0 T value ={ V( plus , minus )* I( Eres )+ d *( Tr -V(T ))}
RauxT T 0 100 meg
CintT T 0 { Ch } IC ={ Tini }
* end of temperature computation
* Cx computation
GCx 0 Cx value =
+ { alpha *(1 - V( Cx ))* stps (V(T )/ Tx -1)* stps (1 - V(T )/ Tm )- beta *V( Cx )* stps (V(T )/ Tm -1)}
RauxCx Cx 0 100 meg
CintCx Cx 0 1 IC ={ Cxini }
* end of Cx computation
* smoothed step function
. param b =1 m
. func stps (x )={1/(1+ exp (-x/b ))}
* end of smoothed step function
. ends PCM
V 1 0 PWL
+ 0 4 300 n 4 301 n 0 400 n 0 401 n 6 500 n 6 501 n 0
Xmem 1 0 PCM
. tran 0 600 n
. probe
. end
HSPICE code
**** Phase change memristive system R3 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for HSPICE ; tested with HSPICE Version A -2008.03*
**********************************************************************
. subckt PCM plus minus
+ Ron =10 K Roff =1 meg Rini =100 k alpha =20 meg beta =100 meg
+ Tr =20 Tx =200 Tm =600 Tini =20 Ch =2e -15 d =5 u
+ Vtr =1.8 V0 =50 m Cxini =0
* resistive port modeling

iv D. BIOLEK, M. DI VENTRA, Y . V . PERSHIN, RELIABLE SPICE SIMULA TIONS OF MEMRISTORS, MEMCAP ACITORS . . .
Ron plus aux ’ Ron ’
Er aux minus vol = ’( Roff - Ron )*(1 - V( Cx ))/(1+ exp (( V( plus , minus )- Vtr )/ V0 ))* I( Er ) ’
* end of resistive port modeling
* temperature computation
GT 0 T cur = ’V( plus , minus )* I( Er )+ d *( Tr -V(T )) ’
RauxT T 0 100 meg
CintT T 0 ’Ch ’
. IC v(T )= ’ Tini ’
* end of temperature computation
* Cx computation
GCx 0 Cx cur =
+ ’ alpha *(1 - V( Cx ))* stps (V(T )/ Tx -1)* stps (1 - V(T )/ Tm )- beta *V( Cx )* stps (V(T )/ Tm -1) ’
RauxCx Cx 0 100 meg
CintCx Cx 0 1
. IC v( Cx )= ’ Cxini ’
* end of Cx computation
* smoothed step function
. param b =1 m
. param stps (x )= ’ 1/(1+ exp (-x/b )) ’
* end of smoothed step function
. ends PCM
. option post
V 1 0 PWL
+ 0 4 300 n 4 301 n 0 400 n 0 401 n 6 500 n 6 501 n 0
Xmem 1 0 PCM
. tran 6n 600 n
. probe v(x *.*) i(x *.*)
. end
4. SPICE code for model R.4
PSpice and LTspice code
**** Insulator -to - metal transition memristive system R4 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for PSpice and LTspice ; tested with Cadence PSpice v. 16.3 and LTspice v. 4*
**********************************************************************
. subckt IMTM plus minus PARAMS : uini =1 u
. param deltaT =784 rch =30 n L =20 n Rhoins =7 m Rhomet =100 u
+ deltaHtr =1.6 e8 k =1.5 cp =2.6 meg
. func Gammath (u )={ -2* pi *L*k/ log (u )}
. func dHdu (u )={ pi *L* rch **2*( cp * deltaT * uExpr (u )+2* deltaHtr *u )}
. func uExpr (u )={(1 - u **2+2* u **2* log (u ))/(2* u* log (u ))**2}
* resistive port modeling
Vsense plus sense 0
Rfix sense minus { Rhoins *L /( pi * rch **2)}
Gvar sense minus value ={ V( plus , minus )* v( uL )**2* pi * rch **2/ L *(1/ Rhomet -1/ Rhoins )}
* end of resistive port modeling
*u computation
Gu 0 u value ={1 p/ dHdu (v( uL ))*( v( plus , minus )* I( Vsense )- Gammath (v( uL ))* deltaT )}
Raux u 0 10 G
Cu u 0 1p IC ={ uini }
* end of u computation
*u limits
EuL uL 0 value ={ LIMIT (v(u ) ,1u ,0.99999)}
* end of u limits
. ends IMTM

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 v
* modeling Pearson - Anson relaxation oscillator
*. options trtol =0.1 method = gear ; use only in LTSpice
. options reltol =1 u
Vdc 1 0 1.8
RL 1 2 4.2 k
Re 2 3 2.7 k
Rscope 4 0 50
Cp 2 0 23 p
XIMTM 3 4 IMTM
. tran 0 10 u 8u 1n
. probe
. end
HSPICE code
**** Insulator -to - metal transition memristive system R4 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for HSPICE ; tested with HSPICE Version A -2008.03*
**********************************************************************
. subckt IMTM plus minus uini =1 u
. param deltaT =784 rch =30 n L =20 n Rhoins =7 m Rhomet =100 u
+ deltaHtr =1.6 e8 k =1.5 cp =2.6 meg
. param pi =3.1415926536
. param Gammath (u )= ’ -2* pi *L*k/ log (u) ’
. param dHdu (u )= ’pi *L* rch **2*( cp * deltaT * uExpr (u )+2* deltaHtr *u) ’
. param uExpr (u )= ’(1 - u **2+2* u **2* log (u ))/(2* u* log (u ))**2 ’
* resistive port modeling
Vsense plus sense 0
Rfix sense minus ’ Rhoins *L /( pi * rch **2) ’
Gvar sense minus cur = ’V( plus , minus )* v( uL )**2* pi * rch **2/ L *(1/ Rhomet -1/ Rhoins ) ’
* end of resistive port modeling
*u computation
Gu 0 u cur = ’1p/ dHdu (v( uL ))*( v( plus , minus )* I( Vsense )- Gammath (v( uL ))* deltaT ) ’
Raux u 0 10 G
Cu u 0 1p
. IC v(u )= ’ uini ’
* end of u computation
*u limits
EuL uL 0 vol = ’ min ( max (v(u ) ,1 u ) ,0.99999) ’
* end of u limits
. ends IMTM
* modeling Pearson - Anson relaxation oscillator
. option post runlvl =6
Vdc 1 0 1.8
RL 1 2 4.2 k
Re 2 3 2.7 k
Rscope 4 0 50
Cp 2 0 23 p
XIMTM 3 4 IMTM
. tran 1n 10 u 8u 1n
. probe v(x *.*) i(x *.*)
. end
5. SPICE code for model C.1
PSpice and LTspice code
**** Ideal memcapacitor C1 ****

vi D. BIOLEK, M. DI VENTRA, Y . V . PERSHIN, RELIABLE SPICE SIMULA TIONS OF MEMRISTORS, MEMCAP ACITORS . . .
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for PSpice and LTspice ; tested with Cadence PSpice v. 16.3 and LTspice v. 4*
**********************************************************************
. subckt memcapacitor plus minus params : Clow =1 p Chigh =100 p Cini =2 p k =100
. param a ={( Chigh - Cini )/( Cini - Clow )}
* model of memcapacitive port
. func C( phi )={ Clow +( Chigh - Clow )/( a* exp ( -4* k* phi )+1)}
EQ Q 0 value ={ C(V( phi ))* V( plus , minus )}
Gcap plus minus value ={ ddt (V(Q ))}
*for OrCAD PSpice 16 , the above line can be replaced by Gcap plus minus Q ={ V(Q )}
* end of the model of memcapacitive port
* integrator model
Gv 0 phi value ={ v( plus , minus )}
Cint phi 0 1
Raux phi 0 100 meg
* end of integrator model
. ends memcapacitor
Vin 1 0 sin 0 1 10
XMC 1 0 memcapacitor
. tran 0 0.2 0 1m
. probe
. end
HSPICE code
**** Ideal memcapacitor C1 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for HSPICE ; tested with HSPICE Version A -2008.03*
**********************************************************************
. subckt memcapacitor plus minus Clow =1 p Chigh =100 p Cini =2 p k =100
. param a= ’( Chigh - Cini )/( Cini - Clow ) ’
* model of memcapacitive port
. param C( phi )= ’ Clow +( Chigh - Clow )/( a* exp ( -4* k* phi )+1) ’
EQ Q 0 vol = ’C(V( phi ))* V( plus , minus ) ’
CQ plus minus C= ’C(V( phi )) ’ CTYPE =1
* end of the model of memcapacitive port
* integrator model
Gv 0 phi cur = ’v( plus , minus ) ’
Cint phi 0 1
Raux phi 0 100 meg
* end of integrator model
. ends memcapacitor
. option runlvl =0 lvltim =1 method = gear
Vin 1 0 sin (0 ,1 ,10)
XMC 1 0 memcapacitor
. tran 1m 0.2
. probe v(x *.*) i(x *.*)
. end
6. SPICE code for model C.2
PSpice and LTspice code
**** Multilayer memcapacitive system C2 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 vii
* Code for PSpice and LTspice ; tested with Cadence PSpice v. 16.3 and LTspice v. 4*
**********************************************************************
. subckt MLMCS plus minus params : d =100 n del =66.6 n Su =100 u er =5 Uev =0.33
. param e0 =8.854 p m =9.109 e -31 e =1.602 e -19 h =6.626 e -34
. param C0 ={ e0 * er * Su /d} C1 ={ C0 /(1 - del /d )} C2 ={ C0 *d/ del }
* Use this below line for LTSpice
*. param a ={ Su *e **2/(4* pi *h* Uev * del **2)} b ={4* pi * del * sqrt (m*e )* pwr ( Uev ,1.5)/ h} loga ={ log (a )}
* Use this below line for OrCAD PSpice
. param a =2.10572 e5 b =91.4682096 loga ={ log (a )}
. func I12 ( V1 )={ V1 * abs ( V1 )* exp ( LIMIT ( loga -b/ MAX ( abs ( V1 ) ,1 n ) , -20 ,20))}
* model of memcapacitive port
C1 plus c { C1 }
C2 c minus { C2 }
GQ c minus value ={ I12 (V(c , minus ))}
Rshunt c 0 100 meg
* end of the model of memcapacitive port
. ends MLMCS
Vin 1 0 sin 0 7.5 100
Rin 1 2 1
XMC 2 0 MLMCS
EQ Q 0 value ={ - sdt (I( Vin ))}
. tran 0 50 m 20 m 50 u skipbp
. probe
. end
HSPICE code
**** Multilayer memcapacitive system C2 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for HSPICE ; tested with HSPICE Version A -2008.03*
**********************************************************************
. subckt MLMCS plus minus d =100 n del =66.6 n Su =100 u er =5 Uev =0.33
. param pi =3.1415926536 e0 =8.854 p m =9.109 e -31 e =1.602 e -19 h =6.626 e -34
. param C0 = ’e0 * er * Su /d ’ C1 = ’C0 /(1 - del /d) ’ C2 = ’C0 *d/ del ’
. param a =2.10572 e5 b =91.4682096 loga = ’ log (a) ’
. param I12 ( V1 )= ’V1 * abs ( V1 )* exp ( min ( max ( loga -b/ MAX ( abs ( V1 ) ,1 n ) , -20) ,20)) ’
* model of memcapacitive port
C1 plus c ’C1 ’
C2 c minus ’C2 ’
GQ c minus cur = ’ I12 (V(c , minus )) ’
Rshunt c 0 100 meg
* end of the model of memcapacitive port
. ends MLMCS
. option post
Vin 1 0 sin (0 ,7.5 ,100)
Rin 1 2 1
XMC 2 0 MLMCS
* charge computation
Gqq qq 0 vol = ’I( Vin ) ’
Cqq qq 0 1
Rqq qq 0 100 meg
* end of charge computation
. tran 50 u 50 m 20 m 50 u
. probe v(x *.*) i(x *.*)
. end
7. SPICE code for model C.3

viii D. BIOLEK, M. DI VENTRA, Y . V . PERSHIN, RELIABLE SPICE SIMULA TIONS OF MEMRISTORS, MEMCAP ACITORS . . .
PSpice and LTspice code
**** Bistable membrane memcapacitive system C3 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for PSpice and LTspice ; tested with Cadence PSpice v. 16.3 and LTspice v. 4*
**********************************************************************
. subckt BEMS plus minus params : y0 =0.2 yd0 =0
. param gamma =0.7 b =1 C0 =10 p
* model of memcapacitive port
C0 plus c { C0 }
Ec c minus value ={ V(Q )* V(y )/ C0 }
* end of the model of memcapacitive port
*Q computation
EQ Q 0 value ={ C0 *V( plus ,c )}
* end of Q computation
*y computation
Gy 0 y value ={ v( yd )}
Cy y 0 1 IC ={ y0 }
Ry y 0 100 meg
* end of y computation
* yd computation
Gyd 0 yd value ={ -(4* pi **2* v(y )*(( V(y )/ y0 )**2 -1)+ gamma *v( yd )+( b*V( plus , minus )/(1+ v(y )))**2)}
Cyd yd 0 1 IC ={ yd0 }
Ryd yd 0 100 meg
* end of yd computation
. ends BEMS
Vin 1 0 sin 0 2.8 0.658
Rin 1 2 1
XMC 2 0 BEMS
. tran 0 20 16 4m
. probe
. end
HSPICE code
**** Bistable membrane memcapacitive system C3 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for HSPICE ; tested with HSPICE Version A -2008.03*
**********************************************************************
. subckt BEMS plus minus y0 =0.2 yd0 =0
. param pi =3.1415926536 gamma =0.7 b =1 C0 =10 p
* model of memcapacitive port
C0 plus c ’C0 ’
CQ c minus C= ’C0 /V(y) ’ CTYPE =1
* Ec c minus vol = ’V(Q )* V(y )/ C0 ’
* end of the model of memcapacitive port
*Q computation
* GQ 0 Q cur = ’I( EC ) ’
* CQ Q 0 1
* RQ Q 0 100 meg
EQ Q 0 vol = ’C0 *V( plus ,c) ’
* end of Q computation
*y computation
Gy 0 y cur = ’v( yd ) ’
Cy y 0 1
. IC v(y )= ’y0 ’
Ry y 0 100 meg
* end of y computation
* yd computation
Gyd 0 yd cur = ’ -(4* pi **2* v(y )*(( V(y )/ y0 )**2 -1)+ gamma *v( yd )+( b*V( plus , minus )/(1+ v(y )))**2) ’

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 ix
Cyd yd 0 1
. IC v( yd )= ’ yd0 ’
Ryd yd 0 100 meg
* end of yd computation
. ends BEMS
. option post runlvl =6
Vin 1 0 sin (0 ,2.8 ,0.658)
Rin 1 2 1
XMC 2 0 BEMS
. tran 4m 20 16 4m
. probe v(x *.*) i(x *.*)
. end
8. SPICE code for model C.4
PSpice and LTspice code
**** Bipolar memcapacitive system with threshold C4 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for PSpice and LTspice ; tested with Cadence PSpice v. 16.3 and LTspice v. 4*
**********************************************************************
. subckt memC_TH plus minus PARAMS :
+ Clow =1 p Chigh =100 p Cinit =50 p beta =70 u Vt =3
* model of memcapacitive port
Ec plus minus value ={ V(Q )/ V(x )}
* end of the model of memcapacitive port
* integrator model
Gx 0 x value ={ fs (V( plus , minus ), b1 )* ws (v(x),v( plus , minus ),b1 , b2 )}
Raux x 0 100 meg
Cx x 0 1 IC ={ Cinit }
* end of integrator model
* charge computation
GQ 0 Q value ={ I( Ec )}
CQ Q 0 1
RQ Q 0 100 meg
* end of charge computation
* smoothed functions
. param b1 =10 m b2 =1 u
. func stps (x ,b )={1/(1+ exp (-x/b ))}
. func abss (x ,b )={ x *( stps (x ,b)- stps (-x ,b ))}
. func fs (v ,b )={ beta *(v -0.5*( abss (v+vt ,b)- abss (v -Vt ,b )))}
. func ws (x ,v ,b1 , b2 )={ stps (v , b1 )* stps (1 - x/ Chigh , b2 )+ stps (-v , b1 )* stps (x/ Clow -1 , b2 )}
* end of smoothed functions
. ends memC_TH
. options reltol =1 u ; use 0.1 u for LTspice
*. options method = gear ; use only for LTspice
Vsin 1 0 sin 0 4 50 k
Ri 1 2 1m
Xmem 2 0 memC_TH
. tran 0 100 u 20 u 0.1 u
. probe
. end
HSPICE code
**** Bipolar memcapacitive system with threshold C4 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *

x D. BIOLEK, M. DI VENTRA, Y . V . PERSHIN, RELIABLE SPICE SIMULA TIONS OF MEMRISTORS, MEMCAP ACITORS . . .
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for HSPICE ; tested with HSPICE RF Version A -2008.03*
**********************************************************************
. subckt memC_TH plus minus
+ Clow =1 p Chigh =100 p Cinit =50 p beta =70 u Vt =3
* model of memcapacitive port
Ec plus minus vol = ’V(Q )/( V(x )) ’
* end of the model of memcapacitive port
* integrator model
Gx 0 x cur = ’fs (V( plus , minus ), b1 )* ws (v(x),v( plus , minus ),b1 , b2 ) ’
Rx x 0 100 meg
Cx x 0 1
. IC v(x )= ’ Cinit ’
* end of integrator model
* charge computation
GQ 0 Q cur = ’I( Ec ) ’
CQ Q 0 1
RQ Q 0 100 meg
* end of charge computation
* smoothed functions
. param b1 =10 m b2 =10 u
. param stps (x ,b )= ’ 1/(1+ exp (-x/b )) ’
. param abss (x ,b )= ’x *( stps (x ,b)- stps (-x ,b )) ’
. param fs (v ,b )= ’ beta *(v -0.5*( abss (v+Vt ,b)- abss (v -Vt ,b ))) ’
. param ws (x ,v ,b1 , b2 )= ’ stps (v , b1 )* stps (1 - x/ Chigh , b2 )+ stps (-v , b1 )* stps (x/ Clow -1 , b2 ) ’
* end of smoothed functions
. ends memC_TH
. option post runlvl =6 delmax =1 n
Vsin 1 0 sin (0 ,4 ,50 k)
Ri 1 2 1
Xmem 2 0 memC_TH
. tran 0.1 u 100 u
. probe v(x *.*) i(x *.*)
. end
9. SPICE code for model L.1
PSpice and LTspice code
**** Ideal meminductor L1 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for PSpice and LTspice ; tested with Cadence PSpice v. 16.3 and LTspice v. 4*
**********************************************************************
. subckt meminductor plus minus params : Llow =1 m Lhigh =10 m Lini =2 m k =10 k
. param a ={( Lhigh - Lini )/( Lini - Llow )}
* model of meminductive port
. func L(q )={ Llow +( Lhigh - Llow )/( a* exp ( -4* k*q )+1)}
Ephi phi 0 value ={ L(V(Q ))* I( EL )}
EL plus minus value ={ ddt (V( phi ))}
* end of the model of meminductive port
* integrator model
GQ 0 Q value ={ I( EL )}
Cint Q 0 1
Raux Q 0 100 meg
* end of integrator model
. ends meminductor
Iin 0 1 sin 0 5m 10

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 xi
XMC 1 0 meminductor
. tran 0 200 m 0 200 u skipbp ; for LTspice , decrease step ceiling from 200 u to 10 u
. probe
. end
HSPICE code
**** Ideal meminductor L1 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for HSPICE ; tested with HSPICE Version A -2008.03*
**********************************************************************
. subckt meminductor plus minus Llow =1 m Lhigh =10 m Lini =2 m k =10 k
. param a= ’( Lhigh - Lini )/( Lini - Llow ) ’
* model of meminductive port
. param L(q )= ’ Llow +( Lhigh - Llow )/( a* exp ( -4* k*q )+1) ’
Ephi phi 0 vol = ’L(V(Q ))* I( LL ) ’
LL plus minus L= ’L(V(Q )) ’ LTYPE =1
* end of the model of meminductive port
* integrator model
GQ 0 Q cur = ’I( LL ) ’
Cint Q 0 1
Raux Q 0 100 meg
* end of integrator model
. ends meminductor
. option post runlvl =0 lvltim =1 method = gear
Iin 0 1 sin (0 ,5m ,10)
XMC 1 0 meminductor
. tran 200 u 200 m
. probe v(x *.*) i(x *.*)
. end
10. SPICE code for model L.2
PSpice and LTspice code
**** Effective meminductive system L2 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for PSpice and LTspice ; tested with Cadence PSpice v. 16.3 and LTspice v. 4*
**********************************************************************
. subckt MLsystem plus minus params : L1 =1 u L2 =1 u k =0.8 R =1 C =1 u
L1 plus minus { L1 }
L2 1 3 { L2 }
k L1 L2 {k}
R 1 2 {R}
C 2 3 {C}
Raux 3 0 100 meg
. ends MLsystem
I 0 in sin 0 1m 100 k
XML in 0 MLsystem
Eflux flux 0 value ={ sdt (v( in ))}
. tran 0 60 u 40 u 0.5 n
. probe
. end
HSPICE code

xii D. BIOLEK, M. DI VENTRA, Y . V . PERSHIN, RELIABLE SPICE SIMULA TIONS OF MEMRISTORS, MEMCAP ACITORS . . .
**** Effective meminductive system L2 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for HSPICE ; tested with HSPICE Version A -2008.03*
**********************************************************************
. subckt MLsystem plus minus L1 =1 u L2 =1 u k =0.8 R =1 C =1 u
L1 plus minus { L1 }
L2 1 3 { L2 }
k L1 L2 {k}
R 1 2 {R}
C 2 3 {C}
Raux 3 0 100 meg
. ends MLsystem
. option post
I 0 in sin (0 ,1m ,100 k)
XML in 0 MLsystem
Gflux 0 flux cur = ’v( in ) ’
Cint flux 0 1
Rx flux 0 100 meg
. tran 0.4 n 60 u 40 u 0.5 n
. probe v(x *.*) i(x *.*)
. end
11. SPICE code for model L.3
PSpice and LTspice code
**** Bipolar meminductive system with threshold L3 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for PSpice and LTspice ; tested with Cadence PSpice v. 16.3 and LTspice v. 4*
**********************************************************************
. subckt memL_TH plus minus PARAMS :
+ Llow =1 u Lhigh =100 u Linit =50 u beta =10 meg It =10 u
* model of meminductive port
EL plus minus value ={ ddt (V( phi ))}
* forOrCADPSpice 16 , the above line can be replaced by EL plus minus F ={ V( phi )}
* end of the model of meminductive port
* integrator model
Gx 0 x value ={ fs (I( EL ), b1 )* ws (v(x),I( EL ),b1 , b2 )}
Raux x 0 100 meg
Cx x 0 1 IC ={ Linit }
* end of integrator model
* flux computation
Ephi phi 0 value ={ I( EL )* V(x )}
* end of flux computation
* smoothed functions
. param b1 =10 n b2 =1 u
. func stps (x ,b )={1/(1+ exp (-x/b ))}
. func abss (x ,b )={ x *( stps (x ,b)- stps (-x ,b ))}
. func fs (I ,b )={ beta *(I -0.5*( abss (I+It ,b)- abss (I -It ,b )))}
. func ws (x ,I ,b1 , b2 )={ stps (I , b1 )* stps (1 - x/ Lhigh , b2 )+ stps (-I , b1 )* stps (x/ Llow -1 , b2 )}
* end of smoothed functions
. ends memL_TH
. options reltol =1 u
*. options method = gear ; use only for LTspice
Isin 0 1 sin 0 12 u 50 k
Xmem 1 0 memL_TH

RADIOENGINEERING, VOL. 22, NO. 4, DECEMBER 2013 xiii
. tran 0 100 u 40 u 0.1 u
. probe
. end
HSPICE code
**** Bipolar meminductive system with threshold L3 ****
*D. Biolek , M. Di Ventra , Y. V. Pershin *
* Reliable SPICE Simulations of Memristors , Memcapacitors and Meminductors , 2013*
* Code for HSPICE ; tested with HSPICE Version A -2008.03*
**********************************************************************
. subckt memL_TH plus minus
+ Llow =1 u Lhigh =100 u Linit =50 u beta =10 meg It =10 u
* model of meminductive port
LL plus minus L= ’V(x) ’ LTYPE =1
* end of the model of meminductive port
* integrator model
Gx 0 x cur = ’fs (I( LL ), b1 )* ws (v(x),I( LL ),b1 , b2 ) ’
Raux x 0 100 meg
Cx x 0 1
. IC v(x )= ’ Linit ’
* end of integrator model
* flux computation
Ephi phi 0 vol = ’I( LL )* V(x) ’
* end of flux computation
* smoothed functions
. param b1 =10 n b2 =1 u
. param stps (x ,b )= ’ 1/(1+ exp (-x/b )) ’
. param abss (x ,b )= ’x *( stps (x ,b)- stps (-x ,b )) ’
. param fs (I ,b )= ’ beta *(I -0.5*( abss (I+It ,b)- abss (I -It ,b ))) ’
. param ws (x ,I ,b1 , b2 )= ’ stps (I , b1 )* stps (1 - x/ Lhigh , b2 )+ stps (-I , b1 )* stps (x/ Llow -1 , b2 ) ’
* end of smoothed functions
. ends memL_TH
. option post runlvl =6 KCLTEST delmax =1 n
Isin 0 1 sin (0 ,12u ,50 k)
Xmem 1 0 memL_TH
. tran 0.1 u 100 u
. probe v(x *.*) i(x *.*)
. end
