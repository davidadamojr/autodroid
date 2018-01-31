import hashing
import unittest
import random
from constants import CLICK, LONG_CLICK, CHECK, UNCHECK, SCROLL_UP, SCROLL_DOWN, TEXT_ENTRY


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
                "type": TEXT_ENTRY,
                "value": None
            }, {
                "target": widgets[1],
                "type": TEXT_ENTRY,
                "value": None
            }, {
                "target": widgets[2],
                "type": CLICK,
                "value": None
            }, {
                "target": widgets[3],
                "type": CHECK,
                "value": None
            }, {
                "target": widgets[3],
                "type": UNCHECK,
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
                "type": TEXT_ENTRY,
                "value": None
            }, {
                "target": widgets[1],
                "type": TEXT_ENTRY,
                "value": None
            }, {
                "target": widgets[2],
                "type": CLICK,
                "value": None
            }, {
                "target": widgets[3],
                "type": CHECK,
                "value": None
            }, {
                "target": widgets[3],
                "type": UNCHECK,
                "value": None
            }
        ]

        hashes = []
        for i in range(10):
            random.shuffle(possible_actions)
            state_id = hashing.generate_state_hash(possible_actions)
            hashes.append(state_id)

        self.assertEqual(len(set(hashes)), 1)