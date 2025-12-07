# rob.py

class ROBEntry:
    def __init__(self):
        self.busy = False
        self.op = None
        self.dest = None
        self.value = None
        self.ready = False
        self.PC = None
        self.mispredict = False
        self.correct_target = None
