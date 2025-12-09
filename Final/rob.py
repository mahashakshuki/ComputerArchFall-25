class ROBEntry:
    def __init__(self):
        self.busy = False
        self.op = None            # opcode
        self.dest = None          # destination register (for LOAD/ALU)
        self.value = None         # result value
        self.ready = False        # result or store info ready?
        self.PC = None            # instruction PC (for debugging)

        # ---- STORE-specific ----
        self.store_addr = None
        self.store_value = None

        # ---- Branch info (optional but useful) ----
        self.is_branch = False
        self.predicted_taken = False
        self.actual_taken = False
        self.correct_target = None

        # ---- Full timing record (required for the timeline table) ----
        self.issue_cycle = None
        self.exec_start_cycle = None
        self.exec_end_cycle = None
        self.write_cycle = None
        self.commit_cycle = None

        # NEW: pointer to the timeline row in state.timeline_records
        self.timeline = None
