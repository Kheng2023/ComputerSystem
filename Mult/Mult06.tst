// Sample Test file for Mult.asm
// Follows the Test Scripting Language format described in 
// Appendix B of the book "The Elements of Computing Systems"

load Mult.asm,
output-file Mult06.out,
compare-to Mult06.cmp,
output-list RAM[0]%D2.6.2 RAM[1]%D2.6.2 RAM[2]%D2.6.2;

set PC 0,
set RAM[0] -22222,  // Set R0
set RAM[1] 11111,  // Set R1
set RAM[2] 2;  // Set R2
repeat 50 {
  ticktock;    // Run for 50 clock cycles
}
set RAM[1] 11111,  // Restore arguments in case program used them
set RAM[2] 2,
output;        // Output to file