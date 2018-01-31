import os
import logging
import time
import json
from framework import database
from uuid import uuid4

from appiumatic.abstraction import create_launch_event, create_home_event, create_state, synthesize
from appiumatic.execution import execute
from appiumatic.ui_analysis import get_available_events, get_current_state


def _create_output_directories(output_path, apk_package_name, test_suite_creation_time):
    output_path = os.path.join(output_path, "{}_{}".format(apk_package_name, str(test_suite_creation_time)))
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    path_to_test_cases = os.path.join(output_path, "testcases")
    if not os.path.exists(path_to_test_cases):
        os.makedirs(path_to_test_cases)

    path_to_logs = os.path.join(output_path, "logs")
    if not os.path.exists(path_to_logs):
        os.makedirs(path_to_logs)

    path_to_coverage = os.path.join(output_path, "coverage")
    if not os.path.exists(path_to_coverage):
        os.makedirs(path_to_coverage)

    return path_to_test_cases, path_to_logs, path_to_coverage


def write_test_case_to_file(path_to_test_cases, test_case, test_case_count, test_case_duration):
    test_case_path = os.path.join(path_to_test_cases, "tc{}_{}.json".format(test_case_count, test_case_duration))
    test_case_data = {
        "events": test_case,
        "length": len(test_case)
    }

    with open(test_case_path, 'w') as test_case_file:
        json.dump(test_case_data, test_case_file)



def construct_test_suite(db_connection, aut_info, setup, event_selection_strategy, termination_criterion,
                         completion_criterion, teardown):
    logger = logging.getLogger(__name__)

    test_suite_id = uuid4().hex
    test_suite_creation_time = int(time.time())
    logger.info("Test generation started at {}.".format(str(test_suite_creation_time))) # TODO: change to human-readable time
    database.add_test_suite(db_connection, test_suite_id, test_suite_creation_time)
    logger.info("Creating test suite with id {}".format(str(test_suite_id)))

    # create output directories
    apk_package_name = aut_info["apk_package_name"]
    path_to_test_cases, path_to_logs, path_to_coverage = _create_output_directories(apk_package_name)
    logger.debug("Test cases are stored in {}.".format(path_to_test_cases))
    logger.debug("Logs are stored in {}.".format(path_to_logs))
    logger.debug("Coverage files are stored in {}.".format(path_to_coverage))

    test_case_count = 0
    test_suite_duration = 0
    test_suite = []
    while not completion_criterion(test_duration=test_suite_duration, test_case_count=test_case_count):
        event_count = 0
        test_case = []
        try:
            apk_path = aut_info["apk_path"]
            driver = setup(apk_path)
        except ConnectionRefusedError as connection_refused:
            logger.error("Could not connect to appium server: %s".format(connection_refused))
            raise ConnectionRefusedError

        start_time = time.time()
        pre_launch_state = create_state(None, None)
        launch_event = create_launch_event(pre_launch_state)
        current_state = get_current_state(driver) # error handling here
        complete_event = synthesize(launch_event, current_state)
        test_case.append(complete_event)
        event_count += 1

        logger.debug("Test case setup complete.")

        while not termination_criterion(event_count=event_count):
            try:
                partial_events = get_available_events(driver) # error handling here
                selected_event = event_selection_strategy(db_connection, partial_events)
                execute(selected_event, driver)
                current_state = get_current_state(driver)
                complete_event = synthesize(selected_event, current_state)
                test_case.append(complete_event)

                event_count += 1
            except Exception as e:
                print(e)
                break # discard the test case

        # always end test cases by clicking the home event, but do not add the event to the test case
        home_event = create_home_event(current_state)
        execute(home_event, driver)

        end_time = time.time()
        test_case_duration = end_time - start_time
        test_suite_duration = end_time - test_suite_creation_time
        test_case_count += 1

        test_suite.append(test_case)

        # write test case to file
        write_test_case_to_file(path_to_test_cases, test_case, test_case_count, test_case_duration)

        # collect coverage

        # write logs

        logger.debug("Beginning test case teardown.")
        teardown(driver)



