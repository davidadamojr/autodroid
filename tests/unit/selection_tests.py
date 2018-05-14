import unittest
from framework.utils import selection


class SelectionUnitTests(unittest.TestCase):

    def test_get_frequency_weights(self):
        # Arrange
        event_frequencies = {
            "event_hash_1": 2,
            "event_hash_2": 2,
            "event_hash_3": 5,
            "event_hash_4": 4
        }
        total_frequency = sum(event_frequencies.values())

        # Act
        event_weights = selection.get_frequency_weights(event_frequencies)

        # Assert
        expected_weights = {
            "event_hash_1": 6.5,
            "event_hash_2": 6.5,
            "event_hash_3": 2.6,
            "event_hash_4": 3.25
        }
        self.assertEqual(expected_weights, event_weights)

    def test_get_uniform_weights(self):
        # Arrange
        event_hashes = ["event_hash_1", "event_hash_2", "event_hash_3"]

        # Act
        event_weights = selection.get_uniform_weights(event_hashes)

        # Assert
        expected_weights = {"event_hash_1": 1, "event_hash_2": 1, "event_hash_3": 1}
        self.assertEqual(expected_weights, event_weights)

