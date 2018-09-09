import unittest
from unittest.mock import patch
from collections import OrderedDict
from framework.utils import selection as selection_utils
from appiumatic.abstraction import create_home_event, create_back_event, create_background_event, create_state


class SelectionUtilsTests(unittest.TestCase):

    def test_get_frequency_weights(self):
        # Arrange
        event_frequencies = {
            "event_hash_1": 1,
            "event_hash_2": 2,
            "event_hash_3": 5,
            "event_hash_4": 4
        }

        # Act
        event_weights = selection_utils.get_frequency_weights(event_frequencies)

        # Assert
        expected_weights = {
            "event_hash_1": 6.0,
            "event_hash_2": 4.0,
            "event_hash_3": 2.0,
            "event_hash_4": 2.4
        }
        self.assertEqual(expected_weights, event_weights)

    def test_get_uniform_weights(self):
        # Arrange
        event_hashes = ["event_hash_1", "event_hash_2", "event_hash_3"]

        # Act
        event_weights = selection_utils.get_uniform_event_weights(event_hashes)

        # Assert
        expected_weights = {"event_hash_1": 1, "event_hash_2": 1, "event_hash_3": 1}
        self.assertEqual(expected_weights, event_weights)

    @patch("framework.utils.selection.generate_event_hash")
    def test_create_hash_to_events_map(self, generate_event_hash_mock):
        # Arrange
        event_1 = "event_1"
        event_2 = "event_2"
        events = [event_1, event_2]

        def side_effect(event):
            if event == event_1:
                return "event_hash_1"
            else:
                return "event_hash_2"
        generate_event_hash_mock.side_effect = side_effect

        # Act
        hash_to_events_map = selection_utils.create_hash_to_events_map(events)

        # Assert
        self.assertEqual(len(hash_to_events_map), 2)
        self.assertEqual(hash_to_events_map["event_hash_1"], event_1)
        self.assertEqual(hash_to_events_map["event_hash_2"], event_2)

    def test_get_min_frequency_events_when_all_have_same_frequency(self):
        # Arrange
        event_frequencies = OrderedDict()
        event_frequencies["event_hash_1"] = 2
        event_frequencies["event_hash_2"] = 2
        event_frequencies["event_hash_3"] = 2

        # Act
        min_frequency_event_hashes = selection_utils.get_min_frequency_event_hashes(event_frequencies)

        # Assert
        self.assertEqual(len(min_frequency_event_hashes), 3)
        self.assertEqual(min_frequency_event_hashes[0], "event_hash_1")
        self.assertEqual(min_frequency_event_hashes[1], "event_hash_2")
        self.assertEqual(min_frequency_event_hashes[2], "event_hash_3")

    def test_get_min_frequency_events_when_only_one_with_min_frequency(self):
        # Arrange
        event_frequencies = OrderedDict()
        event_frequencies["event_hash_1"] = 2
        event_frequencies["event_hash_2"] = 2
        event_frequencies["event_hash_3"] = 1

        # Act
        min_frequency_event_hashes = selection_utils.get_min_frequency_event_hashes(event_frequencies)

        # Assert
        self.assertEqual(len(min_frequency_event_hashes), 1)
        self.assertEqual(min_frequency_event_hashes[0], "event_hash_3")

    def test_make_weighted_selection_with_zero_goal_weight(self):
        # Arrange
        precondition = create_state(current_activity=None, state_id=None)
        hash_to_events_map = OrderedDict()
        hash_to_events_map["event_hash_1"] = create_background_event(precondition)
        hash_to_events_map["event_hash_2"] = create_home_event(precondition)
        hash_to_events_map["event_hash_3"] = create_back_event(precondition)

        event_weights = OrderedDict()
        event_weights["event_hash_1"] = 2
        event_weights["event_hash_2"] = 4
        event_weights["event_hash_3"] = 6

        goal_weight = 0.0

        # Act
        selected_event = selection_utils.make_weighted_selection(hash_to_events_map, event_weights, goal_weight)

        # Assert
        self.assertEqual(selected_event, hash_to_events_map["event_hash_1"])

    def test_make_weighted_selection_with_max_goal_weight(self):
        # Arrange
        precondition = create_state(current_activity=None, state_id=None)
        hash_to_events_map = OrderedDict()
        hash_to_events_map["event_hash_1"] = create_background_event(precondition)
        hash_to_events_map["event_hash_2"] = create_home_event(precondition)
        hash_to_events_map["event_hash_3"] = create_back_event(precondition)

        event_weights = OrderedDict()
        event_weights["event_hash_1"] = 2
        event_weights["event_hash_2"] = 4
        event_weights["event_hash_3"] = 6

        goal_weight = 7.5

        # Act
        selected_event = selection_utils.make_weighted_selection(hash_to_events_map, event_weights, goal_weight)

        # Assert
        self.assertEqual(selected_event, hash_to_events_map["event_hash_3"])