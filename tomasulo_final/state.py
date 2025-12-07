# state.py
print("STATE MODULE LOADED FROM:", __file__)

from rob import ROBEntry

ROB_SIZE = 8
ROB = [ROBEntry() for _ in range(ROB_SIZE)]
rob_head = 0
rob_tail = 0
rob_count = 0

reg_file = [0] * 8
reg_status = [None] * 8

PC = 0
cycle = 0
simulation_done = False

instruction_queue = []
