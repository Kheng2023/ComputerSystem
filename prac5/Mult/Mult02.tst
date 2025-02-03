// Sample Test file for Mult.asm
// Follows the Test Scripting Language format described in 
// Appendix B of the book "The Elements of Computing Systems"

load Mult.asm,
output-file Mult02.out,
compare-to Mult02.cmp,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2 RAM[2]%D2.6.2;

set PC 0,
set RAM[0] -1,  // Set R0
set RAM[1] -100,  // Set R1
set RAM[2] 50;  // Set R2
repeat 700 {
  ticktock;    // Run for 700 clock cycles
}
set RAM[1] -100,  // Restore arguments in case program used them
set RAM[2] 50,
output;        // Output to file
