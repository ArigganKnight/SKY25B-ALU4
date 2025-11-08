<!---
This file is used to generate your project datasheet. Please fill in the information below and delete any unused sections.

You can also include images in this folder and reference them in the markdown. Each image must be less than 512 kb in size, and the combined size of all images must be less than 1 MB.
-->

## How it works

This ALU is based on the JAM-1 ALU by James Sharman.  Give all due credit to him!  Unlike in JAM-1, this ALU is not pipelined.  In fact, it's completely combinational.  It consists of a shift/rotate block and a logic/LUT block which feed into an adder.  Unlike the JAM-1 ALU, which is 8 bits, this ALU is 4 bits.  The opcode input determines what operation is performed on the inputs.  Like the JAM-1 ALU, this one uses separate carry flags for rotation and arithmetic.  It also generates zero and overflow flags.  It is left to the surrounding circuit to store the flags.  It's capable of at least 25 operations.  (A 26th, ABS, could be added if the surrounding circuit does some work, but I have not implemented this.  It would violate encapsulation.)  I picked 16 operations for demonstration/testing purposes, and packed them into a 4-bit opcode decoder.

UI3-UI0 is input A, UI7-UI4 is input B, and UO3-UO0 is the output.  The flags and opcode are mapped like so:
uo7=zero_out			uio3=opcode3
uo6=overflow_out		uio2=opcode2
uo5=rot_carry_out		uio1=opcode1		uio5=rot_carry_in
uo4=math_carry_out		uio0=opcode0		uio4=math_carry_in

These are the operations I selected and encoded:
Code	Pseudonym	Description
0		NOP			no operation (designed to preserve the carry flags unlike SETC,CLRC,MOVB)
1		NEG	B		negate B (out <= -B)
2		SET	C		set the Carry flag (start new subtraction)
3		CLR	C		clear the Carry flag (start new addition)
4		ADD	A,B		add (out <= A+B)
5		SUB	A,B		subtract (out <= A-B)
6		MOV	B		pass B through (out <= B)
7		NOT	B		invert B (out <= ~B)
8		IOR	A,B		bitwise inclusive OR (out <= A|B)
9		XOR	A,B		bitwise exclusive OR (out <= A^B)
A		AND	A,B		bitwise AND (out <= A&B)
B		ASR	A		arithmetic shift right by 1 bit (preserves sign bit)
C		SHL	A		arithmetic/logic shift left by 1 bit
D		LSR	A		logic shift right by 1 bit (zeros the sign bit)
E		RCL	A		rotate through carry left by 1 bit
F		RCR	A		rotate through carry right by 1 bit

These operations are candidates not selected:
		RESET		output zeros to establish a known clean state (CLR C does exactly this)
		ZERO		output zeros (out <= 0 0000b) (CLR C does exactly this)
		ONE			output one (out <= 0001b)
		NONE		output negative one (out <= 1 1111b)
		INC	B		incrment B (out <= B+1)
		DEC	B		decrement B (out <= B-1)
		MOV	A		pass A through (out <= A)
		NOT	A		invert A (out <= ~A)
		NOR	A,B		output <= ~(A|B)
		XNOR A,B	output <= ~(A^B)
		NAND A,B	output <= ~(A&B)
		ROTL A		rotate left by 1 bit (ignore carry)
		ROTR A		rotate right by 1 bit (ignore carry)
		ABS B		output the absolute value of B -- requires improvements or outside help...

## How to test

Present inputs and wait for the outputs. Compare the results to what's expected. See whether it gets anything wrong, and measure how long it takes. (What's the propogation delay?)

## External hardware

<!--List external hardware used in your project (e.g. PMOD, LED display, etc), if any-->
None so far... None planned...
