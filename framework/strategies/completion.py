

def time_budget_exceeded(completion_value, suite_duration=None, sequence_count=None):
    assert completion_value is not None and suite_duration is not None

    if suite_duration >= completion_value:
        return True

    return False


def number_of_sequences_reached(completion_value, suite_duration=None, sequence_count=None):
    assert completion_value is not None and sequence_count is not None

    if sequence_count == completion_value:
        return True

    return False
