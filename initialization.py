import strategies.event_selection as event_selection
import strategies.termination as termination
import strategies.completion as completion
import strategies.setup as test_setup
import strategies.teardown as test_teardown
from appiumatic.exceptions import InvalidParameter
from functools import partial

__author__ = "David Adamo Jr."


def event_selection_strategy(strategy, combination_strength):
    strategy = strategy.lower()
    if strategy == "random":
        return partial(event_selection.random, combination_strength=combination_strength)
    elif strategy == "min_frequency":
        return partial(event_selection.min_frequency, combination_strength=combination_strength)
    elif strategy == "frequency_weighted":
        return partial(event_selection.frequency_weighted, combination_strength=combination_strength)
    elif strategy == "combinatorial":
        return partial(event_selection.combinatorial, combination_strength=combination_strength)

    raise InvalidParameter("Invalid specification '{}' for event selection strategy.".format(strategy))


def teardown(user_specification):
    user_specification = user_specification.lower()
    if user_specification == "standard":
        return test_teardown.standard

    raise InvalidParameter("Invalid specification '{}' for test case tear down.")


def setup(user_specification):
    user_specification = user_specification.lower()
    if user_specification == "standard":
        return test_setup.standard

    raise InvalidParameter("Invalid specification '{}' for test case setup.")

def completion_criterion(criterion, event_count, time_budget, test_suite_length):
    criterion = criterion.lower()
    if criterion == "time":
        return partial(completion.time_budget_exceeded, time_budget=time_budget)
    elif criterion == "length":
        return partial(completion.number_of_test_cases_reached, test_case_budget=test_suite_length)
    elif criterion == "events":
        return partial(completion.number_of_events_reached, event_budget=event_count)

    raise InvalidParameter("Invalid specification '{}' for completion criterion.".format(criterion))


def termination_criterion(criterion, probability, length):
    criterion = criterion.lower()
    if criterion == "probabilistic":
        return partial(termination.probabilistic, probability=probability, test_case_length=length)
    elif criterion == "length":
        return partial(termination.length, probability=probability, test_case_length=length)

    raise InvalidParameter("Invalid specification '{}' for termination criterion.".format(criterion))