# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from enum import IntEnum
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

class op(IntEnum):
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
    def __init__(self, a,b,op,aci,rci, sum,aco,rco,vf,zf):
        self.A=a
        self.B=b
        self.opcode=op
        self.aci=aci
        self.rci=rci
        self.sum=sum
        self.aco=aco
        self.rco=rco
        self.overflow=vf
        self.zero=zf

# class test{A:4, B:4, opcode:4, aci:1, rci:1, sum:4, aco:1, rco:1, vf:1, zf:1};
tests = [
    test( 6,3,op.STC,0,0, 0,1,0,0,0 ),
    test( 6,3,op.CLC,0,0, 0,0,0,0,0 ),
    test( 6,3,op.ADD,0,0, 9,0,0,0,0 )
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

    for test in tests:
        # Prepare the values for the next test
        A=test.A
        B=test.B
        opcode=int(test.opcode)
        aci=test.aci
        rci=test.rci

        # Put the input into the device
        dut.ui_in.value[3:0] = A
        dut.ui_in.value[7:4] = B
        dut.uio_in.value[3:0] = opcode
        dut.uio_in.value[4] = aci
        dut.uio_in.value[5] = rci
        dut.uio_in.value[7:6] = 0
        # dut.uio_in.value = (rci<<5) | (aci<<4) | opcode

        # Wait for one clock cycle
        await ClockCycles(dut.clk, 1)

        # Extract the output from the device
        out = dut.uo_out.value
        sum = out[3:0]
        aco = out[4]
        rco = out[5]
        overflow = out[6]
        zero = out[7]

        # Check the results against the expectation
        dut._log.info("Testing {}".format(test.opcode.name))
        assert test.sum == sum, "sum: {} == {}".format(test.sum, sum)
        # assert test.aco == aco, "aco: {} == {}".format(test.aco, aco)
        # assert test.rco == rco, "rco: {} == {}".format(test.rco, rco)
        # assert test.overflow == overflow, "overflow: {} == {}".format(test.overflow, overflow)
        # assert test.zero == zero, "zero: {} == {}".format(test.zero, zero)

    # Repeat
