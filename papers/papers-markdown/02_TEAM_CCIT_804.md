# 02_TEAM_CCIT_804.pdf

IRWIN AND JOAN JACOBS 
CENTER FOR COMMUNICATION AND INFORMATION TECHNOLOGIES 
 
TEAM: ThrEshold Adaptive 
Memristor Model 
 
S. Kvatinsky, E. G. Friedman, 
A. Kolodny, and U. C. Weiser 
CCIT Report #804 
January 2012 
 
DEPARTMENT OF ELECTRICAL ENGINEERING 
TECHNION - ISRAEL INSTITUTE OF TECHNOLOGY, HAIFA 32000, ISRAEL 
  
Electronics 
Computers 
Communications 

IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS—I: REGULAR PAPERS, VOL. XXX, NO. XXX, XXX 201X  1
  
Abstract —Memristive devices are novel devices, which can be  
used in applications such as memory, logic, and neu romorphic 
systems. A memristive device offers several advantages to existing 
applications: nonvolatility, good scalability, effectively no leakage 
current, and compatibility with CMOS technology, bo th 
electrically and in terms of manufacturing. Several  models for 
memristive devices have been developed and are disc ussed in this 
paper. Digital applications such as memory and logi c require a 
model that is highly nonlinear, simple for calculat ions, and 
sufficiently accurate. In this paper, a new memrist ive device 
model is presented – TEAM, ThrEshold Adaptive Memri stor 
model. This model is flexible and can be fit to any  practical 
memristive device. Previously published models are compared in 
this paper to the proposed TEAM model. It is shown that the 
proposed model is reasonably accurate and computati onally 
efficient, and is more appropriate for circuit simu lation than 
previously published models. 
 
Index Terms —Memristive systems, memristor, SPICE, window 
function.  
I. INTRODUCTION  
emristors are passive two-port elements with variab le 
resistance (also known as a memristance) [1]. Chang es 
in the memristance depend upon the history of the device ( e.g. , 
the memristance may depend on the total charge pass ed 
through the device, or alternatively, on the integr al over time 
of the applied voltage between the ports of the device). 
Formally, a current-controlled time-invariant memri stive 
system [2] is represented by 
 ( , ), dw f w i dt =  (1) 
 ( ) ( , ) ( ), v t R w i i t = ⋅  (2) 
where w is an internal state variable, i(t) is the memristive 
device current, v(t)  is the memristive device voltage, R(w, i)  is 
the memristance, and t is time. The terms memristor and 
memristive systems are often used interchangeably t o describe 
memristive systems [2]. While there are discussions  in the 
literature about specific definitions [29, 30], in this paper we 
use the term “memristive device” to describe all devices within 
these categories. 
 
Manuscript received January 17 th  , 2012, revised April 8 th , 2012. This 
work was partially supported by Hasso Plattner Inst itute, by the Advanced 
Circuit Research Center at the Technion, and by Intel grant no. 864-737-13. 
S. Kvatinsky, A. Kolodny, and U. C. Weiser are with  the Department of 
Electrical Engineering, Technion – Israel Institute  of Technology, Haifa 
32000, Israel. (S. Kvatinsky corresponding author p hone: 972-4829-4662; 
fax: 972-4829-5757; e-mail: skva@tx.technion.ac.il).  
E. G. Friedman is with the Department of Electrical  Engineering and 
Computer Engineering, University of Rochester, Rochester, NY 14627, USA. 
Since Hewlett-Packard announced the fabrication of a 
working memristive device in 2008 [3], there has be en an 
increasing interest in memristors and memristive systems. New 
devices exhibiting memristive behavior have been an nounced 
[4], [5], and existing devices such as spin-transfe r torque 
magnetoresistive random access memory (STT-MRAM) ha ve 
been redescribed in terms of memristive systems [6].  
Memristive devices can be used for a variety of app lications 
such as memory [7], neuromorphic systems [8], analog circuits 
(e.g. see [9]), and logic design [10], [27].  Different 
characteristics are important for the effective use  of 
memristive devices in each of these applications, a nd an 
appropriate designer friendly physical model of a m emristive 
device is therefore required.  
In this paper, the characteristics of memristive de vices are 
described in Section II. Previously published memri stive 
device models are reviewed in Section III.  TEAM - a new 
model that is preferable in terms of the aforementi oned 
characteristics is proposed in Section IV. In secti on V, a 
comparison between these models is presented. The p aper is 
summarized in Section VI. 
II. REQUIREMENTS FOR MEMRISTIVE DEVICE 
CHARACTERISTICS  
Different applications require different characteri stics from 
the building blocks. Logic and memory applications,  for 
example, require elements for computation and control, as well 
as the ability to store data after computation. The se elements 
require sufficiently fast read and write times. The  read 
mechanism needs to be nondestructive, i.e. , the reading 
mechanism should not change the stored data while r eading. 
To store a known digital state and maintain low sen sitivity to 
variations in parameters and operating conditions, it is crucial 
that the stored data be distinct, i.e. , the difference between 
different data must be sufficiently large. The tran sient power 
consumption while reading and writing, as well as static power 
consumption, are also critical issues. 
Although the definition of a memristive system is q uite 
broad, all memristive systems exhibit a variable re sistance, 
which is related to an internal state variable. Mem ristive 
devices employed in practice exhibit a nonvolatile behavior. 
To provide a nondestructive read mechanism, the int ernal state 
variable needs to exhibit a nonlinear dependence on  charge, 
i.e. , changes in the state variable due to high current s should 
be significant, while changes due to low currents s hould be 
negligible. Other mechanisms where the state variab les return 
to the original position after completing the read process may 
also require the nondestructive read mechanism. For  certain 
TEAM: ThrEshold Adaptive Memristor Model 
Shahar Kvatinsky, Eby G. Friedman, Fellow, IEEE , Avinoam Kolodny, Senior Member , IEEE , and 
Uri C. Weiser, Fellow , IEEE   
M

IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS—I: REGULAR PAPERS, VOL. XXX, NO. XXX, XXX 201X  2
applications such as analog counters, however, a li near 
dependence on charge is preferable, since the curre nt is 
integrated during the counting process. 
To store distinct Boolean data in a memristive devi ce, a 
high ratio between the resistances (typically named  RON  and 
ROFF ) is necessary. Several additional characteristics are 
important for all applications, such as low power consumption, 
good scalability, and compatibility with conventional CMOS. 
These characteristics exist in memristive devices. STT-
MRAM exhibits these characteristics except for the high off/on 
resistance ratio [11]. To design and analyze memris tive 
device-based circuits and applications, a model exh ibiting 
these traits is required. 
III. PREVIOUSLY PROPOSED MEMRISTIVE DEVICE MODELS  
A. Requirements from an Effective Memristive Device 
Model 
An effective memristive device model needs to satis fy 
several requirements: it must be sufficiently accur ate and 
computationally efficient . It is desirable for the  model to be 
simple, intuitive, and closed-form. It is also pref erable for the 
model to be general so that it can be tuned to suit  different 
types of memristive devices. 
B. Linear Ion Drift Model 
A linear ion drift model for a memristive device is suggested 
in [3]. In this model, one assumption is that a dev ice of 
physical width D contains two regions, as shown in Figure 1. 
One region of width w (which acts as the state variable of the 
system) has a high concentration of dopants (originally oxygen 
vacancies of TiO 2, namely TiO 2-x). The second region of width 
D - w is an oxide region (originally TiO 2). The region with the 
dopants has a higher conductance than the oxide reg ion, and 
the device is modeled as two resistors connected in  series. 
Several assumptions are made: ohmic conductance, li near ion 
drift in a uniform field, and the ions have equal a verage ion 
mobility µV. Equations (1) and (2) are, respectively, 
 ( ), ON 
v
Rdw i t dt D µ=  (3) 
 ( ) ( ) ( ) 1 ( ), ON OFF 
w t w t v t R R i t D D 
    = + − ⋅         
 (4) 
where RON  is the resistance when w(t) = D , and ROFF  is the 
resistance when w(t) = 0 . The state variable w(t)  is limited to 
the physical dimensions of the device, i.e. , the value is within 
the interval [0, D] . To prevent w from growing beyond the 
physical device size,  the derivative of w is multiplied by a 
window function, as discussed in the next subsectio n. The I-V 
curve of a linear ion drift memristive device for s inusoidal and 
rectangular waveform inputs is shown in Figure 2. 
 
Figure 1. Linear ion drift memristive device model. The device is 
composed of two regions: doped and undoped. The total resistance of the 
device is the sum of the resistances of both regions. 
C. Window Function 
In the linear ion drift model, the permissible valu e of the 
state variable is limited to the interval [0, D] . To satisfy these 
bounds, (3) is multiplied by a function that nullif ies the 
derivative, and forces (3) to be identical to zero when w is at a 
bound. One possible approach is an ideal rectangula r window 
function (the function where the value is 1 for any  value of the 
state variable, except at the boundaries where the value is 0). It 
is also possible to add a nonlinear ion drift pheno menon, such 
as a decrease in the ion drift speed close to the b ounds, with a 
different window [12], 
 
2
2( ) 1 1 , 
p
wf w D
  = − −     
 (5) 
where p is a positive integer. For large values of p, the window 
function becomes similar to a rectangular window fu nction, 
and the nonlinear ion drift phenomenon decreases, a s shown in 
Figure 3. 
The window function in (5) exhibits a significant p roblem 
for modeling practical devices, since the derivativ e of w is 
forced to zero and the internal state of the device  cannot 
change if w reaches one of the bounds. To prevent this 
modeling inaccuracy, a different window function ha s been 
proposed [13], 
 
2
( ) 1 ( ) , 
p
wf w stp i D
  = − − −     
 (6) 
(7a) 
(7b) 
where i is the memristive device current. This function is 
shown in Figure 4. In the original definition, thes e window 
functions do not have a scale factor and therefore cannot be 
adjusted,  i.e. , the maximum value of the window function 
cannot be changed to a value lower or greater than one. To 
overcome this limitation, a minor enhancement – add ing a 
multiplicative scale factor to the window function, has recently 
been proposed [14]. The proposed window function in [14] is 
 
2
( ) 1 0.5 0.75 , 
p
wf w j D
        = − − +               
 (8) 
where j is a control parameter which determines the maximu m 
value of f(w)  (in this function, the maximum value can be 
smaller or larger than one). This function is shown in Figure 5. 
While these window functions alleviate the bounds i ssue and 
suggest a nonlinear phenomenon, these functions do not 
exhibit full nonlinear ion drift behavior since the  model 
1, 0 ( ) 0, 0, 
istp i i
≥= <
 

IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS—I: REGULAR PAPERS, VOL. XXX, NO. XXX, XXX 201X  3
ignores the nonlinear dependence of the state deriv ative on the 
current. A linear ion drift model with a window fun ction does 
not therefore fully model nonlinear ion drift behavior. 
D. Nonlinear Ion Drift Model 
While the linear ion drift model is intuitive and s atisfies the 
basic memristive system equations, experiments have  shown 
that the behavior of fabricated memristive devices deviates 
significantly from this model and is highly nonline ar [15], 
[16]. The nonlinear I-V characteristic is desirable  for logic 
circuits, and hence more appropriate memristive dev ice 
models have been proposed. In [17], a model is prop osed 
based on the experimental results described in [15] . The 
relationship between the current and voltage is 
 ( ) ( )( ) ( ) sinh ( ) exp ( ) 1 , ni t w t v t v t β α χ γ = + −      (9) 
where α, β, γ, and  χ are experimental fitting parameters, and n 
is a parameter that determines the influence of the  state 
variable on the current. In this model, the state v ariable w is a 
normalized parameter within the interval [0, 1]. Th is model 
assumes asymmetric switching behavior. When the device is in 
the ON state, the state variable w is close to one and the 
current is dominated by the first expression in (9),  βsinh(αv(t)) , 
which describes a tunneling phenomenon. When the de vice is 
in the OFF state, the state variable w is close to zero and the 
current is dominated by the second expression in (9 ),  
χ[exp( λv(t))-1] , which resembles an ideal diode equation.  
This model assumes a nonlinear dependence on voltag e in 
the state variable differential equation, 
 ( ) ( ) , mdw a f w v t dt = ⋅ ⋅  (10) 
where a and m are constants, m is an odd integer, and f(w)  is a 
window function. The I-V relationship of a nonlinea r ion drift 
memristive device for sinusoidal and rectangular wa veform 
inputs is illustrated in Figure 6. A similar model is proposed 
by the same authors in [28]. In this model, the sam e I-V 
relationship is described with a more complex state  drift 
derivative.  
A. Simmons Tunnel Barrier Model 
Linear and nonlinear ion drift models are based on 
representing the two regions of oxide and doped oxi de as two 
resistors in series. A more accurate physical model  was 
proposed in [18]. This model assumes nonlinear and 
asymmetric switching behavior due to an exponential  
dependence of the movement of the ionized dopants, namely, 
changes in the state variable. In this model, rathe r than two 
resistors in series as in the linear drift model, t here is a resistor 
in series with an electron tunnel barrier, as shown  in Figure 7. 
The state variable x is the Simmons tunnel barrier width [19] 
(note that a different notation for the state varia ble is used to 
prevent confusion with the role of the state variab le in the 
linear ion drift model). In this case, the derivati ve of x can be 
interpreted as the oxygen vacancy drift velocity, and is 
sinh exp exp , 0 
( ) 
sinh exp exp , 0, 
off 
off 
off c c 
on 
on 
on c c 
x a ii x c i i w b w dx t 
dt ix a i x c i i w b w 
     −  − − − >                   =       − − − − − <                
 
where coff , con , ioff , ion , aoff , aon , wc, and b are fitting parameters. 
Equation (11) is illustrated in Figure 8 for the me asured fitting 
parameters reported in [18]. The physical phenomena  behind 
the behavior shown in (11)  are not yet fully understood, but 
considered to be a mixture of nonlinear drift at hi gh electric 
fields and local Joule heating enhancing the oxygen  vacancies.  
In practical memristive devices, the ON switching i s 
significantly faster than the OFF switching because  of the 
diffusion of the oxygen vacancies from TiO 2-x to TiO 2, and the 
drift of the oxygen vacancies due to the internal electric field is 
different for positive and negative voltages. For a  negative 
voltage (lower x), the drift of the oxygen vacancies and the 
diffusion are in the same direction, while for a po sitive 
voltage, the direction of diffusion and drift are o pposite [20]. 
The parameters  c off  and con  influence the magnitude of the 
change of x. The parameter con  is an order of magnitude larger 
than the parameter coff . The parameters  i off  and ion  effectively 
constrain the current threshold. Below these curren ts, the 
change in the derivative of x is neglected . A current threshold 
phenomenon is desirable for digital applications. T he 
parameters  aoff  and aon  force, respectively, the upper and lower 
bounds for x. Because of the exponential dependence on x - aoff  
or x - a on , the derivative of the state variable is significa ntly 
smaller for the state variable within the permitted  range. There 
is therefore no need for a window function in this model. 
In this model, the relationship between the current  and 
voltage is shown as an implicit equation based on the Simmons 
tunneling model [19], 
 ( )
( ) ( ) ( )
1/2 
1 1 
1/2 
1 1 
( ) ( , ) ( , )exp ( , ) ( , ) 
( , ) ( , ) | | exp ( , ) ( , ) , 
g g g g 
g g g g g g 
i t A x v v x B v x v x 
A x v v x e v B v x v x ev 
φ φ 
φ φ 
= − ⋅ 
− + − ⋅ + 
%
%
 
 ( ) , g s v v i t R = −  (13) 
where v is the internal voltage on the device, which is no t 
necessarily equal to the applied voltage on the dev ice V (i.e. , 
the external voltage V and the internal voltage v are not 
necessarily the same [18]). 
 
 
 
(11a) 
(11b) 
(12) 

IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS—I: REGULAR PAPERS, VOL. XXX, NO. XXX, XXX 201X  4
 
Figure 2. Linear ion drift model I-V curve. D = 10 nm, RON  = 100 Ω, 
ROFF  = 16 k Ω, µV = 10 -14  m2s-1V-1, and w0 = 1 Rad/s. (a) Sinusoidal voltage 
input for several frequencies ω0, 3 ω0, and 6 ω0, and (b) rectangular 
waveform current input. 
 
 
Figure 3. Window function described by (5) according to [12] for several 
values of p. 
 
 
Figure 4. Window function described by (6) according to [13].  
 
 
 
Figure 5. Window function described by (8) according to [14]. (a) 
Varying p, and (b) varying j. 
 
Figure 6. Nonlinear ion drift model I-V curve. m = 5 , n = 2, a = 1 V -ms-1, β 
= 0.9     µAA AA,  γ = 4 V -1, χ = 10 -4 µAA AA, and  α = 2 V -1. (a) Sinusoidal voltage input 
for several frequencies ω0, 2 ω0, and 3 ω0, and (b) rectangular waveform 
of input voltage. 

IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS—I: REGULAR PAPERS, VOL. XXX, NO. XXX, XXX 201X  5
 
Figure 7. Physical model of Simmons tunnel barrier memristive device. 
The state variable x is the width of the oxide region, V is the applied 
voltage on the device, vg is the voltage in the undoped region, and v is the 
internal voltage in the device. 
 
 
Figure 8. Derivative of the state variable x as described in (11). The 
fitting parameters are coff  = 3.5µm/s, i off  = 115µA, a off  = 1.2nm, c on  = 
40µm/s, i on  = 8.9µA, a on  = 1.8nm, b = 500µA , and  wc = 107pm . 
IV. THR ESHOLD ADAPTIVE MEMRISTOR (TEAM)  MODEL  
In this section, TEAM, a novel memristive device mo del, is 
presented. The integral portion of the TEAM model i s based 
on an expression for the derivative of the internal state variable 
that can be fitted to any memristive device type. U nlike other 
memristive device models, the current-voltage relat ionship is 
undefined and can be freely chosen from any current -voltage 
relationship; several examples of possible current- voltage 
relationships are described in Section IVB. This re lationship is 
not limited to these examples. In subsection A, the  
disadvantages of the aforementioned models and the need for 
such a model are explained. The derivative of the i nternal state 
variable of the memristive device (the relevant exp ression for 
(1)) and examples of the current–voltage relationsh ip (the 
relevant expression for (2)) are described, respect ively, in 
subsections B and C. Proper fitting of the Simmons tunnel 
barrier model to the TEAM model is presented in sub section 
D, as well as the proper window function for this fitting.  
A. Need for a Simplified Model 
The Simmons tunnel barrier model is, to the authors ' best 
knowledge, the most accurate physical model of a Ti O 2 
memristive device. This model is however quite comp licated, 
without an explicit relationship between current an d voltage, 
and not general in nature ( i.e. , the model fits only a specific 
type of memristive device). A complex SPICE model o f the 
Simmons tunnel barrier model is presented in [21]. This model 
is also computational inefficient. A model with sim pler 
expressions rather than the complex equations in th e Simmons 
tunnel barrier model is therefore desired. Yet the accuracy of 
the simple model must be adequate. This simplified model 
represents the same physical behavior, but with sim pler 
mathematical functions. In the next section, simpli fying 
assumptions are introduced. Namely, no change in th e state 
variable is assumed below a certain threshold, and a 
polynomial dependence rather than an exponential de pendence 
is used. These assumptions are applied to support s imple 
analysis and computational efficiency. 
B. State Variable Derivative in TEAM Model 
Note in Figure 9 and (11) that because of the high nonlinear 
dependence of the memristive device current, the me mristive 
device can be modeled as a device with threshold cu rrents. 
This approximation is similar to the threshold volt age 
approximation in MOS transistors. This approximatio n is 
justified, since for small changes in the electric tunnel width, 
separation of variables can be performed. The depen dence of 
the internal state derivative on current and the st ate variable 
itself can be modeled as independently multiplying two 
independent functions; one function depends on the state 
variable x and the other function depends on the current. 
Under these assumptions, the derivative of the stat e variable 
for the simplified proposed model is 
 
( ) 1 ( ), 0 
( ) 0, 
( ) 1 ( ), 0, 
off 
on 
off off off 
off 
on off 
on on on 
on 
i t k f x i i i
dx t i i i dt 
i t k f x i i i
α
α
    ⋅ − ⋅ < <   
     = < < 
   
⋅ − ⋅ < <      
  
where koff , k on , αoff , and  αon  are constants, ioff  and  ion  are current 
thresholds, and  x is the internal state variable, which represents 
the effective electric tunnel width. The constant p arameter koff  
is a positive number, while the constant parameter kon  is a 
negative number. The functions foff (x) and  f on (x) represent the 
dependence on the state variable x. These functions behave as 
the window functions described in section II, which  constrain 
the state variable to bounds of [ , ] on off x x x ∈ . Alternatively, 
these functions can be different functions of x.  The functions 
fon (x)  and foff (x)  are not necessarily equal, since the dependence 
on x may be asymmetric (as in the Simmons tunnel barrie r 
model). Note that the role of x in this model is opposite to w in 
the linear ion drift model. 
C. Current – Voltage Relationship in TEAM Model 
Assume the relationship between the voltage and cur rent of 
a memristive device is similar to (4). The memristance changes 
linearly in x, and (2) becomes 
 ( )( ) ( ). OFF ON 
ON on 
off on 
R R v t R x x i t x x 
  −= + − ⋅   −  
  
 (15) 
The reported change in the resistance however is an  
exponential dependence on the state variable [18], since the 
memristance, in practical memristive devices, is de pendent on 
(14a) 
(14b) 
(14c) 

IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS—I: REGULAR PAPERS, VOL. XXX, NO. XXX, XXX 201X  6
a tunneling effect, which is highly nonlinear. If ( 12) describes 
the current-voltage relationship in the model, the model 
becomes inefficient in terms of computational time and is also 
not general. Therefore, any change in the tunnel ba rrier width 
changes the memristance, and is assumed to change i n an 
exponential manner. Under this assumption, (2) becomes 
 
( )
( ) ( ), 
on 
off on 
x x x x 
ON v t R e i t 
λ −−
= ⋅  (16) 
where λ is a fitting parameter, and RON  and ROFF  are the 
equivalent effective resistance at the bounds, simi lar to the 
notation in the linear ion drift model, and satisfy 
 .OFF 
ON 
R eR
λ=  (17) 
D. Fitting the Simmons Tunnel Barrier Model to the TEAM 
Model 
The TEAM model is inspired by the Simmons tunnel ba rrier 
model. However, to use this model for practical mem ristive 
devices, similar to the Simmons tunnel barrier mode l, a fit to 
the TEAM model needs to be accomplished. Since (14)  is 
derived from a Taylor series, for any desired range  of 
memristive device current λ, k
off , k on , αoff , and  αon  can be 
evaluated to achieve a sufficient accurate match be tween the 
models. As the desired operating current range for the 
memristive device is wider, to maintain sufficientl y accuracy, 
the required αoff  and αon  are higher, thereby increasing the 
computational time. The proper fitting procedure to the current 
threshold is to plot the derivative of the exact st ate variable in 
the actual operating range of the current, and deci de what 
value of the state variable derivative is effective ly zero ( i.e. , 
the derivative of the state variable is significant ly smaller and 
can therefore be neglected). The current at this ef fective point 
is a reasonable value of the current threshold. In this paper, the 
parameters ion  and ioff  are chosen as these current thresholds, 
since these terms represent the exponential depende nce of the 
derivative on the state variable of the current in the Simmons 
tunnel barrier model. A fit of the Simmons tunnel b arrier 
model to the TEAM model is shown in Figure 10 (a). The 
proper current threshold fitting procedure is shown  in Figure 
10 (b). Note that a reasonable current threshold ca n be higher 
than ioff .   
As mentioned in section IV-B, the functions foff (x) and  fon (x) 
are window functions, or alternatively, functions t hat fit the 
Simmons tunnel barrier model based upon the separat ion of 
variables of (11). These functions represent the de pendence of 
the derivative in the state variable x. Based on the fitting 
parameters reported in [18], possible functions fon (x)  and foff (x)  
are 
 ( ) exp exp , 
off 
off 
c
x a f x w
  −  = −     
    
 (18) 
 ( ) exp exp . on 
on 
c
x a f x w
    −= − −     
    
 (19) 
The determination process for (18) and (19) is pres ented in 
Appendix A. Note that (18) and (19) maintain the li mitation of 
certain bounds for the state variable x since the derivative of x 
around aon  when using (18) and (19) is effectively zero for 
positive current ( foff  is practically zero) and negative for 
negative current.  x can only be reduced. The value of x can be 
increased for values of x around aoff . Therefore, a reasonable 
value for the state variable bounds xon  and xoff  is, respectively, 
aoff  and aon . Although the proposed function limits the bounds 
of the state variable, there is no problem when the  bounds are 
exceeded, unlike other window functions. This characteristic is 
useful for simulations, where the bounds can be exc eeded due 
to the discrete nature of simulation engines. The p roposed 
terms, foff  and fon , are illustrated in Figure 11. 
The I-V relationship and state variable behavior of  the 
proposed model are shown in Figures 12 and 13 for a n ideal 
rectangular window function and the proposed window  
function. Note in Figures 12 and 13 that there is a performan ce 
difference between the different window functions. Due to the 
significant nonlinearity, the proposed window funct ion 
constrains the state variable to a low range, and t he memristive 
devices are activated within a significantly smalle r time scale 
as compared to an ideal rectangular window function. The 
required conditions for a sufficient fit of the TEA M model to 
the Simmons tunnel barrier model, as described in A ppendix 
A, cannot be maintained for a symmetric input volta ge due to 
the asymmetry of the Simmons tunnel model. The requ ired 
conditions for a sufficient fit are therefore not m aintained in 
Figure 13. These conditions are however maintained  in Figure 
14, where the behavior of the TEAM model and the Si mmons 
tunnel barrier model is compared and exhibit excell ent 
agreement. While the proposed model fits the Simmon s 
Tunnel Barrier model, the TEAM model is general and  
flexible. The model can fit different physical memr istive 
device models, including other types of memristive devices, 
such as STT-MRAM and Spintronic memristors [6], [24]. 
 
 
Figure 9. Derivative of the state variable x as described in (11) under the 
assumption of a small change in x (x ~ 1.5 nm ). Note that the  device 
exhibits a threshold current. The same fitting parameters as used in 
Figure 8 are used. 

IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS—I: REGULAR PAPERS, VOL. XXX, NO. XXX, XXX 201X  7
 
Figure 10. Fitting between the derivative of the state variable x in the 
Simmons tunnel barrier memristive device model and the TEAM model. 
The same fitting parameters as used in Figure 8 are used for the 
Simmons tunnel barrier model. (a) The fitting parameters for the 
proposed model are koff  = 1.46e-9 nm/sec, αoff  = 10 , ioff  = 115µA, k on  = -
4.68e-13 nm/sec, αon  = 10 , and i on  = 8.9µA . (b) Fitting procedure in a 
logarithmic scale. The operating current range is a ssumed to be 0.1 µA 
to 1 mA and the neglected value for the derivative of the state variable is 
assumed to be 10 -4 nm/sec. For any desired current range, the proper 
fitting parameters can be evaluated to maintain an accurate match 
between the models. For the aforementioned parameters, a reasonable 
current threshold is 0.5 mA (marked as the effective threshold in the 
figure). 
 
 
Figure 11. Proposed fon (x)  and foff (x)  based on (18) and (19). These 
functions represent the dependence on x in (14) and also force bounds 
for x since foff  (x)  is used when dx/dt  is positive and is zero around aon , 
and vice versa for fon (x) . 
 
 
 
Figure 12. The TEAM model driven with a sinusoidal input of 1 volt 
using the same fitting parameters as used in Figure 10, RON  = 50 Ω, ROFF  
= 1 k Ω, and an ideal rectangular window function for fon (x)  in (19) and  
foff (x)  in (18). (a) I-V curve, and (b) state variable x. Note that the device 
is asymmetric, i.e. , switching OFF is slower than switching ON. 
V. COMPARISON BETWEEN THE MODELS  
A comparison between the different memristive devic e 
models is listed in Table I and a comparison betwee n different 
window functions is listed in Table II. A compariso n of the 
accuracy and complexity between the Simmons tunnel barrier 
memristive device and TEAM models is shown in Figur e 14. 
The TEAM model can improve the simulation runtime b y 
47.5% and is sufficiently accurate, with a mean err or of 0.2%. 
These results are dependent on the particular TEAM 
parameters. A lower value for α
ON  and αOFF  produce lower 
accuracy and enhanced computational runtime . The TEAM 
model satisfies the primary equations of a memristi ve system 
as described in (1) and (2), and the convergence co nditions 
and computational efficiency required by simulation engines. 
 
 

IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS—I: REGULAR PAPERS, VOL. XXX, NO. XXX, XXX 201X  8
 
Figure 13. The TEAM model driven with a sinusoidal input of 1 volt 
using the same fitting parameters as used in Figure 10, RON  = 50 Ω, ROFF  
= 1 k Ω,  and proposed fon (x)  in (19) and  foff (x)  in (18) with the same 
parameters used in Figure 8. (a) I-V curve, and (b) state variable x. Note 
that the device is asymmetric, i.e. , switching OFF is slower than 
switching ON. 
 
The TEAM model accurately characterizes not only th e 
Simmons tunnel barrier model, but also a variety of  different 
models. For example, the TEAM model can be fitted t o the 
linear ion drift behavior, where 
,ON 
on off v on 
Rk k i Dµ= =   (20) 
1, on off α α = =   (21) 
0, on off i i = →   (22) 
,on x D =   (23) 
0, off x =   (24) 
.x D w = −   (25) 
 
To include memristive devices into the circuit desi gn 
process, these models need to be integrated into a CAD 
environment, such as SPICE. There are several propo sed 
SPICE macromodels for the linear ion drift model [1 3], [22] 
and the nonlinear ion drift model [17]. A SPICE mod el for the 
Simmons tunneling barrier model has recently been p roposed 
[21], but is complicated and inefficient in terms o f 
computational time. Another simplified model has re cently 
been proposed, assuming voltage threshold and an im plicit 
memristance [25]. In this model, the current and vo ltage are 
related through a hyperbolic sine and the derivative of the state 
variable is an exponent. This model is less general  than the 
TEAM model and more complex in terms of computation al 
time (the model uses sinh and exponents rather than  
polynomials as in the TEAM model). The model is als o less 
accurate than the TEAM model when fitting the model  to the 
Simmons tunnel barrier model.  
The TEAM model can be described in a SPICE 
macromodel similar to the proposed macromodel in [2 3], as 
shown in Figure 15. In this macromodel, the interna l state 
variable is represented by the voltage across the c apacitor C 
and the bounds of the state variable are enforced b y diodes D1  
and D2 . A Verilog-A model is however chosen because it is  
more efficient in terms of computational time than a SPICE 
macromodel, while providing similar accuracy. A Ver ilog-A 
form of the model described in this paper has been 
implemented. The code for these models can be found  in [26]. 
Although the state variable derivative in the TEAM model is 
not a smooth function, it is a continuous function,  based only 
on polynomial functions. The Verilog-A model was te sted in 
complex simulations (hundreds of memristive devices) and did 
not exhibit any convergence issues. 
 
VI. CONCLUSIONS  
Different memristive device models are described in  this 
paper – linear ion drift, nonlinear ion drift, Simm ons tunnel 
barrier, and TEAM (ThrEshold Adaptive Memristor), a s well 
as different window functions. The TEAM model is a flexible 
and convenient model that can be used to characteri ze a 
variety of different practical memristive devices.  This model 
suggests a memristive device should exhibit a curre nt 
threshold and nonlinear dependence on the charge, a s well as a 
dependence on the state variable. 
A comparison between the TEAM model and other 
memristive device models is presented. The TEAM mod el is 
simple, flexible, and general. While the simplicity  of this 
model improves the efficiency of the simulation pro cess, the 
model is sufficiently accurate, exhibiting an avera ge error of 
only 0.2% as compared to the Simmons tunnel barrier  state 
variable. This model fits practical memristive devi ces better 
than previously proposed models. This model is suit able for 
memristive device-based circuit design and has been  
implemented in Verilog-A for SPICE simulations. 
ACKNOWLEDGMENTS  
The authors thank Eilam Yalon and Ori Rottenstreich  for 
their useful comments, and Dmitry Belousov, Slavik Liman, 
Elad Osherov, Zahi Lati, Dmitry Fliter, and Keren 
Talisveyberg for their contributions to the SPICE a nd Verilog-
A simulations. 
 
 
 

IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS—I: REGULAR PAPERS, VOL. XXX, NO. XXX, XXX 201X  9
 
Figure 14. TEAM model fitted to Simmons tunnel barrier model. (a) I-V 
curve for both models, and (b) fitting accuracy in terms of internal state 
variable x and maximum improvement in runtime for MATLAB 
simulations. The state variable average and maximum differences are, 
respectively, 0.2% and 12.77%. The TEAM fitting par ameters are RON  = 
1 k Ω, ROFF  = 100 k Ω, kon  = 4.13e-33 nm/sec, αon  = 25 , koff  = 4.13e-33 
nm/sec, αoff  = 25 , ioff  = 115µA, and i on  = 8.9µA . 
 
 
Figure 15. TEAM SPICE macromodel. The state variable x is the voltage 
across the capacitor C = 1 F . The initial voltage is the initial state 
variable. D1  and D2  constrain the bounds of the state variable to the 
value of the voltage sources xON  and xOFF . GON (i) and  GOFF (i)  are the 
relevant functions from (14). CS(x, i)  is determined from the current – 
voltage relationship, and is i·exp[ λ(x-xon )/(x off -xon )]  for the current – 
voltage relationship in (16). VN and VP are, respectively, the negative and 
positive ports of the memristive device, and i is the memristive device 
current. 
REFERENCES 
[1] L. O. Chua, “Memristor – the Missing Circuit Elemen t,” IEEE 
Transactions on Circuit Theory , Vol. 18, No. 5, pp. 507-519, 
September 1971. 
[2] L.O. Chua and S.M. Kang, “Memristive Devices and Sy stems,” 
Proceedings of the IEEE , Vol. 64, No. 2, pp. 209-223, February 1976. 
TABLE I 
COMPARISON  OF DIFFERENT MEMRISTIVE DEVICE MODELS  
Model Linear ion drift 
[3] 
Nonlinear ion drift 
[17] 
Simmons tunneling 
barrier [18] 
Yakopcic et al  
[25]  
TEAM 
State variable 0 w D ≤ ≤  
Doped region 
physical width 
0 1 w≤ ≤  
Doped region 
normalized width 
off on a x a ≤ ≤  
Undoped region 
width 
0 1 x≤ ≤  
No physical 
explanation 
 
on off x x x ≤ ≤  
Undoped region 
width 
Control mechanism  Current controlled  Voltage controlled  Current controlled  Voltage controlled  Current controlled  
Current-voltage 
relationship and 
memristance deduction 
Explicit I-V relationship – 
explicit 
Memristance deduction 
- ambiguous  
Ambiguous Ambiguous Explicit 
Matching memristive 
system definition 
Yes No No No Yes 
Generic  No  No  No  Moderate  Yes  
Accuracy comparing 
practical memristive 
devices 
Lowest accuracy Low accuracy Highest accuracy Moder ate 
accuracy 
Sufficient accuracy 
Threshold exists  No  No  Practically exists  Yes  Yes  
 
TABLE II 
COMPARISON  OF DIFFERENT WINDOW FUNCTIONS  
Function Joglekar [12] Biolek [13] Prodromakis [14]  TEAM 
f(x)/f(w)  f(w) = 1 -(2w/D -1) 2p f(w) = 1 -(w/D -stp( -i)) 2p f(w)=j(1 -[(w -0.5) 2+0.75] p) fon,off =exp[ -exp(|x -xon,off |/w c)]  
Symmetric  Yes  Yes  Yes  Not necessarily  
Resolve boundary 
conditions 
No Yes Practically yes Practically yes 
Impose nonlinear 
drift 
Partially Partially Partially Yes 
Scale factor 
fmax  < 1  
No No Yes No 
Fits memristive 
device model 
Linear/nonlinear ion 
drift/TEAM 
Linear/nonlinear ion 
drift/TEAM 
Linear/nonlinear ion 
drift/TEAM 
TEAM for Simmons tunneling 
barrier fitting 
 

IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS—I: REGULAR PAPERS, VOL. XXX, NO. XXX, XXX 201X  10 
[3] D. B. Strukov, G. S.Snider, D. R. Stewart, and R. S . Williams, "The 
Missing Memristor Found,” Nature , Vol. 453, pp. 80-83, May 2008. 
[4] D. Sacchetto, M. H. Ben-Jamaa, S. Carrara, G. DeMic heli, and Y. 
Leblebici, "Memristive Devices Fabricated with Sili con Nanowire 
Schottky Barrier Transistors," Proceedings of the IEEE International 
Symposium on Circuits and Systems , pp. 9-12, May/June 2010. 
[5] K. A. Campbell, A. Oblea, and A. Timilsina, "Compac t Method for 
Modeling and Simulation of Memristor Devices: Ion C onductor 
Chalcogenide-based Memristor Devices," Proceedings of the 
IEEE/ACM International Symposium on Nanoscale Archi tectures , pp. 
1-4, June 2010. 
[6] X. Wang, Y. Chen, H. Xi, and D. Dimitrov, “Spintron ic Memristor 
through Spin-Torque-Induced Magnetization Motion,” IEEE Electron 
Device Letters , Vol. 30, No. 3, pp. 294-297, March 2009. 
[7] Y. Ho, G. M. Huang, and P. Li, "Nonvolatile Memrist or Memory: 
Device Characteristics and Design Implications," Proceedings of the 
IEEE International Conference on Computer-Aided Des ign , pp. 485-
490, November 2009. 
[8] A. Afifi, A. Ayatollahi, and F. Raissi, "Implementa tion of Biologically 
Plausible Spiking Neural Network Models on the Memr istor Crossbar-
Based CMOS/Nano Circuits," Proceedings of the European 
Conference on Circuit Theory and Design , pp. 563- 566, August 2009. 
[9] Y.V. Pershin and M. Di Ventra, "Practical Approach to Programmable 
Analog Circuits with Memristors," IEEE Transactions on Circuits and 
Systems I: Regular Papers,  Vol. 57, No. 8, pp.1857-1864, August 
2010. 
[10] G. Snider, "Computing with Hysteretic Resistor Cros sbars," Applied 
Physics A: Materials Science and Processing , Vol. 80, No. 6, pp. 
1165-1172, March 2005. 
[11] Z. Diao, Z. Li, S. Wang, Y. Ding, A. Panchula, E. C hen, L.C. Wang, 
and Y. Huai, "Spin-Transfer Torque Switching in Mag netic Tunnel 
Junctions and Spin-Transfer Torque Random Access Me mory," 
Journal of Physics: Condensed Matter , Vol. 19, No. 16, pp. 1-13, 
April 2007. 
[12] Y. N. Joglekar and S. J. Wolf, “The Elusive Memrist or: Properties of 
Basic Electrical Circuits,” European Journal of Physics , Vol. 30, No. 
4, pp. 661-675, July 2009. 
[13] Z. Biolek, D. Biolek, and V. Biolkova, "SPICE Model  of Memristor 
with Nonlinear Dopant Drift," Radioengineering , Vol. 18, No. 2, Part 
2, pp. 210-214, June 2009. 
[14] T. Prodromakis, B. P. Peh, C. Papavassiliou, and C.  Toumazou, “A 
Versatile Memristor Model with Non-linear Dopant Ki netics,” IEEE 
Transactions on Electron Devices , Vol. 58, No. 9, pp. 3099-3105, 
September 2011. 
[15] J. J. Yang, M. D. Pickett, X. Li, D. A. A. Ohlberg,  D. R. Stewart, and 
R. S. Williams, "Memristive Switching Mechanism for  
Metal/Oxide/Metal Nanodevices," Nature Nanotechnology , Vol. 3, pp. 
429-433, July 2008. 
[16] D. B. Strukov and R. S. Williams, "Exponential Ioni c Drift: Fast 
Switching and Low Volatility of Thin-Film Memristor s,"  Applied 
Physics A: Materials Science and Processing , Vol. 94, No. 3, 515-519, 
March 2009. 
[17] E. Lehtonen and M. Laiho, "CNN Using Memristors for  Neighborhood 
Connections,"  Proceedings of the  International Workshop on Cell ular 
Nanoscale Networks and their Applications , pp. 1-4, February 2010. 
[18] M. D. Pickett, D. B. Strukov, J. L. Borghetti, J. J . Yang, G. S. Snider, 
D. R. Stewart, and R. S. Williams, "Switching Dynam ics in Titanium 
Dioxide Memristive Devices," Journal of Applied Physics,  Vol. 106, 
No. 7, pp. 1-6, October 2009. 
[19] J. G. Simmons, "Generalized Formula for the Electri c Tunnel Effect 
between Similar Electrodes Separated by a Thin Insu lating Film," 
Journal of Applied Physics , Vol. 34, No. 6, pp. 1793-1803, January 
1963. 
[20] D. B. Strukov, J. L. Borghetti, and R. S. Williams,  "Coupled Ionic and 
Electronic Transport Model of Thin-Film Semiconduct or Memristive 
Behavior," Small , Vol. 5, No. 9, pp. 1058-1063, May 2009. 
[21] H. Abdalla and M. D. Pickett, "SPICE Modeling of Me mristors,"  IEEE 
International Symposium on Circuits and Systems , pp.1832-1835, May 
2011. 
[22] S. Benderli and T. A. Wey, "On SPICE Macromodelling  of TiO 2 
Memristors," Electronics Letters , Vol. 45, No. 7, pp. 377-379, March 
2009. 
[23] S. Shin, K. Kim, and S.-M. Kang, "Compact Models fo r Memristors 
Based on Charge-Flux Constitutive Relationships," IEEE Transactions 
on Computer-Aided Design of Integrated Circuits and  Systems , Vol. 
29, No. 4, pp. 590-598, April 2010. 
[24] T. Kawahara et al , "2 Mb SPRAM (Spin-Transfer Torque RAM) with 
Bit-by-Bit Bi-Directional Current Write and Paralle lizing-Direction 
Current Read," IEEE Journal of Solid-State Circuits , Vol. 43, No. 1, 
pp. 109-120, January 2008. 
[25] C. Yakopcic, T. M. Taha, G. Subramanyam, R. E.  Pin o, and S. Rogers, 
"A Memristor Device Model," IEEE  Electron Device Letters , Vol. 32, 
No. 10, pp. 1436-1438, October 2011. 
[26] S. Kvatinsky, K. Talisveyberg, D. Fliter, E. G. Fri edman, A. Kolodny, 
and U. C. Weiser, "Verilog-A for Memristors Models," CCIT Technical 
Report #801 , December 2011.  
[27] S. Kvatinsky, E. G. Friedman, A. Kolodny, and U. C.  Weiser, 
"Memristor-based IMPLY Logic Design Procedure," Proceedings of 
the  IEEE International Conference on Computer Design , pp.142-147, 
October 2011. 
[28] E. Lehtonen, J. Poikonen, M. Laiho, and W. Lu, "Tim e-Dependency of 
the Threshold Voltage in Memristive Devices," Proceedings of the 
IEEE International Symposium on Circuits and System s , pp. 2245-
2248, May 2011. 
[29] D. Biolek, Z. Biolek, and V. Biolkova, "Pinched Hys teresis Loops of 
Ideal Memristors, Memcapacitors, and Meminductors M ust be 'Self-
Crossing'," Electronics Letters ,  Vol. 47, No. 25, pp. 1385-1387, 
December 2011. 
[30] L. O. Chua, "Resistance Switching Memories are Memr istors," Applied 
Physics A: Materials Science & Processing , Vol. 102, No. 4, pp. 765-
783, March 2011. 
 
APPENDIX A – APPROPRIATE FITTING WINDOW FUNCTION TO 
THE SIMMONS TUNNEL BARRIER MODEL  
The purpose of this appendix is to determine a prop er 
window function f(x)  that provides a sufficient fit to the 
Simmons tunnel barrier model. To determine a reason able 
approximation, parameter values from [18] are used.  From 
(11a) and (11b), the derivative of the state variable x is 
 
sinh exp exp , 0 
( ) 
sinh exp exp , 0. 
off 
off 
off c c 
on 
on 
on c c 
x a ii x C i i w b w dx t 
dt ix a i x C i i w b w 
     −  − − − >                   =       − − − − − <                  
The derivative of the state variable is a multiplic and of two 
functions – a hyperbolic sine function which depend s only on 
the current and an exponential function which depen ds on 
both the current and the state variable. To simplif y (A.1) and 
to apply separation of variables, an approximation that 
 
off 
c
on 
c
x a i
w b 
ia x 
w b 
− >> 
− >> 
  
(A.1.a)  
(A.1.b) 
(A.2.a) 
(A.2.b) 

IEEE TRANSACTIONS ON CIRCUITS AND SYSTEMS—I: REGULAR PAPERS, VOL. XXX, NO. XXX, XXX 201X  11 
needs to be assumed. In this appendix, the range of  the 
required state variable for this approximation is d etermined. 
From (A.1) an approximation for f(x)  is provided.  
The Simmons tunnel barrier model is appropriate whe n the 
state variable x is limited by aoff  and aon , i.e., 
 .off on a x a ≤ ≤  (A.3) 
From the parameters in [18], 
 
3
3
3
1.8 1.2 600 0 6 10 107 0.1 
0 6 10 
0 6 10 
off on off 
c c 
off 
c
on 
c
x a a a n
w w p n 
x a 
w
a x 
w
µ µ − − −≤ ≤ = ≈ = ⋅ ⇒ 
−≤ ≤ ⋅ 
−≤ ≤ ⋅ 
 (A.4) 
Assume the maximum current in the device is 100 µA,  
 
100 1 0 . 500 5 
i
b
µ
µ≤ ≤ = 
 (A.5) 
Assume that the value of the state variable is one of the 
effective boundaries aon  and aoff , 
 
1 6000 5
1 6000 5
off off off 
on 
c c c 
on on on 
off 
c c c 
x a x a x a ix a w w b w 
ia x a x a x x a w w b w 
− − − ≈ ⇒ << ≤ ⇒ − ≈ 
− − − ≈ ⇒ << ≤ ⇒ − ≈ 
 (A.6) 
To maintain the same approximation as in (A.6), it is 
sufficient to assume that the value of the expressi on in (A.5) 
is relatively small. Assume that one order of magni tude is 
sufficient for this assumption. The proper range of  x can be 
determined as 
 
1 2 2 5
off 
c off 
c
x a i w a x b w 
−≤ << ≤ ⇒ + ≤ 
 (A.7) 
 
1 2 2 5
on 
on c 
c
i a x x a w b w 
−≤ << ≤ ⇒ ≤ − 
 (A.8) 
For positive current, the derivative of x is positive and 
therefore the value of x is increasing. It is reasonable to 
assume (A.8). Similarly, for negative current, it i s reasonable 
to assume (A.7). Under these assumptions, separatio n of 
variables can be achieved. 
 
0, 
0, 
sinh exp exp , 0 
( ) 
sinh exp exp , 0 
sinh exp exp 
off 
on 
off 
off 
off c c 
on 
on 
on c c 
off 
off 
off c c 
i x a 
i x a 
x a ii x f i i w b w dx t 
dt ix a i x f i i w b w 
x a i x f i w w 
< ≈ 
> ≈ 
     −  − − − >                   =       − − − − − <                
  −  − −           ⇒ ≈ 
, 0 
sinh exp exp , 0 
( ) ( ) ( ) 
exp exp , 0 
( ) 
exp exp , 0 
on 
on 
on c c 
off 
c c 
on 
c c 
i
x a i x f i i w w 
dx t g i f x dt 
x a x iw w 
f x 
x a x iw w 
   >   
          − − − − <              
⇒ = ⋅ 
   −  − − >      
     ⇒ =      − − − − <          
(A.9) 
Based on the parameters in [18] and the exponential  
dependence, the exponential term is significantly g reater than 
the second term,  
 
( )exp exp exp 6000 20 
exp 
on 
off on off on 
c c c c 
off 
c c 
x a 
x a a a ax
w w w w 
x a x
w w 
≈
− −     ⇒ ≈ ≈ >> ≈ ≈     
    
−  ⇒ >>   
  
(A.10) 
And similarly, 
 
exp on 
off 
c c 
x a xx a w w 
  −≈ ⇒ − >>   
  
 (A.11) 
From (A.10) and (A.11), the proposed window functio n is 
therefore 
 
( ) exp exp on 
on 
c
x a f x w
    −= − −     
     (A.12) 
 
( ) exp exp 
off 
off 
c
x a f x w
  −  = −     
     (A.13)
