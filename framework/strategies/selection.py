import random
import logging
from framework.utils import selection
import framework.database as database
from appiumatic.hashing import generate_event_hash


logger = logging.getLogger(__name__)


def uniform_random(db_connection, events, test_suite_id=None):
    assert events is not None
    random.seed(42)

    selected_event = random.choice(events)

    return selected_event


def min_frequency_random(db_connection, events, test_suite_id=None):
    assert events is not None and test_suite_id is not None
    random.seed(42)

    logger.info("Making min_frequency_random selection from {} available events.".format(len(events)))

    min_frequency_events = selection.get_min_frequency_events(db_connection, events, test_suite_id)

    selected_event = random.choice(min_frequency_events)

    return selected_event


def min_frequency_deterministic(db_connection, events, test_suite_id=None):
    assert events is not None and test_suite_id is not None

    logger.info("Making min_frequency_deterministic selection from {}")

    min_frequency_events = selection.get_min_frequency_events(db_connection, events, test_suite_id)

    selected_event = min_frequency_events[0]

    return selected_event


def frequency_weighted(db_connection, events, test_suite_id=None):
    assert events is not None and test_suite_id is not None

    logger.info("Making frequency_weighted selection from {} available events.".format(len(events)))

    hash_to_events_map = {generate_event_hash(event): event for event in events}
    event_hashes = hash_to_events_map.keys()
    event_frequencies = database.get_event_frequencies(db_connection, event_hashes, test_suite_id)

    event_weights = selection.get_frequency_weights(event_frequencies)
    total_weight = sum(event_weights.values())
    goal_weight = random.uniform(0.0, 1.0) * total_weight
    selected_event = selection.make_weighted_selection(hash_to_events_map, event_weights, goal_weight)

    return selected_event


def gaussian_random(db_connection, events, test_suite_id=None):
    assert events is not None and test_suite_id is not None

    logger.info("Making gaussian random selection from {} available events.".format(len(events)))

    hash_to_events_map = {generate_event_hash(event): event for event in events}
    event_hashes = hash_to_events_map.keys()
    event_weights = selection.get_uniform_event_weights(event_hashes)
    total_weight = sum(event_weights.values())
    goal_weight = random.gauss(0.5, 0.1) * total_weight
    selected_event = selection.make_weighted_selection(hash_to_events_map, event_weights, goal_weight)

    return selected_event






