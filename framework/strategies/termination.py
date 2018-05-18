import logging
import random


def probabilistic(database, probability=None, test_case_hash=None, test_suite_id=None, event_count=None,):
    assert probability is not None and test_suite_id is not None and test_case_hash is not None

    logger = logging.getLogger(__name__)
    logger.info("Checking probabilistic test termination criterion...")

    if random.random() < probability and database.test_case_exists(test_suite_id, test_case_hash):
        return True

    return False


def length(database, test_case_length=None, test_case_hash=None, test_suite_id=None, event_count=None):
    assert event_count is not None and test_case_length is not None and test_suite_id is not None and \
        test_suite_id is not None

    logger = logging.getLogger(__name__)
    logger.info("Checking length test termination criterion...")

    if event_count >= test_case_length and not database.test_case_exists(test_suite_id, test_case_hash):
        return True

    return False
