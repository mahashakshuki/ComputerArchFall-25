# Simple word-addressable memory (16-bit words). Addresses are integers (0..65535 for 16-bit)
# Memory initialized to zeros.

MEMORY_SIZE_WORDS = 65536  # 128KB = 65536 words (16-bit)

class Memory:
    def __init__(self, size=MEMORY_SIZE_WORDS):
        self.size = size
        self.mem = [0] * size

    def load_word(self, addr):
        if addr < 0 or addr >= self.size:
            raise IndexError("Memory access out of range")
        return self.mem[addr] & 0xFFFF

    def store_word(self, addr, val):
        if addr < 0 or addr >= self.size:
            raise IndexError("Memory access out of range")
        self.mem[addr] = val & 0xFFFF

    def bulk_init(self, pairs):
        # pairs: iterable of (addr, value)
        for a,v in pairs:
            self.store_word(a, v)

def parse_mem_init_file(path):
    """
    Expected format: one entry per line: ADDRESS VALUE
    ADDRESS and VALUE can be decimal or 0x... hex. Comments with # supported.
    """
    pairs = []
    with open(path, 'r') as f:
        for raw in f:
            line = raw.split('#',1)[0].strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) < 2:
                continue
            addr = int(parts[0], 0)
            val = int(parts[1], 0) & 0xFFFF
            pairs.append((addr, val))
    return pairs
