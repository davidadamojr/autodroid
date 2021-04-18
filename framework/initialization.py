from functools import partial
from framework.strategies import selection, completion, setup, teardown, termination
from appiumatic.exceptions import InvalidParameter
import logging
logger = logging.getLogger(__name__)

def event_selection_strategy(strategy):
    strategy = strategy.lower()
    if strategy == "random":
        return selection.uniform_random
    elif strategy == "min_frequency_random":
        return selection.min_frequency_random
    elif strategy == "min_frequency_deterministic":
        return selection.min_frequency_deterministic
    elif strategy == "frequency_weighted":
        return selection.frequency_weighted
    elif strategy == "pairs_interleaved":
        return selection.pairs_interleaved

    raise InvalidParameter("Invalid specification '{}' for event selection strategy.".format(strategy))


def tear_down_strategy(strategy, adb_path, device_id):
    strategy = strategy.lower()
    if strategy == "standard":
        return partial(teardown.standard, adb_path=adb_path, device_id=device_id)

    raise InvalidParameter("Invalid specification '{}' for test case tear down.")


def setup_strategy(strategy, apk_path, adb_path, device_id, context_sequence):
    strategy = strategy.lower()
    if strategy == "standard":
        return partial(setup.standard, apk_path=apk_path, adb_path=adb_path, device_id=device_id)
    elif strategy == "random_start":
        return partial(setup.random_start, apk_path=apk_path, adb_path=adb_path, device_id=device_id, context_sequence=context_sequence)
    elif strategy == "iterative_start":
        return partial(setup.iterative_start, apk_path=apk_path, adb_path=adb_path, device_id=device_id, context_sequence=context_sequence)

    raise InvalidParameter("Invalid specification '{}' for test case setup.")


def completion_criterion(criterion, time_budget, suite_length):
    criterion = criterion.lower()
    if criterion == "time":
        completion_func = partial(completion.time_budget_exceeded, completion_value=time_budget)
        return completion_func
    elif criterion == "length":
        return partial(completion.number_of_sequences_reached, completion_value=suite_length)

    raise InvalidParameter("Invalid specification '{}' for completion criterion.".format(criterion))


def termination_criterion(criterion, probability, length):
    criterion = criterion.lower()
    if criterion == "probabilistic":
        return partial(termination.probabilistic, terminal_value=probability)
    elif criterion == "length":
        return partial(termination.length, terminal_value=length)

    raise InvalidParameter("Invalid specification '{}' for termination criterion.".format(criterion))
