# issue.py

import state
from instruction import Instruction


CONTROL_OPS = ("BEQ", "CALL", "RET")


def _select_rs_group(op: str):
    """
    Map opcode to the correct Reservation Station group.
    """
    if op in ("ADD", "SUB"):
        return state.RS_ADD_SUB
    if op == "NAND":
        return state.RS_NAND
    if op == "MUL":
        return state.RS_MUL
    if op == "LOAD":
        return state.RS_LOAD
    if op == "STORE":
        return state.RS_STORE
    if op == "BEQ":
        return state.RS_BEQ
    if op in ("CALL", "RET"):
        return state.RS_CALLRET
    return None


def _has_unresolved_control():
    """
    Non-speculative model:
    If there is ANY older BEQ/CALL/RET in the ROB that is not ready,
    we stall issuing new instructions.
    """
    count = state.rob_count
    idx = state.rob_head
    for _ in range(count):
        entry = state.ROB[idx]
        if (
            entry.busy
            and entry.op in CONTROL_OPS
            and not entry.ready
        ):
            return True
        idx = (idx + 1) % state.ROB_SIZE
    return False


def issue():
    """
    ISSUE stage:
    - If PC past end of instruction queue → nothing to issue.
    - Check ROB space.
    - Enforce non-speculative behavior for BEQ/CALL/RET.
    - Pick appropriate RS group and find a free entry.
    - Allocate and initialize ROB entry.
    - Fill RS entry with operands and ROB index.
    - Perform register renaming for destination registers.
    """
    # No instruction to issue
    if state.PC >= len(state.instruction_queue):
        return

    instr: Instruction = state.instruction_queue[state.PC]

    # 1) Check ROB availability
    if state.rob_count >= state.ROB_SIZE:
        print("ISSUE: ROB full → stalling")
        return

    # 2) Non-speculative control flow:
    #    If any older BEQ/CALL/RET is still unresolved, we stall.
    if _has_unresolved_control():
        print("STALL: unresolved BEQ/CALL/RET in ROB → non-speculative issue")
        return

    # 3) Choose Reservation Station group
    rs_group = _select_rs_group(instr.op)
    if rs_group is None:
        print(f"ISSUE: Unsupported op {instr.op}, stalling")
        return

    # Find a free RS entry
    rs_entry = None
    for e in rs_group:
        if not e.busy:
            rs_entry = e
            break

    if rs_entry is None:
        print(f"ISSUE: No free RS for {instr.op}, stalling")
        return

    # 4) Allocate ROB entry at tail
    rob_idx = state.rob_tail
    rob_entry = state.ROB[rob_idx]

    # Reset / initialize ROB entry
    rob_entry.busy = True
    rob_entry.op = instr.op
    rob_entry.dest = instr.dest
    rob_entry.value = None
    rob_entry.ready = False
    rob_entry.PC = instr.PC

    rob_entry.store_addr = None
    rob_entry.store_value = None

    rob_entry.is_branch = (instr.op == "BEQ")
    rob_entry.predicted_taken = False
    rob_entry.actual_taken = False
    rob_entry.correct_target = None

    rob_entry.issue_cycle = state.cycle
    rob_entry.exec_start_cycle = None
    rob_entry.exec_end_cycle = None
    rob_entry.write_cycle = None
    rob_entry.commit_cycle = None

    # Timeline record
    record = {
        "seq": len(state.timeline_records),
        "pc": instr.PC,
        "op": instr.op,
        "issue": state.cycle,
        "exec_start": None,
        "exec_end": None,
        "write": None,
        "commit": None,
    }
    state.timeline_records.append(record)
    rob_entry.timeline = record

    # Advance ROB tail
    state.rob_tail = (state.rob_tail + 1) % state.ROB_SIZE
    state.rob_count += 1

    # 5) Initialize RS entry common fields
    rs_entry.busy = True
    rs_entry.op = instr.op
    rs_entry.rob_idx = rob_idx
    rs_entry.executing = False
    rs_entry.remaining_cycles = 0
    rs_entry.Vj = None
    rs_entry.Vk = None
    rs_entry.Qj = None
    rs_entry.Qk = None
    rs_entry.A = None

    # -------------------------------------------------
    # 6) OPERAND SETUP PER INSTRUCTION TYPE
    # -------------------------------------------------

    # Helper to fill a source operand from a register
    def _read_src(reg_num):
        p = state.reg_status[reg_num]
        if p is None:
            return state.reg_file[reg_num], None  # value, no dependency
        else:
            return None, p                        # wait for ROB p

    # ---- Arithmetic / logic ----
    if instr.op in ("ADD", "SUB", "NAND", "MUL"):
        vj, qj = _read_src(instr.src1)
        vk, qk = _read_src(instr.src2)
        rs_entry.Vj, rs_entry.Qj = vj, qj
        rs_entry.Vk, rs_entry.Qk = vk, qk

    # ---- BEQ ----
    elif instr.op == "BEQ":
        vj, qj = _read_src(instr.src1)
        vk, qk = _read_src(instr.src2)
        rs_entry.Vj, rs_entry.Qj = vj, qj
        rs_entry.Vk, rs_entry.Qk = vk, qk
        rs_entry.A = instr.imm   # branch offset

    # ---- LOAD: LOAD rA, offset(rB) ----
    elif instr.op == "LOAD":
        base = instr.src1
        offset = instr.imm
        vj, qj = _read_src(base)
        rs_entry.Vj, rs_entry.Qj = vj, qj
        rs_entry.Vk, rs_entry.Qk = None, None
        rs_entry.A = offset      # offset; addr computed in execute/WB

    # ---- STORE: STORE rA, offset(rB) ----
    elif instr.op == "STORE":
        base = instr.src1        # address base
        val_reg = instr.src2     # value reg
        offset = instr.imm

        vj, qj = _read_src(base)
        vk, qk = _read_src(val_reg)

        rs_entry.Vj, rs_entry.Qj = vj, qj
        rs_entry.Vk, rs_entry.Qk = vk, qk
        rs_entry.A = offset

    # ---- CALL label ----
    elif instr.op == "CALL":
        # No true data deps; A holds absolute target PC (set in parser)
        rs_entry.Vj = rs_entry.Vk = None
        rs_entry.Qj = rs_entry.Qk = None
        rs_entry.A = instr.imm   # target PC
        # CALL writes return address to R1
        rob_entry.dest = 1

    # ---- RET ----
    elif instr.op == "RET":
        # RET uses R1 as source
        vj, qj = _read_src(1)
        rs_entry.Vj, rs_entry.Qj = vj, qj
        rs_entry.Vk, rs_entry.Qk = None, None

    # -------------------------------------------------
    # 7) DESTINATION REGISTER RENAMING
    # -------------------------------------------------
    dest_reg = None
    if instr.op in ("ADD", "SUB", "NAND", "MUL", "LOAD"):
        dest_reg = instr.dest
    elif instr.op == "CALL":
        dest_reg = 1  # R1

    if dest_reg is not None and dest_reg != 0:
        state.reg_status[dest_reg] = rob_idx

    # -------------------------------------------------
    # 8) METRICS + PC ADVANCE
    # -------------------------------------------------
    state.instructions_issued += 1
    print(f"ISSUE: {instr.op} (PC={instr.PC}) → ROB[{rob_idx}], RS[{instr.op}]")
    state.PC += 1
