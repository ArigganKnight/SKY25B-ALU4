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

    # Prepare the values for the next test
    x=0
    A=tests[x].A
    B=tests[x].B
    opcode=int(tests[x].opcode)
    aci=tests[x].aci
    rci=tests[x].rci

    # Put the input into the device
    dut.ui_in.value[3:0] = A
    dut.ui_in[7:4].value = B
    dut.uio_in[3:0].value = opcode
    dut.uio_in[4].value = aci
    dut.uio_in[5].value = rci
    dut.uoi_in[7:6].value = 0
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
    assert tests[x].sum == sum, "sum: {} == {}".format(tests[x].sum, sum)
    # assert tests[x].aco == aco, "aco: {} == {}".format(tests[x].aco, aco)
    # assert tests[x].rco == rco, "rco: {} == {}".format(tests[x].rco, rco)
    # assert tests[x].overflow == overflow, "overflow: {} == {}".format(tests[x].overflow, overflow)
    # assert tests[x].zero == zero, "zero: {} == {}".format(tests[x].zero, zero)

    # Repeat
