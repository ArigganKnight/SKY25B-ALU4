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

  // lc=0 -> rci <- 0;
  // lc=1 -> rci <- rot_carry_in;
  // lc=2 -> rci <- inputA[0];
  // lc=3 -> rci <- inputA[3];
  // ls=0 -> left <- 4'b0; rco <- rci;
  // ls=1 -> left <- inputA; rco <- rci;
  // ls=2 -> {rco,left} <- {inputA,rci};
  // ls=3 -> {left,rco} <- {rci,inputA};
  // rot_carry_out <- rco;
  // for x=[3:0], right[x] <- function[ {inputB[x],inputA[x]} ]
  // ac=0 -> aci <- 0;
  // ac=1 -> aci <- 1;
  // ac=2 -> aci <- math_carry_in;
  // ac=3 -> aci <- ~math_carry_in;
  //   //((aci <- ac1^(cin+ac0) | !ac1^ac0))
  // {aco,sum} <- left+right+aci; math_carry_out <- aco;
  // vflag <- sum.carry[3] ^ sum.carry[2]; overflow_out <- vflag;
  // zflag <- nor(sum); zero_out <- zflag;

  assign uo_out  = ui_in + uio_in;  // Example: uo_out is the sum of ui_in and uio_in

  //Bidir outputs will not be used, but they must still be assigned to.
  assign uio_out = 0;
  assign uio_oe  = 0;
  // List all unused inputs to prevent warnings
  wire _unused = &{ena, clk, rst_n, 1'b0};

endmodule
