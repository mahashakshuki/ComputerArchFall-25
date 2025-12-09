# issue.py
import state 
print("ISSUE sees state ROB:", id(state.ROB))


def issue():
    if state.PC >= len(state.instruction_queue):
        return

    if state.rob_count == state.ROB_SIZE:
        print("STALL: ROB full")
        return

    instr = state.instruction_queue[state.PC]
    rob_id = state.rob_tail
    entry = state.ROB[rob_id]
    



    entry.busy = True
    entry.op = instr.op
    entry.dest = instr.dest
    entry.ready = False
    entry.PC = instr.PC

    state.rob_tail = (state.rob_tail + 1) % state.ROB_SIZE
    state.rob_count += 1

    if instr.dest is not None and instr.dest != 0:
        state.reg_status[instr.dest] = rob_id

    print(f"ISSUE: Instruction {instr.op} → ROB[{rob_id}]")
    state.issue_cycle[state.PC] = state.cycle

    state.PC += 1
