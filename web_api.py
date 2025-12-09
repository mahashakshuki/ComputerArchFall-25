from femTomas.processor import Processor
from femTomas.instruction import InstructionParser

def run_simulation(program_text: str, memory_dict: dict):
    cpu = Processor()

    # Load memory
    for addr, val in memory_dict.items():
        cpu.memory.write_word(addr, val)

    # Parse program
    instructions = InstructionParser.parse_program(program_text)

    # Run simulation
    cpu.run(instructions)

    # Build JSON-like result dictionary
    return {
        "cycles": cpu.cycles,
        "ipc": cpu.instructions_completed / cpu.cycles,
        "branch_misprediction": cpu.mispredictions,
        "timeline": cpu.timeline
    }
