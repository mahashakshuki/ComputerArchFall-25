# main.py

from instruction import Instruction
import state
from engine import run_simulation
from cdb import cdb_broadcast

print("MAIN sees state ROB:", id(state.ROB))

# ----------------------------
# Create a tiny test program
# ----------------------------

state.instruction_queue.append(Instruction("ADD", dest=1, src1=2, src2=3, PC=0))
state.instruction_queue.append(Instruction("ADD", dest=2, src1=1, src2=3, PC=1))



# ----------------------------
# Run simulation
# ----------------------------

run_simulation()

print("\nFinal register file:", state.reg_file)
