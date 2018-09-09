import unittest
import framework.strategies.completion as completion


class CompletionStrategyTests(unittest.TestCase):
    def test_time_budget_exceeded_when_exceeded(self):
        # Arrange
        time_budget = 3
        suite_duration = 4

        # Act
        exceeded = completion.time_budget_exceeded(completion_value=time_budget, suite_duration=suite_duration)

        # Assert
        self.assertTrue(exceeded)

    def test_time_budget_exceeded_when_not_exceeded(self):
        # Arrange
        time_budget = 3
        suite_duration = 2

        # Act
        exceeded = completion.time_budget_exceeded(completion_value=time_budget, suite_duration=suite_duration)

        # Assert
        self.assertFalse(exceeded)

    def test_number_of_sequences_reached_when_reached(self):
        # Arrange
        sequence_budget = 10
        sequence_count = 10

        # Act
        reached = completion.number_of_sequences_reached(completion_value=sequence_budget, sequence_count=sequence_count)

        # Assert
        self.assertTrue(reached)

    def test_number_of_sequences_reached_when_not_reached(self):
        # Arrange
        sequence_budget = 10
        sequence_count = 9

        # Act
        reached = completion.number_of_sequences_reached(completion_value=sequence_budget, sequence_count=sequence_count)

        # Assert
        self.assertFalse(reached)
