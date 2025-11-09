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

# class test{A:4, B:4, opcode:4, aci:1, rci:1, sum:4, aco:1, rco:1, vf:1, zf:1};
# test[]={ };

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
    # A=test[x].A
    # B=test[x].B
    # opcode=test[x].opcode
    # aci=test[x].aci
    # rci=test[x].rci

    # sum=test[x].sum
    # aco=test[x].aco
    # rco=test[x].rco
    # overflow=test[x].overflow
    # zero=test[x].zero

    # Put the input into the device
    #dut.uio_in.value = (0,0,rci,aci,opcode)
    #dut.ui_in.value = (B,A)
    dut.ui_in.value = 20
    dut.uio_in.value = 30

    # Wait for one clock cycle
    await ClockCycles(dut.clk, 1)

    # Extract the output from the device
    # sum = dut.uo_out.value[3:0]
    # aco = dut.uo_out.value[4]
    # rco = dut.uo_out.value[5]
    # overflow = dut.uo_out.value[6]
    # zero = dut.uo_out.value[7]

    # Check the results against the expectation
    assert dut.uo_out.value == 50
    # assert sum == sum
    # assert aco == aco
    # assert rco == rco
    # assert overflow == overflow
    # assert zero == zero

    # Repeat
