# state.py
print("STATE MODULE LOADED FROM:", __file__)

from rob import ROBEntry

# ---------------- ROB ----------------

ROB_SIZE = 8
ROB = [ROBEntry() for _ in range(ROB_SIZE)]
rob_head = 0
rob_tail = 0
rob_count = 0
# -------------- Register file --------

reg_file = [0] * 8         # 8 registers, R0 always 0 (we'll just never write it)
reg_status = [None] * 8    # rename table: reg -> ROB idx (or None)

# -------------- PC & control ---------

PC = 0
cycle = 0
simulation_done = False

# -------------- Branch prediction stats --------------

branch_count = 0
mispredict_count = 0

# -------------- Instruction queue ----

instruction_queue = []     # filled by main.py


# --------- Global metrics ---------
instructions_issued    = 0
instructions_committed = 0

branch_count      = 0
mispredict_count  = 0
# Timeline records for report table (one dict per dynamic instruction)
timeline_records = []

# -------------- Memory --------------

MEM_SIZE = 1024
memory = [0] * MEM_SIZE

def mem_load(addr: int) -> int:
    addr = addr % MEM_SIZE
    return memory[addr]

def mem_store(addr: int, value: int):
    addr = addr % MEM_SIZE
    memory[addr] = value & 0xFFFF
class RSEntry:
    def __init__(self):
        self.busy = False
        self.op = None
        self.Vj = None
        self.Vk = None
        self.Qj = None
        self.Qk = None
        self.A = None          # offset / address / immediate helper
        self.rob_idx = None
        self.remaining_cycles = 0
        self.executing = False


def make_rs(count: int):
    return [RSEntry() for _ in range(count)]


# ----------------- Reservation Stations (per spec) -----------------
# ADD/SUB         : 4
# NAND            : 2
# MUL             : 1
# LOAD            : 2
# STORE           : 1
# BEQ             : 2
# CALL / RET      : 1

RS_ADD_SUB   = make_rs(4)
RS_NAND      = make_rs(2)
RS_MUL       = make_rs(1)
RS_LOAD      = make_rs(2)
RS_STORE     = make_rs(1)
RS_BEQ       = make_rs(2)
RS_CALLRET   = make_rs(1)


# Execution latencies (in cycles) as per project description
def exec_latency(op: str) -> int:
    op = op.upper()

    # ADD / SUB unit
    if op in ("ADD", "SUB"):
        return 2          # 2 cycles

    # NAND unit
    if op == "NAND":
        return 1          # 1 cycle

    # MUL unit
    if op == "MUL":
        return 12         # 12 cycles

    # LOAD / STORE units
    if op == "LOAD":
        # 2 cycles address + 4 cycles memory read
        return 2 + 4      # 6 cycles total
    if op == "STORE":
        # 2 cycles address + 4 cycles memory write
        return 2 + 4      # 6 cycles total

    # BEQ unit
    if op == "BEQ":
        return 1          # 1 cycle (compute target + compare)

    # CALL / RET unit
    if op in ("CALL", "RET"):
        return 2          # 2 cycles as you requested (compute return addr + target)

    # Default fallback
    return 1

