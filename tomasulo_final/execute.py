import state
from flush import flush_pipeline

def execute():
    for rs in state.reservation_stations:

        # Skip empty RS
        if not rs.busy:
            continue

        # If operands not ready → skip
        if not rs.operands_ready():
            continue

        # Mark start
        if state.exec_start.get(rs.rob_id) is None:
            state.exec_start[rs.rob_id] = state.cycle

        # Decrement counter
        rs.remaining_cycles -= 1

        # Execution not done
        if rs.remaining_cycles > 0:
            continue

        # Execution finished
        state.exec_end[rs.rob_id] = state.cycle

        # Branch handling
        if rs.op == "BEQ":
            handle_branch(rs)
        else:
            # Normal result → push to write buffer
            rs.finished = True
