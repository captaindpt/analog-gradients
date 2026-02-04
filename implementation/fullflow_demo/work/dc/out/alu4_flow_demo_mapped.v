/////////////////////////////////////////////////////////////
// Created by: Synopsys DC Expert(TM) in wire load mode
// Version   : W-2024.09-SP2
// Date      : Tue Feb  3 19:56:43 2026
/////////////////////////////////////////////////////////////


module alu4_flow_demo_DW01_sub_0 ( A, B, CI, DIFF, CO );
  input [4:0] A;
  input [4:0] B;
  output [4:0] DIFF;
  input CI;
  output CO;
  wire   n1, n2, n3, n4, n5, n6, n7, n8, n9, n10, n11, n12, n13, n14, n15, n16,
         n17, n18, n19, n20, n21, n22;

  INVX1 U1 ( .A(A[3]), .Y(n1) );
  INVX1 U2 ( .A(n10), .Y(n2) );
  INVX1 U3 ( .A(n19), .Y(n3) );
  INVX1 U4 ( .A(B[2]), .Y(n4) );
  INVX1 U5 ( .A(B[1]), .Y(n5) );
  INVX1 U6 ( .A(B[0]), .Y(n6) );
  OR2X1 U7 ( .A(n7), .B(n8), .Y(DIFF[4]) );
  AND2X1 U8 ( .A(n2), .B(n1), .Y(n8) );
  AND2X1 U9 ( .A(B[3]), .B(n9), .Y(n7) );
  OR2X1 U10 ( .A(n2), .B(n1), .Y(n9) );
  XOR2X1 U11 ( .A(n10), .B(n11), .Y(DIFF[3]) );
  XOR2X1 U12 ( .A(n1), .B(B[3]), .Y(n11) );
  OR2X1 U13 ( .A(n12), .B(n13), .Y(n10) );
  AND2X1 U14 ( .A(A[2]), .B(n14), .Y(n13) );
  AND2X1 U15 ( .A(n15), .B(n4), .Y(n12) );
  OR2X1 U16 ( .A(A[2]), .B(n14), .Y(n15) );
  XOR2X1 U17 ( .A(n14), .B(n16), .Y(DIFF[2]) );
  XOR2X1 U18 ( .A(A[2]), .B(n4), .Y(n16) );
  OR2X1 U19 ( .A(n17), .B(n18), .Y(n14) );
  AND2X1 U20 ( .A(A[1]), .B(n19), .Y(n18) );
  AND2X1 U21 ( .A(n20), .B(n5), .Y(n17) );
  OR2X1 U22 ( .A(A[1]), .B(n19), .Y(n20) );
  XOR2X1 U23 ( .A(n3), .B(n21), .Y(DIFF[1]) );
  XOR2X1 U24 ( .A(B[1]), .B(A[1]), .Y(n21) );
  OR2X1 U25 ( .A(n22), .B(n3), .Y(DIFF[0]) );
  OR2X1 U26 ( .A(A[0]), .B(n6), .Y(n19) );
  AND2X1 U27 ( .A(A[0]), .B(n6), .Y(n22) );
endmodule


module alu4_flow_demo ( a, b, op, y, cout );
  input [3:0] a;
  input [3:0] b;
  input [1:0] op;
  output [3:0] y;
  output cout;
  wire   N17, N18, N19, N20, N21, n49, n50, n51, n52, n53, n54, n55, n56, n57,
         n58, n59, n60, n61, n62, n63, n64, n65, n66, n67, n68, n69, n70, n71,
         n72, n73, n74, n75, n76, n77, n78, n79, n80, n81, n82, n83, n84, n85,
         n86, n87, n88, n89, n90, n91, n92, n93, n94, n95, n96, n97, n98, n99,
         n100, n101, n102, n103, n104, n105, n106, n107, n108, n109, n110,
         n111, n112, n113, n114, n115, n116;

  alu4_flow_demo_DW01_sub_0 sub_22 ( .A({1'b0, a}), .B({1'b0, b}), .CI(1'b0), 
        .DIFF({N21, N20, N19, N18, N17}) );
  OR2X1 U53 ( .A(n49), .B(n50), .Y(y[3]) );
  OR2X1 U54 ( .A(n51), .B(n52), .Y(n50) );
  AND2X1 U55 ( .A(N20), .B(n53), .Y(n52) );
  AND2X1 U56 ( .A(n54), .B(n55), .Y(n51) );
  OR2X1 U57 ( .A(n56), .B(n57), .Y(n49) );
  AND2X1 U58 ( .A(b[3]), .B(n58), .Y(n57) );
  OR2X1 U59 ( .A(n59), .B(n60), .Y(n58) );
  AND2X1 U60 ( .A(n61), .B(a[3]), .Y(n59) );
  AND2X1 U61 ( .A(n62), .B(n63), .Y(n56) );
  AND2X1 U62 ( .A(n64), .B(n65), .Y(n62) );
  INVX1 U63 ( .A(n66), .Y(n65) );
  AND2X1 U64 ( .A(n67), .B(n68), .Y(n66) );
  OR2X1 U65 ( .A(a[3]), .B(b[3]), .Y(n68) );
  OR2X1 U66 ( .A(n67), .B(n55), .Y(n64) );
  XOR2X1 U67 ( .A(a[3]), .B(b[3]), .Y(n55) );
  OR2X1 U68 ( .A(n69), .B(n70), .Y(y[2]) );
  OR2X1 U69 ( .A(n71), .B(n72), .Y(n70) );
  AND2X1 U70 ( .A(n73), .B(b[2]), .Y(n72) );
  OR2X1 U71 ( .A(n74), .B(n75), .Y(n73) );
  AND2X1 U72 ( .A(a[2]), .B(n76), .Y(n75) );
  OR2X1 U73 ( .A(n77), .B(n61), .Y(n76) );
  AND2X1 U74 ( .A(n78), .B(n79), .Y(n74) );
  AND2X1 U75 ( .A(n80), .B(n81), .Y(n71) );
  INVX1 U76 ( .A(b[2]), .Y(n81) );
  OR2X1 U77 ( .A(n82), .B(n83), .Y(n80) );
  AND2X1 U78 ( .A(n77), .B(n79), .Y(n83) );
  INVX1 U79 ( .A(a[2]), .Y(n79) );
  AND2X1 U80 ( .A(n63), .B(n84), .Y(n77) );
  AND2X1 U81 ( .A(a[2]), .B(n78), .Y(n82) );
  OR2X1 U82 ( .A(n85), .B(n54), .Y(n78) );
  AND2X1 U83 ( .A(n63), .B(n86), .Y(n85) );
  INVX1 U84 ( .A(n84), .Y(n86) );
  AND2X1 U85 ( .A(N19), .B(n53), .Y(n69) );
  OR2X1 U86 ( .A(n87), .B(n88), .Y(y[1]) );
  OR2X1 U87 ( .A(n89), .B(n90), .Y(n88) );
  AND2X1 U88 ( .A(N18), .B(n53), .Y(n90) );
  AND2X1 U89 ( .A(n54), .B(n91), .Y(n89) );
  OR2X1 U90 ( .A(n92), .B(n93), .Y(n87) );
  AND2X1 U91 ( .A(n63), .B(n94), .Y(n93) );
  XOR2X1 U92 ( .A(n95), .B(n91), .Y(n94) );
  XOR2X1 U93 ( .A(b[1]), .B(a[1]), .Y(n91) );
  AND2X1 U94 ( .A(n96), .B(n61), .Y(n92) );
  AND2X1 U95 ( .A(a[1]), .B(b[1]), .Y(n96) );
  OR2X1 U96 ( .A(n97), .B(n98), .Y(y[0]) );
  OR2X1 U97 ( .A(n99), .B(n100), .Y(n98) );
  AND2X1 U98 ( .A(n61), .B(n95), .Y(n100) );
  AND2X1 U99 ( .A(n101), .B(op[1]), .Y(n61) );
  AND2X1 U100 ( .A(n102), .B(n103), .Y(n99) );
  OR2X1 U101 ( .A(n54), .B(n63), .Y(n103) );
  AND2X1 U102 ( .A(op[1]), .B(op[0]), .Y(n54) );
  XOR2X1 U103 ( .A(b[0]), .B(a[0]), .Y(n102) );
  AND2X1 U104 ( .A(N17), .B(n53), .Y(n97) );
  OR2X1 U105 ( .A(n104), .B(n105), .Y(cout) );
  OR2X1 U106 ( .A(n60), .B(n106), .Y(n105) );
  AND2X1 U107 ( .A(n107), .B(n63), .Y(n106) );
  AND2X1 U108 ( .A(b[3]), .B(n108), .Y(n107) );
  OR2X1 U109 ( .A(a[3]), .B(n67), .Y(n108) );
  AND2X1 U110 ( .A(n63), .B(n109), .Y(n60) );
  AND2X1 U111 ( .A(n67), .B(a[3]), .Y(n109) );
  OR2X1 U112 ( .A(n110), .B(n111), .Y(n67) );
  AND2X1 U113 ( .A(a[2]), .B(n84), .Y(n111) );
  AND2X1 U114 ( .A(b[2]), .B(n112), .Y(n110) );
  OR2X1 U115 ( .A(a[2]), .B(n84), .Y(n112) );
  OR2X1 U116 ( .A(n113), .B(n114), .Y(n84) );
  AND2X1 U117 ( .A(a[1]), .B(n95), .Y(n114) );
  AND2X1 U118 ( .A(b[1]), .B(n115), .Y(n113) );
  OR2X1 U119 ( .A(n95), .B(a[1]), .Y(n115) );
  AND2X1 U120 ( .A(a[0]), .B(b[0]), .Y(n95) );
  AND2X1 U121 ( .A(n116), .B(n101), .Y(n63) );
  INVX1 U122 ( .A(op[0]), .Y(n101) );
  AND2X1 U123 ( .A(N21), .B(n53), .Y(n104) );
  AND2X1 U124 ( .A(n116), .B(op[0]), .Y(n53) );
  INVX1 U125 ( .A(op[1]), .Y(n116) );
endmodule

