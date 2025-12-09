# cdb.py
import state
print("CDB sees state ROB:", id(state.ROB))

def _all_rs_lists():
    return [
        state.RS_ADD_SUB,
        state.RS_NAND,
        state.RS_MUL,
        state.RS_LOAD,
        state.RS_STORE,
    ]

def cdb_broadcast(rob_id, value):
    rob_entry = state.ROB[rob_id]
    rob_entry.value = value
    rob_entry.ready = True
    rob_entry.write_cycle = state.cycle
    if rob_entry.timeline is not None:
     rob_entry.timeline["write"] = state.cycle

    for rs_list in _all_rs_lists():
        for e in rs_list:
            if e.busy:
                if e.Qj == rob_id:
                    e.Vj = value
                    e.Qj = None
                if e.Qk == rob_id:
                    e.Vk = value
                    e.Qk = None

    print(f"CDB: ROB[{rob_id}] ready with value {value}")


