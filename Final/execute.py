import state


def _all_rs_lists():
    return [
        state.RS_ADD_SUB,
        state.RS_NAND,
        state.RS_MUL,
        state.RS_LOAD,
        state.RS_STORE,
        state.RS_BEQ,
        state.RS_CALLRET,
    ]


def execute_stage():
    """
    Execution Stage:
    - Progress running instructions (decrement remaining_cycles)
    - When an instruction finishes:
        * ALU / LOAD / STORE: just mark exec_end; WB/CDB will handle value
        * BEQ: resolve branch + possibly change PC, mark ready
        * CALL: compute return addr + jump, mark ready
        * RET : jump to target, mark ready
    - Start execution for any ready RS entry (operands ready, not executing)
    """

    # ------------------------------------------------------------
    # 1) PROGRESS EXECUTING INSTRUCTIONS
    # ------------------------------------------------------------
    for rs_list in _all_rs_lists():
        for e in rs_list:
            if not (e.busy and e.executing and e.remaining_cycles > 0):
                continue

            # countdown
            e.remaining_cycles -= 1

            # finished this cycle?
            if e.remaining_cycles == 0:
                # safety: rob_idx must be valid
                if e.rob_idx is None:
                    # Should never happen, but avoid crashing
                    continue

                rob = state.ROB[e.rob_idx]

                # record exec end
                if rob.exec_end_cycle is None:
                    rob.exec_end_cycle = state.cycle
                    if getattr(rob, "timeline", None) is not None:
                        rob.timeline["exec_end"] = state.cycle

                # ============ BEQ RESOLUTION ============
                if e.op == "BEQ":
                    state.branch_count += 1

                    taken = (e.Vj == e.Vk)
                    predicted_taken = False  # always-not-taken

                    # actual target
                    if taken:
                        target = rob.PC + 1 + (e.A or 0)
                    else:
                        target = rob.PC + 1

                    # misprediction?
                    if taken != predicted_taken:
                        state.mispredict_count += 1
                        print(f"BRANCH MISPREDICT at PC={rob.PC}, target={target}")
                        state.PC = target

                    # mark branch as completed (so it can commit)
                    rob.ready = True
                    rob.write_cycle = state.cycle
                    if getattr(rob, "timeline", None) is not None:
                        rob.timeline["write"] = state.cycle

                # ============ CALL ============
                elif e.op == "CALL":
                    # CALL: R1 = PC+1 (return address), jump to e.A
                    rob.value = rob.PC + 1
                    rob.ready = True
                    rob.write_cycle = state.cycle
                    if getattr(rob, "timeline", None) is not None:
                        rob.timeline["write"] = state.cycle

                    print(f"CALL: jump to {e.A}, return_addr={rob.value}")
                    state.PC = e.A

                # ============ RET ============
                elif e.op == "RET":
                    # RET: jump to value in R1 (already in Vj)
                    target = e.Vj
                    rob.ready = True
                    rob.write_cycle = state.cycle
                    if getattr(rob, "timeline", None) is not None:
                        rob.timeline["write"] = state.cycle

                    print(f"RET: jump to {target}")
                    state.PC = target

                # For ALU / LOAD / STORE we do nothing special here:
                # they become ready in the CDB/writeback stage.


    # ------------------------------------------------------------
    # 2) START EXECUTION FOR ANY READY RS ENTRY
    # ------------------------------------------------------------
    for rs_list in _all_rs_lists():
        for e in rs_list:
            if not e.busy:
                continue
            if e.executing:
                continue

            # need operands ready
            if e.Qj is not None or e.Qk is not None:
                continue

            # start execution
            e.remaining_cycles = state.exec_latency(e.op)
            e.executing = True

            # safety: skip if rob_idx somehow missing
            if e.rob_idx is None:
                continue

            rob = state.ROB[e.rob_idx]
            if rob.exec_start_cycle is None:
                rob.exec_start_cycle = state.cycle
                if getattr(rob, "timeline", None) is not None:
                    rob.timeline["exec_start"] = state.cycle
