import logging
import random


def probabilistic(database, sequence_hash, suite_id, terminal_value, event_count=None):
    assert terminal_value is not None and suite_id is not None and sequence_hash is not None and \
           database is not None

    logger = logging.getLogger(__name__)
    logger.info("Checking probabilistic test termination criterion...")

    if random.random() <= terminal_value and not database.sequence_exists(suite_id, sequence_hash):
        return True

    return False


def length(database, sequence_hash, suite_id, terminal_value, event_count):
    assert event_count is not None and terminal_value is not None and suite_id is not None and \
           suite_id is not None and database is not None

    logger = logging.getLogger(__name__)
    logger.info("Checking length test termination criterion...")

    if event_count >= terminal_value and not database.sequence_exists(suite_id, sequence_hash):
        return True

    return False
