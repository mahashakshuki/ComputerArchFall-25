import state
from cdb import cdb_broadcast

def write():
    for rs in state.reservation_stations:

        if not rs.finished:
            continue

        # Broadcast on CDB using ROB id (ROB index)
        cdb_broadcast(rs.rob_id, rs.result)

        # Record write cycle keyed by instruction PC
        state.write_cycle[rs.PC] = state.cycle

        rs.clear()

