import unittest
from unittest.mock import MagicMock
from unittest.mock import patch

from database import Database

from framework.strategies import termination


class TerminationStrategyTests(unittest.TestCase):
    @patch("framework.strategies.termination.random.random")
    def test_probabilistic_termination_when_is_probable_and_sequence_does_not_exist(self, random_mock):
        # Arrange
        database = Database(None)
        database.sequence_exists = MagicMock(return_value=False)
        sequence_hash = "sequence_hash"
        suite_id = "suite_id"
        terminal_value = 0.05
        random_mock.return_value = 0.04

        # Act
        termination_result = termination.probabilistic(database=database,
                                                       sequence_hash=sequence_hash,
                                                       suite_id=suite_id,
                                                       terminal_value=terminal_value)

        # Assert
        self.assertTrue(termination_result)

    @patch("framework.strategies.termination.random.random")
    def test_probabilistic_termination_when_is_probable_and_sequence_already_exists(self, random_mock):
        # Arrange
        database = Database(None)
        database.sequence_exists = MagicMock(return_value=True)
        sequence_hash = "sequence_hash"
        suite_id = "suite_id"
        terminal_value = 0.05
        random_mock.return_value = 0.04

        # Act
        termination_result = termination.probabilistic(database=database,
                                                       sequence_hash=sequence_hash,
                                                       suite_id=suite_id,
                                                       terminal_value=terminal_value)

        # Assert
        self.assertFalse(termination_result)

    @patch("framework.strategies.termination.random.random")
    def test_probabilistic_termination_when_is_not_probable_and_sequence_already_exists(self, random_mock):
        # Arrange
        database = Database(None)
        database.sequence_exists = MagicMock(return_value=True)
        sequence_hash = "sequence_hash"
        suite_id = "suite_id"
        terminal_value = 0.05
        random_mock.return_value = 0.09

        # Act
        termination_result = termination.probabilistic(database=database,
                                                       sequence_hash=sequence_hash,
                                                       suite_id=suite_id,
                                                       terminal_value=terminal_value)

        # Assert
        self.assertFalse(termination_result)

    @patch("framework.strategies.termination.random.random")
    def test_probabilistic_termination_when_is_not_probable_and_sequence_does_not_exist(self, random_mock):
        # Arrange
        database = Database(None)
        database.sequence_exists = MagicMock(return_value=False)
        sequence_hash = "sequence_hash"
        suite_id = "suite_id"
        terminal_value = 0.05
        random_mock.return_value = 0.09

        # Act
        termination_result = termination.probabilistic(database=database,
                                                       sequence_hash=sequence_hash,
                                                       suite_id=suite_id,
                                                       terminal_value=terminal_value)

        # Assert
        self.assertFalse(termination_result)
