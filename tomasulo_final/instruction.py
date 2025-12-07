# instruction.py

class Instruction:
    def __init__(self, op, dest=None, src1=None, src2=None, PC=None):
        self.op = op
        self.dest = dest
        self.src1 = src1
        self.src2 = src2
        self.PC = PC
