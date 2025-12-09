# program2.asm - simple loop that decrements R2 until zero
# Initialize: R2 = loop count, R1 = base address for loads (assumed pre-init)
loop_start:
BEQ R2, R0, end    # if R2 == 0, end
LOAD R3, 0(R1)
ADD R1, R1, R4     # move pointer (assuming R4=1)
SUB R2, R2, R5     # R5 contains 1
BEQ R0, R0, loop_start   # unconditional branch via BEQ R0,R0,...
end:
RET
