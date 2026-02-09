# 10_vteam_improved_numerical_performance.pdf

Received November 24, 2020, accepted February 9, 2021, date of publication February 12, 2021, date of current version February 25, 2021.
Digital Object Identifier 10.1 109/ACCESS.202 1.3059241
(V)TEAM for SPICE Simulation of Memristive
Devices With Improved Numerical Performance
DALIBOR BIOLEK
 1,2, (Senior Member, IEEE), ZDENĚK KOLKA
 3, (Member, IEEE),
VIERA BIOLKOVÁ
 3, (Member, IEEE), ZDENĚK BIOLEK
 1,2,
AND SHAHAR KVATINSKY
 4, (Senior Member, IEEE)
1Department of Electrical Engineering, University of Defence, 66210 Brno, Czech Republic
2Department of Microelectronics, Brno University of Technology, 61600 Brno, Czech Republic
3Department of Radio Electronics, Brno University of Technology, 61600 Brno, Czech Republic
4Viterbi Faculty of Electrical Engineering, Technion—Israel Institute of Technology, Haifa 32000, Israel
Corresponding author: Dalibor Biolek (dalibor.biolek@unob.cz)
This work was supported in part by the Czech Science Foundation under Grant 20-26849S, and in part by the Infrastructure of K217UD,
Brno, Czech Republic.
ABSTRACT The paper introduces a set of models of memristive devices for a reliable, accurate and
fast analysis of large networks in the SPICE (Simulation Program with Integrated Circuit Emphasis)
environment. The modeling starts from the recently introduced TEAM (ThrEshold Adaptive Memristor
Model) and VTEAM (V oltage ThrEshold Adaptive Memristor Model). A number of improvements are
made towards the stick effect elimination and other numerical reﬁnements to make the analysis of large
networks fast and accurate. A set of models are proposed that utilize the synergy of several techniques such as
window asymmetrization, integration with saturation, state equation preprocessing, scaling, and smoothing.
The performance of models is tested in Cadence PSPICE 17.2 and particularly in HSPICE v2017, the latter
on a large-scale CNN (Cellular Nonlinear Network) for detecting edges of binary images. The simulations
manifest the usability of developed models for fast and reliable operation in networks containing more than
one million nodes.
INDEX TERMS Memristor, VTEAM, window function, stick effect, SPICE, cellular nonlinear network.
I. INTRODUCTION
In 2013, a model for current-controlled memristive devices,
called TEAM (ThrEshold Adaptive Memristor Model), was
published in [1]. Two years later, an analogous VTEAM
(V oltage ThrEshold Adaptive Memristor Model) was pro-
posed in [2], which exhibits a voltage threshold, not current
threshold.
The (V)TEAM falls into the category of phenomenolog-
ical models, which are ﬁtted to real memristive devices via
tweaking a set of parameters. In other words, the ‘‘fabrication
details’’ of the device are stamped onto experimental data
which are used for setting the parameters of the universal
(V)TEAM model.
The development of the TEAM model started from the
Pickett model [3], also denoted as Simmons’s Tunnel Bar-
rier Model. Its port (resistive) equation consistently starts
from the physical model of the tunnel effect between elec-
trodes separated by a thin insulating ﬁlm [4]. Although its
state equations are phenomenological, not physical, they
The associate editor coordinating the review of this manuscript and
approving it for publication was Dušan Grujić
.
model accurately enough the large dynamic range of the
time derivative of the tunnel barrier width of this memristive
device.
The Pickett model is rightly regarded as the reference
model of the TiO 2 memristor with a high predictive ability,
since its physical parameters are ﬁtted to the behavior of a
real-world device. Paradoxically, this strong point has also
negative implications: the numerical problems during simu-
lations, caused by the complexity of equations, and by the
impossibility of modeling memristors operating on differ-
ent physical principles than the reference TiO 2 memristive
device.
Developing the TEAM and consequently the VTEAM was
motivated by three aims, namely: 1. To simplify the Pickett
model and thus improve its robustness in the environment of
numerical simulation programs. 2. To make the models more
universal such that they can be ﬁtted to various real-world
memristors via a set of parameters. 3. To provide the required
accuracy of the simulations.
It was shown in [1] and particularly in [2] that the TEAM
and VTEAM meet the above requirements and that they can
be ﬁtted with a high accuracy to previously proposed but
30242 This work is licensed under a Creative Commons Attribution 4.0 License. For more information, see https://creativecommons.org/licenses/by/4.0/ VOLUME 9, 2021

D. Biolek et al.: (V)TEAM for SPICE Simulation of Memristive Devices With Improved Numerical Performance
more complex and numerically exacting physical models of
a variety of current memristive devices.
The V erilog-A and Matlab codes of the models are avail-
able in [5]. The V erilog-A codes are written with a view
to achieving fast computation. It is noted in [1] that ‘‘A
V erilog-A model . . . is more efﬁcient in terms of computa-
tional time than a SPICE macromodel. . . ’’. On the other hand,
the simple Euler method with a ﬁxed time step is used for
the integration of differential equations, with the well-known
impact on accuracy. The same applies to the models in
MA TLAB. On the other hand, the V erilog-A enables partial
corrections of this way generated numerical errors via meth-
ods that cannot be directly used in SPICE, such as resetting
the state variable if it overﬂows/underﬂows its limit value
due to some inaccuracy. A similar approach is used in [5] for
resolving a fundamental numerical problem associated with
the window functions in (V)TEAM – the stick effect, but at
the expense of accuracy.
This work deals with the implementation of (V)TEAM in
the environment of SPICE simulation programs with the aim
of providing robust and fast simulations that utilize sophisti-
cated numerical algorithms. The results described below will
make the universal models of memristive devices accessible
to a wide community of SPICE users.
The paper has the following structure: In Section II
the facts about the (V)TEAM are summarized and poten-
tial problems associated with their implementation in cur-
rent simulation programs are identiﬁed. Several methods
of effective solution of the stick effect are suggested in
Section III. Section IV describes further procedures of
numerical improvements. The relevant versions of the models
are subjected to an exacting test for the accuracy and speed,
with subsequent evaluation. The source codes of the selected
models are available to potential users.
II. (VOLTAGE) THRESHOLD ADAPTIVE MEMRISTOR
MODEL
The current-voltage relationship of the (V)TEAM model can
be chosen arbitrarily to best accommodate the behavior of
concrete modeled device. In [1] and [2], two simple mod-
els are suggested, which consider the linear or exponential
dependence of the memristance RM and the state variable w:
RM (w)= Ron+ (Roff− Ron) w− won
woff− won
(1)
or
RM (w)= Ron
( Roff
Ron
) w−won
woff−won
(2)
where Ron, Roff and won, woff are the limit values of the
memristance and the state variable w in the ON and OFF
regime.
Crucial for the (V)TEAM model are the state equations,
which have the same form for both the TEAM and the
VTEAM. Given below are the equations for the VTEAM (the
equations for the TEAM are generated via the (v, von, voff )
and (i, ion, ioff ) replacement):
dw
dt
=







koff
( v
voff
− 1
)αoff
foff (w), 0< voff < v (OFF)
0, von< v< voff (subTHR)
kon
(
v
von− 1
)αon
fon(w), v< von< 0 (ON)
(3)
Here v is the voltage across the device, von, voff are the
threshold voltages, kon, koff ,αon,αoff are the ﬁtting parame-
ters, and fon(w), foff (w) are the window functions whose role
is to preserve the state variable within the physically realistic
limits w∈ (won, woff ). It is indicated on the right side of (3)
that the state equation has different forms for the OFF, ON,
and subTHReshold regime of operation.
It is demonstrated in [2], [5] that the above model can be
ﬁtted with high accuracy to various experimental memristive
devices even for the symmetric window functions, namely for
fon(w)= foff (w)= f (w) (4)
The V erilog-A and MA TLAB codes of the TEAM and
VTEAM models containing the well-known rectangular,
Joglekar, Prodromakis, Biolek and Kvatinsky windows used
in (3) and (4) are given in [5]. It should be noted that the
last two windows are asymmetric, thus they are not governed
by (4). The Kvatinsky windows, designed to approximate the
complex state equations of the Pickett model, are in the form
foff (w)= exp
[
− exp
( w− aoff
wc
)]
fon(w)= exp
[
− exp
( aon− w
wc
)]
(5)
where aoff , aon, and wc are parameters assumed from the
Pickett model.
The utilization of the VTEAM model in conventional sim-
ulation programs consists in the classical numerical integra-
tion of the differential equation (3), starting from the initial
condition w(0), and in subsequently computing the memris-
tance from the known state variable. The corresponding block
diagram is shown in Fig. 1. The numerical integration is prone
to well-known numerical errors [6], which can be intensiﬁed
just via windowing. Note that the windowing is a numerically
problematic operation, acting in the schematic in Fig. 1 in the
feedback loop together with the block of integrator.
It is demonstrated in [7] that the utilization of window
functions in state equations of ideal generic memristors can
result in fatal numerical errors. The substance of these errors
consists in the co-existence of two types of memory in the
real-world memristor, which is modeled by an ideal generic
memristor: The memory, represented by the so-called Natural
state variable (the charge or the ﬂux), which is boundless in
principle, and its physical implementation, represented by a
physical state variable, for example the width of conductive
VOLUME 9, 2021 30243

D. Biolek et al.: (V)TEAM for SPICE Simulation of Memristive Devices With Improved Numerical Performance
FIGURE 1. Block diagram of the original VTEAM model with
Eqs. (1), (2), (3).
channel w, which has its physical limits. If one-to-one cor-
respondence between the natural and physical state variables
exists, then the corresponding model exhibits all the ﬁnger-
prints of ideal generic memristor. However, if the physical
memory reaches its physical limit, its state is ﬁxed, and its
link to the natural state variable is interrupted. An interesting
consequence of this phenomenon is described in [7]: The
numerical solution of the simulation task is quite different
from the analytic solution. It is alarming that this hidden error
can be revealed only after confronting the simulation results
from a physical viewpoint or with the analytic solution if it is
available for simple simulation tasks.
To avoid this problem and to speed-up the simulation of
networks containing ideal generic memristors, a method for
state-space transformation is developed in [8]. This method
also prevents another problem, known as the stick effect,
which is associated with the limit states of the physical state
variable.
Luckily for the (V)TEAM, the problem of the above hidden
errors does not apply, since these models are not classiﬁed
as ideal generic memristors. The corresponding extended
memristors cannot be described via charge-ﬂux constitutive
relations, and therefore the problem of natural versus physical
state variable does not exist here. However, it is obvious from
the state equation (3) and from the diagram in Fig. 1 that
the stick effect in unavoidable in (V)TEAM for an arbitrary
symmetric window (4), which takes zero values at boundaries
(such as the rectangular, Joglekar and Prodromakis window),
so the method of state space transformation can play an
important role in such cases. On the contrary, the Biolek win-
dow, designed in [9] with discontinuities at boundary states
or the Kvatinsky window prevents the stick effect reliably.
It is obvious that such a discontinuity, frequently regarded as
disadvantage, is in fact an effective tool for avoiding such a
problem.
Since the VTEAM is ﬁtted in [2] to several real-world
memristive systems just by using symmetric windows (5),
most frequently the rectangular window, the stick effect
must be resolved. It can be read from the source codes
in [5] that the solution may be via a parameter called in [5]
p_window_noise. The corresponding algorithm slightly mod-
iﬁes the behavior of the window function depending on the
direction of the memristor current. For example, if the state
variable approaches its upper limit woff , then, after crossing
the level woff –p_window_noise, the value p_window_noise
is systematically subtracted in the Euler integration formula
from the computed value of the state variable until w leaves
the boundary region (w off –p_window_noise, woff ). This pro-
cedure is applied accordingly also for preventing the stick
effect near the lower limit won. A similar remedy is suggested
in [10], [11], when a small number, added to the window
function, ensures that the right side of the state equation is
not multiplied by zero at the boundaries. The limit states can
also be provided via controlled switches [12] or by tools of
behavioral modeling [13]. An interesting solution consists
in the replacement of the window function by an integrator
with artiﬁcial limitation of its boundary states via diode lim-
iters [10]. The low quality of such a limitation, caused by the
speciﬁc shape of the current-voltage characteristics of diodes,
is a potential disadvantage. Classical behavioral modeling of
ideal diodes can lead to numerical problems.
Other potential numerical problems are hidden in the state
equation (3): Model discontinuities during the transition of
memristor voltage through threshold levels, multiplication of
extremely large and small numbers, and the variables taking
extremely large or small values that can overﬂow or under-
ﬂow the SPICE limits. The inspiration for resolving these
issues may be found in the general procedures described e.g.
in [6].
The following Section suggests three effective methods
of avoiding the stick effect: window asymmetrization, inte-
gration with saturation, and analytic pre-processing of state
equations, also denoted below as the transformation of state
variables.
III. AVOIDING STICK EFFECT
A. WINDOW ASYMMETRIZATION
Although the utilization of standard symmetric window func-
tions (4) in the state equations (3) leads to simple models,
all these window functions, which are zero at the boundaries
of the state variables, inevitably cause the stick effect if
the memristor acquires one of its limit states. This effect
is perhaps most evident when trying to get a maximum
simpliﬁcation of the model by using the rectangular window.
On the other hand, the stick effect can be easily removed
via asymmetric window functions. Experiments show that
when the symmetric window is replaced by an asymmetric
window, for example the Biolek window function, then, after
some prospective trimming of model parameters, the ‘‘small-
signal’’ behavior of both models is identical, and the simu-
lation of the ‘‘hard-switching’’ regime is robust and without
the stick effect.
Asymmetrization of standard window functions is trivial.
For example, the simplest rectangular window
f (w)=σ (w− won)−σ (w− woff ) (6)
whereσ is the Heaviside step function, can be made asym-
metric as follows:
foff (w)=σ (woff− w), fon(w)=σ (w− won) (7)
30244 VOLUME 9, 2021

D. Biolek et al.: (V)TEAM for SPICE Simulation of Memristive Devices With Improved Numerical Performance
Equation (7) means that in the OFF state, when the state
variable w increases towards the limit value woff , the win-
dow function foff is zeroing if this limit is reached, and the
state variable stops moving. After changing the state to ON,
the window function changes to fon which attains the value
1 for the limit state woff . That is why the state variable
unsticks from this boundary and moves back towards the
state won.
A typical implementation of (3) into the simulation pro-
gram consists in the utilization of a pair of current sources
ioff and ion in parallel, which charge the integrating capacitor.
The OFF or ON source is controlled by the corresponding
formula (3) and is active only for the respective values of
the driving voltage, thus for v > voff or v < von. It can be
accomplished via multiplying the current by a logic function,
which provides the value 1 for v > voff and 0 for the
remaining cases, or the value 1 for v< von and 0 otherwise.
The asymmetric rectangular window can be then introduced
by a similar logic function, which sets to zero the derivative
of the state for w> woff or w<won:
ioff= koff
( v
voff
− 1
)αoff
(v> voff ) (w < woff )
ion= kon
( v
von
− 1
)αon
(v< von) (w > won) (8)
The prospective numerical problems caused by the discon-
tinuities in (8) can be resolved via the smoothing techniques
described in Section IV .
B. INTEGRATION WITH SATURATION
There are two methods of how to maintain the state variable
within given limits: Either by interrupting the driving sig-
nal of the integrator when the limit state is reached, or via
limiting the integrator states independently of its excitation.
The ﬁrst method is used for windowing, the second can be
implemented by modeling the saturation of the integrator
output.
The integration with saturation is advantageous in the sense
that it avoids the stick effect and simultaneously prevents the
state variable from swinging out of its natural limits due to
numerical errors. This method is mentioned in several works,
e.g. in [10]. An example of SPICE implementation is given
in Fig. 2. Modeling the diodes may be an issue, since the
diodes should behave as ideal switches with zero threshold
voltage and zero voltage drop in ON state. The experiments
described in Section V led to the model of ideal diode in
Fig. 2. The model is based on the SPICE modeling of a
voltage-controlled switch whose resistanceRS depends on the
control voltage vc according to a smooth function, thus with
the continuous derivative dRS /dvc.
With reference to the dynamic range of the number rep-
resentation in the program, the ratio between the switch
resistances in the OFF and ON states should be chosen below
1012 [14]. In the case of convergence problems, the difference
between the Von and Voff values should be increased, and the
FIGURE 2. Spice implementation of integrator with saturation. The diodes
should behave as ideally as possible but not causing numerical problems.
Here, the diode switches between the OFF and ON states within a narrow
region of voltages, from 0V (OFF) to 100mV (ON). The switch model syntax
may vary in different SPICE simulators.
corresponding voltage drop on the diodes can be compensated
by the respective modiﬁcations of the levels won and woff .
The questionable windowing can be avoided, if the inte-
gration with saturation is utilized. On the other hand, both
methods can be combined in order to model the boundary
effects more precisely, but the window function cannot be
zero at boundaries [10]. Basically, various types of shaping
the current-voltage characteristics of diodes might be used for
such a modeling.
C. STATE EQUATION PREPROCESSING
The state equation (3) can be rewritten in the form
dw
dt = g(v)f (w, sign(v)) (9)
where sign(v) is the sign function, and
g(v)= k(v)
( v
vt (v)− 1
)α(v)
, (10)
f (w, 1)= foff (w), f (w,−1)= fon(w), (11)
k(v) is koff , kon, 0 for OFF, ON, subTHR state,
vt (v) is voff , von for OFF, ON state,
α(v) isαoff ,αon for OFF, ON state.
The window function and the voltage-dependent parame-
ters vt ,α can be for the subTHR state deﬁned in an arbitrary
but mathematically correct way.1
It is obvious from (4), (10) and (11) that the original
VTEAM model can work with the classical window func-
tions, which depend only on the state (see, for example,
the Joglekar or Prodromakis window), but it generally takes
1Since k= 0 for the subTHR state, the window function can be deﬁned as
dependent on the sign of voltage. Alternatively, the window function could
have been deﬁned as zero for the subTHR state, with g(v) playing no role.
VOLUME 9, 2021 30245

D. Biolek et al.: (V)TEAM for SPICE Simulation of Memristive Devices With Improved Numerical Performance
FIGURE 3. Window function f (w ) and the corresponding function F (w ).
windowing to be dependent on the signal direction (a typical
example is the Biolek window).
Symmetric windowing
In the ﬁrst step, consider the simple case of symmetric
windows (4). Then the state equation (9) holds:
dw
dt = g(v)f (w). (12)
Re-arranging and integrating both sides of (12) yield
w∫
w0
dw
f (w)= G(w, t)= F(w)− F(w0),. (13)
where
G(w, t)=
t∫
t0
g(v)dt (14)
is the integral of g(v) with respect to time, F(w) is the prim-
itive function of the function 1/f (w), w0 is the initial state at
time t0, and -F (w0) is a constant of integration.
Figure 3 shows the relationship between the window func-
tion and F(w). The graph of F(w) is drawn for an arbitrarily
chosen constant of integration. The Figure illustrates the
condition where the operating point starts moving from the
initial state w= w0 (point ) towards point . According to
(13), after reaching this point, the F function changes by the
value of the integral G (14).
It can be easily veriﬁed that the F function, which cor-
responds to the rectangular window, is in the form of the
piece-wise-linear function (dashed line in Fig. 3).
As demonstrated in [8], the general smooth window func-
tion, which is a smooth approximation of the rectangular
FIGURE 4. FI functions as an alternative to windowing.
TABLE 1. F functions for selected window functions.
window, is transformed into an F function which is mono-
tonically increasing within the interval (w min, wmax) (solid
curves in Fig. 3). Then the inverse FI( ) of the F func-
tion from Fig. 3 exists, and (13) can be rewritten in the
form
w= FI(G+ F(w0)) (15)
It is obvious from Fig. 4 that, when the function FI( ) is
known, it can be used for computing the state variable w
directly from the variable G. The initial condition w0 must be
known for this computation as well as the original function
F( ).
The F functions for the Joglekar and Prodromakis window
functions f (w) are derived in [8]. The FI functions for general
window functions can be found via formula (13) and the
subsequent inversion of the F function. In addition, a univer-
sal sigmoidal approximation of the parametric FI function is
proposed in [8].
Analytical expressions of F functions for several win-
dows are summarized in Table 1. The symbols 2F1 and Ei
denote the hypergeometric functions and the exponential inte-
gral. The F function for the Prodromakis window cannot be
derived in terms of known mathematical functions.
30246 VOLUME 9, 2021

D. Biolek et al.: (V)TEAM for SPICE Simulation of Memristive Devices With Improved Numerical Performance
FIGURE 5. Block diagram of the simulation using the F and FI functions.
The concept of using FI functions instead of classical
window functions leads to the original procedure of eval-
uating the VTEAM model in Fig. 1 being modiﬁed to the
block diagram in Fig. 5. The voltage v is transformed into
g(v) via the algebraic equation (10) and then integrated
with the initial condition computed as F(w0). The resulting
waveform G is transformed via algebraic FI function (15)
into the state variable w, which controls the memristance
by (1) or (2). This transformation requires a corresponding
shift of the G waveform, so F(w0) is added to G according
to Fig. 5.
Recall the consequence of the original state equations (3):
if the window function attains the value zero, the state vari-
able w stops moving at this moment. In the modeling dia-
gram in Fig. 5, the variable w is derived from another state
variable G, which is the result of integrating an auxiliary
variable g. If the memristor reaches its boundary state and
the state variable w is stopped, it is necessary to interrupt the
integration of variable g, thus the movement of the state G
must be stopped. Otherwise, the model would behave as a
memristor with an inﬁnite depth of memory, which is a fea-
ture of ideal memristor. In combination with the given form
of the differential equation (3) of VTEAM, it would imply an
inﬁnite increase in the state variable G, because the function
g in the integral (14) evolves in time as asymmetric, thus
with a nonzero DC component. This ﬁnding points out the
unsuitability of the given method for modeling memristors
with window functions of type (5), which decrease to zero
asymptotically. The ‘‘stop at boundaries’’ operation in Fig. 5
cannot be implemented via interrupting the signal g(v), which
drives the integrator, since it would cause deﬁnitive stick-
ing of the integrator state. More convenient is introducing
the saturation limits of the integrator, which are computed
to be in coincidence with the limit values of the state
variable w.
Comparing Fig. 5 with Fig. 1, we can conclude that the
integration of the differential equation is now provided by the
integrator in a feedforward conﬁguration. The only feedback
is of the ‘‘stop at boundaries’’ type, which can be provided
by the integration with saturation. On the other hand, for the
memristor with a simple rectangular window, the diagram
in Fig. 5 can be reduced to the initial diagram in Fig. 1,
because the F and FI functions are linear within the limits
won and woff , namely F(x)= x. The model from Fig. 5 can
therefore be advantageous for stick effect elimination for
FIGURE 6. Window functions fon(w ), foff (w ), and the corresponding F
functions of the on and off types.
window functions of general forms with zero values at
boundaries.
Asymmetric windowing
Now consider a more general asymmetric windowing (11),
when the window function depends on the direction of
memristor voltage or current.
Fig. 6 illustrates a sketch of fon and foff functions that apply
to positive v > voff and negative v < von, respectively. The
arrows denote the corresponding directions of changing the
state variable w, or, the sign of the time derivative of the state
variable in (3). For positive v > voff , the operating point
moves in the (f,w) coordinates from the initial point  with
w= w0 to the right along the foff (w) curve, and the state vari-
able w increases towards its upper limit woff . Simultaneously,
the time-integral G according to (14) increases along the blue
curve ‘ ‘off’ ’. Fig. 6 shows that at the moment when the state
variable reaches the value of w and the voltage decreases
below voff threshold the operating point stops moving in the
(F , w) coordinates at point , and after the voltage decreases
below von, the operating point switches to the position  on
the fon curve and moves along it back towards won. After
reaching the position , the memristor switches to the off
state and the operating point moves to the position .
The trajectory of the operating point in the (F , w) coor-
dinates (see Fig. 6) or also in the (w, F) coordinates
(see Fig. 7) is characterized by discontinues changes of the F
function during off-on and on-off switching. Simultaneously,
however, the G variable changes continuously: the move of
the operating point from position  to  and from position
 to  is accompanied by a change of the variable G by the
VOLUME 9, 2021 30247

D. Biolek et al.: (V)TEAM for SPICE Simulation of Memristive Devices With Improved Numerical Performance
FIGURE 7. Principle of off-on switching: In the off regime, the operating
point proceeds along the blue curve in the arrow direction. At the point
(Gx , wx ), the voltage decreases below von and the memristor switches
from the off to the on regime. The operating point continues to move
back along the shifted red curve.
values of Goff and Gon, where
Goff=
w∫
w0
dw
f (w), Gon=
w′
∫
w
dw
f (w) (16)
Since
Goff+ Gon=
w′
∫
w0
dw
f (w), (17)
the variable G does not change when switching from point 
to point . The same holds for switching from the ON state
to the OFF state. The continuous nature of the G variable
is also obvious from the fact that it is integrated from the
signal g(v).
The block diagram in Fig. 5 is modiﬁed for asymmetric
windowing according to Fig. 8.
The immediate state of the memristor is evaluated via a
comparison of the memristor voltage and the threshold levels
voff and von in the block ‘‘state on-off’’. The value−1 or 1 is
assigned to the ON state or to the remaining OFF states and
subTHR according to (3). This state then controls the utiliza-
tion of the transforming functions F and FI in computation,
and the value of state is also used for evaluating the time
instant of the state change in the block ‘‘state change’’. This
evaluation is crucial for computing the auxiliary variable wini
(see Fig. 8), which is the last coordinate of the ‘‘changeover
points’’ in Fig. 6 (for example w0 for point  or w for
points  and ) and which is the starting coordinate for the
operating point moving along the F(w) characteristic as a
consequence of the evolution of the variable G. The value of
wini is evaluated via the following algorithm:
wini=



w0 initialization
w state change
last value otherwise
(18)
FIGURE 8. Block diagram of the simulation for the case of asymmetric
windowing.
At the beginning of the simulation (time = 0), the initial
condition w0 is assigned to wini. Every change of the state
from ON to OFF or from OFF to ON, which is identiﬁed in the
‘‘state change’’ block in Fig. 8, is accompanied by sampling
the state variable w, and the ‘‘old’’ value wini is rewritten by
this sample. When the state is not changed, the variable wini
is not changed either.
The operation of the ‘‘state change’’ block can be accom-
plished via the logic operation
state_change= (state̸= last(state)) (19)
If the values of state are different in the current and pre-
vious simulation steps (i.e. if the state was changed), then
state_change= 1, otherwise state_change= 0.
Finding the values of waveforms in the previous simulation
step is not trivial in SPICE programs working with adaptive
time step in the transient analysis. Starting with the version
16.5, the function STA TE can be used in ORCAD PSpice.
A similar function LAST is available in Micro-Cap. HSPICE
does not provide such a possibility. The cross function can
be used in V erilog-A. It detects the state change and enforces
the time step of analog solver in the vicinity of the point of
discontinuity.
IV. OTHER NUMERICAL IMPROVEMENTS
A. SCALING, LOG-ANTILOG
A commonly used format on PCs is the double-precision
binary ﬂoating-point with number representation from 2−1022
to 2 1023, thus from about ca 10 −308 to 10 308. This range
can be violated during the execution of some mathemati-
cal operations, for example the evaluation of the window
functions (5), when exp(–exp(–6.6)) = 5.6521× 10−320.
In reality, the layout may be even worse, because various
simulation programs apply stricter limits to internal variables
or voltages and currents. For example, the smallest nonzero
positive number which PSPICE and HSPICE can process is
10−30. The corresponding argument x of the above function
exp(–exp(x)) is 4.235. For higher value of this argument,
the window function returns zero.
Even worse results can be expected if the results of the
computations, represented by high numbers, are evaluated as
30248 VOLUME 9, 2021

D. Biolek et al.: (V)TEAM for SPICE Simulation of Memristive Devices With Improved Numerical Performance
the voltages or currents of controlled sources. The PSpice
limits for voltages and currents are 10 10 V and 10 10 A, and
their overﬂow leads to the termination of the simulation run
due to convergence problems. These limits are rather higher
for HSPICE, LTspice, and Micro-Cap.
The fact that PSPICE and HSPICE handle incorrectly
parameters smaller than 10−30 in magnitude should be taken
into account when working with physical quantities that fre-
quently appear in physical models of memristive devices,
such as the electron mass (9.109 × 10−31 kg) or the Planck
constant (6.626× 10−34 Js).
For the simulation of (3), the above issues can be resolved
via classical procedures known as scaling and log-antilog:
The quantities which, in principle, take extremely low or
high values, particularly those which are represented via
voltages or currents, must be scaled in order to ﬁt them
within acceptable limits. A typical example is the width of
the conductive channel of the TiO 2 memristor, which is in
the range of units of nanometers. The scaling of the state
variable also affects its time derivative, and therefore it must
be accompanied by the corresponding scaling of the right
side of the differential equation (3). Another example is the
integration of the differential equation in SPICE via charging
the capacitor from a current source, whose current is given by
the right side of (3). The dynamic range of this current should
be scaled to values that match the typical set of error criteria.
Concretely for the state equation (3) it means to multiply the
coefﬁcients kon and koff by a proper scaling factor, and to
divide the original capacitance (1 Farad) of the integrating
capacitor by the same factor.
The right side of (3) is given as a product of three terms;
the last two of them can signiﬁcantly change during the
simulation run. For example, the term (v/v off –1)αoff can take
extremely high values whereas the multiplying window func-
tion can produce values near zero, potentially beyond the
numerical limits of the program. In such cases, it is useful
to compute the logarithms of such terms, which on principle
cannot be zero (for example the window functions (5)), to sum
them and perform the inverse exp operation.
B. SMOOTHING
Equations (8) of VTEAM for the rectangular window can
be easily generalized to arbitrary window functions as
follows:
ioff= koff
( v
voff
− 1
)αoff
foff (w) (v > voff )
ion= kon
( v
von
− 1
)αon
fon(w) (v < von) (20)
The discontinuous functions modelling the threshold prop-
erty introduce discontinuities into the simulated waveforms
and become a potential source of numerical problems. It is
therefore useful to replace them by their smooth approx-
imations, thus by continuous functions with continuous
ﬁrst derivatives. Experiments described in Section V con-
ﬁrmed the usefulness of the smooth functions LTH and HTL
TABLE 2. VTEAM parameters of memristor from [15].
(Low-To-High and High-To-Low) as the replacement of the
discontinuous functions (v > voff ) and (v < von) from (20):
LTH(x)=



0, x<−0.5
2× 4−(x+1)(x−0.5)2
− 1, −0.5≤ x≤ 0.5
1, x> 0.5
(21)
HTL(x)=



1, x<−0.5
2× 4(x−1)(x+0.5)2
− 1, −0.5≤ x≤ 0.5
0, x> 0.5
(22)
where the auxiliary variable
x= v− vL+vH
2
vH− vL
(23)
is derived from the voltage v and the limits vL and vH .
The functions (21) change their values continuously for the
voltage v within the interval between vL and vH , not discon-
tinuously at the point v= voff or v= von.
The corresponding smoothing (21), (23) can also be used
as a remedy for other discontinuities described in Section III.
V. BENCHMARK TESTING
A. METHODOLOGY OF TESTING
The models were tested in two steps: First, each model was
analyzed with sinusoidal driving voltage in Cadence PSpice
17.2. Then, the models successfully passing the ﬁrst test
were used for testing in a large CNN (Cellular Nonlinear
Network) for detecting edges in the image according to [15].
The HSPICE v2017 was used for the simulation of network
containing 5000 to 200,000 memristive cells.
The VTEAM parameters were ﬁtted to the memristor used
in [15]. The results are summarized in Table 2.
Since von > 0, voff < 0, it is obvious that the memristor
from [15], in contrast to the original equations (1) - (3),
decreases/increases its memristance for positive voltage v>
von / negative voltage v < voff . This can be taken into
consideration by formally arranging the state equation (3)
such that the ON / OFF state corresponds to a voltage higher
than von / lower than voff [2].
The port equation was in the form of (1) with scaled limits
of the state variable won= 0, woff= 1, wini= 0.375.
VOLUME 9, 2021 30249

D. Biolek et al.: (V)TEAM for SPICE Simulation of Memristive Devices With Improved Numerical Performance
TABLE 3. F and FI functions for modeling selected symmetric and
asymmetric window functions∗).
The Joglekar and Biolek windows, used in several mod-
els, were considered with the parameter p= 10. The corre-
sponding nonlinear functions F(w) for these windows were
computed in Matlab for their prospective implementation in
Spice as table-based functions. Also their inversesFI(F) were
derived. However, since such functions cannot be directly
imported into HSPICE, their analytical approximations were
found, and the corresponding formulae are summarized
in Table 3. Finally, they were used for simulations in HSPICE
and also in PSpice.
Simulations were run on the HP Z840 Workstation,
Intel R⃝CPU E5-2690 v3 @ 2 × 2.60 GHz, 512 GB RAM,
Windows 10 Pro.
B. TESTING UNDER SINUSOIDAL EXCITATION
The following 10 models were tested:
R:
Model employing asymmetric rectangular window (8).
R_d:
Model with symmetric rectangular window and integrator
with saturation, implemented by ideal diodes with parameters
according to Fig. 2.
R_s:
Modiﬁed R model with smooth approximations (21)–(23).
Parameters for smoothing k(v) from (10) are: vL = von -
0.1V ,vH= von (HTL), vL= voff , vH= voff+ 0.1V (LTH),
parameters for smoothing the rectangular window: vL= 0V ,
vH= 1V (HTL), vL= 0.9V ,vH= 1V (LTH).
R_t:
Model with the rectangular window, implemented byF and
FI transformations according to Fig. 5.
J:
Model employing the Joglekar window and the integrator
with saturation.
J_s:
Modiﬁed J model with smoothing discontinuities in k(v)
from (10) and parameters from R_s model.
J_t:
Model with the Joglekar window, implemented by F and
FI transformations according to Fig. 5.
B:
Model with the Biolek window and the classical integrator
without saturation.
B_s:
Modiﬁed B model with smoothing discontinuities in k(v)
from (10) and parameters from R_s model.
B_t:
Model with the Biolek window, implemented by F and FI
transformations according to Fig. 8.
All the models were driven by sinusoidal voltage with
various amplitudes and repeating frequencies. Regarding a
high value of the parameter p = 10 used in the window
functions, the models exhibited a good match in the simulated
responses. The results of transient analysis for the B and B_t
models are shown in Fig. 9.
The performance of models was evaluated under their
uniﬁed excitation via 2V/10 Hz sinusoidal voltage. Simula-
tion time, accuracy, model sensitivity to simulation options
(vntol, Gmin, step ceiling), and nonconvergence liability
were compared. Table 4 summarizes the results of transient
runs within 10 repeating periods of the driving signal with a
maximum timestep of 0.5ms and skipbp directive.
Concerning the simulation time, the fastest is the R_d
model, closely followed by the R_t and J, J_t, and B models.
A common issue of the R and R_s models with rectangular
window is the difﬁculty of preserving the accuracy and,
simultaneously, low sensitivity to simulation options. The
weak point of the classical R model (asymmetric window
without smoothing) is related to an inaccurate evaluation of
the condition w < woff or w > won in (8). Consequently,
the limit values of the state variable are computed incorrectly.
The accuracy can be increased via decreasing the step ceiling
but at the cost of slowing down the simulation. The speed
of the computation strongly depends on the analysis options
(e.g. vntol= 0.1m, Gmin= 1e-14 lead to a forty-fold decel-
eration of the transient analysis in comparison to the standard
settings).
The R_d model is very fast, with a low sensitivity of the
analysis speed to analysis options. The threshold voltage
of diodes can be relatively high (ca 100mV), but then the
saturation levels of the integrator should be adjusted to exact
values via a modiﬁcation of the voltages Vhigh and Vlow.
Decreasing the diode threshold leads to a signiﬁcant decel-
eration of the analysis, which can be eliminated in part via
a proper selection of the analysis options (particularly vntol
and Gmin).
For a proper operation of the R_s model, double smoothing
of discontinuities in the state equation (threshold property and
state variable limitations) must be performed. The model is
then accurate, with a low sensitivity to the analysis options.
Though the simulation times are longer than without smooth-
ing, the behavior is robust and the precision of computation
is high even for a higher difference of the levels vH and vL
30250 VOLUME 9, 2021

D. Biolek et al.: (V)TEAM for SPICE Simulation of Memristive Devices With Improved Numerical Performance
FIGURE 9. Results of the transient analysis of memristor B- and B_t
models under sinusoidal voltage excitation; (a) v-i hysteresis loops of B
model for various frequencies, (b) waveforms of memristor voltage and
current, (c) waveform of state variable wb of B model and state variable
wb_t and variable G (14) of B_t model, (d) waveforms of state and
state_change (19) signals.
deﬁning the width of the transition zone in the denominator
of (23).
The R_t model is very accurate and fast, and it is not nec-
essary to specially set the simulation options for its optimal
behavior. From this point of view, it can be evaluated as
the most suitable model for a memristor with a rectangular
window.
The results of testing all the variants of models with the
Joglekar window can be generalized to memristor models
with different symmetric windows which are described via
unambiguous polynomial functions of the state variable (such
as the Prodromakis window and others): To avoid the stick
TABLE 4. Model comparison, sinusoidal excitation.
effect, the classical variant requires a diode limiter of the
integrator output, which slows down the simulation for diodes
with a relatively low threshold voltage. Although the model
based on the transformation of the state variable does not use
this direct limitation, the simulation times can be extended
due to evaluating the nonlinear functions F and FI, particu-
larly if they are modeled as tables. In the end, however, the J
and J_t models are comparable to the best models with a
rectangular window in terms of speed and accuracy, and the
J_s model performs even better than the R_s model does.
The B and B_s models can also be evaluated positively.
The natural advantage of the Biolek window is that it does not
cause the stick effect, so it is not necessary to take measures
against it, which usually leads to slowdowns in calculations
or to a reduction in accuracy.
Convergence problems were recorded in the B_t model,
i.e. in the model using asymmetric windowing, implemented
by the algorithm from Fig. 8. It turns out that the core of the
problem lies in the need to accurately identify the moment
of change of the memristor state according to (19) and sub-
sequent sampling of the state variable w for updating the
initial condition wini. The SPICE programs are not equipped
with tools for an accurate identiﬁcation of the time instant
of occurrence of an event (e.g. changes in the memristor
state), as in VERILOG-A, for example, and so memristor
models with asymmetric windows according to Fig. 8 should
be implemented on other platforms, e.g. HSPICE with the
possibility of utilizing the VERILOG code.
Figure 9 (a) shows the simulation of the pinched hysteresis
loops of a memristor with the Biolek window (B) driven
by a sinusoidal signal with an amplitude of 2V and various
repeating frequencies. The Figures 9 (b), (c), (d) demonstrate
simulations with the B and the B_t model for a frequency
of 10 Hz. The results are in full agreement with the knowledge
that the state variablew cannot be changed in the subthreshold
region, that is to say when the driving voltage is within the
interval (v off , von)= (–0.8V ,+ 0.8V). Figure 9 (d) sum-
marizes the waveforms of the auxiliary quantities state and
VOLUME 9, 2021 30251

D. Biolek et al.: (V)TEAM for SPICE Simulation of Memristive Devices With Improved Numerical Performance
FIGURE 10. (a) Structure of CNN. A cell (i , j ) with connections to its
nearest neighbors is drawn with a solid line. (b) Circuit realization of the
cell.
state_change. It is obvious that, in this case, the state of the
memristor changes at the moments when the state variable
w is practically constant. This contributes to alleviating the
convergence problems that may occur when sampling a state
variable that is changing dramatically over time. The accu-
racy of the simulation of the B_t model is strongly related to
the setting of the saturation levels of the integrator, the output
of which is the quantity G (see Fig. 8). For a correct operation
of the model B_t it is necessary to carefully set the error
criterion VNTOL so that it is at least one order of magnitude
lower than the difference in the threshold levels of the control
voltage of the switch in Fig. 2 in the diode model, which is
used to limit the output of the respective integrator. Even so,
we do not avoid convergence problems that can occur due
to changes in the conditions outside the model, for example
when the network of interacting components is changed or
the driving signal parameters are modiﬁed.
Therefore, all models from Table 4 apart from the
B_t model advance to the subsequent stage of testing in
large CNNs.
C. TESTING IN LARGE CNNs
The suitability of the designed models for the simulation of
large memristive networks was tested via a CNN (Cellular
Nonlinear Network), which allows a simple scaling of the
simulation problem complexity. The used EDGE M-CNN
from [15] can detect edges in a binary image (with black or
white pixels only). The network consists of cells organized in
a two-dimensional lattice corresponding to the image pixels.
Each cell is connected with the nearest neighbors as shown
in Fig. 10 (a) for a cell at the position (i, j).
Each cell has an input node connected to a constant-
voltage source, whose voltage represents the pixel state
TABLE 5. CNN parameters from [15].
(white≡−1V, black ≡+1V). In the benchmark network,
each cell is connected with inputs and outputs of its eight
nearest neighbors as shown in Fig. 10 (a). The relative posi-
tion of the neighboring cells will be denoted by two indices
(k, l)∈ {–1,0,1}, while the combination (0,0) is the cell itself.
Figure 10 (b) shows the circuit implementation of each
cell. The ‘‘memcomputing core’’ [15] consists of a controlled
current source ix, constant current source Iz, capacitor Cx,
resistor Rx, and memristor Mx. The current source ixi,j of a
cell at the position (i, j) is controlled by its own input and
output and by inputs and outputs of the neighboring cells
ixi,j=
1∑
k,l=−1
ak,lvyi+k,j+l+
1∑
k,l=−1
bk,lvui+k,j+l (24)
where vu and vy are the input and output voltages, respec-
tively, and ak,l and bk,l are transconductances. The elements
of the core form a dynamical system of the second order.
The output block consists of a resistor Ry and a current
source controlled by the x-node
vy= Rygy(vx) (25)
where
gy(vx)= 0.5glin(|vx+ vsat|−|vx− vsat|) (26)
is a saturation function.
The parameters of the CNN [15] are summarized
in Table 5. The parameters of memristor models are the same
as in Table 2.
The simulations in PSPICE 17.2 have some limitations:
The analysis of a CNN with 50,000 memristors takes about
1316 seconds, and an attempt to analyze the network with
100,000 cells leads to the analysis being terminated by
‘‘Aborting simulation (Symbols Table overﬂow)’’. Therefore,
the simulations were performed with a more robust HPP
solver of HSPICE v2017.
For automated generation of HSPICE input ﬁles, a MA T-
LAB script was used. The test image is resampled to the
desired resolution and converted to a binary image. Let the
image pixel size be M× N . The CNN cells are generated
only for internal pixels, i.e. the number of cells will be
(M –2)(N –2). The pixels of the ﬁrst and last rows and
30252 VOLUME 9, 2021

D. Biolek et al.: (V)TEAM for SPICE Simulation of Memristive Devices With Improved Numerical Performance
FIGURE 11. Example of CNN simulation. The original image -a vintage-car
mask [16] (a) - was resampled to a resolution of 356 × 563 pixels and
converted to binary image (b). After 10 ms transient analysis, the CNN
found edges (c). The initial conditions of all the 199510 memristor cells
were: vx (0)= 0 V, Mx (0)= 5 k.
columns are used as ‘‘neighbor’’ inputs in (24). If the
cell output voltage is in the negative saturation (see (25)),
the cell has detected an edge, while positive saturation means
‘‘no edge’’ [15]. The simulator output is read back by the
MA TLAB script and presented as an image. Fig. 11 shows
an example of the process.
Figure 12 shows the dependence of the simulation times
(the wall time of transient analysis) on the number of cells
in the CNN for all the memristor models being tested.
The transient analysis was performed with the parameter
FIGURE 12. The computation time of transient analyses vs the number of
cells for various memristor models.
Tmax= 10ms. It is clear from the graph that the models can
be divided into two groups in terms of achieved simulation
times, represented by red and yellow lines: the B, B_s, and
R models (fast), and the J, J_s, J_t, R_t, R_d models (longer
simulation times). The R_s model can be classiﬁed as fast,
except for the CNN consisting of about 50,000 cells, where
the simulation times approach a slower variant of the models.
The simulation of a CNN with half a million cells is already
beyond the capabilities of HSPICE, where simulation runs
are terminated prematurely without any error message. Since
the submodel of each memristor in the CNN cell represents
4 to 6 nodes for the simulator, a network with 500,000 cells
represents a simulation network with 2-3 million nodes.
VI. CONCUSION
The mathematical model of VTEAM [2] was optimized for
implementation in SPICE simulation programs. The results
are fully transferable for the dual TEAM model [1]. Attention
was paid to the solution of the stick effect. Several techniques
were used, including the technique of state variable trans-
formation. These techniques were combined with methods
of smoothing the discontinuities in state equations. Several
variants of the model were tested for accuracy, speed, and
reliability in Cadence PSpice and HSPICE. In the HSPICE
environment, the models were subjected to demanding tests
in extremely large memristive networks.
The results show 9 variants of models that are robust and
stable when simulating networks with hundreds of thousands
of CNN cells employing memristors. These models can be
divided into two categories, the so-called fast and slower
variants. "Fast" models use asymmetric windows (Biolek and
asymmetric rectangular windows), which in principle do not
need additional aids to prevent the stick effect. Smoothing
techniques in themselves improve the convergence proper-
ties, but, on the other hand, they slow down the calculations.
VOLUME 9, 2021 30253

D. Biolek et al.: (V)TEAM for SPICE Simulation of Memristive Devices With Improved Numerical Performance
It has also been shown that the operation of smoothing
algorithms is sensitive to the setting of transient analysis
parameters and error criteria. The testing of models for speed,
accuracy and the above-mentioned sensitivity revealed that
the least advantageous models were models with classic sym-
metrical windows of the Joglekar type. If, due to a numerical
error, there is even a "slight" overﬂow or underﬂow of the
state variable outside the allowed region of the window func-
tion, the derivative of the state variable is calculated from the
values of the window function outside this region, which can
lead to errors. This can be partially reduced by appropriately
redeﬁning the window function outside the allowed area of
the state variable, which, however, causes other complica-
tions - slowing down the calculations and a greater tendency
to the stick effect. Thus, it clearly turns out that symmetric
windowing should be either avoided or implemented by the
method of transforming the state variables. Even after this
transformation, however, the J_t model is slower than the
models based on asymmetric windows (e.g. the B model).
Furthermore, it has become clear that models with the
transformation of state variables cannot be successfully
implemented in the SPICE environment for asymmetric win-
dows, because the SPICE standard does not allow an effective
identiﬁcation of an event associated with a discontinuity in
time (speciﬁcally the time at which this discontinuity occurs).
The relevant B_t model was therefore only tested in Cadence
PSpice 17.2 with the provisional use of the "state" function.
In the next step, it will be interesting to implement this model
as an embedded V erilog-A code in HSPICE and then perform
its testing in a multi-memristor structure according to the
methodology used in this work.
The models that passed the tests with best results (B, B_s,
R, R_s) work reliably and quickly in networks with 200k
CNN cells (in fact, the extent of the simulated circuits is
only given by the computer hardware and the limits of the
HSPICE program), and their optimized SPICE codes there-
fore may be useful for a wide variety of researchers involved
in simulations of large memristor circuits.
The procedures from this work can be applied not only
to VTEAM but also to other known models of memristors.
In particular, the stick effect elimination is a challenge asso-
ciated with all models that use symmetric window func-
tions in their differential equations of motion. The proposed
method of state variable transformation is directly applicable
to the General Hyperbolic Sine Model [17] and the Y akopcic
model [18], whose state equations represent the product of
nonlinear functions of the state variable and the voltage or
current.
REFERENCES
[1] S. Kvatinsky, E. G. Friedman, A. Kolodny, and U. C. Weiser, ‘‘TEAM:
ThrEshold adaptive memristor model,’’ IEEE Trans. Circuits Syst. I, Reg.
Papers, vol. 60, no. 1, pp. 211–221, Jan. 2013.
[2] S. Kvatinsky, M. Ramadan, E. G. Friedman, and A. Kolodny,
‘‘VTEAM: A general model for voltage-controlled memristors,’’
IEEE Trans. Circuits Syst. II, Exp. Briefs, vol. 62, no. 8, pp. 786–790,
Aug. 2015.
[3] M. D. Pickett, D. B. Strukov, J. L. Borghetti, J. J. Y ang, G. S. Snider,
D. R. Stewart, and R. S. Williams, ‘‘Switching dynamics in titanium
dioxide memristive devices,’’ J. Appl. Phys., vol. 106, no. 7, Oct. 2009,
Art. no. 074508.
[4] J. G. Simmons, ‘‘Electric tunnel effect between dissimilar electrodes
separated by a thin insulating ﬁlm,’’ J. Appl. Phys., vol. 34, no. 9,
pp. 2581–2590, Sep. 1963.
[5] S. Kvatinsky, K. Talisveyberg, D. Fliter, A. Kolodny, U. C. Weiser, and
E. G. Friedman, ‘‘Models of memristors for SPICE simulations,’’ in Proc.
IEEE 27th Conv. Electr . Electron. Eng. Isr . , Eilat, Israel, Nov. 2012,
pp. 1–5.
[6] D. Biolek, M. Di V entra, and Y . V . Pershin, ‘‘Reliable SPICE simulations
of memristors, memcapacitors and meminductors,’’ Radioengineering,
vol. 22, no. 4, pp. 945–968, 2013.
[7] D. Biolek, Z. Biolek, V . Biolkova, and Z. Kolka, ‘‘Modeling of TiO 2
memristor: From analytic to numerical analyses,’’Semicond. Sci. Technol.,
vol. 29, Nov. 2014, Art. no. 125008.
[8] D. Biolek, Z. Biolek, V . Biolkova, and Z. Kolka, ‘‘Reliable modeling of
ideal generic memristors via state-space transformation,’’ Radioengineer-
ing, vol. 24, no. 2, pp. 393–407, Jun. 2015.
[9] Z. Biolek, D. Biolek, and V . Biolkova, ‘‘SPICE model of memristor with
nonlinear dopant drift,’’ Radioengineering, vol. 18, no. 2, pp. 210–214,
Jun. 2009.
[10] S. Shin, K. Kim, and S-M. Kang, ‘‘Compact models for memristors based
on charge-ﬂux constitutive relationships,’’ IEEE Trans. Comput.-Aided
Design Integr . Circuits Syst., vol. 29, no. 4, pp. 590–598, Mar. 2010.
[11] K. Eshraghian, O. Kavehei, K.-R. Cho, J. M. Chappell, A. Iqbal,
S. F. Al-Sarawi, and D. Abbott, ‘‘Memristive device fundamentals and
modeling: Applications to circuits and systems simulation,’’ Proc. IEEE,
vol. 100, no. 6, pp. 1991–2007, Jun. 2012.
[12] Á. Rak and G. Cserey, ‘‘Macromodeling of the memristor in SPICE,’’
IEEE Trans. Comput.-Aided Design Integr . Circuits Syst., vol. 29, no. 4,
pp. 632–636, Apr. 2010.
[13] F. Garcia-Redondo, M. Lopez-V allejo, and P . Ituero, ‘‘Building memristor
applications: From device model to circuit design,’’IEEE Trans. Nanotech-
nol., vol. 13, no. 6, pp. 1154–1162, Nov. 2014.
[14] PSpice A/D Reference Guide. Cadence, San Jose, CA, USA, Product
V ersion 16.0, Jun. 2007.
[15] A. Ascoli, R. Tetzlaff, S.-M. Kang, and L. O. Chua, ‘‘Theoretical founda-
tions of memristor cellular nonlinear networks: A DRM2-based method
to design memcomputers with dynamic memristors,’’ IEEE Trans. Cir-
cuits Syst. I, Reg. Papers, vol. 67, no. 8, pp. 2753–2766, Aug. 2020, doi:
10.1109/TCSI.2020.2978460.
[16] Pixabay (Royalty Free Stock). Accessed: Feb. 12, 2021. [Online].
Available: https://cdn.pixabay.com/photo/2016/08/07/11/50/jaguar-15761
09_960_720.jpg
[17] M. Laiho, E. Lehtonen, A. Russel, and P . Dudek, ‘‘Memristive synapses
are becoming reality,’’ in The Neuromorphic Engineer, College Park, MD,
USA: Institute of Neuromorphic Engineering, 2010.
[18] C. Y akopcic, T. M. Taha, G. Subramanyam, R. E. Pino, and S. Rogers,
‘‘A memristor device model,’’IEEE Electron Device Lett., vol. 32, no. 10,
pp. 1436–1438, Oct. 2011.
DALIBOR BIOLEK (Senior Member, IEEE)
received the M.Sc. degree in electrical engineering
from the Brno University of Technology, Czech
Republic, in 1983, and the Ph.D. degree in elec-
tronics from the Military Academy Brno, Czech
Republic, in 1989.
He is currently with the Department of EE,
University of Defence Brno (UDB), and with the
Department of Microelectronics, Brno University
of Technology (BUT), Czech Republic. His sci-
entiﬁc activity is directed to the areas of general circuit theory, frequency
ﬁlters, mem-systems, and computer simulation of electronic systems. He is
currently a Professor at BUT and UDB in the ﬁeld of theoretical electrical
engineering.
Dr. Biolek is a member of the CAS/COM Czech National Group of IEEE.
He has been a member of editorial boards of international journals including
the International Journal of Electronics and Communications (AEU) and
Electronics Letters.
30254 VOLUME 9, 2021

D. Biolek et al.: (V)TEAM for SPICE Simulation of Memristive Devices With Improved Numerical Performance
ZDENĚK KOLKA (Member, IEEE) received the
M.Sc. and Ph.D. degrees in electrical engineering
from the Brno University of Technology (BUT),
Czech Republic, in 1992 and 1997, respectively.
In 1995, he joined the Department of Radio Elec-
tronics, Brno University of Technology. His sci-
entiﬁc activity is directed to the areas of general
circuit theory, computer simulation of electronic
systems and digital circuits. For years, he has
been engaged in algorithms of the symbolic and
numerical computer analysis of electronic circuits. He has published over
100 articles. He is currently a Professor at BUT in the ﬁeld of radio
electronics.
VIERA BIOLKOVÁ (Member, IEEE) received the
M.Sc. degree in electrical engineering from the
Brno University of Technology, Czech Republic,
in 1983. She joined the Department of Radio
Electronics in 1985, and is currently working
as a Research Assistant with the Department of
Radio Electronics, Brno University of Technol-
ogy, Czech Republic. Her research and educa-
tional interests include modeling of large-scale
systems, signal theory, analog signal process-
ing, memristors and memristive systems, optoelectronics, and digital
electronics.
ZDENĚK BIOLEK received the Ph.D. degree
in electronics and informatics from the Brno
University of Technology, Czech Republic,
in 2001.
He is currently with the Department of Micro-
electronics, Brno University of Technology, and
with the Department of EE, University of Defence
Brno, Czech Republic. Until the year 1993,
he worked as an Independent Researcher in semi-
conductor company TESLA Rožnov. He is the
author of unique electronic instruments associated with IC production and
testing. He is also the author of several articles from the area of the utilization
of variational principles in electrical engineering, and also from the ﬁeld
of memristors and mem-systems. He is the coauthor of two books about
memristive systems and modeling and simulation of special electronic
circuits including switched-capacitor ﬁlters, switched DC-DC converters,
and memristors.
SHAHAR KVATINSKY (Senior Member, IEEE)
received the B.Sc. degree in computer engineering
and applied physics and the M.B.A. degree from
the Hebrew University of Jerusalem, in 2009 and
2010, respectively, and the Ph.D. degree in electri-
cal engineering from the Technion – Israel Insti-
tute of Technology in 2014. He is currently an
Associate Professor with the Andrew and Erna
Viterbi Faculty of Electrical Engineering, Tech-
nion – Israel Institute of Technology. From 2006 to
2009, he worked as a Circuit Designer at Intel. From 2014 and 2015,
he was a Postdoctoral Research Fellow with Stanford University. He is
an Editor of Microelectronics journal and has been the recipient of numer-
ous awards: 2020 MDPI Electronics Y oung Investigator Award, 2019 Wolf
Foundation’s Krill Prize for Excellence in Scientiﬁc Research, 2015 IEEE
Guillemin-Cauer Best Paper Award, 2015 Best Paper of Computer Archi-
tecture Letters, Viterbi Fellowship, Jacobs Fellowship, ERC starting grant,
the 2017 Pazy Memorial Award, the 2014 and 2017 Hershel Rich Technion
Innovation Awards, 2013 Sanford Kaplan Prize for Creative Management
in High Tech, 2010 Benin prize, and seven Technion excellence teaching
awards. His current research is focused on circuits and architectures with
emerging memory technologies and design of energy efﬁcient architectures.
VOLUME 9, 2021 30255
