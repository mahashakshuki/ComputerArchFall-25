def commit():
    if state.rob_count == 0:
        return

    entry = state.ROB[state.rob_head]

    if not entry.busy or not entry.ready:
        return

    # STORE commits early (no register write)
    if entry.op == "STORE":
        # record under instruction PC
        if entry.PC is not None:
            state.commit_cycle[entry.PC] = state.cycle
        else:
            state.commit_cycle[f"ROB{state.rob_head}"] = state.cycle
        entry.busy = False
        advance()
        return

    # Normal commit
    if entry.dest is not None and entry.dest != 0:
        state.reg_file[entry.dest] = entry.value

    if entry.PC is not None:
        state.commit_cycle[entry.PC] = state.cycle
    else:
        state.commit_cycle[f"ROB{state.rob_head}"] = state.cycle

    entry.busy = False
    advance()
