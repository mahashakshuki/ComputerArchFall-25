# flush.py
import state 
from rob import ROBEntry
from state import clear_reservation_stations

def flush_pipeline(correct_target):

    # Clear ROB
    for i in range(state.ROB_SIZE):
        state.ROB[i] = ROBEntry()

    state.rob_head = 0
    state.rob_tail = 0
    state.rob_count = 0

    # Clear reg status
    for i in range(8):
        state.reg_status[i] = None

    # Clear RS
    clear_reservation_stations()

    # Fix PC
    state.PC = correct_target

    print(f"PIPELINE FLUSH (Jump to PC={correct_target})")
