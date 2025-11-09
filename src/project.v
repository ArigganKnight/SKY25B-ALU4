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
    assign op = uio_in[3:0];
    assign q = {op[3]&op[2], op[3]&~op[2], ~op[3]&op[2], ~op[3]&~op[2]};
    assign se21 = q[2]&~op[1];
    assign se11 = q[1]&~op[1];
    assign lc[1] = q[2]&op[1]&op[0];
    assign lc[0] = q[3]&op[1] | q[2] | q[1] | q[0]&~op[1];
    assign ls[1] = q[3] | lc[1];
    assign ls[0] = q[3]&op[0] | lc[1] | se11;
    assign fn[3] = ~(op[3]&op[2] | op[0]);
    assign fn[2] = se21 | ~(op[3] | op[0]);
    assign fn[1] = se21 | fn[0];
    assign fn[0] = q[1]&op[0] | q[0]&~(op[1]&op[0]);
    assign ac[1] = se11 | q[0]&!(op[1]|op[0]);
    assign ac[0] = q[0]&!(op[1]^op[0]);

    wire math_carry_in, rot_carry_in;
    wire [3:0] inputA, inputB, right, out;
    reg [3:0] left;
    assign inputA = ui_in[3:0];
    assign inputB = ui_in[7:4];
    assign math_carry_in = uio_in[4];
    assign rot_carry_in = uio_in[5];

    ///rotation & shifting
    wire rci;
    reg rco;
    assign rci =
        lc==2'b00 ? 0:
        lc==2'b01 ? rot_carry_in:
        lc==2'b10 ? inputA[0]:
        lc==2'b11 ? inputA[3]:
    0;
    always@(*) case(ls)
        2'b00: {rco,left} = 5'b0;
        2'b01: {rco,left} = {rci,inputA};
        2'b10: {rco,left} = {inputA,rci};
        2'b11: {left,rco} = {rci,inputA};
    endcase

    ///logic using a LUT
    // for x=[3:0], right[x] <- fn[ {inputB[x],inputA[x]} ]

    ///arithmatic
    wire aci, aco;
    wire [3:0] carry_prop, carry_gen, carry;
    wire [4:0] sum;
    assign aci =
        ac==2'b00 ? 0:
        ac==2'b01 ? 1:
        ac==2'b10 ? math_carry_in:
        ac==2'b11 ? ~math_carry_in:
    0;
    assign carry_prop = left ^ right;
    assign carry_gen = left & right;
    assign {aco,4'carry} = {0,4'carry_gen} | {1,4'carry_prop}&{4'carry,aci};
    assign sum = {0,4'carry_prop} ^ {4'carry,aci};
    //((aci = ac[1]&(math_carry_in ^ ac[0]) | ~ac[1]&ac[0]))
    //{aco,sum} = left+right+aci; w/4-bit sum
    assign out = sum[3:0];

    ///flags
    wire overflow_out, zero_out, lastz, math_carry_out, rot_carry_out;
    wire [3:0] zero;
    assign math_carry_out = aco;
    assign rot_carry_out = rco;
    assign overflow_out = aco ^ carry[3];
    assign {lastz,zero} = ~{0,sum}&{zero,1}; //zero_out = ~|sum;
    assign zero_out = lastz;

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
