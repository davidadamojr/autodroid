import time
import json
import collections
import os
import framework.utils.scripts as scripts
from framework.database import *
from uuid import uuid4

from appiumatic.abstraction import create_launch_event, create_home_event, create_back_event, synthesize
from appiumatic.execution import Executor
from appiumatic.ui_analysis import get_available_events, get_current_state
from appiumatic.hashing import generate_test_case_hash, generate_event_hash

logger = logging.getLogger(__name__)


def write_test_case_to_file(path_to_test_cases, events, test_case_count, test_case_duration):
    test_case_count = str(test_case_count+1).zfill(3)
    test_case_path = os.path.join(path_to_test_cases, "tc{}_{}.json".format(test_case_count, test_case_duration))
    test_case_data = {
        "events": events,
        "length": len(events)
    }

    with open(test_case_path, 'w') as test_case_file:
        json.dump(test_case_data, test_case_file, sort_keys=True)

    return test_case_path


def create_test_case_path(output_path):
    path_to_test_cases = os.path.join(output_path, "testcases")
    if not os.path.exists(path_to_test_cases):
        os.makedirs(path_to_test_cases)
    logger.debug("Test cases are stored in {}.".format(path_to_test_cases))

    return path_to_test_cases


def create_log_path(output_path):
    path_to_logs = os.path.join(output_path, "logs")
    if not os.path.exists(path_to_logs):
        os.makedirs(path_to_logs)
    logger.debug("Logs are stored in {}.".format(path_to_logs))

    return path_to_logs


def create_coverage_path(output_path):
    path_to_coverage = os.path.join(output_path, "coverage")
    if not os.path.exists(path_to_coverage):
        os.makedirs(path_to_coverage)
    logger.debug("Coverage files are stored in {}.".format(path_to_coverage))

    return path_to_coverage


class Generator:
    def __init__(self, db_connection, configuration):
        self.db_connection = db_connection
        self.configuration = configuration

    def initialize_test_suite(self):
        test_suite_id = uuid4().hex
        test_suite_creation_time = int(time.time())

        add_test_suite(self.db_connection, test_suite_id, test_suite_creation_time)

        TestSuite = collections.namedtuple("TestSuite", ["id", "creation_time"])
        return TestSuite(test_suite_id, test_suite_creation_time)

    def remove_termination_events(self, test_suite_id, events):
        non_termination_events = []
        for event in events:
            event_hash = generate_event_hash(event)
            if is_termination_event(self.db_connection, test_suite_id, event_hash):
                logger.debug("Removing termination event {}".format(event_hash))
                continue

            non_termination_events.append(event)

        return non_termination_events

    def create_output_directories(self, test_suite_creation_time):
        apk_package_name = self.configuration["apk_package_name"]
        logger.debug("APK package name is {}".format(apk_package_name))
        output_path = self.configuration["output_path"]
        logger.debug("Output path is {}".format(output_path))
        output_path = os.path.join(output_path, "{}_{}".format(apk_package_name, str(test_suite_creation_time)))

        if not os.path.exists(output_path):
            os.makedirs(output_path)

        path_to_test_cases = create_test_case_path(output_path)
        path_to_logs = create_log_path(output_path)
        path_to_coverage = create_coverage_path(output_path)

        OutputPaths = collections.namedtuple("OutputPaths", ["test_cases", "logs", "coverage"])
        return OutputPaths(path_to_test_cases, path_to_logs, path_to_coverage)

    def initialize_test_case(self, setup_strategy):
        apk_path = self.configuration["apk_path"]
        adb_path = self.configuration["adb_path"]
        logger.debug("Path to APK is {}".format(apk_path))
        driver = setup_strategy(apk_path, adb_path)

        start_time = time.time()
        launch_event = create_launch_event()
        start_state = get_current_state(driver)  # error handling here
        complete_event = synthesize(launch_event, start_state)
        events = [complete_event]
        logger.debug("Test case initialization complete.")

        TestCase = collections.namedtuple("TestCase", ["driver", "events", "start_time", "start_state"])
        return TestCase(driver, events, start_time, start_state)

    def process_next_event(self, executor, test_suite_id, event_selection_strategy):
        driver = executor.driver
        partial_events = get_available_events(driver)
        non_termination_events = self.remove_termination_events(test_suite_id, partial_events)
        if non_termination_events:
            selected_event = event_selection_strategy(self.db_connection, non_termination_events,
                                                      test_suite_id=test_suite_id)
        else:
            logger.warning("No events available for selection. All events in the current state are "
                           "marked as termination events.")
            current_state = partial_events[0]["precondition"]
            selected_event = create_back_event(current_state)
        executor.execute(selected_event)
        resulting_state = get_current_state(driver)
        complete_event = synthesize(selected_event, resulting_state)
        event_hash = generate_event_hash(complete_event)
        update_event_frequency(self.db_connection, test_suite_id, event_hash)

        NextEvent = collections.namedtuple("NextEvent", ["event", "event_hash", "resulting_state"])
        return NextEvent(complete_event, event_hash, resulting_state)

    def get_coverage(self, coverage_path, test_case_count):
        coverage_file_path = self.configuration["coverage_file_path"] + "/coverage.ec"
        coverage_file_name = "coverage{}.ec".format(str(test_case_count+1).zfill(3))
        coverage_broadcast = self.configuration["coverage_broadcast"]
        scripts.get_coverage(self.configuration["adb_path"], coverage_file_path, coverage_path, coverage_file_name,
                             coverage_broadcast)

    def get_logs(self, logs_path, test_case_count):
        log_file_name = "log{}.txt".format(str(test_case_count+1).zfill(3))
        log_file_path = os.path.join(logs_path, log_file_name)
        apk_package_name = self.configuration["apk_package_name"]
        app_process_id = scripts.get_process_id(self.configuration["adb_path"], apk_package_name)
        scripts.get_logs(self.configuration["adb_path"], log_file_path, app_process_id)

    def generate_events(self, executor, test_case, test_suite, event_selection_strategy, termination_criterion):
        event_count = len(test_case.events)
        current_state = test_case.start_state
        while not termination_criterion(self.db_connection, test_case_hash=generate_test_case_hash(test_case.events),
                                        event_count=event_count, test_suite_id=test_suite.id):
            next_event = self.process_next_event(executor, test_suite.id, event_selection_strategy)
            current_state = next_event.resulting_state
            test_case.events.append(next_event.event)
            event_count += 1

            # end the test case if event explores beyond boundary of the application under test
            current_package = test_case.driver.current_package
            if current_package != self.configuration["apk_package_name"]:
                add_termination_event(self.db_connection, next_event.event_hash, test_suite.id)
                logger.debug("Identified termination event: {}".format(next_event.event))
                break

        return current_state

    def construct_test_suite(self, setup_strategy, event_selection_strategy, termination_criterion, completion_criterion,
                             teardown_strategy):
        test_suite = self.initialize_test_suite()
        output_paths = self.create_output_directories(test_suite.creation_time)

        test_suite_duration = 0
        test_case_count = 0
        while not completion_criterion(test_duration=test_suite_duration, test_case_count=test_case_count):
            try:
                test_case = self.initialize_test_case(setup_strategy)
                logger.debug(
                    "Generating test case {}. Start time is {}.".format(test_case_count + 1, test_case.start_time))
                executor = Executor(test_case.driver, self.configuration["event_interval"],
                                    self.configuration["text_entry_values"])
                final_state = self.generate_events(executor, test_case, test_suite, event_selection_strategy,
                                                   termination_criterion)
            except Exception as e:
                print(e)
                continue  # start a new test case

            # always end test cases by clicking the home event, but do not add the event to the test case
            home_event = create_home_event(final_state)
            executor.execute(home_event)

            self.get_coverage(output_paths.coverage, test_case_count)
            self.get_logs(output_paths.logs, test_case_count)
            self.finalize_test_case(test_case, test_suite, output_paths.test_cases, test_case_count)
            test_case_count += 1

            logger.debug("Beginning test case teardown.")
            teardown_strategy(test_case.driver, self.configuration["adb_path"])

            test_suite_end_time = time.time()
            test_suite_duration = int(test_suite_end_time - test_suite.creation_time)

        print("Test suite generation took {} seconds.".format(test_suite_duration))

    def finalize_test_case(self, test_case, test_suite, path_to_test_cases, test_case_count):
        end_time = time.time()
        test_case_duration = int(end_time - test_case.start_time)
        add_test_case(self.db_connection, generate_test_case_hash(test_case.events), test_suite.id, end_time,
                      test_case_duration)
        test_case_path = write_test_case_to_file(path_to_test_cases, test_case.events, test_case_count,
                                                 test_case_duration)
        logger.debug("Test case {} written to {}.".format(test_case_count, test_case_path))



