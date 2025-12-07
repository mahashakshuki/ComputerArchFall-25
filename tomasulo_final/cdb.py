# cdb.py
import state 
print("CDB sees state ROB:", id(state.ROB))


def cdb_broadcast(rob_id, value):
    state.ROB[rob_id].value = value
    state.ROB[rob_id].ready = True
    print(f"CDB: ROB[{rob_id}] ready with value {value}")
