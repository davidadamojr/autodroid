from functools import partial
from framework.strategies import selection, completion, setup, teardown, termination
from appiumatic.exceptions import InvalidParameter


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
    elif strategy == "gaussian_random":
        return selection.gaussian_random

    raise InvalidParameter("Invalid specification '{}' for event selection strategy.".format(strategy))


def tear_down_strategy(strategy):
    strategy = strategy.lower()
    if strategy == "standard":
        return teardown.standard

    raise InvalidParameter("Invalid specification '{}' for test case tear down.")


def setup_strategy(strategy):
    strategy = strategy.lower()
    if strategy == "standard":
        return setup.standard

    raise InvalidParameter("Invalid specification '{}' for test case setup.")


def completion_criterion(criterion, time_budget, suite_length):
    criterion = criterion.lower()
    if criterion == "time":
        completion_func = partial(completion.time_budget_exceeded, time_budget=time_budget)
        return completion_func
    elif criterion == "length":
        return partial(completion.number_of_sequences_reached, test_case_budget=suite_length)

    raise InvalidParameter("Invalid specification '{}' for completion criterion.".format(criterion))


def termination_criterion(criterion, probability, length):
    criterion = criterion.lower()
    if criterion == "probabilistic":
        return partial(termination.probabilistic, probability=probability)
    elif criterion == "length":
        return partial(termination.length, test_case_length=length)

    raise InvalidParameter("Invalid specification '{}' for termination criterion.".format(criterion))