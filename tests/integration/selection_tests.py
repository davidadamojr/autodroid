import unittest
import sqlite3
import os
from framework.database import Database
from framework.strategies.selection import min_frequency_random, min_frequency_deterministic
from appiumatic import abstraction, hashing, actions
from appiumatic.constants import GUIActionType


def setup_events():
    current_state = abstraction.create_state("contactsActivity", "abcdef")
    target_1 = {
        "selector": "id",
        "selectorValue": "ok_btn",
        "type": "button",
        "description": "OK",
        "state": "enabled"
    }
    action_1 = actions.Click(target_1, GUIActionType.CLICK, None)

    target_2 = {
        "selector": "id",
        "selectorValue": "cancel_btn",
        "type": "button",
        "description": "Cancel",
        "state": "enabled"
    }
    action_2 = actions.Click(target_2, GUIActionType.CLICK, None)

    target_3 = {
        "selector": "id",
        "selectorValue": "gender_radio_btn",
        "type": "radiobutton",
        "description": "Gender",
        "state": "enabled"
    }
    action_3 = actions.Click(target_3, GUIActionType.CLICK, None)

    event_1 = {
        "precondition": current_state,
        "actions": [action_1]
    }
    event_2 = {
        "precondition": current_state,
        "actions": [action_2]
    }
    event_3 = {
        "precondition": current_state,
        "actions": [action_3]
    }
    available_events = [event_1, event_2, event_3]

    return available_events


class SelectionTests(unittest.TestCase):

    def setUp(self):
        connection = sqlite3.connect("autodroid.db")
        self.database = Database(connection)
        self.database.create_tables()

        cursor = self.database.cursor()
        cursor.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND (name='test_suites' OR name='stats' OR name='test_cases'" +
            " OR name='event_info')")
        self.assertEqual(len(cursor.fetchall()), 4)

        self.available_events = setup_events()

    def test_min_frequency_random_selection_with_single_choice(self):
        # Arrange
        event_hash_2 = hashing.generate_event_hash(self.available_events[1])
        event_hash_3 = hashing.generate_event_hash(self.available_events[2])
        test_suite_id = "test_suite_id"

        self.database.update_event_frequency(test_suite_id, event_hash_2)
        self.database.update_event_frequency(test_suite_id, event_hash_3)

        # Act
        selected_event = min_frequency_random(self.database, self.available_events, suite_id=test_suite_id)

        # Assert
        expected_selected_event = self.available_events[0]
        self.assertEqual(selected_event, expected_selected_event)

    def test_min_frequency_random_selection_with_multiple_choices(self):
        # Arrange
        event_hash_2 = hashing.generate_event_hash(self.available_events[1])
        test_suite_id = "test_suite_id"

        self.database.update_event_frequency(test_suite_id, event_hash_2)

        # Act
        selected_event = min_frequency_random(self.database, self.available_events, suite_id=test_suite_id)

        # Assert
        expected_selected_events = [self.available_events[0], self.available_events[2]]
        self.assertIn(selected_event, expected_selected_events)

    def test_min_frequency_deterministic_selection_with_single_choice(self):
        # Arrange
        event_hash_2 = hashing.generate_event_hash(self.available_events[1])
        event_hash_3 = hashing.generate_event_hash(self.available_events[2])
        test_suite_id = "test_suite_id"

        self.database.update_event_frequency(test_suite_id, event_hash_2)
        self.database.update_event_frequency(test_suite_id, event_hash_3)

        # Act
        selected_event = min_frequency_deterministic(self.database, self.available_events, suite_id=test_suite_id)

        # Assert
        expected_selected_event = self.available_events[0]
        self.assertEqual(selected_event, expected_selected_event)

    def test_min_frequency_deterministic_selection_with_multiple_choices(self):
        # Arrange
        event_hash_2 = hashing.generate_event_hash(self.available_events[1])
        test_suite_id = "test_suite_id"

        self.database.update_event_frequency(test_suite_id, event_hash_2)

        # Act
        selected_event = min_frequency_deterministic(self.database, self.available_events, suite_id=test_suite_id)

        # Assert
        expected_events = [self.available_events[0], self.available_events[2]]
        self.assertIn(selected_event, expected_events)

    def tearDown(self):
        self.database.close()
        db_path = os.path.join("autodroid.db")
        if os.path.isfile(db_path):
            os.remove(db_path)