# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from enum import Enum
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

class opcode(Enum):
    NOP=0
    NEG=1
    STC=2
    CLC=3
    ADD=4
    SUB=5
    LDB=6
    NOT=7
    IOR=8
    XOR=9
    AND=10
    ASR=11
    SHL=12
    LSR=13
    RCL=14
    RCR=15

@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Set the clock period to 10 us (100 KHz)
    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    # Reset
    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1

    dut._log.info("Test project behavior")

    cri,aci,opcode,B,A=?
    zf,vf,rco,aco,sum=?

    # Set the input values you want to test
    #dut.uio_in.value = (0,0,rci,aci,opcode)
    #dut.ui_in.value = (B,A)
    dut.ui_in.value = 20
    dut.uio_in.value = 30

    # Wait for one clock cycle to see the output values
    await ClockCycles(dut.clk, 1)

    # The following assersion is just an example of how to check the output values.
    # Change it to match the actual expected output of your module:
    assert dut.uo_out.value == 50
    #assert dut.uo_out.value == (zf,vf,rco,aco,sum)

    # Keep testing the module by changing the input values, waiting for
    # one or more clock cycles, and asserting the expected output values.
