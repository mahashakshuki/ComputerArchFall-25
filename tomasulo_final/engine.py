# engine.py
import state 
from issue import issue
from commit import commit

def run_simulation():

    while not state.simulation_done:

        print(f"\nCYCLE {state.cycle}: PC={state.PC}, ROB_count={state.rob_count}")

        commit()
        issue()

        state.cycle += 1

        # End condition: no more instructions & ROB empty
        if state.PC >= len(state.instruction_queue) and state.rob_count == 0:
            state.simulation_done = True

    print("\nSimulation finished in", state.cycle, "cycles")
