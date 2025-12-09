import state

def commit():
    if state.rob_count == 0:
        return

    entry = state.ROB[state.rob_head]

    if not entry.busy or not entry.ready:
        return

    # STORE commits early (no register write)
    if entry.op == "STORE":
        state.commit_cycle[state.rob_head] = state.cycle
        entry.busy = False
        advance()
        return

    # Normal commit
    if entry.dest is not None and entry.dest != 0:
        state.reg_file[entry.dest] = entry.value

    state.commit_cycle[state.rob_head] = state.cycle
    entry.busy = False
    advance()

def advance():
    state.rob_head = (state.rob_head + 1) % state.ROB_SIZE
    state.rob_count -= 1
