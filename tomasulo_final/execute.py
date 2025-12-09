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

        # Mark start (use instruction PC as canonical key)
        if state.exec_start.get(rs.PC) is None:
            state.exec_start[rs.PC] = state.cycle

        # Decrement counter
        rs.remaining_cycles -= 1

        # Execution not done
        if rs.remaining_cycles > 0:
            continue

        # Execution finished
        state.exec_end[rs.PC] = state.cycle

        # Branch handling
        if rs.op == "BEQ":
            # instrumentation
            state.branch_count += 1
            taken = (rs.vj == rs.vk)
            predicted_taken = False        # always not-taken predictor
            if taken != predicted_taken:
                state.branch_mispred += 1
                correct_target = rs.PC + 1 + rs.offset
                flush_pipeline(correct_target)
                # branch flush returns early so we don't mark finished
                continue
            # else branch predicted correctly → nothing to flush; treat as normal result
            # For BEQ we don't produce a result to writeback necessarily.
            rs.finished = True
        else:
            # Normal result → push to write buffer
            rs.finished = True
