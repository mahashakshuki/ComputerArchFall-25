; ============================================
; Program 1: Full Test (NO infinite loop)
; Tests: LOAD, STORE, ADD, SUB, NAND, MUL, BEQ, CALL, RET
; Program ends normally by falling off the end.
; ============================================

        ; Assume:
        ; Mem[0] = 10
        ; Mem[1] = 5

        LOAD   R2, 0(R0)       ; R2 = Mem[0] = 10
        LOAD   R3, 1(R0)       ; R3 = Mem[1] = 5

        ADD    R4, R2, R3      ; R4 = 10 + 5 = 15
        SUB    R5, R4, R3      ; R5 = 15 - 5 = 10
        NAND   R6, R4, R5      ; R6 = ~(15 & 10)
        MUL    R7, R2, R3      ; R7 = 10 * 5 = 50 (long latency)

        STORE  R2, 2(R0)       ; Mem[2] = 10
        STORE  R7, 3(R0)       ; Mem[3] = 50

; ---- BEQ test: NOT taken path ----
; R2 = 10, R3 = 5 → not equal → branch NOT taken

        BEQ    R2, R3, skip    ; should NOT branch
        ADD    R4, R4, R4      ; executes: R4 = 15 + 15 = 30

skip:
; ---- CALL + RET test ----
        CALL   func            ; jumps to func, saves return PC in R1

        ; After return from func:
        ADD    R4, R4, R3      ; R4 = previous R4 + 5

        ; Program ends here by falling off the end.

; ============================================
; Function: func
; ============================================
func:
        ADD    R5, R5, R2      ; R5 = 10 + 10 = 20
        RET                    ; return to caller

