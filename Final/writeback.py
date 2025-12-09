# writeback.py
import state
from cdb import cdb_broadcast

def _all_rs_lists():
    return [
        state.RS_ADD_SUB,
        state.RS_NAND,
        state.RS_MUL,
        state.RS_LOAD,
        state.RS_STORE,
    ]

def _compute_alu_result(e):
    op = e.op
    vj = e.Vj if e.Vj is not None else 0
    vk = e.Vk if e.Vk is not None else 0

    if op == "ADD":
        return (vj + vk) & 0xFFFF
    if op == "SUB":
        return (vj - vk) & 0xFFFF
    if op == "NAND":
        return (~(vj & vk)) & 0xFFFF
    if op == "MUL":
        return (vj * vk) & 0xFFFF
    return 0

def writeback_stage():
    for rs_list in _all_rs_lists():
        for e in rs_list:
            if e.busy and e.executing and e.remaining_cycles == 0 and e.op != "BEQ":
                rob_entry = state.ROB[e.rob_idx]

                if e.op == "STORE":
                    base = e.Vk if e.Vk is not None else 0
                    addr = (base + (e.A or 0)) & 0xFFFF
                    rob_entry.store_addr = addr
                    rob_entry.store_value = e.Vj
                    rob_entry.ready = True
                    rob_entry.write_cycle = state.cycle
                    if rob_entry.timeline is not None:
                      rob_entry.timeline["write"] = state.cycle
                    print(f"WB: STORE ready addr={addr} val={e.Vj} into ROB[{e.rob_idx}]")

                elif e.op == "LOAD":
                    base = e.Vj if e.Vj is not None else 0
                    addr = (base + (e.A or 0)) & 0xFFFF
                    value = state.mem_load(addr)
                    cdb_broadcast(e.rob_idx, value)
                    print(f"WB: LOAD from addr={addr} value={value} → ROB[{e.rob_idx}]")
                else:
                    result = _compute_alu_result(e)
                    cdb_broadcast(e.rob_idx, result)

                e.busy = False
                e.executing = False
                e.Vj = e.Vk = None
                e.Qj = e.Qk = None
                e.A = None
                e.rob_idx = None
                e.remaining_cycles = 0

                return  # one broadcast per cycle
