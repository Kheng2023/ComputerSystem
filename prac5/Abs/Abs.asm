// Calculates the absolute value of R1 and stores the result in R0.
// (R0, R1 refer to RAM[0], and RAM[1], respectively.)

// Put your code here.
//If R1>=0 goto END
    @1
    D=M
    @STORE
    D;JGE
//Negate value of R1
    @1
    D=M
    D=!D
    D=D+1
    M=D
(STORE)
//Store value to R0
    @0
    M=D
(END)
    @END
    0;JMP