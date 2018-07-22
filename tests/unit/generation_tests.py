import unittest
from unittest.mock import patch, MagicMock
from framework.generation import Generator
from framework.database import Database
from appium import webdriver
from appiumatic.abstraction import create_launch_event, create_action, synthesize, create_target
from appiumatic.execution import Executor
from appiumatic.constants import GUIActionType, SelectorType, TargetType, TargetState


class GenerationTests(unittest.TestCase):
    @patch("framework.generation.time")
    @patch("framework.generation.uuid4")
    def test_can_initialize_test_suite(self, mock_uuid4, mock_time):
        # Arrange
        mock_uuid4().hex = "hexadecimal_uuid"
        mock_time.time.return_value = 123456
        database = MagicMock(Database)
        generator = Generator(database, {})

        # Act
        test_suite = generator.initialize_test_suite()

        # Assert
        generator.database.create_test_suite.assert_called_with(mock_uuid4().hex, mock_time.time())
        self.assertEqual(test_suite.id, mock_uuid4().hex)
        self.assertEqual(test_suite.creation_time, mock_time.time())

    @patch("framework.generation.time")
    @patch("framework.generation.get_current_state")
    def test_can_initialize_test_case(self, get_current_state_func, mock_time):
        # Arrange
        configuration = {
            "apk_path": "apk_path",
            "adb_path": "adb_path"
        }
        generator = Generator(None, configuration)

        driver = MagicMock(webdriver.Remote)
        setup_strategy_func = MagicMock()
        setup_strategy_func.return_value = driver

        start_state = {"stateId": "stateId", "activityName": "activityName"}
        get_current_state_func.return_value = start_state
        complete_launch_event = synthesize(create_launch_event(), start_state)

        start_time = 123456
        mock_time.time.return_value = start_time

        # Act
        test_case = generator.initialize_test_case(setup_strategy_func)

        # Assert
        setup_strategy_func.assert_called_with(configuration["apk_path"], configuration["adb_path"])
        get_current_state_func.assert_called_with(driver)
        self.assertEqual(test_case.driver, driver)
        self.assertEqual(test_case.events, [complete_launch_event])
        self.assertEqual(test_case.start_time, start_time)
        self.assertEqual(test_case.start_state, start_state)

    @patch("framework.generation.get_available_events")
    @patch.object(Generator, "remove_termination_events")
    def test_process_next_event_when_there_are_non_termination_events(self, mock_remove_termination_events, get_available_events):
        # Arrange
        driver = MagicMock(webdriver.Remote)
        executor = MagicMock(Executor)
        executor.driver = driver
        executor.execute = MagicMock()
        target = create_target(SelectorType.ID, "selector", "description", TargetType.BUTTON, TargetState.ENABLED)
        action = create_action(GUIActionType.CLICK, target)
        available_events = [
            {
                "precondition": {
                    "stateId": "stateId",
                    "activityName": "activityName"
                },
                "actions": [action]
            }
        ]
        get_available_events.return_value = available_events
        database = MagicMock(Database)
        generator = Generator(database, {})
        event_selection_strategy = MagicMock()
        event_selection_strategy.return_value = available_events[0]
        mock_remove_termination_events.return_value = available_events

        # Act
        generator.process_next_event(executor, "test_suite_id", event_selection_strategy)

        # Assert
        event_selection_strategy.assert_called_with(database, available_events, test_suite_id="test_suite_id")
        executor.execute.assert_called_with(available_events[0])
        mock_remove_termination_events.assert_called_with("test_suite_id", available_events)

    @patch("framework.generation.time")
    @patch("framework.generation.generate_test_case_hash")
    @patch("framework.generation.write_test_case_to_file")
    def test_finalize_test_case(self, mock_write_test_case, mock_generate_hash, mock_time):
        # Arrange
        mock_time.time.return_value = 123456
        test_case = MagicMock()
        test_case.start_time = 111111
        test_case.events = []
        duration = mock_time.time() - test_case.start_time
        database = MagicMock(Database)
        database.add_test_case = MagicMock()
        test_suite = MagicMock()
        test_suite.id = "abcdef"
        path_to_test_cases = "path_to_test_cases"
        test_case_count = 10
        generator = Generator(database, {})
        mock_generate_hash.return_value = "test_case_hash"

        # Act
        generator.finalize_test_case(test_case, test_suite, path_to_test_cases, test_case_count)

        # Assert
        database.add_test_case.assert_called_with("test_case_hash", test_suite.id, mock_time.time(), duration)
        mock_write_test_case.assert_called_with(path_to_test_cases, test_case.events, test_case_count,
                                                duration)






