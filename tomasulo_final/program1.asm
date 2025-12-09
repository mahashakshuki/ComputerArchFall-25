# program1.asm - exercises all instruction types
# PC 0:
ADD R2, R3, R4
SUB R3, R2, R4
NAND R4, R3, R2
MUL R5, R2, R3
LOAD R6, 0(R1)    # load from address in R1
STORE R6, 4(R1)
CALL func
RET

func:
ADD R7, R1, R2
RET
