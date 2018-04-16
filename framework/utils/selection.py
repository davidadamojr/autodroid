import random
import logging
from appiumatic.hashing import generate_event_hash
from framework import database

logger = logging.getLogger(__name__)


def get_min_frequency_events(db_connection, events, test_suite_id=None):
    hash_to_events_map = {generate_event_hash(event): event for event in events}
    event_hashes = hash_to_events_map.keys()
    event_frequencies = database.get_event_frequencies(db_connection, event_hashes, test_suite_id)

    min_frequency = float("inf")
    min_frequency_events = []
    for event_hash in event_frequencies:
        event = hash_to_events_map[event_hash]
        event_frequency = event_frequencies[event_hash]
        if event_frequency < min_frequency:
            min_frequency_events = [event]
            min_frequency = event_frequencies[event_hash]
        elif event_frequency == min_frequency:
            min_frequency_events.append(event)

    return min_frequency_events


def get_frequency_weights(event_frequencies):
    total_frequency = sum(event_frequencies.values())
    event_weights = {}
    for event_hash, event_frequency in event_frequencies.items():
        event_weights[event_hash] = float(total_frequency) / event_frequency

    return event_weights


def get_uniform_weights(event_hashes):
    return {event_hash: 1 for event_hash in event_hashes}


def make_weighted_selection(hash_to_events_map, event_weights, goal_weight):
    random.seed(a=42)

    sum_of_weights = 0.0
    for event_hash, weight in event_weights.items():
        event = hash_to_events_map[event_hash]
        sum_of_weights += weight
        if sum_of_weights >= goal_weight:
            logger.debug("Selected event with weight {}.".format(weight))
            return event

    logger.error("Did not return proper weighted event. An error occurred.")
    return hash_to_events_map[event_hash]

