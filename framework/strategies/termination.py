import logging
import random
from  framework.database import test_case_exists


def probabilistic(db_connection, probability=None, test_case_hash=None, test_suite_id=None, event_count=None,):
    assert probability is not None and test_suite_id is not None and test_case_hash is not None

    logger = logging.getLogger(__name__)
    logger.info("Checking probabilistic test termination criterion...")

    if random.random() < probability and test_case_exists(db_connection, test_suite_id, test_case_hash):
        return True

    return False


def length(db_connection, test_case_length=None, test_case_hash=None, test_suite_id=None, event_count=None):
    assert event_count is not None and test_case_length is not None and test_suite_id is not None and \
        test_suite_id is not None

    logger = logging.getLogger(__name__)
    logger.info("Checking length test termination criterion...")

    if event_count >= test_case_length and not test_case_exists(db_connection, test_suite_id, test_case_hash):
        return True

    return False
