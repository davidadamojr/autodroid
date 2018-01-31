
import random
from appiumatic.hashing import

def probabilistic(db_connection, test_case, probability=None, event_count=None, test_case_length=None):
    assert probability is not None

    if random.random() < probability and testcase not in test_suite


def length(db_connection, test_case, probability=None, event_count=None, test_case_length=None):
    assert event_count is not None and test_case_length is not None

    if event_count == test_case_length:
        return True

    return False
