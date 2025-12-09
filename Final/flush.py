# flush.py
import state 
from rob import ROBEntry

def flush_pipeline(correct_target):
    for i in range(state.ROB_SIZE):
        state.ROB[i] = ROBEntry()

    state.rob_head = 0
    state.rob_tail = 0
    state.rob_count = 0

    for i in range(8):
        state.reg_status[i] = None

    state.PC = correct_target

    print(f"PIPELINE FLUSH (Jump to PC={correct_target})")
