import random
import logging
from framework.utils import selection as selection_utils

logger = logging.getLogger(__name__)


def uniform_random(events, database=None, suite_id=None):
    assert events is not None

    selected_event = random.choice(events)

    return selected_event


def min_frequency_random(events, database, suite_id):
    assert events is not None and suite_id is not None and database is not None

    logger.info("Making min_frequency_random selection from {} available events.".format(len(events)))

    hash_to_events_map = selection_utils.create_hash_to_events_map(events)
    event_hashes = hash_to_events_map.keys()
    event_frequencies = database.get_event_frequencies(event_hashes, suite_id)
    min_frequency_event_hashes = selection_utils.get_min_frequency_event_hashes(event_frequencies)
    selected_event_hash = random.choice(min_frequency_event_hashes)

    return hash_to_events_map[selected_event_hash]


def min_frequency_deterministic(events, database, suite_id):
    assert events is not None and suite_id is not None and database is not None

    logger.info("Making min_frequency_deterministic selection from {}")

    hash_to_events_map = selection_utils.create_hash_to_events_map(events)
    event_hashes = hash_to_events_map.keys()
    event_frequencies = database.get_event_frequencies(event_hashes, suite_id)
    min_frequency_event_hashes = selection_utils.get_min_frequency_event_hashes(event_frequencies)

    selected_event_hash = min_frequency_event_hashes[0]

    return hash_to_events_map[selected_event_hash]


def frequency_weighted(events, database, suite_id):
    assert events is not None and suite_id is not None and database is not None

    logger.info("Making frequency_weighted selection from {} available events.".format(len(events)))

    hash_to_events_map = selection_utils.create_hash_to_events_map(events)
    event_hashes = hash_to_events_map.keys()
    event_frequencies = database.get_event_frequencies(event_hashes, suite_id)

    event_weights = selection_utils.get_frequency_weights(event_frequencies)
    total_weight = sum(event_weights.values())
    goal_weight = random.uniform(0.0, 1.0) * total_weight
    selected_event = selection_utils.make_weighted_selection(hash_to_events_map, event_weights, goal_weight)

    return selected_event







