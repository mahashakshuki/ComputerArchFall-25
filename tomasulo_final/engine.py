from issue import issue
import state 
from commit import commit
from execute import execute
from write import write

def run_simulation():

    while not state.simulation_done:

        print(f"\nCYCLE {state.cycle}: PC={state.PC}, ROB_count={state.rob_count}")

        # Order: COMMIT → WRITE → EXECUTE → ISSUE
        commit()
        write()
        execute()
        issue()

        state.cycle += 1

        if state.PC >= len(state.instruction_queue) and state.rob_count == 0:
            state.simulation_done = True

    print("\nSimulation finished in", state.cycle, "cycles")
