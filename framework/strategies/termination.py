import logging
import random


def probabilistic(database, probability=None, sequence_hash=None, suite_id=None, event_count=None, ):
    assert probability is not None and suite_id is not None and sequence_hash is not None

    logger = logging.getLogger(__name__)
    logger.info("Checking probabilistic test termination criterion...")

    if random.random() < probability and database.sequence_exists(suite_id, sequence_hash):
        return True

    return False


def length(database, sequence_length=None, sequence_hash=None, suite_id=None, event_count=None):
    assert event_count is not None and sequence_length is not None and suite_id is not None and \
           suite_id is not None

    logger = logging.getLogger(__name__)
    logger.info("Checking length test termination criterion...")

    if event_count >= sequence_length and not database.sequence_exists(suite_id, sequence_hash):
        return True

    return False
