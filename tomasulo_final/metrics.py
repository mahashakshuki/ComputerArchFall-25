import state
from tabulate import tabulate  # optional; if not available we'll format manually

def per_instruction_table():
    headers = ['PC', 'OP', 'ISSUE', 'EXE_START', 'EXE_END', 'WRITE', 'COMMIT']
    rows = []
    for pc, instr in enumerate(state.instruction_queue):
        issue = state.issue_cycle.get(pc, '-')
        start = state.exec_start.get(pc, '-')
        end = state.exec_end.get(pc, '-')
        write = state.write_cycle.get(pc, '-')
        commit = state.commit_cycle.get(pc, '-')
        rows.append([pc, instr.op, issue, start, end, write, commit])
    try:
        print(tabulate(rows, headers=headers, tablefmt='grid'))
    except Exception:
        # fallback print
        print(headers)
        for r in rows:
            print(r)

def global_metrics():
    total_cycles = state.cycle
    instrs_completed = sum(1 for i in state.commit_cycle if i) if hasattr(state, 'commit_cycle') else len(state.instruction_queue)
    # Better: count commits from commit_cycle dict
    committed = len([k for k,v in state.commit_cycle.items() if v is not None])
    ipc = committed / total_cycles if total_cycles > 0 else 0.0
    branch_count = getattr(state, 'branch_count', 0)
    mispred = getattr(state, 'branch_mispred', 0)
    mispred_rate = (mispred / branch_count * 100.0) if branch_count > 0 else 0.0
    print("\n=== GLOBAL METRICS ===")
    print(f"Total cycles: {total_cycles}")
    print(f"Instructions committed: {committed}")
    print(f"IPC: {ipc:.4f}")
    print(f"Branches encountered: {branch_count}")
    print(f"Branch mispredictions: {mispred} ({mispred_rate:.2f}%)")

def print_all_metrics():
    print("\nINSTRUCTION TIMELINE:")
    per_instruction_table()
    global_metrics()
