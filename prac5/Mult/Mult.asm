// This file is based on part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: Mult.asm

// Multiplies R1 and R2 and stores the result in R0.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
@R0
M=0     //initialize R0
@R1
D=M
@END
D;JEQ   //Goto END if R1 is zero
@R2
D=M
@END
D;JEQ   //Goto END if R2 is zero

@negate
M=0     //initialize flag for negative

@R1
D=M
@NEGATIVE1
D;JLT
(CONTINUE)   
@R2
D=M
@NEGATIVE2
D;JLT

(COMPARE)
@R1
D=M
@R2
D=M-D
@SWAP
D;JGT

(LOOP)
@R1
D=M
@R0
M=D+M
@R2
M=M-1  //Decrement of R2
D=M
@LOOP
D;JGT   //if R2 is still more than 0, continue loop
@negate
D=M
@CHECK
D;JLT   //negate the R0 if -1(TRUE)
@END
0;JMP

(NEGATIVE1)
D=!D
D=D+1
@R1
M=D
@negate
M=!M
@CONTINUE
0;JMP

(NEGATIVE2)
D=!D
D=D+1
@R2
M=D
@negate
M=!M
@COMPARE
0;JMP

(SWAP)
@R2
D=M
@temp
M=D     //put R2 value in temp
@R1
D=M
@R2
M=D     //save R1 value in R2
@temp
D=M
@R1
M=D     //save temp(R2 value) into R1
@LOOP
0;JMP

(CHECK)
@R0
M=!M
M=M+1
(END)
@END
0;JMP