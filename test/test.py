# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from enum import IntEnum
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles

class expected():
    def __init__(self, out, ac, rc, v, z):
        self.out=out
        self.aco=ac
        self.rco=rc
        self.overflow=v
        self.zero=z

class op(IntEnum):
    def getExpected(self, A, B, aci, rci):
    def _nop(self, A, B, aci, rci):
        return expected(0, aci, rci, 0, 1)
    NOP=0
    NOP.getExpected=_nop
    def _neg(self, A, B, aci, rci):
        if B == 0:
            z=1
        else:
            z=0
        return expected(-B, aci, rci, 0, z)
    NEG=1
    NEG.getExpected=_neg
    def _stc(self, A, B, aci, rci):
        return expected(0, 1, rci, 0, 1)
    STC=2
    STC.getExpected=_stc
    def _clc(self, A, B, aci, rci):
        return expected(0, 0, rci, 0, 1)
    CLC=3
    CLC.getExpected=_clc
    def _add(self, A, B, aci, rci):
        sum=A+B
        if sum == 0:
            zero=1
        else:
            zero=0
        if A[3]==B[3] and A[3]!=sum[3]:
            over=1
        else:
            over=0
        aco=sum[4]
        return expected(sum, aco, rci, over, zero)
    ADD=4
    ADD.getExpected=_add
    def _sub(self, A, B, aci, rci):
        sum=A-B
        if sum == 0:
            zero=1
        else:
            zero=0
        if A[3]==B[3] and A[3]!=sum[3]:
            over=1
        else:
            over=0
        aco=sum[4]
        return expected(sum, aco, rci, over, zero)
    SUB=5
    SUB.getExpected=_sub
    def _ldb(self, A, B, aci, rci):
        if B == 0:
            zero=1
        else:
            zero=0
        return expected(B, aci, rci, 0, zero)
    LDB=6
    LDB.getExpected=_ldb
    def _not(self, A, B, aci, rci):
        out=~A
        if out == 0:
            zero=1
        else:
            zero=0
        return expected(out, aci, rci, 0, zero)
    NOT=7
    NOT.getExpected=_not
    def _ior(self, A, B, aci, rci):
        out=A|B
        if out == 0:
            zero=1
        else:
            zero=0
        return expected(out, aci, rci, 0, zero)
    IOR=8
    IOR.getExpected=_ior
    def _xor(self, A, B, aci, rci):
        out=A^B
        if out == 0:
            zero=1
        else:
            zero=0
        return expected(out, aci, rci, 0, zero)
    XOR=9
    XOR.getExpected=_xor
    def _and(self, A, B, aci, rci):
        out=A&B
        if out == 0:
            zero=1
        else:
            zero=0
        return expected(out, aci, rci, 0, zero)
    AND=10
    AND.getExpected=_and
    def _asr(self, A, B, aci, rci):
        out=A>>1
        if out == 0:
            zero=1
        else:
            zero=0
        return expected(out, aci, A[0], 0, zero)
    ASR=11
    ASR.getExpected=_asr
    def _shl(self, A, B, aci, rci):
        out=A<<1
        if out == 0:
            zero=1
        else:
            zero=0
        return expected(out, aci, A[3], 0, zero)
    SHL=12
    SHL.getExpected=_shl
    def _lsr(self, A, B, aci, rci):
        out=A>>1
        out=out&7
        if out == 0:
            zero=1
        else:
            zero=0
        return expected(out, aci, A[0], 0, zero)
    LSR=13
    LSR.getExpected=_lsr
    def _rcl(self, A, B, aci, rci):
        out=A<<1 | aci
        if out == 0:
            zero=1
        else:
            zero=0
        return expected(out, aci, A[3], 0, zero)
    RCL=14
    RCL.getExpected=_rcl
    def _rcr(self, A, B, aci, rci):
        out=A>>1
        out=out&7
        out=out | aci<<3
        if out == 0:
            zero=1
        else:
            zero=0
        return expected(out, aci, A[0], 0, zero)
    RCR=15
    RCR.getExpected=_rcr

class test:
    def __init__(self, a, b, op, aci, rci):
        self.A=a
        self.B=b
        self.opcode=op
        self.aci=aci
        self.rci=rci

# class test{A:4, B:4, opcode:4, aci:1, rci:1, sum:4, aco:1, rco:1, vf:1, zf:1};
tests = [
    test( 6,3,op.ADD,0,0 )
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
    dut.ui_in[3:0].value = A
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
