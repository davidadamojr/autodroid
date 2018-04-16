

def time_budget_exceeded(time_budget=None, test_duration=None, test_case_count=None):
    assert time_budget is not None and test_duration is not None

    if test_duration > time_budget:
        return True

    return False


def number_of_test_cases_reached(test_case_budget=None, test_case_count=None, test_duration=None):
    assert test_case_count is not None and test_case_budget is not None

    if test_case_count == test_case_budget:
        return True

    return False
