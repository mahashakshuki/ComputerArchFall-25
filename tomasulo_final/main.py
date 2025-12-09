# main.py (updated)
from instruction import Instruction
import state
from engine import run_simulation
from cdb import cdb_broadcast
from parser import assemble
from memory import parse_mem_init_file, Memory
from metrics import print_all_metrics

print("MAIN sees state ROB:", id(state.ROB))

# ---------- Config ----------
PROGRAM_FILE = "samples/program1.asm"    # default - you can change or pass args
MEM_INIT_FILE = "samples/program1.mem"    # optional
START_ADDR = 0

# ---------- Load program ----------
with open(PROGRAM_FILE, 'r') as f:
    lines = f.readlines()

instrs = assemble(lines, start_address=START_ADDR)
state.instruction_queue.extend(instrs)

# ---------- Load memory (if present) ----------
try:
    pairs = parse_mem_init_file(MEM_INIT_FILE)
    state.memory.bulk_init(pairs)
    print(f"Initialized memory with {len(pairs)} entries from {MEM_INIT_FILE}")
except FileNotFoundError:
    print("No memory init file found or specified.")

# Run simulation
run_simulation()

# Print final register file & metrics
print("\nFinal register file:", state.reg_file)
print_all_metrics()
