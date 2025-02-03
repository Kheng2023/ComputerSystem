// Sample Test file for ArrSort.asm
// Follows the Test Scripting Language format described in 
// Appendix B of the book "The Elements of Computing Systems"

load ArrSort.asm,
output-file ArrSort02.out,
compare-to ArrSort02.cmp,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2 RAM[2]%D2.6.2 RAM[20]%D2.6.2 RAM[21]%D2.6.2 RAM[22]%D2.6.2 RAM[23]%D2.6.2 RAM[24]%D2.6.2 RAM[25]%D2.6.2 RAM[26]%D2.6.2 RAM[27]%D2.6.2 RAM[28]%D2.6.2 RAM[29]%D2.6.2;

set PC 0,
set RAM[0]  34,  // Set R0
set RAM[1]  20, // Set R1
set RAM[2]  10,  // Set R2
set RAM[20] 2,  // Set Arr[0]
set RAM[21] 8,  // Set Arr[1]
set RAM[22] 0,  // Set Arr[2]
set RAM[23] 1;  // Set Arr[3]
set RAM[24] -1;  // Set Arr[4]
set RAM[25] 0;  // Set Arr[5]
set RAM[26] 0;  // Set Arr[6]
set RAM[27] 9;  // Set Arr[7]
set RAM[28] -2;  // Set Arr[8]
set RAM[29] -8;  // Set Arr[9]
repeat 2000 {
  ticktock;    // Run for 600 clock cycles
}
set RAM[1] 20,  // Restore arguments in case program used them
set RAM[2] 10,
output;        // Output to file

