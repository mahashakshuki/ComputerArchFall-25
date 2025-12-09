print("STATE MODULE LOADED FROM:", __file__)

from rob import ROBEntry
from memory import Memory

# Config
ROB_SIZE = 8
NUM_REGS = 8

# Instrumentation counters
instr_count = 0
branch_count = 0
branch_mispred = 0

# Memory model
memory = Memory()

# Reorder Buffer
ROB = [ROBEntry() for _ in range(ROB_SIZE)]
rob_head = 0
rob_tail = 0
rob_count = 0

# Registers
reg_file = [0] * NUM_REGS
reg_status = [None] * NUM_REGS   # maps register -> ROB id that will write it (or None)

# Program counter / cycle
PC = 0
cycle = 0
simulation_done = False

# Instruction storage / trace
instruction_queue = []

# Timeline dictionaries (choose canonical key = instruction PC)
# Use PC as key for issue/exec/write/commit so metrics printing is straightforward.
# If you use ROB-id keys elsewhere, convert to PC when recording (see suggested patches).
issue_cycle = {}    # issue_cycle[PC] = cycle
exec_start = {}     # exec_start[PC] = cycle when execution started
exec_end = {}       # exec_end[PC] = cycle when execution finished
write_cycle = {}    # write_cycle[PC] = cycle when value written on CDB
commit_cycle = {}   # commit_cycle[PC] = cycle when retired

# Reservation stations (placeholder)
reservation_stations = []

def clear_reservation_stations():
    for rs in reservation_stations:
        rs.clear()

