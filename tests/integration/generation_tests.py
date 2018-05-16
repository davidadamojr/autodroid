import os
import shutil
import unittest
import config
import json
import sqlite3

import framework.generation as generation
from framework.generation import Generator
from framework.database import Database
from appiumatic import abstraction
from appiumatic import hashing


def remove_output_files(output_path):
    if not os.path.exists(output_path):
        return

    output_file_names = os.listdir(output_path)
    for output_filename in output_file_names:
        file_path = os.path.join(output_path, output_filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)


def remove_db_file(db_path):
    if not os.path.exists(db_path):
        return

    try:
        os.unlink(db_path)
    except Exception as e:
        print(e)


class GenerationTests(unittest.TestCase):
    def setUp(self):
        self.output_path = config.OUTPUT_PATH
        self.db_path = "autodroid.db"
        remove_output_files(self.output_path)
        remove_db_file(self.db_path)

        print(self.db_path)

    def test_create_output_directories(self):
        # Arrange
        configuration = {
            "apk_package_name": "special_android_app",
            "output_path": self.output_path
        }
        generator = Generator(None, configuration)
        test_suite_creation_time = 1234567890
        apk_package_name = configuration["apk_package_name"]

        # Act
        output_path = config.OUTPUT_PATH
        paths = generator.create_output_directories(test_suite_creation_time)
        path_to_test_cases = paths.test_cases
        path_to_logs = paths.logs
        path_to_coverage = paths.coverage

        # Assert
        self.assertEqual(path_to_test_cases, os.path.join(output_path, "{}_{}".format(apk_package_name, str(test_suite_creation_time)), "testcases"))
        self.assertEqual(path_to_logs, os.path.join(output_path, "{}_{}".format(apk_package_name, str(test_suite_creation_time)), "logs"))
        self.assertEqual(path_to_coverage, os.path.join(output_path, "{}_{}".format(apk_package_name, str(test_suite_creation_time)), "coverage"))
        self.assertEqual(os.path.exists(path_to_test_cases), True)
        self.assertEqual(os.path.exists(path_to_logs), True)
        self.assertEqual(os.path.exists(path_to_coverage), True)

    def test_write_test_case_to_file(self):
        # Arrange
        event_1 = abstraction.create_launch_event()
        state = abstraction.create_state("blaActivity", "state_id")
        event_2 = abstraction.create_back_event(state)
        events = [abstraction.synthesize(event_1, state), abstraction.synthesize(event_2, state)]
        test_suite_creation_time = 1234567890
        configuration = {
            "apk_package_name": "wonderful_apk_package",
            "output_path": self.output_path
        }
        generator = Generator(None, configuration)
        path_to_test_cases, _, _ = generator.create_output_directories(test_suite_creation_time)
        test_case_count = 1
        test_case_duration = 15000

        # Act
        test_case_path = generation.write_test_case_to_file(path_to_test_cases, events, test_case_count,
                                                            test_case_duration)

        # Assert
        self.assertTrue(os.path.exists(test_case_path))

        with open(test_case_path) as test_case_file:
            test_case_from_json = json.load(test_case_file)
            self.assertEqual(len(test_case_from_json), 2)

    def test_remove_termination_events(self):
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
            "actions": [{
                "target": {
                    "selector": "id",
                    "selectorValue": "android:id/add_contact",
                    "description": "Add contact",
                    "type": "Button",
                    "state": "enabled"
                },
                "type": "click",
                "value": None
            }],
            "precondition": {
                "activityName": "contactActivity",
                "stateId": "a1b1c1"
            }
        }
        event3 = {
            "actions": [{
                "target": {
                    "selector": "id",
                    "selectorValue": "android:id/contact_name",
                    "description": "Contact Name",
                    "type": "EditText",
                    "state": "disabled"
                },
                "type": "click",
                "value": None
            }],
            "precondition": {
                "activityName": "launchActivity",
                "stateId": "abcdef"
            }
        }

        db_connection = sqlite3.connect(self.db_path)
        database = Database(db_connection)
        database.create_tables()

        test_suite_id = "test_suite_id"

        available_events = [event1, event2, event3]
        event1_hash = hashing.generate_event_hash(event1)

        database.add_termination_event(event1_hash, test_suite_id)
        generator = Generator(database, {})

        # Act
        non_termination_events = generator.remove_termination_events(test_suite_id, available_events)
        database.close()

        # Assert
        self.assertEqual(len(non_termination_events), 2)
        self.assertNotIn(event1, non_termination_events)

    def tearDown(self):
        remove_output_files(self.output_path)
        remove_db_file(self.db_path)

