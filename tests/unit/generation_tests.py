import unittest
from unittest.mock import patch, MagicMock
from framework.generation import Generator
from framework.database import Database
from appium import webdriver
from appiumatic.abstraction import create_launch_event, synthesize


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
        generator.database.add_test_suite.assert_called_with(mock_uuid4().hex, mock_time.time())
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

