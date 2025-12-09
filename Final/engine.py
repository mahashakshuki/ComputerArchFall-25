# engine.py
import state
from issue import issue
from commit import commit
from execute import execute_stage
from writeback import writeback_stage

def run_simulation(max_cycles=5000):
    while True:
        print(f"\nCYCLE {state.cycle}:")
        issue()
        execute_stage()
        writeback_stage()
        commit()

        state.cycle += 1

        # ----- HALT CONDITION -----
        if (
            state.PC >= len(state.instruction_queue)  # no more instructions to issue
            and state.rob_count == 0                 # ROB empty
            and all_rs_empty()                       # all RS are empty
        ):
            print("\n=== PROGRAM FINISHED ===")
            break

        # Safety net: avoid infinite runaway
        if state.cycle > max_cycles:
            print("\n!!! ERROR: Infinite loop detected — stopping simulation !!!")
            break


def all_rs_empty():
    for group in (
        state.RS_ADD_SUB,
        state.RS_NAND,
        state.RS_MUL,
        state.RS_LOAD,
        state.RS_STORE,
        state.RS_BEQ,
        state.RS_CALLRET,
    ):
        for e in group:
            if e.busy:
                return False
    return True

