# Simple assembler parser
# - supports labels, immediate offsets, and simple syntax:
#   ADD rA, rB, rC
#   LOAD rA, offset(rB)
#   STORE rA, offset(rB)
#   BEQ rA, rB, label_or_offset
#   CALL label
#   RET

import re
from instruction import Instruction

REGISTER_RE = re.compile(r'R?([0-7])$')

def reg_token(tok):
    m = REGISTER_RE.match(tok.strip().upper())
    if not m:
        raise ValueError(f"Invalid register token: {tok}")
    return int(m.group(1))

def parse_operand_token(tok):
    tok = tok.strip()
    # register
    if tok.upper().startswith('R') or tok.isdigit():
        return reg_token(tok)
    # immediate number
    if tok.startswith('-') or tok.isdigit():
        return int(tok)
    raise ValueError(f"Unknown operand {tok}")

def parse_line(line):
    # remove comments
    line = line.split('#',1)[0].strip()
    if not line:
        return None
    return line

def first_pass(lines):
    """Return label->PC mapping and list of cleaned lines."""
    pc = 0
    labels = {}
    cleaned = []
    for raw in lines:
        line = parse_line(raw)
        if line is None:
            continue
        # label?
        if ':' in line:
            parts = line.split(':')
            label = parts[0].strip()
            labels[label] = pc
            rest = ':'.join(parts[1:]).strip()
            if rest:
                cleaned.append(rest)
                pc += 1
        else:
            cleaned.append(line)
            pc += 1
    return labels, cleaned

def assemble(lines, start_address=0):
    """Return a list of Instruction objects with PC set to start_address + idx."""
    labels, cleaned = first_pass(lines)
    instrs = []
    PC = start_address
    for ln in cleaned:
        tokens = re.split(r'[,\s()\t]+', ln.strip())
        # remove empty
        tokens = [t for t in tokens if t != '']
        op = tokens[0].upper()
        if op == 'ADD' or op == 'SUB' or op == 'NAND' or op == 'MUL':
            # format: OP rA, rB, rC
            dest = reg_token(tokens[1])
            src1 = reg_token(tokens[2])
            src2 = reg_token(tokens[3])
            instrs.append(Instruction(op, dest=dest, src1=src1, src2=src2, PC=PC))
        elif op == 'LOAD':
            # LOAD rA, offset(rB)
            dest = reg_token(tokens[1])
            offset = int(tokens[2])
            base = reg_token(tokens[3])
            # We'll encode offset in src2 for the simulator; parser stores offset in src2
            instrs.append(Instruction('LOAD', dest=dest, src1=base, src2=offset, PC=PC))
        elif op == 'STORE':
            # STORE rA, offset(rB)
            src = reg_token(tokens[1])
            offset = int(tokens[2])
            base = reg_token(tokens[3])
            instrs.append(Instruction('STORE', dest=None, src1=src, src2=(base, offset), PC=PC))
        elif op == 'BEQ':
            rA = reg_token(tokens[1])
            rB = reg_token(tokens[2])
            label_or_imm = tokens[3]
            # resolve label or immediate
            if label_or_imm in labels:
                offset = labels[label_or_imm] - PC - 1
            else:
                try:
                    offset = int(label_or_imm)
                except:
                    raise ValueError(f"Unknown label/imm {label_or_imm}")
            instrs.append(Instruction('BEQ', dest=None, src1=rA, src2=(rB, offset), PC=PC))
        elif op == 'CALL':
            target = tokens[1]
            if target in labels:
                offset = labels[target] - PC - 1
            else:
                offset = int(target)
            instrs.append(Instruction('CALL', dest=None, src1=None, src2=offset, PC=PC))
        elif op == 'RET':
            instrs.append(Instruction('RET', dest=None, src1=None, src2=None, PC=PC))
        else:
            raise ValueError(f"Unknown op {op} on line: {ln}")
        PC += 1
    return instrs
