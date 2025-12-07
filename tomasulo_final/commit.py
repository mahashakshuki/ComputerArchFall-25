# commit.py
import state 
print("COMMIT sees state ROB:", id(state.ROB))
def commit():
    if state.rob_count == 0:
        return

    entry = state.ROB[state.rob_head]

    if not entry.busy:
        return

    if not entry.ready:
        return

    print(f"COMMIT: ROB[{state.rob_head}] → Reg[{entry.dest}] = {entry.value}")

    if entry.dest is not None and entry.dest != 0:
        state.reg_file[entry.dest] = entry.value

    entry.busy = False
    state.rob_head = (state.rob_head + 1) % state.ROB_SIZE
    state.rob_count -= 1
