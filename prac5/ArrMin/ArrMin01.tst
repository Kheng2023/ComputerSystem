// Sample Test file for ArrMin.asm
// Follows the Test Scripting Language format described in 
// Appendix B of the book "The Elements of Computing Systems"

load ArrMin.asm,
output-file ArrMin01.out,
compare-to ArrMin01.cmp,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2 RAM[2]%D2.6.2 RAM[24]%D2.6.2 RAM[25]%D2.6.2 RAM[26]%D2.6.2 RAM[27]%D2.6.2 RAM[28]%D2.6.2;

set PC 0,
set RAM[0]  0,  // Set R0
set RAM[1]  24, // Set R1
set RAM[2]  5,  // Set R2
set RAM[24] 10,  // Set Arr[0]
set RAM[25] 5,  // Set Arr[1]
set RAM[26] -32767,  // Set Arr[2]
set RAM[27] 3;  // Set Arr[3]
set RAM[28] -100;  // Set Arr[4]
repeat 300 {
  ticktock;    // Run for 300 clock cycles
}
set RAM[1] 24,  // Restore arguments in case program used them
set RAM[2] 5,
output;        // Output to file

