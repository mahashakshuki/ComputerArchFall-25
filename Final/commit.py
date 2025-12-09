import state
print("COMMIT sees state ROB:", id(state.ROB))

def commit():
    if state.rob_count == 0:
        return

    entry = state.ROB[state.rob_head]

    # Entry must be both busy AND ready to commit
    if not entry.busy or not entry.ready:
        return

    # =====================================================
    # STORE
    # =====================================================
    if entry.op == "STORE":
        addr = entry.store_addr
        val = entry.store_value
        state.mem_store(addr, val)
        print(f"COMMIT: STORE to Mem[{addr}] = {val}")

    # =====================================================
    # BEQ
    # =====================================================
    elif entry.op == "BEQ":
        print(f"COMMIT: BEQ at PC={entry.PC}")

    # =====================================================
    # CALL
    # =====================================================
    elif entry.op == "CALL":
        # R1 = PC+1 saved into entry.value
        state.reg_file[1] = entry.value
        if state.reg_status[1] == state.rob_head:
            state.reg_status[1] = None
        print(f"COMMIT: CALL → R1 = {entry.value}")

    # =====================================================
    # RET
    # =====================================================
    elif entry.op == "RET":
        # RET does not write any register.
        print(f"COMMIT: RET at PC={entry.PC}")

    # =====================================================
    # NORMAL ALU / LOAD (writes a register)
    # =====================================================
    else:
        if entry.dest is not None and entry.dest != 0:
            state.reg_file[entry.dest] = entry.value

            # Clear rename table if this ROB entry produced the value
            if state.reg_status[entry.dest] == state.rob_head:
                state.reg_status[entry.dest] = None

        print(f"COMMIT: ROB[{state.rob_head}] op={entry.op} → Reg[{entry.dest}] = {entry.value}")




    # =====================================================
    # Advance ROB head + metrics
    # =====================================================
    state.instructions_committed += 1
    entry.busy = False
    entry.commit_cycle = state.cycle
    if entry.timeline is not None:
        entry.timeline["commit"] = state.cycle

    state.rob_head = (state.rob_head + 1) % state.ROB_SIZE
    state.rob_count -= 1
