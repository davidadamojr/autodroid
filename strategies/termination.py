__author__ = "David Adamo Jr."


def probabilistic(db_connection, probability=None, event_count=None, test_case_length=None):
    assert probability is not None


def length(db_connection, probability=None, event_count=None, test_case_length=None):
    assert event_count is not None and test_case_length is not None

    if event_count == test_case_length:
        return True

    return False
