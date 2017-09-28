import database
from appiumatic.uianalysis import get_events, get_current_state
from uuid import uuid4
from appiumatic.execution import execute
from appiumatic.abstractions import create_launch_event, get_current_state, synthesize

__author__ = "David Adamo Jr."


class SuiteBuilder:
    def __init__(self, apk_path, event_interval, test_suite_dir, db_connection):
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
            driver = setup(self.apk_path)
            partial_event = create_launch_event()
            execute(partial_event) # error handling here
            current_state = get_current_state(driver) # error handling here
            complete_event = synthesize(partial_event, current_state)
            test_case.append(complete_event)

            test_case_event_count = 1
            test_suite_event_count += 1

            test_case_complete = termination_criterion(self.db_connection, event_count=test_case_event_count)
            while not test_case_complete:
                try:
                    partial_events = get_events(driver) # error handling here
                    selected_event = event_selection_strategy(partial_events, self.db_connection)
                    execute(selected_event)
                    complete_event = synthesize(selected_event)
                    test_case.append(complete_event)
                    test_case_event_count += 1
                    test_suite_event_count += 1
                except Exception as e:
                    print(e)

                test_case_complete = termination_criterion(self.db_connection, event_count=test_case_event_count)

            teardown(test_case, driver, self.db_connection)

            test_suite_complete = completion_criterion()



class MonkeyBuilder:
    def __init__(self, apk_path, db_connection):
        self.apk_path = apk_path
        self.db_connection = db_connection

    def generate_monkey_test(self, event_selection_strategy, completion_criterion, setup, teardown):
        pass




