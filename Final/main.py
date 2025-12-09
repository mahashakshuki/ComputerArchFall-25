# main.py
from instruction import Instruction
from instruction import parse_program_file
import state
from engine import run_simulation

# reset state
state.reg_file[:] = [0] * 8
state.reg_status[:] = [None] * 8
state.memory[:] = [0] * state.MEM_SIZE
state.PC = 0
state.cycle = 0
state.simulation_done = False
state.instruction_queue.clear()
state.rob_head = 0
state.rob_tail = 0
state.rob_count = 0
state.branch_count = 0
state.mispredict_count = 0

# Registers
state.reg_file[0] = 0   # always 0
state.reg_file[1] = 0   # will hold return address
state.reg_file[2] = 0
state.reg_file[3] = 0
state.reg_file[4] = 0
state.reg_file[5] = 0
state.reg_file[6] = 0
state.reg_file[7] = 0

# Memory
state.memory[0] = 10
state.memory[1] = 5


# r1 initially = garbage, we will overwrite it
#state.instruction_queue.append(Instruction("CALL", dest=None, src1=None, src2=None, imm=4, PC=0))
#state.instruction_queue.append(Instruction("ADD", dest=2, src1=0, src2=0, imm=None, PC=1))  # should be skipped
#state.instruction_queue.append(Instruction("RET", dest=None, src1=1, src2=None, imm=None, PC=2))
#state.instruction_queue.append(Instruction("ADD", dest=3, src1=2, src2=2, imm=None, PC=3))
#state.instruction_queue.append(Instruction("ADD", dest=4, src1=0, src2=0, imm=None, PC=4))



# reset state.* arrays as you already do...

# Example: load program.asm in the same folder
state.instruction_queue = parse_program_file("program1.asm")

run_simulation()
# then print stats + timeline as before

print("\nFinal registers:", state.reg_file)
print(f"\nSimulation finished in {state.cycle} cycles")
print(f"Instructions issued    : {state.instructions_issued}")
print(f"Instructions committed : {state.instructions_committed}")
print(f"Branches               : {state.branch_count}")
print(f"Mispredictions         : {state.mispredict_count}")

if state.cycle > 0:
    ipc = state.instructions_committed / state.cycle
    print(f"IPC                    : {ipc:.3f}")
    if state.branch_count > 0:
        misp_pct = 100.0 * state.mispredict_count / state.branch_count
        print(f"Branch misprediction % : {misp_pct:.2f}%")
 
def _fmt(x):
    return "-" if x is None else str(x)

print("\n=== Instruction Timeline (dynamic) ===")
print("Seq  PC  OP      Issue  ExecS  ExecE  Write  Commit")
for rec in state.timeline_records:
    print(f"{rec['seq']:3}  {rec['pc']:3}  {rec['op']:<6} "
          f"{_fmt(rec['issue']):>5}  "
          f"{_fmt(rec['exec_start']):>5}  "
          f"{_fmt(rec['exec_end']):>5}  "
          f"{_fmt(rec['write']):>5}  "
          f"{_fmt(rec['commit']):>6}")
