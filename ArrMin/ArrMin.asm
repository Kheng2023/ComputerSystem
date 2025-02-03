// Finds the smallest element in the array of length R2 whose first element is at RAM[R1] and stores the result in R0.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Put your code here.
//Initialize R0 with 1st element
@R1
A=M
D=M
@R0
M=D
@n 
M=0   

(LOOP)
//While n < R2
@R2
D=M
@n
M=M+1
D=D-M
@END
D;JEQ

//Read the address from R1
@n
D=M
@R1
A=D+M   //go to address of array[n]
D=M     //Get the element in the array[n]

//compare the result stored at R0 with i, if smaller then update R0 with smaller value
@i
M=D     //temporary store the value at i
@EDGE
D;JLT   //jump to edge case when i is negative
@R0
D=M
@EDGE2
D;JLT   //jump to edge when R0 is negative

(COMPARE)
@i
D=M
@R0
D=M-D   //compare R0 and i
@LOOP
D;JLT   //if R0 value is lower, no exchange needed, goto LOOP
@i
D=M
@R0
M=D     //replace R0 with value of i
@LOOP
0;JMP

(END)
@END
0;JMP

(EDGE)
@R0
D=M
@COMPARE
D;JLT
@i
D=M
@R0
M=D
@LOOP
0;JMP

(EDGE2)
@i
D=M
@COMPARE
D;JLT
@LOOP
0;JMP