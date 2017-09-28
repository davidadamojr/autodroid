__author__ = "David Adamo Jr."


def time_budget_exceeded(time_budget=None, test_duration=None, test_case_budget=None, test_case_count=None,
                         event_budget=None, event_count=None):
    assert time_budget is not None and test_duration is not None

    if test_duration > time_budget:
        return True

    return False


def number_of_test_cases_reached(time_budget=None, test_duration=None, test_case_budget=None, test_case_count=None,
                                 event_budget=None, event_count=None):
    assert test_case_count is not None and test_case_budget is not None

    if test_case_count == test_case_budget:
        return True

    return False


def number_of_events_reached(time_budget=None, test_duration=None, test_case_budget=None, test_case_count=None,
                             event_budget=None, event_count=None):
    assert event_count is not None and event_budget is not None

    if event_count == event_budget:
        return True

    return False