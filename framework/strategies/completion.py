

def time_budget_exceeded(time_budget=None, suite_duration=None, sequence_count=None):
    assert time_budget is not None and suite_duration is not None

    if suite_duration > time_budget:
        return True

    return False


def number_of_sequences_reached(sequence_budget=None, sequence_count=None, suite_duration=None):
    assert sequence_count is not None and sequence_budget is not None

    if sequence_count == sequence_budget:
        return True

    return False
