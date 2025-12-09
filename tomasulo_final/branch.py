import state
from flush import flush_pipeline

def handle_branch(rs):

    A = rs.vj
    B = rs.vk

    taken = (A == B)

    predicted_taken = False        # Always not taken

    if taken != predicted_taken:
        # Misprediction
        correct_target = rs.PC + 1 + rs.offset
        flush_pipeline(correct_target)
        return

    # Correct prediction
    # No flush needed
