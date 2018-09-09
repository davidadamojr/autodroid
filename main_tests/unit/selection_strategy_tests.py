import unittest
from collections import OrderedDict
from unittest.mock import patch, MagicMock

import appiumatic.abstraction as abstraction
from database import Database

import framework.strategies.selection as selection


class SelectionStrategyTests(unittest.TestCase):
    def test_uniform_random_selection_returns_an_event(self):
        # Arrange
        precondition = abstraction.create_state(current_activity=None, state_id=None)
        back_event = abstraction.create_back_event(precondition)
        home_event = abstraction.create_home_event(precondition)
        background_event = abstraction.create_background_event(precondition)
        events = [back_event, home_event, background_event]

        # Act
        selected_event = selection.uniform_random(events=events)

        # Assert
        self.assertIn(selected_event, events)

    @patch("framework.strategies.selection.selection_utils.create_hash_to_events_map")
    def test_min_frequency_random_returns_single_min_event(self, create_hash_to_events_map):
        # Arrange
        precondition = abstraction.create_state(current_activity=None, state_id=None)
        back_event = abstraction.create_back_event(precondition)
        home_event = abstraction.create_home_event(precondition)
        background_event = abstraction.create_background_event(precondition)

        hash_to_events_map = OrderedDict()
        hash_to_events_map["back_event"] = back_event
        hash_to_events_map["home_event"] = home_event
        hash_to_events_map["background_event"] = background_event
        create_hash_to_events_map.return_value = hash_to_events_map

        event_frequencies = OrderedDict()
        event_frequencies["back_event"] = 2
        event_frequencies["home_event"] = 1
        event_frequencies["background_event"] = 2

        database = Database(None)
        database.get_event_frequencies = MagicMock(return_value=event_frequencies)
        events = [back_event, home_event, background_event]

        # Act
        selected_event = selection.min_frequency_random(events=events, database=database, suite_id=1)

        # Assert
        self.assertEqual(selected_event, home_event)

    @patch("framework.strategies.selection.selection_utils.create_hash_to_events_map")
    def test_min_frequency_random_returns_one_of_two_min_events(self, create_hash_to_events_map):
        # Arrange
        precondition = abstraction.create_state(current_activity=None, state_id=None)
        back_event = abstraction.create_back_event(precondition)
        home_event = abstraction.create_home_event(precondition)
        background_event = abstraction.create_background_event(precondition)

        hash_to_events_map = OrderedDict()
        hash_to_events_map["back_event"] = back_event
        hash_to_events_map["home_event"] = home_event
        hash_to_events_map["background_event"] = background_event
        create_hash_to_events_map.return_value = hash_to_events_map

        event_frequencies = OrderedDict()
        event_frequencies["back_event"] = 2
        event_frequencies["home_event"] = 1
        event_frequencies["background_event"] = 1

        database = Database(None)
        database.get_event_frequencies = MagicMock(return_value=event_frequencies)
        events = [back_event, home_event, background_event]

        # Act
        selected_event = selection.min_frequency_random(events=events, database=database, suite_id=1)

        # Assert
        expected_events = [home_event, background_event]
        self.assertNotEqual(selected_event, back_event)
        self.assertIn(selected_event, expected_events)

    @patch("framework.strategies.selection.selection_utils.create_hash_to_events_map")
    def test_min_frequency_deterministic_returns_first_min_event_of_two(self, create_hash_to_events_map):
        # Arrange
        precondition = abstraction.create_state(current_activity=None, state_id=None)
        back_event = abstraction.create_back_event(precondition)
        home_event = abstraction.create_home_event(precondition)
        background_event = abstraction.create_background_event(precondition)

        hash_to_events_map = OrderedDict()
        hash_to_events_map["back_event"] = back_event
        hash_to_events_map["home_event"] = home_event
        hash_to_events_map["background_event"] = background_event
        create_hash_to_events_map.return_value = hash_to_events_map

        event_frequencies = OrderedDict()
        event_frequencies["back_event"] = 1
        event_frequencies["home_event"] = 1
        event_frequencies["background_event"] = 2

        database = Database(None)
        database.get_event_frequencies = MagicMock(return_value=event_frequencies)
        events = [back_event, home_event, background_event]

        # Act
        selected_event = selection.min_frequency_deterministic(events=events, database=database, suite_id=1)

        # Assert
        self.assertEqual(selected_event, back_event)

    @patch("framework.strategies.selection.selection_utils.create_hash_to_events_map")
    def test_min_frequency_deterministic_returns_first_min_event_of_all(self, create_hash_to_events_map):
        # Arrange
        precondition = abstraction.create_state(current_activity=None, state_id=None)
        back_event = abstraction.create_back_event(precondition)
        home_event = abstraction.create_home_event(precondition)
        background_event = abstraction.create_background_event(precondition)

        hash_to_events_map = OrderedDict()
        hash_to_events_map["back_event"] = back_event
        hash_to_events_map["home_event"] = home_event
        hash_to_events_map["background_event"] = background_event
        create_hash_to_events_map.return_value = hash_to_events_map

        event_frequencies = OrderedDict()
        event_frequencies["back_event"] = 2
        event_frequencies["home_event"] = 2
        event_frequencies["background_event"] = 2

        database = Database(None)
        database.get_event_frequencies = MagicMock(return_value=event_frequencies)
        events = [back_event, home_event, background_event]

        # Act
        selected_event = selection.min_frequency_deterministic(events=events, database=database, suite_id=1)

        # Assert
        self.assertEqual(selected_event, back_event)

    @patch("framework.strategies.selection.selection_utils.create_hash_to_events_map")
    @patch("framework.strategies.selection.random.uniform")
    def test_min_frequency_weighted_for_middle_event_of_three(self, random_mock, create_hash_to_events_map):
        # Arrange
        precondition = abstraction.create_state(current_activity=None, state_id=None)
        back_event = abstraction.create_back_event(precondition)
        home_event = abstraction.create_home_event(precondition)
        background_event = abstraction.create_background_event(precondition)

        hash_to_events_map = OrderedDict()
        hash_to_events_map["back_event"] = back_event
        hash_to_events_map["home_event"] = home_event
        hash_to_events_map["background_event"] = background_event
        create_hash_to_events_map.return_value = hash_to_events_map

        event_frequencies = OrderedDict()
        event_frequencies["back_event"] = 2
        event_frequencies["home_event"] = 2
        event_frequencies["background_event"] = 2

        random_mock.return_value = 0.5

        database = Database(None)
        database.get_event_frequencies = MagicMock(return_value=event_frequencies)
        events = [back_event, home_event, background_event]

        # Act
        selected_event = selection.frequency_weighted(events=events, database=database, suite_id=1)

        # Assert
        self.assertEqual(selected_event, home_event)

    @patch("framework.strategies.selection.selection_utils.create_hash_to_events_map")
    @patch("framework.strategies.selection.random.uniform")
    def test_min_frequency_weighted_for_first_event_of_three(self, random_mock, create_hash_to_events_map):
        # Arrange
        precondition = abstraction.create_state(current_activity=None, state_id=None)
        back_event = abstraction.create_back_event(precondition)
        home_event = abstraction.create_home_event(precondition)
        background_event = abstraction.create_background_event(precondition)

        hash_to_events_map = OrderedDict()
        hash_to_events_map["back_event"] = back_event
        hash_to_events_map["home_event"] = home_event
        hash_to_events_map["background_event"] = background_event
        create_hash_to_events_map.return_value = hash_to_events_map

        event_frequencies = OrderedDict()
        event_frequencies["back_event"] = 2
        event_frequencies["home_event"] = 2
        event_frequencies["background_event"] = 2

        random_mock.return_value = 0.2

        database = Database(None)
        database.get_event_frequencies = MagicMock(return_value=event_frequencies)
        events = [back_event, home_event, background_event]

        # Act
        selected_event = selection.frequency_weighted(events=events, database=database, suite_id=1)

        # Assert
        self.assertEqual(selected_event, back_event)

    @patch("framework.strategies.selection.selection_utils.create_hash_to_events_map")
    @patch("framework.strategies.selection.random.uniform")
    def test_min_frequency_weighted_for_last_event_of_three(self, random_mock, create_hash_to_events_map):
        # Arrange
        precondition = abstraction.create_state(current_activity=None, state_id=None)
        back_event = abstraction.create_back_event(precondition)
        home_event = abstraction.create_home_event(precondition)
        background_event = abstraction.create_background_event(precondition)

        hash_to_events_map = OrderedDict()
        hash_to_events_map["back_event"] = back_event
        hash_to_events_map["home_event"] = home_event
        hash_to_events_map["background_event"] = background_event
        create_hash_to_events_map.return_value = hash_to_events_map

        event_frequencies = OrderedDict()
        event_frequencies["back_event"] = 2
        event_frequencies["home_event"] = 2
        event_frequencies["background_event"] = 2

        random_mock.return_value = 0.8

        database = Database(None)
        database.get_event_frequencies = MagicMock(return_value=event_frequencies)
        events = [back_event, home_event, background_event]

        # Act
        selected_event = selection.frequency_weighted(events=events, database=database, suite_id=1)

        # Assert
        self.assertEqual(selected_event, background_event)