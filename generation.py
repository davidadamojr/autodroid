import logging
import database
from appiumatic.uianalysis import get_available_events, get_current_state
from uuid import uuid4
from appiumatic.execution import execute
from appiumatic.abstraction import create_launch_event, synthesize

__author__ = "David Adamo Jr."

logger = logging.getLogger(__name__)

class TestBuilder:
    def __init__(self):
        self.connection_failures = 0

class SuiteBuilder(TestBuilder):
    def __init__(self, apk_path, event_interval, test_suite_dir, db_connection):
        super().__init__()
        self.apk_path = apk_path
        self.event_interval = event_interval
        self.test_suite_dir = test_suite_dir
        self.db_connection = db_connection

    def generate_test_suite(self, event_selection_strategy, termination_criterion, completion_criterion, setup,
                            teardown):
        test_suite_id = uuid4().hex
        database.add_test_suite(self.db_connection, test_suite_id)

        test_suite_event_count = 0

        test_suite_complete = False
        while not test_suite_complete:
            test_case = []
            try:
                driver = setup(self.apk_path)
            except ConnectionRefusedError as conn_refused:
                self.connection_failures += 1
                logger.error("Could not connect to appium server: %s".format(conn_refused))
                if self.connection_failures > 2:
                    raise ConnectionRefusedError

                continue

            launch_event = create_launch_event()
            current_state = get_current_state(driver) # error handling here
            complete_event = synthesize(launch_event, current_state)
            test_case.append(complete_event)

            test_case_event_count = 1
            test_suite_event_count += 1

            test_case_complete = termination_criterion(self.db_connection, event_count=test_case_event_count)
            while not test_case_complete:
                try:
                    partial_events = get_available_events(driver) # error handling here
                    selected_event = event_selection_strategy(partial_events, self.db_connection)
                    execute(selected_event)
                    current_state = get_current_state(driver)
                    complete_event = synthesize(selected_event, current_state)
                    test_case.append(complete_event)
                    test_case_event_count += 1
                    test_suite_event_count += 1
                except Exception as e:
                    print(e)

                test_case_complete = termination_criterion(self.db_connection, event_count=test_case_event_count)

            teardown(test_case, driver, self.db_connection)

            test_suite_complete = completion_criterion()


class MonkeyBuilder(TestBuilder):
    def __init__(self, apk_path, db_connection):
        super().__init__()
        self.apk_path = apk_path
        self.db_connection = db_connection

    def generate_monkey_test(self, event_selection_strategy, completion_criterion, setup, teardown):
        pass




