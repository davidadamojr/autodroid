import os
import logging
import time
import json
from framework.utils.scripts import *
from framework.database import *
from uuid import uuid4

from appiumatic.abstraction import create_launch_event, create_home_event, synthesize
from appiumatic.execution import Executor
from appiumatic.ui_analysis import get_available_events, get_current_state
from appiumatic.hashing import generate_test_case_hash, generate_event_hash

logger = logging.getLogger(__name__)


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

    logger.debug("Test cases are stored in {}.".format(path_to_test_cases))
    logger.debug("Logs are stored in {}.".format(path_to_logs))
    logger.debug("Coverage files are stored in {}.".format(path_to_coverage))

    return path_to_test_cases, path_to_logs, path_to_coverage


def _write_test_case_to_file(path_to_test_cases, test_case, test_case_count, test_case_duration):
    test_case_count = str(test_case_count).zfill(3)
    test_case_path = os.path.join(path_to_test_cases, "tc{}_{}.json".format(test_case_count, test_case_duration))
    test_case_data = {
        "events": test_case,
        "length": len(test_case)
    }

    with open(test_case_path, 'w') as test_case_file:
        json.dump(test_case_data, test_case_file, sort_keys=True)

    return test_case_path


def remove_termination_events(db_connection, test_suite_id, events):
    non_termination_events = []
    for event in events:
        event_hash = generate_event_hash(event)
        if is_termination_event(db_connection, test_suite_id, event_hash):
            logger.debug("Removing termination event {}".format(event_hash))
            continue

        non_termination_events.append(event)

    return non_termination_events


# TODO: refactor into Generator class, reduce method sizes
def construct_test_suite(db_connection, configuration, setup, event_selection_strategy, termination_criterion,
                         completion_criterion, teardown):
    test_suite_id = uuid4().hex
    test_suite_creation_time = int(time.time())

    add_test_suite(db_connection, test_suite_id, test_suite_creation_time)

    # create output directories
    apk_package_name = configuration["apk_package_name"]
    logger.debug("APK package name is {}".format(apk_package_name))
    output_path = configuration["output_path"]
    logger.debug("Output path is {}".format(output_path))
    path_to_test_cases, path_to_logs, path_to_coverage = _create_output_directories(output_path,
                                                                                    apk_package_name,
                                                                                    test_suite_creation_time)

    test_case_count = 0
    test_suite_duration = 0
    while not completion_criterion(test_duration=test_suite_duration, test_case_count=test_case_count):
        event_count = 0
        test_case = []

        apk_path = configuration["apk_path"]
        adb_path = configuration["adb_path"]
        logger.debug("Path to APK is {}".format(apk_path))
        driver = setup(apk_path, adb_path)

        test_case_start_time = time.time()
        logger.debug("Generating test case {}. Start time is {}.".format(test_case_count+1, test_case_start_time))

        launch_event = create_launch_event()
        current_state = get_current_state(driver)  # error handling here
        complete_event = synthesize(launch_event, current_state)
        test_case.append(complete_event)
        event_count += 1

        executor = Executor(driver, configuration["event_interval"], configuration["text_entry_values"])
        logger.debug("Test case setup complete.")

        try:
            while not termination_criterion(db_connection, test_case_hash=generate_test_case_hash(test_case),
                                            event_count=event_count, test_suite_id=test_suite_id):

                partial_events = get_available_events(driver)
                non_termination_events = remove_termination_events(db_connection, test_suite_id, partial_events)
                selected_event = event_selection_strategy(db_connection, non_termination_events, test_suite_id=test_suite_id)
                executor.execute(selected_event)
                current_state = get_current_state(driver)
                complete_event = synthesize(selected_event, current_state)
                event_hash = generate_event_hash(complete_event)
                update_event_frequency(db_connection, test_suite_id, event_hash)
                test_case.append(complete_event)

                event_count += 1

                # end the test case if event explores beyond boundary of the application under test
                current_package = driver.current_package
                if current_package != apk_package_name:
                    add_termination_event(db_connection, event_hash, test_suite_id)
                    break
        except Exception as e:
            print(e)
            continue  # start a new test case

        # always end test cases by clicking the home event, but do not add the event to the test case
        home_event = create_home_event(current_state)
        executor.execute(home_event)

        # try:
        # collect coverage
        coverage_file_path = configuration["coverage_file_path"] + "/coverage.ec"
        coverage_file_name = "coverage{}.ec".format(str(test_case_count+1).zfill(3))
        coverage_broadcast = configuration["coverage_broadcast"]
        get_coverage(adb_path, coverage_file_path, path_to_coverage, coverage_file_name, coverage_broadcast)

        # write logs
        log_file_name = "log{}.txt".format(str(test_case_count+1).zfill(3))
        log_file_path = os.path.join(path_to_logs, log_file_name)
        apk_package_name = configuration["apk_package_name"]
        app_process_id = get_process_id(adb_path, apk_package_name)
        get_logs(adb_path, log_file_path, app_process_id)
        # except subprocess.CalledProcessError as cp_error:
        #     print(cp_error)
        #     continue  # start a new test case

        end_time = time.time()
        test_case_duration = int(end_time - test_case_start_time)
        test_suite_duration = int(end_time - test_suite_creation_time)

        add_test_case(db_connection, generate_test_case_hash(test_case), test_suite_id, test_suite_creation_time,
                      test_suite_duration)

        test_case_count += 1

        # write test case to file
        test_case_path = _write_test_case_to_file(path_to_test_cases, test_case, test_case_count, test_case_duration)
        logger.debug("Test case {} written to {}.".format(test_case_count, test_case_path))

        logger.debug("Beginning test case teardown.")
        teardown(driver, adb_path)



