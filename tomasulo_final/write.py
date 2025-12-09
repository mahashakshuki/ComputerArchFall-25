import state
from cdb import cdb_broadcast

def write():
    for rs in state.reservation_stations:

        if not rs.finished:
            continue

        cdb_broadcast(rs.rob_id, rs.result)

        state.write_cycle[rs.rob_id] = state.cycle

        rs.clear()
