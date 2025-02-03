// Sorts the array of length R2 whose first element is at RAM[R1] in ascending order in place. Sets R0 to True (-1) when complete.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

// Input:
// R0 = True (-1)
// R1 = Address of the first element of the array
// R2 = Length of the array
// R3 = minimum pointer
// R4 = current pointer
// R5 = minimum value
// R6 = j innerloop counter
@R1
M=M-1

(OUTERLOOP)
@R2
M=M-1  //Decrement of R2 by 1 every innerloop
D=M
@END
D;JEQ   //goto end when R2==0
@R6
M=D+1     //initialize INNERLOOP counter
@R1
M=M+1  //increment of R1 by 1 every outerloop
D=M
@R3
M=D     //initialize minimum pointer to R1
@R4
AM=D    //initialize current pointer and move to address of R1**
D=M     //get value in R1
@R5
M=D     //initialize minimum value

(INNERLOOP)
@R6
M=M-1  //decrement of j every innerloop
D=M
@SWAP
D;JEQ   //goto swap when complete innerloop, j==0
@R4
AM=M+1  //move current pointer to next
D=M     //get current value
@EDGE
D;JLT   //jump to edge if current value negative
@R5
D=M
@EDGE2
D;JLT   //jump to edge2 if minimum value negative

(COMPARE)
@R4
A=M
D=M     //get current value
@R5
D=M-D   //minimum - current, if minimum is smaller, result will be negative
@INNERLOOP
D;JLE   //goto INNERLOOP if current is bigger or equal to minimum, no update needed
(UPDATE_MINIMUM)
@R4
D=M
@R3
AM=D    //update minimum address and go to that address
D=M
@R5
M=D     //save the latest minimum value
@INNERLOOP
0;JMP

(EDGE)
@R5
D=M
@COMPARE
D;JLT   //if minimum is also negative, continue compare
@UPDATE_MINIMUM
0;JMP   //if minimum is positive replace minimum

(EDGE2)
@R4
A=M
D=M
@COMPARE
D;JLT   //if current is also negative, continue compare
@INNERLOOP
0;JMP   //if current is positive, no replacment needed

(SWAP)
@R1
D=M
@R3
D=M-D
@OUTERLOOP
D;JEQ   //no swap needed if minimum_pointer = R1
@R1
A=M
D=M
@R3
A=M
M=D
@R5
D=M
@R1
A=M
M=D     //swap arr[R1] with arr[minimum_pointer]
@OUTERLOOP
0;JMP

(END)
@R0
M=-1
@END
0;JMP