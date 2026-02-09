# 09_chua_kang_memristive_devices_1975.pdf

Copyright © 1975, by the author(s). 
All rights reserved. 
 
Permission to make digital or hard copies of all or part of this work for personal or 
classroom use is granted without fee provided that copies are not made or distributed 
for profit or commercial advantage and that copies bear this notice and the full citation 
on the first page. To copy otherwise, to republish, to post on servers or to redistribute to 
lists, requires prior specific permission. 

MEMRISTIVE DEVICES AND SYSTEMS
by
L, 0. Chua and S, M, Kang
Memorandum No. ERL-M515
15 April 1975
ELECTRONICS RESEARCH LABORATORY
College of Engineering
Universityof California, Berkeley
94720

MEMRISTIVE DEVICES AND SYSTEMS
L. 0. Chua and S. M. Kang
Department of Electrical Engineering and Computer Sciences
and the Electronics Research Laboratory
University of California, Berkeley, California 94720
ABSTRACT
A broad generalization of memristors a recently postulated
circuit element to an interesting class of nonlinear dynamical systems
called memristive systems is introduced. These systems are unconventional
in the sense that while they behave like resistive devices, they can be
endowed with a rather exotic variety of dynamic characteristics. While pos
sessing memory and exhibitingsmall-signal inductive or capacitive effects,
they are incapable of energy discharge and they introduce no phase shift
between the input and output waveforms. This zero-crossingproperty gives
rise to aLissajous figure which always passes through theorigin. Mem
ristive systems are hystereticin the sense that theirLissajous figures
vary with the excitation frequency. At very low frequencies, memristive
systems are indistinguishable from nonlinear resistors while at extremely
high frequencies, they reduce to linearresistors. These anomalous
propertieshave misled andprevented the identificationof many memristive
devices and systems including the thermistor, the Hodgkin-Huxley
membrane circuit model, and thedischargetubes.
Generic properties of memristive systems are derived and a canonic
dynamical systemmodel is presented along with an explicit algorithmfor
identifyingthe model parametersand functions.
Research sponsored by the Joint Services ElectronicsProgram Contract
F44620-71-C-0087 and the National Science Foundation GrantGK-32236xl,

I. INTRODUCTION
The memristor has been postulated recently as the fourth basic
circuit element [1]. This element behaves like a linear resistor with
memory but exhibits many interesting nonlinear characteristics. These
unconventional properties have led to the successful modeling of a number
of physical devices and systems [1-4]. Notwithstanding these applications,
however, there remains an even broader class of physical devices and systems
whose characteristicsresemble those of the memristor and yet cannot be
realistically modeled by this element. The reason being that the mem
ristor is only a special case of a much more general class of dynamical
systems henceforth called memristive systems defined by
x = f(x, u, t)
y = g(x, u, t)u
(1)
where u and y denote the input and output of the system and x denotes
the state of the system. The function f :Rn x R x R -> Rn is a
continuousn-dimensionalvector function and g:l£ x R x R •> R is a
continuous scalar function. It is assumed that the state equation in(1)
has a unique solution for any initial state x G R . The output equation
in (1) is such that the output y is equal to theproduct between the input
u and the scalar function g. This special structure of the read-out map
is what distinguishes a memristive system from an arbitrary dynamical
system [5]; namely, the output y iszero whenever the input u is zero,
regardless of the state x whichincorporates the memory effect. This
The extension of this definition to the multi-port case is straight
forward. Hence, only theone-port case will be discussed in this paper.
-1-

zero-crossing property manifests itself vividly in the form of a Lissajous
figure which always passes through the origin.
2
An nth-order current-controlled memristive one-port is represented
by
x = f(x, i, t)
" ~ " (2)
v = R(x, i, t)i
and an nth-order voltage-controlled memristive one-port is represented by
x = f(x, v, t)
~ ~ ~ (3)
i = G(x, v, t)v
where v and i denote the port voltage andcurrent, respectively. The
functions f, R or G are similarly defined as f, g in (1). In the special
3
case when theone-port is time-invariant and R(resp. G) is not an explicit
function of i(resp. v) we have
x = f(x, i) (resp., x = f(x, v))
(4)
v = R(x)i (resp., i = G(x)v)
To motivate the significance of memristive systems, we pause to present
some examples of physical devices which should be modeled as memristive
one-ports, but which have so far been improperlyidentified.
Example 1. Thermistor
Thermistorshave been widely used as alinear resistor whose resistance
varies with the ambient temperature [6]. In particular, a negative-1em-
2
The number n denotes the dimension of the state space of the dynamical
system.
3
The dynamical system (1) is said to be time-invariantif both f and g
are not explicit functions of time t.
-2-

perature coefficient thermistor is characterized by [7]
I -61''v= Ro(Tq) expleft-iHli4R(T)i (5)
4
where 6 is the material constant , T is theabsolute body temperatureof
the thermistorand T is the ambient temperaturein degrees Kelvin. The
constant R (T ) denotes the cold temperatureresistance at T = T . The
instantaneoustemperatureT, however, is known to be a function of the
power dissipated in the thermistor and is governed by the heat transfer
equation
p(t) =v(t) i(t) =6(T -Tq) +C^ (6)
where C is the heat capacitance and <5 is the dissipation constant of the
thermistor which is defined as the ratio of a change in the power dissi
pation to the resultant change in the body temperature. Substituting
Eq. (5) into Eq. (6) and by rearranging terms, we obtain
£ -.-|ch0)+-v--p. .
o
[3(t'T")]i2 Af<T» i) (7)
We observe from Eqs. (5) and (7) that a thermistor is in fact not a
memoryless temperature-dependent linear resistor as is usually assumed
to be the case but rather a first-order time-invariant current-controlled
memristive one-port.
Example 2. Ionic Systems
The celebratedHodgkin-Huxleykcircuitmodel [8] of the nerve axon
4
Although $ increases slightly with increasing temperature, it may be
approximated by a constant over the temperature range of interest.
Strictly speaking, <5 is not a true constant, but varies slightly with
both T and T-T . However, for simplicity, 6 is assumed to be constant here.
-3-

membrane is shown in Fig. 1. Hodgkin and Huxley described the Potassium
channel conductanceg and the Sodium channel conductanceg^ as time-
varying conductances whose variations are functions of the solutions of
first-order differential equations. The Potassium channel is described
by
^=^ n4 vK AGK(n) vR
• °-01(vK+EK+10) , ni„ /Wn = r?—j-p .in\ /im i (1-n) - 0.125 explexptCv^F^+W/lO]-]
A f(n, vR)
(8)
/VK+EK\
where g^ and EL, are constants. The sodium channel is described by
*Ma =%a m3 hvNa AGNa(m« h)vNa
m=expUv^-E^^/lO]-!(1-m> " k"» V—18 >* m
Afi<W (9)
h=0.07 exppf^)(1-h) -exp[(VNa_^a+30)/lomh
4 f2.0>. vNa)
where g^ and E are constants. It follows from Eqs. (8) and (9) that
since the time-varying conductances can not be specified as an a priori
function of time, they are actually memristivesystems. In particular,
the Potassium channel of the Hodgkin-Huxley model should be identified as
a first-order time-invariant voltage-controlled memristive one-port and
the Sodium channel should be identified as a second-order time-
invariant voltage-controlled memristive one-port.
-4-

Example 3. Discharge Tubes
Francis [9] described the behaviors of discharge-tubesby
n = a i v - 3n (10.a)
v = - i AR(n)i (10.b)
n —
where a, 3 and F are constants dependingon the dimensionsof the tubes
and the gas fillings. The variablen denotes the electrondensity of the
tubes. SubstitutingEq. (10.b) into Eq. (lO.a) we obtain
n=— i2 -3 A f(n, i) (10.c)
n n —
It follows from Eqs. (10.b) and (10.c) that the discharge tube should also
be modeled as a first-order time-invariant current-controlled memristive
one-port. It is unfortunatethat whileresearchershave long regarded
such discharge tubes as neonbulbs and fluorescent lamps as dynamic devices,
they have failed to recognize their memristive properties.
II. GENERIC PROPERTIES OF MEMRISTIVE ONE-PORTS
Since many memristivedevices have beenincorrectlyclassified, our
next objectivewill be toderive the generic propertieswhich clearly
distinguisha memristive device from othersystems. For simplicity, we
6
will restrict our study to current-controlled memristive one-ports.
Property 1 (Passivity Criterion)
Let a current-controlled memristive one-port be time-invariant and
let its nonlinear function R(«) associated with the read-out map satisfy the
The same property obviouslyapply to the "dual" voltage-controlledcase.
This criterion can be easily extended to the time-varying case.
-5-

constraint R(x, i) = 0 only if 1=0. Then the one-port is passive if,
and only if, R(x, i) >_ 0 for any admissibleinput current i(t), for all
t 1 t i where t is chosen such that x(t ) = x , where x is the state
of minimum energystorage [10].
Proof; If R(x, i) > 0, then
J v(t) i(x) dx =f r(x(t), i(x)j i2(x) dx >_ 0for all t>_
o to
and hence the one-port is passive. We prove the necessity part
by contradiction. First, suppose that the one-port is passive and
R(x ,i ) < 0for some i £ R. Then by the continuityof the
of the function R in R , there exists an open neighborhood
B[(x*, i), 6] of (x*, i)6Rn+1 in which R(x, i) <0. Hence
O •• O " O "•
there exists an input waveform i(#) such that i(t ) = i and
o o
I v(t) i(x) dx <0 for all t€ (t ,t.), where t- depends on
o
B and i(*)» But this contradictsthe assumption that the one-
"k
port is passive and R(x ,i) _> 0for any admissible i £ R.
Suppose next that R(x ,i)<0 for some (xA, i.) ^R1
t
o
ft je
where x. 7s x . Then we can draw a"connecting"arc r from (x , i )
to (xA, i )such that the open arc (excludingthe two end points)
does not intersect the hyperplanei=0. Since R(x , i )>^ 0 and
R(x., i ) < 0 byassumption, and since the function R is continuous
in (x, i), there exists a point (x_, i^) at which R(x«, i_) = 0.
However, this contradicts the assumption that R(x, i) = 0 only
if i=0, and hence R(x, i) >^ 0 for passivity to hold 
Property 2 (No Energy Discharge Property)
If a current-controlled memristive one-port satisfies the hypothesis
-6-

of Property 1, then the instantaneouspower entering the one-port is
always nonnegative.
Proof: By hypothesis, R(x, i) ^ 0 for any admissiblesignal pair (v, i),
and hence the instantaneouspower entering the one-port (i.e.,
p(t) = v(t) i(t)) is always nonnegative. *
Remark: Except for pathologicalcases, it is alwayspossible to extract
stored energy from a passive RLC one-port by simply connectinga
load across it. However, for the case of a memristiveone-port
which satisfiesProperty1, such energy discharge is never possible,
To emphasize this unique property, we label it the "no energy
discharge property."
Property 3 (DC Characteristics)
A time-invariantcurrent-controlledmemristive one-port under dc
operation is equivalent to a time-invariant current-controlled nonlinear
resistor if f(x, I) = 0 has aunique solutionx = X(I) such that for each
value of I£ IR, the equilibriumpoint x = X(I) is globally asymptotically
stable [11].
o
Proof: Substitutingx = X(I) into the outputequation in (2) , we obtain
V=r(x(I), ih AV(I). Since X(I) is globally asymptotically
stable, each value of dc input current I gives a stable, hence
measurable, dc voltage V. Hence the function V(I) can be inter
preted as the V-I curve of a time-invariant nonlinear resistor. *
Remark: In practical analysis, Property 3 is still valid under low
frequency periodic operation so long as the period of the excita-
g
Strictly speaking we are referring to thetime-invariant version of
representation (2).
-7-

tion is much larger than the settling time of the associated
transient response.
To illustrate the significance of Property 3, the dc
characteristics of a thermistor with 3 = 3460 °K, 6 = 0.1mW/°C,
Tq =298 °K and RQ(T )= 8000 ft are derived from Eqs. (5) and (7)
and are shown in Fig. 2 for 0 <_ I <_ 12.5 mA. Notice that only
the curve in the first quadrant is shown since the dc character
istic is symmetrical with respect to theorigin. Such dc V-I
characteristics are often supplied by thermistor manufacturers
with the steady state temperature specified along the curve.
Property 3 can now be used to interpret the use of this curve and
its limitations; namely, the dc thermistor V-I curve is useful
only if the thermistor is to be operated under dc or slowly-
varying input signals. Observe that the fact that a time-invariant
memristive one-port under dc operation behaves just like a nonlinear
resistor is one reason why so many memristive devices have been
improperly identified as nonlinear resistors!
The dc characteristic curve of the Potassium channel (with
_ 2
g =36 my/cm and EL^ =12 mV) of the Hodgkin-Huxleymodel described
by Eq. (8) is shown in Fig. 3. Similarly, a typical dc V-I curve
of discharge tubes is shown inFig. 4. Again, only the first-
quadrant V-I curve is shown since it issymmetricalwith respect
to the origin. Observe that all these dc characteristic curves
pass through the origin as they should.
Property 4 (Double-Valued Lissajous Figure Property)
A current-controlled memristive one-port under periodic opera-
-8-

9
tion with i(t) = I cos o)t always gives rise to a v-iLissajous figure
whose voltage v is at most a cjouble-valuedfunction of i.
Proof: In the representation(2), the state equation has a uniqueperiodic
solution x(t) for all t _> t for some initial state x , byassump
tion. Hence, for any value of thecurrent i £ [-1,1], there
correspond at most twp distinct values of v. *
Remark: This property is illustrated in Fig. 5. Observe that the Lissajous
figure in Fig. 5(b) cannot correspond to that of a current-controlled
memristiveone-port, because at i =ip, there correspondmore than
two distinct values of v.
Property 5 (Symmetric Lissajous Figure Property)
If the read-out map of a time-invariant current-controlled memristive
one-port is suchthat R(x,i) «= R(x,-i), then the v-iLissajous figure
correspondingto the input current i(t) = I cos tot is open (i.e., not a
closed loop) whenever the state x(t) is periodic of the same period as
that of the input i(t) and ishalfwave symmetric. Moreover, it is odd
symmetricwith respect to theorigin whenever the statex(t) is periodic
of the same period as that of i(t) and isquarterwavesymmetric.
Proof: If both x(t) and i(t) are halfwave symmetric, then it follows from
the output equation v = R(x,i)i that
9
A one-port is said to be inperiodic operationwhen its response is
periodicwith the same period as that of theinput.
A periodic waveform x(t) of period T is said to be halfwave symmetric if
kT kT T
x(t +—)=x(-t +2~ )for k=l, 2for all t€[0, -|], and quarterwave
symmetric if x(t +— ) =x(-t + — ) for k=l, 3 for all t<= [0, ±].
-9-

v(t +f) =R(x(t +|), i(t +|)) i(t +|)
=R(x(-t +|), i(-t +|)j i(-t +|)
=v(-t +|) for all tG[0, |]
where T is the period of both x(t) and i(t). Hence the v-i curve
does not form a closed loop and'is open. If x(t) is quarterwave
symmetric, then since i(t +t) --i(-t + j) for all t€ [0, j]
when i(t) = I cos o>t, we obtain
v(t +f) =R(x(t +|), i(t +|)) i(t +|)
=-R(x(-t+|), i(-t +|)) i(-t +|)
«-v(-t +-|) for all te[0, j].
3T 3TSimilarly, we can show that v(t + -r—) = -v(-t + 7—) for all
T
t £ [0, v]. Hence, the v-i curve is oddsymmetricwith respect
to the origin. 
Property 6 (Limiting Linear Characteristics)
If a time-invariant current-controlled memristive one-port described
by Eq. (4) is bounded-inputbounded-state (b.i.b.s.) stable , then under
periodic operation it degenerates into a linear time-invariant resistor as
the excitation frequency increases toward infinity.
Proof: It suffices to show that the state vector x(t) -*- x where x is
~ ~o ~o
some constant vector in R , as the excitation frequencyw •> ».
A dynamical system (4) is said to be b.i.b.s. stable if for alltQ, for
all initial states x0 and for all bounded inputs i, . , the state
trajectory x(«) is bounded. °'
-10-

It follows from the b.i.b.s. stability and the continuity of the
function f in Eq. (4) that for any bounded input i(t), f(x,i) can
be written as
f(x,i) -a +-£ eikwt a. (11)
~° k=-N ~K
#0
where N is some integer and the vectors a and a. belong to the
• ~o ~k
space $ of n-tuples of complex numbers. Note that the vectors
a and a, are bounded. From Eqs. (4) and (11) we obtain
x(t) =x(tQ) +ff(x(x), i(x)jdx
'o
rt / N
= x + /a + T
~° Jt P k=-N° X k^O
ikwx \ ,e a, Jdx
M ikwt iku)tN o
=x + a(t-t )+ Y, jt^-Z a. (12)~o -o o , « iku) ~kk=-N
k^O
Since x(t) is periodic and bounded by assumption, Eq. (12) implies
a = 0 and as w + «, the state x(t) ->• x . 
~o - ~o
Remark: When the memristive one-port is under periodicoperation, different
initial states x will have to be chosen for different excitation
~o
frequencies. However, the state x(t) still approaches some constant
vector as the excitation frequency increases toward infinity. This
property is illustrated in Fig. 6, where a family of Lissajous
figures is shown shrinking to a straight line as o> + ».
Property 7 (Small-Signal AC Characteristics)
If a time-invariant current-controlled memristive one-port is globally
-11-

asymptoticallystable for all dc input current I, then its small-signal
equivalent circuit about the dc operatingpoint is as shown in Fig. 7.
Proof: Let the input current i(t) be such that
i(t) « I+ 6i(t), where sup |«i(t)| « |l|
telR
(13)
and let a time-invariantcurrent-controlledmemristiveone-port
be characterized by
x = f(x,i)
v = R(x,i)i A h(x,i)
(14)
If we linearize Eq. (14) about (X,I), where X is the solution of
f(x,I) = 0, we obtain
6x =
9f(X,I) 3J(X,I)
5x + 6i A A(X,I)6x + b(X,I)6i
6i A c(X,I)6x + d(X,I)6i6v =
9x
3h(X,I)
3x
where
A(X,I) =
b(X,I)
6x +
3i
3h(X,I)
9f1(X,I)
9x,
3f2(X,I)
3x1
9f2(X,I)
3x1
3f (X,I) 3f (X,I)
n ~ n -
3x, 3x,
Zf^X,!) 3f2(X,I)
3i 3i
-12-
^^(J.!)
3x
n
3f2(X,I)
3x
n
3f (X,I)
n -
3x
n
3fn(X,I)"l
' 31 J
(15)
(16)
(17)
(18)

f3h(X,I) 3h(X,I) 3h(X,I)
S«'«"[-1^ 3^- •••-i^-I (19)
3hQC,I)
and d(X,I) = —r-. (20)
ol
Taking Laplace transformof both sides of Eqs. (14) and (15) with
6x(0) = 0, we obtain
s'AX(s) = A(X,I) AX(s)"+ b(X,I)AI(s) (21)
AV(s) = c(X,I) AX(s) + d(X,I) AI(s) (22)
Solving for AX(s) from Eq. (21), we obtain
AX(s) =[si -MX,!)]"1 b(X,I) AI(s) (23)
where 1 denotes an identity matrix of order n.
Substituting Eq. (23) into Eq. (22), we obtain
AV(s) ={c(X,I)[sl-MX.I)]"1b(X,I) +d(X,I)}Al(s) (24)
It follows from Eq. (24) that the small-signal impedance for a time-
invariant current-controlled memristive one-port is given by
WW AV(s) Atr t, +gj ^ +h S""2 +• • •+6n-l 8*gnzq(s) AH(i) " d(?.« +TT £TT ^T~ 7 ~~x s + a, s +a_s + ... + a , s + a12 n-1 n
where a ,3. are functions of (X,I) € R x R. Equation (25) can be
rewritten into the form of a continued fraction expansion
Zn(s) = d(X,I) +— - (26)
x 1
sC.+
8C2 +
-13-
sC„+¥-
n
(25)

where again C. and R. are functions of (X,I). The circuit in
Fig. (7) follows from Eq. (26) upon setting R(X,I) = d(X,I) 
Remark 1; For the case of time-invariant current-controlled memristive
one-port described by Eq. (4), the associated small-signal equiv
alent circuit is as shown in Fig. 8. Observe that Fig. 8 is
obtained from Fig. 7 upon replacing R (X,I) by R (X), R.(X,I) by
I R.(X,I) and C.(X,I) by C.(X,I)/I. When the biasingcurrent
1=0, the small-signal input impedanceZ (s) reduces to that of
a linear resistor R (X) and is therefore purely dissipative for
R (X) > 0.
o ~
Remark 2: As the excitationfrequencyof the small signal 6i(t) approaches
zero, the small-signalimpedanceZQ(s) in Fig. 8degenerates into
ZQ(s) =Rq(X) +1Q E V^'V (27)
the small-signalimpedancein Eq. (27) correspondsto theslope
of the dc current at I = L. The value R (X) represents the dc
resistanceat I a I and is equal to the small-signalimpedance
Z (s) as the excitation frequency increases toward infinity.
The frequencydependenceof the small-signalLissajous
figures about the operatingpoint I=IQ is depicted in Fig. 9.
This behavior has beenobserved in many physical devices and
12
systems, includingthermistorsand ionic systems [12].
Remark 3: The small-signalequivalent circuits for the thermistorand
12
Mauro [12] was so perplexed and mystified by these unconventional
behaviors that he collectivelyreferred to these elements as an anomalous
impedance!
-14-

the Potassium channel of the Hodgkin-Huxley model are shown in
Figs. 10 and 11. In Fig. 10, ^£2ctPR(T) 'wher® a4"\ <°
and P = VI. Since C- is negative, the thermistor is inductive
under small-signaloperation. In Fig. 11, the small-signal K
admittance Y (s) of the Potassium channel can be shown to be
inductive for V > 0 andcapacitlve for V < 0.
Property 8 (Local Passivity Criteria)
A first-ordertime-invariantcurrent-controlledmemristiveone-port
described by Eq. (4) is locally passive with respect to an operating
point I = I if, and only if,
i) ^^1 o
ii) R(X) > 0 and«<
3f(X,I) 3R(X)
vtv\ >> 91 3x . 3f(X,I) , _
R(X) - 3f(X,I) When —*^— *°
3x
aiaa sssql x y 0 when zt&n m0
3i 3x 3x
• x •
Proof: The small-signalimpedanceof a first-ordertime-invariant
current-controlledmemristiveone-port described by Eq. (4) is
3f(X,I) 3R(X) j
Vs) =R(x) + 9i afoLp ™
S ~ 3x
In order for Z (s) to be the impedanceof a passive one-port, it
is necessaryand sufficientthat Z (s) be positive real. The
conditionsgiven in Eq. (28) follow directly from thewell-known
pr criteria [13]. 
Remark: The Potassiumchannel of the Hodgkin-Huxleymodel violates the
15-
(28)

second criterion (with ireplaced by v) at V = 10mV and hence
is locally active at this operatingpoint. This is verified by
the fact that inFig. 3 the slope of the V-I curve at V = 10mV
is negative. For the case of the thermistordescribedby Eqs. (5)
and (7), the second criterion is also violated at I =1.5 mA, and
hence the thermistoris also locally active at this operating
point. Observe that the slope of the V-I curve at I = 1.5mA is
negative, which is consistentwith the local activity of the
thermistor.
General Remarks on the Generic Properties
The propertiesderived above can beused not only toidentify those
memristive devices and systems which have so far eluded a correct identi
fication, but also to suggest potential applications. For example, the
local activity of the thermistorand the Potassiumchannel of the Hodgkin-
Huxley model has important practical significance. Indeed, the two-
thermistorcircuit shown in Fig. 12 has beendesigned to function as an
ultra-low frequencyoscillatorby biasing the thermistorsin their locally
active regions [14]. It is also well known that the Hodgkin-Huxleymodel
is locally active and hence iscapable of firing nerve impulses. Many more
examples abound which possess thegeneric properties of memristive
systems [12].
There are good reasons to believe that many physical and biological
systems should be modeled as memristive one-ports. To identify such
devices and systems, we look for the following properties of the one-port
(JV) under investigation:
i) The dc characteristiccurve of -J\i passes through the origin.
-16-

ii) The v-i Lissajous figures corresponding to any periodic
excitation having a zero mean value always pass through the
origin.
iii) The one-port(JVI behaves as a linear resistor as the excitation
13frequency to increases toward infinity.
iv) For amemristiveone-portlMwhich admits the representation(4),
its small-signal impedance degenerates into a pure resistor
under zero bias, but becomes either inductive or capacitive
depending on the operating point.
v) The order of thesmall-signalimpedance (or admittance) is
invariant with respect to the dc biasing current (orvoltage).
III. A CANONICAL MODEL FOR MEMRISTIVE ONE-PORTS
Once a device or system has been identified as memristive, the next
task will be to find asuitablemathematicalmodel describing its behavior.
Our objective in this section is to present a canonical model which will
correctlymimic the steady state response,of memristiveone-ports to the
followingclass of input "testing signals":
1. DC or slowly-varying waveforms.
2. Sinusoidal signals of arbitraryamplitudesand frequencies.
3. Sinusoidal signals of arbitraryamplitudesand frequencies
superimposed on top of a dc bias.
We willdenote the above class of input testing signals by
C\} A(u(t) AA +A cos wt |(t,w) € R x[!,«,)} (30)
13T* „ t . .If a one-port is notb.i.b.s. stable, then it is possible that the mem
ristive one-port does not behave as a linear resistor asto increase toward
infinity. This situation, however, is highly pathological.
-17-

where (A ,A) G R x R , R ^ [0,»). The constants A and A represent
the dc component and the amplitude of the sinusoidal component of the
input testing signals, respectively. Observe that the lower bound on the
frequency range in Eq. (30) is not a stringent restriction since in
practical applications we can always normalize any given set of nonzero
frequencies so that the lowest frequencybecomes unity. In Eq. (30), the
value of A is set equal to zerofor dc operation, while the value ofA
is set equal to zero forsinusoidal excitations. When the one-port is
operating in the small signal mode, A will be set equal to a small positive
number and A will be set equal to somebiasing value. These testing
signals are chosen mainly because they are the ones most commonly used
in laboratorytests. Although our model is derived to yield exact
simulationsonly for these testing signals, the fact that our model also
possesses all the generic propertiespresented in the preceding section
suggests that it should also give reasonablyrealistic simulationsfor
arbitrary testing signals.
Our main assumptionin the followingderivation is that the system
responsey(t) tends to aunique steady state for each input u(t) £ -U
such that the function p(t) A y(t)/u(t) tends to a periodic waveformof
14
the same period as that of the input u(t) in steady state. Observe
that each input testing signal u(t) €Qjis uniquely specifiedby
three numbers, namely; A , Aand w. Hence for each combinationof
{A ,A, to}, there correspondsa unique p(t). In other words, p(t) is
o
actually a function of A , Aand w and to be precise, we may denote it
The frequencyof p(t) in steady state may be a harmonic of the input
frequency, but neither subharmonicsnor incommensuratefrequenciesare
allowed in p(t).
-18-

by p(t; A , A, w). Let the steady state component of p(t) be denoted by
p (t). Since the function p (t) is periodic of the same period as that
s s
of input u(t), by assumption, it admits the' following Fourier series
representation
N
P_(t) = aft(A ,A,o)) + T\ Ja. (A ,A,w) cos ku)t + b. (A ,A,oo) sin ktot\ (31)
where the integer N is anarbitrarynumber which is determined by p (t).
k=l I
s
The Fourier coefficientsin Eq. (31) are determinedby
2tt
or f*7"ao(Ao,A,w) = -^ pg(x; AQ, A, u>)dx (32)
o
2ir
ak^Ao,A,c^ =f I ps^t; Ao' A' w)cos kwT dT <33)s o
o
,.A,«) =fj
2£
0)
and bk(AQ,A,a)) =-^ I Ps(t; Aq, A, a))sin kwx dx (34)
o
These coefficients are assumed to be continuous functions of A and A in
o
the mean-squaresense, and square-integrablefunctions of u>; namely,
1. For each e > 0and for each (A ,A) G |R x (R ,there exists a
neighborhoodN- of (A,A\) such that
/* a
ao(Ao,A,ai) " a0(A0»A,w)" 2<e (35)
Li
llak(Ao,A,o)) - ^(A^Aa)!! 2<e (36)
Li
15T , ,In most practical cases the integer N is a finite number. If it is
not a finite number, then we will approximatep«(t) by a finite Fourier
series expansionup to the Nth harmonic term and model the approximated
waveform.
-19-

and llbk(Ao,A,u)) --bk(Ao,A,w.)B 2<e (37)
Li
2
for all (A ,A) £ N«, where L denotes the space of square-integrablefunctions,
2. a (A ,A, •)» ^(A »A» *) an(* \(^ »A» ') are square-integrable
2functions of to, i.e., they belong to L-n . .
Before we present a canonical state space model for memristive one-
16
ports which satisfies the preceding assumptions , we will introduce two
2families of complete orthonormal functions in L - . These functions
lk, ;
will allow a uniquedecomposition of the Fouriercoefficients into the
product between a frequency-dependentcomponent and a frequency-independent
componentwhich depends only on A and A of the input u(t) ^^U.. The two
families of complete orthonormalfunctions are defined by [15]:
<_A 4{a,,(a.) 4k2 E"Hz «€£.->. *££\ (38)
K L *" m=l (fao)Zm K J
%4{*UM4k1'£I -^I»*[i -),I6,4} (39)
I m=l (kw) y
where .9 denotes the set of natural numbers and a and $. are constants
, m < I (40)
defined by:
Jl-1
1 n {2(m+n)- -1}
alm A (4£-i)2 n=l
n
n=l
n^m
2 (m-n)
1 fi •
These assumptions can be relaxed such that whenever there is a Fourier
coefficientcontaining terms that are not functionsof the excitation
frequencyw, then the w-dependentterms are square-integrablefunctions
of to and the oj-independentterms are continuousfunctions of (AQ,A).
The model presented is also valid under these relaxed assumptions.
-20-

Jl-1
1 n {2(m+n)+l}
8fcm ^<4£+1)2BT^ ,m<* (41)
n 2(m-n)
n«l
n&a
the families<J\. and^o, will be used shortly to construct the read-out
map of pur state space model.
To model the steady state response of memristive one-ports subject
to the input testing signals u(t) ^HA, we propose the following:
Canonical State Space Model Representation
State Equation:
x. = -a(t) x.. + b(t) u
x2 - -X]L + u
•
x3 =p(u-x1-x3)
> (42.a)
x4 =p("x2"x4)
where xQ A [x1(0), x2(0), x3(0), xA(0)]T =0
Output Equation:
y= g(x1,x2,x3,x4,u)u (42.b)
where
i "Kt ia(t) =—^-^ , b(t) = , K » 1 (42.c)
_ . 1 -Kt fc , 1 -Kt
t+ Ke t+ K6
and p(«) is a monotonicallyincreasingnonlinear functionwhose graph is
similar to the diodecharacteristiccurve. The nonlinear map g(«) in the
output equation (42.b) is defined by
-21-

M
g(x1,x2,x3,x4,u)AZ^ ^o^VVaU H^HJLI^'
x3)
• \l (1 + 2> ,y]Tk( X31
M
£ a.^x^x.)
a=i
UN„1,«3>
. bu((l+-)- <-f>|*!v,& (43)
where M is an integer, and C o(#)» YvpC*) and ^vo/*) are scalar nonlinear
functions of x- and x~ which are identified via the following Fourier
coefficient expansions:
fCoJt(VA) = J a0(Ao'A'u) *uMd'°
rYk£(Ao,A) =^ •kCAo'A«"> V(o,)d(0
k
o'A) "{fiU(A bk(AQ,A,a)) bk£(o))do)
(44)
(45)
(46)
The functions a (•)> a (•) and b.(') in these equations are themselves
Fourier coefficientsof p(t) defined in Eq. (31) while ak£(*) and t>kJl(*)
are basis functions defined in Eqs. (38) and (39). In Eq. (43), N is a
fixed integer defined via Eq. (31) and Tfc(-)> Ufc(-) are the Chebyshev
polynomial functions of the first and second kind, respectively;namely [16],
[k/2]
j=o
T(z) A± lVJ (-l)j <k-1-l)! (2z)k"2jVZ) =2 2* <i; j! (k-2j)! UZ;
-22-
(47)

V«> aEX?] (-Dj jrJfeijyT <2z>k~2j (48)
where [k/2] denotes the largest integer less than or equal to k/2.
Observe that in spite of theseeminglycomplicatedalgebraic structure
of the preceding canonicalmodel, the only model parameter and model
functions that need to be identified are the integer M and (2N+1)M non-
linear functions, C A')> Yk£^ and 5k£^' and the nonlinear function
p(«). As mentioned earlier the nonlinearfunction p(«) may be anystrictly
monotonically-increasingLipschitz continuous functionwhose graph is
similar to the diode characteristic curve. However, for simplicity, we
will choose p(0 to be apiecewiselinear functiondefined by [15]
p(e) Acte +(i -a) r(e) (49)
where a € (0,1) and r(*) is a unit rampfunction, i.e.,
Lo
for e >_ 0
r(e) A i (50)
for e < '0
Notice from Eq. (49) that the nonlinear functionp(») is uniquely specified
by the parameter a € (0,1). Hence, only the value of a need beidentified.
We willpresent an algorithmthat will determine the model parameters
M and a and the(2N+1)Mnonlinearfunctions. Before we state the algorithm
let us first define the following stop rule. Given any set of input testing
signalsQJ A{u,,,(t) AA.+ A. cos \t}9 where the subscripts i,j,k range
from 1 toN. , N., N , respectively, the performance index of the model
° 17with respect to these testing signals are defined to be
We are assuming without loss of generality that the time instant at which
both p(t) and p(t) attain steady state has been set to zero. Hence, by this
assumption, Ps(t) and Ps(t) are periodic on R., after an appropriatetime
translation.
-23-r

\ NA
o
N
aLEE
i=i j-i k=i
^k
2tt
2£
0),(
{ p (t;u. ..)s ijk p (t;u.' )s ijk
dx (51)
where p (t;u...,) denotes the steady state component of p(t) in the
original systemand p (t;u...) denotes the steady statecomponent of
S 1JK
p(t) in the model subject to the input u,..(t) e(~UD* Another error index
18to be used is
NA N. N
A A a)
eM4E E E
i=l j=l k=l
M
(Aoi'Aj'V" 2 Cot^ol'^j'V aU(uk>
N f M .2
?n] •ta(Aoi'*J'"k)" ,?. V^oi'V^Vl
>n(Aoi'Vk>"&6n*(Aoi'VW1/ (52)
where a (•)» a (•) and b (•) are the Fourier coefficientsof p (t;u..,)
on n s ijk.
defined in Eqs. (31)-(34), and a^(0, bn£(*) are defined in Eqs. (38)
and (39). The error e is a function of the integer M and the nonlinear
functions £„(•)» 6 „(•)• To initiate the algorithm, we need toprescribe
o£ nx.
an upper bound n £ (0,1) for the performance index n. We also need to
assume an initial guess on the iterative parametera £ (0,1).
Model Parameter and Function Identification Algorithm
Step 0. Select and a G (0,1), and n Q e (0,1). Set A=l
Step 1. Compute Co£(Aoi,Aj), Y^CA^Aj)and 6^^^) from Eqs. (44)-
18The second error index e^ is used to ensure that the model parameterM
and the nonlinearmodel functions C0jj,(')» YnfcC*) and 5n£,(*) are determined
properly so that the Fourier coefficientsa0(*), an(«) and bn(«) can be
approximatedclosely for the given componentsAq^, Aj and w^.
-24-

(46) for n =1,2,...,Nfor each i,j ranging from 1 toN and
o
N , respectively. •-..
Step 2. Set M= I and compute eM using Eq. (52).
n
max
Step 3. If eM >—r— set i = Z+l and go to Step 1.
Step 4. Compute the performance index n using Eq. (51)
Step 5. If n > n , set a = -z and go to Step4.
max L
Otherwise stop.
The convergenceof this algorithmis guaranteedby the following
theorem.
Main Theorem
If theFourier series representationof a (A ,A,0 relative to the
o o
basis functions inLzL. afc(A ,A,•) relative to the basis functions in
k* and bk^Ao,A'"^ relat*ve to the basis functions in^B, converge
uniformlyover the set of testing signal components {(A ,A.)} for i, j
ranging from 1to NA and NA> respectively, and for k= 1,2,...,N, then
for each nmax >0 the precedingalgorithm,terminates in afinite number
of iterations.
Proof: For each (Aq,A), the scalars ^(A^A),Yk^(AQ,A) and 6kA(AQ,A)
as defined by Eqs. (44)-(46) are the Fourier coefficientsof
ao(AQ,A,«)» ak(AQ,A,-) and bk(AQ,A,') relative to the basis
functions in the complete orthonormalsets <Jk ,Jk, and ^B. . Hence
by the uniform convergencehypothesis, there exists a finite integer
n
Msuch that eM defined by Eq. (52) is less than or equal to -~£
for any n > 0, i.e.,max ' *
^ max , ^
-25-

From Lemma A-1 of the AppendixA, Co£(A()i,Aj), Yk£(AQi,Aj) and
<skJl(Aoi,A)are continuousfunctions of (A ±,A.). From Theorem
A-1 in the AppendixA, there exists a 6e (0,1) such that for any
a G (0,6), the steady state solutionof the state equation (42.a)
yields arbitrarilyclose approximationsA „, A. and aif to A „, Aoi j k oi' j
and wk, respectively. Also by the continuityof the Chebyshev
polynomialsTfc(.) and \(') of the first and second kind as defined
in Eqs. (47) and (48), cos nu>t and sin nut can be approximated
/u-x
arbitrarilyclosely in steady state by T t Mand((l+£)^+n\ x„ / V v 2 x,
i)\JZ—1, where u£nA, respectively. For convenience,we
- 3/ /u(t) -x (t)'
denote these approximatingfunctionsby C (t) A T
 x (t) \ /u(t)-x.(t)
andSn(t)A((l+f)^ +f uj
From Eqs. (31), (43) and (51), we obtain
2tt
na na N rTT
"*£ E LSJ |a0(AorAj'wk>+i=l j=l k=l o ' J
x3(t)
n^ x3(t)
N r
YWa (A .,A.,
£iln 0i J
oi, ) cos no), t
+ b (A . ,A.,ul) sin no), tn oi j k k
1 M
n [ r m
- E E
n=l I U=l
A A
^<Aoi'V V(uk> Cn(T)
+\jt «nAi>V bn,(V Sn(T) dx
V aH('V
It follows from Eq. (54) and the triangular inequality that
NA NA NA0 A oi "
n< E E EI i=l j=l k=l
M
(A«1'W - E ^oP.<An^A^aToK>ox oi' j' k £=1
oJT oi' j' 1JIV k'
-26-
(54)

+
N
+ E
n=l
M
in(Aoi,Aj(lok)- E ^oi'V'nt^
M
-n(Aoi,A B) - E «nJlCAol>V W
J £=1 J )]
NA NA N
A A u)
E° E E
i=i j=i k=i
M
E ^ol^oi'V- aU(V " col(Aoi'*j>"l*^
N
+ E
n=l'
Y „(A .,A.) a . (to. ) - y „(A .,A.) a -(a).)'nil oi j nil k nJl oi j nil k
.+ 6 n(A ^,A.) b 0(iO - 6 „(A .,A.) b „(w, )nil oi' j nil k nil oi* j nilv k ')]
2tt
+
NA \
N
0
E E
i=l j=l
5
k
Y n(A . ,A.) a 0(a). )'nil oi j nil k
6 0(A ,,A.) b 0(a>.)nil oi* j nil k
A E, + En + E„— 1 2 3
where e (t), e (t) are defined by
c s
n n
C (t) - cos nwt + e (t)
n c
n
S (t) = sin nwt + e (t)
n s
n
n
e (t)
c
n
dx
(55)
(56)
(57)
Hence, it follows from Eq. (52) and Step 3 of the algorithm that
E, <
max
1-3 (58)
Moreover, since CoA(-)» Yn£(0, ^j^')? anfc<#) and bnJl^ are
-27-

continuous, it follows from TheoremA.1 in Appendix A that there
exists a 6 € (0,1) such that for any a ^ (0,6 )
E2£^P (59)
Since the Fourier coefficientsof p (t) are by assumptionbounded
s
for any inputtesting signal u.,, (t), there exist a 6 £ (0,1)
such that for any a£ (0,6.)
E3 i-p (60>
Hence, for any a€ (0,6), where 6=min{61,6.}, we obtain from
Eqs. (55) and (58)-(60) the inequality
n < n  
— max
The preceding model is canonical in the sense that given any memristive
one-port satisfying the technical assumptions described earlier, we can
construct a dynamical system model having the same structure given in
Eq. (42). The state equation (42.a) is fixed— independent of the
device or system being modeled — except for the parameter a defining the
nonlinear function p(') which has to be chosen properly so that the time
constant of the model is much smaller than the period of the input signals.
To illustrate the implementation and the validity of the preceding algo
rithm, we present next a hypothetical memristive system and then derive
its associated model. We choose a hypothetical example rather than a real
19
19This choice is to ensure that for anyinput frequency the canonical model
is capable ofdetecting the componentsof the input signalcorrectly in
steady state. Otherwisethe solutionsX3 and x^ in Eq. (42.a) may never
reach the steady state and hence fail to detect the peak values of
u-x-^ and -X2«
-28-

device in order that the input-outputsignal pairs can be generated
accurately on a digital computer.
Example
Let cAl be a 5th-order memristive one-port characterized by
i. = -2x- + 2x2 i
x2 = -x2 + i
x3 =-4x3 +2x4 r y
x4 =-2x4 +i2
x5 = 1 - x5
2 2v = (Xj^+Xj-fx^.+Xg)i A R(x1,x2,x3,x4,x5)i
(61.a)
(61.b)
The block diagram for this system is shown in Fig. 13. The steady state
component of R(x(t)) of the zero-state solution x(t) due to the input
current i(t) « A + A cos u>t has been found analytically and is given by
p (t) A R(x(t)) =ao(Ao,A,o)) + £ Jan(Ao,A,u)) cos ntut
n-1 t
}
where
+ b (A ,A,w) sin nutn o*
/a a x i _l o*2 , 1 A4 . 1 .2 .2 , 1 .4 . Aa_(A_,A,w) = 1 + 2A^ + — A^+— A^A +t A + —r
o o o 2 o 2 o
w2+4
Ik Ao)\2 Ik A\2 A.
+ 4(-2=—1 +16f-?-l + A
w +1
u>2+4/ I6(a>2+1)
A A ? AAA A3(oj2+2)al(Ao,A,u,) =4-f- +4(A2 +A2) -§- + %_ , 2
w +1 a) +4 (u) +l)(w +4)
-29-
(62)
(63)
(64)

2 -^ A2 2A2A=W)
*2<VA»"> "T£5t*\t +T)\+ ° 2^,2 <65>+1 (u> +4)
.2,. 2. /A2 A2\ iA . A (1-u) ) .10, i
.•A'-) = , 2.n2 +lr +ry-(U) +1) \ / b)
3 2
Aq AJ(2-o) )a (A ,A,u) =—^ ^ (66)
5 ° (o)+l)(u>+4)
A4n 2.
a (A A,(o) = AU7 \ (67)
* 16(co +1)Z
3
4A A a) 9 . A A a) A A a)
b, (A ,A,w) =—| + (4AZ + 2AZ) -^ +—£ = . -(68)
1 ° u> +1 ° u> +4 (w +1) (u> +4)
/a2 / o a2\ a2 16A« A2 0)b2(Ao,A,u) =^+A+ff-|- +-f-y- (69)
o) +1 \ / a) +1 (w +4)
3A A a)
b,(A .A.eo) =—=-2 « (70)
J ° (u +1) (to +4)
A4
b, (An,A,o)) = % " 9 (71)
4 ° 4(eo +1)Z
The model parameters and model functions were identified from the above
data and from the system response to the input testing signals
3JD =|i(t) - Ao±+Aj cos tok t Ao±,Aj €{1,2,3,4,5),ufc €{1,2,3,10A}}
The high "testing frequency" w = 10,000 is used to segregate the frequency
independentcomponent of the Fourier coefficienta (A ,A,u>) in Eq. (63)
(see footnote 16). The model parametersdeterminedby the algorithm
subject to n = 0.5 is found to beJ max
<M,.> -(3, &) (72)
There are a total of 28 nonlinear model functions. Observe that if the
Fourier coefficientscontain no frequency independentcomponents then only
-30-

27 (i.e., (2N+1)M, where N=4, M=3) nonlinearmodel functionsneed be
identified. The final nonlinearfunction g(*) for this model is given
as follow:
M=3
TT x 3g(Xl,x2,x3,x4,i)Av(xrx3)+£ ^(Xl,x3) ax /(I +f)
N I|M=3
*3> "J*+f>^
ri-x.
n\ x.
M=3
it x 3
+ g'AVJ^i^
x.
a+f)^ +f
ri-x.
U
n-l\ x. (73)
where the nonlinearmodel functionsy(0, C „(•), Y „(•) and 6 (•) are
OX/ nJo n*>
identifiedusing the precedingalgorithm. Standard computer optimization
techniquesare then used to fit the data points defining each model function
into atwo-dimensionalpolynomialsin x- and x3. The completedescriptions
for these functions are listed in AppendixB.
To verify that the model can indeed mimic the original system for
any input signal that belongs to the setQi ,we compute the predicted
steady state response P.g(t) using the model as well as the exact steady
state response Pg(t) of the given system due to an input i(t) =A +A
cos cot, where (Aq,A,co) = (1,1,1). The resultingwaveforms of p (t)
(dotted curve) and p (t) (solid curve) are shown in Fig. 14. Note the
remarkableresemblancebetween the twowaveforms. To further illustrate
the propertiesof the model, we choose an arbitrary (not amember ofQi )
sinusoidal input i(t) = Acos ait with A=l. The frequencydependenceof
-31-

the Lissajous figures of the model (dotted curve) and those of the orig
inal system (solid curve) are shown in Fig. 15. Observe that as the
excitationfrequency increases the Lissajous figures of the model and
those of the original system shrink and tend to a straight line passing
through the origin. The dc characteristiccurves of the model(dotted
curve) and that of the original system (solid curve) are depicted in
Fig. 16. The model was also tested using a triangular input signal of
period 2tt defined as follow:
r- f«-1>
Kt) = <
for t € [1, it]
(74)
^ f(t "¥) for tG [7r» 2ir]
The output voltage waveform of the model (dotted curve) and that of the
original system (solid curve) are shown inFig. 17. Observe that there
is a closesimilaritybetween the twowaveforms in spite of the fact that
the input signal is not amember of theclass of input signals^U defined
in Eq. (30).
IV. CONCLUSIONS
A broad generalization of memristors to an interesting class of
nonlinear devices and systems called memristive systems has been presented.
The most salient feature of memristive systems is its zero-crossing
property. Observe that in spite of the memory effect which normally
introduces phase shifts in conventional systems, the output of a memristive
system is zero whenever the input is zero and hence the input-output
Lissajous figure always passes through theorigin. Roughly speaking,
therefore, we could say that a memristivesystem is a "zero phase shift"
-32-

dynamical system. Various generic properties of memristive systems have
been derived and shown to coincide with those possessed by many physical
devices and systems. Among the various properties of memristive systems,
the frequency response of the Lissajous figure is especially interesting.
As the excitation frequency increases toward infinity, the Lissajous
figure shrinks and tends to a straight line passing through the origin —
except for some pathological cases where the b.i.b.s. stability property
is not satisfied. The physical interpretation of this phenomenon is that
the system possesses certain inertia and cannot respond as rapidly as the
fast variation in the excitation waveform and therefore must settle to
some equilibrium state. This implies that the hysteretic effect of the
memristive system decreases as the frequency increases and hence it
eventually degenerates into a purely resistive system. Under small-signal
operations, the memristive one-port can be either inductive or capacitive
depending on the biasing point.
We believe that many devices and systems which have so far been
identified as dissipative should actually be modeled as memristive systems.
Only by using such a model can the dynamic behavior be properiy simulated.
Finally, we remark that the model presented can be made exact under dc,
small-signal (for all operating points) or sinusoidal (with dc component)
excitations. Even though our canonical model contains a time-varying
component in the stateequations; namely i- = a(t)x.+b(t)u,we observe that
both a(t) and b(t) tend to zero in steady state. Hence, under steady-state
operation, our canonical model generates into a time-invariant dynamical
system. Furthermore, if the class of input testing signals is confined to
only purely sinusoidalwaveforms, then our canonicalmodel can be drastically
-33-

simplified to a dynamical system characterizedby a 3rd-order time-
invariant state equation and a much simpler output equation.
-34-

APPENDIX A
Lemma A.1
The scalarfunctionsc «(•)> Ykfi(0 and ^nC*) defined via Eqs. (44)-
(46) are continuous functionsof (A,A) £ R x R .
Proof: From Eq. (44)
YM(Ao'A) "\*(AoA- f (ak(Ao,A,u>) -ak(Ao,A,a))J a^GiOdu) (A.l)
From Eq. (A.l) and the Schwarz inequality, we obtain
Y, n(A ,A) - Yi «(A ,A) <kJl o' lk£ o' — J ak(AQ,A,o)) -a^A^A.w)
!v(u) du
The normality of a, (•) implies that
YM(VA) " Yk£(Ao'A) I ak(Ao,A,w) - ak(Ao,A,w)
k
du>
(A.2)
dot (A. 3)
Since av(»,»,u>) are mean-squarecontinuous (Eq. (36)) by assumption,
Y, „(•) is continuous in (A ,A) G R x R . Similar arguments reveal
kJfc o +
that r, „(•) and 6ln(*) are continuousin (A ,A) G R x R *
oZ k£ o +
Lemma A. 2
The steady-state solution of
x =-a(t)x1+b(t)u (A.4)
-35-

where u(t) = A + A cos ait, x.(0) = 0
tends to a constant A .
o
Proof: In Eq. (A.4), a(t) and b(t) are given by Eq. (42.c); namely,
a(t) "'V-Kt and b(t) " I -Kt •K» *•
t+-e t+-e
Hence, the function t h- -a(t)x- + b(t) u(t) is continuous and
the function x. H- -a(t)x- + b(t)u is Lipschitz continuous with
continuousLipschitz function on R, . By the fundamentaltheorem
of differential equations [5,17], there exists a unique solution
xx(t) on R+ (for x]L(0) =0)
i(t) 1—Kt fu(T)dT (A,5)
K
It follows from Eq. (A.5) that the solutionx,(t) corresponding
to u(t) = A + A cos ut tends to A , i.e.,
o o
Lemma A. 3
x-(t) -*• A as t -» °°1 o
Consider the first-order differential equation
x3 =p(u-X]L-x3), x3(0) =0 (A.6)
where the nonlinear function p(.) is defined by Eq. (49), x is the
solution of Eq. (A.4) and u(t) = A + A cos tot. Then for each £ > 0,
there exists a 6G (0,1) such that for any aG (0,6), the solution x3(t)
tends to a constant A; namely
lim |x3(t) -A| <e (A.7)
t-*»
-36-

Proof: From Lemma A.2 the steady-statecomponent of x. (t) is A . Hence
for t21 t , where t is a sufficientlylarge number, Eq. (A.6) is
equivalent to
x3 =p(u-x3) (A.8)
where u(t) = A cos ut. The inequality (A.7) follows from Eq. (A.8).
For a proof of this assertion see [15] 
Remark: The differential equation (A.8) describes a peak detector and
tin steady state the solutionx3(t) for an arbitraryinitial
condition is arbitrarily close to the peak value of any periodic
waveform u(») .
Theorem A.l
Given any e > 0, thereexists a 6 £ (0,1) such that for any a£ (0,6),
and for any input signalu(t) - A + A cos <ot the steady-state solutions
to Eq. (42.a) satisfy the followinginequalities:
|x- - A 1 < £1 1 o' (A. 9)
|x3 - A | <£ (A. 10)
1(1 +1) J-.1 <e
4
(A. 11)
1(1 +f) ^ +f - sin u)t| <£
4
(A. 12)
U-X-
1 COS U)t| < Ex3 (A. 13)
Proof: The inequalities (A.9) and (A.10) follow from Lemma A.2 and
Lemma A.3, respectively. Consider the differential equation for
t
By steady state we mean that the transient component is negligible.
-37-

x„ in Eq. (42.a); namely,
x2 = -x1 + u, x2(0) = 0
It follows from Eq. (A. 5) and u(t) = A + A cos o>t that
x2(t) f (^ '7±7^ f u(s) ds)dTo \ K o /
X / k
o e
-Kt
l \ K ^ . 1 -KtJo V t +Ke
A Ao f*= — sin o)t + — I
b) K 1
+ A cos
A sin WT \
UT "0. .1 -KT)
1 A f sin o)T
dT
(A. 14)
Applying Eq. (A.15) and the triangle inequality, we obtain
A „t
o
Kxn(t) [sin(ot -2 u)\
sin o)T
( ^
dT
J 1+t e1
(1)
C I sin o)T sinorcX . . of 1
A + w
sin wt sin wx
dx < ° v
1 + e
. 1 -Kt T K e
t + — e
K
dT
dt
(where e=2.71828 ...) for all teR+ , Since the integral
{'
sln fa)T dT -*- £ ast +", for sufficientlylarge Kand for
sufficientlylarge t, the solutionx2(t) in steady state is such
that
x2(t) ~ - (sin wt -^ (A.17)
-38-

Hence as K and t increase toward infinity, xAt) becomes almost
periodic. In Eq. (42.a) the*solutionof
X4 =p(~x2 ~x4}» x4(0) =° (A.18)
is almost periodic in steady state when x2(t) is almost periodic
because x^(t) is bounded on R and the function th- p(-x9(t)-x)
is almost periodic [17]. By a similar argument used in the proof
of Lemma A.3, we can assert that given any £ > 0there exists a
64 G(°>1) such that for any aG(0,6^), the steady state component
of x^(t) is arbitrarilyclose to the peak value of -x2(t), i.e.,
lim
t-x»
x4(t)-(i+f)A < e (A.19)
Let 53 €(0,1) denote the associated constant so that for any
aG(0,63) the inequality (A.10) is satisfied. If we choose
6= min{63,6^}, then the inequality (A.11) follows from inequalities
(A.10) and (A.19). Similarly, the inequality (A.12) follows from
Eq. (A.17) and inequality (A.19). The last inequality (A.13)
follows from the inequalities(A.9) and (A.10) *
?
A function f(t) is said to be almost periodic if for any n > 0, there is
an I = £(f,n) > 0such that in any interval of length I there is a tsuch
that |f(t+r) - f(t)| <n for all t€ R. .
-39-

APPENDIX B
The nonlinearmodel functions vfr^Xj), ^(x^x^,Y^te^2^) and
6 (x ,x..) are described in terms of two-dimensionalpolynomialsof the
nx l j
form:
N±=5 N=5
P(Xl,x3) =£ £ a x*"1 x^1 (B.l)
1 J i=l j=l J J
Observe that for eachnonlinearmodel function there are 25 polynomial
coefficients. The list of these coefficientsare as shown in TableB.l,
where a . is located at the ith rowand the jth column associatedwith
each function. These coefficients were determined using the Fletcher-
Powell minimizationalgorithm [18].
-40-

TABLE B.l
<-y>
.749 .024 .199 -.087 .135
.662 -.410 -.150 .108 -.013
v(xx,x3) 1.510 .420 .485 -.040 .006
.134 -.132 .023 .005 -.001
.488 .013 -.003 -.000 .000
.407 -.073 .708 .127 .048
-.388 -.537 .923 -.330 .034
C01(x1,x3) .057 .643 2.764 .243 -.024
.018 -.212 .212 -.066 .006
-.003 .021 -.020 .006 -.001
.295 -.545 -.524 -.078 -.047
-.545 1.008 -.602 .143 -.012
09 1,2^' .326 -.602 -6.779 -.086 .007
-.078 .143 -.086 .020 -.002
.006 -.012 .007 -.002 .000
.162 .059 .219 .047 .018
.016 -.689 .606 -.170 .015
O1^ 1 *^^' -.092 .564 3.977 .124 -.011
.031 -.152 .119 -.032 .003
-.003 .013 -.010 .003 -.000
.056 .335 -.416 .139 -.014
.625 1.992 1.575 3.973 .042
Yn(x1,x3) -.726 1.827 -1.329 .361 -.032
.238 6.461 .388 -.103 .009
-.024 .053 -.036 .010 -.001
-.633 .273 .271 -.144 .017
-.361 -1.074 -2.190 -7.943 -.064
Y12(x1,x3) .947 -2.741 2.115 -.592 .054
-.359 -13.377 -.651 .176 -.016
.038 -.090 .063 -.017 .001
-.317 .619 -.394 .097 -.008
.616 .243 .760 5.102 .016
Y13(x1,x3) -.421 .811 -.511  .125 -.010
.115 8.642 .137 -.033 .003
-.011 .020 -.013 .003 -.000
.160 -.464 -3.412 -.107 1.000
-.211 .701 -.595 .176 -.017
Y21(x1,x3) .103 -.376 -1.964 -.099 .009
-.022 .085 -.075 .023 -.002
.002 -.007 .006 -.002 .000
-41-

-4.058 7.499 30.242 1.067 -3.488
7.499 -13.859 8.276 -1.971 .162
Yoo 'X- »X,j/ -4.478 8.276 72.450 1.177 -.097
1.067 -1.971 1.177 -.280 .023
-.088 .162 -.097 .023 -.002
11.616 -21.466 -65.517 -3.053 6.011
-21.467 39.671 -23.690 5.642 -.464
Y23(x1,x3) 12.820 -23.691 -227.364 -3.369 .277
-3.053 5.642 -3.369 .802 -.066
.251 -.464 .277 -.066 .005
-.306 -.187 .474 -.179 .019
.574 .331 -.867 -6.546 -.035
Y31(x1,x3) -.346 -.191 .514 -.196 .021
.083 .044 -.122 .046 -.005
-.007 -.004 .010 -.004 .000
-3.257 6.021 -3.595 .856 -.070
6.022 -11.127 6.641 218.677 .130
Y32(x±,x3) -3.598 6.645 -3.965 .943 -.078
.857 -1.583 .944 -.225 .018
-.070 .130 -.078 .018 -.002
19.779 -34.663 24.536 -6.979 .662
-37.749 66.006 -46.361 -1339.469 -1.238
Y33(x1,x3) 22.109 -38.421 26.992 -7.640 .723
-5.087 8.778 -6.185 1.757 -.167
.403 -.691 .489 -.139 .013
.001 -.001 .001 -.000 -.946
-.001 .002 -.002 .000 -.000
Y41(x1,x3) .000 -.001 .001 -.000 .000
-.000 .000 -.000 .000 -.000
.000 -.000 .000 -.000 .000
-.022 .045 -.029 .007 34.719
.038 -.078 .051 -.013 .001
Y42(x1,x3) -.021 .045 -.029 .007 -.001
.005 -.010 .007 -.002 .000
-.000 .001 -.001 .000 -.000
.219 -.403 .298 -.087 -313.336
-.351 .657 -.504 .151 -.015
Y43(x1,x3) .196 -.373 .293 -.089 .009
-.045 .087 -.069 .021 -.002
.004 -.007 .006 -.002 .000
-.379 .766 -.499 .127 -.011
.848 2.291 1.065 1.524 .023
6n(Xl,x3) -.583 1.131 -.712 .177 -.015
-42-

.154 3.213 .184 -.045 .004
-.014 .026 -.016 .004 -.000
-.064 "-.193 .269 -.092 .009
-.618 -1.681 -1.310 -2.893 -.033
612(xrx3) .724 -1.682 1.174 -.311 .028
-.237 -6.617 -.351 .091 -.008
.024 -.050 .033 -.009 .001
.121 -.026 -.081 .037 -.004
.249 .615 .671 1.774 .018
613(xrx3) -.375 .911 -.650 .174 -.016
.131 4.137 .200 -.052 .005
-.013 .029 -.019 .005 -.000
-.076 .139 .094 .019 .246
.139 -.255 .151 -.036 .003
621(xrx3) -.083 .151 1.776 .021 -.002
.020 -.036 .021 -.005 .000
-.002 .003 -.002 .000 -.000
-1.155 2.134 19.845 .304 -.875
2.134 -3.944 2.355 -.561 .046
622(x1,x3) -1.275 2.356 10.435 .335 -.028
.304 -.561 .335 -.080 .007
-.025 .046 -.028 .007 -.001
3.796 -7.071 -51.057 -1.011 1.523
-7.021 13.078 -7.839 1.870 -.154
623(xrx3) 4.185 -7.797 -48.070 -1.115 .092
-.994 1.853 -1.111 .265 -.022
.082 -.152 .091 -.022 .002
.015 .009 -.023 .009 -.001
-.028 -.016 .043 .323 .002
631(xrx3) .017 .009 -.025 .010 -.001
-.004 -.002 .006 -.002 .000
.000 .000 -.000 .000 -.000
-.375 .694 -.414 .099 -.008
.694 -1.282 .765 25.052 .015
"on \X-i jXoJ -.414 .765 -.457 .109 -.009
.099 -.182 .109 -.026 .002
-.008 .015 -.009 .002 -.000
2.702 -4.993 2.982 -.710 .058
-4.993 9.228 -5.511 -180.377 -.108
633(Xl,x3) 2.982 -5.511 3.291 -.784 .064
-.710 1.313 -.784 .187 -.015
.058 -.108 .064 -.015 .001
-43-

.000 .000 v -.000 .000 .022
-.000 -.000 .000 -.000 .000
641(xrx3) .000 -.000 -.000 .000 -.000
-.000 .000 .000 -.000 .000
.000 -.000 .000 .000 -.000
.011 .049 -.063 .021 10.558
-.056 -.023 .075 -.029 .003
642(xl,x3) .051 -.019 -.025 .013 -.001
-.016 .011 .002 -.002 .000
.001 -.001 .000 .000 -.000
-.106 -.508 .641 -.217 -110.570
.572 .243 -.769 .301 -.032
643(xrx3) -.524 .190 .259 -.132 .015
.158 -.107 -.025 .023 -.003
-.015 .013 -.000 -.001 .000
-44-

REFERENCES
[1] L. 0. Chua, "Memristors,-rthe Missing CircuitElement," IEEE Trans.
on Circuit Theory, Vol. CT-18, September 1971, pp. 507-519.
[2] G. F. Oster and D. M. Auslander, "The Memristor: A New Bond Graph
Element," Trans, of ASME onDynamical System Measurement and Control,
Vol. 94, No. 3, 1972, pp. 249-252.
[3] G. F. Oster, "A Note on Memristor," IEEE Trans, on Circuits and Systems,
January 1974, p. 152.
[4] L. 0. Chua and C. W. Tseng, "A MemristiveCircuit Model for P-N
Junction Diodes," International Journal of Circuit Theory and
Applications, Vol. 2, December 1974, pp. 367-389.
[5] C. A. Desoer, Notes for a Second Course on LinearSystems, Van Nostrand
Rheinhold, 1970.
[6] L. 0. Chua, Introductionto Nonlinear Circuit Theory, New York:
McGraw-Hill, 1969.
[7] M. Sapoff and R. M. Oppenheim, "Theory and Applicationof Self-Heated
Thermistors,"Proceedingsof IEEE, October 1963, pp. 1292-1305.
[8] A. L. Hodgkin and A. F. Huxley, "A QuantitativeDescriptionof Membrane
Current and Its Application to Conduction in Nerve," Journal of
Physiology, Vol. 117, 1952, pp. 500-544.
[9] V. J. Francis, Fundamentalsof DischargeTube Circuits, London,
England: Metheon & Co. Ltd., 1948.
[10] J. C. Willems, "DissipativeDynamical Systems Part I: General Theory,"
Arch. Rational Mech. Anal., Vol. 45, April - May 1972, pp. 321-351.
[11] W. Hahn, Stabilityof Motion, Berlin, New York (etc): Springer-
Verlag, 1967.
-45-

[12] A. Mauro, "AnomalousImpedance, A PhenomenologicalProperty of
Time-VariantResistance,"Biophy. Journal, Vol. 1, 1961, pp. 353-
372.
[13] L. Weinberg, NetworkAnalysis and Synthesis, New York: McGraw-Hill,
1962.
[14] A. L. Reenstra, "ALow-FrequencyOscillatorUsing PTC and NTC
v Thermistors,"IEEE Trans, on Electron. Devices, Vol. ED-16, No. 6,
June 1969.
[15] L. 0. Chua and R. J. Schilling, "An Algorithmfor Modeling the
SinusoidalInput/SteadyState Response Behavior of Nonlinear Systems
Over a Set ofFrequencies and Amplitudes,"Journal of Franklin
Institute, Vol. 298, No. 2, August 1974, pp. 101-124.
[16] L. Fox and I. B. Parker, ChebyshevPolynomials in Numerical Analysis,
London, England: Oxford, 1968.
[17] J. K. Hale, OrdinaryDifferentialEquations, New York: Wiley-
Interscience, 1969.
[18] R. Fletcher and M. J. D. Powell, "A Rapidly ConvergentDescent
Method of Minimization,"The British Computer Journal, Vol. 6, 1963,
pp. 163-168.
-46-

Ci
<>
1
riNa wiK "'I
♦ ♦ ♦
n vno; *«No Vk; \ v_i!igl vm
"ENa *** ^l
I A
Fig. 1. The Hodgkin-Huxley model.
-47-

I
00
I
Fig. 2. The dc V-I curve of a typical thermistor.

20 V(mV)
Fig. 3. The Potassiumchannel dc characteristics,
-49-

V(volt)t
200
100-
200 I(mA)
Fig. 4. The dc characteristics of a short neon tube.
-50-

I i
Fig. 5. Illustration of Property 4
(a) possible Lissajous figure, (b) impossible Lissajous figure
-51-

0*1 < 0*2
Fig. 6. Frequency response of Lissajousfigures.
-52-

R0(X,I) R,(X,I)
O **+r
Impedance=ZQ(s)
Rn(X.I)
Fig. 7. The small-signalequivalent circuit.
-53-

R„{X) IR.(X,I) IRn(X,D
Fig. 8. The small-signalequivalentcircuit for representation(4)
-54-

slope=R0(XMQXRi(X,I0), at a>=0
1=1
Fig. 9. The small-signalLissajous figures,
-55-

C A A
C'^7^T^C'(T•I,
, 2«PR(T) A a
R| 8-aP -Rl(T'1'
where a=--4" <0 , P=VI =R(T)I2
Fig. 10. The small-signal equivalent circuit for the thermistor,
-56-

6K(n)
GK(n) =9"Kn4
L.-
4g K"4V[V
-n da„(V) d$niV)
dv dv
R,=
an(V)+)9n(V)
4gKn4V |-n daAV) d0n(V)
dv
where an (w) =. O.OI(v +EK +IO)
exp[(v+EK+IO)/lo]-l
)8n(v)=O.I25exp(^^-)
A A
= L,(n,V)
= R,(n,V)
Fig. 11. The small-signal equivalent circuit for the Potassium channel
of the Hodgkin-Huxley model.
-57-

E -5-
(.> 2\ Positive temperature\*J coefficient thermisto
_j) Negative temperature
coefficient thermistor
Fig. 12. A two-thermistorcircuit which functions as an ultra-low
frequency oscillator.
-58-

CSJ
+
V*
*in KgHKX)
— n
2«©-*q£
CM
(VI
+
— +
Fig. 13. The block diagram for the hypothetical example in Section III.
-59-

£
o
o
c
o
15.0
i 10.0
5.0-
0.0
Time (sec)
Fig. 1A. The steady state model response vs. system response.
-60-

00
Ui
/n *
a n
o (D
rt .O
rr c
fD (D
a P
O
o ^
e
3 (0
(D •o
N-/
0
0) Ou
P ft
a P
O
r» (D
p4
(V o
1
CO
Hi
r-» *< r«
CO H«
ft 0)
n (0
0 ca
/"N o
to c
o en
H«
H« H»
cu H«
O 9
c H
2 CO
ft
N-/ M»
• o
M
ft
D*
ft
»
g
a
. 3.0
2.0
1.0
0.0
o- 1.0
Q.
CO
0>
JL^^"
—&
/>
//
^/
^
^7 Frequency =
1
1
0>
-2.0
-3.0
| 3.0
en
2.0
1.0
0.0
-1.0
-2.0
y* '
Freqi
1
jency := 10
Data
Model
y^5
4?&
i£p
-
Freqi
I
»ncy =3
i
— i
•
^
s*^7
Frequency -
1 1
100
L —
-3.0
-1.5 -1.0 -0.5 0.0 0.5 1.0 1.5 -1.5 -1.0 -0.5 0.0 0.5
Excitation
1.0 1.5

200.0 -t
inn n_IUU.U
e
o
Of
© on
teadyst
<
c
_ inA n—
//
-IUU.U
-200.0-
-3.0 -2.0 -1.0 0.0 1.0
dc excitation
2.0 3.0
Fig. 16. The dc characteristicsof the model (dotted curve) and the
system (solid curve)•
-62-

i
cr\
l
2.00
4.00 5.00
Time
Fig. 17. The response due to a triangularinput for the model (dotted
curve) and the system(solid curve).
