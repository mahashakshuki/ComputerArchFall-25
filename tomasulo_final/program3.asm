# program3.asm - alternating loads/stores and branches to create hazards
# Fill memory with sequence, then loop reading/writing and conditional branches
start:
LOAD R2, 0(R1)
LOAD R3, 1(R1)
ADD R4, R2, R3
STORE R4, 2(R1)
BEQ R2, R3, skip
NAND R5, R2, R3
skip:
SUB R1, R1, R6
BEQ R1, R0, done
BEQ R0, R0, start  # unconditional to start
done:
RET
