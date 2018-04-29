import hashing
import unittest
import random
from constants import *


class HashingTests(unittest.TestCase):

    def test_state_hash_is_stable(self):
        widgets = [
            {
                "selector": "id",
                "selectorValue": "android:id/title1",
                "description": "",
                "type": "EditText",
                "state": "enabled"
            },
            {
                "selector": "id",
                "selectorValue": "android:id/title2",
                "description": "",
                "type": "EditText",
                "state": "enabled"
            },
            {
                "selector": "id",
                "selectorValue": "android:id/btn2",
                "description": "Login",
                "type": "TextView",
                "state": "enabled"
            },
            {
                "selector": "id",
                "selectorValue": "android:id/checkbox1",
                "description": "Show All",
                "type": "CheckBox",
                "state": "enabled"
            }
        ]

        possible_actions = [
            {
                "target": widgets[0],
                "type": GUIAction.TEXT_ENTRY,
                "value": "Hello World!"
            }, {
                "target": widgets[1],
                "type": GUIAction.TEXT_ENTRY,
                "value": None
            }, {
                "target": widgets[2],
                "type": GUIAction.CLICK,
                "value": None
            }, {
                "target": widgets[3],
                "type": GUIAction.CHECK,
                "value": None
            }, {
                "target": widgets[3],
                "type": GUIAction.UNCHECK,
                "value": None
            }
        ]

        hashes = []
        for i in range(10):
            state_id = hashing.generate_state_hash(possible_actions)
            hashes.append(state_id)
        self.assertEqual(len(set(hashes)), 1)

    def test_state_hash_ignores_order(self):
        widgets = [
            {
                "selector": "id",
                "selectorValue": "android:id/title1",
                "description": "",
                "type": "EditText",
                "state": "enabled"
            },
            {
                "selector": "id",
                "selectorValue": "android:id/title2",
                "description": "",
                "type": "EditText",
                "state": "enabled"
            },
            {
                "selector": "id",
                "selectorValue": "android:id/btn2",
                "description": "Login",
                "type": "TextView",
                "state": "enabled"
            },
            {
                "selector": "id",
                "selectorValue": "android:id/checkbox1",
                "description": "Show All",
                "type": "CheckBox",
                "state": "enabled"
            }
        ]

        possible_actions = [
            {
                "target": widgets[0],
                "type": GUIAction.TEXT_ENTRY,
                "value": None
            }, {
                "target": widgets[1],
                "type": GUIAction.TEXT_ENTRY,
                "value": None
            }, {
                "target": widgets[2],
                "type": GUIAction.CLICK,
                "value": None
            }, {
                "target": widgets[3],
                "type": GUIAction.CHECK,
                "value": None
            }, {
                "target": widgets[3],
                "type": GUIAction.UNCHECK,
                "value": None
            }
        ]

        hashes = []
        for i in range(10):
            random.shuffle(possible_actions)
            state_id = hashing.generate_state_hash(possible_actions)
            hashes.append(state_id)

        self.assertEqual(len(set(hashes)), 1)

    def test_get_hash_event(self):
        # Arrange
        event = {
            "actions": [{
                "target": {
                    "selector": "id",
                    "selectorValue": "android:id/display_preferences",
                    "description": "Display Preferences",
                    "type": "TextView",
                    "state": "enabled"
                },
                "type": "click",
                "value": None
            }],
            "precondition": {
                "activityName": "launchActivity",
                "stateId": "abcdef"
            }
        }

        # Act
        hash_event = hashing._get_hash_event(event)

        # Assert
        self.assertNotIn("value", hash_event["actions"][0])

    def test_event_hashing(self):
        # Arrange
        event = {
            "actions": [{
                "target": {
                    "selector": "id",
                    "selectorValue": "android:id/display_preferences",
                    "description": "Display Preferences",
                    "type": "TextView",
                    "state": "enabled"
                },
                "type": "click",
                "value": None
            }],
            "precondition": {
                "activityName": "launchActivity",
                "stateId": "abcdef"
            }
        }

        # Act
        event_hash = hashing.generate_event_hash(event)

        # Assert
        self.assertEqual(event_hash, "1c7d92889def3c42168491899e45bfb9a70ef790")

    def test_event_hash_is_stable(self):
        # Arrange
        event = {
            "actions": [{
                "target": {
                    "selector": "id",
                    "selectorValue": "android:id/display_preferences",
                    "description": "Display Preferences",
                    "type": "TextView",
                    "state": "enabled"
                },
                "type": "click",
                "value": None
            }],
            "precondition": {
                "activityName": "launchActivity",
                "stateId": "abcdef"
            }
        }

        # Act
        hashes = []
        for i in range(10):
            event_hash = hashing.generate_event_hash(event)
            hashes.append(event_hash)

        # Assert
        self.assertEqual(len(set(hashes)), 1)

    def test_event_hashing_does_not_change_with_key_order(self):
        # Arrange
        event1 = {
            "actions": [{
                "target": {
                    "selector": "id",
                    "selectorValue": "android:id/display_preferences",
                    "description": "Display Preferences",
                    "type": "TextView",
                    "state": "enabled"
                },
                "type": "click",
                "value": None
            }],
            "precondition": {
                "activityName": "launchActivity",
                "stateId": "abcdef"
            }
        }

        event2 = {
            "precondition": {
                "activityName": "launchActivity",
                "stateId": "abcdef"
            },
            "actions": [{
                "target": {
                    "selector": "id",
                    "selectorValue": "android:id/display_preferences",
                    "description": "Display Preferences",
                    "type": "TextView",
                    "state": "enabled"
                },
                "type": "click",
                "value": None
            }]
        }

        # Act
        event_hash1 = hashing.generate_event_hash(event1)
        event_hash2 = hashing.generate_event_hash(event2)

        # Assert
        self.assertEqual(event_hash1, event_hash2)

    def test_event_hash_is_same_regardless_of_value(self):
        # Arrange
        event1 = {
            "actions": [{
                "target": {
                    "selector": "id",
                    "selectorValue": "android:id/display_preferences",
                    "description": "Display Preferences",
                    "type": "EditText",
                    "state": "enabled"
                },
                "type": "click",
                "value": "Wunderland"
            }],
            "precondition": {
                "activityName": "launchActivity",
                "stateId": "abcdef"
            }
        }

        event2 = {
            "actions": [{
                "target": {
                    "selector": "id",
                    "selectorValue": "android:id/display_preferences",
                    "description": "Display Preferences",
                    "type": "EditText",
                    "state": "enabled"
                },
                "type": "click",
                "value": "Jekyll"
            }],
            "precondition": {
                "activityName": "launchActivity",
                "stateId": "abcdef"
            }
        }

        # Act
        event_hash1 = hashing.generate_event_hash(event1)
        event_hash2 = hashing.generate_event_hash(event2)

        # Assert
        self.assertEqual(event_hash1, event_hash2)

    def test_that_disabled_and_enabled_events_have_different_hash(self):
        # Arrange
        enabled_event = {
            "actions": [{
                "target": {
                    "selector": "id",
                    "selectorValue": "android:id/display_preferences",
                    "description": "Display Preferences",
                    "type": "TextView",
                    "state": "enabled"
                },
                "type": "click",
                "value": None
            }],
            "precondition": {
                "activityName": "launchActivity",
                "stateId": "abcdef"
            }
        }

        disabled_event = {
            "precondition": {
                "activityName": "launchActivity",
                "stateId": "abcdef"
            },
            "actions": [{
                "target": {
                    "selector": "id",
                    "selectorValue": "android:id/display_preferences",
                    "description": "Display Preferences",
                    "type": "TextView",
                    "state": "disabled"
                },
                "type": "click",
                "value": None
            }]
        }

        # Act
        enabled_event_hash = hashing.generate_event_hash(enabled_event)
        disabled_event_hash = hashing.generate_event_hash(disabled_event)

        # Assert
        self.assertNotEqual(enabled_event_hash, disabled_event_hash)

    def test_generate_test_case_hash(self):
        # Arrange
        event1 = {
            "actions": [{
                "target": {
                    "selector": "id",
                    "selectorValue": "android:id/display_preferences",
                    "description": "Display Preferences",
                    "type": "TextView",
                    "state": "enabled"
                },
                "type": "click",
                "value": None
            }],
            "precondition": {
                "activityName": "launchActivity",
                "stateId": "abcdef"
            }
        }

        event2 = {
            "precondition": {
                "activityName": "launchActivity",
                "stateId": "abcdef"
            },
            "actions": [{
                "target": {
                    "selector": "id",
                    "selectorValue": "android:id/display_preferences",
                    "description": "Display Preferences",
                    "type": "TextView",
                    "state": "disabled"
                },
                "type": "click",
                "value": None
            }]
        }
        test_case = [event1, event2]

        # Act
        test_case_hash = hashing.generate_test_case_hash(test_case)

        # Assert
        self.assertEqual(test_case_hash, "854ec40eabd6348cd96507a1339d9bd64919e747")

    def test_generate_test_case_hash_with_different_order_of_events(self):
        # Arrange
        event1 = {
            "actions": [{
                "target": {
                    "selector": "id",
                    "selectorValue": "android:id/display_preferences",
                    "description": "Display Preferences",
                    "type": "TextView",
                    "state": "enabled"
                },
                "type": "click",
                "value": None
            }],
            "precondition": {
                "activityName": "launchActivity",
                "stateId": "abcdef"
            }
        }

        event2 = {
            "precondition": {
                "activityName": "launchActivity",
                "stateId": "abcdef"
            },
            "actions": [{
                "target": {
                    "selector": "id",
                    "selectorValue": "android:id/display_preferences",
                    "description": "Display Preferences",
                    "type": "TextView",
                    "state": "disabled"
                },
                "type": "click",
                "value": None
            }]
        }
        test_case1 = [event1, event2]
        test_case2 = [event2, event1]

        # Act
        test_case_hash1 = hashing.generate_test_case_hash(test_case1)
        test_case_hash2 = hashing.generate_test_case_hash(test_case2)

        # Assert
        self.assertNotEqual(test_case_hash1, test_case_hash2)



