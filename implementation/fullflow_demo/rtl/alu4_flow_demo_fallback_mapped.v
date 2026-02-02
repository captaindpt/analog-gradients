module alu4_flow_demo (
    input  [3:0] a,
    input  [3:0] b,
    input  [1:0] op,
    output [3:0] y,
    output       cout
);
    wire n0, n1, n2, n3;
    wire c0;

    AND2X1 u_and0 (.A(a[0]), .B(b[0]), .Y(n0));
    AND2X1 u_and1 (.A(a[1]), .B(b[1]), .Y(n1));
    AND2X1 u_and2 (.A(a[2]), .B(b[2]), .Y(n2));
    AND2X1 u_and3 (.A(a[3]), .B(b[3]), .Y(n3));

    XOR2X1 u_xor0 (.A(n0), .B(op[0]), .Y(y[0]));
    XOR2X1 u_xor1 (.A(n1), .B(op[0]), .Y(y[1]));
    XOR2X1 u_xor2 (.A(n2), .B(op[0]), .Y(y[2]));
    XOR2X1 u_xor3 (.A(n3), .B(op[0]), .Y(y[3]));

    OR2X1  u_or0  (.A(a[3]), .B(b[3]), .Y(c0));
    XOR2X1 u_xor4 (.A(c0), .B(op[1]), .Y(cout));
endmodule
