# 04_data_driven_VerilogA_ReRAM.pdf

1
A Data-Driven Verilog-A ReRAM Model
Ioannis Messaris, Alexander Serb, Member, IEEE, Spyros Stathopoulos, Ali Khiat,
Spyridon Nikolaidis, Senior Member, IEEE, and Themistoklis Prodromakis, Senior Member, IEEE
Abstract—The translation of emerging application concepts
that exploit Resistive Random Access Memory (ReRAM) into
large-scale practical systems requires realistic yet computation-
ally efﬁcient device models. Here, we present a ReRAM model
where device current-voltage characteristics and resistive switch-
ing rate are expressed as a function of a) bias voltage and b)
initial resistive state. The model’s versatility is validated on de-
tailed characterization data, for both ﬁlamentary valence change
memory and non-ﬁlamentary ReRAM technologies, where device
resistance is swept across its operating range using multiple
input voltage levels. Furthermore, the proposed model embodies
a window function which features a simple mathematical form
analytically describing resistive state response under constant
bias voltage as extracted from physical device response data. Its
Verilog-A implementation captures the ReRAM memory effect
without requiring integration of the model state variable, making
it suitable for fast and/or large-scale simulations and overall inter-
operable with current design tools.
Index Terms —Characterization, modeling, ReRAM, simula-
tion, Verilog-A.
I. I NTRODUCTION
S
INCE 2008 when the basic resistive switching property of a
double-layer nano-scale ﬁlm based on titanium dioxide was
studied [1] and linked to Chua’s theory of the ’memristor’ [ 2],
understanding of practical memristor realizations has moved
far beyond the simple ’moving barrier’ model. Solid-state
memristor devices stem from different technological roots
(phase-change memory, spin-torque transfer, metal-oxide etc.
[3], [ 4], [ 5]) and employ a variety of electrode/active layer
materials and geometries. Such devices are becoming more
and more accessible to researchers, and it is now more clear
on how different implementations feature properties that render
them suitable for different applications. There are memristors
that have been reported to switch quickly and in a probabilistic
fashion [ 6], while others can have their resistive state (RS)
shifted in small continuous steps [ 7] that are ideal for synaptic
learning and reconﬁgurable electronics [ 8], [ 9]. Resistive
Random Access Memory (ReRAM) devices are a class of
(metal-oxide) memristors that support multi-state programming,
can be programmed swiftly and with low energy and can be
compatible with post-CMOS processing.
This work was supported in part by the EU COST Action IC1401 MEMOCIS
and the Engineering and Physical Sciences Research Council under Grant
EP/K017829/1.
The data from this paper can be obtained from University of Southampton
e-Prints Repository DOI:xxxx.
I. Messaris and S. Nikolaidis was with the Department of Physics,
Aristotle University of Thessaloniki, 54124 Thessaloniki Greece (email:
imessa@physics.auth.gr).
A. Serb, S. Stathopoulos, A. Khiat and T. Prodromakis are with the Nano
Group, ECS, University of Southampton, Highﬁeld, Southampton SO17 1BJ.
(email: A.Serb@soton.ac.uk.)
In general, a 1 st order, extended, voltage controlled memris-
tive system is expressed as,
i =G(x,v )v (1)
dx
dt =g(x,v ) (2)
where, i is the current ﬂowing through the device, v is the
voltage applied on its terminals and x is the device’s internal
state variable. Equation (1) calculates the current ﬂowing
through the device as a function of the state variable ( x)
and bias voltage (v) while function g(·) in (2) describes the
dependency of the state variable time-derivative on the same
variables (x, v).
Among the well-established, generalized, voltage controlled
memristor models published to date, the model presented in [10]
uses a linear or exponential relationship for (1), while models
[11], [12] and [ 13] utilize a hyperbolic sinusoidal expression
to approximate the Simmons tunneling barrier model which de-
scribes theI−V characteristics of metal-insulator-metal (MIM)
memristive devices [14]. Regarding equation (2), the mentioned
models (besides [ 13]) have their internal state ( x) and external
stimuli (v) dependencies expressed by separate functions which
are linked orthogonally, i.e. g(x,v ) =s(v)×f(x). Function
s(v) expresses the device’s ’(voltage) switching sensitivity’ for
which various non-linear forms have been proposed such as
the simple exponential presented in [ 11] or the more complex
a-power law function in [ 10]. Function f(x) corresponds to
the ’window function’ that bounds the device state variable in a
ﬁxed range (projected to a ﬁxed resistive range[Rmin,Rmax ])
and models the experimentally veriﬁed nonlinear kinetics in
the state variable motion as it approximates these constant
boundaries (maximum and minimum resistive states Rmin,
Rmax). A number of window functions have been presented
([11], [15], [16], [17]) which take various mathematical forms,
though the ﬁtting parameters in these expressions are hard
to extract from characterization data which in most cases are
particularly noisy.
As different physical models describe different types of
ReRAM devices ([ 18], [19]), here, we present a general, em-
pirical, 1st order, voltage controlled ReRAM model for devices
exhibiting non-volatile, bipolar switching characteristics. The
state variable of the proposed model is the device RS ( R)
which can be easily measured with modern characterization
instrumentation ([ 20]) therefore establishing a direct link
between experimental data and model parameters. The I−V
relationship (1) is proportional to device conductance ( 1/R)
and a voltage controlled hyperbolic sinusoid. The ’sensitivity’
function s(v) takes the form of a simple voltage controlled
exponential expression while the ’window function’ f(R,v ) is
described by a similar RS and voltage dependent exponential,

2
which is different from the previously proposed empirical
formulations that are expressed as solely state dependent.
Notably, the proposed window function allows for the derivation
of a predictive analytical RS time-response expression under
constant bias voltageR(t)|Vb which greatly simpliﬁes the ﬁtting
of the model on characterization data and can be exploited to
implement a computationally efﬁcient simulation model that
does not require the integration of the state variable equation
(dR/dt). Accordingly, the proposed model is suitably coded
in Verilog-A which is a behavioral language standardized in
the semiconductor industry mainly due to its ease of use and
ﬂexibility to run in numerous industrial circuitry simulators
(Spectre, HSPICE, Eldo etc.).
The paper is structured as follows: Section II brieﬂy describes
the operation theory of the devices ﬁtted by the proposed model.
Model functionality and equations are presented in Section
III. Section IV analyzes a) the characterization procedure
employed on in-house fabricated TiOx -based devices and b)
the parameter extraction method used to calculate the model
parameters from the exported data. Section V validates the
proposed model and the parameter extraction algorithm on
both valence change memory (VCM) ﬁlamentary and non-
ﬁlamentary ReRAM devices and compares its ﬁtting accuracy
against a widely adopted generalized and highly non-linear
memristor model. Section VI details the coding strategy utilized
to implement a computationally efﬁcient Verilog-A module
based on the model expressions while Section VII describes the
methods used throughout the manuscript. Finally, in Section
VIII certain model characteristics are discussed and the paper
is concluded.
II. O PERATION THEORY CAPTURED BY THE PROPOSED
MODEL
The previously mentioned generalized models have demon-
strated excellent performance in capturing memristive device
I−V characterization data responding to different kinds of
voltage sweeps (piece-wise linear, sinusoidal etc). Nevertheless,
these data enclose only a subset of device switching dynamics.
Detailed switching characterization data where device RS is
swept in its resistive region of operation for different voltage
levels, such as the ReRAM RS responses shown in Fig. 1,
have not been ﬁtted in any of these works. The illustrated plots
resemble the form of typical VCM and non-ﬁlamentary RS
responses where regardless of the voltage value applied, we
notice an initially steep change in RS followed by gradual
saturation. This behavior has been reported by many ReRAM
technologies [13], [21], [22], [23], [24], [25], etc.
Focusing on VCM devices, these operate via the formation
of oxygen-deﬁcient ﬁlaments in transition metal oxides with
among the most commonly met examples being the TiOx -,
FeOx - and TaOx -based devices for which R(t)|Vb plots are
shown in Figs. 1(a), (b) and (c) respectively. Brieﬂy, as oxygen
ions are considered more mobile than metal elements, bias ap-
plication causes the local motion of these defects (oxygen ions)
which induces a local valence change of the cations triggering
resistive switching [26]. Moreover, in [24] the authors presented
a physical model for a VCM Pt/Ta/TaOx/Pt device where
0 100 200 300 400 500
400
800
1200
1600
2000
2400
0 5 10 15 20 25
200
400
600
800
1000
0 4 8 12 16 20
1.0
1.5
2.0
2.5
0 100 200 300 400 500
5.0
5.4
5.8
Pulse number
V > 0
Resistance (K )
V
V
V > 0
a.
Resistance ( )
Pulse number
V < 0
b.
|V|
Resistance ( )
Pulse numberc.
V > 0
V
Resistance (M )
Pulse numberd.
Fig. 1. Typical resistive responses to voltage pulses of constant amplitude
reproduced by four different ReRAM technologies: (a) OFF-switching transi-
tions of an in-house fabricated ﬁlamentary VCM TiOx -based sample. (b) ON-
switching transitions for the ﬁlamentary VCMFeOx -based device presented in
[23]. (c) OFF transitions for the ﬁlamentary VCMTaOx -based device modeled
in [24]. (d) ON transitions for the non-ﬁlamentaryTa/TaOx/TiO 2/Ti stack
modeled in [21]. Sub-plots (b)-(d) were digitized from the corresponding ﬁgures
in the respective papers.
resistive switching is linked to the radius modulation of a
Ta -rich conducting cylindrical-assumed ﬁlament surrounded
by a matrix of insulating forms of TaOx . They consider that
two speciﬁc competing components of ionic ﬂux, Fick and
Soret diffusion, determine a steady state ﬁlament radius and
resistive state for the device. Speciﬁcally, this is deﬁned from
the balance between these two diffusion mechanisms which
is controlled by the applied voltage, i.e. a speciﬁc voltage
level ultimately settles the device at a speciﬁc RS (see Fig.
1(c)). Regarding the switching mechanism in non-ﬁlamentary
devices, the authors in [ 21] presented a Ta/TaOx/TiO 2/Ti
stack where resistance change is determined by homogeneous
barrier modulation (HBM) induced by oxygen ion migration
[27]. Under pulsed voltage stimulation and starting from an
initial high RS, the ﬁrst pulses provoke oxygen ions to drift
rapidly from the TaOx bulk toward the Ta/TaOx interface
thus lowering device resistance. The accumulated charge (in
the anode) reduces the internal electric ﬁeld which in turn
dampens further ion migration toward the interface (saturation).
ON-switching responses of the described physical mechanism
are illustrated in Fig. 1(d). A similar phenomenon occurs when
OFF-switching pulses are applied. Behaviorally, in both VCM
and non-ﬁlamentary cases, we notice that RS saturation seems
to take place at well separated voltage dependent resistive
levels.
Conversely to the previously proposed generalized memristor
models, the presented model embodies a voltage dependent win-
dow function expression which implements voltage dependent
rather than constant resistive boundaries of operation, Rmin(v)
and Rmax(v). As this approach is in tune with commonly met
ReRAM behavior (Fig. 1), we will show that the proposed
model is able to capture accurately such responses.

3
III. R ERAM M ODEL
In the proposed ReRAM model both the current-voltage
(I−V ) characteristics and the time derivative of the state
variable (dR/dt) are linked to bias voltage v and RS R with
the following differential algebraic equation (DAE) set:
i(R,v ) =
{
ap(1/R) sinh(bpv), forv > 0
an(1/R) sinh(bnv), forv ≤ 0 (3)
dR
dt =g(R,v ) =s(v)×f(R,v ) (4)
where s(v) is the switching sensitivity function,
s(v) =



Ap(−1 +etp|v|), v >0
An(−1 +etn|v|), v <0
else 0
(5)
and f(R,v ) corresponds to the window function,
f(R,v ) =



−1 +eηkp(rp(v)−R),R<η ·rp(v), v >0
−1 +eηkn(R−rn(v)),R>η ·rn(v), v <0
else 0
(6)
Symbols ap,n, bp,n, Ap,n, tp,n, kp,n are ﬁtting parameters,
while rp,n(v) are the voltage dependent resistive boundary
functions for the positive and negative stimulation cases which
will be discussed in the next paragraph. Parameter η is 1 or
-1 depending on the switching direction of device RS to said
stimulus polarity. Speciﬁcally, for bipolar device functionality,
η = 1 when ∆R(Vb) > 0 for Vb > 0 while η =−1 when
∆R(Vb) > 0 for Vb < 0. A sample switching rate surface
reproduced by the proposed model (4)-(6) is shown in Fig. 2
which describes changes in the device’s state variable because
of stimulation given a well-deﬁned initial state R0 and with a
ﬁxed voltagev.
Functions rp,n(v) in (6) take the form of voltage controlled
polynomials,
rp,n(v) =
qp,n∑
mp,n=0
rmp,nvmp,n (7)
where mp,n are positive integers and qp,n deﬁne the order of
the polynomials for the positive and negative stimulation cases.
Notably, for m = 0 , resistive boundaries become constant
matching the conventional modeling approach. Assuming that
η = 1, (6) calculates zero switching above a speciﬁed voltage
dependent resistive threshold value rp(Vb) for Vb > 0 and
below rn(Vb) for Vb < 0. In agreement with the generic
ReRAM behavior shown in Fig. 1, the positions of these
resistive limits are monotonically dependent on voltage. The
model predicts that higher positive voltages push rp(Vb) to
higher RSs while more invasive negative biases push rn(Vb) to
lower RSs. The physical interpretation of these boundaries is
described as follows: for any RS below rp(Vb) (active region)
at a given positive voltage Vb, applying this voltage can push
the device to rp(Vb), but no further (saturation). If the device
is already above rp(Vb), no switching occurs (for positive
stimulation). The same applies for negative biasing and the
Fig. 2. Example switching rate surface ( g(R,v )- gray surface) characteristics
as reproduced by the proposed switching rate expression (4). Green lines
correspond todR/dt vsR plots for constant bias stimulationVb (g(R,±Vbi)).
The characterization routine (see Section IV) is designed to sample the device’s
switching surface along these lines. Conversely, red lines sample the device’s
switching surface on lines parallel to the voltage axis (g(R0,v )), though a
much more complex testing algorithm is required in order to gather such
measurements. Purple lines delineate the voltage dependent resistive boundary
functions (7) (in linear form) for the positive rp(v) and negative rn(v)
stimulation cases. These are projected on the ﬁgure base to mark the interface
between non-zero (white) and zero (gray) switching regions (z(R,v ) = 0).
rn(Vb) limit. Experimentally, the speciﬁc functional form of
(7) is revealed by utilizing the parameter extraction algorithm
described in the Section that follows. For the tested devices:
qp,n≤ 2 (see Section V).
By examining the switching model equations, we notice that
the proposed sensitivity function (5) lacks voltage thresholds.
Threshold voltage parameters have been adopted by the models
presented in [ 10], [11], [28] as an approximation that neglects
the device’s low voltage (modeled as sub-threshold) kinetics.
Mathematically, these models bear relatively simple switching
expressions that are focused in capturing physical device
behavior in the over-threshold region, thereby enhancing their
ftting performance on I− V characterization data. This
approximation is further justiﬁed as certain demonstrated
practical applications are based on the assumption of ReRAM
thresholded behavior [29]. However, the response of a physical
device to input voltage doesn’t depend solely on voltage but
also on current RS which implies that the same device may
exhibit different voltage thresholds depending on its running
RS (Vth(R)). This is also captured by our model. Solving (7)
with respect to voltage gives us the switching threshold voltage
dependency on device RS,
Vth,p,n(R) =r−1
p,n(R) (8)
We should note here that for q > 1, equation (8) has more
than a single solution. The value for Vth,p,n corresponds to
the solution that is included in the device’s operating voltage
region. Purple lines in Fig. 2 are reproduced by the resistive
boundary function (7) (in linear form for both polarities) which

4
delineates the zero-switching area z(R,v ) = 0 (projected at
the base of Fig. 2).
Summarizing, a) the presence of RS dependent switching
voltage thresholds (Vth(R)) and b) the variable (rather than
constant) voltage dependent window function boundaries are
modeled by (6) via the voltage dependency expressed by the
resistive boundary function (7), an approach that was initially
introduced in the method presented in [30].
IV. M ODEL FITTING TO CHARACTERIZATION DATA
In order to ﬁt the model on an arbitrary ReRAM device,
a proper device-characterization procedure complemented by
a parameter extraction algorithm for the proposed model is
employed. In this section, we describe the characterization
applied on in-house fabricated TiOx -based samples similar to
the ones investigated in [ 31], along with the ﬁtting procedure
that calculated the model parameters (see Methods for device
fabrication details).
Parametersap,n,bp,n were obtained by ﬁtting (3) on multiple
static current-voltage responses taken at different RSs during
the ﬂow of the characterization protocol.
The parameters for s(v) and f(R,v ) were determined by
exploiting the simple form of the proposed switching rate
expression (4)-(7) which can be solved analytically under
constant bias voltage stimulation. Thus
R(t)|Vb =
= ln(eηkprp(Vb) +e−ηkpsp(Vb)t(eηkpR0−eηkprp(Vb))
kp
(9)
for Vb > 0 and R<η ·rp(Vb),
R(t)|Vb =
ln(e−ηknR0+ηknsn(Vb)t−e−ηknrn(Vb)(−1 +eηknsn(Vb)t))
kn
(10)
for Vb < 0 and R>η ·rn(Vb),
else R0.
Parameter R0 is the initial RS, t is time, s(Vb), r(Vb)
are constant valued when the input voltage is ﬁxed, v =Vb,
and η = ±1 deﬁnes the switching direction as discussed
in the previous Section. The parameters for the switching
member of the proposed model were calculated by repeatedly
applying constant voltage stimulation on the device under
test (DUT) (at different Vb levels) and ﬁtting (9), (10) to
the resulting transient responses. Practically, the device’s
dynamical behavior is interrogated by sampling its switching
rate surface (g(R,v ), assumed to be stationary for sufﬁciently
low voltage stimulation) at multiple constant voltage levels
Vbi, such as the example g(R,Vbi) plots shown as green lines
in Fig. 2.
A. Characterization routine
The characterization routine applied can be described as a
two-stage process repeated multiple times in order to gather
Fig. 3. Example 2-stage characterization sequence and the data exported at
every stage of the device testing procedure. (a) Red pulses signify the triangular
voltage sweep for capturing the static I−V characteristics at R0 shown in
(b). The second stage applies a train of S identical pulses (blue pulses) and the
device RS is read after each pulse is applied therefore capturing the device’s
RS time-response R(t) during the process, seen in (c).
sufﬁcient information regarding the current-voltage and the
switching characteristics of the DUT. An example of this
two-stage process is shown in Fig. 3 while a more detailed
description of the speciﬁc characterization protocol applied
on the tested TiOx devices is given in the Methods section.
During the ﬁrst stage, device RS R0 is read and a triangular,
pulsed, sub-threshold voltage sweep is employed (red pulses),
such so as to not induce any apparent hysteresis in the resulting
I−V response. The outcome is the static I−V characteristic
plot at R0 (Fig. 3(b)). At the second stage, a train of pulses of
ﬁxed voltage amplitude and time duration is employed (blue
pulses) resulting in the typical resistive response shown in Fig.
3(c) which corresponds to an OFF-switching event. Depending
on the polarity of the voltage pulses applied the extracted RS
response may match an ON-switching transition instead. At the
end of stage 2 the device has switched to a new value R′
0, i.e.
at the next iteration both steps are repeated having the device
initialized from a new initial RS and so on. Throughout this
process a) static current-voltage measurements are collected
for different RSs (see Fig. 4) and b) switching characterization
data is gathered for different voltage levels (of both polarities)
starting from different initial RSs (see Fig. 5).
B. Switching parameter extraction algorithm
We seek for a set of parameter values that collectively ﬁts
all exhibited RS time domain responses (Fig. 3(c)) for every
voltage level employed (in the observed device dependent
voltage space of operation) and for every initial RS sampled.
This may be achieved through the following steps.
For the positive stimulation case v >0 the model consists of
parametersAp,tp, that deﬁne the sensitivity function (5) andkp
along with the coefﬁcients for the voltage controlled polynomial
rp(v) (7) that are contained in the window function (6). We

5
Fig. 4. Static I−V characteristics for DUT 1. A number of 8 sets of I−Vs
were exported for different device RSs ranging from 4.85 KΩ to 5.70 KΩ.
Only 5 sets are shown for the sake of clarity. The experimental responses
shown (colored symbols) were ﬁtted with (3) (solid lines). Parameter values
and ﬁtting error are listed in Table I.
assume η = 1 (positive biasing causes the device to switch
towards higher RSs) and that we have extracted experimental
results from multiple voltage levels Vi,i = 1, 2, 3,... . The
procedure is initiated by ﬁtting an RS response R(t)|Vx that
exhibits a clear trend and shape, i.e. it is provoked by a relatively
invasive voltage amplitude Vx. Expression (9) is used for this
ﬁrst ﬁtting action and sp(Vx) is substituted with (5). This
ﬁtting determines the parameter values Ap, tp along with kp
and rp(Vx) at the same voltage level.
Next, the deﬁned Ap, tp, kp parameter values are used to
perform the same ﬁtting on data for the remaining voltage
levels which determine points on rp(Vi). Fitting these to
the corresponding voltage controlled polynomial rp(v) (7)
determines its coefﬁcients.
The same procedure applies on the negative stimulation case
(v <0) where equation (10) is used instead.
V. F ITTING RESULTS
In this section, we validate the ﬁtting performance of
the presented model and the proposed parameter extraction
algorithm. The overall root mean square (RMS) error is deﬁned
as 3.19 % for the presented static I−V ﬁts and 2.07 % for
the ﬁtted dynamic resistive responses. Speciﬁcally we ﬁtted:
a) 2 in house fabricated Pt/TiOx/Pt VCM devices, b) the
Pt/Ta/TaOx/Pt VCM device modeled in [ 24] and c) the
non-ﬁlamentaryTa/TaOx/TiO 2/Ti device modeled in [ 21].
The illustrated static I−Vs were ﬁtted with (3) bearing the
parameter values listed in Table I. Dynamic resistive switching
responses were ﬁtted with (4)-(7) with the parameter values
listed in Table II.
A. Pt/TiOx/Pt case
1) DUT 1: The experimental static I−V characteristics
of Fig. 4 (colored symbols) are typical responses exhibited
by the TiOx samples ﬁtted in this work where the maximum
absolute voltage applied in the triangular pulsed excitation (see
Methods) was kept below |0.5| V to prevent the device from
Fig. 5. Pt/TiOx/Pt DUT 1 case study. Bottom trace: Blue vertical lines
correspond to pulse trains employed for the purpose of device RS modulation.
Red square symbols depict the sub-threshold, triangular, pulsed voltage sweep
for static I−V characterization. Top trace: Evolution of measured physical
device RS (gray crosses) starting from the initial value R0 (green symbol)
responding to device characterization. Solid and dotted lines are reproduced
by the proposed switching model (4) and the VTEAM [ 10] model respectively.
Parameter values for (4) are listed in Table II. VTEAM parameter values are
tabulated in the Appendix. % RMS ﬁtting errors are compared in Table III.
Characterization routine parameters (see Methods): tw,iv = 1.1 ms,tw,∆R =
100µs, Vstart,n =−1.2 V, Vstop,n =−1.5 V, Vstart,p = 1.7 V and
Vstep =|0.1| V.
TABLE I
PARAMETER VALUES AND RMS ERRORS FOR STATIC I−V FITS WITH (3)
Device ap an bp bn % RMS error
TiOx 0.24 0 .24 2 .81 2 .81 2 .49
[24] 0.36 0 .34 1 .83 3 .50 3 .89
switching. The I−V model performance (3) is illustrated with
black solid lines. % RMS ﬁtting errors are listed in Table I.
We should comment here that at a ﬁrst glance, equation
(3) reads very similar to the sinh-based current-voltage
relationships adopted by the models in [11] and [12],
i =Axsinh(Bv) (11)
where A, B are ﬁtting parameters and x is the state variable.
Nevertheless, their port equations are proportional to their
internal state variable x which is limited in the interval [0, 1].
According to their state variable mechanism, for R =Rmax⇔
x = 0⇔ i = 0 which is fundamentally unrealistic behavior
that limits their applicability.
Fig. 5 (top trace) demonstrates the dynamical behavior of
physical (gray crosses) versus simulated device RS (red line)
under the characterization routine (bottom trace). Multiple ON-
and OFF-switching responses for various voltage levels starting
from different initial RSs are ﬁtted with excellent accuracy.
The RS boundary functions, rp(v),rn(v) (7), are used in linear
form for both biasing polarities (see Table II).
2) DUT 2: For DUT 2 we focus solely on its switching
behavior. Fig. 6 (top trace) compares experimental (pale
gray crosses) with ﬁtted (red line) RS responses under the
characterization routine for model parameter extraction (bottom
trace) demonstrating once more excellent performance. A
constant resistive boundary value rp≡Rmax is used for v >0

6
Fig. 6. Pt/TiOx/Pt DUT 2 case study. Bottom trace: Blue vertical lines
depict the pulse trains employed to modulate device RS. Only the switching
mode of the characterization routine is utilized for this device. Top trace: Gray
crosses belong to physical device measurements. Solid and dotted lines are
reproduced by the proposed switching model (4) and the VTEAM model [ 10]
respectively. Parameter values for (4) are listed in Table II. VTEAM parameter
values are tabulated in the Appendix. % RMS ﬁtting errors are compared
in Table III. Characterization routine parameters (see Methods): Vstart,p =
0.6 V, Vstop,p = 0.8 V, Vstart,n =−0.6 V and Vstep =|0.1| V.
TABLE II
PARAMETER VALUES THAT FIT THE PROPOSED SWITCHING MODEL (4) ON
THE CASE STUDY DEVICES
Para-
meters
TiOx
(DUT 1)
TiOx
(DUT 2)
TaOx/TiO 2
[21]
TaOx
[24]
Ap 0.12 743 .47 −2.06· 105 −6.82· 106
An −79.03 −6.80· 104 3.66 7 .25· 107
tp 0.59 6 .51 0 .38 1 .08
tn 1.12 0 .31 0 .015 0 .036
kp 8.10· 10−3 5.11· 10−4 6.13· 10−6 0.017
kn 9.43· 10−3 1.17· 10−3 2.17· 10−6 0.018
rp0 3085 16 .71· 103 1.23· 107 2794
rp1 1862 0 −2.39· 106 −4553
rp2 0 0 1 .21· 105 1973
rn0 5193 29 .30· 103 1.29· 107 857
rn1 378 23 .69· 104 58.07· 104 1135
rn2 0 0 56 .45· 103 675
while for v <0, function rn(v) is utilized in linear form (see
Table II).
One further test regarding the switching behavior of DUT
2 was performed and is shown in Fig. 7(a) (bottom trace).
Conversely to the characterization routine for model parameter
extraction (Fig. 6) which was focused on gathering switching
data under constant bias voltage application (∆R(R,Vb)), we
employed a testing algorithm previously presented in [ 7], so as
to characterize the device’s switching characteristics around the
same initial RS R0 for multiple voltage levels (∆R(R0,v )).
The algorithm operates by employing pulsed voltage ramps of
alternating polarities and the bipolar DUT behavior exhibiting
OFF transitions under positive voltage bias and ON transitions
under negative, was exploited in order to restrict DUT RS
within a narrow resistive range (Fig. 7 - top trace). Each
ramp level was a pulse train that consisted of N pulses/train
Fig. 7. Pt/TiOx/Pt DUT 2 case study. Model validation on alternative de-
vice testing. (a) Bottom trace: Application of successive incremental step pulse
train ramps (ISPTR) for the purpose of gathering switching data of the form
∆R(R0,v ). The demonstrated ISPTR-based testing algorithm is thoroughly
analyzed in [ 7]. ISPTR testing routine parameters: N = 10 pulses/train,
tw = 100µs. Top trace: Resistive response of DUT 2 to alternative device
testing. Gray shadings highlight the most data-populated resistive bands
for ON and OFF transitions with a tolerance of ϵref = 5 % around their
central resistive values (Rref,p , Rref,n ). (b) Pale blue symbols approximate
dR(Rref,p,v ) switching data exported by the ISPTRs applied. Pale red
symbols approximate dR(Rref,n,v ) switching data. Purple solid line is
reproduced by the proposed switching model (4) bearing the parameters
exported by the proposed parameter extraction algorithm and the testing shown
in Fig. 6.
with ﬁxed duration tw (see ﬁgure caption). As device RS was
read and stored after each pulse train applied, the RS around
which most gathered data was clustered was deﬁned as the
central value of Rx for which the interval [Rx−ϵref,Rx +
ϵref ] contained the maximum number of data points. We then
considered that these data points could be used to determine
∆R(Rx,v ) as a fair approximation.
Fig. 7(b) plots switching rate data (round colored symbols) as
a function of bias voltage for ϵref = 5 %. For OFF transitions,
the most populated interval had its center at 12.65 KΩ while
for ON transitions this was deﬁned at 14.90 KΩ. The purple
line in Fig. 7(b) was reproduced by the proposed switching
rate model (4) with the parameter values extracted from the
initial device testing (Fig. 6) showing good agreement with
the measured results thereby supporting the initial assumption
of switching rate surface stationarity (Fig. 2).

7
Fig. 8. Fitted static current-voltage characteristics of the Pt/Ta/TaOx/Pt
device presented in [ 24] with (3). Symbols correspond to data points digitized
from Fig. 4 of the same work. Device RS was deﬁned at the positive read
voltage of Vread = 0.1 V. Parameter values and ﬁtting error for (3) are listed
in Table I.
TABLE III
% RMS FITTING ERRORS OF THE TESTED DYNAMIC MODELS ON DIFFERENT
DEVICE CHARACTERIZATION DATA
Device Model (4) VTEAM (12) DUT RS range
TiOx - DUT 1 0.52 % 0 .88 % 4 .5 KΩ− 6.0 KΩ
TiOx - DUT 2 2.18 % 2 .19 % 10 KΩ − 17 KΩ
TaOx - [24] 3.27 % 15 .54 % 200 Ω − 1000 Ω
TaOx/TiO 2 - [21] 2.32 % 4 .49 % 1 MΩ − 4 MΩ
B. Pt/Ta/TaOx/Pt case
Fig. 8 demonstrates the static I− V ﬁts of the device
presented in [ 24] with the proposed model (3). The % RMS
ﬁtting error is listed in Table I.
In Fig. 9 resistive responses are plotted (pale green symbols)
as a function of applied voltage pulse number for multiple ON-
and OFF- switching transitions provoked by different constant
voltage levels. Green lines match the ﬁtting performance of the
proposed switching model (4). For this case, the r(Vb) points
extracted by the testing routine were ﬁtted with a 2 nd order
expression (see Table II).
C. Ta/TaOx/TiO 2/Ti case
Fig. 10 compares measured (pale blue symbols) versus
simulated (blue lines) RS responses to pulse stimulation for
the analog ReRAM device presented in [ 21]. Model and
experimental results are once again in very good agreement.
As with the previous device case study, (7) takes the form of
a 2 nd order expression (see Table II).
The % RMS errors regarding the accuracy of the switching
model (4) on the RS responses of Figs 5, 6, 9, 10, are
concentrated in Table III. Fitting errors indicate that the
proposed model can be used to ﬁt a wide range of devices
with sufﬁcient accuracy by employing the compact parameter
extraction method presented in Section IV .
Fig. 9. TaOx -based device case study ([ 24]). Figure illustrates RS responses
versus voltage pulse number for different voltage levels for (a) ON- and (b) OFF-
switching transitions. Symbols correspond to RS data measured at Vread =
0.05 mV. Data points were digitized from Fig. 3 in [ 24]. Solid green line
matches the proposed switching model (4) while red dashed line matches the
VTEAM model [ 10]. (a) For v >0:Vb = 0.65 V→ 1 V, Vstep = 0.05 V.
(b) For v < 0: Vb =−1 V→− 1.75 V, Vstep =−0.15 V. Parameter
values for (4) are listed in Table II. VTEAM parameter values are tabulated
in the Appendix. % RMS ﬁtting errors are compared in Table III.
Fig. 10. Ta/TaOx/TiO 2/Ti device case study ([ 21]). Symbols correspond
to experimental a) ON and b) OFF RS transitions measured at Vread =−2 V.
Data points were digitized from Fig. 6 in the relevant manuscript. In both panels
solid lines match the proposed model (4) while dashed lines are reproduced
by the VTEAM model [ 10]. Parameter values for (4) are listed in Table II.
VTEAM parameter values are tabulated in the Appendix. % RMS ﬁtting errors
are compared in Table III.
D. Comparison with a previously proposed generalized, highly
non-linear memristor model
Among the generalized, well established memristor models
published till know, we compare the accuracy of the proposed
model in capturing the dynamical RS responses shown in the
previous subsections versus the VTEAM model presented in
[10]. The state variable equation in the VTEAM model consists
of a threshold-equipped sensitivity function s(v), expressed
with an α-power law function, which is much more ﬂexible
than the simple exponential proposed by Yakopcic [ 11] or
the sinh forms proposed by Laiho [ 12] and Chang [ 13]. For
the VTEAM model, any window function implementation
can be coupled with the sensitivity function s(v) ([16], [17],
[32]). In our case study, we utilize a modiﬁed version of the

8
approximation of the Simmons tunnel barrier model presented
in [17], which is particularly non-linear and is expressed with
a double exponential function for both biasing polarities. The
benchmarked switching model reads,
dx
dt =



koff ( v
uof f
− 1)aof fe−ex/xof f
,v >uoff > 0
kon( v
uon
− 1)aone−e−(x−1)/xon
,v <uon < 0
else 0
(12)
where koff , kon, aoff , aon ,xoff , xon are ﬁtting parameters
and uoff , uon are the threshold voltages. In (12), the state
variablex is dimensionless and practicaly bound in the interval
[0, 1] while increasing its value increases device resistance.
Figs. 5, 6, 9, 10 demonstrate the ﬁtting performance of (12)
on the corresponding physical device characterization data. For
the Pt/TiOx/Pt devices signiﬁed as DUT 1 and DUT 2,
both models present similar accuracy while for the ﬁlamen-
tary TaOx -based and non-ﬁlamentary Ta/TaOx/TiO 2/Ti
devices our model outperforms the implementation expressed
with (12). % RMS errors are compared in Table III.
As with every other generalized memristor model, in order
to ﬁt the VTEAM model on the ReRAM case study responses
shown, the application of certain iterative processes such
as simulated annealing algorithms and gradient descend are
required. Here, we invoked the Eureqa Nutonian A.I. (Artiﬁcial
Intelligence) powered modeling engine software [33]. Eureqa
supports the modeling of derivatives, thus RS time-responses
for each tested device and polarity were fed to this ﬁtting
software which exported the best parameter values for the state
derivative expression (12). The data processing for linking
device RS measurements ( R) with state variable values ( x)
along with the parameter values for (12) can be found in the
Appendix.
On the other hand, the model presented in Section III via
its analytical time response expressions (9), (10) determines
the most suitable parameter values for an R(t)|Vb response in
a single step, allowing the design of the parameter extraction
method described in Section IV . The method is powerful
as it can easily adapt on noisy and/or sparsely populated
data sets, general as it can ﬁt different types of ReRAM
devices and technologies but also extremely practical. This
was demonstrated in [ 34], where a slightly modiﬁed version
of this algorithm was integrated in a characterization platform
previously described in [ 20]. There, we used the system-
available Python interface to a) program the appropriate
experimental routine, b) apply the testing on the device and
c) analyze the exported data to ﬁt ReRAM devices on the
corresponding model expressions. Impressively, all operations
were carried out extremely fast (approximately 3 minutes per
ﬁtted sample) at a click of a button.
VI. V ERILOG -A M ODEL
In every memristor computer model published so far [ 10],
[11], [15], [35], [36], [37] the memory effect of the memristor is
modeled by solving numerically the corresponding model DAE
set. SPICE models perform numerical integration with the use
of a feedback controlled integrator circuit where the value of
AC
device 1
device 2
Fig. 11. Comparison of the ‘numerical’ (blue line) against the ‘analytical’ (red
line) model implementations on the test circuit drawn in (a). Panel (b) plots
the triangular input voltage excitation applied on the anti-series connection
of the devices shown in (a) and compares the circuit’s current responses.
Panels (c) and (d) plot the RS responses of device 1 and device 2 during the
simulation. Both devices were simulated with parameters that corresponded to
the Pt/TiO 2/Pt device referred as DUT 2 in Section IV .
the devices state variable is represented by the voltage across a
unitary capacitance which serves as an integrator of the internal
state variable function. The Verilog-A (V A) models presented in
[38], [39] perform state variable integration by implementing in-
code the forward Euler method as a ﬁnite difference method for
numerical approximation of integration. Nevertheless, these V A
implementations do not make use of the simulator’s dedicated
integration algorithms which are particularly useful in large
scale simulations where the well-established ReRAM models
have been reported to present convergence issues [11], [40].
In the suggested V A model the time-evolution of RS (the state
variable for the proposed model) is calculated analytically thus
in a less compacted fashion (the integration process is omitted)
and therefore faster. Our approach exploits that throughout the
simulation and for the duration of each time-step used by the
simulator, the voltage across the proposed voltage-controlled
ReRAM model is ﬁxed, i.e. the resistive state time-response is
solved analytically with equations (9), (10). The use of these
requires that the initial RS at the beginning of every time-
step and the duration of each time-step are tracked during the
simulation which can be carried out with proper V A coding.
The module that follows the described modeling strategy will
be refered from here after as the ‘analytical’ model.
Here, we validate the proposed ‘analytical’ implementation
in the test circuit shown in Fig. 11(a). This is composed
by the anti-series connection of two ReRAMs driven by a
triangular voltage source. ReRAM devices match the ﬁtted
Pt/TiO 2/Pt case referred as DUT 2 in the preceding section.
Results are compared with those exported from simulations
that perform numerical integration of the model’s DAE set
(see ‘numerical’ model in Methods). The accuracy of the
proposed implementation is veriﬁed as analytical and numerical

9
Fig. 12. Relative simulation speed performance versus crossbar size for
three Verilog-A implementations that model the behavior of the physical
Pt/TiOx/Pt device referred as DUT 1 in Section V . Blue columns
correspond to the proposed analytical model while red and black columns
match two alternative Verilog-A implementations of the benchmark model.
The smoothed VTEAM model (red columns) utilizes (13) in order to smooth
all discontinuous piece-wise functions included in the model’s equations. Black
columns are again reproduced by the VTEAM model where all piece-wise
functions are implemented with the use of the discontinuous step function.
Simulation time results are normalized according to the smoothed VTEAM
model measurements. The proposed ’analytical’ implementation is on average
×2.73 faster than the smoothed VTEAM model.
responses are practically matched. In Fig. 11, the triangular
input excitation and test circuit current response are plotted in
(b) while the RS responses for the two anti-series connected
devices are shown in (c) and (d). The amplitude and period
for input stimulus are Vamp = 2 V and T = 0.1 s respectively.
For the simulation the maximum time step was chosen 0.1%
of the input signal period. The simulation speed-up in both
circuits averaged on 10 runs was ×1.9 for the circuit shown
in Fig. 11(a). The V A codes (‘numerical’ and ‘analytical’) for
the proposed ReRAM model can be found in [41].
We conclude this section by comparing the proposed analyt-
ical model presented in Section V with the V A implementation
of the VTEAM model expressed with (12) for which the
’numerical’ V A coding approach was followed (see Methods).
Model parameters matched the Pt/TiOx/Pt DUT 1 device
presented in Section V . As the I− V relationship is not
inherently deﬁned in the VTEAM model, expression (3) was
utilized for this case with the parameter values listed in Fig. 3
(DUT 1). The simulation speed-up achieved by our proposed
analytical expression was evaluated by simulating with both
models an OFF- followed by an ON- switching event applied
on an entire row of an N×N selector-less crossbar for various
array sizes. Switching was induced by applying voltage pulses
(with suitable values for pulse amplitude and duration) to
modulate the RS of the devices. The parasitic line resistances
were included only to add complexity to the simulated system,
thus, their values were deﬁned unrealistically low, such so as to
allow switching in every device consisted in the row and at the
same time impose different biasing conditions at the terminals
of the devices. Our goal was to benchmark the simulation speed
performance for the compared implementations in a large-scale
ReRAM circuit. Fig. 12 plots simulation speed vs crossbar
size N. The proposed analytical implementation is on average
×2.73 faster than the benchmark model.
VII. M ETHODS
A. Device fabrication and preparation
The in-house TiOx -based samples tested (DUT 1, DUT
2) correspond to micrometer-scale devices featuring a metal-
insulator-metal structure. The process ﬂow started by ther-
mally oxidizing a 6-inch Silicon wafer to create a layer
that serves as an insulator medium. Then, three major steps
were realized to obtain the bottom electrode, active layer and
top electrode consecutively. Each step consisted of optical
lithography, material deposition and lift-off process. The
10 nm platinum layers were deposited for top electrode and
bottom electrode by electron beam evaporation, whilst 25 nm
TiO 2 was deposited by reactive magnetron sputtering. These
fabrication steps resulted in a metal-insulator-metal stack
of Pt (10 nm)/TiO 2(25 nm)/Pt (10 nm) devices. Before use,
all devices were electro-formed using positive polarity (top
electrode at higher potential than bottom electrode) pulsed
voltage ramps. A series resistor was used as a current limiting
mechanism in all cases. Typical electro-forming voltages
were in the range of 7 V− 8 V. Fabrication details for the
Ta/TaOx/TiO 2/Ti and Pt/Ta/TaOx/Pt devices can be
found in [21] and [24] respectively.
B. Characterization routine parameters
The characterization algorithm applied on the TiOx -based
devices is summarized in Fig. 3 and thoroughly illustrated in
Fig. 5. It consisted of multiple pulse trains of S identical
pulses of ﬁxed pulse duration tw,∆R where each applied
train had its own voltage level Vb deﬁned. Pulse trains were
interleaved by triangular sub-threshold pulsed voltage sweeps
(≤| 0.5| V) with ﬁxed pulse duration tw,iv which exploited
the RS modulation provoked by the pulse trains and captured
staticI−V characteristics at multiple RSs of the device under
test. In its ﬂow, the algorithm was carried out by changing
polarity with each applied train and increasing the amplitude
every two trains by a deﬁned voltage step Vstep. The absolute
amplitude of the negative pulses applied scaled according to
Vstep from an initial voltageVstart,n, up to a user deﬁned value
Vstop,n determining the voltage interval of characterization
∆Vc =|Vstart,n−Vstop,n|. Similarly, the positive pulse trains
applied, starting fromVstart,p scaled with the same voltage step
Vstep up to Vstop,p = Vstart,p + ∆Vc and the algorithm was
terminated after pulse trains featuring the ﬁnal characterization
values of both polarities ( Vstop,n, Vstop,p) were applied. The
speciﬁc parameters of the characterization routine employed
on the device under test are given in the caption of Figs. 5 and
6. RS data was gathered throughout the ﬂow of the algorithm
as the initial device RS R0 and the RS after each single pulse
applied were measured. Regardless of the modulated voltage
value used to bias the device for the purposes of switching, all
assessments of RS for the TiOx devices were carried out at
the standard voltage Vread = 0.5 V.

10
C. Data transformation
In order to ﬁt the analytical expression (9), (10) to the
responses reproduced by the tested devices, each pulse was
multiplied by its duration ( tw,∆R), thus, the R(pulseno. )
responses shown in Figs. 5, 6, 8, 9 were transformed into
R(t) responses. Pulse rise/fall times were neglected as they
comprised only a small fraction of the total pulse duration
tw,∆R.
D. Instrumentation
All experiments were carried out using an upgraded version
of the in-house instrumentation previously described in [20].
E. ‘Numerical’ Verilog-A code implementation
The numerical V A module solves the models DAE set (3)-(7)
with the use of the built in V A time-domain integration operator
idt(·) which utilizes simulator dedicated numerical integration
algorithms. As a continuous and differentiable mathematical
description is a mandatory requirement for proper operation of
the iterative solution methods used by differential solvers, all
discontinuous piecewise model functions were reshaped with
the use of the continuous sigmoid approximation,
θi(x) = 1/(1 +exp(−x/bi) (13)
Parameterbi controls the slope of the sigmoid function around
the discontinuous corner points imposed by piecewise functions.
Its value was adjusted accordingly to facilitate simulator
convergence and to keep the models dynamics practically
unaffected. For the functions that involved voltage controlled
conditionals (5), bi was modiﬁed as, bv = 10−6. For RS
related conditionals (6), bR = 10−3. Finally, the steepness
of the exponential function in (13) may impose numerical
overﬂows during the simulation. This was dealt by using
the limiting exponential function limexp(·) which bounds
potentially overﬂowed values by linearizing the exponential
response after an internally deﬁned threshold [42].
VIII. D ISCUSSION AND CONCLUSION
In this work, we have presented a behavioral ReRAM model
that ﬁts staticI−V characteristics and the switching behaviors
of typical VCM and non-ﬁlamentary ReRAM technologies.
The presented model is engineering-friendly as it captures
changes in the device’s internal state variable as projected
macroscopically on its RS. The proposed window function
expression is simple, allowing the derivation of an analytical RS
time-response expression for constant bias voltage application
(R(t)|Vb) which offers a predictive capability for the model
that can be exploited practically in multiple ways. Here, the
analytical expressions (9), (10) were utilized to directly ﬁt
physical RS time-responses of a) 2 in-house fabricated VCM
TiOx -based devices, b) a VCM TaOx -based device ([21]) and
c) a non-ﬁlamentary TiOx/TaO 2 device ([24]), all of which
are tested under the constant biasing conditions imposed by
the compact characterization routine presented in Section IV-A.
The use of (9) and (10) rendered a powerful and general method
that optimized the parameter values by exploiting the clear
shape and trend of the device’s RS responses to constant voltage
application (R(t)|Vb) rather than extracting and working on
measured amount of switching ( ∆R) values which in general
are particularly noisy. The ﬁtting performance of this approach
is demonstrated in Figs. 5, 6, 9, 10 showing excellent efﬁciency
on measured RS time-responses. The overall average % RMS
error for both static I−V and dynamic measurements is 2.63%.
The plots shown in these ﬁgures are characteristic resistive time-
responses of MOx ReRAM devices which are also met in the
WOx -based device presented in [ 13], the FeOx -based device
in [ 23], the Ag/Si device in [ 25], etc. Moroever, as TiOx
devices (also ﬁtted in this work) are considered prototypical
for all VCM devices ([ 43]), it is reasonable to assume that the
proposed model is able to account for this broader class of
ReRAM devices. Whilst the VCM and non-ﬁlamentary device
cases cover practically all metal-oxide devices, there are other
families of memristive, such as STT- (Spin-transfer torque)
and FeRAM-based, (Ferroelectric RAM) devices. The model
has not been constructed to ﬁt such cases, however the extent
to which the fundamental principles used to build the model
are transferable to these is a topic for further investigation.
The proposed model form is explicitly designed to capture
the I−V characteristics of devices and their data-derived
switching behavior. In order to build more general technology-
level rather than device-level models the parameter extraction
procedure must be applied a) on the same device, b) on many
devices repeatedly, in order to capture cycle-to-cycle and device-
to-device variation respectively. Performing a large number
of tests on the same device will offer useful information
regarding the stability of the model, i.e. for how long the
extracted parameters are still an accurate description of the
tested device. Assuming the device presents variable behavior,
each testing applied will lead to a new set of parameters.
Thus, performing multiple tests will have the device trace
a trajectory in model parameter space that will reveal both
intrinsic cycle-to-cycle variability and perhaps longer trends
causing the underlying parameters of the model to fundamental
drift as the device ages/is used. Similarly, for device-to-device
variability, the routine must be ran on multiple devices and
then parameters extracted in order to build a statistical model
of the technology being studied which will manifest itself
as a technology-dependent joint probability distribution. With
enough measurements taken, statistically signiﬁcant results can
be extracted in order to differentiate between in-wafer and inter-
wafer variation. But in all cases, the model extraction routine
presented is the unit cell that is used to generate each and
every data point. As the proposed model expressions are under
constant extension and upgrade, other non-ideal effects, such
as temperature dependence, are being currently incorporated
into the modeling procedure.
Finally, (9) and (10) were exploited to implement a fast
computer model that does not require the integration of the
model’s DAE set, which is a substantial beneﬁt when it comes
to large scale ReRAM-based simulations. The proposed model
was compared with a previously proposed highly non-linear
generalized memristor model showing both increased accuracy
and simulation speed. All in all, its general nature and validated
performance render this model a practical proposal for enabling

11
TABLE IV
PARAMETER VALUES FOR THE STATE VARIABLE EQUATION (12) IN THE
VTEAM M ODEL
Para-
meters
TiOx
(DUT 1)
TiOx
(DUT 2)
TaOx/TiO 2
[21]
TaOx
[24]
kon −400 −1.20· 105 −1.3· 10−2 −5.29
kof f 3100 2150 12 .81 6 .73· 104
uon 0.50 0 .50 2 .00 0 .25
uof f 1.10 0 .50 −2.00 −0.60
eon 4.65 6 .00 14 .75 16 .39
eof f 8.69 1 .00 5 .00 4 .14
wcon 0.45 0 .43 0 .39 0 .39
wcof f 0.39 3 .37· 10−4 0.44 0 .50
Rmin 4850 Ω 10 KΩ 0 .9 MΩ 200 Ω
Rmax 6000 Ω 2 KΩ 4 .2 MΩ 1000 Ω
informed memristor-based system design before committing
to silicon implementations.
APPENDIX
In this section we deﬁne the link between state variable x
and physical device RS measurements R for the Simmons-
based expression (12) and describe the procedure followed to
the end of extracting the most suitable parameter values for
the corresponding dynamic ﬁts shown in Section V via the
Eureqa ﬁtting software tool [33].
State variable and resistance (at a speciﬁc read voltageVread)
are linked with the following equation,
x = R−Rmin
Rmax−Rmin
(14)
where Rmin, Rmax are the window function boundaries. We
notice that for R = Rmin⇔ x = 0 and for R = Rmax⇔
x = 1 which agrees with the state variable mechanism of the
investigated model. Accordingly, switching rates are linked
with,
dx
dt = 1
Rmax−Rmin
dR
dt (15)
As the experimental data were either noisy (Figs. 5, 6) or
sparsely populated (Figs. 9, 10), all physical RS responses
were initially ﬁtted with the minimum mean average error
(MAE) that could be achieved by a log-based function. The
ﬁtted data sets, rather than the initial raw data points, were
then fed to the ﬁtting software (Eureqa) that in turn calculated
the most suitable parameter values for expression (12) based
on the MAE ﬁtting criterion. Speciﬁcally, for the TaOx -based
responses shown in Fig. 9, in order to improve the ﬁtting result
for the OFF- transition cases, the data that corresponded to
the three most invasive responses ( Vb =−1.75V ,−1.60V ,
−1.45V ) were given increased weights relative to the rest data
sets. Notably, the only response ﬁtted accurately was the most
invasive (Vb =−1.75V ). Fitting results are shown in Section
V while the exported parameter values are listed in Table IV.
REFERENCES
[1] D. B. Strukov, G. S. Snider, D. R. Stewart, and R. S. Williams, “The
missing memristor found.” Nature, vol. 453, no. 7191, pp. 80–3, 2008.
[2] L. O. Chua, “MemristorThe Missing Circuit Element,” IEEE Transactions
on Circuit Theory , vol. 18, no. 5, pp. 507–519, 1971.
[3] Bedeschi et al. , “A bipolar-selected phase change memory featuring
multi-level cell storage,” in IEEE Journal of Solid-State Circuits , vol. 44,
no. 1, 2009, pp. 217–227.
[4] A. F. Vincent et al., “Spin-transfer torque magnetic memory as a stochas-
tic memristive synapse for neuromorphic systems,” IEEE Transactions
on Biomedical Circuits and Systems , vol. 9, no. 2, pp. 166–174, 2015.
[5] T. Prodromakis, K. Michelakis, and C. Toumazou, “Switching mech-
anisms in microscale memristors,” Electronics Letters, vol. 46, no. 1,
p. 63, 2010.
[6] S. Gaba, P. Sheridan, J. Zhou, S. Choi, and W. Lu, “Stochastic memristive
devices for computing and neuromorphic applications.” Nanoscale, vol. 5,
no. 13, pp. 5872–8, 2013.
[7] A. Serb, A. Khiat, and T. Prodromakis, “An RRAM Biasing Parameter
Optimizer,” IEEE Transactions on Electron Devices , vol. 62, no. 11, pp.
3685–3691, 2015.
[8] A. Serb et al., “Unsupervised learning in probabilistic neural networks
with multi-state metal-oxide memristive synapses,” Nature Communica-
tions, vol. 7, p. 12611, sep 2016.
[9] S. G. Hu et al. , “Associative memory realized by a reconﬁgurable
memristive Hopﬁeld neural network,” Nature Communications, vol. 6, p.
7522, jun 2015.
[10] S. Kvatinsky, M. Ramadan, E. G. Friedman, and A. Kolodny, “VTEAM: A
General Model for V oltage-Controlled Memristors,”Circuits and Systems
II: Express Briefs, IEEE Transactions on , vol. 62, no. 8, pp. 786–790,
2015.
[11] C. Yakopcic, T. M. Taha, G. Subramanyam, and R. E. Pino, “Generalized
memristive device SPICE model and its application in circuit design,”
IEEE Transactions on Computer-Aided Design of Integrated Circuits
and Systems, vol. 32, no. 8, pp. 1201–1214, 2013.
[12] M. Laiho, E. Lehtonen, A. Russell, and P. Dudek, “Memristive synapses
are becoming reality,” The Neuromorphic Engineer , pp. 10–12, 2010.
[13] T. Chang et al. , “Synaptic behaviors and modeling of a metal oxide
memristive device,” Applied Physics A: Materials Science and Processing,
vol. 102, no. 4, pp. 857–863, 2011.
[14] J. G. Simmons, “Generalized Formula for the Electric Tunnel Effect
between Similar Electrodes Separated by a Thin Insulating Film,” Journal
of Applied Physics , vol. 34, no. 6, pp. 1793–1803, 1963.
[15] Z. Biolek, D. Biolek, and V . Biolkov´a, “SPICE model of memristor with
nonlinear dopant drift,” Radioengineering, vol. 18, no. 2, pp. 210–214,
2009.
[16] T. Prodromakis, B. P. Peh, C. Papavassiliou, and C. Toumazou, “A versa-
tile memristor model with nonlinear dopant kinetics,” IEEE Transactions
on Electron Devices , vol. 58, no. 9, pp. 3099–3105, 2011.
[17] S. Kvatinsky, E. G. Friedman, A. Kolodny, and U. C. Weiser, “TEAM:
Threshold adaptive memristor model,” IEEE Transactions on Circuits
and Systems I: Regular Papers , vol. 60, no. 1, pp. 211–221, 2013.
[18] H. Li, P. Huang, B. Gao, B. Chen, X. Liu, and J. Kang, “A SPICE
model of resistive random access memory for large-scale memory array
simulation,” IEEE Electron Device Letters , vol. 35, no. 2, pp. 211–213,
2014.
[19] Z. Jiang et al. , “A Compact model for metal-oxide resistive random
access memory with experiment veriﬁcation,” IEEE Transactions on
Electron Devices, vol. 63, no. 5, pp. 1884–1892, 2016.
[20] R. Berdan et al., “A u-Controller-Based System for Interfacing Selector-
less RRAM Crossbar Arrays,” IEEE Transactions on Electron Devices ,
vol. 62, no. 7, pp. 2190–2196, 2015.
[21] Y .-F. Wang, Y .-C. Lin, I.-T. Wang, T.-P. Lin, and T.-H. Hou, “Charac-
terization and Modeling of Nonﬁlamentary Ta/TaOx/TiO2/Ti Analog
Synaptic Device,” Scientiﬁc Reports, vol. 5, p. 10150, may 2015.
[22] K. Seo et al., “Analog memory and spike-timing-dependent plasticity
characteristics of a nanoscale titanium oxide bilayer resistive switching
device,” Nanotechnology, vol. 22, no. 25, p. 254023, 2011.
[23] C. Wang, W. He, Y . Tong, and R. Zhao, “Investigation and Manipulation
of Different Analog Behaviors of Memristor as Electronic Synapse for
Neuromorphic Applications,” Scientiﬁc Reports, vol. 6, p. 22970, mar
2016.
[24] P. R. Mickel et al., “A physical model of switching dynamics in tantalum
oxide memristive devices,” Applied Physics Letters , vol. 102, no. 22,
2013.
[25] S. H. Jo et al., “Nanoscale memristor device as synapse in neuromorphic
systems,” Nano Letters, vol. 10, no. 4, pp. 1297–1301, 2010.
[26] U. Celano, Filamentary-Based Resistive Switching . Cham, Switzerland:
Springer International Publishing, 2016, pp. 11–45.

12
[27] C.-W. Hsu et al. , “Homogeneous barrier modulation of TaO/TiO
bilayers for ultra-high endurance three-dimensional storage-class memory,”
Nanotechnology, vol. 25, no. 16, p. 165202, 2014.
[28] F. Corinto and A. Ascoli, “A boundary condition-based approach to the
modeling of memristor nanostructures,” IEEE Transactions on Circuits
and Systems I: Regular Papers , vol. 59, no. 11, pp. 2713–2726, 2012.
[29] I. Gupta et al., “Real-time encoding and compression of neuronal spikes
by metal-oxide memristors,” Nature Communications, vol. 7, p. 12805,
sep 2016.
[30] I. Messaris et al., “A tio2 reram parameter extraction method,” in 2017
IEEE International Symposium on Circuits and Systems (ISCAS) , May
2017, pp. 1–4.
[31] D. Carta et al., “Investigation of the switching mechanism in tio2-based
rram: A two-dimensional edx approach,” ACS Applied Materials &
Interfaces, vol. 8, no. 30, pp. 19 605–19 611, 2016.
[32] Y . N. Joglekar and S. J. Wolf, “The elusive memristor: signatures in
basic electrical circuits,” Physics, pp. 1–22, 2008.
[33] “Eureqa, Nutonian,” 2017. [Online]. Available: http://www.nutonian.com/
[34] I. Messaris et al., “Live demonstration: A tio2 reram parameter extraction
method,” in 2017 IEEE International Symposium on Circuits and Systems
(ISCAS), May 2017, pp. 1–1.
[35] Q. Li, A. Serb, T. Prodromakis, and H. Xu, “A memristor SPICE model
accounting for synaptic activity dependence,” PLoS ONE, vol. 10, no. 3,
2015.
[36] H. Abdalla and M. D. Pickett, “SPICE modeling of memristors,” in
Proceedings - IEEE International Symposium on Circuits and Systems ,
2011, pp. 1832–1835.
[37] R. Berdan, C. Lim, A. Khiat, C. Papavassiliou, and T. Prodromakis,
“A memristor SPICE model accounting for volatile characteristics of
practical ReRAM,” IEEE Electron Device Letters , vol. 35, no. 1, pp.
135–137, 2014.
[38] P. Y . Chen and S. Yu, “Compact Modeling of RRAM Devices and Its
Applications in 1T1R and 1S1R Array Design,” IEEE Transactions on
Electron Devices, vol. 62, no. 12, pp. 4022–4028, 2015.
[39] S. Kvatinsky et al., “Verilog-A for Memristor Models,” CCIT Technical
Report, vol. 8, no. December, 2011.
[40] D. Biolek, M. Di Ventra, and Y . V . Pershin, “Reliable SPICE simulations
of memristors, memcapacitors and meminductors,” Radioengineering,
vol. 22, no. 4, pp. 945–968, 2013.
[41] I. Messaris, A. Serb, and T. Prodromakis, “Dataset for a computationally
efﬁcient verilog-a reram model (v.2),” May 2017. [Online]. Available:
https://eprints.soton.ac.uk/411693/
[42] Accellera, “Verilog-AMS Language Reference Manual,” p. 392, 2009.
[43] K. Szot et al., “TiO2–a prototypical memristive material,” Nanotechnol-
ogy, vol. 22, no. 25, p. 254001, 2011.
Ioannis Messaris is a Phd student at the Physics
dept., Aristotle University of Thessaloniki. His re-
search interests are: transistor and memristor device
modeling and CMOS digital cell modeling.
Alexander Serb (M11) is a research fellow at the
Electronics and Computer Science (ECS) dept., Uni-
versity of Southampton, UK. His research interests
are: instrumentation, algorithms and applications for
RRAM testing, and neuro-inspired engineering.
Spyros Stathopoulos received his Diploma in Ap-
plied Physics and his MSc in Microelectronics and
Nanodevices from the National Technical University
of Athens (NTUA), Greece in 2009 and 2011 respec-
tively. In 2015 he was awarded his PhD in Applied
Physics from NTUA working on shallow junction
engineering in silicon and germanium As of 2016 he
is with the NanoGroup, School of Electronics and
Computer Science, University of Southampton, UK
working on the fabrication and characterization of
memristive devices.
Ali Khiat is an Experimental Ofﬁcer at Southampton
Nanofabrication Centre, University of Southamp-
ton. His current main research interests are micro-
/nanofabrication, optimisation, metrology and char-
acterization of memristors and memristive devices.
Nikolaidis Spyridon (SM88) is a full professor at
the Physics dept., Aristotle University of Thessaloniki.
His current research interests include: modeling the
operations of basic CMOS structures, development
of analytical expressions for the propagation delay
and the power consumption of logic gates, design
of high speed and low power digital circuit and
embedded systems, modeling the power consumption
of embedded processors.
Themistoklis Prodromakis (SM08) is a Professor
of Nanotechnology and EPSRC and Royal Soci-
ety Industry Fellow afﬁliated with the Southamp-
ton Nanofabrication Centre at the University of
Southampton. He previously held a Corrigan Fellow-
ship in Nanoscale Technology and Science within
the Centre for Bio-inspired Technology at Imperial
College and a Lindemann Trust Visiting Fellowship
in EECS UC Berkeley. Prof Prodromakis is a Fellow
of the IET, Fellow of the Institute of Physics, Senior
Member of the IEEE. His background is in Electron
Devices and nanofabrication techniques, with his research being focused on
bio-inspired devices for advanced computing architectures and biomedical
applications..
