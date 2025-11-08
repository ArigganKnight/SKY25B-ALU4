/*
 * Copyright (c) 2025 Ariggan Knight
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_Ariggan_Knight_ALU4 (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // clock
    input  wire       rst_n     // reset_n - low to reset
);

    ///opcode decoder
    wire se21, se11;            //subexpressions
    wire [1:0] lc, ls, ac;      //left carry, left select, adder carry
    wire [3:0] q, fn, op;       //opcode space quradrant, logic function, opcode
    // op<-opcode<-uio_in[3:0];
    // q = {op[3]&op[2], op[3]&~op[2], ~op[3]&op[2], ~op[3]&~op[2]};
    // se21 = q[2]&~op[1]; se11 = q[1]&~op[1];
    // lc[1] = q[2]&op[1]&op[0];
    // lc[0] = q[3]&op[1] | q[2] | q[1] | q[0]&~op[1];
    // ls[1] = q[3] | lc[1];
    // ls[0] = q[3]&op[0] | lc[1] | se11;
    // fn[3] = ~(op[3]&op[2] | op[0]);
    // fn[2] = se21 | ~(op[3] | op[0]);
    // fn[1] = se21 | fn[0];
    // fn[0] = q[1]&op[0] | q[0]&~(op[1]&op[0]);
    // ac[1] = se11 | q[0]&!(op[1]|op[0]);
    // ac[0] = q[0]&!(op[1]^op[0]);

    wire math_carry_in, rot_carry_in;
    wire [3:0] inputA, inputB, left, right, out;
    // inputA = ui_in[3:0]; inputB = ui_in[7:4];
    // math_carry_in = uio_in[4];
    // rot_carry_in = uio_in[5];

    ///rotation & shifting
    wire rci, rco;
    // lc==0 -> rci <- 0;
    // lc==1 -> rci <- rot_carry_in;
    // lc==2 -> rci <- inputA[0];
    // lc==3 -> rci <- inputA[3];
    // ls==0 -> {rco,left} <- 5'b0;
    // ls==1 -> {rco,left} <- {rci,inputA};
    // ls==2 -> {rco,left} <- {inputA,rci};
    // ls==3 -> {left,rco} <- {rci,inputA};

    ///logic using a LUT
    // for x=[3:0], right[x] <- fn[ {inputB[x],inputA[x]} ]

    ///arithmatic
    wire aci, aco;
    wire [3:0] carry_prop, carry_gen, carry;
    wire [4:0] sum;
    // ac==0 -> aci <- 0;
    // ac==1 -> aci <- 1;
    // ac==2 -> aci <- math_carry_in;
    // ac==3 -> aci <- ~math_carry_in;
    //   //((aci <- ac1^(cin+ac0) | !ac1^ac0))
    //   //{aco,sum} <- left+right+aci;
    // carry_prop = left ^ right; carry_gen = left & right;
    // {aco,carry} = {0,carry_gen} | {1,carry_prop}^{carry,aci};
    // sum = {0,carry_prop} ^ {carry,aci};
    // out = sum[3:0];

    ///flags
    wire overflow_out, zero_out, zflag, math_carry_out, rot_carry_out;
    wire [3:0] zero;
    // math_carry_out = aco;
    // rot_carry_out = rco;
    // overflow_out = aco ^ carry[3];
    // {zflag,zero} = ~{0,sum}&{zero,1}; zero_out = zflag; //zero <- ~|sum;

    // uo_out[3:0] = out;
    // uo_out[4] = math_carry_out;
    // uo_out[5] = rot_carry_out;

    assign uo_out  = ui_in + uio_in;  // Example: uo_out is the sum of ui_in and uio_in

    //Bidir outputs will not be used, but they must still be assigned to.
    assign uio_out = 0;
    assign uio_oe  = 0;
    // List all unused inputs to prevent warnings
    wire _unused = &{ena, clk, rst_n, 1'b0};
    // wire _unused = &{ena, clk, rst_n, ui_in[7], ui_in[6], 1'b0};

endmodule
