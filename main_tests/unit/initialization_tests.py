import unittest
import types
from framework.initialization import event_selection_strategy, tear_down_strategy, setup_strategy, completion_criterion, \
    termination_criterion
from unittest.mock import patch
from framework.strategies import completion, termination
from framework.strategies import setup as setup_strategies
from framework.strategies import teardown as teardown_strategies


class InitializationTests(unittest.TestCase):
    def test_can_initiate_random_event_selection_strategy(self):
        strategy = event_selection_strategy("random")
        self.assertIsInstance(strategy, types.FunctionType)
        self.assertEqual(strategy.__name__, "uniform_random")

    def test_can_initiate_min_frequency_random_strategy(self):
        strategy = event_selection_strategy("min_frequency_random")
        self.assertIsInstance(strategy, types.FunctionType)
        self.assertEqual(strategy.__name__, "min_frequency_random")

    def test_can_initiate_min_frequency_deterministic_strategy(self):
        strategy = event_selection_strategy("min_frequency_deterministic")
        self.assertIsInstance(strategy, types.FunctionType)
        self.assertEqual(strategy.__name__, "min_frequency_deterministic")

    def test_can_initiate_frequency_weighted_strategy(self):
        strategy = event_selection_strategy("frequency_weighted")
        self.assertIsInstance(strategy, types.FunctionType)
        self.assertEqual(strategy.__name__, "frequency_weighted")

    @patch("framework.initialization.partial")
    def test_can_initiate_standard_teardown_strategy(self, partial_mock):
        # Arrange
        adb_path = "adb_path"
        device_id = "device_id"

        # Act
        tear_down_strategy("standard", adb_path=adb_path, device_id=device_id)

        # Assert
        partial_mock.assert_called_with(teardown_strategies.standard, adb_path=adb_path, device_id=device_id)

    @patch("framework.initialization.partial")
    def test_can_initiate_standard_setup_strategy(self, partial_mock):
        # Arrange
        strategy = "standard"
        apk_path = "apk_path"
        adb_path = "adb_path"
        device_id = "device_id"

        # Act
        setup_strategy(strategy, apk_path, adb_path, device_id)

        partial_mock.assert_called_with(setup_strategies.standard, apk_path=apk_path, adb_path=adb_path, device_id=device_id)

    @patch("framework.initialization.partial")
    def test_can_initiate_time_based_completion_criterion(self, partial_mock):
        # Arrange
        criterion = "time"
        time_budget = 1
        test_suite_length = 20

        # Act
        completion_criterion(criterion, time_budget, test_suite_length)

        # Assert
        partial_mock.assert_called_with(completion.time_budget_exceeded, completion_value=time_budget)

    @patch("framework.initialization.partial")
    def test_can_initiate_length_based_completion_criterion(self, partial_mock):
        # Arrange
        criterion = "length"
        time_budget = 1
        test_suite_length = 20

        # Act
        completion_criterion(criterion, time_budget, test_suite_length)

        # Assert
        partial_mock.assert_called_with(completion.number_of_sequences_reached, completion_value=test_suite_length)

    @patch("framework.initialization.partial")
    def test_can_initiate_probabilistic_termination_criterion(self, partial_mock):
        # Arrange
        criterion = "probabilistic"
        probability = 0.05
        length = 15

        # Act
        termination_criterion(criterion, probability, length)

        # Assert
        partial_mock.assert_called_with(termination.probabilistic, terminal_value=probability)

    @patch("framework.initialization.partial")
    def test_can_initiate_length_based_termination_criterion(self, partial_mock):
        # Arrange
        criterion = "length"
        probability = 0.05
        length = 15

        # Act
        termination_criterion(criterion, probability, length)

        # Assert
        partial_mock.assert_called_with(termination.length, terminal_value=length)

