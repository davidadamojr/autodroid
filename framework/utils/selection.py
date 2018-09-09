import logging
from appiumatic.hashing import generate_event_hash
from collections import OrderedDict

logger = logging.getLogger(__name__)


def create_hash_to_events_map(events):
    hash_to_events_map = OrderedDict()
    for event in events:
        event_hash = generate_event_hash(event)
        hash_to_events_map[event_hash] = event

    return hash_to_events_map


def get_min_frequency_event_hashes(event_frequencies):
    min_frequency = float("inf")
    min_frequency_event_hashes = []
    for event_hash, event_frequency in event_frequencies.items():
        if event_frequency < min_frequency:
            min_frequency_event_hashes = [event_hash]
            min_frequency = event_frequency
        elif event_frequency == min_frequency:
            min_frequency_event_hashes.append(event_hash)

    return min_frequency_event_hashes


def get_frequency_weights(event_frequencies):
    total_frequency = sum(event_frequencies.values())
    event_weights = OrderedDict()
    for event_hash, event_frequency in event_frequencies.items():
        event_weights[event_hash] = float(total_frequency) / (event_frequency + 1)

    return event_weights


def get_uniform_event_weights(event_hashes):
    return {event_hash: 1 for event_hash in event_hashes}


def make_weighted_selection(hash_to_events_map, event_weights, goal_weight):
    sum_of_weights = 0.0
    event_hash = list(event_weights.keys())[0]
    for event_hash, weight in event_weights.items():
        event = hash_to_events_map[event_hash]
        sum_of_weights += weight
        if sum_of_weights >= goal_weight:
            logger.debug("Selected event with weight {}.".format(weight))
            return event

    logger.error("Did not return proper weighted event. An error occurred.")
    return hash_to_events_map[event_hash]
