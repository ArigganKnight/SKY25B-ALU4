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

class test:
    def __init__(self, a, b, op, aci, rci, sum, aco, rco, over, zero):
        self.A=a
        self.B=b
        self.opcode=op
        self.aci=aci
        self.rci=rci
        self.sum=sum
        self.aco=aco
        self.rco=rco
        self.overflow=over
        self.zero=zero

# class test{A:4, B:4, opcode:4, aci:1, rci:1, sum:4, aco:1, rco:1, vf:1, zf:1};
tests = [
    test( 2,3,ADD,0,0, 5, 0,0,0,0 )
]

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

    # Prepare the values for the next test
    x=0
    A=tests[x].A
    B=tests[x].B
    opcode=tests[x].opcode
    aci=tests[x].aci
    rci=tests[x].rci

    # Put the input into the device
    dut.ui_in.value = B<<4|A
    dut.uio_in.value = rci<<5 | aci<<4 |opcode

    # Wait for one clock cycle
    await ClockCycles(dut.clk, 1)

    # Extract the output from the device
    out = dut.uo_out.value
    sum = out&15
    aco = (out>>4)&1
    rco = (out>>5)&1
    overflow = (out>>6)&1
    zero = (out>>7)&1

    # Check the results against the expectation
    assert dut.uo_out.value == 50
    assert sum == tests[x].sum
    assert aco == tests[x].aco
    assert rco == tests[x].rco
    assert overflow == tests[x].overflow
    assert zero == tests[x].zero

    # Repeat
