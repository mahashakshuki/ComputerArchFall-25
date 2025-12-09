# instruction.py

class Instruction:
    """
    Simple decoded instruction.
    For now we focus on ALU ops: ADD, SUB, NAND, MUL.
    Later we'll extend this to LOAD/STORE/BEQ/CALL/RET with immediates.
    """
    def __init__(self, op, dest=None, src1=None, src2=None, PC=None, imm=None, raw=None):
        self.op = op          # 'ADD','SUB','NAND','MUL','LOAD','STORE','BEQ','CALL','RET'
        self.dest = dest      # destination register index (0..7) if any
        self.src1 = src1      # first source register index
        self.src2 = src2      # second source register index
        self.PC = PC          # program counter / index
        self.imm = imm        # immediate / offset / branch target (for later)
        self.raw = raw        # original line (for debugging)
import re

REG_NAMES = {f"R{i}": i for i in range(8)}
REG_NAMES.update({f"r{i}": i for i in range(8)})

def _parse_reg(token: str) -> int:
    token = token.strip()
    if token not in REG_NAMES:
        raise ValueError(f"Unknown register '{token}'")
    return REG_NAMES[token]

def _strip_comment(line: str) -> str:
    # support ; or # or // comments
    for sep in (";", "#", "//"):
        if sep in line:
            line = line.split(sep, 1)[0]
    return line.strip()
def _first_pass(lines):
    """
    Returns:
      instructions_raw: list of (pc, line_text)
      labels: dict label -> pc
    """
    instructions_raw = []
    labels = {}
    pc = 0

    for line in lines:
        line = _strip_comment(line)
        if not line:
            continue

        # label?
        if ":" in line:
            label, rest = line.split(":", 1)
            label = label.strip()
            if label:
                labels[label] = pc
            line = rest.strip()
            if not line:
                continue  # label-only line

        # genuine instruction line
        instructions_raw.append((pc, line))
        pc += 1

    return instructions_raw, labels
def _parse_alu(op, pc, args):
    # EXPECT: dest, src1, src2
    dest = _parse_reg(args[0])
    src1 = _parse_reg(args[1])
    src2 = _parse_reg(args[2])
    return Instruction(op, dest=dest, src1=src1, src2=src2, imm=None, PC=pc)

def _parse_load(pc, args):
    # LOAD rA, offset(rB)
    # example: LOAD R1, 4(R2)
    dest = _parse_reg(args[0])
    addr = args[1].strip()
    m = re.match(r"(-?\d+)\((R\d|r\d)\)", addr)
    if not m:
        raise ValueError(f"Bad LOAD address syntax: {addr}")
    offset = int(m.group(1))
    base = _parse_reg(m.group(2))
    return Instruction("LOAD", dest=dest, src1=base, src2=None, imm=offset, PC=pc)

def _parse_store(pc, args):
    # STORE rA, offset(rB)
    src = _parse_reg(args[0])        # value register
    addr = args[1].strip()
    m = re.match(r"(-?\d+)\((R\d|r\d)\)", addr)
    if not m:
        raise ValueError(f"Bad STORE address syntax: {addr}")
    offset = int(m.group(1))
    base = _parse_reg(m.group(2))
    return Instruction("STORE", dest=None, src1=base, src2=src, imm=offset, PC=pc)

def _parse_beq(pc, args, labels):
    # BEQ rA, rB, offset_or_label
    rA = _parse_reg(args[0])
    rB = _parse_reg(args[1])
    last = args[2].strip()

    # label?
    if last in labels:
        target_pc = labels[last]
        offset = target_pc - (pc + 1)
    else:
        offset = int(last)

    return Instruction("BEQ", dest=None, src1=rA, src2=rB, imm=offset, PC=pc)

def _parse_call(pc, args, labels):
    # CALL label
    label = args[0].strip()
    if label not in labels:
        raise ValueError(f"Unknown label '{label}' in CALL")
    target_pc = labels[label]
    # We'll store the absolute target in imm; execute stage will set PC=imm
    return Instruction("CALL", dest=None, src1=None, src2=None, imm=target_pc, PC=pc)

def _parse_ret(pc):
    # RET uses R1 in hardware, no operands
    return Instruction("RET", dest=None, src1=1, src2=None, imm=None, PC=pc)
def parse_program_from_lines(lines):
    """
    Parse a list of assembly lines into a list of Instruction objects.
    Supported syntax:
      - ADD  R1, R2, R3
      - SUB  R1, R2, R3
      - NAND R1, R2, R3
      - MUL  R1, R2, R3
      - LOAD  R1, imm(R2)
      - STORE R1, imm(R2)
      - BEQ   R1, R2, offset_or_label
      - CALL  label
      - RET
    Labels: 'LOOP:' at start of a line.
    """
    raw, labels = _first_pass(lines)
    program = []

    for pc, text in raw:
        parts = text.replace(",", " ").split()
        if not parts:
            continue
        op = parts[0].upper()
        args = parts[1:]

        if op in ("ADD", "SUB", "NAND", "MUL"):
            inst = _parse_alu(op, pc, args)
        elif op == "LOAD":
            inst = _parse_load(pc, args)
        elif op == "STORE":
            inst = _parse_store(pc, args)
        elif op == "BEQ":
            inst = _parse_beq(pc, args, labels)
        elif op == "CALL":
            inst = _parse_call(pc, args, labels)
        elif op == "RET":
            inst = _parse_ret(pc)
        else:
            raise ValueError(f"Unknown opcode '{op}' in line: {text}")

        program.append(inst)

    return program


def parse_program_file(filename: str):
    with open(filename, "r") as f:
        lines = f.readlines()
    return parse_program_from_lines(lines)
