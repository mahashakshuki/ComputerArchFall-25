Tomasulo Algorithm Simulator
CSCE 3301 – Computer Architecture (Fall 2025)

Team members:
- Hanna Mostafa 9000222857
- Maha Shakshuki 900225906
- Joudy Elgayar 900222142

- Language: Python 3
- Files included:
  - source/: all .py source files (main.py, state.py, instruction.py, issue.py, execute.py, writeback.py, cdb.py, commit.py, engine.py, flush.py)
  - test/: assembly test programs (program1.asm, program2.asm, program3.asm)
  - report.docx (report)
  - README.txt (this file)
  - journals/: individual member journals
- What works:
  - Full simulation pipeline: Issue, Execute, Write (CDB), Commit.
  - Support for: ADD, SUB, NAND, MUL, LOAD, STORE, BEQ, CALL, RET.
  - ROB size 8, RS counts and latencies as per project spec.
  - Timeline records and final summary (cycles, IPC, branch mispred %).
- Known issues / limitations:
  - Non-speculative issue policy used (we intentionally stall issue on unresolved control).
  - Single CDB broadcast per cycle (as implemented); this is part of the model but could be extended to model multi-broadcast as a bonus.
  - Memory is a simple array with modulo addressing (MEM_SIZE default 1024). For full spec (128KB), change MEM_SIZE constant in state.py.
- How to run:
  1. Ensure Python 3 is installed.
  2. Place the provided source files in the same folder.
  3. Edit `test/programX.asm` as needed. `main.py` loads `program1.asm` by default.
  4. Run: `python3 main.py`
  5. Inspect output printed to the terminal and the `state.timeline_records`.
- Notes on AI usage:
  - We used ChatGPT (assistant) for debugging hints & troubleshooting small issues only. All code is handwritten and tested by us (see report for example prompts and usage summary).

